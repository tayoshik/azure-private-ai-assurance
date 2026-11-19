#!/usr/bin/env python3
"""Ten more source-grounded P1 evidence comparisons. OFFLINE, ALWAYS NO_GO.

The observations AND the allegedly approved baselines are untrusted local JSON.
This tool neither verifies an approval signature nor invokes Azure, a runner,
a browser or a network probe. Matching local values => REVIEW_REQUIRED only.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import ipaddress
import json
from pathlib import Path
import re

if __package__:
    from . import review_p1_evidence_correlation as base
else:
    import review_p1_evidence_correlation as base

CASES = {
    "AZ-T35-13": "SEARCH_AUTHENTICATED_QUERY",
    "AZ-T40-13": "PRIVATE_SCM_DEPLOYED_ARTIFACT",
    "AZ-T41-11": "SEARCH_INDEXER_PRIVATE_SOURCE",
    "AZ-T42-17": "TOKEN_REDACTION_NEGATIVE_AND_POSITIVE_CONTROLS",
    "AZ-T43-17": "COSMOS_UNAUTHORIZED_PRINCIPAL_DENIED",
    "AZ-T48-21": "PROMPT_CREDENTIAL_PII_REDACTION_CONTROLS",
    "AZ-T49-15": "APP_TO_THREE_PRIVATE_DEPENDENCIES",
    "AZ-T50-19": "ACR_PULL_APPROVED_PRIVATE_RUNNER",
    "AZ-T56-19": "PRIVATE_FLOW_LOG_CORRELATION",
    "AZ-T58-07": "SIGNED_RELEASE_COMMIT_PLAN_BINDING_REVIEW",
}
SOURCE_COMMIT = re.compile(r"^[0-9a-f]{40}$")
MAX_DOC_BYTES = 2_000_000


def truth(row, key, expected=True):
    base.need(type(row.get(key)) is bool, "MISSING_OR_NOT_BOOLEAN_" + key.upper())
    base.agree(row[key] is expected, "UNEXPECTED_" + key.upper())


def ip_private(value):
    ip = base.address(value)
    base.agree(ip.is_private and not ip.is_loopback and not ip.is_link_local
               and not ip.is_unspecified, "IP_NOT_PRIVATE")
    return str(ip)


def approved_pe(value, allowed, label):
    ip = ip_private(value)
    base.need(base.strings(allowed), "MISSING_APPROVED_PE_SET_" + label)
    good = {ip_private(entry) for entry in allowed}
    base.agree(ip in good, "PE_NOT_IN_APPROVED_SET_" + label)


def strict_int(x, *, minimum=0, label="NUMBER"):
    base.need(type(x) is int and x >= minimum, "INVALID_" + label)
    return x


def text_value(v, label):
    base.need(base.text(v), "MISSING_" + label)
    return v


def same(o, a, *names):
    for name in names:
        base.exact_field(o, a, name)


def matching_sha(o, a, key):
    same(o, a, key)
    base.need(base.digest(o[key]) and base.digest(a[key]),
              "INVALID_SHA256_" + key.upper())


def check(case_id, o, a):
    if case_id == "AZ-T35-13":
        same(o, a, "search_resource_id", "index_name", "principal_id",
             "runner_resource_id", "query_id")
        base.agree(text_value(o.get("auth_method"), "SEARCH_AUTH") == "managed_identity",
                   "SEARCH_AUTH_NOT_MI")
        base.agree(strict_int(o.get("http_status"), label="SEARCH_HTTP") == 200,
                   "SEARCH_QUERY_NOT_SUCCESS")
        truth(o, "private_route_observed")
        got, wanted = o.get("returned_synthetic_doc_ids"), a.get("expected_synthetic_doc_ids")
        base.need(base.strings(got) and base.strings(wanted),
                  "MISSING_SYNTHETIC_SEARCH_DOCS")
        base.agree(set(got) == set(wanted), "SEARCH_RESULTS_DO_NOT_MATCH_APPROVED_FIXTURE")
    elif case_id == "AZ-T40-13":
        same(o, a, "app_resource_id", "runner_resource_id", "scm_hostname",
             "deployment_id", "source_commit_sha")
        matching_sha(o, a, "artifact_sha256")
        base.need(bool(SOURCE_COMMIT.fullmatch(o["source_commit_sha"])),
                  "INVALID_SOURCE_COMMIT")
        approved_pe(o.get("scm_private_ip"), a.get("approved_scm_pe_ips"), "SCM")
        truth(o, "tls_verified")
        truth(o, "private_route_observed")
        base.agree(text_value(o.get("deployment_status"), "DEPLOYMENT_STATUS") == "Succeeded",
                   "DEPLOYMENT_NOT_SUCCEEDED")
    elif case_id == "AZ-T41-11":
        same(o, a, "indexer_resource_id", "datasource_resource_id",
             "indexer_principal_id", "datasource_hostname")
        approved_pe(o.get("datasource_private_ip"), a.get("approved_datasource_pe_ips"),
                    "DATASOURCE")
        truth(o, "private_route_observed")
        base.agree(text_value(o.get("connection_status"), "INDEXER_CONN_STATUS") == "Succeeded",
                   "INDEXER_PRIVATE_CONNECTION_NOT_SUCCEEDED")
        text_value(o.get("correlation_id"), "INDEXER_REQUEST_CORRELATION")
    elif case_id == "AZ-T42-17":
        same(o, a, "policy_revision", "scan_scope_id")
        scans = o.get("artifact_scans")
        base.need(type(scans) is dict and set(scans) ==
                  {"pipeline_logs", "application_logs", "traces"},
                  "MISSING_TOKEN_SANITIZATION_SCAN_COVERAGE")
        for key in sorted(scans):
            item = scans[key]
            base.need(type(item) is dict, "BAD_SCAN_RECORD_" + key.upper())
            strict_int(item.get("scanned_artifact_count"), minimum=1,
                       label="SCANNED_ARTIFACTS_" + key.upper())
            strict_int(item.get("positive_control_detections"), minimum=1,
                       label="SCAN_POSITIVE_CONTROL_" + key.upper())
            leaked = strict_int(item.get("unredacted_token_findings"),
                                label="TOKEN_FINDINGS_" + key.upper())
            base.agree(leaked == 0, "UNREDACTED_TOKEN_IN_" + key.upper())
            text_value(item.get("sanitized_scan_ref"), "SCAN_REFERENCE_" + key.upper())
        truth(o, "raw_token_logged", False)
    elif case_id == "AZ-T43-17":
        same(o, a, "unauthorized_principal_id", "container_resource_id",
             "denied_operation", "request_id")
        base.agree(text_value(o.get("result"), "COSMOS_NEGATIVE_RESULT") == "Denied",
                   "COSMOS_UNAUTHORIZED_ACCESS_NOT_DENIED")
        base.agree(strict_int(o.get("http_status"), label="COSMOS_DENY_HTTP") == 403,
                   "COSMOS_DENIAL_HTTP_UNEXPECTED")
        truth(o, "account_key_used", False)
        text_value(o.get("audit_log_correlation_id"), "COSMOS_DENIAL_AUDIT")
    elif case_id == "AZ-T48-21":
        same(o, a, "redaction_policy_revision", "pipeline_scope_id",
             "synthetic_test_fixture_id")
        controls = o.get("redaction_controls")
        base.need(type(controls) is dict and set(controls) ==
                  {"prompt", "credentials", "personal_data"},
                  "MISSING_THREE_REDACTION_CLASSES")
        for key in sorted(controls):
            item = controls[key]
            base.need(type(item) is dict, "BAD_REDACTION_CLASS_" + key)
            strict_int(item.get("synthetic_marker_count"), minimum=1,
                       label="REDACTION_INPUT_" + key)
            strict_int(item.get("masking_positive_control_detected"), minimum=1,
                       label="REDACTION_POSITIVE_CONTROL_" + key)
            leaked = strict_int(item.get("unredacted_marker_findings"),
                                label="UNREDACTED_MARKERS_" + key)
            base.agree(leaked == 0, "SENSITIVE_MARKER_EXPOSED_" + key)
            text_value(item.get("sanitized_evidence_ref"), "REDACTION_REF_" + key)
    elif case_id == "AZ-T49-15":
        same(o, a, "app_resource_id", "app_principal_id", "runner_resource_id")
        actual, expected = o.get("dependencies"), a.get("approved_private_endpoints")
        needed = {"openai", "search", "cosmos"}
        base.need(type(actual) is dict and type(expected) is dict and
                  set(actual) == needed and set(expected) == needed,
                  "DEPENDENCY_SET_INCOMPLETE")
        for key in sorted(needed):
            row, control = actual[key], expected[key]
            base.need(type(row) is dict and type(control) is dict,
                      "BAD_DEPENDENCY_RECORD_" + key)
            same(row, control, "resource_id", "hostname")
            approved_pe(row.get("resolved_private_ip"), control.get("approved_pe_ips"),
                        key.upper())
            base.agree(strict_int(row.get("port"), minimum=1, label="PORT_"+key) == 443,
                       "DEPENDENCY_PORT_NOT_443_" + key)
            truth(row, "tls_verified")
            truth(row, "private_route_observed")
            base.agree(text_value(row.get("status"), "DEPENDENCY_STATUS_"+key) == "Succeeded",
                       "DEPENDENCY_NOT_SUCCESSFUL_" + key)
    elif case_id == "AZ-T50-19":
        same(o, a, "acr_resource_id", "runner_resource_id", "repository_name",
             "source_commit_sha")
        matching_sha(o, a, "image_digest")
        base.need(bool(SOURCE_COMMIT.fullmatch(o["source_commit_sha"])),
                  "INVALID_IMAGE_SOURCE_COMMIT")
        ip = ip_private(o.get("runner_source_ip"))
        base.in_cidrs(base.address(ip), a.get("approved_runner_cidrs"),
                      "UNAPPROVED_ACR_RUNNER_NETWORK")
        approved_pe(o.get("acr_private_ip"), a.get("approved_acr_pe_ips"), "ACR")
        truth(o, "private_route_observed")
        truth(o, "raw_registry_credential_logged", False)
        base.agree(text_value(o.get("pull_status"), "ACR_PULL_STATUS") == "Succeeded",
                   "ACR_PULL_FAILED")
    elif case_id == "AZ-T56-19":
        same(o, a, "gateway_resource_id", "request_id", "runner_resource_id")
        rows = o.get("observed_flows")
        expected = a.get("approved_destination_pe_ips")
        base.need(type(rows) is list and 2 <= len(rows) <= 64 and
                  base.strings(expected), "INSUFFICIENT_FLOW_LOG_COVERAGE")
        allowed = {ip_private(x) for x in expected}
        observed_destinations, flow_ids = set(), []
        for row in rows:
            base.need(type(row) is dict, "BAD_FLOW_ROW")
            base.agree(text_value(row.get("request_id"), "FLOW_REQUEST") == o["request_id"],
                       "FLOW_FOR_DIFFERENT_REQUEST")
            src = base.address(row.get("source_ip"))
            base.in_cidrs(src, a.get("approved_source_cidrs"),
                          "FLOW_SOURCE_OUTSIDE_APPROVED_CIDR")
            dest = ip_private(row.get("destination_ip"))
            base.agree(dest in allowed, "FLOW_REACHED_UNAPPROVED_DESTINATION")
            observed_destinations.add(dest)
            base.agree(strict_int(row.get("destination_port"), minimum=1,
                                  label="FLOW_DESTINATION_PORT") == 443,
                       "FLOW_DESTINATION_PORT_NOT_443")
            text_value(row.get("collector_id"), "FLOW_COLLECTOR")
            flow_ids.append(text_value(row.get("flow_log_id"), "FLOW_LOG_ID"))
        base.agree(len(set(flow_ids)) == len(flow_ids), "DUPLICATE_FLOW_LOG_IDENTIFIER")
        base.agree(observed_destinations == allowed, "FLOW_DESTINATION_SET_INCOMPLETE")
    elif case_id == "AZ-T58-07":
        same(o, a, "deployment_scope_id", "change_ticket", "release_actor_id",
             "source_commit_sha", "approved_commit_sha", "plan_source_commit_sha")
        matching_sha(o, a, "plan_sha256")
        for key in ("source_commit_sha", "approved_commit_sha", "plan_source_commit_sha"):
            base.need(bool(SOURCE_COMMIT.fullmatch(o[key])),
                      "INVALID_COMMIT_SHA_" + key.upper())
        base.agree(o["source_commit_sha"] == o["approved_commit_sha"] ==
                   o["plan_source_commit_sha"], "PLAN_COMMIT_DIFFERS_FROM_APPROVED_SOURCE")
        base.need(base.text(a.get("approved_reviewer_id")), "MISSING_APPROVED_REVIEWER")
        base.need(base.text(o.get("reviewer_id")), "MISSING_ACTUAL_REVIEWER")
        base.agree(o["reviewer_id"] == a["approved_reviewer_id"] and
                   o["reviewer_id"] != o["release_actor_id"],
                   "APPROVAL_REVIEWER_NOT_INDEPENDENT")
    else:
        raise base.Incomplete("UNKNOWN_CASE")


def assess(case_id, observation, approved, *, now=None):
    result, reason = "NOT_READY", "UNVERIFIED_OR_MALFORMED_INPUT"
    try:
        base.need(case_id in CASES, "UNKNOWN_CASE")
        base.need(type(observation) is dict and type(approved) is dict,
                  "OBSERVATION_OR_BASELINE_MISSING")
        om, am = observation.get("metadata"), approved.get("metadata")
        base.need(type(om) is dict and type(am) is dict, "SOURCE_METADATA_MISSING")
        for key in ("case_id", "resource_id", "runner_id", "source_sha256"):
            same(om, am, key)
        base.agree(om["case_id"] == case_id, "CASE_ID_DIFFERS")
        base.need(base.digest(om["source_sha256"]) and base.digest(am["source_sha256"]),
                  "SOURCE_SHA256_INVALID")
        base.need(base.digest(am.get("approval_record_sha256")),
                  "APPROVAL_RECORD_DIGEST_MISSING")
        base.observed_at(om.get("observed_at_utc"),
                         now if now is not None else datetime.now(timezone.utc))
        o, a = observation.get("observation"), approved.get("expected")
        base.need(type(o) is dict and type(a) is dict, "CONTROL_SPECIFIC_VALUES_MISSING")
        check(case_id, o, a)
        result, reason = "REVIEW_REQUIRED", "UNTRUSTED_LOCAL_MATCH_REQUIRES_INDEPENDENT_ATTESTATION"
    except base.Incomplete as ex:
        result, reason = "NOT_READY", str(ex)
    except base.Mismatch as ex:
        result, reason = "DIFFERENCE_REVIEW_REQUIRED", str(ex)
    except (KeyError, TypeError, ValueError, OverflowError):
        result, reason = "NOT_READY", "INVALID_FIELD_OR_TYPE"
    return {
        "schema": "azure-p1-source-evidence-correlation/v1",
        "case_id": case_id,
        "review_kind": CASES.get(case_id, "UNKNOWN_CASE"),
        "result": result,
        "reason_code": reason,
        "origin_signature_verified": False,
        "actual_runner_and_network_verified": False,
        "approval_authority_verified": False,
        "real_runtime_semantics_verified": False,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
    }


def load(path):
    if path.stat().st_size > MAX_DOC_BYTES:
        raise ValueError("oversize input")
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case-id", required=True)
    p.add_argument("--observation", type=Path, required=True)
    p.add_argument("--approved", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        obs, baseline = load(args.observation), load(args.approved)
    except (OSError, UnicodeError, ValueError, TypeError):
        obs = baseline = None
    print(json.dumps(assess(args.case_id, obs, baseline),
                     ensure_ascii=False, sort_keys=True))
    return 2  # never authorize release from self-reported local data


if __name__ == "__main__":
    raise SystemExit(main())
