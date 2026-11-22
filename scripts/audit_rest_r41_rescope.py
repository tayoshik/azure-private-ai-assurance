#!/usr/bin/env python3
"""R41: source-locked, offline-only 13-case REST rescope proposal audit.

Checks proposed crosswalk against frozen English catalogues. Does NOT alter
1,716 test IDs or approve any REST unit test, live observation, or release.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = "specs/r41-rest-api-rescope-proposal.json"
ORIGINALS = {
    "specs/english_tests_001_440.json": "cases",
    "specs/phase6_220_en.json": "tests",
}
EXPECTED = (
    "AZ-T20-07", "AZ-T20-09", "AZ-T20-15", "AZ-T20-17",
    "AZ-T64-01", "AZ-T64-03", "AZ-T64-05", "AZ-T64-07",
    "AZ-T64-09", "AZ-T64-11", "AZ-T64-13", "AZ-T64-15", "AZ-T64-17",
)
PATHS = {
    "tests/playwright.config.ts": set(EXPECTED[:4]),
    "tests/phase6/phase6.spec.ts": set(EXPECTED[4:]),
}


def read_json(root: Path, relative: str):
    path = root / relative
    return json.loads(path.read_text(encoding="utf-8"))


def inspect(root: Path = ROOT) -> dict:
    root = Path(root)
    errors: list[str] = []
    try:
        proposal = read_json(root, PROPOSAL)
        assert isinstance(proposal, dict)
    except (OSError, ValueError, AssertionError) as exc:
        return {
            "schema": "r41-rest-rescope-audit/v1", "result": "INVALID_PROPOSAL",
            "errors": [f"{PROPOSAL}: {exc}"], "approved": False,
            "api_unit_test_passes": 0, "azure_live_passes": 0,
            "release_decision": "NO_GO",
        }

    checks = {
        "schema": "azure-rest-api-test-rescope/v1",
        "intent": "Azure REST API unit tests, not web UI browser testing",
        "approval_status": "PROPOSED_NOT_APPROVED",
        "frozen_case_count": 1716,
        "frozen_case_modifications": 0,
        "original_test_reference_count": 13,
        "azure_independent_acceptance": 0,
        "release_decision": "NO_GO",
    }
    for name, value in checks.items():
        if proposal.get(name) != value:
            errors.append(f"R41 {name}: expected {value!r}")
    if sorted(proposal.get("original_test_reference_paths", [])) != sorted(PATHS):
        errors.append("R41 original reference paths differ")

    actual = proposal.get("cases")
    if not isinstance(actual, list):
        actual = []
        errors.append("R41 cases is not an array")
    ids = [c.get("id") if isinstance(c, dict) else None for c in actual]
    if ids != list(EXPECTED):
        errors.append("R41 case IDs/order differ from exactly 13 frozen references")

    catalogues: dict[str, dict] = {}
    for relative, key in ORIGINALS.items():
        try:
            doc = read_json(root, relative)
            source = doc[key]
            assert isinstance(source, list)
            catalogues[relative] = {r["id"]: r for r in source}
            if len(catalogues[relative]) != len(source):
                errors.append(f"{relative}: duplicate catalogue IDs")
        except (OSError, ValueError, KeyError, TypeError, AssertionError) as exc:
            errors.append(f"{relative}: original catalogue unavailable: {exc}")
            catalogues[relative] = {}

    checked: list[dict] = []
    for case in actual:
        if not isinstance(case, dict):
            errors.append("non-object R41 case")
            continue
        case_id = case.get("id")
        if case_id not in EXPECTED:
            errors.append(f"unknown R41 ID {case_id!r}")
            continue
        relative = ("specs/english_tests_001_440.json"
                    if case_id.startswith("AZ-T20-") else "specs/phase6_220_en.json")
        path = ("tests/playwright.config.ts"
                if case_id.startswith("AZ-T20-") else "tests/phase6/phase6.spec.ts")
        if case.get("frozen_catalogue") != relative:
            errors.append(f"{case_id}: wrong original catalogue")
        if case.get("old_ref_path") != path:
            errors.append(f"{case_id}: wrong original reference path")
        original = catalogues[relative].get(case_id)
        if original is None:
            errors.append(f"{case_id}: missing from original catalogue")
        else:
            if case.get("frozen_command") != original.get("command"):
                errors.append(f"{case_id}: frozen command drift")
            if case.get("frozen_expected") != original.get("expected"):
                errors.append(f"{case_id}: frozen expected-result drift")
            if path not in original.get("command", ""):
                errors.append(f"{case_id}: no longer cites original browser path")
            if original.get("azure_live_pass") is not False:
                errors.append(f"{case_id}: original live result unexpectedly changed")
        for name, value in {
            "approval": "PENDING_SCOPE_CHANGE_APPROVAL",
            "frozen_case_changed": False,
            "azure_live_acceptance": "NOT_READY",
            "api_unit_test_pass": False,
        }.items():
            if case.get(name) != value:
                errors.append(f"{case_id}: {name} must remain {value!r}")
        for name in ("proposed_disposition", "proposed_rest_check", "qualification"):
            if not isinstance(case.get(name), str) or not case[name].strip():
                errors.append(f"{case_id}: missing {name}")
        checked.append({"id": case_id,
                        "proposal": case.get("proposed_disposition"),
                        "original_catalogue": relative,
                        "scope_approval": "PENDING_SCOPE_CHANGE_APPROVAL",
                        "unit_test_status": "NOT_EXECUTED",
                        "azure_acceptance": "NOT_READY"})

    return {
        "schema": "r41-rest-rescope-audit/v1",
        "result": ("INVALID_CROSSWALK" if errors
                   else "CROSSWALK_VERIFIED_PROPOSAL_UNAPPROVED"),
        "execution_class": "OFFLINE_SOURCE_CROSSWALK_ONLY",
        "original_id_count": 1716,
        "reviewed_case_count": len(checked),
        "case_ids": ids,
        "source_files_checked": list(ORIGINALS),
        "case_records": checked,
        "source_change_approved": False,
        "approved": False,
        "api_unit_test_passes": 0,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "errors": errors,
        "limitations": [
            "Original English catalogue records are compared but not modified",
            "A valid proposed crosswalk is not an approved replacement of browser requirements",
            "No HTTP requests, Azure authentication, Terraform or browser tests are run",
            "ARM management plane, service data plane and network integration require separate contracts",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--strict", action="store_true",
                        help="Refuse completion until separately approved; expected exit 2")
    args = parser.parse_args(argv)
    result = inspect(args.root)
    raw = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(raw, encoding="utf-8")
    print(raw, end="")
    if result["errors"]:
        return 1
    return 2 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
