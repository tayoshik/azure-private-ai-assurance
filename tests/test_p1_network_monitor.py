"""Untrusted fixture regressions for ten source-grounded P1 network/monitor reviews."""
from datetime import datetime, timedelta, timezone
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import review_p1_network_monitor as p
from scripts.triage_static_criteria import triage

ROOT = Path(__file__).resolve().parents[1]


def iso(dt):
    return dt.astimezone(timezone.utc).isoformat()


def fixture(case_id):
    t = datetime.now(timezone.utc)
    src_sha = "b"*64
    meta = {"case_id":case_id,"resource_id":"resource-under-test",
            "runner_id":"synthetic-runner","source_sha256":src_sha}
    a, o = {}, {}
    if case_id == "AZ-T18-19":
        a={"target_resource_id":"resource-under-test","expected_block_rule_id":"deny-001",
           "approved_external_probe_cidrs":["192.0.2.0/24"]}
        o={"target_resource_id":"resource-under-test","expected_block_rule_id":"deny-001",
           "probe_source_ip":"192.0.2.7","effective_public_network_access":False,
           "external_probe_result":"Denied","blocking_rule_id":"deny-001",
           "correlation_id":"synthetic-request-1"}
    elif case_id == "AZ-T19-19":
        a={"principal_id":"managed-principal","role_scope":"scope-rg",
           "token_audience":"https://management.azure.com/"}
        o={**a,"auth_method":"managed_identity","token_obtained":True,
           "raw_token_logged":False,"correlation_id":"synthetic-auth-1"}
    elif case_id == "AZ-T41-09":
        a={"resolver_id":"resolver-1","indexer_hostname":"idx.privatelink.test",
           "approved_pe_ips":["10.20.1.4"]}
        o={"resolver_id":"resolver-1","indexer_hostname":"idx.privatelink.test",
           "resolved_ip_addresses":["10.20.1.4"],"query_id":"synthetic-dns-1"}
    elif case_id == "AZ-T42-21":
        a={"unauthorized_principal_id":"forbidden-principal","operation":"CosmosRead"}
        o={**a,"denied":True,"http_status":403,
           "audit_correlation_id":"synthetic-denied-1"}
    elif case_id == "AZ-T48-17":
        resources={"openai":("ai.internal.test","10.30.1.4"),
                   "search":("search.internal.test","10.30.1.5"),
                   "cosmos":("cosmos.internal.test","10.30.1.6")}
        a={"resolver_id":"resolver-1",
           "approved_private_answers":{
               key:{"hostname":host,"approved_pe_ips":[ip]}
               for key,(host,ip) in resources.items()}}
        o={"resolver_id":"resolver-1",
           "answers":{
               key:{"status":"Resolved","hostname":host,"addresses":[ip]}
               for key,(host,ip) in resources.items()}}
    elif case_id == "AZ-T49-17":
        a={"approved_public_targets":["8.8.8.8","1.1.1.1"],
           "approved_source_cidrs":["10.50.0.0/24"]}
        o={"source_ip":"10.50.0.7","public_probes":[
           {"destination_ip":ip,"outcome":"Denied","flow_log_id":f"synthetic-flow-{i}"}
           for i,ip in enumerate(a["approved_public_targets"])]}
    elif case_id == "AZ-T51-21":
        a={"policy_resource_id":"waf-policy","policy_revision":"rev-current",
           "change_ticket":"CHG-SYNTHETIC","reviewer_id":"approved-reviewer",
           "approved_rule_ids":["942100","941100"],"approved_exception_rule_ids":[]}
        o={"policy_resource_id":"waf-policy","policy_revision":"rev-current",
           "change_ticket":"CHG-SYNTHETIC","reviewer_id":"approved-reviewer",
           "effective_rule_ids":["942100","941100"],"exception_rule_ids":[],
           "rollback_revision":"rev-prior"}
    elif case_id == "AZ-T55-21":
        a={"gateway_resource_id":"appgw-1","backend_resource_id":"appsvc-1",
           "request_id":"synthetic-req-1"}
        o={**a,"appgw_access":{"request_id":"synthetic-req-1",
               "resource_id":"appgw-1","observed_at_utc":iso(t-timedelta(seconds=42)),
               "route":"private"},
           "app_service":{"request_id":"synthetic-req-1","resource_id":"appsvc-1",
                          "observed_at_utc":iso(t-timedelta(seconds=40))}}
    elif case_id == "AZ-T57-17":
        a={"workspace_resource_id":"workspace-1","approved_p95_minutes":4.0}
        o={"workspace_resource_id":"workspace-1","p95_minutes":2.0,
           "ingestion_samples":[{"event_utc":iso(t-timedelta(minutes=10+i)),
                                 "ingested_utc":iso(t-timedelta(minutes=8+i))}
                                for i in range(20)]}
    elif case_id == "AZ-T57-21":
        a={"alert_rule_id":"alert-1","recipient_id":"protected-recipient",
           "delivery_channel":"secured-system",
           "synthetic_event_id":"event-1","approved_delivery_lag_minutes":3.0}
        o={k:a[k] for k in ("alert_rule_id","recipient_id",
                             "delivery_channel","synthetic_event_id")}
        o.update({"delivery_ack_id":"synthetic-ack-1","delivery_status":"Delivered",
                  "emitted_at_utc":iso(t-timedelta(minutes=4)),
                  "delivered_at_utc":iso(t-timedelta(minutes=3))})
    else:
        raise ValueError(case_id)
    observation={"metadata":{**meta,"observed_at_utc":iso(t)},
                 "observation":o}
    baseline={"metadata":{**meta,"approval_record_sha256":"c"*64},
              "expected":a}
    return observation,baseline


class NextTenNetworkMonitorTests(unittest.TestCase):
    def test_exact_ten_new_original_p1_ids_and_no_overlap(self):
        ranked={x["id"]:x for x in triage(ROOT)["cases"]}
        self.assertEqual(len(p.CASES),10)
        self.assertTrue(set(p.CASES).issubset(ranked))
        previous={"AZ-T19-03","AZ-T39-19","AZ-T43-15","AZ-T48-19",
                  "AZ-T50-15","AZ-T50-17","AZ-T51-19","AZ-T53-09",
                  "AZ-T55-15","AZ-T58-09"}
        self.assertFalse(set(p.CASES)&previous)
        self.assertTrue(all(ranked[x]["priority"]=="P1" for x in p.CASES))

    def test_all_ten_synthetic_matching_cases_are_never_azure_pass(self):
        for cid in p.CASES:
            with self.subTest(cid=cid):
                j=p.assess(cid,*fixture(cid))
                self.assertEqual(j["result"],"REVIEW_REQUIRED",j)
                self.assertFalse(j["signature_verified"])
                self.assertFalse(j["runner_identity_verified"])
                self.assertFalse(j["approval_authority_verified"])
                self.assertEqual(j["azure_live_passes"],0)
                self.assertEqual(j["release_decision"],"NO_GO")

    def test_tampered_resource_runner_source_or_case_never_matches(self):
        for cid in p.CASES:
            with self.subTest(cid=cid):
                for field,new in (("resource_id","other-resource"),
                                  ("runner_id","other-runner"),
                                  ("source_sha256","f"*64),
                                  ("case_id","AZ-T00-00")):
                    o,a=fixture(cid)
                    o["metadata"][field]=new
                    self.assertEqual(p.assess(cid,o,a)["result"],
                                     "DIFFERENCE_REVIEW_REQUIRED")

    def test_stale_future_missing_and_unsigned_approval_rejected(self):
        cid="AZ-T18-19"
        for time in ("2000-01-01T00:00:00+00:00",
                     iso(datetime.now(timezone.utc)+timedelta(days=2)),
                     "NOT-A-TIME","2026-11-19T10:00:00"):
            o,a=fixture(cid)
            o["metadata"]["observed_at_utc"]=time
            self.assertEqual(p.assess(cid,o,a)["result"],"NOT_READY")
        o,a=fixture(cid)
        a["metadata"]["approval_record_sha256"]="bad"
        self.assertEqual(p.assess(cid,o,a)["result"],"NOT_READY")

    def test_external_denial_not_proof_if_wrong_rule_or_public_access_true(self):
        o,a=fixture("AZ-T18-19")
        o["observation"]["blocking_rule_id"]="other-rule"
        self.assertEqual(p.assess("AZ-T18-19",o,a)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture("AZ-T18-19")
        o["observation"]["effective_public_network_access"]=True
        self.assertEqual(p.assess("AZ-T18-19",o,a)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")

    def test_managed_identity_no_token_logging_and_right_scope(self):
        cid="AZ-T19-19"
        o,a=fixture(cid)
        o["observation"]["raw_token_logged"]=True
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["principal_id"]="wrong"
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")

    def test_indexer_private_dns_not_public_wrong_or_nxdomain(self):
        cid="AZ-T41-09"
        for addr in ("8.8.8.8","10.20.1.5","localhost"):
            o,a=fixture(cid)
            o["observation"]["resolved_ip_addresses"]=[addr]
            self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED")

    def test_denied_identity_requires_expected_principal_and_status(self):
        cid="AZ-T42-21"
        for field,value in (("http_status",401),("http_status",True),
                            ("denied",False),("unauthorized_principal_id","authorized")):
            o,a=fixture(cid)
            o["observation"][field]=value
            self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED")

    def test_dependency_dns_distinguishes_nxdomain_wrong_pe_and_public(self):
        cid="AZ-T48-17"
        for field,value in (("status","NXDOMAIN"),("status","Timeout"),
                            ("addresses",["8.8.8.8"]),
                            ("addresses",["10.30.1.99"])):
            o,a=fixture(cid)
            o["observation"]["answers"]["search"][field]=value
            self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED")

    def test_public_egress_must_be_denied_and_linked_to_test_log(self):
        cid="AZ-T49-17"
        o,a=fixture(cid)
        o["observation"]["public_probes"][0]["outcome"]="Allowed"
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        del o["observation"]["public_probes"][0]["flow_log_id"]
        self.assertEqual(p.assess(cid,o,a)["result"],"NOT_READY")
        o,a=fixture(cid)
        o["observation"]["public_probes"][0]["destination_ip"]="10.10.10.10"
        self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED")

    def test_waf_revision_requires_exact_rules_exceptions_and_rollback(self):
        cid="AZ-T51-21"
        o,a=fixture(cid)
        o["observation"]["effective_rule_ids"].remove("941100")
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["exception_rule_ids"].append("941100")
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["rollback_revision"]="rev-current"
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")

    def test_gateway_and_backend_must_share_request_and_time(self):
        cid="AZ-T55-21"
        o,a=fixture(cid)
        o["observation"]["app_service"]["request_id"]="different"
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["app_service"]["observed_at_utc"]=iso(
            datetime.now(timezone.utc)-timedelta(hours=3))
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["appgw_access"]["route"]="public"
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")

    def test_log_p95_is_recomputed_from_individual_timestamp_pairs(self):
        cid="AZ-T57-17"
        o,a=fixture(cid)
        o["observation"]["p95_minutes"]=0.0
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["ingestion_samples"][0]["ingested_utc"]=iso(
            datetime.now(timezone.utc)+timedelta(hours=6))
        self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED")
        o,a=fixture(cid)
        a["expected"]["approved_p95_minutes"]=1.0
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["p95_minutes"]=True
        self.assertEqual(p.assess(cid,o,a)["result"],"NOT_READY")

    def test_alert_must_have_correlated_recipient_ack_and_bounded_time(self):
        cid="AZ-T57-21"
        o,a=fixture(cid)
        o["observation"]["recipient_id"]="other-recipient"
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        del o["observation"]["delivery_ack_id"]
        self.assertEqual(p.assess(cid,o,a)["result"],"NOT_READY")
        o,a=fixture(cid)
        o["observation"]["delivered_at_utc"]=iso(
            datetime.now(timezone.utc)+timedelta(hours=4))
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")

    def test_cli_never_exits_zero_even_with_all_fields_present(self):
        with tempfile.TemporaryDirectory() as d:
            o,a=fixture("AZ-T19-19")
            po,pa=Path(d)/"obs.json",Path(d)/"base.json"
            po.write_text(json.dumps(o),encoding="utf-8")
            pa.write_text(json.dumps(a),encoding="utf-8")
            run=subprocess.run([sys.executable,
                str(ROOT/"scripts/review_p1_network_monitor.py"),
                "--case-id","AZ-T19-19","--observation",str(po),
                "--baseline",str(pa)],cwd=ROOT,text=True,capture_output=True,check=False)
            self.assertEqual(run.returncode,2,run.stderr)
            self.assertEqual(json.loads(run.stdout)["result"],"REVIEW_REQUIRED")
            self.assertEqual(json.loads(run.stdout)["release_decision"],"NO_GO")

    def test_unsafe_json_or_missing_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/"bad.json"
            file.write_text("broken json",encoding="utf-8")
            run=subprocess.run([sys.executable,
                str(ROOT/"scripts/review_p1_network_monitor.py"),
                "--case-id","AZ-T48-17","--observation",str(file),
                "--baseline",str(file)],cwd=ROOT,text=True,capture_output=True,check=False)
            self.assertEqual(run.returncode,2)
            self.assertEqual(json.loads(run.stdout)["result"],"NOT_READY")


if __name__ == "__main__":
    unittest.main()
