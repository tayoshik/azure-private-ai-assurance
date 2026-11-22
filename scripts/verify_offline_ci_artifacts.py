#!/usr/bin/env python3
"""Pre-upload allowlist and high-confidence credential guard for OFFLINE CI outputs.

This is a preventive, fail-closed heuristic and NOT an infallible DLP engine.
Do not upload any raw Azure state, plan, real cloud evidence or personal data.
Never log artifact contents: only approved relative names, sizes and SHA-256.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = "specs/github-actions-artifact-policy.json"
EXPECTED_SCHEMA = "github-actions-offline-artifacts/v1"
EXPECTED_RETENTION = 14
EXPECTED_WORKFLOW_COUNT = 16
EXPECTED_FILES = 69

# High-confidence signatures, not a complete guarantee against secrets/PII.
# Use bounded fixed signatures, not generic 'token'/'secret' words in audit JSON.
BLOCKED_CONTENT = {
    "private-key": re.compile(rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----", re.I),
    "github-token": re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{30,})\b"),
    "aws-access-key": re.compile(rb"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "authorization-credential": re.compile(rb"\bAuthorization\s*[:=]\s*['\"]?(?:Bearer|Basic)\s+[A-Za-z0-9._~+/\-=]{16,}", re.I),
    "jwt": re.compile(rb"\beyJhbGciOi[A-Za-z0-9_-]{30,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "storage-key": re.compile(rb"\b(?:AccountKey|SharedAccessSignature)\s*=\s*[A-Za-z0-9+/=%_-]{24,}", re.I),
    "sas-signature": re.compile(rb"[?&]sig=[A-Za-z0-9%+/_=-]{24,}", re.I),
    "long-credential-field": re.compile(
        rb"""(?i)["'](?:client_secret|refresh_token|access_token|api_key|password)["']\s*:\s*["'][A-Za-z0-9.+/=_-]{24,}["']"""
    ),
}
ALLOWED_EXTENSIONS = frozenset({".json", ".txt", ".log"})


def _safe_path(rel: str) -> bool:
    if not isinstance(rel, str):
        return False
    path = PurePosixPath(rel)
    return bool(
        isinstance(rel, str) and rel and "\\" not in rel and
        not path.is_absolute() and len(rel) <= 160 and
        all(part not in ("", ".", "..") and not part.startswith(".") for part in path.parts) and
        path.suffix.lower() in ALLOWED_EXTENSIONS and
        str(path) == rel and
        not re.search(r"[\x00-\x1f]", rel)
    )


def load_policy(repo_root: Path = ROOT) -> dict:
    try:
        policy = json.loads((repo_root / POLICY_PATH).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise ValueError("artifact policy absent or invalid") from exc
    if not isinstance(policy, dict) or any((
        policy.get("schema") != EXPECTED_SCHEMA,
        type(policy.get("retention_days")) is not int or policy["retention_days"] != EXPECTED_RETENTION,
        type(policy.get("allowed_file_bytes")) is not int or policy["allowed_file_bytes"] != 8_388_608,
        type(policy.get("allowed_total_bytes")) is not int or policy["allowed_total_bytes"] != 16_777_216,
        policy.get("release_decision") != "NO_GO",
        policy.get("azure_live_passes") != 0,
    )):
        raise ValueError("artifact policy metadata differs from reviewed security baseline")
    mapping = policy.get("workflow_paths")
    if not isinstance(mapping, dict) or len(mapping) != EXPECTED_WORKFLOW_COUNT:
        raise ValueError("artifact policy workflow inventory drift")
    count = 0
    for workflow, approved in mapping.items():
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.yml", workflow):
            raise ValueError("unsafe workflow policy key")
        if not isinstance(approved, list) or not approved:
            raise ValueError("empty workflow artifact allowlist")
        if approved != sorted(set(approved)) or not all(_safe_path(x) for x in approved):
            raise ValueError("unsafe, duplicate or unsorted permitted artifact paths")
        count += len(approved)
    if count != EXPECTED_FILES:
        raise ValueError("approved artifact path count changed without security review")
    return policy


def scan(workflow: str, root: Path, repo_root: Path = ROOT,
         stage: Path | None = None) -> dict:
    """Return sanitized metadata; fail closed without printing evidence contents."""
    policy = load_policy(repo_root)
    allowed = policy["workflow_paths"].get(workflow)
    if allowed is None:
        raise ValueError("workflow has no approved offline artifact policy")
    if root.is_symlink():
        raise ValueError("artifact root must not be a symlink")
    if not root.exists():
        return {
            "classification": "SAFE_EMPTY_NO_ARTIFACT_DIR",
            "workflow": workflow,
            "files": [],
            "file_count": 0,
            "total_bytes": 0,
            "network_requests": 0,
            "azure_live_passes": 0,
            "release_decision": "NO_GO",
        }
    if not root.is_dir():
        raise ValueError("artifact root is not a directory")
    if stage is not None and (stage.name != "artifacts-reviewed" or
                              stage.parent.resolve() != root.parent.resolve() or
                              stage.exists() or stage.is_symlink()):
        raise ValueError("isolated reviewed-artifact staging directory must be new and a sibling")
    approved = set(allowed)
    found = []
    accepted_bytes: list[tuple[str, bytes]] = []
    total = 0
    for base, dirs, files in os.walk(root, followlinks=False):
        parent = Path(base)
        for name in dirs:
            path = parent / name
            if not stat.S_ISDIR(path.lstat().st_mode) or path.is_symlink():
                raise ValueError("artifact subdirectory is not a plain directory")
        for name in files:
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if relative not in approved or not _safe_path(relative):
                raise ValueError("unapproved artifact file path: " + relative)
            metadata = path.lstat()
            if not stat.S_ISREG(metadata.st_mode) or path.is_symlink():
                raise ValueError("artifact is not a regular file: " + relative)
            if metadata.st_size > policy["allowed_file_bytes"]:
                raise ValueError("artifact file is too large: " + relative)
            total += metadata.st_size
            if total > policy["allowed_total_bytes"]:
                raise ValueError("artifact total size exceeds reviewed limit")
            raw = path.read_bytes()
            if len(raw) != metadata.st_size:
                raise ValueError("artifact changed while being scanned: " + relative)
            try:
                raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError("artifact must contain UTF-8 text: " + relative) from exc
            for signature, pattern in BLOCKED_CONTENT.items():
                if pattern.search(raw):
                    raise ValueError(
                        "artifact credential signature blocked (" + signature + "): " + relative)
            accepted_bytes.append((relative, raw))
            found.append({
                "path": relative,
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            })
    if stage is not None and accepted_bytes:
        # Upload only the independently checked byte snapshot, never the original
        # writable artifacts directory. Failed validation creates no upload.
        stage.mkdir(mode=0o700)
        for relative, raw in accepted_bytes:
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            with target.open("xb") as out:
                out.write(raw)
            target.chmod(0o600)
    return {
        "classification": "OFFLINE_ARTIFACT_PREFLIGHT_PASS" if found else "SAFE_EMPTY_ARTIFACT_DIR",
        "workflow": workflow,
        "files": sorted(found, key=lambda row: row["path"]),
        "file_count": len(found),
        "total_bytes": total,
        "network_requests": 0,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--root", type=Path, default=Path("artifacts"))
    parser.add_argument("--stage", type=Path)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        result = scan(args.workflow, args.root, args.repo_root, args.stage)
    except (OSError, ValueError) as exc:
        # Do not include the contents of untrusted files in logs.
        print(json.dumps({"classification": "BLOCKED_ARTIFACT_UPLOAD",
                          "reason": str(exc),
                          "azure_live_passes": 0,
                          "release_decision": "NO_GO"}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
