#!/usr/bin/env python3
"""Review 10 original P1 WAF/supply-chain/TLS/route claims, offline and fail-closed.

Neither the observed JSON, JUnit XML nor the claimed approved baseline is
authenticated. A local match is REVIEW_REQUIRED (not Pass), always exit 2.
Never executes Azure, Terraform, Playwright or network commands.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import ipaddress
import json
from pathlib import Path
import xml.etree.ElementTree as ET

if __package__:
    from . import review_p1_evidence_correlation as base
else:
    import review_p1_evidence_correlation as base

CASES = {
    "AZ-T50-13": "SBOM_BOUND_TO_IMAGE_DIGEST",
    "AZ-T50-21": "UNTRUSTED_IMAGE_DENIED",
    "AZ-T51-13": "WAF_BENIGN_TRAFFIC_ALLOWED_JUNIT",
    "AZ-T51-15": "WAF_SQLI_RULE_DENIAL_JUNIT",
    "AZ-T51-17": "WAF_XSS_RULE_DENIAL_JUNIT",
    "AZ-T53-17": "TLS_ROTATION_AND_ROLLBACK",
    "AZ-T54-19": "GATEWAY_503_AND_ALERT_MONITORING",
    "AZ-T55-11": "BACKEND_CERTIFICATE_SAN_AND_CHAIN",
    "AZ-T56-09": "UNAUTHORIZED_SUBNET_BLOCKED",
    "AZ-T56-21": "ROUTE_CHANGE_ALERT_AND_ROLLBACK",
}
WAF_IDS = {"AZ-T51-13", "AZ-T51-15", "AZ-T51-17"}
MAX_DOC_BYTES = 2_000_000
MAX_XML_BYTES = 1_000_000


def same(obs, approved, *names):
    for key in names:
        base.exact_field(obs, approved, key)


def require_sha256(value, name):
    base.need(base.digest(value), "MISSING_OR_INVALID_SHA256_" + name)


def number(value, name, minimum=0):
    base.need(type(value) is int and value >= minimum, "INVALID_INTEGER_" + name)
    return value


def boolean(observation, key, desired):
    base.need(type(observation.get(key)) is bool,
              "MISSING_OR_NONBOOLEAN_" + key.upper())
    base.agree(observation[key] is desired, "UNEXPECTED_" + key.upper())


def required_string(value, name):
    base.need(base.text(value), "MISSING_" + name.upper())
    return value


def exact_digest(observation, approved, key):
    same(observation, approved, key)
    require_sha256(observation[key], key)


def safe_xml_junit(filename, approved_sha, expected_case):
    """Parse a *local* JUnit summary, not execute tests or trust the producer."""
    require_sha256(approved_sha, "approved_junit")
    base.need(base.text(filename), "MISSING_JUNIT_PATH")
    path = Path(filename)
    try:
        base.need(path.is_file() and not path.is_symlink(),
                  "JUNIT_FILE_NOT_PRESENT_OR_SYMLINK")
        base.need(path.stat().st_size <= MAX_XML_BYTES and path.stat().st_size > 0,
                  "JUNIT_FILE_SIZE_INVALID")
        raw = path.read_bytes()
        base.agree(hashlib.sha256(raw).hexdigest() == approved_sha,
                   "JUNIT_SHA256_DIFFERS_FROM_CLAIMED_APPROVAL")
        base.need(b"<!DOCTYPE" not in raw.upper() and b"<!ENTITY" not in raw.upper(),
                  "UNTRUSTED_JUNIT_XML_DTD")
        xml = ET.fromstring(raw)
    except (OSError, ET.ParseError, ValueError) as err:
        raise base.Incomplete("INVALID_OR_UNREADABLE_JUNIT") from None

    base.need(xml.tag in ("testsuite", "testsuites"), "UNEXPECTED_JUNIT_ROOT")
    suites = [xml] if xml.tag == "testsuite" else list(xml.findall("testsuite"))
    base.need(bool(suites), "NO_JUNIT_SUITES")
    names = []
    for suite in suites:
        rows = suite.findall("testcase")
        base.need(bool(rows), "JUNIT_NO_CASES")
        declared = suite.get("tests")
        base.need(declared is not None and declared.isdecimal(),
                  "JUNIT_MISSING_TEST_COUNT")
        base.agree(int(declared) == len(rows), "JUNIT_DECLARED_TESTS_MISMATCH")
        for row in rows:
            for forbidden in ("failure", "error", "skipped"):
                base.agree(row.find(forbidden) is None,
                           "JUNIT_CONTAINS_" + forbidden.upper())
            name = required_string(row.get("name"), "JUNIT_TEST_NAME")
            names.append(name)
    base.need(len(names) == len(set(names)), "DUPLICATE_JUNIT_TEST_NAME")
    base.agree(expected_case in names, "JUNIT_EXPECTED_CASE_NOT_PRESENT")


def compare(case_id, o, approved):
    if case_id == "AZ-T50-13":
        same(o, approved, "image_resource_id", "repository_name", "image_version")
        exact_digest(o, approved, "image_digest")
        required_string(o.get("sbom_format"), "SBOM_FORMAT")
        base.agree(o["sbom_format"] in ("CycloneDX", "SPDX"),
                   "SBOM_FORMAT_UNRECOGNIZED")
        base.agree(o["sbom_format"] == approved.get("approved_format"),
                   "SBOM_FORMAT_NOT_APPROVED")
        exact_digest(o, approved, "sbom_sha256")
        base.need(number(o.get("component_count"), "SBOM_COMPONENTS", 1) >= 1,
                  "SBOM_HAS_NO_COMPONENTS")
        boolean(o, "sbom_artifact_digest_matches", True)
        required_string(o.get("immutable_sbom_reference"), "SBOM_REFERENCE")
    elif case_id == "AZ-T50-21":
        same(o, approved, "policy_resource_id", "unapproved_image_ref",
             "test_request_id", "denial_rule_id")
        boolean(o, "denied", True)
        base.agree(required_string(o.get("decision"), "IMAGE_ADMISSION_DECISION") == "Deny",
                   "UNTRUSTED_IMAGE_NOT_DENIED")
        required_string(o.get("admission_log_correlation_id"), "ADMISSION_CORRELATION")
        boolean(o, "used_isolated_test", True)
    elif case_id in WAF_IDS:
        same(o, approved, "waf_policy_id", "test_request_id", "scenario_id")
        safe_xml_junit(o.get("junit_path"), approved.get("approved_junit_sha256"),
                       approved.get("approved_junit_testcase"))
        action = required_string(o.get("waf_action"), "WAF_ACTION")
        status = number(o.get("http_status"), "WAF_HTTP_STATUS", 100)
        if case_id == "AZ-T51-13":
            base.agree(action == "Allowed", "BENIGN_REQUEST_NOT_ALLOWED")
            base.agree(status in (200, 201, 202, 204, 301, 302),
                       "BENIGN_REQUEST_STATUS_UNEXPECTED")
        else:
            same(o, approved, "waf_rule_id")
            base.agree(action == "Blocked", "MALICIOUS_SIMULATION_NOT_BLOCKED")
            base.agree(status == 403, "MALICIOUS_SIMULATION_NOT_HTTP_403")
        required_string(o.get("waf_log_correlation_id"), "WAF_LOG_CORRELATION")
        boolean(o, "authorized_nonproduction_test", True)
    elif case_id == "AZ-T53-17":
        same(o, approved, "gateway_resource_id", "keyvault_secret_uri",
             "old_secret_version", "new_secret_version", "change_ticket")
        base.agree(o["old_secret_version"] != o["new_secret_version"],
                   "TLS_ROTATION_NO_VERSION_CHANGE")
        base.agree(o.get("rollback_secret_version") == o["old_secret_version"],
                   "TLS_ROLLBACK_TARGET_NOT_OLD")
        boolean(o, "renewal_test_succeeded", True)
        boolean(o, "rollback_test_succeeded", True)
        boolean(o, "private_key_disclosed", False)
        required_string(o.get("isolated_drill_log_id"), "TLS_DRILL_LOG")
    elif case_id == "AZ-T54-19":
        same(o, approved, "gateway_resource_id", "backend_resource_id",
             "monitor_alert_rule_id", "approved_window_id")
        total = number(o.get("total_approved_requests"), "GATEWAY_REQUESTS", 1)
        errors = number(o.get("unexpected_503_count"), "UNEXPECTED_503_COUNT")
        base.agree(total >= 20, "INSUFFICIENT_APPROVED_REQUEST_SAMPLES")
        base.agree(errors == 0, "UNEXPLAINED_503_OBSERVED")
        boolean(o, "backend_health_healthy", True)
        boolean(o, "synthetic_incident_alert_delivered", True)
        required_string(o.get("alert_ack_id"), "GATEWAY_503_ALERT_ACK")
    elif case_id == "AZ-T55-11":
        same(o, approved, "backend_resource_id", "approved_hostname")
        exact_digest(o, approved, "certificate_sha256")
        sans = o.get("san_dns_names")
        base.need(base.strings(sans), "MISSING_SAN_LIST")
        base.agree(o["approved_hostname"] in sans,
                   "BACKEND_HOSTNAME_MISSING_FROM_SAN")
        boolean(o, "hostname_verified", True)
        boolean(o, "chain_verified", True)
        boolean(o, "tls_bypass_enabled", False)
    elif case_id == "AZ-T56-09":
        same(o, approved, "test_source_subnet_id", "target_pe_resource_id",
             "test_request_id", "approved_deny_rule_id")
        src = base.address(o.get("source_ip"))
        base.in_cidrs(src, approved.get("unauthorized_test_cidrs"),
                      "UNAUTHORIZED_TEST_SOURCE_NOT_APPROVED")
        base.need(base.text(o.get("test_result")), "MISSING_NEGATIVE_TEST_RESULT")
        base.agree(o["test_result"] == "Blocked", "UNAUTHORIZED_ACCESS_NOT_BLOCKED")
        base.agree(o.get("flow_deny_rule_id") == approved["approved_deny_rule_id"],
                   "BLOCKED_OUTCOME_NOT_LINKED_TO_DENY_RULE")
        required_string(o.get("flow_log_id"), "DENY_FLOW_LOG")
    elif case_id == "AZ-T56-21":
        same(o, approved, "route_table_resource_id", "change_ticket",
             "simulated_drift_route_id", "monitor_alert_rule_id")
        exact_digest(o, approved, "baseline_route_set_sha256")
        exact_digest(o, approved, "post_rollback_route_set_sha256")
        base.agree(o["baseline_route_set_sha256"] == o["post_rollback_route_set_sha256"],
                   "ROUTE_SET_DID_NOT_RETURN_TO_BASELINE")
        base.agree(number(o.get("unapproved_changes_remaining"),
                          "UNAPPROVED_ROUTE_CHANGES") == 0,
                   "UNAPPROVED_ROUTE_DRIFT_REMAINS")
        boolean(o, "simulated_drift_detected", True)
        boolean(o, "alert_delivered", True)
        required_string(o.get("alert_ack_id"), "ROUTE_ALERT_ACK")
        required_string(o.get("rollback_run_id"), "ROUTE_ROLLBACK_RUN")
    else:
        raise base.Incomplete("UNKNOWN_SOURCE_CASE")


def assess(case_id, observation, baseline, *, now=None):
    result, reason = "NOT_READY", "INVALID_OR_MISSING_INPUT"
    try:
        base.need(case_id in CASES, "UNKNOWN_SOURCE_CASE")
        base.need(type(observation) is dict and type(baseline) is dict,
                  "MISSING_OBSERVATION_OR_BASELINE")
        om, am = observation.get("metadata"), baseline.get("metadata")
        base.need(type(om) is dict and type(am) is dict, "MISSING_CASE_METADATA")
        for key in ("case_id", "resource_id", "runner_id", "source_sha256"):
            same(om, am, key)
        base.agree(om["case_id"] == case_id, "CASE_ID_MISMATCH")
        require_sha256(om["source_sha256"], "source")
        require_sha256(am["source_sha256"], "approved_source")
        require_sha256(am.get("approval_record_sha256"), "approval_record")
        base.observed_at(om.get("observed_at_utc"),
                         now if now is not None else datetime.now(timezone.utc))
        o, a = observation.get("observation"), baseline.get("expected")
        base.need(type(o) is dict and type(a) is dict, "MISSING_CONTROL_FIELDS")
        compare(case_id, o, a)
        result, reason = ("REVIEW_REQUIRED",
                          "LOCAL_MATCH_ONLY_EXTERNAL_PROVENANCE_UNVERIFIED")
    except base.Incomplete as e:
        result, reason = "NOT_READY", str(e)
    except base.Mismatch as e:
        result, reason = "DIFFERENCE_REVIEW_REQUIRED", str(e)
    except (KeyError, OSError, ValueError, TypeError, OverflowError):
        result, reason = "NOT_READY", "MALFORMED_CONTROL_FIELDS"
    return {
        "schema": "azure-p1-waf-supplychain-review/v1",
        "case_id": case_id,
        "category": CASES.get(case_id, "UNKNOWN"),
        "result": result,
        "reason_code": reason,
        "approval_signature_verified": False,
        "origin_and_runner_verified": False,
        "junit_execution_provenance_verified": False,
        "runtime_control_verified": False,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
    }


def read_json(path):
    if path.stat().st_size > MAX_DOC_BYTES:
        raise ValueError("oversized input")
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case-id", required=True)
    p.add_argument("--observation", type=Path, required=True)
    p.add_argument("--approved", type=Path, required=True)
    a = p.parse_args(argv)
    try:
        observation = read_json(a.observation)
        baseline = read_json(a.approved)
    except (OSError, ValueError, UnicodeError, TypeError):
        observation = baseline = None
    print(json.dumps(assess(a.case_id, observation, baseline),
                     ensure_ascii=False, sort_keys=True))
    return 2  # a local input match is never independent acceptance


if __name__ == "__main__":
    raise SystemExit(main())
