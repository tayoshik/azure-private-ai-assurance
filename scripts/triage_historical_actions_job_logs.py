#!/usr/bin/env python3
"""Issue #30: local-only triage of owner-supplied historical Actions JOB logs.

No GitHub API, downloader, shell invocation, network, Azure or secret handling.
Only an approved operator may place real logs in an encrypted restricted
directory. Raw lines, environment variables, paths, token values and matched
text are never included in stdout or the private indicator report. Heuristic
no-match is NOT a confidentiality clearance or evidence of complete coverage.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import stat

from triage_historical_actions_archives import REPO_ROOT, write_private_report
from verify_offline_ci_artifacts import BLOCKED_CONTENT

SCHEMA = "historical-actions-job-log-local-triage/v1"
JOB_FILE = re.compile(r"job-([1-9][0-9]{0,18})\.log\Z")
MAX_JOB_LOGS = 5000
MAX_LOG_BYTES = 16 * 1024 * 1024
MAX_TOTAL_BYTES = 128 * 1024 * 1024

# These additional *heuristic* classes are intentionally conservative;
# absence of a match never certifies an unexposed historical log.
RISK_HINTS = {
    "oidc_token_runtime_marker": re.compile(
        rb"(?i)(?:ACTIONS_ID_TOKEN_REQUEST_(?:TOKEN|URL)|SYSTEM_ACCESSTOKEN)\s*[:=]"
    ),
    "environment_credential_assignment": re.compile(
        rb"(?im)(?:^|[\s>])(?:GH_TOKEN|GITHUB_TOKEN|AZURE_CLIENT_SECRET|ARM_CLIENT_SECRET|"
        rb"AWS_SECRET_ACCESS_KEY|TF_VAR_(?:password|secret|token|api_key))\s*="
    ),
    "github_workflow_command_secret_marker": re.compile(
        rb"(?i)::(?:add-mask|set-output|save-state)::"
    ),
    "terraform_sensitive_state_or_plan_reference": re.compile(
        rb"(?i)(?:\.tfstate(?:\b|[\x22\x27])|\.tfplan(?:\b|[\x22\x27])|terraform\.tfvars(?:\b|[\x22\x27]))"
    ),
    "unmasked_long_secret_field": re.compile(
        rb"(?i)\b(?:client[_-]?secret|refresh[_-]?token|access[_-]?token|password|api[_-]?key)\s*[:=]\s*"
        rb"[\"']?[A-Za-z0-9._~+/=-]{24,}"
    ),
    "shell_xtrace_or_debug": re.compile(rb"(?m)^\s*\+\s+(?:export|env|printenv|set\s+-x|curl|az|terraform)\b"),
    "github_mask_placeholder_unverifiable": re.compile(rb"\*\*\*"),
}


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def private_directory(folder: Path) -> None:
    if (folder.is_symlink() or not folder.is_dir()
            or folder.resolve().is_relative_to(REPO_ROOT.resolve())
            or stat.S_IMODE(folder.stat().st_mode) & 0o077):
        raise ValueError("log_input_must_be_private_directory_outside_repository")


def read_private_job_log(path: Path) -> bytes | None:
    """Open without following final symlinks; return None for oversized files."""
    if path.is_symlink() or not path.is_file():
        raise ValueError("job_log_must_be_regular_file")
    before = path.stat()
    if (not stat.S_ISREG(before.st_mode)
            or stat.S_IMODE(before.st_mode) & 0o077
            or before.st_nlink != 1):
        raise ValueError("job_log_permissions_or_link_count_not_restricted")
    if before.st_size > MAX_LOG_BYTES:
        return None
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as stream:
        st = os.fstat(stream.fileno())
        if (not stat.S_ISREG(st.st_mode)
                or stat.S_IMODE(st.st_mode) & 0o077
                or st.st_nlink != 1
                or st.st_ino != before.st_ino
                or st.st_dev != before.st_dev
                or st.st_size != before.st_size):
            raise ValueError("job_log_changed_or_unsafe_before_read")
        raw = stream.read(MAX_LOG_BYTES + 1)
        after = os.fstat(stream.fileno())
        if (len(raw) != st.st_size or len(raw) > MAX_LOG_BYTES
                or after.st_size != st.st_size
                or after.st_mtime_ns != st.st_mtime_ns):
            raise ValueError("job_log_changed_while_reading")
    return raw


def inspect_log(path: Path) -> dict:
    match = JOB_FILE.fullmatch(path.name)
    if not match:
        raise ValueError("job_log_must_use_numeric_job_ID_name")
    raw = read_private_job_log(path)
    flags: set[str] = set()
    result = {
        "job_id": int(match.group(1)),  # owner-only report; never stdout
        "log_sha256": None,
        "log_bytes": path.stat().st_size,
        "indicators": [],
        "decision": "MANUAL_REVIEW_REQUIRED",
    }
    if raw is None:
        flags.add("log_size_limit_unexamined")
    else:
        result["log_sha256"] = sha256(raw)
        if b"\x00" in raw:
            flags.add("binary_or_nul_log_content")
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError:
            flags.add("non_utf8_log_content")
        for kind, pattern in BLOCKED_CONTENT.items():
            if pattern.search(raw):
                flags.add("credential_signature_" + kind.replace("-", "_"))
        for kind, pattern in RISK_HINTS.items():
            if pattern.search(raw):
                flags.add(kind)
    result["indicators"] = sorted(flags)
    if flags:
        result["decision"] = "INDICATORS_PRESENT_RESTRICTED_REVIEW_REQUIRED"
    return result


def scan_directory(folder: Path) -> dict:
    private_directory(folder)
    files = sorted(folder.iterdir())
    if not files or len(files) > MAX_JOB_LOGS:
        raise ValueError("job_log_count_is_zero_or_exceeds_limit")
    ids = set()
    size = 0
    for f in files:
        match = JOB_FILE.fullmatch(f.name)
        if not match or f.is_symlink() or not f.is_file():
            raise ValueError("job_log_input_contains_unapproved_name_or_nonregular_file")
        ident = int(match.group(1))
        if ident in ids:
            raise ValueError("duplicate_numeric_job_id")
        ids.add(ident)
        st = f.stat()
        if stat.S_IMODE(st.st_mode) & 0o077 or st.st_nlink != 1:
            raise ValueError("job_log_input_not_restricted")
        size += st.st_size
        if size > MAX_TOTAL_BYTES:
            raise ValueError("job_log_total_size_limit")
    rows = [inspect_log(p) for p in files]
    count = Counter(i for r in rows for i in r["indicators"])
    return {
        "schema": SCHEMA,
        "scope": "OWNER_SUPPLIED_RESTRICTED_JOB_LOGS_ONLY",
        "job_log_files_present": len(files),
        "job_logs_content_examined": sum(r["log_sha256"] is not None for r in rows),
        "indicator_counts": dict(sorted(count.items())),
        "jobs_requiring_manual_review": len(files),
        "historical_full_job_log_inventory_verified": False,
        "log_access_exposure_verified": False,
        "artifact_zip_content_verified": False,
        "historical_exposure_status": "UNKNOWN",
        "independent_security_review_signed": False,
        "azure_live_accepted": 0,
        "release_decision": "NO_GO",
        "logs": rows,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--log-dir", required=True, type=Path)
    p.add_argument("--report", required=True, type=Path)
    args = p.parse_args(argv)
    try:
        r = scan_directory(args.log_dir)
        write_private_report(r, args.report, args.log_dir)
    except (OSError, ValueError, UnicodeError) as exc:
        # Report error *type*, never original job IDs, names or log bytes.
        print(json.dumps({"status": "RESTRICTED_LOG_TRIAGE_BLOCKED",
                          "error_type": type(exc).__name__,
                          "historical_exposure_status": "UNKNOWN",
                          "release_decision": "NO_GO"}))
        return 2
    print(json.dumps({
        "status": "RESTRICTED_LOG_MANUAL_REVIEW_REQUIRED",
        "job_log_files_present": r["job_log_files_present"],
        "job_logs_content_examined": r["job_logs_content_examined"],
        "indicator_counts": r["indicator_counts"],
        "historical_exposure_status": "UNKNOWN",
        "release_decision": "NO_GO",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
