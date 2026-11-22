#!/usr/bin/env python3
"""Local-only, conservative historical GitHub Actions ZIP triage.

Never uploads, extracts, executes, clears or deletes evidence. No raw names, URLs,
contents, or matched secret values appear in the report. A clean heuristic scan is
NOT a confidentiality assessment. Use an encrypted, access-restricted workstation.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

from verify_offline_ci_artifacts import BLOCKED_CONTENT

REPO_ROOT = Path(__file__).resolve().parents[1]
MAX_ARCHIVES = 5000
MAX_ARCHIVE_BYTES = 64 * 1024 * 1024
MAX_MEMBERS = 2000
MAX_MEMBER_BYTES = 8 * 1024 * 1024
MAX_UNCOMPRESSED_BYTES = 32 * 1024 * 1024
MAX_RATIO = 200
SENSITIVE_EXTENSIONS = frozenset({
    ".tfstate", ".tfplan", ".pem", ".pfx", ".p12", ".key", ".kdbx",
    ".zip", ".tar", ".gz", ".7z", ".db", ".sqlite", ".sqlite3",
})
SENSITIVE_NAME = re.compile(r"(?i)(?:^|[/._-])(?:\.env|credentials|private|secret|token|keyvault)(?:$|[/._-])")


def name_digest(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8", errors="surrogatepass")).hexdigest()


def invalid_member_name(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(
        not name or len(name) > 256 or "\\" in name or "\x00" in name or
        re.search(r"[\x01-\x1f\x7f]", name) or name.startswith("/") or
        p.is_absolute() or bool(re.match(r"^[A-Za-z]:", name)) or
        any(x in (".", "..") for x in name.split("/")) or
        "//" in name or p.parts == () or ".." in p.parts
    )


def _archive_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fd:
        for block in iter(lambda: fd.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inspect_archive(path: Path) -> dict:
    """Returns redacted indicators; never reveals ZIP filenames or member names."""
    if path.is_symlink() or not path.is_file():
        raise ValueError("archive_path_not_plain_file")
    if path.suffix.lower() != ".zip":
        raise ValueError("archive_extension_not_zip")
    st = path.stat()
    flags: set[str] = set()
    result = {
        "archive_name_sha256": name_digest(path.name),
        "archive_bytes": st.st_size,
        "archive_sha256": None,
        "member_count": 0,
        "inspected_content_members": 0,
        "indicators": [],
        "decision": "MANUAL_REVIEW_REQUIRED",
    }
    if st.st_size > MAX_ARCHIVE_BYTES:
        flags.add("archive_size_limit")
    else:
        result["archive_sha256"] = _archive_digest(path)
        try:
            with zipfile.ZipFile(path, "r") as archive:
                members = archive.infolist()
                result["member_count"] = len(members)
                if len(members) > MAX_MEMBERS:
                    flags.add("member_count_limit")
                else:
                    seen: set[str] = set()
                    total = 0
                    for info in members:
                        n = info.filename
                        normalized = n.casefold().rstrip("/")
                        if invalid_member_name(n):
                            flags.add("unsafe_member_path")
                            continue
                        if normalized in seen:
                            flags.add("duplicate_member_name")
                            continue
                        seen.add(normalized)
                        mode = (info.external_attr >> 16) & 0o170000
                        if mode not in (0, stat.S_IFREG, stat.S_IFDIR):
                            flags.add("nonregular_member")
                            continue
                        if info.is_dir():
                            continue
                        if mode == stat.S_IFDIR:
                            flags.add("directory_mode_on_file")
                            continue
                        if info.flag_bits & 1:
                            flags.add("encrypted_member")
                            continue
                        ext = PurePosixPath(n).suffix.lower()
                        if ext in SENSITIVE_EXTENSIONS or SENSITIVE_NAME.search(n):
                            flags.add("sensitive_member_name")
                        if ext in {".zip", ".tar", ".gz", ".7z"}:
                            flags.add("nested_archive_not_inspected")
                        total += info.file_size
                        if (info.file_size > MAX_MEMBER_BYTES or
                                total > MAX_UNCOMPRESSED_BYTES or
                                (info.file_size and info.file_size / max(info.compress_size, 1) > MAX_RATIO)):
                            flags.add("uncompressed_or_ratio_limit")
                            continue
                        try:
                            with archive.open(info, "r") as fd:
                                raw = fd.read(MAX_MEMBER_BYTES + 1)
                            if len(raw) != info.file_size:
                                flags.add("member_size_mismatch")
                                continue
                        except (OSError, RuntimeError, ValueError, zipfile.BadZipFile, EOFError):
                            flags.add("member_read_failure")
                            continue
                        result["inspected_content_members"] += 1
                        if b"\x00" in raw:
                            flags.add("binary_or_nul_content")
                        try:
                            raw.decode("utf-8")
                        except UnicodeDecodeError:
                            flags.add("non_utf8_content")
                        for kind, pattern in BLOCKED_CONTENT.items():
                            if pattern.search(raw):
                                flags.add("credential_signature_" + kind.replace("-", "_"))
        except (OSError, RuntimeError, ValueError, zipfile.BadZipFile, EOFError, NotImplementedError):
            flags.add("unreadable_zip")
    result["indicators"] = sorted(flags)
    if flags:
        result["decision"] = "INDICATORS_PRESENT_RESTRICTED_REVIEW_REQUIRED"
    return result


def scan_directory(folder: Path) -> dict:
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("archive_input_must_be_plain_directory")
    paths = sorted(folder.iterdir())
    if len(paths) > MAX_ARCHIVES:
        raise ValueError("archive_count_limit")
    if any(p.is_symlink() or not p.is_file() or p.suffix.lower() != ".zip" for p in paths):
        raise ValueError("archive_input_contains_non_zip_or_symlink")
    reports = [inspect_archive(p) for p in paths]
    indicators = Counter(kind for report in reports for kind in report["indicators"])
    return {
        "schema": "historical-actions-local-zip-triage/v1",
        "scan_scope": "USER_SUPPLIED_LOCAL_ARCHIVES_ONLY",
        "archives_inspected": len(reports),
        "indicator_counts": dict(sorted(indicators.items())),
        "archives_requiring_restricted_review": len(reports),
        "no_secret_exposure_assurance": True,
        "complete_historical_inventory_verified": False,
        "artifact_access_review_verified": False,
        "azure_live_accepted": 0,
        "release_decision": "NO_GO",
        "archives": reports,
    }


def write_private_report(report: dict, path: Path, folder: Path) -> None:
    target = path.absolute()
    root = REPO_ROOT.resolve()
    if (target.resolve().is_relative_to(root) or
            target.resolve().is_relative_to(folder.resolve())):
        raise ValueError("report_must_be_outside_repository_and_archive_input")
    parent = target.parent
    if not parent.is_dir() or parent.is_symlink() or (parent.stat().st_mode & 0o077):
        raise ValueError("report_directory_must_exist_and_be_mode_0700")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(target, flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, indent=2, sort_keys=True)
        out.write("\n")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = scan_directory(args.archive_dir)
        write_private_report(report, args.report, args.archive_dir)
    except (OSError, ValueError) as exc:
        # Error *types*, not untrusted paths/content. Avoid print(exc).
        print(json.dumps({"status": "LOCAL_TRIAGE_BLOCKED", "error_type": type(exc).__name__,
                          "release_decision": "NO_GO"}))
        return 2
    print(json.dumps({"status": "RESTRICTED_MANUAL_REVIEW_REQUIRED",
                      "archives_inspected": report["archives_inspected"],
                      "indicator_counts": report["indicator_counts"],
                      "report_written_privately": True,
                      "release_decision": "NO_GO"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
