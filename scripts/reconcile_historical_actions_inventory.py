#!/usr/bin/env python3
"""Offline reconciliation of owner-exported GitHub Actions artifact/run METADATA.

No ZIP contents, API calls, or secrets are accessed. Untrusted artifact names,
URLs and commit SHA values are never emitted on stdout. A metadata summary
is NOT evidence that historical credential exposure is absent.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "specs/github-actions-artifact-policy.json"
CUTOFF = "2026-11-22T12:24:44Z"  # PR #29 merge UTC; time alone cannot prove safety.
MAX_INPUT_BYTES = 64 * 1024 * 1024
MAX_ROWS = 200_000


def timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone(timezone.utc) if parsed.tzinfo else None


def read_private_ndjson(path: Path, *, kind: str) -> list[dict]:
    if path.is_symlink() or not path.is_file():
        raise ValueError("input_not_regular_file")
    st = path.stat()
    if st.st_size > MAX_INPUT_BYTES or stat.S_IMODE(st.st_mode) & 0o077:
        raise ValueError("input_must_be_private_and_bounded")
    rows: list[dict] = []
    ids: set[int] = set()
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            if len(rows) >= MAX_ROWS:
                raise ValueError("input_row_count_limit")
            row = json.loads(line)
            if not isinstance(row, dict) or type(row.get("id")) is not int or row["id"] <= 0:
                raise ValueError("invalid_metadata_id")
            if row["id"] in ids:
                raise ValueError("duplicate_metadata_id")
            ids.add(row["id"])
            if kind == "runs" and (not isinstance(row.get("path"), str) or
                                     not isinstance(row.get("head_sha"), str) or
                                     timestamp(row.get("created_at")) is None):
                raise ValueError("invalid_run_metadata")
            if kind == "artifacts" and (type(row.get("size_in_bytes")) is not int or
                                          row["size_in_bytes"] < 0 or
                                          timestamp(row.get("created_at")) is None or
                                          type(row.get("expired")) is not bool):
                raise ValueError("invalid_artifact_metadata")
            rows.append(row)
    return rows


def reconcile(artifacts: list[dict], runs: list[dict], producer_names: set[str]) -> dict:
    if len(producer_names) != 16:
        raise ValueError("producer_policy_count_not_reviewed")
    run_by_id = {r["id"]: r for r in runs}
    if len(run_by_id) != len(runs):
        raise ValueError("duplicate_run_id")
    cutoff = timestamp(CUTOFF)
    queue = []
    findings = Counter()
    for artifact in artifacts:
        wf = artifact.get("workflow_run")
        rid = wf.get("id") if isinstance(wf, dict) else None
        run = run_by_id.get(rid) if type(rid) is int else None
        workflow_path = run.get("path") if run else None
        producer = (workflow_path.rsplit("/", 1)[-1] if
                    isinstance(workflow_path, str) and workflow_path.startswith(".github/workflows/")
                    else None)
        recognized = producer in producer_names
        if not run:
            category = "UNMAPPED_RUN_RESTRICTED_REVIEW"
        elif not recognized:
            category = "NON_PRODUCER_OR_UNKNOWN_WORKFLOW_REVIEW"
        elif (timestamp(artifact["created_at"]) < cutoff or
              timestamp(run["created_at"]) < cutoff):
            category = "PRE_GUARD_HISTORICAL_CANDIDATE"
        else:
            # Branches or reruns may still execute an unguarded old source revision.
            category = "AFTER_CUTOFF_GUARD_NOT_VERIFIED"
        findings[category] += 1
        queue.append({
            "artifact_id": artifact["id"],
            "run_id": rid if type(rid) is int else None,
            "producer_workflow": producer if recognized else None,
            "artifact_size_bytes": artifact["size_in_bytes"],
            "created_at": artifact["created_at"],
            "expires_at": artifact.get("expires_at") if timestamp(artifact.get("expires_at")) else None,
            "expired_at_query": artifact["expired"],
            "classification": category,
            "content_inspected": False,
            "access_exposure_verified": False,
            "review_decision": "RESTRICTED_REVIEW_REQUIRED",
        })
    producer_runs = Counter(r["path"].split("/")[-1] for r in runs
                            if r["path"].startswith(".github/workflows/") and
                            r["path"].split("/")[-1] in producer_names)
    return {
        "schema": "github-actions-historical-metadata-reconciliation/v1",
        "cutoff_utc": CUTOFF,
        "artifact_records": len(artifacts),
        "workflow_run_records": len(runs),
        "recognized_producer_count": len(producer_names),
        "producer_workflows_seen_in_run_export": sum(bool(producer_runs[n]) for n in producer_names),
        "producer_workflows_missing_run_export": sorted(n for n in producer_names if not producer_runs[n]),
        "class_counts": dict(sorted(findings.items())),
        "artifact_content_inspected": False,
        "historical_full_inventory_verified": False,
        "historical_exposure_status": "UNKNOWN",
        "independent_review_verified": False,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "review_queue": sorted(queue, key=lambda x: x["artifact_id"]),
    }


def create_private_report(report: dict, output: Path, input_paths: tuple[Path, ...]) -> None:
    target = output.absolute()
    if (any(target.resolve() == p.resolve() for p in input_paths) or
            target.resolve().is_relative_to(ROOT.resolve())):
        raise ValueError("report_path_must_be_separate_from_inputs_and_repo")
    parent = target.parent
    if (not parent.is_dir() or parent.is_symlink() or
            stat.S_IMODE(parent.stat().st_mode) & 0o077):
        raise ValueError("report_parent_must_be_private_directory")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(target, flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--artifacts", type=Path, required=True)
    p.add_argument("--runs", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
        producer_names = set(policy["workflow_paths"])
        a = read_private_ndjson(args.artifacts, kind="artifacts")
        r = read_private_ndjson(args.runs, kind="runs")
        result = reconcile(a, r, producer_names)
        create_private_report(result, args.report, (args.artifacts, args.runs))
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "METADATA_RECONCILIATION_BLOCKED", "reason_class": type(exc).__name__,
                          "release_decision": "NO_GO"}, sort_keys=True))
        return 2
    print(json.dumps({"status": "METADATA_RECONCILED_RESTRICTED_REVIEW_REQUIRED",
                      "artifact_records": result["artifact_records"],
                      "workflow_run_records": result["workflow_run_records"],
                      "class_counts": result["class_counts"],
                      "historical_exposure_status": "UNKNOWN",
                      "release_decision": "NO_GO"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
