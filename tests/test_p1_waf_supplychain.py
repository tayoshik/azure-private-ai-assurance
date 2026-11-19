"""Source-grounded synthetic regression for 10 P1 WAF/supply chain/route controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import review_p1_waf_supplychain as p
from scripts.triage_static_criteria import triage

ROOT = Path(__file__).resolve().parents[1]


def fixture(case_id, root):
    a, o = {}, {}
    h = "a" * 64
    if case_id == "AZ-T50-13":
        o = {"image_resource_id":"acr-test","repository_name":"synthetic/app",
             "image_version":"v1","image_digest":h,"sbom_format":"CycloneDX",
             "sbom_sha256":"b"*64,"component_count":2,
             "sbom_artifact_digest_matches":True,
             "immutable_sbom_reference":"synthetic-artifact#bom"}
        a = {k:o[k] for k in ("image_resource_id","repository_name",
                              "image_version","image_digest","sbom_sha256")}
        a["approved_format"]="CycloneDX"
    elif case_id == "AZ-T50-21":
        o = {"policy_resource_id":"gatekeeper-1","unapproved_image_ref":"synthetic/untrusted:v1",
             "test_request_id":"admission-1","denial_rule_id":"image-signature-policy",
             "denied":True,"decision":"Deny","admission_log_correlation_id":"admission-log-1",
             "used_isolated_test":True}
        a = {k:o[k] for k in ("policy_resource_id","unapproved_image_ref",
                              "test_request_id","denial_rule_id")}
    elif case_id in p.WAF_IDS:
        name = { "AZ-T51-13":"benign-allowed",
                 "AZ-T51-15":"sqli-denied",
                 "AZ-T51-17":"xss-denied"}[case_id]
        filename = root / (case_id+".xml")
        filename.write_text('<testsuite tests="1"><testcase name="'+name+'"/></testsuite>',
                            encoding="utf-8")
        actual_sha = sha256(filename.read_bytes()).hexdigest()
        o = {"waf_policy_id":"synthetic-waf","test_request_id":"synthetic-req-"+case_id,
             "scenario_id":name,"junit_path":str(filename),
             "waf_action":"Allowed" if case_id=="AZ-T51-13" else "Blocked",
             "http_status":200 if case_id=="AZ-T51-13" else 403,
             "waf_log_correlation_id":"synthetic-log-"+case_id,
             "authorized_nonproduction_test":True}
        a = {k:o[k] for k in ("waf_policy_id","test_request_id","scenario_id")}
        a.update({"approved_junit_sha256":actual_sha,"approved_junit_testcase":name})
        if case_id!="AZ-T51-13":
            o["waf_rule_id"] = "942100" if case_id=="AZ-T51-15" else "941100"
            a["waf_rule_id"] = o["waf_rule_id"]
    elif case_id == "AZ-T53-17":
        o = {"gateway_resource_id":"gateway-1",
             "keyvault_secret_uri":"https://vault.internal.test/secrets/cert",
             "old_secret_version":"ver-001","new_secret_version":"ver-002",
             "change_ticket":"SYNTHETIC-CHG","rollback_secret_version":"ver-001",
             "renewal_test_succeeded":True,"rollback_test_succeeded":True,
             "private_key_disclosed":False,"isolated_drill_log_id":"drill-1"}
        a = {k:o[k] for k in ("gateway_resource_id","keyvault_secret_uri",
                  "old_secret_version","new_secret_version","change_ticket")}
    elif case_id == "AZ-T54-19":
        o = {"gateway_resource_id":"appgw","backend_resource_id":"webapp",
             "monitor_alert_rule_id":"gateway-503","approved_window_id":"window-test",
             "total_approved_requests":30,"unexpected_503_count":0,
             "backend_health_healthy":True,"synthetic_incident_alert_delivered":True,
             "alert_ack_id":"ack-1"}
        a = {k:o[k] for k in ("gateway_resource_id","backend_resource_id",
                      "monitor_alert_rule_id","approved_window_id")}
    elif case_id == "AZ-T55-11":
        o = {"backend_resource_id":"webapp","approved_hostname":"app.internal.test",
             "certificate_sha256":h,"san_dns_names":["app.internal.test"],
             "hostname_verified":True,"chain_verified":True,"tls_bypass_enabled":False}
        a = {k:o[k] for k in ("backend_resource_id","approved_hostname",
                              "certificate_sha256")}
    elif case_id == "AZ-T56-09":
        o = {"test_source_subnet_id":"unauthorized-test-segment",
             "target_pe_resource_id":"search-pe","test_request_id":"deny-req-1",
             "approved_deny_rule_id":"nsg-deny","source_ip":"10.77.0.5",
             "test_result":"Blocked","flow_deny_rule_id":"nsg-deny",
             "flow_log_id":"deny-flow-1"}
        a = {k:o[k] for k in ("test_source_subnet_id","target_pe_resource_id",
                       "test_request_id","approved_deny_rule_id")}
        a["unauthorized_test_cidrs"]=["10.77.0.0/24"]
    elif case_id == "AZ-T56-21":
        o = {"route_table_resource_id":"rt1","change_ticket":"TEST-CHG",
             "simulated_drift_route_id":"synthetic-route",
             "monitor_alert_rule_id":"route-alert",
             "baseline_route_set_sha256":h,"post_rollback_route_set_sha256":h,
             "unapproved_changes_remaining":0,"simulated_drift_detected":True,
             "alert_delivered":True,"alert_ack_id":"synthetic-alert-ack",
             "rollback_run_id":"synthetic-rollback"}
        a = {k:o[k] for k in ("route_table_resource_id","change_ticket",
                              "simulated_drift_route_id","monitor_alert_rule_id",
                              "baseline_route_set_sha256","post_rollback_route_set_sha256")}
    else:
        raise KeyError(case_id)
    common = {"case_id":case_id,"resource_id":"synthetic-test-resource",
              "runner_id":"nonprod-runner","source_sha256":"c"*64}
    ob = {"metadata":{**common,"observed_at_utc":datetime.now(timezone.utc).isoformat()},
          "observation":o}
    approved = {"metadata":{**common,"approval_record_sha256":"d"*64},
                "expected":a}
    return ob, approved


class TenSourceReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def f(self, id):
        return fixture(id, self.root)

    def test_exact_ten_distinct_original_p1_cases(self):
        rows = {x["id"]:x for x in triage(ROOT)["cases"]}
        old = set(__import__("scripts.review_p1_source_evidence",fromlist=["CASES"]).CASES)
        old |= set(__import__("scripts.review_p1_network_monitor",fromlist=["CASES"]).CASES)
        old |= set(__import__("scripts.review_p1_evidence_correlation",fromlist=["CASE_CRITERIA"]).CASE_CRITERIA)
        self.assertEqual(len(p.CASES),10)
        self.assertFalse(set(p.CASES)&old)
        self.assertTrue(all(rows[x]["priority"]=="P1" for x in p.CASES))

    def test_all_ten_matching_synthetic_records_never_produce_pass(self):
        for id in p.CASES:
            with self.subTest(id=id):
                actual=p.assess(id,*self.f(id))
                self.assertEqual(actual["result"],"REVIEW_REQUIRED", actual)
                self.assertEqual(actual["release_decision"],"NO_GO")
                self.assertEqual(actual["azure_live_passes"],0)
                self.assertFalse(actual["approval_signature_verified"])
                self.assertFalse(actual["junit_execution_provenance_verified"])

    def test_wrong_case_scope_runner_digest_fail_for_all(self):
        for id in p.CASES:
            for key,val in (("case_id","AZ-T00-00"),("resource_id","wrong-resource"),
                            ("runner_id","wrong-runner"),("source_sha256","e"*64)):
                with self.subTest(id=id,key=key):
                    ob,ap=self.f(id)
                    ob["metadata"][key]=val
                    self.assertEqual(p.assess(id,ob,ap)["result"],
                                     "DIFFERENCE_REVIEW_REQUIRED")

    def test_invalid_approval_and_old_time_fail_for_all(self):
        for id in p.CASES:
            ob,ap=self.f(id)
            ap["metadata"]["approval_record_sha256"]="invalid"
            self.assertEqual(p.assess(id,ob,ap)["result"],"NOT_READY")
            ob,ap=self.f(id)
            ob["metadata"]["observed_at_utc"]="2000-01-01T00:00:00+00:00"
            self.assertEqual(p.assess(id,ob,ap)["result"],"NOT_READY")

    def test_sbom_wrong_digest_or_component_count_and_format(self):
        id="AZ-T50-13"
        for key,val in (("image_digest","e"*64),("sbom_sha256","f"*64),
                        ("component_count",0),("component_count",True),
                        ("sbom_format","unknown"),("sbom_artifact_digest_matches",False)):
            ob,ap=self.f(id)
            ob["observation"][key]=val
            self.assertNotEqual(p.assess(id,ob,ap)["result"],"REVIEW_REQUIRED")

    def test_untrusted_image_must_be_denied_by_right_policy(self):
        id="AZ-T50-21"
        for key,val in (("denied",False),("decision","Allowed"),
                        ("policy_resource_id","other"),
                        ("used_isolated_test",False)):
            ob,ap=self.f(id)
            ob["observation"][key]=val
            self.assertNotEqual(p.assess(id,ob,ap)["result"],"REVIEW_REQUIRED")

    def test_waf_benign_must_be_allowed_not_denied(self):
        id="AZ-T51-13"
        for key,val in (("waf_action","Blocked"),("http_status",403),
                        ("authorized_nonproduction_test",False)):
            ob,ap=self.f(id)
            ob["observation"][key]=val
            self.assertEqual(p.assess(id,ob,ap)["result"],"DIFFERENCE_REVIEW_REQUIRED")

    def test_waf_sqli_xss_must_be_rule_correlated_blocked_403(self):
        for id in ("AZ-T51-15","AZ-T51-17"):
            for key,val in (("waf_action","Matched"),("http_status",200),
                            ("waf_rule_id","wrong-rule")):
                ob,ap=self.f(id)
                ob["observation"][key]=val
                self.assertEqual(p.assess(id,ob,ap)["result"],
                                 "DIFFERENCE_REVIEW_REQUIRED")

    def test_xml_must_match_sha_name_counts_without_failures_skips(self):
        id="AZ-T51-15"
        for content in (
            '<testsuite tests="1"><testcase name="sqli-denied"><failure/></testcase></testsuite>',
            '<testsuite tests="1"><testcase name="sqli-denied"><skipped/></testcase></testsuite>',
            '<testsuite tests="2"><testcase name="sqli-denied"/></testsuite>',
            '<testsuite tests="1"><testcase name="some-other-test"/></testsuite>',
            '<!DOCTYPE foo [<!ENTITY x "bad">]><testsuite tests="1"><testcase name="sqli-denied"/></testsuite>',
            '<testsuite tests="1"><testcase name="sqli-denied"></testsuite>',
        ):
            ob,ap=self.f(id)
            path=Path(ob["observation"]["junit_path"])
            path.write_text(content,encoding="utf-8")
            ap["expected"]["approved_junit_sha256"]=sha256(path.read_bytes()).hexdigest()
            result=p.assess(id,ob,ap)["result"]
            if "</testsuite>" not in content:
                self.assertEqual(result,"NOT_READY")
            else:
                self.assertNotEqual(result,"REVIEW_REQUIRED", content)
        ob,ap=self.f(id)
        ob["observation"]["junit_path"]=str(self.root/"absent.xml")
        self.assertEqual(p.assess(id,ob,ap)["result"],"NOT_READY")

    def test_junit_hash_mismatch_causes_difference(self):
        ob,ap=self.f("AZ-T51-17")
        ap["expected"]["approved_junit_sha256"]="0"*64
        self.assertEqual(p.assess("AZ-T51-17",ob,ap)["result"],
                         "DIFFERENCE_REVIEW_REQUIRED")

    def test_tls_rotation_requires_rollback_to_previous_without_key_leak(self):
        id="AZ-T53-17"
        for key,val in (("new_secret_version","ver-001"),
                        ("rollback_secret_version","ver-003"),
                        ("renewal_test_succeeded",False),
                        ("rollback_test_succeeded",False),
                        ("private_key_disclosed",True)):
            ob,ap=self.f(id)
            ob["observation"][key]=val
            self.assertNotEqual(p.assess(id,ob,ap)["result"],"REVIEW_REQUIRED")

    def test_gateway_503_monitor_needs_enough_requests_and_alert(self):
        id="AZ-T54-19"
        for key,val in (("total_approved_requests",0),
                        ("total_approved_requests",10),
                        ("unexpected_503_count",1),
                        ("backend_health_healthy",False),
                        ("synthetic_incident_alert_delivered",False)):
            ob,ap=self.f(id)
            ob["observation"][key]=val
            self.assertNotEqual(p.assess(id,ob,ap)["result"],"REVIEW_REQUIRED")

    def test_backend_tls_requires_san_chain_no_bypass(self):
        id="AZ-T55-11"
        for key,val in (("certificate_sha256","0"*64),
                        ("san_dns_names",["other.internal.test"]),
                        ("chain_verified",False),
                        ("hostname_verified",False),
                        ("tls_bypass_enabled",True)):
            ob,ap=self.f(id)
            ob["observation"][key]=val
            self.assertNotEqual(p.assess(id,ob,ap)["result"],"REVIEW_REQUIRED")

    def test_subnet_denial_needs_source_and_deny_flow_id(self):
        id="AZ-T56-09"
        for key,val in (("source_ip","10.78.0.5"),
                        ("test_result","Timeout"),
                        ("flow_deny_rule_id","unrelated-rule"),
                        ("flow_log_id","")):
            ob,ap=self.f(id)
            ob["observation"][key]=val
            self.assertNotEqual(p.assess(id,ob,ap)["result"],"REVIEW_REQUIRED")

    def test_route_change_must_restore_exact_digest_with_alert_ack(self):
        id="AZ-T56-21"
        for key,val in (("post_rollback_route_set_sha256","e"*64),
                        ("unapproved_changes_remaining",1),
                        ("unapproved_changes_remaining",True),
                        ("simulated_drift_detected",False),
                        ("alert_delivered",False),
                        ("alert_ack_id","")):
            ob,ap=self.f(id)
            ob["observation"][key]=val
            self.assertNotEqual(p.assess(id,ob,ap)["result"],"REVIEW_REQUIRED")

    def test_cli_never_exits_zero_and_does_not_print_input(self):
        id="AZ-T55-11"
        ob,ap=self.f(id)
        ob["observation"]["unrelated_secret"]="NEVER_ECHO_SYNTHETIC_DATA"
        o,a=self.root/"obs.json",self.root/"approved.json"
        o.write_text(json.dumps(ob),encoding="utf-8")
        a.write_text(json.dumps(ap),encoding="utf-8")
        proc=subprocess.run([sys.executable,str(ROOT/"scripts/review_p1_waf_supplychain.py"),
                             "--case-id",id,"--observation",str(o),"--approved",str(a)],
                            cwd=ROOT,capture_output=True,text=True,check=False)
        self.assertEqual(proc.returncode,2,proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["result"],"REVIEW_REQUIRED")
        self.assertNotIn("NEVER_ECHO_SYNTHETIC_DATA",proc.stdout)

    def test_missing_file_and_unrecognized_case_are_not_ready(self):
        for id in ("AZ-T51-13","AZ-T99-99"):
            ob,ap=self.f("AZ-T51-13")
            (self.root/"absent.json").unlink(missing_ok=True)
            run=subprocess.run([sys.executable,str(ROOT/"scripts/review_p1_waf_supplychain.py"),
                 "--case-id",id,"--observation",str(self.root/"absent.json"),
                 "--approved",str(self.root/"absent.json")],
                cwd=ROOT,capture_output=True,text=True,check=False)
            self.assertEqual(run.returncode,2)
            self.assertEqual(json.loads(run.stdout)["result"],"NOT_READY")


if __name__ == "__main__":
    unittest.main()
