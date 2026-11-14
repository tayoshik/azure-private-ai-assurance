import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("rest03_resource_audit", ROOT / "scripts/rest03_resource_audit.py")
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
SID = "01234567-89ab-4def-8123-0123456789ab"


def target(profile):
    typ = a.PROFILES[profile]
    namespace, name = typ.split("/")
    rid = f"/subscriptions/{SID}/resourceGroups/rg-synthetic/providers/{namespace}/{name}/sample"
    d = {"resource_id": rid, "profile": profile, "api_version": "2024-04-01"}
    if profile == "private_endpoint":
        d["expected_group_ids"] = ["sites"]
    return d


def good_data(profile):
    t = target(profile)
    d = {"id": t["resource_id"], "type": a.PROFILES[profile], "properties": {}}
    for path, expected in a.SCALAR_CHECKS.get(profile, []):
        dest = d
        parts = path.split(".")
        for k in parts[:-1]:
            dest = dest.setdefault(k, {})
        dest[parts[-1]] = expected
    if profile == "private_endpoint":
        d["properties"]["privateLinkServiceConnections"] = [{"properties": {
            "groupIds": ["sites"], "privateLinkServiceConnectionState": {"status": "Approved"}}}]
    if profile == "application_gateway":
        d["properties"]["frontendIPConfigurations"] = [{"properties": {
            "privateIPAddress": "10.1.2.3", "privateIPAllocationMethod": "Static"}}]
        d["properties"]["firewallPolicy"] = {"id": "/policy/synthetic"}
    return d


def observed(d):
    return {"state": "OBSERVED_NOT_ACCEPTED", "resource_id": d["id"],
            "observation": d, "evidence_sha256": a.digest(d)}


class REST03Tests(unittest.TestCase):
    def test_selftest(self):
        self.assertEqual(a.run_selftest()["status"], "PASS_OFFLINE_FIXTURES_ONLY")
    def test_all_seven_profiles_synthetic_good(self):
        for profile in a.PROFILES:
            with self.subTest(profile=profile):
                result = a.assess_observation(target(profile), observed(good_data(profile)), synthetic=True)
                self.assertEqual(result["status"], "PASS_OFFLINE_FIXTURE_ONLY")
                self.assertEqual(result["azure_live_acceptance"], "NOT_READY")
    def test_even_good_live_not_pass(self):
        result = a.assess_observation(target("web_app"), observed(good_data("web_app")))
        self.assertEqual(result["status"], "OBSERVED_PENDING_INDEPENDENT_REVIEW")
    def test_web_public_enabled_fails(self):
        d=good_data("web_app");d["properties"]["publicNetworkAccess"]="Enabled"
        self.assertEqual(a.assess_observation(target("web_app"),observed(d),synthetic=True)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")
    def test_missing_https_not_ready(self):
        d=good_data("web_app");d["properties"].pop("httpsOnly")
        self.assertEqual(a.assess_observation(target("web_app"),observed(d),synthetic=True)["status"],"NOT_READY")
    def test_boolean_not_interpreted_as_one(self):
        d=good_data("key_vault");d["properties"]["enablePurgeProtection"]=1
        self.assertEqual(a.assess_observation(target("key_vault"),observed(d),synthetic=True)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")
    def test_case_insensitive_enum(self):
        d=good_data("web_app");d["properties"]["publicNetworkAccess"]="dISableD"
        self.assertEqual(a.assess_observation(target("web_app"),observed(d),synthetic=True)["status"],"PASS_OFFLINE_FIXTURE_ONLY")
    def test_missing_auth_key_no_false_green(self):
        d=good_data("azure_openai");d["properties"].pop("disableLocalAuth")
        self.assertEqual(a.assess_observation(target("azure_openai"),observed(d),synthetic=True)["status"],"NOT_READY")
    def test_search_key_auth_enabled(self):
        d=good_data("ai_search");d["properties"]["disableLocalAuth"]=False
        self.assertEqual(a.assess_observation(target("ai_search"),observed(d),synthetic=True)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")
    def test_cosmos_public_enabled(self):
        d=good_data("cosmos_nosql");d["properties"]["publicNetworkAccess"]="Enabled"
        self.assertEqual(a.assess_observation(target("cosmos_nosql"),observed(d),synthetic=True)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")
    def test_vault_rbac_disabled(self):
        d=good_data("key_vault");d["properties"]["enableRbacAuthorization"]=False
        self.assertEqual(a.assess_observation(target("key_vault"),observed(d),synthetic=True)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")
    def test_private_endpoint_pending_connection(self):
        d=good_data("private_endpoint");d["properties"]["privateLinkServiceConnections"][0]["properties"]["privateLinkServiceConnectionState"]["status"]="Pending"
        self.assertEqual(a.assess_observation(target("private_endpoint"),observed(d),synthetic=True)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")
    def test_private_endpoint_wrong_group(self):
        d=good_data("private_endpoint");d["properties"]["privateLinkServiceConnections"][0]["properties"]["groupIds"]=["vault"]
        self.assertEqual(a.assess_observation(target("private_endpoint"),observed(d),synthetic=True)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")
    def test_private_endpoint_no_connections_not_ready(self):
        d=good_data("private_endpoint");d["properties"]["privateLinkServiceConnections"]=[]
        self.assertEqual(a.assess_observation(target("private_endpoint"),observed(d),synthetic=True)["status"],"NOT_READY")
    def test_private_endpoint_manual_connection(self):
        d=good_data("private_endpoint");d["properties"]["manualPrivateLinkServiceConnections"]=d["properties"].pop("privateLinkServiceConnections")
        self.assertEqual(a.assess_observation(target("private_endpoint"),observed(d),synthetic=True)["status"],"PASS_OFFLINE_FIXTURE_ONLY")
    def test_gateway_public_frontend(self):
        d=good_data("application_gateway");d["properties"]["frontendIPConfigurations"][0]["properties"]["publicIPAddress"]={"id":"/publicip/synthetic"}
        self.assertEqual(a.assess_observation(target("application_gateway"),observed(d),synthetic=True)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")
    def test_gateway_missing_frontend(self):
        d=good_data("application_gateway");d["properties"]["frontendIPConfigurations"]=[]
        self.assertEqual(a.assess_observation(target("application_gateway"),observed(d),synthetic=True)["status"],"NOT_READY")
    def test_gateway_dynamic_frontend(self):
        d=good_data("application_gateway");d["properties"]["frontendIPConfigurations"][0]["properties"]["privateIPAllocationMethod"]="Dynamic"
        self.assertEqual(a.assess_observation(target("application_gateway"),observed(d),synthetic=True)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")
    def test_gateway_missing_waf_not_ready(self):
        d=good_data("application_gateway");d["properties"].pop("firewallPolicy")
        self.assertEqual(a.assess_observation(target("application_gateway"),observed(d),synthetic=True)["status"],"NOT_READY")
    def test_wrong_resource_type(self):
        d=good_data("web_app");d["type"]="Microsoft.KeyVault/vaults"
        self.assertEqual(a.assess_observation(target("web_app"),observed(d),synthetic=True)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")
    def test_wrong_id_not_ready(self):
        d=good_data("web_app");d["id"]+="-wrong"
        self.assertEqual(a.assess_observation(target("web_app"),observed(d),synthetic=True)["status"],"NOT_READY")
    def test_invalid_target_rejected(self):
        for key,bad in [("api_version","latest"),("profile","anything"),("resource_id","/wrong")]:
            t=target("web_app");t[key]=bad
            with self.subTest(key=key),self.assertRaises(ValueError):a.validate_targets([t])
    def test_reject_nested_or_query_resource_id(self):
        for suffix in ("/providers/Microsoft.KeyVault/vaults/x", "?api-version=latest", "#fragment"):
            t=target("web_app");t["resource_id"]+=suffix
            with self.subTest(suffix=suffix),self.assertRaises(ValueError):a.validate_targets([t])
    def test_wrong_type_for_target_rejected(self):
        t=target("web_app");t["profile"]="key_vault"
        with self.assertRaises(ValueError):a.validate_targets([t])
    def test_pe_requires_exact_group(self):
        t=target("private_endpoint");t.pop("expected_group_ids")
        with self.assertRaises(ValueError):a.validate_targets([t])
    def test_duplicate_targets_rejected(self):
        t=target("web_app")
        with self.assertRaises(ValueError):a.validate_targets([t,t])
    def test_inventory_complete(self):
        t=target("web_app")
        data={"state":"OBSERVED_NOT_ACCEPTED","rows":[{"id":t["resource_id"],"type":a.PROFILES["web_app"]}],"complete_pages":True,"evidence_sha256":a.digest([{"id":t["resource_id"],"type":a.PROFILES["web_app"]}])}
        self.assertEqual(a.assess_inventory(data,[t])["status"],"OBSERVED_PENDING_INDEPENDENT_REVIEW")
    def test_inventory_missing(self):
        t=target("web_app")
        data={"state":"OBSERVED_NOT_ACCEPTED","rows":[],"complete_pages":True}
        self.assertEqual(a.assess_inventory(data,[t])["status"],"NOT_READY")
    def test_inventory_incomplete(self):
        t=target("web_app")
        data={"state":"OBSERVED_NOT_ACCEPTED","rows":[],"complete_pages":False}
        self.assertEqual(a.assess_inventory(data,[t])["status"],"NOT_READY")
    def test_inventory_duplicate(self):
        t=target("web_app");row={"id":t["resource_id"],"type":a.PROFILES["web_app"]}
        data={"state":"OBSERVED_NOT_ACCEPTED","rows":[row,row],"complete_pages":True,"evidence_sha256":a.digest([row,row])}
        self.assertEqual(a.assess_inventory(data,[t])["status"],"NOT_READY")
    def test_inventory_wrong_type(self):
        t=target("web_app");rows=[{"id":t["resource_id"],"type":a.PROFILES["key_vault"]}]
        data={"state":"OBSERVED_NOT_ACCEPTED","rows":rows,"complete_pages":True,"evidence_sha256":a.digest(rows)}
        self.assertEqual(a.assess_inventory(data,[t])["status"],"FAIL_POLICY_OBSERVED")
    def test_mocked_audit_one_target_no_live_pass(self):
        t=target("web_app");d=good_data("web_app")
        class FakeClient:
            def resource_graph_inventory(self,types):
                rows=[{"id":t["resource_id"],"type":a.PROFILES["web_app"]}]
                return {"state":"OBSERVED_NOT_ACCEPTED","rows":rows,"complete_pages":True,"evidence_sha256":a.digest(rows)}
            def get_resource(self,resource_id,api_version):
                assert resource_id==t["resource_id"] and api_version==t["api_version"]
                return observed(d)
        out=a.audit_client(FakeClient(),[t])
        self.assertEqual(out["status"],"OBSERVED_PENDING_INDEPENDENT_REVIEW")
        self.assertEqual(out["azure_live_passes"],0)
    def test_mocked_audit_notready_on_missing_scope(self):
        t=target("web_app")
        class FakeClient:
            def resource_graph_inventory(self,types):
                raise a.NotReadyError("Missing permission")
        self.assertEqual(a.audit_client(FakeClient(),[t])["status"],"NOT_READY")
    def test_observation_missing_or_bad_digest_not_ready(self):
        d=good_data("web_app")
        o=observed(d);o["evidence_sha256"]="0"*64
        self.assertEqual(a.assess_observation(target("web_app"),o)["status"],"NOT_READY")
        o.pop("evidence_sha256")
        self.assertEqual(a.assess_observation(target("web_app"),o)["status"],"NOT_READY")
    def test_inventory_bad_digest_not_ready(self):
        t=target("web_app");rows=[{"id":t["resource_id"],"type":a.PROFILES["web_app"]}]
        x={"state":"OBSERVED_NOT_ACCEPTED","rows":rows,"complete_pages":True,"evidence_sha256":"0"*64}
        self.assertEqual(a.assess_inventory(x,[t])["status"],"NOT_READY")
    def test_no_cloud_credential_dependency_for_selftest(self):
        result=subprocess.run([sys.executable,str(ROOT/"scripts/rest03_resource_audit.py"),"--selftest"],capture_output=True,text=True,check=False,env={})
        self.assertEqual(result.returncode,0)
        self.assertNotIn("token",result.stdout.lower())
    def test_cli_reject_unsafe_fixture(self):
        t=target("web_app");d=good_data("web_app");d["properties"]["publicNetworkAccess"]="Enabled"
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"fixture.json";p.write_text(json.dumps({"targets":[t],"observations":[observed(d)]}))
            result=subprocess.run([sys.executable,str(ROOT/"scripts/rest03_resource_audit.py"),"--fixture",str(p)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(json.loads(result.stdout)["status"],"FAIL_OFFLINE_POLICY_FIXTURE")

if __name__ == '__main__':unittest.main()
