#!/usr/bin/env python3
"""Offline comparison of unsigned Azure IaC observations and approval records."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path

if __package__:
    from . import plan_policy_guard as policy
    from . import review_p1_source_evidence as prior
else:
    import plan_policy_guard as policy
    import review_p1_source_evidence as prior

base = prior.base
need, agree = base.need, base.agree
same, truth, number = prior.same, prior.truth, prior.strict_int

CASES = {
    "AZ-T40-15": ("pipeline_id", "run_id", "scan_policy_revision"),
    "AZ-T40-21": ("deployment_id", "commit", "actor", "approval_id",
                  "change_record_id", "reviewer", "deployed_at"),
    "AZ-T41-13": ("indexer_id", "data_source_id", "target_index_id", "run_id",
                  "runtime_id", "principal_id", "fixture_id"),
    "AZ-T41-17": ("indexer_id", "unauthorized_source_id", "run_id", "runtime_id",
                  "principal_id", "fixture_id"),
    "AZ-T41-21": ("search_service_id", "target_id", "connection_id", "group_id",
                  "decision", "approval_id", "reviewer", "requester"),
    "AZ-T42-15": ("identity_id", "tenant_id", "audience", "runtime_id", "request_id"),
    "AZ-T42-19": ("principal_id", "role_id", "assignment_id", "scope", "operation"),
    "AZ-T43-13": ("principal_id", "role_id", "assignment_id", "scope", "operation",
                  "account_id", "container_id"),
    "AZ-T43-21": ("account_id", "assignment_id", "role_id", "principal_id",
                  "scope", "operation", "change_record_id", "actor", "reviewer",
                  "rationale"),
    "AZ-T44-15": ("source_commit", "policy_revision", "approval_id"),
}

LOG_CLASSES = {"tokens", "keys", "credentials", "sensitive_prompts"}
ACTIONS = {
    ("create",), ("read",), ("update",), ("delete",), ("no-op",),
    ("delete", "create"), ("create", "delete"),
}


def content_digest(value):
    """Hash the complete normalized JSON value, including scope and timestamps."""
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode("ascii")).hexdigest()


def string(row, key):
    return prior.text_value(row.get(key), key.upper())


def expected(row, key, value):
    agree(string(row, key) == value, "UNEXPECTED_" + key.upper())


def valid_commit(value):
    need(bool(prior.SOURCE_COMMIT.fullmatch(value)), "INVALID_COMMIT")


def time_at(row, key, observed):
    timestamp = base.observed_at(row.get(key), observed)
    agree(timestamp <= observed, "EVENT_AFTER_OBSERVATION")
    return timestamp


def compare_propagation(case_id, o, a, observed):
    assigned = time_at(o, "assigned_at", observed)
    first = time_at(o, "initial_probe_at", observed)
    propagated = time_at(o, "propagation_verified_at", observed)
    retested = time_at(o, "retested_at", observed)
    limit = number(a.get("max_wait_seconds"), minimum=1, label="PROPAGATION_WINDOW")
    need(limit <= 604800, "PROPAGATION_WINDOW_TOO_LARGE")
    agree(assigned <= first < propagated < retested <= assigned + timedelta(seconds=limit),
          "PROPAGATION_TIMELINE_MISMATCH")
    expected(o, "propagation_status", "verified")
    expected(o, "retest_status", "allowed")
    requests = [string(o, key) for key in ("initial_request_id", "propagation_probe_id",
                                           "retest_request_id")]
    agree(len(set(requests)) == len(requests), "REUSED_REQUEST_ID")
    if case_id == "AZ-T43-13":
        expected(o, "plane", "cosmos_sql_data")
        expected(o, "client", "sdk")
        truth(o, "account_key_used", False)


def operations(rows):
    need(type(rows) is list and rows, "MISSING_PLAN_OPERATION_INVENTORY")
    result = {}
    for row in rows:
        need(type(row) is dict, "INVALID_PLAN_OPERATION")
        address, kind = string(row, "address"), string(row, "type")
        change = row.get("change")
        need(type(change) is dict, "MISSING_PLAN_CHANGE")
        actions = change.get("actions")
        need(base.strings(actions) and tuple(actions) in ACTIONS, "UNKNOWN_PLAN_ACTIONS")
        agree(address not in result, "DUPLICATE_PLAN_ADDRESS")
        result[address] = (kind, tuple(actions))
    return result


def unknown_values(value):
    if type(value) is dict:
        return any(unknown_values(item) for item in value.values())
    if type(value) is list:
        return any(unknown_values(item) for item in value)
    need(type(value) is bool, "INVALID_PLAN_AFTER_UNKNOWN")
    return value


def compare_plan(o, a):
    truth(o, "sanitized")
    valid_commit(o["source_commit"])
    plan = o.get("plan")
    need(type(plan) is dict and type(plan.get("planned_values")) is dict,
         "MISSING_SANITIZED_PLAN")
    digest = a.get("plan_sha256")
    need(base.digest(digest), "MISSING_PLAN_DIGEST")
    agree(content_digest(plan) == digest, "PLAN_CONTENT_DIGEST_MISMATCH")
    # The local rule set is defined for resource changes. Unsupported change
    # sections require a separate review instead of silently dropping them.
    for key in ("output_changes", "resource_drift", "deferred_changes", "action_invocations"):
        need(not plan.get(key), "UNSUPPORTED_PLAN_CHANGE_SECTION")
    actual = operations(plan.get("resource_changes"))
    approved = operations(a.get("approved_resource_changes"))
    agree(actual == approved, "PLAN_OPERATION_INVENTORY_MISMATCH")
    rules = a.get("required_rules")
    need(base.strings(rules), "MISSING_PLAN_RULES")
    agree(len(rules) == len(policy.RULES) and set(rules) == policy.RULES,
          "INCOMPLETE_PLAN_RULE_SET")
    scope = {
        "approval_id": o["approval_id"],
        "plan_sha256": digest,
        "reviewers": a.get("reviewers"),
        "approved_addresses": sorted(approved),
        "source_commit": o["source_commit"],
    }
    # Inspect both legs of replacements with the existing per-operation rules.
    # Unknown computed fields are retained for the explicit check below.
    outcomes = set()
    for row in plan["resource_changes"]:
        change = row["change"]
        for action in change["actions"]:
            if action in {"create", "update"}:
                need(not unknown_values(change.get("after_unknown", {})), "UNKNOWN_PLAN_AFTER_VALUES")
            single = {**row, "change": {**change, "actions": [action]}}
            for rule in sorted(policy.RULES):
                verdict, _ = policy.decision(rule, {"resource_changes": [single]}, scope, digest)
                outcomes.add(verdict)
    agree("FAIL" not in outcomes, "PLAN_POLICY_VIOLATION")
    need(outcomes == {"REVIEW_REQUIRED"}, "PLAN_POLICY_EVALUATION_INCOMPLETE")


def compare(case_id, o, a, observed):
    same(o, a, *CASES[case_id])
    if case_id == "AZ-T40-15":
        prior.matching_sha(o, a, "sanitized_report_sha256")
        scans = o.get("scans")
        need(type(scans) is dict and LOG_CLASSES <= scans.keys(), "MISSING_LOG_SCAN_CLASSES")
        agree(scans.keys() == LOG_CLASSES, "UNEXPECTED_LOG_SCAN_CLASS")
        count = number(a.get("artifact_count"), minimum=1, label="APPROVED_ARTIFACT_COUNT")
        for key in sorted(LOG_CLASSES):
            row = scans[key]
            need(type(row) is dict, "INVALID_LOG_SCAN")
            agree(number(row.get("artifact_count"), label="SCANNED_ARTIFACT_COUNT") == count,
                  "INCOMPLETE_CI_LOG_SCAN")
            number(row.get("positive_controls"), minimum=1, label="POSITIVE_CONTROLS")
            agree(number(row.get("unredacted_findings"), label="UNREDACTED_FINDINGS") == 0,
                  "SENSITIVE_CI_LOG_FINDINGS")
    elif case_id == "AZ-T40-21":
        valid_commit(o["commit"])
        agree(o["actor"] != o["reviewer"], "DEPLOYMENT_SELF_APPROVAL")
        expected(o, "approval_status", "approved")
        same(o, a, "approved_at")
        agree(time_at(o, "approved_at", observed) <= time_at(o, "deployed_at", observed),
              "APPROVAL_AFTER_DEPLOYMENT")
    elif case_id == "AZ-T41-13":
        truth(o, "synthetic_fixture")
        expected(o, "status", "success")
        count = number(a.get("expected_documents"), minimum=1, label="EXPECTED_DOCUMENTS")
        agree(number(o.get("indexed_documents"), label="INDEXED_DOCUMENTS") == count and
              number(o.get("failed_documents"), label="FAILED_DOCUMENTS") == 0,
              "INDEXER_DOCUMENT_RESULTS_MISMATCH")
        agree(time_at(o, "started_at", observed) < time_at(o, "completed_at", observed),
              "INDEXER_TIMELINE_MISMATCH")
    elif case_id == "AZ-T41-17":
        truth(o, "isolated_test")
        expected(o, "status", "denied")
        expected(o, "denial_reason", "authorization")
        agree(number(o.get("http_status"), label="HTTP_STATUS") == 403 and
              number(o.get("fetched_documents"), label="FETCHED_DOCUMENTS") == 0,
              "INDEXER_DENIAL_NOT_DEMONSTRATED")
    elif case_id == "AZ-T41-21":
        agree(o["reviewer"] != o["requester"], "SHARED_LINK_SELF_APPROVAL")
        expected(o, "approval_status", "approved")
        same(o, a, "reviewed_at")
        time_at(o, "reviewed_at", observed)
        need(o["decision"] in {"adopt", "decline"}, "INVALID_ADOPTION_DECISION")
        expected(o, "connection_status", "approved" if o["decision"] == "adopt" else "absent")
    elif case_id == "AZ-T42-15":
        expected(o, "auth_method", "managed_identity")
        truth(o, "internal_runtime")
        truth(o, "token_obtained")
        truth(o, "token_bytes_recorded", False)
        allowed = set(CASES[case_id]) | {"auth_method", "internal_runtime",
                                        "token_obtained", "token_bytes_recorded"}
        agree(o.keys() <= allowed, "UNEXPECTED_TOKEN_OBSERVATION_FIELD")
    elif case_id in {"AZ-T42-19", "AZ-T43-13"}:
        compare_propagation(case_id, o, a, observed)
    elif case_id == "AZ-T43-21":
        expected(o, "role_type", "cosmos_sql_data")
        expected(o, "review_status", "approved")
        agree(o["operation"] in {"create", "update", "delete"}, "INVALID_ROLE_CHANGE_OPERATION")
        agree(o["actor"] != o["reviewer"], "ROLE_CHANGE_SELF_APPROVAL")
        same(o, a, "reviewed_at")
        time_at(o, "reviewed_at", observed)
    elif case_id == "AZ-T44-15":
        compare_plan(o, a)


def assess(case_id, observation, baseline, *, now=None):
    status, reason = "NOT_READY", "INVALID_FIELD_OR_TYPE"
    try:
        need(case_id in CASES, "UNKNOWN_CASE")
        need(type(observation) is dict and type(baseline) is dict,
             "OBSERVATION_OR_BASELINE_MISSING")
        om, am = observation.get("metadata"), baseline.get("metadata")
        need(type(om) is dict and type(am) is dict, "SOURCE_METADATA_MISSING")
        same(om, am, "case_id", "resource_id", "runner_id", "source_sha256")
        agree(om["case_id"] == case_id, "CASE_ID_DIFFERS")
        need(base.digest(om["source_sha256"]), "INVALID_SOURCE_DIGEST")
        need(base.digest(am.get("approval_record_sha256")), "MISSING_APPROVAL_DIGEST")
        digest = am.get("observation_sha256")
        need(base.digest(digest), "MISSING_OBSERVATION_DIGEST")
        observed = base.observed_at(om.get("observed_at_utc"), now or datetime.now(timezone.utc))
        o, a = observation.get("observation"), baseline.get("expected")
        need(type(o) is dict and type(a) is dict, "CONTROL_VALUES_MISSING")
        compare(case_id, o, a, observed)
        agree(content_digest(observation) == digest, "OBSERVATION_CONTENT_DIGEST_MISMATCH")
        approval_record = {"metadata": {key: value for key, value in am.items()
                                        if key != "approval_record_sha256"},
                           "expected": a}
        agree(content_digest(approval_record) == am["approval_record_sha256"],
              "APPROVAL_CONTENT_DIGEST_MISMATCH")
        status, reason = "REVIEW_REQUIRED", "UNTRUSTED_LOCAL_MATCH_REQUIRES_ATTESTATION"
    except base.Incomplete as exc:
        reason = str(exc)
    except base.Mismatch as exc:
        status, reason = "DIFFERENCE_REVIEW_REQUIRED", str(exc)
    except (TypeError, ValueError, OverflowError, RecursionError):
        pass
    return {
        "schema": "azure-p1-iac-evidence-review/v1",
        "case_id": case_id if case_id in CASES else "UNKNOWN_CASE",
        "result": status,
        "reason_code": reason,
        "origin_signature_verified": False,
        "approval_authority_verified": False,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
    }


def unique_object(pairs):
    obj = dict(pairs)
    if len(obj) != len(pairs):
        raise ValueError("duplicate JSON key")
    return obj


def invalid_constant(_):
    raise ValueError("invalid JSON constant")


def load(path):
    with path.open("rb") as stream:
        raw = stream.read(prior.MAX_DOC_BYTES + 1)
    if len(raw) > prior.MAX_DOC_BYTES:
        raise ValueError("oversized JSON")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=invalid_constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--observation", required=True, type=Path)
    parser.add_argument("--approved", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        observation, baseline = load(args.observation), load(args.approved)
    except (OSError, ValueError, RecursionError):
        observation = baseline = None
    print(json.dumps(assess(args.case_id, observation, baseline), sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
