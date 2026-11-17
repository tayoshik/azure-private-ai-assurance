"""Synthetic AZ-T29 regressions. No DNS, HTTP, token exchange or Azure calls."""
import base64
from contextlib import redirect_stdout
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
import io
import json
from pathlib import Path
import ssl
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import azure_entra_step29 as audit
from test_azure_gateway_step28 import fixture as gateway_fixture


GUID = "00000000-0000-0000-0000-000000000000"
GITHUB_SUBJECT = "repo:tayoshik/azure-private-ai-assurance:environment:synthetic"


def fixture():
    issuer = f"{audit.AUTHORITY}/{GUID}/v2.0"
    cfg = {"schema": "azure-entra-egress/az-t29/v1", "environment": "nonproduction", "topology": "dev",
           "approval_ref": "synthetic", "scope_ref": "synthetic", "approved_private_runner": True,
           "tenant_id": GUID, "cloud": "AzurePublic", "entra_issuer": issuer, "subscriptions": [GUID],
           "identity": {
               "app": {"issuer": issuer, "audience": "synthetic-app", "design_ref": "synthetic"},
               "managed": {"platform": "app_service", "audience": "synthetic-service", "client_id": GUID},
               "github": {"issuer": audit.GITHUB_ISSUER, "subject": GITHUB_SUBJECT,
                          "exchange_audience": audit.EXCHANGE_AUDIENCE, "resource_scope": audit.ARM_SCOPE,
                          "client_id": GUID}},
           "private_target": {"host": "health.example.invalid", "chain": ["health.example.invalid"],
                              "resolver_ip": "10.3.0.3", "ips": ["10.3.0.4"], "cidrs": ["10.3.0.0/24"],
                              "health_path": "/health", "health_status": 200}}
    cfg["dependencies"] = [
        {"category": kind, "actor": actor, "host": host, "port": port, "control": "firewall", "owner": "synthetic",
         "purpose": "synthetic", "approval_ref": "synthetic", "expires": (date.today() + timedelta(days=30)).isoformat()}
        for kind, actor, host, port in (
            ("entra", "app_browser", "login.microsoftonline.com", 443),
            ("entra", "github_runner", "login.microsoftonline.com", 443),
            ("monitor", "private_runner", "monitor.example.invalid", 443),
            ("certificate_validation", "gateway", "crl.example.invalid", 80),
        )]
    cfg["github_auth_probe"] = {"explicit_auth_approved": True, "auth_approval_ref": "synthetic",
                                "direct_https_approved": True,
                                "arm_read_id": f"/subscriptions/{GUID}/resourceGroups/synthetic/providers/Microsoft.Web/sites/sample"}
    return cfg


def policy(cfg):
    return {"complete": True, "scope_ref": cfg["scope_ref"], "collection_ref": "synthetic",
            "no_bypass_reviewed": True, "dns_view_reviewed": True, "default_unapproved_deny": True,
            "allows": deepcopy(cfg["dependencies"])}


def answer(*_):
    return [("health.example.invalid", "A", "10.3.0.4")]


def denied(cfg):
    moment = datetime.now(timezone.utc).isoformat()
    fixture_only_ip = "8.8.8.8"
    cfg["deny_evidence"] = {"source_ip": "10.3.0.4", "destination_ip": fixture_only_ip, "direction": "deny",
                            "approval_ref": "synthetic", "isolated_scope_approved": True,
                            "probe_ref": "synthetic", "observed_at": moment}
    return {"scope_ref": cfg["scope_ref"], "complete": True, "source_type": "firewall_flow",
            "review_ref": "synthetic", "collection_ref": "synthetic", "records": [
                {"source_ip": "10.3.0.4", "destination_ip": fixture_only_ip, "port": 443, "protocol": "TCP",
                 "decision": "Deny", "probe_ref": "synthetic", "observed_at": moment}]}


class Step29(unittest.TestCase):
    def setUp(self):
        self.cfg = audit.validate(fixture())

    def test_t29_02_missing_entra(self):
        exported = policy(self.cfg)
        audit.review_policy(self.cfg, exported, "entra")
        exported["allows"] = exported["allows"][1:]
        with self.assertRaisesRegex(audit.Mismatch, "missing"):
            audit.review_policy(self.cfg, exported, "entra")

    def test_t29_04_monitor_wildcard(self):
        exported = policy(self.cfg)
        audit.review_policy(self.cfg, exported, "monitor")
        exported["allows"][2]["host"] = "*.example.invalid"
        with self.assertRaisesRegex(audit.Mismatch, "wildcard"):
            audit.review_policy(self.cfg, exported, "monitor")

    def test_t29_06_dns_wrong_destination(self):
        audit.dns_observe(self.cfg, answer)
        with self.assertRaises(audit.Mismatch):
            audit.dns_observe(self.cfg, lambda *_: [("health.example.invalid", "A", "10.3.0.5")])

    def test_t29_08_certificate_inventory(self):
        exported = policy(self.cfg)
        audit.review_policy(self.cfg, exported, "certificate_validation")
        exported["allows"][-1]["port"] = 443
        with self.assertRaises(audit.Mismatch):
            audit.review_policy(self.cfg, exported, "certificate_validation")

    def network_fixture(self):
        design, _, subnet, nsg = gateway_fixture()
        self.cfg["network"] = {**design, "paas_pe_cidrs": ["10.28.0.0/24"]}
        client = Mock()
        client.get_resource.side_effect = lambda rid, _: {"observation":
            {design["subnet_id"]: subnet, design["nsg_id"]: nsg}[rid]}
        return client, subnet, nsg

    def test_t29_10_nsg_overbroad(self):
        client, _, nsg = self.network_fixture()
        self.assertEqual(audit.read_arm(self.cfg, client)[9][0], "CONFIG_OBSERVED_NOT_ACCEPTED")
        nsg["properties"]["securityRules"][3]["properties"]["destinationAddressPrefix"] = "*"
        self.assertEqual(audit.read_arm(self.cfg, client)[9][0], "FAIL")

    def test_t29_12_effective_hop(self):
        self.cfg["effective_next_hop"] = {"source_ip": "10.3.0.4", "destination_ip": "10.4.0.4",
                                          "hop_ip": "10.5.0.4", "hop_type": "VirtualAppliance"}
        doc = {**self.cfg["effective_next_hop"], "scope_ref": "synthetic", "complete": True, "collection_ref": "synthetic"}
        audit.review_next_hop(self.cfg, doc)
        doc["hop_ip"] = "10.5.0.5"
        with self.assertRaises(audit.Mismatch):
            audit.review_next_hop(self.cfg, doc)

    def test_t29_14_route_attachment(self):
        client, subnet, _ = self.network_fixture()
        self.assertEqual(audit.read_arm(self.cfg, client)[13][0], "CONFIG_OBSERVED_NOT_ACCEPTED")
        subnet["properties"]["routeTable"] = {"id": self.cfg["network"]["nsg_id"]}
        self.assertEqual(audit.read_arm(self.cfg, client)[13][0], "FAIL")

    def test_t29_16_denial_requires_actual_logged_decision(self):
        doc = denied(self.cfg)
        audit.review_denied(self.cfg, doc)
        doc["records"][0]["decision"] = "Allow"
        with self.assertRaises(audit.Mismatch):
            audit.review_denied(self.cfg, doc)

    def test_t29_18_missing_ownership(self):
        exported = policy(self.cfg)
        audit.review_policy(self.cfg, exported)
        self.cfg["dependencies"][0]["owner"] = ""
        with self.assertRaisesRegex(ValueError, "ownership"):
            audit.validate(self.cfg)

    def test_t29_20_https_and_tls(self):
        conn = Mock()
        conn.return_value.getresponse.return_value.status = 200
        audit.health_observe(self.cfg, answer, conn)
        conn.assert_called_once_with("health.example.invalid", "10.3.0.4")
        conn.return_value.getresponse.return_value.status = 302
        with self.assertRaises(audit.Mismatch):
            audit.health_observe(self.cfg, answer, conn)
        conn.return_value.request.side_effect = ssl.SSLError("private backend fixture")
        self.assertEqual(audit.observed(lambda: audit.health_observe(self.cfg, answer, conn))[0], "NOT_READY")

    def test_t29_22_activity_logs_cannot_substitute_flow(self):
        doc = denied(self.cfg)
        audit.review_denied(self.cfg, doc)
        doc["source_type"] = "arm_activity"
        with self.assertRaisesRegex(audit.NotReadyError, "Flow"):
            audit.review_denied(self.cfg, doc)

    def test_wrong_cloud_tenant_audience(self):
        cfg = fixture()
        cfg["cloud"] = "AzureUSGovernment"
        with self.assertRaisesRegex(ValueError, "AzurePublic"):
            audit.validate(cfg)
        cfg = fixture()
        cfg["tenant_id"] = "11111111-1111-1111-1111-111111111111"
        with self.assertRaisesRegex(ValueError, "tenant"):
            audit.validate(cfg)
        cfg = fixture()
        cfg["identity"]["github"]["exchange_audience"] = audit.ARM_HOST
        with self.assertRaisesRegex(ValueError, "audience"):
            audit.validate(cfg)

    def test_oidc_phases_are_distinct_and_fail_closed(self):
        route, credential, client = Mock(), Mock(), Mock()
        credential.return_value.get_token.return_value.token = "secret-fixture-token"
        client.return_value.get_resource.side_effect = audit.NotReadyError("403 secret-fixture-token")
        stages = audit.auth_probe(self.cfg, transport=route, credential=credential, client_factory=client)
        self.assertEqual(tuple(stages.values()), ("OBSERVED_NOT_ACCEPTED", "OBSERVED_NOT_ACCEPTED", "NOT_READY"))
        self.assertNotIn("secret-fixture-token", str(stages))
        credential.return_value.get_token.side_effect = RuntimeError("secret-fixture-token")
        client.reset_mock()
        stages = audit.auth_probe(self.cfg, transport=route, credential=credential, client_factory=client)
        self.assertEqual(tuple(stages.values()), ("OBSERVED_NOT_ACCEPTED", "NOT_READY", "NOT_READY"))
        client.assert_not_called()
        credential.reset_mock()
        route.side_effect = ssl.SSLError("secret-fixture-token")
        self.assertTrue(all(v == "NOT_READY" for v in audit.auth_probe(
            self.cfg, transport=route, credential=credential, client_factory=client).values()))
        credential.assert_not_called()

    def test_assertion_prefilter_uses_exact_issuer_subject_and_exchange_audience(self):
        approved = self.cfg["identity"]["github"]
        valid = {"iss": approved["issuer"], "sub": approved["subject"], "aud": approved["exchange_audience"]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture"
            def put(claims):
                payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=")
                path.write_bytes(b"synthetic." + payload + b".unsignedfixture")
            put(valid)
            self.assertTrue(audit.checked_assertion(path, approved))
            for key in ("iss", "sub", "aud"):
                put({**valid, key: "wrong-fixture"})
                with self.assertRaisesRegex(audit.NotReadyError, "issuer, subject or exchange audience"):
                    audit.checked_assertion(path, approved)

    def test_auth_review_app_and_managed_are_not_github_exchange(self):
        for actor in ("app", "managed"):
            identity = self.cfg["identity"][actor]
            extract = {**identity, "flow": actor, "scope_ref": "synthetic", "collector_ref": "synthetic",
                       "tenant_id": GUID, "cloud": "AzurePublic", "target_audience": identity["audience"],
                       "transport": "observed", "token_acquisition": "observed", "target_authorization": "denied"}
            self.assertEqual(audit.review_auth(self.cfg, extract)["target_authorization"], "NOT_READY")

    def test_permission_incomplete_and_dns_timeout(self):
        client, _, nsg = self.network_fixture()
        nsg["nextLink"] = "https://incomplete.invalid"
        self.assertEqual(audit.read_arm(self.cfg, client)[9][0], "NOT_READY")
        client.get_resource.side_effect = audit.NotReadyError("protected host and 403")
        self.assertEqual(audit.read_arm(self.cfg, client)[13][0], "NOT_READY")
        dns = Mock(side_effect=audit.NotReadyError("DNS query timed out"))
        self.assertEqual(audit.observed(lambda: audit.dns_observe(self.cfg, dns))[0], "NOT_READY")

    def test_default_and_configuration_never_call_live_code(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            root = Path(directory)
            config = root / "cfg.json"
            config.write_text(json.dumps(self.cfg))
            with patch.object(audit, "client_for") as arm, patch.object(audit, "auth_probe") as token:
                self.assertEqual(audit.main(["--out", str(root / "none")]), 2)
                self.assertEqual(audit.main(["--check-config", "--config", str(config), "--out", str(root / "cfg")]), 0)
                arm.assert_not_called()
                token.assert_not_called()
            for path in (root / "cfg").iterdir():
                self.assertNotIn("health.example.invalid", path.read_text())
                self.assertNotIn("10.3.0.", path.read_text())


def write_synthetic(path):
    results = {}
    for case in range(2, 23, 2):
        method = next(name for name in dir(Step29) if name.startswith(f"test_t29_{case:02}_"))
        result = unittest.TestResult()
        Step29(method).run(result)
        results[case] = (("MATCHED_OFFLINE", "positive and negative fixtures checked") if result.wasSuccessful()
                         else ("FAIL", "paired fixture regression"))
    audit.reports(results, "synthetic", path, step=29, kinds=audit.KINDS)
    return int(any(state == "FAIL" for state, _ in results.values()))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--evidence":
        raise SystemExit(write_synthetic(Path(sys.argv[2])))
    unittest.main()
