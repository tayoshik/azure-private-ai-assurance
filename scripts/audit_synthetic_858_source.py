#!/usr/bin/env python3
"""Read-only, source-locked pre-execution review of 858 synthetic test definitions.

Never execute canonical commands, read private fixtures, call Azure or promote
synthetic detector checks into independently accepted Azure control results.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from audit_tool_semantics_13 import load_sources
from build_execution_route_1716 import (
    ROOT, ROUTE_SYNTHETIC, build as build_routes, digest_case,
)

SCHEMA = "azure-synthetic-858-source-contract-review/v1"
GROUP_COUNTS = {
    "PHASE1_POLICY": 110,
    "PHASE2_POLICY": 110,
    "PHASE3_GUARD": 132,
    "PHASE4_GUARD": 143,
    "PHASE5_GUARD": 143,
    "PHASE6_GUARD": 110,
    "PHASE7_GUARD": 110,
}
GROUP_SOURCE = {
    "PHASE1_POLICY": "specs/english_tests_001_440.json",
    "PHASE2_POLICY": "specs/english_tests_001_440.json",
    "PHASE3_GUARD": "specs/phase3_264_en.json",
    "PHASE4_GUARD": "specs/phase4_286_en.json",
    "PHASE5_GUARD": "specs/phase5_286_en.json",
    "PHASE6_GUARD": "specs/phase6_220_en.json",
    "PHASE7_GUARD": "specs/phase7_220_en.json",
}
COMMAND_SPECS = {
    "PHASE1_POLICY": ("scripts/phase1_policy_check.py", "specs/phase1_policies_110.json", "rules"),
    "PHASE2_POLICY": ("scripts/phase2_policy_check.py", "specs/phase2_220.json", "spec"),
    "PHASE3_GUARD": ("scripts/phase3_guard.py", "specs/phase3_264.json", "spec"),
    "PHASE4_GUARD": ("scripts/phase4_guard.py", "specs/phase4_286.json", "spec"),
    "PHASE5_GUARD": ("scripts/phase5_guard.py", "specs/phase5_286_en.json", "spec"),
    "PHASE6_GUARD": ("scripts/phase6_guard.py", "specs/phase6_220_en.json", "spec"),
    "PHASE7_GUARD": ("scripts/phase7_guard.py", "specs/phase7_220_en.json", "spec"),
}
REVIEW_CHECKS = (
    "VERIFY_PINNED_PYTHON_AND_SCRIPT_CONTENT_SHA256",
    "VERIFY_APPROVED_CREDENTIAL_FREE_SYNTHETIC_FIXTURE_SOURCE_AND_EXPECTED_VERDICTS",
    "VERIFY_GOOD_BAD_MISSING_OR_EQUIVALENT_NEGATIVE_DETECTOR_COVERAGE",
    "VERIFY_SELFTEST_IS_OFFLINE_AND_CANNOT_SATISFY_LIVE_CONTROL_PREDICATE",
    "OBTAIN_OWNER_APPROVAL_AND_INDEPENDENT_REVIEW_BEFORE_ANY_REAL_EXECUTION",
)


class SyntheticSourceError(ValueError):
    """Frozen synthetic source or routing contract no longer matches."""


def group_for(case_id: str, source: str) -> str:
    if not isinstance(case_id, str) or not isinstance(source, str):
        raise SyntheticSourceError("invalid canonical source or ID")
    if not case_id.startswith("AZ-T") or len(case_id) != 8:
        raise SyntheticSourceError("malformed case ID")
    try:
        step = int(case_id[4:6])
        number = int(case_id[7:])
    except ValueError as exc:
        raise SyntheticSourceError("malformed case ID numeric fields") from exc
    if case_id[6] != "-" or not (1 <= step <= 78 and 2 <= number <= 22 and number % 2 == 0):
        raise SyntheticSourceError("ID is not a canonical even-numbered synthetic candidate")
    if step <= 10:
        group = "PHASE1_POLICY"
    elif step <= 20:
        group = "PHASE2_POLICY"
    elif step <= 32:
        group = "PHASE3_GUARD"
    elif step <= 45:
        group = "PHASE4_GUARD"
    elif step <= 58:
        group = "PHASE5_GUARD"
    elif step <= 68:
        group = "PHASE6_GUARD"
    else:
        group = "PHASE7_GUARD"
    if GROUP_SOURCE[group] != source:
        raise SyntheticSourceError("ID and frozen source phase do not agree")
    return group


def verify_command(case_id: str, group: str, command: str) -> str:
    """Check the *entire literal* grammar; do not parse as an executable shell."""
    if group not in COMMAND_SPECS or not isinstance(command, str):
        raise SyntheticSourceError("unknown group or command")
    script, config, mode = COMMAND_SPECS[group]
    if mode == "rules":
        expected = f"python3 {script} --rules {config} --selftest --test-id {case_id}"
    else:
        expected = f"python3 {script} --selftest {case_id} --spec {config}"
    if command != expected:
        raise SyntheticSourceError("frozen synthetic command does not match exact approved grammar")
    return script


def build_review(root: Path = ROOT, *, include_cases: bool = True) -> dict:
    root = Path(root)
    upstream = build_routes(root, include_cases=True)
    if (upstream["status"] != "ROUTING_INVENTORY_ONLY"
            or upstream["errors"]
            or upstream["canonical_test_ids"] != 1716
            or upstream["route_counts"].get(ROUTE_SYNTHETIC) != 858):
        raise SyntheticSourceError("upstream frozen routing is not verified")
    sources = load_sources(root)
    target = {i: row for i, row in upstream["cases"].items()
              if row["route"] == ROUTE_SYNTHETIC}
    if len(target) != 858 or set(target) - set(sources):
        raise SyntheticSourceError("synthetic source IDs incomplete")
    output: dict[str, dict] = {}
    group_counts: Counter = Counter()
    for case_id, row in sorted(target.items()):
        source = sources[case_id]
        if digest_case(source) != row["catalogue_contract_sha256"]:
            raise SyntheticSourceError("canonical ID/command/expected digest mismatch")
        if (row["direct_command_family"] != "python3"
                or row["semantic_readiness"] != "OFFLINE_SYNTHETIC_ONLY"
                or row["case_polarity"] != "EVEN"
                or row["source_test_executed"] is not False
                or row["azure_live_acceptance"] != "NOT_READY"):
            raise SyntheticSourceError("unapproved execution or acceptance state")
        group = group_for(case_id, row["canonical_catalogue"])
        script = verify_command(case_id, group, source.get("command"))
        # Script and spec existence is only a source prerequisite, not an
        # endorsement of code safety, runtime pinning or fixture correctness.
        config = COMMAND_SPECS[group][1]
        if not (root / script).is_file() or not (root / config).is_file():
            raise SyntheticSourceError("synthetic script or configuration source missing")
        group_counts[group] += 1
        output[case_id] = {
            "canonical_source": row["canonical_catalogue"],
            "contract_sha256": row["catalogue_contract_sha256"],
            "review_group": group,
            "script_reference": script,
            "spec_reference": config,
            "review_checklist": list(REVIEW_CHECKS),
            "script_source_present": True,
            "spec_source_present": True,
            "pinned_runtime_verified": False,
            "semantic_detection_verified": False,
            "synthetic_execution_authorized": False,
            "synthetic_detector_result_verified": False,
            "original_command_executed": False,
            "independent_reviewer_signed": False,
            "azure_live_acceptance": "NOT_READY",
        }
    if dict(group_counts) != GROUP_COUNTS:
        raise SyntheticSourceError("the 858 synthetic groups changed")
    return {
        "schema": SCHEMA,
        "status": "SYNTHETIC_SOURCE_CONTRACT_REVIEW_ONLY",
        "canonical_cases": 1716,
        "synthetic_candidates": 858,
        "source_group_counts": {k: group_counts[k] for k in GROUP_COUNTS},
        "original_commands_executed": 0,
        "synthetic_detector_passes_claimed": 0,
        "independent_review_approvals": 0,
        "azure_live_passes": 0,
        "azure_not_ready": 1716,
        "release_decision": "NO_GO",
        "limitations": [
            "Command syntax and source existence do not prove implementation safety",
            "Synthetic good/bad/missing fixtures and expected outcomes not executed",
            "No approved real evidence, credentials, Azure tenant or network were inspected",
            "The historical frozen catalogue remains unchanged",
        ],
        **({"cases": output} if include_cases else {}),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path)
    p.add_argument("--summary-only", action="store_true")
    p.add_argument("--strict", action="store_true", help="return 2 while signoff/live evidence absent")
    a = p.parse_args(argv)
    try:
        result = build_review(a.root, include_cases=not a.summary_only)
        if a.out:
            a.out.parent.mkdir(parents=True, exist_ok=True)
            a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (SyntheticSourceError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({
            "status": "SYNTHETIC_SOURCE_REVIEW_BLOCKED",
            "error_type": type(exc).__name__,
            "azure_live_passes": 0,
            "release_decision": "NO_GO",
        }))
        return 1
    print(json.dumps({k: v for k, v in result.items() if k != "cases"},
                     ensure_ascii=False, indent=2, sort_keys=True))
    return 2 if a.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
