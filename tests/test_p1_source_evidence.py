"""Regression: ten source-grounded P1 local evidence comparisons cannot issue PASS."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import review_p1_source_evidence as p
from scripts.triage_static_criteria import triage

ROOT = Path(__file__).resolve().parents[1]


def fixture(case_id):
    h, rev = "a"*64, "b"*40
    now = datetime.now(timezone.utc).isoformat()
    o, a = {}, {}
    if case_id == "AZ-T35-13":
        o = {"search_resource_id":"search-resource", "index_name":"synthetic-index",
             "principal_id":"identity-1", "runner_resource_id":"private-runner",
             "query_id":"synthetic-query", "auth_method":"managed_identity",
             "http_status":200, "private_route_observed":True,
             "returned_synthetic_doc_ids":["synthetic-doc-1","synthetic-doc-2"]}
        a = {k:o[k] for k in ("search_resource_id","index_name","principal_id",
                             "runner_resource_id","query_id")}
        a["expected_synthetic_doc_ids"]=["synthetic-doc-1","synthetic-doc-2"]
    elif case_id == "AZ-T40-13":
        o = {"app_resource_id":"app-resource","runner_resource_id":"private-runner",
             "scm_hostname":"scm.qa.internal.test","deployment_id":"deployment-1",
             "source_commit_sha":rev,"artifact_sha256":h,
             "scm_private_ip":"10.21.0.4", "tls_verified":True,
             "private_route_observed":True, "deployment_status":"Succeeded"}
        a={k:o[k] for k in ("app_resource_id","runner_resource_id",
                            "scm_hostname","deployment_id","source_commit_sha",
                            "artifact_sha256")}
        a["approved_scm_pe_ips"]=["10.21.0.4"]
    elif case_id == "AZ-T41-11":
        o={"indexer_resource_id":"indexer-1","datasource_resource_id":"source-1",
           "indexer_principal_id":"principal-1","datasource_hostname":"source.internal.test",
           "datasource_private_ip":"10.22.0.4", "private_route_observed":True,
           "connection_status":"Succeeded", "correlation_id":"correlation-1"}
        a={k:o[k] for k in ("indexer_resource_id","datasource_resource_id",
                            "indexer_principal_id","datasource_hostname")}
        a["approved_datasource_pe_ips"]=["10.22.0.4"]
    elif case_id == "AZ-T42-17":
        o={"policy_revision":"redaction-v1","scan_scope_id":"synthetic-scan",
           "raw_token_logged":False,
           "artifact_scans":{k:{"scanned_artifact_count":3,
                    "positive_control_detections":2,
                    "unredacted_token_findings":0,
                    "sanitized_scan_ref":"synthetic-scan/"+k}
              for k in ("pipeline_logs","application_logs","traces")}}
        a={"policy_revision":"redaction-v1","scan_scope_id":"synthetic-scan"}
    elif case_id == "AZ-T43-17":
        o={"unauthorized_principal_id":"forbidden-principal",
           "container_resource_id":"container-1","denied_operation":"Read",
           "request_id":"req-1","result":"Denied","http_status":403,
           "account_key_used":False,"audit_log_correlation_id":"audit-1"}
        a={k:o[k] for k in ("unauthorized_principal_id","container_resource_id",
                            "denied_operation","request_id")}
    elif case_id == "AZ-T48-21":
        o={"redaction_policy_revision":"redaction-policy-v1",
           "pipeline_scope_id":"synthetic-pipeline",
           "synthetic_test_fixture_id":"fixture-non-sensitive",
           "redaction_controls":{k:{"synthetic_marker_count":3,
               "masking_positive_control_detected":3,
               "unredacted_marker_findings":0,
               "sanitized_evidence_ref":"synthetic-redaction/"+k}
           for k in ("prompt","credentials","personal_data")}}
        a={k:o[k] for k in ("redaction_policy_revision","pipeline_scope_id",
                            "synthetic_test_fixture_id")}
    elif case_id == "AZ-T49-15":
        o={"app_resource_id":"app-1","app_principal_id":"app-mi",
           "runner_resource_id":"private-runner","dependencies":{}}
        a={k:o[k] for k in ("app_resource_id","app_principal_id",
                            "runner_resource_id")}
        a["approved_private_endpoints"]={}
        for k,ip in (("openai","10.23.0.4"),("search","10.23.0.5"),
                     ("cosmos","10.23.0.6")):
            row={"resource_id":"resource-"+k,"hostname":k+".internal.test",
                 "resolved_private_ip":ip,"port":443,
                 "tls_verified":True,"private_route_observed":True,
                 "status":"Succeeded"}
            o["dependencies"][k]=row
            a["approved_private_endpoints"][k]={
                "resource_id":row["resource_id"],"hostname":row["hostname"],
                "approved_pe_ips":[ip]}
    elif case_id == "AZ-T50-19":
        o={"acr_resource_id":"acr-1","runner_resource_id":"private-runner",
           "repository_name":"nonprod/synthetic","source_commit_sha":rev,
           "image_digest":h,"runner_source_ip":"10.24.0.4",
           "acr_private_ip":"10.25.0.4","private_route_observed":True,
           "raw_registry_credential_logged":False,"pull_status":"Succeeded"}
        a={k:o[k] for k in ("acr_resource_id","runner_resource_id",
                            "repository_name","source_commit_sha","image_digest")}
        a["approved_runner_cidrs"]=["10.24.0.0/24"]
        a["approved_acr_pe_ips"]=["10.25.0.4"]
    elif case_id == "AZ-T56-19":
        o={"gateway_resource_id":"appgw-1","request_id":"request-1",
           "runner_resource_id":"private-runner",
           "observed_flows":[{
               "request_id":"request-1","source_ip":"10.26.0.4",
               "destination_ip":ip,"destination_port":443,
               "collector_id":"synthetic-collector",
               "flow_log_id":"flow-"+str(i)}
              for i,ip in enumerate(("10.27.0.4","10.27.0.5"))]}
        a={k:o[k] for k in ("gateway_resource_id","request_id",
                            "runner_resource_id")}
        a["approved_source_cidrs"]=["10.26.0.0/24"]
        a["approved_destination_pe_ips"]=["10.27.0.4","10.27.0.5"]
    elif case_id == "AZ-T58-07":
        o={"deployment_scope_id":"scope-1","change_ticket":"SYNTHETIC-CHANGE",
           "release_actor_id":"executor-1","source_commit_sha":rev,
           "approved_commit_sha":rev,"plan_source_commit_sha":rev,
           "plan_sha256":h,"reviewer_id":"reviewer-1"}
        a={k:o[k] for k in ("deployment_scope_id","change_ticket",
             "release_actor_id","source_commit_sha","approved_commit_sha",
             "plan_source_commit_sha","plan_sha256")}
        a["approved_reviewer_id"]="reviewer-1"
    else:
        raise KeyError(case_id)

    meta={"case_id":case_id,"resource_id":"scope-resource",
          "runner_id":"runner-metadata","source_sha256":"c"*64}
    return ({"metadata":{**meta,"observed_at_utc":now},"observation":o},
            {"metadata":{**meta,"approval_record_sha256":"d"*64},"expected":a})


class SourceEvidenceCorrelationTests(unittest.TestCase):
    def test_exact_ten_unique_original_p1_ids_no_overlap_with_prior_twenty(self):
        ranked={row["id"]:row for row in triage(ROOT)["cases"]}
        previous={"AZ-T19-03","AZ-T39-19","AZ-T43-15","AZ-T48-19","AZ-T50-15",
                  "AZ-T50-17","AZ-T51-19","AZ-T53-09","AZ-T55-15","AZ-T58-09",
                  "AZ-T18-19","AZ-T19-19","AZ-T41-09","AZ-T42-21","AZ-T48-17",
                  "AZ-T49-17","AZ-T51-21","AZ-T55-21","AZ-T57-17","AZ-T57-21"}
        self.assertEqual(len(p.CASES),10)
        self.assertFalse(set(p.CASES)&previous)
        self.assertTrue(all(ranked[k]["priority"]=="P1" for k in p.CASES))

    def test_all_ten_synthetic_matching_inputs_remain_unapproved(self):
        for case_id in p.CASES:
            with self.subTest(case_id=case_id):
                x=p.assess(case_id,*fixture(case_id))
                self.assertEqual(x["result"],"REVIEW_REQUIRED",x)
                self.assertEqual(x["azure_live_passes"],0)
                self.assertEqual(x["release_decision"],"NO_GO")
                self.assertFalse(x["origin_signature_verified"])
                self.assertFalse(x["approval_authority_verified"])
                self.assertFalse(x["actual_runner_and_network_verified"])

    def test_all_ten_reject_tampered_scope_runner_source_and_case(self):
        for case_id in p.CASES:
            for key,value in (("resource_id","other-resource"),
                              ("runner_id","other-runner"),
                              ("source_sha256","0"*64),
                              ("case_id","AZ-T00-00")):
                with self.subTest(case_id=case_id,key=key):
                    o,a=fixture(case_id)
                    o["metadata"][key]=value
                    self.assertEqual(p.assess(case_id,o,a)["result"],
                                     "DIFFERENCE_REVIEW_REQUIRED")

    def test_missing_approval_digest_and_stale_timestamp_fail_closed(self):
        for case_id in p.CASES:
            o,a=fixture(case_id)
            a["metadata"]["approval_record_sha256"]="not-a-hash"
            self.assertEqual(p.assess(case_id,o,a)["result"],"NOT_READY")
            o,a=fixture(case_id)
            o["metadata"]["observed_at_utc"]="2000-01-01T00:00:00+00:00"
            self.assertEqual(p.assess(case_id,o,a)["result"],"NOT_READY")

    def test_search_auth_and_expected_synthetic_results(self):
        cid="AZ-T35-13"
        for key,value in (("auth_method","api_key"),
                          ("http_status",401),
                          ("returned_synthetic_doc_ids",["unapproved-document"]),
                          ("private_route_observed",False)):
            o,a=fixture(cid)
            o["observation"][key]=value
            self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")

    def test_scm_deployment_binds_private_endpoint_digest_tls_and_commit(self):
        cid="AZ-T40-13"
        for key,value in (("scm_private_ip","8.8.8.8"),
                          ("artifact_sha256","0"*64),
                          ("source_commit_sha","f"*40),
                          ("tls_verified",False),
                          ("deployment_status","Failure")):
            o,a=fixture(cid)
            o["observation"][key]=value
            self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED",key)

    def test_indexer_cannot_claim_private_connection_to_wrong_source(self):
        cid="AZ-T41-11"
        for key,value in (("datasource_private_ip","10.22.0.5"),
                          ("datasource_resource_id","different-source"),
                          ("private_route_observed",False),
                          ("connection_status","Timeout")):
            o,a=fixture(cid)
            o["observation"][key]=value
            self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")

    def test_token_sanitization_requires_positive_control_and_actual_scan_count(self):
        cid="AZ-T42-17"
        for key,value in (("scanned_artifact_count",0),
                          ("positive_control_detections",0),
                          ("unredacted_token_findings",1)):
            o,a=fixture(cid)
            o["observation"]["artifact_scans"]["pipeline_logs"][key]=value
            self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["raw_token_logged"]=True
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")

    def test_cosmos_denial_must_bind_disallowed_identity_and_request(self):
        cid="AZ-T43-17"
        for key,value in (("unauthorized_principal_id","allowed-principal"),
                          ("result","Pass"),("http_status",200),
                          ("account_key_used",True),
                          ("request_id","other-request")):
            o,a=fixture(cid)
            o["observation"][key]=value
            self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED")

    def test_redaction_must_report_each_class_and_positive_controls(self):
        cid="AZ-T48-21"
        o,a=fixture(cid)
        del o["observation"]["redaction_controls"]["prompt"]
        self.assertEqual(p.assess(cid,o,a)["result"],"NOT_READY")
        o,a=fixture(cid)
        o["observation"]["redaction_controls"]["credentials"]["unredacted_marker_findings"]=1
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["redaction_controls"]["personal_data"]["synthetic_marker_count"]=0
        self.assertEqual(p.assess(cid,o,a)["result"],"NOT_READY")

    def test_app_private_dependencies_must_match_three_correct_pes(self):
        cid="AZ-T49-15"
        for key,value in (("resolved_private_ip","10.23.0.99"),
                          ("port",80),("tls_verified",False),
                          ("private_route_observed",False),
                          ("status","Timeout")):
            o,a=fixture(cid)
            o["observation"]["dependencies"]["cosmos"][key]=value
            self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED")
        o,a=fixture(cid)
        del o["observation"]["dependencies"]["search"]
        self.assertEqual(p.assess(cid,o,a)["result"],"NOT_READY")

    def test_acr_digest_runner_network_and_credentials_are_scoped(self):
        cid="AZ-T50-19"
        for key,value in (("image_digest","0"*64),
                          ("runner_source_ip","10.99.0.4"),
                          ("acr_private_ip","8.8.8.8"),
                          ("private_route_observed",False),
                          ("raw_registry_credential_logged",True),
                          ("pull_status","Failed")):
            o,a=fixture(cid)
            o["observation"][key]=value
            self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED")

    def test_flow_logs_require_distinct_ids_approved_pe_and_443(self):
        cid="AZ-T56-19"
        for field,value in (("destination_ip","8.8.8.8"),
                            ("destination_port",80),
                            ("source_ip","10.99.0.4"),
                            ("request_id","wrong-request")):
            o,a=fixture(cid)
            o["observation"]["observed_flows"][0][field]=value
            self.assertNotEqual(p.assess(cid,o,a)["result"],"REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["observed_flows"][1]["flow_log_id"]="flow-0"
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")

    def test_release_commit_binding_must_compare_plan_and_independent_reviewer(self):
        cid="AZ-T58-07"
        for field,value in (("plan_sha256","0"*64),
                            ("approved_commit_sha","f"*40),
                            ("plan_source_commit_sha","e"*40),
                            ("reviewer_id","executor-1")):
            o,a=fixture(cid)
            o["observation"][field]=value
            self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")
        o,a=fixture(cid)
        o["observation"]["source_commit_sha"]="malformed"
        self.assertEqual(p.assess(cid,o,a)["result"],"DIFFERENCE_REVIEW_REQUIRED")

    def test_unknown_or_bad_data_fail_closed(self):
        for cid in (*p.CASES,"AZ-T99-99"):
            self.assertEqual(p.assess(cid,None,None)["result"],"NOT_READY")

    def test_cli_all_matching_synthetic_input_exits_two_and_redacts_input(self):
        with tempfile.TemporaryDirectory() as d:
            o,a=fixture("AZ-T35-13")
            o["observation"]["extra_sensitive_value"]="SYNTHETIC_NEVER_PRINT"
            po,pa=Path(d)/"obs.json",Path(d)/"approved.json"
            po.write_text(json.dumps(o),encoding="utf-8")
            pa.write_text(json.dumps(a),encoding="utf-8")
            r=subprocess.run([sys.executable,
                              str(ROOT/"scripts/review_p1_source_evidence.py"),
                              "--case-id","AZ-T35-13","--observation",str(po),
                              "--approved",str(pa)],
                             cwd=ROOT,capture_output=True,text=True,check=False)
            self.assertEqual(r.returncode,2,r.stderr)
            out=json.loads(r.stdout)
            self.assertEqual(out["result"],"REVIEW_REQUIRED")
            self.assertEqual(out["release_decision"],"NO_GO")
            self.assertNotIn("SYNTHETIC_NEVER_PRINT",r.stdout)

    def test_missing_inputs_cli_exits_two(self):
        with tempfile.TemporaryDirectory() as d:
            filename=Path(d)/"absent.json"
            r=subprocess.run([sys.executable,
                              str(ROOT/"scripts/review_p1_source_evidence.py"),
                              "--case-id","AZ-T56-19","--observation",str(filename),
                              "--approved",str(filename)],
                             cwd=ROOT,capture_output=True,text=True,check=False)
            self.assertEqual(r.returncode,2)
            self.assertEqual(json.loads(r.stdout)["result"],"NOT_READY")


if __name__ == "__main__":
    unittest.main()
