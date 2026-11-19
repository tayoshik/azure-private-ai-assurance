#!/usr/bin/env python3
"""Offline source-linked discrepancy review for 10 more P1 network/identity/WAF/monitor cases.

Inputs are untrusted local observations and claimed baselines.  No command
from the catalogue is run, no network call, Azure authentication, real identity,
signed evidence verification or browser testing occurs.  Every CLI use exits 2.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import ipaddress
import json
import math
from pathlib import Path

if __package__:
    from . import review_p1_evidence_correlation as base
else:
    import review_p1_evidence_correlation as base

CASES = {
    "AZ-T18-19": "EXTERNAL_CONFIG_VS_NETWORK",
    "AZ-T19-19": "MANAGED_IDENTITY_RUNNER_SMOKE",
    "AZ-T41-09": "SEARCH_INDEXER_PRIVATE_DNS",
    "AZ-T42-21": "UNAUTHORIZED_PRINCIPAL_DENIAL",
    "AZ-T48-17": "AI_DEPENDENCY_DNS",
    "AZ-T49-17": "PUBLIC_EGRESS_DENIAL",
    "AZ-T51-21": "WAF_POLICY_CHANGE_AND_ROLLBACK",
    "AZ-T55-21": "GATEWAY_BACKEND_REQUEST_CORRELATION",
    "AZ-T57-17": "LOG_INGEST_P95_FROM_TIMESTAMPS",
    "AZ-T57-21": "AUTHORIZATION_SCOPED_ALERT_DELIVERY",
}
MAX_DOC_BYTES = 2_000_000


def valid_number(x):
    return type(x) in (int, float) and math.isfinite(x) and x >= 0


def timestamp(x):
    base.need(base.text(x), "MISSING_UTC_TIMESTAMP")
    try:
        dt = datetime.fromisoformat(x.replace("Z", "+00:00"))
    except ValueError:
        raise base.Incomplete("BAD_UTC_TIMESTAMP") from None
    base.need(dt.tzinfo is not None, "TIMESTAMP_WITHOUT_TIMEZONE")
    return dt.astimezone(timezone.utc)


def approved_ips(raw):
    base.need(base.strings(raw), "MISSING_APPROVED_PRIVATE_ENDPOINT_IPS")
    out = []
    for item in raw:
        ip = base.address(item)
        base.need(ip.is_private and not ip.is_loopback and not ip.is_link_local,
                  "APPROVED_PE_ADDRESS_NOT_PRIVATE")
        out.append(str(ip))
    return set(out)


def require_same(o, a, *keys):
    for key in keys:
        base.exact_field(o, a, key)


def positive_int(x, reason):
    base.need(type(x) is int and x > 0, reason)


def compare_control(case_id, obs, approved):
    """Typed comparison; raises Incomplete or Mismatch, never issues PASS."""
    if case_id == "AZ-T18-19":
        require_same(obs, approved, "target_resource_id", "expected_block_rule_id")
        src = base.address(obs.get("probe_source_ip"))
        base.in_cidrs(src, approved.get("approved_external_probe_cidrs"),
                      "EXTERNAL_PROBE_UNAPPROVED")
        base.obs_false(obs, "effective_public_network_access")
        base.need(base.text(obs.get("external_probe_result")), "MISSING_EXTERNAL_PROBE")
        base.agree(obs["external_probe_result"] == "Denied", "EXTERNAL_PROBE_NOT_DENIED")
        base.need(base.text(obs.get("blocking_rule_id")), "MISSING_OBSERVED_BLOCK_RULE")
        base.agree(obs["blocking_rule_id"] == approved["expected_block_rule_id"],
                   "DENIAL_NOT_CORRELATED_WITH_APPROVED_RULE")
        base.need(base.text(obs.get("correlation_id")), "MISSING_NETWORK_CORRELATION")
    elif case_id == "AZ-T19-19":
        require_same(obs, approved, "principal_id", "role_scope", "token_audience")
        base.need(base.text(obs.get("auth_method")), "MISSING_AUTH_METHOD")
        base.agree(obs["auth_method"] == "managed_identity", "NON_MANAGED_IDENTITY_AUTH")
        base.obs_true(obs, "token_obtained")
        base.obs_false(obs, "raw_token_logged")
        base.need(base.text(obs.get("correlation_id")), "MISSING_AUTH_CORRELATION")
    elif case_id == "AZ-T41-09":
        require_same(obs, approved, "resolver_id", "indexer_hostname")
        addrs = obs.get("resolved_ip_addresses")
        base.need(base.strings(addrs), "MISSING_OBSERVED_DNS_ADDRESSES")
        actual = set()
        for s in addrs:
            ip = base.address(s)
            base.agree(ip.is_private and not ip.is_loopback and not ip.is_link_local,
                       "INDEXER_DNS_RETURNED_NON_PRIVATE_IP")
            actual.add(str(ip))
        expected = approved_ips(approved.get("approved_pe_ips"))
        base.agree(actual == expected, "INDEXER_DNS_PE_SET_DIFFERS")
        base.need(base.text(obs.get("query_id")), "MISSING_DNS_QUERY_ID")
    elif case_id == "AZ-T42-21":
        require_same(obs, approved, "unauthorized_principal_id", "operation")
        base.obs_true(obs, "denied")
        code = obs.get("http_status")
        base.need(type(code) is int, "MISSING_DENIAL_HTTP_STATUS")
        base.agree(code == 403, "DENIAL_STATUS_NOT_EXPECTED")
        base.need(base.text(obs.get("audit_correlation_id")), "MISSING_DENY_AUDIT_CORRELATION")
    elif case_id == "AZ-T48-17":
        require_same(obs, approved, "resolver_id")
        actual, expected = obs.get("answers"), approved.get("approved_private_answers")
        needed = {"openai", "search", "cosmos"}
        base.need(type(actual) is dict and type(expected) is dict and
                  set(actual) == needed and set(expected) == needed,
                  "MISSING_AI_DNS_RESOLUTION_SET")
        for key in sorted(needed):
            a, e = actual[key], expected[key]
            base.need(type(a) is dict and type(e) is dict,
                      "INVALID_DNS_ANSWER_" + key.upper())
            base.need(base.text(a.get("status")), "MISSING_DNS_STATUS")
            base.agree(a["status"] == "Resolved", "DNS_NOT_RESOLVED_" + key.upper())
            require_same(a, e, "hostname")
            base.need(base.strings(a.get("addresses")), "MISSING_DNS_ADDRESSES")
            ips = set()
            for raw in a["addresses"]:
                ip = base.address(raw)
                base.agree(ip.is_private and not ip.is_loopback and not ip.is_link_local,
                           "DNS_RETURNED_PUBLIC_ADDRESS_" + key.upper())
                ips.add(str(ip))
            base.agree(ips == approved_ips(e.get("approved_pe_ips")),
                       "DNS_PE_SET_MISMATCH_" + key.upper())
    elif case_id == "AZ-T49-17":
        records = obs.get("public_probes")
        targets = approved.get("approved_public_targets")
        base.need(type(records) is list and type(targets) is list and len(records) >= 2
                  and base.strings(targets) and len(records) == len(targets),
                  "MISSING_PUBLIC_EGRESS_TEST_SET")
        got = []
        for item in records:
            base.need(type(item) is dict, "BAD_PUBLIC_EGRESS_RECORD")
            dest = base.address(item.get("destination_ip"))
            base.need(dest.is_global, "PUBLIC_TEST_TARGET_NOT_GLOBAL")
            got.append(str(dest))
            base.need(base.text(item.get("outcome")), "MISSING_EGRESS_OUTCOME")
            base.agree(item["outcome"] == "Denied", "UNAPPROVED_PUBLIC_EGRESS_SUCCEEDED")
            base.need(base.text(item.get("flow_log_id")), "MISSING_EGRESS_FLOW_LOG")
        base.agree(set(got) == set(targets) and len(set(got)) == len(got),
                   "PUBLIC_EGRESS_TARGET_SET_MISMATCH")
        src = base.address(obs.get("source_ip"))
        base.in_cidrs(src, approved.get("approved_source_cidrs"),
                      "PUBLIC_EGRESS_SOURCE_NOT_APPROVED")
    elif case_id == "AZ-T51-21":
        require_same(obs, approved, "policy_resource_id", "policy_revision",
                     "change_ticket", "reviewer_id")
        approved_rules = approved.get("approved_rule_ids")
        effective_rules = obs.get("effective_rule_ids")
        base.need(base.strings(approved_rules) and base.strings(effective_rules),
                  "MISSING_WAF_RULE_INVENTORY")
        base.agree(set(approved_rules) == set(effective_rules), "WAF_RULE_SET_DIFFERS")
        approved_exceptions = approved.get("approved_exception_rule_ids")
        actual_exceptions = obs.get("exception_rule_ids")
        base.need(base.strings(approved_exceptions, allow_empty=True) and
                  base.strings(actual_exceptions, allow_empty=True),
                  "MISSING_WAF_EXCEPTION_INVENTORY")
        base.agree(set(actual_exceptions) == set(approved_exceptions),
                   "UNAPPROVED_WAF_EXCEPTION")
        base.need(base.text(obs.get("rollback_revision")), "MISSING_WAF_ROLLBACK_REVISION")
        base.agree(obs["rollback_revision"] != obs["policy_revision"],
                   "WAF_ROLLBACK_NOT_SEPARATE_REVISION")
    elif case_id == "AZ-T55-21":
        require_same(obs, approved, "gateway_resource_id", "backend_resource_id", "request_id")
        a, b = obs.get("appgw_access"), obs.get("app_service")
        base.need(type(a) is dict and type(b) is dict,
                  "MISSING_GATEWAY_AND_BACKEND_RECORDS")
        for name, item in (("GATEWAY", a), ("BACKEND", b)):
            base.need(base.text(item.get("request_id")) and
                      base.text(item.get("resource_id")),
                      "INCOMPLETE_" + name + "_TRACE")
            base.agree(item["request_id"] == obs["request_id"],
                       name + "_REQUEST_ID_MISMATCH")
        base.agree(a["resource_id"] == obs["gateway_resource_id"],
                   "GATEWAY_RESOURCE_ID_MISMATCH")
        base.agree(b["resource_id"] == obs["backend_resource_id"],
                   "BACKEND_RESOURCE_ID_MISMATCH")
        ta, tb = timestamp(a.get("observed_at_utc")), timestamp(b.get("observed_at_utc"))
        base.agree(abs((tb - ta).total_seconds()) <= 120,
                   "GATEWAY_BACKEND_TRACE_TIME_GAP")
        base.need(base.text(a.get("route")), "MISSING_GATEWAY_ROUTE")
        base.agree(a["route"] == "private", "GATEWAY_ROUTE_NOT_PRIVATE")
    elif case_id == "AZ-T57-17":
        samples = obs.get("ingestion_samples")
        base.need(type(samples) is list and 20 <= len(samples) <= 5000,
                  "INSUFFICIENT_OR_OVERSIZE_INGEST_SAMPLES")
        delays = []
        for row in samples:
            base.need(type(row) is dict, "MALFORMED_INGEST_SAMPLE")
            event, ingest = timestamp(row.get("event_utc")), timestamp(row.get("ingested_utc"))
            delay = (ingest - event).total_seconds() / 60
            base.need(0 <= delay <= 10080, "NEGATIVE_OR_IMPLAUSIBLE_INGEST_DELAY")
            delays.append(delay)
        delays.sort()
        # Nearest-rank P95: x_(ceil(0.95*N)).
        computed = delays[math.ceil(.95 * len(delays)) - 1]
        claimed = obs.get("p95_minutes")
        threshold = approved.get("approved_p95_minutes")
        base.need(valid_number(claimed) and valid_number(threshold) and threshold > 0,
                  "INVALID_INGEST_P95_OR_THRESHOLD")
        base.agree(abs(claimed - computed) <= .01, "REPORTED_P95_DIFFERS_FROM_SAMPLES")
        base.agree(computed <= threshold, "INGEST_P95_EXCEEDS_APPROVED_THRESHOLD")
        require_same(obs, approved, "workspace_resource_id")
    elif case_id == "AZ-T57-21":
        require_same(obs, approved, "alert_rule_id", "recipient_id",
                     "delivery_channel", "synthetic_event_id")
        base.need(base.text(obs.get("delivery_ack_id")), "MISSING_ALERT_DELIVERY_ACK")
        sent = timestamp(obs.get("emitted_at_utc"))
        delivered = timestamp(obs.get("delivered_at_utc"))
        elapsed = (delivered - sent).total_seconds() / 60
        threshold = approved.get("approved_delivery_lag_minutes")
        base.need(valid_number(threshold) and threshold > 0,
                  "MISSING_APPROVED_ALERT_LAG")
        base.agree(0 <= elapsed <= threshold, "ALERT_DELIVERY_OUTSIDE_APPROVED_WINDOW")
        base.need(base.text(obs.get("delivery_status")), "MISSING_DELIVERY_STATUS")
        base.agree(obs["delivery_status"] == "Delivered", "ALERT_NOT_DELIVERED")
    else:
        raise base.Incomplete("UNSUPPORTED_CASE")


def assess(case_id, observation, baseline, *, now=None):
    result, reason = "NOT_READY", "UNVERIFIED_INPUT"
    try:
        base.need(case_id in CASES, "UNSUPPORTED_CASE")
        base.need(type(observation) is dict and type(baseline) is dict,
                  "INVALID_OBSERVATION_OR_BASELINE")
        om, am = observation.get("metadata"), baseline.get("metadata")
        base.need(type(om) is dict and type(am) is dict, "MISSING_METADATA")
        for key in ("case_id", "resource_id", "runner_id", "source_sha256"):
            base.exact_field(om, am, key)
        base.agree(om["case_id"] == case_id, "CASE_ID_DISAGREES_WITH_SOURCE")
        base.need(base.digest(om["source_sha256"]) and base.digest(am["source_sha256"]),
                  "INVALID_SOURCE_SHA256")
        base.need(base.digest(am.get("approval_record_sha256")),
                  "MISSING_APPROVAL_DIGEST")
        base.observed_at(om.get("observed_at_utc"),
                         now if now is not None else datetime.now(timezone.utc))
        o, a = observation.get("observation"), baseline.get("expected")
        base.need(type(o) is dict and type(a) is dict, "MISSING_CONTROL_VALUES")
        compare_control(case_id, o, a)
        result, reason = "REVIEW_REQUIRED", "LOCAL_COMPARISON_ONLY_NOT_ATTESTATION"
    except base.Incomplete as exc:
        result, reason = "NOT_READY", str(exc)
    except base.Mismatch as exc:
        result, reason = "DIFFERENCE_REVIEW_REQUIRED", str(exc)
    except (ValueError, KeyError, TypeError, OverflowError):
        result, reason = "NOT_READY", "INVALID_CONTROL_VALUES"
    return {
        "schema": "azure-p1-network-monitor-correlation/v1",
        "case_id": case_id,
        "finding_kind": CASES.get(case_id, "UNSUPPORTED"),
        "result": result,
        "reason_code": reason,
        "signature_verified": False,
        "runner_identity_verified": False,
        "azure_route_or_app_verified": False,
        "approval_authority_verified": False,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case-id", required=True)
    p.add_argument("--observation", type=Path, required=True)
    p.add_argument("--baseline", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        observation = base.read_json(args.observation)
        baseline = base.read_json(args.baseline)
    except (OSError, ValueError, UnicodeError, TypeError):
        observation = baseline = None
    print(json.dumps(assess(args.case_id, observation, baseline),
                     ensure_ascii=False, sort_keys=True))
    return 2  # local, unsigned JSON can never independently authorize a PASS


if __name__ == "__main__":
    raise SystemExit(main())
