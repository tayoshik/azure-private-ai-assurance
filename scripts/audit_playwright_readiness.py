#!/usr/bin/env python3
"""Offline, read-only Playwright *readiness* inventory; NEVER run browser tests.

Coverage: four AZ-T20 configuration references and nine AZ-T64 browser journeys.
A file existing (even a syntactically valid .spec.ts) is not evidence that a
real private app, login, selector or authorized runner exists.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

if __package__:
    from .audit_catalogue_dependencies import audit, path_exists
else:
    from audit_catalogue_dependencies import audit, path_exists

ROOT = Path(__file__).resolve().parents[1]
CONFIG = "tests/playwright.config.ts"
SPEC = "tests/phase6/phase6.spec.ts"
CONFIG_IDS = ("AZ-T20-07", "AZ-T20-09", "AZ-T20-15", "AZ-T20-17")
JOURNEY_IDS = tuple(f"AZ-T64-{n:02}" for n in range(1, 18, 2))
EXPECTED_REFERENCES = {**{x: CONFIG for x in CONFIG_IDS},
                       **{x: SPEC for x in JOURNEY_IDS}}
REQUIREMENTS = {
    "AZ-T20-07": "External Playwright project must use an approved external vantage point",
    "AZ-T20-09": "Internal Playwright project must execute only on an approved private runner",
    "AZ-T20-15": "JUnit reporting must retain sanitized structured evidence",
    "AZ-T20-17": "Traces must have approved retention and sensitive-data handling",
    "AZ-T64-01": "Internal HTTPS response through actual private gateway",
    "AZ-T64-03": "TLS trust, hostname, certificate chain and expiration",
    "AZ-T64-05": "Real, explicitly authorized application sign-in",
    "AZ-T64-07": "Authenticated /healthz status under approved policy",
    "AZ-T64-09": "Actual application screen and reviewed DOM selectors",
    "AZ-T64-11": "Search uses approved synthetic data and verified results",
    "AZ-T64-13": "Chat handles safe input without sensitive logging",
    "AZ-T64-15": "Expired or revoked session cannot be reused",
    "AZ-T64-17": "Error paths contain no tokens, credentials or protected data",
}
# Any service repository/runner not present in this tree must be supplied
# by a separately reviewed immutable reference; neither is assumed here.
REQUIRED_CONTRACTS = {
    "approved_app_source_revision": "Immutable source/artifact reference for the real application and its routing",
    "approved_private_base_url": "Authorized private gateway hostname, never a synthetic localhost substitute",
    "approved_encrypted_test_identity": "Authorized test identity and reproducible authentication/session contract",
    "approved_ui_selectors": "Reviewed real DOM selectors, main screen/action and expected results",
    "approved_internal_runner": "Private runner group, DNS/route, no public GitHub-hosted execution of live tests",
    "approved_external_vantage": "Separate authorized external-origin negative check without interpreting timeout as proof",
    "approved_synthetic_test_data": "Scoped, sanitized search/chat data and independent evidence handling",
    "approved_evidence_and_review": "UTC, scoped asset and source hashes, secured artifacts, independent reviewer",
}
LOCAL_ARTIFACTS = (
    "tests/package.json",
    "tests/package-lock.json",
    "tests/playwright.config.ts",
    "tests/phase6/phase6.spec.ts",
    "docs/test-data-handling.md",
)


def inspect(root: Path = ROOT) -> dict:
    root = Path(root)
    inventory = audit(root, include_cases=True)
    errors = list(inventory["errors"])
    cases = {}
    for case_id, target in EXPECTED_REFERENCES.items():
        actual = inventory.get("cases", {}).get(case_id)
        if actual is None:
            errors.append(f"missing canonical ID {case_id}")
            continue
        if target not in actual["script_refs"]:
            errors.append(f"{case_id}: catalogue command no longer cites {target}")
        path_present = path_exists(root, target)
        cases[case_id] = {
            "expected_path": target,
            "path_present": path_present,
            "state": "SOURCE_REVIEW_REQUIRED" if path_present else "SOURCE_MISSING",
            "criterion": REQUIREMENTS[case_id],
            "azure_acceptance": "NOT_READY",
        }
    local = {path: {
        "present": path_exists(root, path),
        "meaning": "presence only; does not verify behavior or approvals",
    } for path in LOCAL_ARTIFACTS}
    # No approval or active credentials can be inferred from a repo file.
    prerequisites = {
        k: {"state": "UNVERIFIED_EXTERNAL_OWNER_INPUT", "description": v}
        for k, v in REQUIRED_CONTRACTS.items()
    }
    return {
        "schema": "azure-playwright-readiness/v1",
        "execution_class": "OFFLINE_READ_ONLY_INVENTORY",
        "canonical_case_ids": inventory["canonical_test_ids"],
        "case_references_reviewed": len(cases),
        "case_path_missing": sum(not c["path_present"] for c in cases.values()),
        "case_source_review_required": sum(c["path_present"] for c in cases.values()),
        "cases": cases,
        "local_artifacts": local,
        "independent_prerequisites": prerequisites,
        "errors": errors,
        "readiness": "INVALID_INVENTORY" if errors else "BLOCKED_UNVERIFIED_APP_AND_RUNNERS",
        "approved_live_azure_passes": 0,
        "release_decision": "NO_GO",
        "limitations": [
            "Only literal referenced-path existence was checked; no Playwright execution",
            "Presence of a spec/config cannot prove implemented selectors, authentication or TLS checks",
            "No private runner, external vantage point, real app revision or identity was verified",
            "The remaining 717 cases without a direct script reference are NOT browser tests",
            "This report cannot authorize live validation, deployment or release",
        ],
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path)
    p.add_argument("--strict", action="store_true",
                   help="exit 2 until every browser prerequisite has external verification")
    args = p.parse_args(argv)
    report = inspect(args.root)
    data = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(data, encoding="utf-8")
    print(data, end="")
    return 2 if report["errors"] or args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
