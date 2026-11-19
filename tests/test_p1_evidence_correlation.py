"""Synthetic security regressions for ten P1 untrusted evidence correlations."""
from __future__ import annotations

import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import review_p1_evidence_correlation as r
from scripts.triage_static_criteria import triage

ROOT = Path(__file__).resolve().parents[1]


def pair(case_id):
    digest = "a" * 64
    expected = {}
    observed = {}
    if case_id == "AZ-T19-03":
        observed = {"private_ip": "10.10.1.7"}
        expected = {"approved_runner_cidrs": ["10.10.0.0/16"]}
    elif case_id == "AZ-T39-19":
        observed = {"source_ip": "10.10.1.7", "scm_target_ip": "10.30.0.4",
                    "scm_hostname": "web.scm.internal.test", "tls_validated": True,
                    "deployment_result": "success"}
        expected = {"approved_runner_cidrs": ["10.10.0.0/16"],
                    "approved_scm_pe_ips": ["10.30.0.4"],
                    "scm_hostname": "web.scm.internal.test"}
    elif case_id == "AZ-T43-15":
        observed = {"principal_id": "principal-a", "container_id": "db/test",
                    "auth": "managed_identity", "result": "Pass", "account_key_used": False}
        expected = {"principal_id": "principal-a", "container_id": "db/test"}
    elif case_id == "AZ-T48-19":
        resources = {k: "resource-" + k for k in ("openai", "search", "cosmos")}
        observed = {"dependencies": {
            k: {"resource_id": val, "status": "Pass", "private_route_observed": True,
                "principal_id": "principal-a"} for k, val in resources.items()
        }}
        expected = {"dependency_resource_ids": resources, "principal_id": "principal-a"}
    elif case_id == "AZ-T50-15":
        observed = {"image_digest": digest, "trusted_signer_id": "approved-signer",
                    "cryptographic_signature_verified": True}
        expected = {"image_digest": digest, "trusted_signer_id": "approved-signer"}
    elif case_id == "AZ-T50-17":
        observed = {"image_digest": digest, "critical_findings": 0,
                    "high_finding_ids": ["HIGH-1"], "waived_high_ids": ["HIGH-1"]}
        expected = {"image_digest": digest, "approved_high_waiver_ids": ["HIGH-1"]}
    elif case_id == "AZ-T51-19":
        observed = {"transaction_id": "tx-1", "request_id": "req-1",
                    "rule_id": "942100", "action": "Blocked", "http_status": 403}
        expected = {"transaction_id": "tx-1", "request_id": "req-1", "rule_id": "942100"}
    elif case_id == "AZ-T53-09":
        observed = {"approved_hostname": "web.internal.test",
                    "san_dns_names": ["web.internal.test", "other.internal.test"],
                    "chain_verified": True, "hostname_verified": True}
        expected = {"approved_hostname": "web.internal.test"}
    elif case_id == "AZ-T55-15":
        observed = {"source_ip": "10.10.0.7", "destination_ip": "10.40.0.9",
                    "port": 443, "tls_verified": True, "webapp_resource_id": "webapp-1",
                    "status": "Pass"}
        expected = {"approved_gateway_cidrs": ["10.10.0.0/16"],
                    "approved_webapp_pe_ips": ["10.40.0.9"],
                    "webapp_resource_id": "webapp-1"}
    elif case_id == "AZ-T58-09":
        observed = {"plan_sha256": digest, "author_id": "author",
                    "executor_id": "deploy",
                    "reviewers": [
                        {"identity_id": "security", "role": "security", "plan_sha256": digest},
                        {"identity_id": "operations", "role": "operations", "plan_sha256": digest}]}
        expected = {"plan_sha256": digest,
                    "approved_reviewer_ids": ["security", "operations"]}
    else:
        raise ValueError(case_id)

    timestamp = datetime.now(timezone.utc).isoformat()
    meta = {"case_id": case_id, "resource_id": "scope-resource-a",
            "runner_id": "runner-a", "source_sha256": "b" * 64}
    observation = {"metadata": {**meta, "observed_at_utc": timestamp},
                   "observation": observed}
    baseline = {"metadata": {**meta, "approval_record_sha256": "c" * 64},
                "expected": expected}
    return observation, baseline


class P1EvidenceCorrelationTests(unittest.TestCase):
    def test_exact_ten_original_p1_case_ids(self):
        rows = triage(ROOT)["cases"]
        by_id = {x["id"]: x for x in rows}
        self.assertEqual(len(r.CASE_CRITERIA), 10)
        self.assertTrue(set(r.CASE_CRITERIA).issubset(set(by_id)))
        for case_id in r.CASE_CRITERIA:
            self.assertEqual(by_id[case_id]["priority"], "P1", case_id)
            self.assertEqual(by_id[case_id]["semantic_risk"], "EVIDENCE")
            self.assertFalse(by_id[case_id]["criterion_verified"])

    def test_all_ten_synthetic_matching_cases_remain_review_required(self):
        for case_id in r.CASE_CRITERIA:
            with self.subTest(case_id=case_id):
                result = r.assess(case_id, *pair(case_id))
                self.assertEqual(result["result"], "REVIEW_REQUIRED", result)
                self.assertEqual(result["reason_code"],
                                 "LOCAL_MATCH_REQUIRES_INDEPENDENT_PROVENANCE")
                self.assertFalse(result["approval_authority_verified"])
                self.assertFalse(result["runner_provenance_verified"])
                self.assertFalse(result["independent_evidence_signature_verified"])
                self.assertEqual(result["azure_live_passes"], 0)
                self.assertEqual(result["release_decision"], "NO_GO")

    def test_all_cases_require_scoped_matching_resource_id(self):
        for case_id in r.CASE_CRITERIA:
            with self.subTest(case_id=case_id):
                ob, ap = pair(case_id)
                ob["metadata"]["resource_id"] = "substituted-resource"
                self.assertEqual(r.assess(case_id, ob, ap)["result"],
                                 "DIFFERENCE_REVIEW_REQUIRED")

    def test_all_cases_reject_changed_source_digest_and_runner_id(self):
        for case_id in r.CASE_CRITERIA:
            with self.subTest(case_id=case_id):
                ob, ap = pair(case_id)
                ob["metadata"]["source_sha256"] = "d" * 64
                self.assertEqual(r.assess(case_id, ob, ap)["result"],
                                 "DIFFERENCE_REVIEW_REQUIRED")
                ob, ap = pair(case_id)
                ob["metadata"]["runner_id"] = "different-runner"
                self.assertEqual(r.assess(case_id, ob, ap)["result"],
                                 "DIFFERENCE_REVIEW_REQUIRED")

    def test_missing_approval_reference_and_wrong_boolean_types_fail_closed(self):
        for case_id in r.CASE_CRITERIA:
            with self.subTest(case_id=case_id):
                ob, ap = pair(case_id)
                del ap["metadata"]["approval_record_sha256"]
                self.assertEqual(r.assess(case_id, ob, ap)["result"], "NOT_READY")
        ob, ap = pair("AZ-T55-15")
        ob["observation"]["port"] = True
        self.assertEqual(r.assess("AZ-T55-15", ob, ap)["result"], "NOT_READY")

    def test_stale_future_or_missing_observation_timestamp_is_not_ready(self):
        ob, ap = pair("AZ-T19-03")
        for value in ("2001-01-01T00:00:00+00:00",
                      (datetime.now(timezone.utc) + timedelta(days=3)).isoformat(),
                      "", "2026-11-19T10:30:00"):
            with self.subTest(value=value):
                ob["metadata"]["observed_at_utc"] = value
                self.assertEqual(r.assess("AZ-T19-03", ob, ap)["result"], "NOT_READY")

    def test_runner_ip_outside_approved_network_and_loopback_denied(self):
        ob, ap = pair("AZ-T19-03")
        ob["observation"]["private_ip"] = "10.99.1.1"
        self.assertEqual(r.assess("AZ-T19-03", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob["observation"]["private_ip"] = "127.0.0.1"
        self.assertEqual(r.assess("AZ-T19-03", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob["observation"]["private_ip"] = "garbage"
        self.assertEqual(r.assess("AZ-T19-03", ob, ap)["result"], "NOT_READY")

    def test_scm_cannot_claim_private_route_from_true_approval_flag(self):
        ob, ap = pair("AZ-T39-19")
        ob["observation"]["approved"] = True  # ignored self-asserted flag
        ob["observation"]["scm_target_ip"] = "52.1.2.3"
        self.assertEqual(r.assess("AZ-T39-19", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T39-19")
        ob["observation"]["tls_validated"] = False
        self.assertEqual(r.assess("AZ-T39-19", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")

    def test_cosmos_sdk_password_key_cannot_pass_as_managed_identity(self):
        ob, ap = pair("AZ-T43-15")
        ob["observation"]["account_key_used"] = True
        self.assertEqual(r.assess("AZ-T43-15", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T43-15")
        ob["observation"]["principal_id"] = "other-principal"
        self.assertEqual(r.assess("AZ-T43-15", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")

    def test_dependency_smoke_must_bind_each_resource_id(self):
        ob, ap = pair("AZ-T48-19")
        ob["observation"]["dependencies"]["cosmos"]["resource_id"] = "other-cosmos"
        self.assertEqual(r.assess("AZ-T48-19", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T48-19")
        ob["observation"]["dependencies"]["search"]["private_route_observed"] = False
        self.assertEqual(r.assess("AZ-T48-19", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")

    def test_image_signature_must_bind_trusted_signer_and_exact_digest(self):
        ob, ap = pair("AZ-T50-15")
        ob["observation"]["trusted_signer_id"] = "evil"
        self.assertEqual(r.assess("AZ-T50-15", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T50-15")
        ob["observation"]["cryptographic_signature_verified"] = False
        self.assertEqual(r.assess("AZ-T50-15", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")

    def test_critical_vulnerability_and_unapproved_high_waiver_rejected(self):
        ob, ap = pair("AZ-T50-17")
        ob["observation"]["critical_findings"] = 1
        self.assertEqual(r.assess("AZ-T50-17", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T50-17")
        ob["observation"]["high_finding_ids"] = ["HIGH-2"]
        self.assertEqual(r.assess("AZ-T50-17", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T50-17")
        ob["observation"]["critical_findings"] = True
        self.assertEqual(r.assess("AZ-T50-17", ob, ap)["result"], "NOT_READY")

    def test_waf_matched_is_not_blocked_even_with_http_403(self):
        ob, ap = pair("AZ-T51-19")
        ob["observation"]["action"] = "Matched"
        self.assertEqual(r.assess("AZ-T51-19", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T51-19")
        ob["observation"]["request_id"] = "other-request"
        self.assertEqual(r.assess("AZ-T51-19", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")

    def test_san_claim_requires_actual_hostname_membership_and_chain(self):
        ob, ap = pair("AZ-T53-09")
        ob["observation"]["san_dns_names"] = ["some-other.internal.test"]
        self.assertEqual(r.assess("AZ-T53-09", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T53-09")
        ob["observation"]["chain_verified"] = False
        self.assertEqual(r.assess("AZ-T53-09", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")

    def test_gateway_private_peer_and_tls_not_just_port_or_pass(self):
        ob, ap = pair("AZ-T55-15")
        ob["observation"]["destination_ip"] = "10.40.0.10"
        self.assertEqual(r.assess("AZ-T55-15", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T55-15")
        ob["observation"]["tls_verified"] = False
        self.assertEqual(r.assess("AZ-T55-15", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")

    def test_reviewer_count_must_be_independent_and_bound_to_exact_plan(self):
        ob, ap = pair("AZ-T58-09")
        ob["observation"]["reviewers"][0]["identity_id"] = "author"
        self.assertEqual(r.assess("AZ-T58-09", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T58-09")
        ob["observation"]["reviewers"][1]["plan_sha256"] = "d" * 64
        self.assertEqual(r.assess("AZ-T58-09", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        ob, ap = pair("AZ-T58-09")
        ob["observation"]["reviewers"][1]["role"] = "security"
        self.assertEqual(r.assess("AZ-T58-09", ob, ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")

    def test_cli_never_returns_zero_or_leaks_input_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            ob, ap = pair("AZ-T50-15")
            ob["observation"]["unused_secret_like_field"] = "SYNTHETIC_DO_NOT_PRINT"
            a, b = p / "observation.json", p / "baseline.json"
            a.write_text(json.dumps(ob), encoding="utf-8")
            b.write_text(json.dumps(ap), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts/review_p1_evidence_correlation.py"),
                 "--case-id", "AZ-T50-15", "--observation", str(a), "--baseline", str(b)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(proc.returncode, 2, proc.stderr)
            result = json.loads(proc.stdout)
            self.assertEqual(result["result"], "REVIEW_REQUIRED")
            self.assertEqual(result["release_decision"], "NO_GO")
            self.assertNotIn("SYNTHETIC_DO_NOT_PRINT", proc.stdout)

    def test_missing_or_malformed_files_never_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.json"
            rpath = Path(tmp) / "record.json"
            rpath.write_text("not json", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts/review_p1_evidence_correlation.py"),
                 "--case-id", "AZ-T50-15", "--observation", str(path),
                 "--baseline", str(rpath)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(json.loads(proc.stdout)["result"], "NOT_READY")


if __name__ == "__main__":
    unittest.main()
