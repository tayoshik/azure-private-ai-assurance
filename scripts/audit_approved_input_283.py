#!/usr/bin/env python3
"""Non-executing, source-locked review queue for 283 approved-input candidates.

Classifies *source references only*; does not open, download, run, verify,
approve or publish the real input, baseline, Terraform state, plan or evidence.
Review labels are not trust levels or authorization to run canonical commands.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

from build_execution_route_1716 import ROOT, digest_case
from triage_local_464 import (
    PRIORITY_INPUT, TriageError, inspect_command, make_queue,
)

SCHEMA = "azure-local-p1-283-approved-input-review/v1"
PLAN = "A_TERRAFORM_PLAN_STATE_OR_TFVARS_CUSTODY"
EVIDENCE = "B_RESTRICTED_EVIDENCE_LOG_AND_OBSERVATION_CUSTODY"
NETWORK = "C_NETWORK_IPAM_DNS_AND_TOPOLOGY_BASELINE"
POLICY = "D_POLICY_APPROVAL_AND_SIGNED_BASELINE"
OTHER = "E_OTHER_ENV_OR_SOURCE_INPUT_MANUAL_REVIEW"
CLASSES = (PLAN, EVIDENCE, NETWORK, POLICY, OTHER)
SOURCES = (
    "specs/english_tests_001_440.json", "specs/phase3_264_en.json",
    "specs/phase4_286_en.json", "specs/phase5_286_en.json",
    "specs/phase6_220_en.json", "specs/phase7_220_en.json",
)

# These expressions identify *source text* clues and may overlap. Never
# substitute such a clue for verified provenance, authorization or custody.
PLAN_RE = re.compile(
    r"(?i)(?:\.tfplan\b|\.tfstate(?:\b|\.)|\.tfvars(?:\b|\.)|"
    r"\$[{]?(?:APPROVED_PLAN|PLAN_JSON_EVIDENCE|TF_PRIVATE_|TFPLAN|TFSTATE)\b|"
    r"(?:[/_-]plan[/_-]|[/_-]state[/_-])(?:approved|private|backend|artifact)\b)"
)
EVIDENCE_RE = re.compile(
    r"(?i)(?:evidence[/_-]|raw[/_-]evidence|logs?[/_-]|"
    r"\$[{]?(?:EVIDENCE|APPROVED_EVIDENCE|OBSERVATIONS?|AUDIT_LOG|SCAN_REPORT)\b|"
    r"\b(?:observations|attestation|signed[_-]evidence|ci[_/-]report)\b)"
)
NETWORK_RE = re.compile(
    r"(?i)(?:\bIPAM\b|\$[{]?(?:IPAM|DNS|CIDR|NETWORK|PEER|TOPOLOGY|SUBNET|PRIVATE_DNS)\w*|"
    r"\b(?:networks|subnets|cidrs|routes|vnet|dns_zone|peering)\b)"
)
POLICY_RE = re.compile(
    r"(?i)(?:\bpolicy\b|policies|baseline|\bapproval\b|approved|"
    r"\$[{]?(?:POLICY|BASELINE|APPROVED|CONTROL)\w*)"
)
ENV_RE = re.compile(r"\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*[^}]*\})")
TRIGGERS = (
    (PLAN, PLAN_RE),
    (EVIDENCE, EVIDENCE_RE),
    (NETWORK, NETWORK_RE),
    (POLICY, POLICY_RE),
)
NEXT_REVIEW = {
    PLAN: (
        "CONFIRM_APPROVED_PLAN_STATE_ARTIFACT_OWNER_AND_ENCRYPTED_STORAGE",
        "VERIFY_IMMUTABLE_SHA256_SCOPE_STATE_LINEAGE_AND_SIGNED_BASELINE",
        "BLOCK_PUBLIC_CI_LOGS_ARTIFACTS_OR_UNAPPROVED_TERRAFORM_PROCESSING",
    ),
    EVIDENCE: (
        "VERIFY_ORIGIN_COLLECTOR_UTC_AND_CHAIN_OF_CUSTODY",
        "VALIDATE_SCOPE_RESOURCE_ID_LOG_REDACTION_AND_IMMUTABLE_EVIDENCE_HASH",
        "STORE_RESTRICTED_EVIDENCE_OUTSIDE_PUBLIC_REPOSITORY",
    ),
    NETWORK: (
        "CONFIRM_NETWORK_IPAM_DNS_BASELINE_OWNER_SCOPE_AND_APPROVAL",
        "VERIFY_ASSET_IDENTIFIERS_EFFECTIVE_DATES_AND_INDEPENDENT_SIGNATURE",
        "SEPARATE_OFFLINE_DOCUMENT_ASSERTIONS_FROM_LIVE_NETWORK_ACCEPTANCE",
    ),
    POLICY: (
        "VERIFY_SIGNED_POLICY_OR_BASELINE_VERSION_AND_CONTROL_OWNER",
        "VALIDATE_EXPECTED_PREDICATE_AGAINST_APPROVED_RESOURCE_SCOPE",
        "DO_NOT_ACCEPT_SELF_ASSERTED_APPROVAL_FIELD_OR_MOCK_AS_LIVE_PASS",
    ),
    OTHER: (
        "EXPLICITLY_IDENTIFY_EVERY_INPUT_ENV_VALUE_AND_SOURCE",
        "VERIFY_APPROVED_STORAGE_PROVENANCE_HASH_AND_REQUIRED_PERMISSIONS",
        "REVIEW_ORIGINAL_COMMAND_AND_EXPECTED_ASSERTION_BEFORE_AUTHORIZATION",
    ),
}


def classify_input(command: str, parent_reason_codes: list[str]) -> tuple[str, list[str]]:
    """Exclusive review order and overlapping coarse indicators; no raw refs."""
    if not isinstance(command, str) or not command.strip():
        raise TriageError("empty canonical command")
    if not isinstance(parent_reason_codes, list):
        raise TriageError("malformed upstream reason codes")
    indicators: set[str] = set()
    matched = []
    for group, pattern in TRIGGERS:
        if pattern.search(command):
            matched.append(group)
            indicators.add("SOURCE_HINT_" + group.split("_", 1)[0])
    if ENV_RE.search(command):
        indicators.add("ENV_REFERENCE_UNVERIFIED")
    if "MISSING_LITERAL_INPUT_PATH" in parent_reason_codes:
        indicators.add("MISSING_LITERAL_INPUT_REFERENCE")
    if "POSSIBLE_RESTRICTED_OR_APPROVED_INPUT" in parent_reason_codes:
        indicators.add("RESTRICTED_INPUT_CANDIDATE")
    if "ENVIRONMENT_INPUT_UNVERIFIED" in parent_reason_codes:
        indicators.add("PARENT_ENV_DEPENDENCY")
    if "IMPLEMENTATION_OR_TOOL_SEMANTICS" in parent_reason_codes:
        indicators.add("TOOL_ASSERTION_SEMANTICS_REQUIRED")
    if not matched:
        indicators.add("NO_KNOWN_INPUT_KIND_MANUAL_REVIEW")
    if len(matched) > 1:
        indicators.add("MULTIPLE_INPUT_CLASSES_REQUIRE_INDEPENDENT_REVIEW")
    return (matched[0] if matched else OTHER), sorted(indicators)


def build_review(root: Path = ROOT, *, include_cases: bool = True) -> dict:
    parent = make_queue(root, include_cases=True)
    if parent["status"] != "REVIEW_PRIORITIES_ONLY" or parent["local_candidate_cases"] != 464:
        raise TriageError("upstream local priority inventory invalid")
    target = {id_: row for id_, row in parent["cases"].items()
              if row["review_priority"] == PRIORITY_INPUT}
    if len(target) != 283:
        raise TriageError("expected exact 283 input-dependent candidates")

    original = {}
    for source in SOURCES:
        try:
            payload = json.loads((Path(root) / source).read_text(encoding="utf-8"))
            records = payload["cases"] if "cases" in payload else payload["tests"]
            if not isinstance(records, list):
                raise TriageError("frozen catalogue not a list")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            raise TriageError("immutable catalogue unavailable") from exc
        for row in records:
            if row["id"] in original:
                raise TriageError("duplicate immutable case ID")
            original[row["id"]] = row
    rows = {}
    counts = Counter()
    overlapping = Counter()
    by_source = defaultdict(Counter)
    for ident, meta in sorted(target.items()):
        case = original.get(ident)
        if not case or digest_case(case) != meta["contract_sha256"]:
            raise TriageError("frozen command/expected fingerprint drift")
        missing = ["PRIVATE_INPUT_NOT_VERIFIED"] if (
            "MISSING_LITERAL_INPUT_PATH" in meta["review_reason_codes"]) else []
        parent_class, reasons = inspect_command(
            case["command"], meta["command_family"], missing)
        if parent_class != PRIORITY_INPUT or reasons != meta["review_reason_codes"]:
            raise TriageError("source and inherited input risk classification disagree")
        cls, indicators = classify_input(case["command"], reasons)
        counts[cls] += 1
        by_source[meta["canonical_source"]][cls] += 1
        overlapping.update(indicators)
        rows[ident] = {
            "canonical_source": meta["canonical_source"],
            "contract_sha256": meta["contract_sha256"],
            "command_family": meta["command_family"],
            "review_input_class": cls,
            "overlapping_source_indicators": indicators,
            "required_review_checks": list(NEXT_REVIEW[cls]),
            "input_source_identified": False,
            "actual_input_bytes_examined": False,
            "approved_input_hash_verified": False,
            "access_and_custody_approved": False,
            "expected_control_semantics_reviewed": False,
            "independent_reviewer1_signed": False,
            "independent_reviewer2_signed": False,
            "command_executed": False,
            "azure_live_acceptance": "NOT_READY",
        }
    if len(rows) != 283 or sum(counts.values()) != 283 or set(rows) != set(target):
        raise TriageError("incomplete restricted-input queue")
    return {
        "schema": SCHEMA,
        "status": "SOURCE_INPUT_REVIEW_ONLY",
        "frozen_1716_case_count": 1716,
        "local_464_candidate_count": 464,
        "restricted_input_283_candidate_count": 283,
        "review_input_class_counts": {c: counts[c] for c in CLASSES},
        "source_class_counts": {
            source: {c: count[c] for c in CLASSES}
            for source, count in sorted(by_source.items())
        },
        "overlapping_indicator_counts": dict(sorted(overlapping.items())),
        "input_bytes_inspected": 0,
        "approved_inputs_verified": 0,
        "source_commands_executed": 0,
        "independent_approvals_verified": 0,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "limitations": [
            "A lexical source hint is not an inventory of actual files or safe content",
            "No private inputs, approved plans, state, tokens, Azure APIs or network were accessed",
            "Source-only per-ID fingerprints do not independently attest evidence signatures",
            "Every bucket remains owner+two-reviewer NOT_READY, including OTHER",
        ],
        **({"cases": rows} if include_cases else {}),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--summary-only", action="store_true")
    parser.add_argument("--strict", action="store_true",
                        help="exit 2 until true independent Azure acceptance exists")
    args = parser.parse_args(argv)
    try:
        report = build_review(args.root, include_cases=not args.summary_only)
        encoded = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(encoded, encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "INPUT_REVIEW_SOURCE_BLOCKED",
                          "error_type": type(exc).__name__,
                          "azure_live_passes": 0, "release_decision": "NO_GO"}))
        return 1
    print(json.dumps({k: v for k, v in report.items() if k != "cases"},
                     ensure_ascii=False, indent=2, sort_keys=True))
    return 2 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
