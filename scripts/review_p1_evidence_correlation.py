#!/usr/bin/env python3
"""Offline, fail-closed comparison for ten P1 self-reported evidence cases.

This is NOT a verifier of signatures, runner provenance, Azure infrastructure,
approval authority or deployed control behavior. Matching *untrusted* local
observation and baseline JSON yields REVIEW_REQUIRED and exit code 2, NEVER PASS.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import ipaddress
import json
from pathlib import Path
import re

CASE_CRITERIA = {
    "AZ-T19-03": "Runner private IP within approved CIDR",
    "AZ-T39-19": "Private SCM path, approved origin and endpoint",
    "AZ-T43-15": "Cosmos SDK managed-identity access without account key",
    "AZ-T48-19": "OpenAI, Search and Cosmos private dependency results",
    "AZ-T50-15": "Image digest and signing identity binding",
    "AZ-T50-17": "Artifact-specific security scan and approved high waivers",
    "AZ-T51-19": "WAF Blocked action correlated to expected request and rule",
    "AZ-T53-09": "Certificate SAN contains approved hostname and validated chain",
    "AZ-T55-15": "Gateway-to-WebApp PE over TLS 443",
    "AZ-T58-09": "Two independent non-author reviewers of same plan",
}
HEXDIGEST = re.compile(r"^[a-f0-9]{64}$")
MAX_DOC_BYTES = 2_000_000


class Incomplete(Exception):
    pass


class Mismatch(Exception):
    pass


def need(condition: bool, reason: str):
    if not condition:
        raise Incomplete(reason)


def agree(condition: bool, reason: str):
    if not condition:
        raise Mismatch(reason)


def text(value):
    return type(value) is str and bool(value.strip()) and len(value) <= 512


def digest(value):
    return text(value) and bool(HEXDIGEST.fullmatch(value))


def exact_bool(value, wanted):
    return type(value) is bool and value is wanted


def strings(value, *, allow_empty=False):
    return (type(value) is list and (allow_empty or bool(value))
            and all(text(x) for x in value) and len(set(value)) == len(value))


def network_list(value):
    need(strings(value), "MISSING_APPROVED_NETWORKS")
    networks = []
    for cidr in value:
        try:
            networks.append(ipaddress.ip_network(cidr, strict=True))
        except ValueError:
            raise Incomplete("INVALID_APPROVED_NETWORK") from None
    return networks


def address(value):
    need(text(value), "MISSING_IP_ADDRESS")
    try:
        return ipaddress.ip_address(value)
    except ValueError:
        raise Incomplete("INVALID_IP_ADDRESS") from None


def in_cidrs(ip, cidrs, reason):
    allowed = network_list(cidrs)
    agree(any(ip in item for item in allowed), reason)


def exact_field(obs, approved, key):
    need(text(obs.get(key)) and text(approved.get(key)), "MISSING_" + key.upper())
    agree(obs[key] == approved[key], key.upper() + "_MISMATCH")


def obs_true(obs, key):
    need(type(obs.get(key)) is bool, "MISSING_OR_NONBOOLEAN_" + key.upper())
    agree(obs[key] is True, key.upper() + "_NOT_TRUE")


def obs_false(obs, key):
    need(type(obs.get(key)) is bool, "MISSING_OR_NONBOOLEAN_" + key.upper())
    agree(obs[key] is False, key.upper() + "_NOT_FALSE")


def observed_at(value, now):
    need(text(value), "MISSING_OBSERVATION_TIME")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise Incomplete("INVALID_OBSERVATION_TIME") from None
    need(dt.tzinfo is not None, "TIME_WITHOUT_UTC_OFFSET")
    utc = dt.astimezone(timezone.utc)
    need(now - timedelta(days=7) <= utc <= now + timedelta(minutes=5),
         "STALE_OR_FUTURE_OBSERVATION")
    return utc


def compare_case(case_id, o, a):
    if case_id == "AZ-T19-03":
        ip = address(o.get("private_ip"))
        agree(ip.is_private and not ip.is_loopback and not ip.is_link_local,
              "RUNNER_ADDRESS_NOT_APPROVED_PRIVATE")
        in_cidrs(ip, a.get("approved_runner_cidrs"), "RUNNER_OUTSIDE_APPROVED_CIDR")
    elif case_id == "AZ-T39-19":
        src = address(o.get("source_ip"))
        dst = address(o.get("scm_target_ip"))
        in_cidrs(src, a.get("approved_runner_cidrs"), "SCM_SOURCE_OUTSIDE_APPROVED_CIDR")
        need(strings(a.get("approved_scm_pe_ips")), "MISSING_APPROVED_SCM_PE")
        agree(str(dst) in a["approved_scm_pe_ips"], "SCM_TARGET_NOT_APPROVED_PE")
        exact_field(o, a, "scm_hostname")
        obs_true(o, "tls_validated")
        need(text(o.get("deployment_result")), "MISSING_DEPLOYMENT_RESULT")
        agree(o["deployment_result"] == "success", "SCM_DEPLOYMENT_DID_NOT_SUCCEED")
    elif case_id == "AZ-T43-15":
        exact_field(o, a, "principal_id")
        exact_field(o, a, "container_id")
        need(text(o.get("auth")) and text(o.get("result")), "MISSING_SDK_RESULT")
        agree(o["auth"] == "managed_identity" and o["result"] == "Pass",
              "COSMOS_SDK_RESULT_OR_IDENTITY_UNEXPECTED")
        obs_false(o, "account_key_used")
    elif case_id == "AZ-T48-19":
        dependencies = o.get("dependencies")
        expected = a.get("dependency_resource_ids")
        need(type(dependencies) is dict and type(expected) is dict,
             "MISSING_DEPENDENCY_MAP")
        needed = {"openai", "search", "cosmos"}
        need(set(dependencies) == needed and set(expected) == needed,
             "INCOMPLETE_DEPENDENCY_SET")
        for key in sorted(needed):
            row = dependencies[key]
            need(type(row) is dict and text(row.get("resource_id")) and
                 text(row.get("status")), "MISSING_DEPENDENCY_" + key.upper())
            agree(row["resource_id"] == expected[key] and row["status"] == "Pass",
                  "DEPENDENCY_MISMATCH_" + key.upper())
            obs_true(row, "private_route_observed")
            exact_field(row, a, "principal_id")
    elif case_id == "AZ-T50-15":
        exact_field(o, a, "image_digest")
        exact_field(o, a, "trusted_signer_id")
        need(digest(o["image_digest"]) and digest(a["image_digest"]),
             "INVALID_IMAGE_DIGEST")
        obs_true(o, "cryptographic_signature_verified")
        # The boolean is still untrusted local data; no cryptographic check here.
    elif case_id == "AZ-T50-17":
        exact_field(o, a, "image_digest")
        need(digest(o["image_digest"]) and digest(a["image_digest"]),
             "INVALID_IMAGE_DIGEST")
        critical = o.get("critical_findings")
        need(type(critical) is int and critical >= 0,
             "MISSING_OR_INVALID_CRITICAL_FINDINGS")
        agree(critical == 0, "CRITICAL_VULNERABILITIES_REPORTED")
        highs = o.get("high_finding_ids")
        waivers = o.get("waived_high_ids")
        approved_waivers = a.get("approved_high_waiver_ids")
        need(strings(highs, allow_empty=True) and
             strings(waivers, allow_empty=True) and
             strings(approved_waivers, allow_empty=True),
             "MISSING_HIGH_FINDING_ADJUDICATION")
        agree(set(highs) == set(waivers) and set(waivers).issubset(set(approved_waivers)),
              "UNAPPROVED_HIGH_FINDINGS")
    elif case_id == "AZ-T51-19":
        for key in ("transaction_id", "request_id", "rule_id"):
            exact_field(o, a, key)
        need(text(o.get("action")), "MISSING_WAF_ACTION")
        agree(o["action"] == "Blocked", "WAF_MATCHED_IS_NOT_BLOCKED")
        need(type(o.get("http_status")) is int, "MISSING_WAF_HTTP_STATUS")
        agree(o["http_status"] == 403, "WAF_EXPECTED_DENIAL_ABSENT")
    elif case_id == "AZ-T53-09":
        exact_field(o, a, "approved_hostname")
        names = o.get("san_dns_names")
        need(strings(names), "MISSING_SAN_DNS_NAMES")
        agree(o["approved_hostname"] in names, "APPROVED_HOSTNAME_NOT_IN_SAN")
        obs_true(o, "chain_verified")
        obs_true(o, "hostname_verified")
    elif case_id == "AZ-T55-15":
        src = address(o.get("source_ip"))
        dst = address(o.get("destination_ip"))
        in_cidrs(src, a.get("approved_gateway_cidrs"), "GATEWAY_SOURCE_UNAPPROVED")
        need(strings(a.get("approved_webapp_pe_ips")), "MISSING_APPROVED_WEBAPP_PE")
        agree(str(dst) in a["approved_webapp_pe_ips"], "WEBAPP_DESTINATION_NOT_APPROVED_PE")
        need(type(o.get("port")) is int, "INVALID_GATEWAY_PORT")
        agree(o["port"] == 443, "GATEWAY_PORT_NOT_443")
        obs_true(o, "tls_verified")
        exact_field(o, a, "webapp_resource_id")
        need(text(o.get("status")), "MISSING_GATEWAY_STATUS")
        agree(o["status"] == "Pass", "GATEWAY_CONNECTION_NOT_PASS")
    elif case_id == "AZ-T58-09":
        exact_field(o, a, "plan_sha256")
        need(digest(o["plan_sha256"]) and digest(a["plan_sha256"]),
             "INVALID_APPROVED_PLAN_DIGEST")
        for key in ("author_id", "executor_id"):
            need(text(o.get(key)), "MISSING_" + key.upper())
        allowed = a.get("approved_reviewer_ids")
        people = o.get("reviewers")
        need(strings(allowed) and type(people) is list and len(people) >= 2,
             "MISSING_REVIEWER_SET")
        ids, roles = [], []
        for reviewer in people:
            need(type(reviewer) is dict and
                 text(reviewer.get("identity_id")) and
                 text(reviewer.get("role")) and
                 digest(reviewer.get("plan_sha256")),
                 "INVALID_REVIEWER_RECORD")
            ids.append(reviewer["identity_id"])
            roles.append(reviewer["role"])
            agree(reviewer["plan_sha256"] == a["plan_sha256"],
                  "REVIEWER_APPROVED_DIFFERENT_PLAN")
        agree(len(set(ids)) >= 2 and len(set(roles)) >= 2 and
              o["author_id"] not in ids and o["executor_id"] not in ids and
              set(ids).issubset(set(allowed)),
              "REVIEWERS_NOT_AUTHORIZED_AND_INDEPENDENT")
    else:
        raise Incomplete("UNKNOWN_CASE")


def assess(case_id, observation, baseline, *, now=None):
    result = "NOT_READY"
    reason = "UNVERIFIED_OR_INVALID_INPUT"
    now = now if now is not None else datetime.now(timezone.utc)
    try:
        need(case_id in CASE_CRITERIA, "CASE_NOT_SUPPORTED")
        need(type(observation) is dict and type(baseline) is dict,
             "MISSING_OBSERVATION_OR_BASELINE")
        om = observation.get("metadata")
        am = baseline.get("metadata")
        need(type(om) is dict and type(am) is dict, "MISSING_SOURCE_METADATA")
        for key in ("case_id", "resource_id", "runner_id", "source_sha256"):
            exact_field(om, am, key)
        agree(om["case_id"] == case_id, "EVIDENCE_CASE_ID_MISMATCH")
        need(digest(om["source_sha256"]) and digest(am["source_sha256"]),
             "INVALID_SOURCE_DIGEST")
        need(digest(am.get("approval_record_sha256")), "MISSING_APPROVAL_RECORD_DIGEST")
        observed_at(om.get("observed_at_utc"), now)
        o = observation.get("observation")
        a = baseline.get("expected")
        need(type(o) is dict and type(a) is dict, "MISSING_CONTROL_VALUES")
        compare_case(case_id, o, a)
        result, reason = "REVIEW_REQUIRED", "LOCAL_MATCH_REQUIRES_INDEPENDENT_PROVENANCE"
    except Incomplete as exc:
        result, reason = "NOT_READY", str(exc)
    except Mismatch as exc:
        result, reason = "DIFFERENCE_REVIEW_REQUIRED", str(exc)
    except (TypeError, KeyError, ValueError):
        result, reason = "NOT_READY", "MALFORMED_CONTROL_VALUES"

    return {
        "schema": "azure-p1-evidence-correlation/v1",
        "case_id": case_id,
        "result": result,
        "reason_code": reason,
        "independent_evidence_signature_verified": False,
        "runner_provenance_verified": False,
        "approval_authority_verified": False,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "limitations": (
            "Untrusted local JSON comparison only; does not verify Azure, "
            "real cryptographic signatures, identity, runner route or signer authority."
        ),
    }


def read_json(path):
    if path.stat().st_size > MAX_DOC_BYTES:
        raise ValueError("oversized input")
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--observation", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        obs, baseline = read_json(args.observation), read_json(args.baseline)
    except (OSError, UnicodeError, ValueError, TypeError):
        obs, baseline = None, None
    print(json.dumps(assess(args.case_id, obs, baseline), ensure_ascii=False, sort_keys=True))
    return 2  # A local comparison is NEVER independent Azure acceptance.


if __name__ == "__main__":
    raise SystemExit(main())
