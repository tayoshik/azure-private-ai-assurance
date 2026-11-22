#!/usr/bin/env python3
"""R41: prepare 13 immutable, unapproved REST scope-decision review records.

Reads the existing exact source-crosswalk audit. Never interprets a proposal,
mock response, or missing Playwright file as an approved requirements change.
Does not execute tests, request HTTP, use identity, or modify catalogues.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from audit_rest_r41_rescope import (
    EXPECTED, EXPECTED_DISPOSITIONS, ORIGINALS, PATHS, PROPOSAL, ROOT,
    inspect, read_json,
)

SCHEMA = "r41-owner-decision-readiness/v1"

# Owner input questions are review *requirements*, not recorded approvals.
GATES = {
    "AZ-T20-07": ("RUNNER_TOPOLOGY", (
        "APPROVED_EXTERNAL_TEST_ORIGIN_AND_IDENTITY",
        "APPROVED_TARGET_AND_NEGATIVE_REACHABILITY_PREDICATE",
        "INDEPENDENT_DNS_ROUTE_AND_NETWORK_EVIDENCE",
    )),
    "AZ-T20-09": ("RUNNER_TOPOLOGY", (
        "APPROVED_PRIVATE_RUNNER_AND_EXECUTION_IDENTITY",
        "PRIVATE_DNS_EGRESS_ROUTE_AND_RBAC_EVIDENCE",
        "INDEPENDENT_PROTECTED_OBSERVATION_CUSTODY",
    )),
    "AZ-T20-15": ("EVIDENCE_FORMAT", (
        "VERSIONED_JUNIT_XML_AND_SANITIZED_JSON_SCHEMA",
        "EXPLICIT_MOCK_UNIT_VERSUS_AUTHORIZED_LIVE_CLASSIFICATION",
        "IMMUTABLE_PROVENANCE_AND_INDEPENDENT_REVIEW_FIELDS",
    )),
    "AZ-T20-17": ("EVIDENCE_CUSTODY", (
        "APPROVED_RESTRICTED_EVIDENCE_STORAGE_AND_ACCESS_ROLES",
        "HTTP_TRACE_REDACTION_NEGATIVE_TESTS",
        "RETENTION_HASH_AND_REVIEW_CHAIN_OF_CUSTODY",
    )),
    "AZ-T64-01": ("REST_INTEGRATION", (
        "APPROVED_ENDPOINT_AND_TARGET_ASSET_CORRELATION",
        "REQUEST_ORIGIN_ROUTE_HTTP_STATUS_AND_CORRELATION_ID",
        "INDEPENDENT_AUTHORIZED_NETWORK_OBSERVATION",
    )),
    "AZ-T64-03": ("REST_TLS_INTEGRATION", (
        "APPROVED_PEER_HOSTNAME_AND_CERTIFICATE_POLICY",
        "CHAIN_EXPIRY_AND_TLS_NEGATIVE_TEST_EXPECTATIONS",
        "AUTHORIZED_RUNNER_AND_VERIFIED_PEER_OBSERVATION",
    )),
    "AZ-T64-05": ("REST_AUTHORIZATION", (
        "APPROVED_ENTRA_AUDIENCE_SCOPE_AND_ROLE_CONTRACT",
        "LEAST_PRIVILEGE_AND_401_403_NEGATIVE_ASSERTIONS",
        "IDENTITY_PROVENANCE_AND_AUTHORIZED_HTTP_EVIDENCE",
    )),
    "AZ-T64-07": ("HEALTH_ENDPOINT_DECISION", (
        "NAMED_IN_SCOPE_TARGET_SERVICE_AND_API_VERSION",
        "PROOF_OF_ACTUAL_APPLICABLE_HEALTH_ENDPOINT_OR_NONE",
        "OWNER_SIGNED_REPLACEMENT_OR_RETAIN_ORIGINAL_DECISION",
    )),
    "AZ-T64-09": ("UI_ONLY_REQUIREMENT_DECISION", (
        "ACKNOWLEDGE_DOM_RENDERING_CANNOT_BE_PROVED_BY_REST",
        "OWNER_SIGNED_EXPLICIT_NA_OR_SEPARATE_SCHEMA_REQUIREMENT",
        "INDEPENDENT_IMPACT_AND_COVERAGE_REVIEW",
    )),
    "AZ-T64-11": ("AI_SEARCH_CONTRACT", (
        "APPROVED_INDEX_SCHEMA_API_VERSION_ENDPOINT_AND_AUDIENCE",
        "SYNTHETIC_QUERY_4XX_429_AND_PAGINATION_CONTRACT",
        "LIVE_RESPONSE_REQUIRES_AUTHORIZED_PRIVATE_RUNNER",
    )),
    "AZ-T64-13": ("AZURE_OPENAI_CONTRACT", (
        "APPROVED_DEPLOYMENT_API_VERSION_ENDPOINT_AND_AUDIENCE",
        "SYNTHETIC_RESPONSE_FAILURE_REDACTION_AND_POLICY_ASSERTIONS",
        "LIVE_INFERENCE_REQUIRES_SEPARATE_EXPLICIT_AUTHORIZATION",
    )),
    "AZ-T64-15": ("TOKEN_VALIDITY_CONTRACT", (
        "APPROVED_TOKEN_EXPIRY_AND_AUTHORIZATION_POLICY",
        "REJECTION_401_403_TEST_SCOPE_AND_EXPECTED_BEHAVIOR",
        "NO_UNPROVEN_TOKEN_REVOCATION_SEMANTICS",
    )),
    "AZ-T64-17": ("ERROR_AND_REDACTION_CONTRACT", (
        "APPROVED_SAFE_HTTP_ERROR_CLASSIFICATION",
        "SANITIZED_DIAGNOSTIC_LOGS_WITH_NEGATIVE_SECRET_TESTS",
        "PROTECTED_EVIDENCE_CUSTODY_AND_INDEPENDENT_REVIEW",
    )),
}
OPTIONS_DEFAULT = (
    "APPROVE_VERSIONED_REBASELINE_AFTER_EVIDENCE_AND_REVIEW",
    "REJECT_SCOPE_CHANGE_KEEP_ORIGINAL_REQUIREMENT",
    "DEFER_PENDING_EVIDENCE",
)
OPTIONS_SPECIAL = {
    "AZ-T64-07": (
        "APPROVE_VERSIONED_SERVICE_SPECIFIC_HEALTH_ENDPOINT",
        "RETAIN_ORIGINAL_REQUIREMENT",
        "DEFER_ENDPOINT_DECISION",
    ),
    "AZ-T64-09": (
        "APPROVE_EXPLICIT_NA_WITH_IMPACT_REVIEW",
        "APPROVE_SEPARATE_SCHEMA_REQUIREMENT_WITH_NEW_ID",
        "RETAIN_ORIGINAL_UI_REQUIREMENT",
        "DEFER_UI_SCOPE_DECISION",
    ),
}
EXPECTED_GROUP_COUNTS = {
    "RUNNER_TOPOLOGY": 2,
    "EVIDENCE_FORMAT": 1,
    "EVIDENCE_CUSTODY": 1,
    "REST_INTEGRATION": 1,
    "REST_TLS_INTEGRATION": 1,
    "REST_AUTHORIZATION": 1,
    "HEALTH_ENDPOINT_DECISION": 1,
    "UI_ONLY_REQUIREMENT_DECISION": 1,
    "AI_SEARCH_CONTRACT": 1,
    "AZURE_OPENAI_CONTRACT": 1,
    "TOKEN_VALIDITY_CONTRACT": 1,
    "ERROR_AND_REDACTION_CONTRACT": 1,
}


class DecisionError(ValueError):
    """An unapproved or drifting R41 source cannot be packaged as a decision."""


def contract_digest(case: dict) -> str:
    """Fingerprint only original and proposed fields, excluding any payload bytes."""
    if not isinstance(case, dict):
        raise DecisionError("R41 case must be an object")
    keys = (
        "id", "frozen_catalogue", "old_ref_path", "frozen_command",
        "frozen_expected", "proposed_disposition", "proposed_rest_check",
        "qualification", "approval",
    )
    if any(not isinstance(case.get(k), str) or not case[k] for k in keys):
        raise DecisionError("R41 source contract field missing")
    raw = json.dumps({key: case[key] for key in keys},
                     sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                     allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def packet(root: Path = ROOT, *, include_cases: bool = True) -> dict:
    root = Path(root)
    original_audit = inspect(root)
    if (original_audit.get("result") != "CROSSWALK_VERIFIED_PROPOSAL_UNAPPROVED"
            or original_audit.get("errors")
            or original_audit.get("reviewed_case_count") != 13
            or original_audit.get("original_id_count") != 1716
            or original_audit.get("approved") is not False
            or original_audit.get("api_unit_test_passes") != 0
            or original_audit.get("azure_live_passes") != 0
            or original_audit.get("release_decision") != "NO_GO"):
        raise DecisionError("the original frozen R41 crosswalk is not independently valid")
    source = read_json(root, PROPOSAL)
    originals = source.get("cases")
    if (not isinstance(originals, list)
            or [c.get("id") if isinstance(c, dict) else None for c in originals] != list(EXPECTED)
            or set(GATES) != set(EXPECTED)
            or set(EXPECTED_DISPOSITIONS) != set(EXPECTED)):
        raise DecisionError("R41 13-case membership or ordering changed")
    rows = {}
    counts = Counter()
    for original in originals:
        case_id = original["id"]
        group, evidence = GATES[case_id]
        if (len(evidence) != 3
                or original["proposed_disposition"] != EXPECTED_DISPOSITIONS[case_id]
                or original["approval"] != "PENDING_SCOPE_CHANGE_APPROVAL"
                or original["azure_live_acceptance"] != "NOT_READY"
                or original["api_unit_test_pass"] is not False
                or original["frozen_case_changed"] is not False
                or original["frozen_catalogue"] not in ORIGINALS
                or original["old_ref_path"] not in PATHS
                or case_id not in PATHS[original["old_ref_path"]]):
            raise DecisionError("case drift or unsafe approval promotion")
        counts[group] += 1
        rows[case_id] = {
            "frozen_catalogue": original["frozen_catalogue"],
            "old_ref_path": original["old_ref_path"],
            "immutable_contract_sha256": contract_digest(original),
            "proposed_disposition": original["proposed_disposition"],
            "review_group": group,
            "required_owner_and_reviewer_evidence_classes": list(evidence),
            "available_decision_options_NOT_SELECTED": list(
                OPTIONS_SPECIAL.get(case_id, OPTIONS_DEFAULT)),
            "owner_decision_selected": None,
            "scope_change_approved": False,
            "approved_endpoint_or_na": None,
            "signed_owner_evidence_verified": False,
            "independent_reviewer_signed": False,
            "original_command_executed": False,
            "azure_live_acceptance": "NOT_READY",
        }
    if dict(counts) != EXPECTED_GROUP_COUNTS:
        raise DecisionError("R41 source/decision group totals changed")
    return {
        "schema": SCHEMA,
        "status": "DECISION_PACKET_PREPARED_NOT_APPROVED",
        "historical_ids": 1716,
        "r41_cases": 13,
        "review_group_counts": dict(sorted(counts.items())),
        "scope_decisions_approved": 0,
        "owner_signatures_verified": 0,
        "independent_reviewer_signatures_verified": 0,
        "api_unit_test_passes_claimed": 0,
        "original_commands_executed": 0,
        "azure_live_passes": 0,
        "azure_not_ready": 1716,
        "release_decision": "NO_GO",
        "limitations": [
            "Choices are unselected options; none is a recorded owner approval",
            "The 13 immutable browser requirements are not replaced or marked N/A",
            "Existing REST fixture unit checks cannot prove private DNS, TLS, identity, UI or live behavior",
            "Independent signed scope decisions and versioned catalogue changes remain blocked",
        ],
        **({"cases": rows} if include_cases else {}),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path)
    p.add_argument("--summary-only", action="store_true")
    p.add_argument("--strict", action="store_true", help="return 2 pending authorized scope change")
    args = p.parse_args(argv)
    try:
        r = packet(args.root, include_cases=not args.summary_only)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(
                json.dumps(r, sort_keys=True, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    except (DecisionError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "R41_DECISION_PACKET_BLOCKED",
                          "error_type": type(exc).__name__,
                          "release_decision": "NO_GO",
                          "azure_live_passes": 0}))
        return 1
    print(json.dumps({k: v for k, v in r.items() if k != "cases"},
                     sort_keys=True, ensure_ascii=False, indent=2))
    return 2 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
