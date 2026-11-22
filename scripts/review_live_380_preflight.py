#!/usr/bin/env python3
"""L1: source-only owner preflight of 380 Azure/private-runner-required tests.

NEVER execute canonical commands, call a cloud service, obtain credentials,
run network probes or authorize Terraform/WAF. Per-ID records are metadata only.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shlex

from audit_tool_semantics_13 import load_sources
from build_execution_route_1716 import (
    ROOT, ROUTE_LIVE, build as build_routes, digest_case,
)

SCHEMA = "azure-live-380-risk-review/v1"
WAF_IDS = frozenset({"AZ-T69-05", "AZ-T69-07", "AZ-T69-09"})
EXTERNAL_DNS_ID = "AZ-T18-05"
WAF = "P0_ACTIVE_WAF_TRAFFIC_REQUIRES_EXPLICIT_TICKET"
TERRAFORM = "P0_TERRAFORM_PLAN_STATE_AND_LOCK_REVIEW"
EXTERNAL_DNS = "P0_EXTERNAL_DNS_QUERY_EXPOSURE_REVIEW"
HTTP = "P1_HTTP_TLS_OBSERVATION_REVIEW"
TLS = "P1_TLS_PEER_OBSERVATION_REVIEW"
DNS = "P1_PRIVATE_DNS_SCOPE_REVIEW"
AZ = "P1_AZURE_CLI_OPERATION_AND_SCOPE_REVIEW"
GROUPS = (WAF, TERRAFORM, EXTERNAL_DNS, HTTP, TLS, DNS, AZ)
EXPECTED_COUNTS = {
    WAF: 3, TERRAFORM: 11, EXTERNAL_DNS: 1, HTTP: 8,
    TLS: 3, DNS: 33, AZ: 321,
}
FAMILIES = {"az": 321, "dig": 33, "curl": 11, "getent": 1,
            "terraform": 11, "openssl": 3}
GATES = {
    WAF: (
        "SIGNED_NONPROD_WAF_SCOPE_TEST_WINDOW_RATE_LIMIT_AND_APPROVED_VECTORS",
        "INDEPENDENT_WAF_TEST_TICKET_AND_APPROVED_OPERATOR",
        "CONTROLLED_RESPONSE_LOGS_AND_POST_TEST_REVIEW",
    ),
    TERRAFORM: (
        "APPROVED_PRIVATE_BACKEND_IDENTITY_AND_STATE_ACCESS",
        "PLAN_REFRESH_LOCK_SIDE_EFFECT_AND_STATE_CUSTODY_REVIEW",
        "PINNED_TERRAFORM_PROVIDER_AND_INDEPENDENT_PLAN_BASELINE",
    ),
    EXTERNAL_DNS: (
        "APPROVED_EXTERNAL_RECURSOR_CONTACT_AND_DATA_LEAKAGE_SCOPE",
        "EXPLICIT_TEST_ORIGIN_FQDN_AND_RESOLVER_AUTHORIZATION",
        "RECORDED_DNS_OBSERVATION_WITHOUT_ISOLATION_PASS_INFERENCE",
    ),
    HTTP: (
        "APPROVED_PROBE_ORIGIN_EXACT_FQDN_AND_READ_ONLY_METHOD",
        "TARGET_TLS_AND_NO_PROXY_NETWORK_EGRESS_REVIEW",
        "HTTP_STATUS_REMOTE_IP_NOT_SUFFICIENT_TO_PROVE_ISOLATION",
    ),
    TLS: (
        "APPROVED_REMOTE_TLS_HOST_PORT_AND_PRIVATE_RUNNER",
        "TRUST_ROOT_CERTIFICATE_HOSTNAME_CHAIN_AND_EXPIRY_REVIEW",
        "TCP_TLS_OBSERVATION_NOT_PROOF_OF_AZURE_CONFIG_OR_ROUTING",
    ),
    DNS: (
        "APPROVED_RESOLVER_AND_NETWORK_ORIGIN_SCOPE",
        "PINNED_EXPECTED_RECORD_CNAME_AND_PRIVATE_PE_NIC_MAPPING",
        "RESOLUTION_ALONE_IS_NOT_PRIVATE_CONNECTIVITY_PROOF",
    ),
    AZ: (
        "EXACT_AZ_SUBCOMMAND_FLAGS_AND_ALL_EXPANSIONS_REVIEW",
        "APPROVED_SUBSCRIPTION_TENANT_RESOURCE_SCOPE_AND_WORKLOAD_IDENTITY",
        "INDEPENDENT_OBSERVATION_PREDICATE_AND_EVIDENCE_CUSTODY",
    ),
}


class LiveReviewError(ValueError):
    """Unknown, drifting or unreviewed original command shape."""


def classify(ident: str, command: str) -> tuple[str, str]:
    """Lexical risk category only. No shell evaluation or command execution."""
    if not isinstance(ident, str) or not isinstance(command, str) or not command.strip():
        raise LiveReviewError("original ID/command is missing")
    try:
        argv = shlex.split(command, posix=True)
    except ValueError as exc:
        raise LiveReviewError("unparseable original command must be manually reviewed") from exc
    if not argv:
        raise LiveReviewError("blank command")
    head = argv[0]
    if head == "curl":
        if ident in WAF_IDS:
            if ("--data-urlencode" not in argv or "--get" not in argv
                    or "X-Test-ID:" not in command
                    or "WAF_TEST_URL" not in command):
                raise LiveReviewError("WAF attack-vector command no longer matches review class")
            return WAF, head
        if ("--data-urlencode" in argv or "--get" in argv
                or any(x in argv for x in ("--request", "-X", "--data", "-d", "--upload-file", "-T"))):
            raise LiveReviewError("unreviewed HTTP method or request body")
        if not any(x in argv for x in ("-o", "--output")):
            raise LiveReviewError("probe response output requires independent review")
        return HTTP, head
    if ident in WAF_IDS:
        raise LiveReviewError("WAF target no longer starts with curl")
    if head == "terraform":
        if not re.match(r"^terraform(?:\s+-\S+)*\s+plan\b", command):
            raise LiveReviewError("unexpected live Terraform command")
        if "-detailed-exitcode" not in argv or "-no-color" not in argv:
            raise LiveReviewError("Terraform plan output/exit contract changed")
        return TERRAFORM, head
    if head == "dig":
        if ident == EXTERNAL_DNS_ID:
            if not any(x == "@1.1.1.1" for x in argv):
                raise LiveReviewError("externally scoped DNS command changed")
            return EXTERNAL_DNS, head
        if any(x.startswith("@") and re.match(r"^@\d+\.\d+\.\d+\.\d+$", x) for x in argv):
            raise LiveReviewError("unreviewed literal external resolver in private DNS queue")
        return DNS, head
    if ident == EXTERNAL_DNS_ID:
        raise LiveReviewError("external DNS review case has changed family")
    if head == "getent":
        return DNS, head
    if head == "openssl":
        if len(argv) < 3 or argv[1] != "s_client":
            raise LiveReviewError("unexpected OpenSSL operation")
        return TLS, head
    if head == "az":
        if len(argv) < 3:
            raise LiveReviewError("Azure CLI operation incomplete")
        return AZ, head
    raise LiveReviewError("unreviewed direct live command family")


def build_review(root: Path = ROOT, *, include_cases: bool = True) -> dict:
    root = Path(root)
    routes = build_routes(root, include_cases=True)
    if (routes["status"] != "ROUTING_INVENTORY_ONLY" or routes["errors"]
            or routes["canonical_test_ids"] != 1716
            or routes["route_counts"].get(ROUTE_LIVE) != 380):
        raise LiveReviewError("upstream source-only 1716 routing invalid")
    source = load_sources(root)
    targets = {i: row for i, row in routes["cases"].items()
               if row["route"] == ROUTE_LIVE}
    if len(targets) != 380:
        raise LiveReviewError("source live queue count changed")
    rows = {}
    counts, families = Counter(), Counter()
    for ident, row in sorted(targets.items()):
        original = source.get(ident)
        if (not original or digest_case(original) != row["catalogue_contract_sha256"]
                or row["azure_live_acceptance"] != "NOT_READY"
                or row["source_test_executed"] is not False
                or row["approved_inputs_verified"] is not False
                or row["independent_reviewer_signed"] is not False):
            raise LiveReviewError("source provenance or Azure acceptance drift")
        category, family = classify(ident, original.get("command"))
        if family != row["direct_command_family"]:
            raise LiveReviewError("source command family/route drift")
        counts[category] += 1
        families[family] += 1
        rows[ident] = {
            "canonical_catalogue": row["canonical_catalogue"],
            "catalogue_contract_sha256": row["catalogue_contract_sha256"],
            "direct_command_family": family,
            "review_priority": category,
            "review_checklist": list(GATES[category]),
            "owner_authorized_execution": False,
            "private_runner_oidc_verified": False,
            "approved_nonproduction_target_verified": False,
            "original_command_executed": False,
            "approved_input_or_expected_baseline_verified": False,
            "independent_reviewer_signed": False,
            "azure_live_acceptance": "NOT_READY",
        }
    if dict(counts) != EXPECTED_COUNTS or dict(families) != FAMILIES:
        raise LiveReviewError("live queue source counts changed; independent review required")
    if set(rows) != set(targets):
        raise LiveReviewError("not all live IDs reviewed")
    return {
        "schema": SCHEMA,
        "status": "LIVE_EXECUTION_PRECHECK_ONLY_NOT_AUTHORIZED",
        "total_canonical_ids": 1716,
        "source_only_live_candidates": 380,
        "review_priority_counts": {c: counts[c] for c in GROUPS},
        "direct_command_family_counts": {k: families[k] for k in FAMILIES},
        "owner_authorized_cases": 0,
        "approved_private_runner_cases": 0,
        "canonical_commands_executed": 0,
        "azure_live_passes": 0,
        "azure_not_ready": 1716,
        "release_decision": "NO_GO",
        "limitations": [
            "Source lexical grouping is not a complete shell safety proof or execution permission",
            "WAF request vectors require explicit approval and must never run from public CI",
            "Terraform plan may interact with backend/state and is not an offline syntax check",
            "Azure CLI, DNS and TLS command observations cannot prove the effective security control",
            "No approved target identity, private runner, restricted evidence or independent review provided",
        ],
        **({"cases": rows} if include_cases else {}),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path)
    p.add_argument("--summary-only", action="store_true")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args(argv)
    try:
        r = build_review(args.root, include_cases=not args.summary_only)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(r, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    except (LiveReviewError, ValueError, TypeError, KeyError, OSError) as exc:
        print(json.dumps({"status": "LIVE_PRECHECK_BLOCKED",
                          "error_type": type(exc).__name__,
                          "azure_live_passes": 0,
                          "release_decision": "NO_GO"}))
        return 1
    print(json.dumps({k: v for k, v in r.items() if k != "cases"},
                     sort_keys=True, ensure_ascii=False, indent=2))
    return 2 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
