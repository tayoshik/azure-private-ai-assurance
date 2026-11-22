#!/usr/bin/env python3
"""1716-case offline execution routing inventory: evidence-dependent, no execution.

Read the six immutable published catalogues, literal-dependency audit, R41
proposal and semantic-readiness audit. Never execute a catalogue command,
connect to Azure or infer live acceptance from source/CI/fixture presence.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

if __package__:
    from .audit_catalogue_dependencies import ROOT, SOURCES, EXPECTED_IDS, audit
    from .audit_semantic_readiness import review
    from .audit_rest_r41_rescope import inspect as inspect_r41, EXPECTED as R41_IDS
else:
    from audit_catalogue_dependencies import ROOT, SOURCES, EXPECTED_IDS, audit
    from audit_semantic_readiness import review
    from audit_rest_r41_rescope import inspect as inspect_r41, EXPECTED as R41_IDS

SCHEMA = "azure-1716-execution-routing/v1"
ROUTE_SYNTHETIC = "OFFLINE_SYNTHETIC_CANDIDATE"
ROUTE_LOCAL = "LOCAL_APPROVED_INPUT_AND_REVIEW"
ROUTE_LIVE = "AZURE_OR_PRIVATE_RUNNER_REQUIRED"
ROUTE_R41 = "LEGACY_R41_SCOPE_DECISION_REQUIRED"
ROUTE_SELFTEST = "ODD_SELFTEST_SEMANTIC_DECISION_REQUIRED"
EXPECTED_ROUTES = {
    ROUTE_SYNTHETIC: 858,
    ROUTE_R41: 13,
    ROUTE_SELFTEST: 1,
}
LIVE_COMMANDS = frozenset({"az", "dig", "curl", "openssl", "getent", "npx"})
TERRAFORM_LIVE = re.compile(
    r"^\s*terraform(?:\s+-\S+)*\s+(?:plan|apply|refresh|import|state)\b"
)
PREREQUISITES = {
    ROUTE_SYNTHETIC: (
        "REPRODUCIBLE_CREDENTIAL_FREE_RUNNER",
        "PINNED_SYNTHETIC_INPUT_AND_EXPECTED_ASSERTION",
        "OFFLINE_COMMAND_SEMANTIC_REVIEW",
    ),
    ROUTE_LOCAL: (
        "APPROVED_SOURCE_ARTIFACT_OR_BASELINE",
        "REVIEW_OF_ASSERTION_VS_CONTROL",
        "INDEPENDENT_EVIDENCE_REVIEW",
    ),
    ROUTE_LIVE: (
        "APPROVED_NONPRODUCTION_TARGET_AND_SCOPE",
        "APPROVED_IDENTITY_OR_PRIVATE_NETWORK_RUNNER",
        "INDEPENDENT_BASELINE_EVIDENCE_AND_REVIEW",
    ),
    ROUTE_R41: (
        "OWNER_APPROVAL_OF_EACH_R41_SCOPE_DISPOSITION",
        "VERSIONED_REPLACEMENT_OR_EXPLICIT_NA_DECISION",
        "APPROVED_APP_OR_API_TEST_CONTRACT",
    ),
    ROUTE_SELFTEST: (
        "OWNER_DECISION_ON_ODD_ID_SELFTEST_SEMANTICS",
        "INDEPENDENT_ASSERTION_AND_EVIDENCE_CRITERION",
    ),
}
OWNER_LANE = {
    ROUTE_SYNTHETIC: "TEST_IMPLEMENTER_AND_QA_REVIEWER",
    ROUTE_LOCAL: "CONTROL_OWNER_AND_INDEPENDENT_REVIEWER",
    ROUTE_LIVE: "AZURE_OWNER_AND_APPROVED_RUNNER_OPERATOR",
    ROUTE_R41: "REQUIREMENTS_OWNER_AND_SECURITY_REVIEWER",
    ROUTE_SELFTEST: "CONTROL_OWNER_AND_QA_REVIEWER",
}
NEXT_ACTION = {
    ROUTE_SYNTHETIC: "REVIEW_THEN_EXECUTE_IN_PINNED_OFFLINE_CI",
    ROUTE_LOCAL: "OBTAIN_APPROVED_INPUT_AND_REVIEW_EXACT_CONTROL_ASSERTION",
    ROUTE_LIVE: "DEFER_DIRECT_COMMAND_UNTIL_APPROVED_AZURE_ENV_AND_RUNNER",
    ROUTE_R41: "APPROVE_OR_REJECT_VERSIONED_R41_CHANGE_BEFORE_REPLACEMENT",
    ROUTE_SELFTEST: "DECIDE_IF_SELFTEST_CAN_REPLACE_ODD_REAL_EVIDENCE",
}


class InventoryError(ValueError):
    """A case cannot be safely assigned an evidence-aware execution route."""


def route_case(case_id: str, command: str, semantic: dict) -> tuple[str, str]:
    """Classify direct command's *required environment*, NOT actual executability."""
    if case_id not in EXPECTED_IDS:
        raise InventoryError("case ID is outside frozen catalogue")
    if not isinstance(command, str) or not command.strip():
        raise InventoryError("canonical command absent")
    if not isinstance(semantic, dict):
        raise InventoryError("semantic source record absent")
    status = semantic.get("assurance_readiness")
    odd = int(case_id[-2:]) % 2 == 1
    first = command.lstrip().split()[0]
    if case_id in R41_IDS:
        if not odd or status != "SOURCE_REFERENCE_MISSING":
            raise InventoryError("R41 case must retain unresolved historical source reference")
        return ROUTE_R41, first
    if status == "SOURCE_REFERENCE_MISSING":
        raise InventoryError("unexpected missing historical source reference")
    if not odd:
        if status != "OFFLINE_SYNTHETIC_ONLY" or first != "python3":
            raise InventoryError("synthetic design/command no longer matches canonical partition")
        return ROUTE_SYNTHETIC, first
    if status == "ODD_SELFTEST_REQUIRES_SEMANTIC_REVIEW":
        if case_id != "AZ-T74-13":
            raise InventoryError("unexpected odd selftest requires new explicit review")
        return ROUTE_SELFTEST, first
    if status != "UNVERIFIED_NON_SYNTHETIC_PROCEDURE":
        raise InventoryError("non-synthetic case no longer matches canonical semantics")
    # Only a literal top-level command classification, never a shell executor.
    # A local artifact inspection still requires approved evidence/baseline.
    if first in LIVE_COMMANDS or (first == "terraform" and TERRAFORM_LIVE.search(command)):
        return ROUTE_LIVE, first
    return ROUTE_LOCAL, first


def digest_case(case: dict) -> str:
    """Stable fingerprint of the frozen ID, command and expected criterion."""
    canonical = {k: case.get(k) for k in ("id", "command", "expected")}
    raw = json.dumps(canonical, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build(root: Path = ROOT, *, include_cases: bool = True) -> dict:
    root = Path(root)
    errors: list[str] = []
    semantic = review(root, include_cases=True)
    deps = audit(root, include_cases=True)
    r41 = inspect_r41(root)
    errors.extend(semantic["errors"])
    errors.extend(deps["errors"])
    if r41.get("result") != "CROSSWALK_VERIFIED_PROPOSAL_UNAPPROVED":
        errors.append("R41 source crosswalk is absent, altered or not pending approval")
    errors.extend(r41.get("errors", []))
    frozen_records: dict[str, tuple[str, dict]] = {}
    for rel in SOURCES:
        try:
            source = json.loads((root / rel).read_text(encoding="utf-8"))
            cases = source["cases"] if "cases" in source else source["tests"]
            if not isinstance(cases, list):
                raise ValueError("catalogue is not an array")
        except (OSError, KeyError, ValueError, TypeError) as exc:
            errors.append(f"{rel}: catalogue not readable: {type(exc).__name__}")
            continue
        for case in cases:
            if not isinstance(case, dict) or not isinstance(case.get("id"), str):
                errors.append(f"{rel}: malformed case")
                continue
            ident = case["id"]
            if ident in frozen_records:
                errors.append(f"duplicate frozen case: {ident}")
            else:
                frozen_records[ident] = (rel, case)

    rows: dict[str, dict] = {}
    routing = Counter()
    by_phase = defaultdict(Counter)
    command_groups = defaultdict(Counter)
    for ident in sorted(frozen_records):
        rel, case = frozen_records[ident]
        s = semantic.get("cases", {}).get(ident)
        d = deps.get("cases", {}).get(ident)
        try:
            lane, command_head = route_case(ident, case.get("command"), s)
            if d is None or s.get("catalogue") != rel or d.get("source") != rel:
                raise InventoryError("semantic/literal source provenance mismatch")
            if s.get("azure_acceptance") != "NOT_READY" or s.get("accepted_live_evidence") is not False:
                raise InventoryError("source has unverified acceptance promotion")
        except InventoryError as exc:
            errors.append(f"{ident}: {exc}")
            continue
        routing[lane] += 1
        by_phase[s["phase"]][lane] += 1
        command_groups[lane][command_head] += 1
        rows[ident] = {
            "phase": s["phase"],
            "canonical_catalogue": rel,
            "catalogue_contract_sha256": digest_case(case),
            "original_execution_class_claim": s["execution_class_claim"],
            "case_polarity": s["case_polarity"],
            "semantic_readiness": s["assurance_readiness"],
            "direct_command_family": command_head,
            "source_reference_state": d["literal_script_state"],
            "script_references": d["script_refs"],
            "input_references": d["input_refs"],
            "missing_script_paths": d["missing_scripts"],
            "missing_input_paths": d["missing_inputs"],
            "route": lane,
            "direct_execution_requires_azure_or_private_runner": lane == ROUTE_LIVE,
            "prerequisite_classes": list(PREREQUISITES[lane]),
            "proposed_owner_role": OWNER_LANE[lane],
            "next_action": NEXT_ACTION[lane],
            "source_test_executed": False,
            "approved_inputs_verified": False,
            "independent_reviewer_signed": False,
            "r41_scope_approved": False if lane == ROUTE_R41 else None,
            "azure_live_acceptance": "NOT_READY",
        }

    if set(rows) != EXPECTED_IDS:
        errors.append(f"only {len(rows)}/1716 canonical cases routed")
    if len(r41.get("case_records", [])) != 13:
        errors.append("R41 13-case source crosswalk count drift")
    for k, count in EXPECTED_ROUTES.items():
        if routing[k] != count:
            errors.append(f"routing partition changed: {k} {routing[k]} != {count}")
    if routing[ROUTE_LIVE] + routing[ROUTE_LOCAL] != 844:
        errors.append("non-synthetic 844-case routing partition drift")
    if sum(routing.values()) != 1716:
        errors.append("execution routing is not exhaustive")
    phase_totals = {p: sum(n.values()) for p, n in by_phase.items()}
    expected_phase_totals = {p: detail["cases"] for p, detail in semantic["by_phase"].items()}
    if phase_totals != expected_phase_totals:
        errors.append("routing phase totals differ from semantic audit")
    if semantic.get("independently_approved_azure_passes") != 0:
        errors.append("semantic audit must not claim accepted Azure PASS")
    return {
        "schema": SCHEMA,
        "status": "INVALID_SOURCE_OR_ROUTE" if errors else "ROUTING_INVENTORY_ONLY",
        "execution_class": "OFFLINE_READ_ONLY_METADATA_AUDIT",
        "canonical_test_ids": len(rows),
        "route_counts": dict(sorted(routing.items())),
        "phase_route_counts": {p: dict(sorted(c.items())) for p, c in sorted(by_phase.items())},
        "command_family_by_route": {r: dict(sorted(c.items())) for r, c in sorted(command_groups.items())},
        "r41_status": "PROPOSED_NOT_APPROVED",
        "r41_reference_count": 13,
        "original_missing_script_count": deps["literal_script_reference"]["MISSING_SCRIPT_REFERENCE"],
        "source_cases_executed_by_this_report": 0,
        "approved_inputs_verified": 0,
        "independent_review_approvals_verified": 0,
        "azure_live_passes_verified": 0,
        "azure_not_ready": len(rows),
        "release_decision": "NO_GO",
        "errors": errors,
        "limitations": [
            "Routes are conservative source/command-family hints, not validated runnable tests",
            "No canonical command was executed; no credentials, Azure API or private network inspected",
            "A local shell command may still require external baseline or privileged evidence",
            "Synthetic case parity describes design intent; it does not count synthetic execution PASS",
            "Unreferenced local scripts may be CLI/manual operations rather than missing work",
            "The 13 historical Playwright references are not silently replaced or marked N/A",
            "All Azure acceptance remains NOT_READY and release remains NO_GO",
        ],
        **({"cases": rows} if include_cases else {}),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--summary-only", action="store_true",
                        help="omit 1716 individual case rows from JSON output")
    parser.add_argument("--strict", action="store_true",
                        help="expected 2 until approved execution/evidence; never a release GO")
    args = parser.parse_args(argv)
    report = build(args.root, include_cases=not args.summary_only)
    encoded = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    if args.summary_only:
        print(encoded, end="")
    else:
        print(json.dumps({k: v for k, v in report.items() if k != "cases"},
                         ensure_ascii=False, indent=2, sort_keys=True))
    return 2 if report["errors"] or args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
