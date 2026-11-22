#!/usr/bin/env python3
"""Issue #30: offline crosswalk of owner-exported job/run metadata and local log triage.

Uses previously restricted inputs only. No HTTP, job log downloads, log body
inspection or live tests. A matching job ID/hash is NOT a signature,
confidentiality clearance or proof that the exported historical set is complete.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import stat

from reconcile_historical_actions_inventory import (
    CUTOFF, POLICY, ROOT, create_private_report, read_private_ndjson, timestamp,
)
from triage_historical_actions_job_logs import SCHEMA as TRIAGE_SCHEMA

SCHEMA = "historical-actions-job-log-coverage/v1"
HEX_SHA = re.compile(r"[0-9a-f]{40}\Z")
HEX_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
MAX_REPORT_BYTES = 32 * 1024 * 1024
MAX_JOBS = 200_000


def ensure_private_input(path: Path) -> None:
    if (path.is_symlink() or not path.is_file()
            or path.resolve().is_relative_to(ROOT.resolve())
            or not path.parent.is_dir() or path.parent.is_symlink()
            or stat.S_IMODE(path.parent.stat().st_mode) & 0o077):
        raise ValueError("owner_input_file_or_parent_not_private")
    st = path.stat()
    if (not stat.S_ISREG(st.st_mode) or st.st_nlink != 1
            or stat.S_IMODE(st.st_mode) & 0o077):
        raise ValueError("owner_input_requires_private_regular_file")


def read_triage(path: Path) -> dict:
    ensure_private_input(path)
    if path.stat().st_size > MAX_REPORT_BYTES:
        raise ValueError("triage_report_too_large")
    doc = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(doc, dict)
            or doc.get("schema") != TRIAGE_SCHEMA
            or doc.get("scope") != "OWNER_SUPPLIED_RESTRICTED_JOB_LOGS_ONLY"
            or doc.get("historical_full_job_log_inventory_verified") is not False
            or doc.get("log_access_exposure_verified") is not False
            or doc.get("historical_exposure_status") != "UNKNOWN"
            or doc.get("independent_security_review_signed") is not False
            or doc.get("azure_live_accepted") != 0
            or doc.get("release_decision") != "NO_GO"):
        raise ValueError("triage_source_not_pending_manual_review")
    rows = doc.get("logs")
    if (not isinstance(rows, list)
            or not rows or len(rows) > 5000
            or type(doc.get("job_log_files_present")) is not int
            or doc["job_log_files_present"] != len(rows)
            or type(doc.get("job_logs_content_examined")) is not int):
        raise ValueError("triage_member_count_invalid")
    seen: set[int] = set()
    checked = 0
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("triage_row_invalid")
        ident, digest = row.get("job_id"), row.get("log_sha256")
        if type(ident) is not int or ident <= 0 or ident in seen:
            raise ValueError("triage_job_id_duplicate_or_invalid")
        seen.add(ident)
        if digest is not None and (not isinstance(digest, str) or not HEX_DIGEST.fullmatch(digest)):
            raise ValueError("triage_log_digest_invalid")
        if type(row.get("log_bytes")) is not int or row["log_bytes"] < 0:
            raise ValueError("triage_log_size_invalid")
        if row.get("decision") not in (
            "MANUAL_REVIEW_REQUIRED", "INDICATORS_PRESENT_RESTRICTED_REVIEW_REQUIRED"
        ):
            raise ValueError("triage_decision_not_pending")
        indicators = row.get("indicators")
        if (not isinstance(indicators, list)
                or any(not isinstance(x, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,80}", x)
                       for x in indicators)):
            raise ValueError("triage_indicators_invalid")
        if digest is None and "log_size_limit_unexamined" not in indicators:
            raise ValueError("triage_missing_digest_without_unexamined_indicator")
        checked += digest is not None
    if doc["job_logs_content_examined"] != checked:
        raise ValueError("triage_content_count_drift")
    return doc


def link(jobs: list[dict], runs: list[dict], triage: dict,
         producer_workflows: set[str]) -> dict:
    if len(producer_workflows) != 16 or len(jobs) > MAX_JOBS or not jobs or not runs:
        raise ValueError("incomplete_or_unapproved_owner_metadata_scope")
    by_run = {}
    for run in runs:
        ident = run.get("id")
        if (type(ident) is not int or ident <= 0 or ident in by_run
                or timestamp(run.get("created_at")) is None
                or not isinstance(run.get("path"), str)
                or not isinstance(run.get("head_sha"), str)
                or not HEX_SHA.fullmatch(run["head_sha"].lower())):
            raise ValueError("run_metadata_id_scope_or_sha_invalid")
        by_run[ident] = run
    local = {row["job_id"]: row for row in triage["logs"]}
    classified = Counter()
    cover = Counter()
    rows = []
    seen_jobs = set()
    cutoff = timestamp(CUTOFF)
    for job in jobs:
        if not isinstance(job, dict):
            raise ValueError("job_metadata_row_not_object")
        jid, rid, attempt = (job.get(k) for k in ("id", "run_id", "run_attempt"))
        if (type(jid) is not int or jid <= 0 or jid in seen_jobs
                or type(rid) is not int or rid <= 0
                or type(attempt) is not int or attempt <= 0
                or not isinstance(job.get("head_sha"), str)
                or not HEX_SHA.fullmatch(job["head_sha"].lower())):
            raise ValueError("job_metadata_identifiers_invalid")
        seen_jobs.add(jid)
        run = by_run.get(rid)
        workflow = run.get("path") if run else None
        name = workflow[len(".github/workflows/"):] if (
            isinstance(workflow, str) and workflow.startswith(".github/workflows/")
            and "/" not in workflow[len(".github/workflows/"):]
        ) else None
        if run is None:
            classification = "UNMAPPED_RUN_REVIEW_REQUIRED"
        elif name not in producer_workflows:
            classification = "UNRECOGNIZED_WORKFLOW_REVIEW_REQUIRED"
        elif job["head_sha"].lower() != run["head_sha"].lower():
            classification = "RUN_JOB_COMMIT_MISMATCH_REVIEW_REQUIRED"
        elif timestamp(run["created_at"]) < cutoff:
            classification = "PRE_GUARD_OR_OLD_SOURCE_REVIEW_REQUIRED"
        else:
            classification = "POST_CUTOFF_SOURCE_NOT_VERIFIED"
        classified[classification] += 1
        local_row = local.get(jid)
        if local_row is None:
            state = "LOCAL_JOB_LOG_MISSING_OR_NOT_COLLECTED"
        elif local_row["log_sha256"] is None:
            state = "LOCAL_LOG_UNEXAMINED_SIZE_OR_FORMAT"
        else:
            state = "LOCAL_LOG_HEURISTIC_SCAN_ONLY"
        cover[state] += 1
        rows.append({
            "job_id": jid,
            "run_id": rid,
            "run_attempt": attempt,
            "producer": name if name in producer_workflows else None,
            "metadata_classification": classification,
            "local_log_state": state,
            "log_sha256_from_unverified_owner_report": (
                local_row["log_sha256"] if local_row else None
            ),
            "original_job_log_content_signed": False,
            "log_access_exposure_verified": False,
            "owner_and_independent_reviewer_signed": False,
            "incident_review_decision": "RESTRICTED_REVIEW_REQUIRED",
        })
    extra = sorted(set(local) - seen_jobs)
    for jid in extra:
        row = local[jid]
        rows.append({
            "job_id": jid, "run_id": None, "run_attempt": None,
            "producer": None,
            "metadata_classification": "LOCAL_LOG_WITHOUT_EXPORTED_JOB_METADATA",
            "local_log_state": ("LOCAL_LOG_HEURISTIC_SCAN_ONLY" if row["log_sha256"] is not None
                                else "LOCAL_LOG_UNEXAMINED_SIZE_OR_FORMAT"),
            "log_sha256_from_unverified_owner_report": row["log_sha256"],
            "original_job_log_content_signed": False,
            "log_access_exposure_verified": False,
            "owner_and_independent_reviewer_signed": False,
            "incident_review_decision": "RESTRICTED_REVIEW_REQUIRED",
        })
    if extra:
        classified["LOCAL_LOG_WITHOUT_EXPORTED_JOB_METADATA"] += len(extra)
        cover["LOCAL_LOG_NOT_IN_JOB_METADATA"] += len(extra)
    return {
        "schema": SCHEMA,
        "status": "JOB_LOG_COVERAGE_RECONCILED_RESTRICTED_REVIEW_REQUIRED",
        "scope": "OWNER_EXPORTED_METADATA_AND_OWNER_TRIAGE_REPORT_ONLY",
        "jobs_in_metadata": len(jobs),
        "runs_in_metadata": len(runs),
        "local_logs_in_triage_report": len(local),
        "local_logs_not_in_job_metadata": len(extra),
        "missing_or_unexamined_for_exported_jobs": (
            cover["LOCAL_JOB_LOG_MISSING_OR_NOT_COLLECTED"]
            + cover["LOCAL_LOG_UNEXAMINED_SIZE_OR_FORMAT"]
        ),
        "classification_counts": dict(sorted(classified.items())),
        "local_coverage_counts": dict(sorted(cover.items())),
        "owner_exported_set_completeness_verified": False,
        "historical_full_job_log_inventory_verified": False,
        "job_log_content_independently_verified": False,
        "log_access_exposure_verified": False,
        "run_source_security_guard_verified": False,
        "independent_security_review_signed": False,
        "historical_exposure_status": "UNKNOWN",
        "azure_live_accepted": 0,
        "release_decision": "NO_GO",
        "review_queue": sorted(rows, key=lambda r: r["job_id"]),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jobs", type=Path, required=True)
    p.add_argument("--runs", type=Path, required=True)
    p.add_argument("--triage-report", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        for path in (args.jobs, args.runs, args.triage_report):
            ensure_private_input(path)
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
        names = set(policy["workflow_paths"])
        triage = read_triage(args.triage_report)
        jobs = read_private_ndjson(args.jobs, kind="jobs")
        runs = read_private_ndjson(args.runs, kind="runs")
        report = link(jobs, runs, triage, names)
        create_private_report(report, args.report,
                              (args.jobs, args.runs, args.triage_report))
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "JOB_LOG_COVERAGE_BLOCKED",
                          "error_class": type(exc).__name__,
                          "historical_exposure_status": "UNKNOWN",
                          "release_decision": "NO_GO"}, sort_keys=True))
        return 2
    # No numeric job/run IDs, names, SHAs, full paths or user input echoed.
    print(json.dumps({
        "status": report["status"],
        "jobs_in_metadata": report["jobs_in_metadata"],
        "local_logs_in_triage_report": report["local_logs_in_triage_report"],
        "missing_or_unexamined_for_exported_jobs":
            report["missing_or_unexamined_for_exported_jobs"],
        "classification_counts": report["classification_counts"],
        "historical_exposure_status": "UNKNOWN",
        "release_decision": "NO_GO",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
