"""Synthetic tests for the Azure Monitor Private Link observer."""
import contextlib
import io
from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import azure_monitor_private_audit as audit

GUID = "00000000-0000-0000-0000-000000000000"
BASE = f"/subscriptions/{GUID}/resourceGroups/synthetic/providers"
SCOPE = f"{BASE}/Microsoft.Insights/privateLinkScopes/scope"
WORKSPACE = f"{BASE}/Microsoft.OperationalInsights/workspaces/workspace"
ENDPOINT = f"{BASE}/Microsoft.Network/privateEndpoints/pe"


def configuration():
    return {
        "approved_private_runner": True,
        "environment": "nonproduction",
        "mode": "dev",
        "topology_approval_ref": "synthetic",
        "query_approval_ref": "synthetic",
        "log_source_approval_ref": "synthetic",
        "subscriptions": [GUID],
        "tenant_id": GUID,
        "client_id": GUID,
        "workspace_guid": GUID,
        "transaction_guid": GUID,
        "scope_id": SCOPE,
        "workspace_id": WORKSPACE,
        "association_id": SCOPE + "/scopedResources/workspace",
        "endpoint_id": ENDPOINT,
        "zone_group_id": ENDPOINT + "/privateDnsZoneGroups/monitor",
        "gateway_id": f"{BASE}/Microsoft.Network/applicationGateways/gateway",
        "zone_ids": {z: f"{BASE}/Microsoft.Network/privateDnsZones/{z}" for z in audit.ZONES},
        "endpoint_ips": ["10.10.10.10"],
    }


def observations(cfg):
    return {
        SCOPE: {"accessModeSettings": {"queryAccessMode": "PrivateOnly", "ingestionAccessMode": "PrivateOnly"}},
        WORKSPACE: {"customerId": GUID, "publicNetworkAccessForIngestion": "Disabled",
                    "publicNetworkAccessForQuery": "Disabled"},
        cfg["association_id"]: {"linkedResourceId": WORKSPACE},
        ENDPOINT: {"manualPrivateLinkServiceConnections": [{"properties": {
            "privateLinkServiceId": SCOPE, "groupIds": ["azuremonitor"],
            "privateLinkServiceConnectionState": {"status": "Approved"},
        }}]},
        cfg["zone_group_id"]: {"privateDnsZoneConfigs": [
            {"properties": {"privateDnsZoneId": z}} for z in cfg["zone_ids"].values()
        ]},
    }


class MonitorAuditTests(unittest.TestCase):
    def setUp(self):
        self.cfg = audit.read_config(configuration())
        self.arm_data = observations(self.cfg)
        self.arm = Mock()
        self.arm.get_resource.side_effect = lambda rid, api: {
            "observation": {"properties": self.arm_data[rid]},
        }
        self.outcome = {}

    def test_default_does_not_contact_azure(self):
        out = io.StringIO()
        with patch.object(audit, "run_live") as live, contextlib.redirect_stdout(out):
            self.assertEqual(audit.main([]), 2)
        live.assert_not_called()
        report = json.loads(out.getvalue())
        self.assertEqual(report["status"], "NOT_READY")
        self.assertEqual(report["azure_live_passes"], 0)

    def test_missing_approval_is_not_ready(self):
        for approval in ("topology_approval_ref", "query_approval_ref", "log_source_approval_ref"):
            with self.subTest(approval=approval):
                cfg = configuration()
                del cfg[approval]
                with self.assertRaisesRegex(audit.NotReadyError, approval):
                    audit.read_config(cfg)

    def test_rejects_foreign_subscription_and_path_aliases(self):
        for uri in (WORKSPACE.replace(GUID, "11111111-1111-1111-1111-111111111111"),
                    WORKSPACE.replace("/synthetic/", "/../")):
            with self.subTest(uri=uri):
                cfg = configuration()
                cfg["workspace_id"] = uri
                with self.assertRaisesRegex(audit.NotReadyError, "resource ID"):
                    audit.read_config(cfg)

    def test_scope_observation_never_becomes_acceptance(self):
        audit.audit_arm(self.arm, self.cfg, self.outcome)
        self.assertEqual(self.outcome, {f"AZ-T31-{n:02}": "OBSERVED_NOT_ACCEPTED" for n in (3, 9, 11)})

    def test_rejects_open_scope_or_exclusion(self):
        modes = self.arm_data[SCOPE]["accessModeSettings"]
        modes["exclusions"] = [{"queryAccessMode": "Open"}]
        with self.assertRaisesRegex(audit.NotReadyError, "PrivateOnly"):
            audit.audit_arm(self.arm, self.cfg, self.outcome)

    def test_rejects_public_workspace(self):
        self.arm_data[WORKSPACE]["publicNetworkAccessForQuery"] = "Enabled"
        with self.assertRaisesRegex(audit.NotReadyError, "public network flags"):
            audit.audit_arm(self.arm, self.cfg, self.outcome)

    def test_rejects_wrong_associated_workspace(self):
        self.arm_data[self.cfg["association_id"]]["linkedResourceId"] = WORKSPACE + "2"
        with self.assertRaisesRegex(audit.NotReadyError, "wrong workspace"):
            audit.audit_arm(self.arm, self.cfg, self.outcome)

    def test_rejects_pending_endpoint(self):
        conn = self.arm_data[ENDPOINT]["manualPrivateLinkServiceConnections"][0]["properties"]
        conn["privateLinkServiceConnectionState"]["status"] = "Pending"
        with self.assertRaisesRegex(audit.NotReadyError, "approval is pending"):
            audit.audit_arm(self.arm, self.cfg, self.outcome)

    def test_rejects_wrong_subresource(self):
        conn = self.arm_data[ENDPOINT]["manualPrivateLinkServiceConnections"][0]["properties"]
        conn["groupIds"] = ["blob"]
        with self.assertRaisesRegex(audit.NotReadyError, "expected one PE connection"):
            audit.audit_arm(self.arm, self.cfg, self.outcome)

    def test_rejects_incomplete_dns_zone_group(self):
        self.arm_data[self.cfg["zone_group_id"]]["privateDnsZoneConfigs"].pop()
        with self.assertRaisesRegex(audit.NotReadyError, "DNS zone group"):
            audit.audit_arm(self.arm, self.cfg, self.outcome)

    def test_rejects_unapproved_dns_answers(self):
        resolver = Mock(return_value=[(0, 0, 0, "", ("10.10.10.10",)), (0, 0, 0, "", ("8.8.8.8",))])
        with self.assertRaisesRegex(audit.NotReadyError, "Monitor DNS"):
            audit.resolve_private(audit.QUERY_HOST, self.cfg["endpoint_ips"], resolver)
        resolver.return_value.pop()
        self.assertEqual(audit.resolve_private(audit.QUERY_HOST, self.cfg["endpoint_ips"], resolver), ["10.10.10.10"])

    def test_transport_binds_ip_and_validates_canonical_host(self):
        with patch.object(audit.ssl, "create_default_context") as policy, patch.object(
                audit.socket, "create_connection") as connect:
            client = audit.PrivateHTTPSConnection(audit.QUERY_HOST, "10.10.10.10")
            client.connect()
            connect.assert_called_once_with(("10.10.10.10", 443), timeout=8)
            policy.return_value.wrap_socket.assert_called_once_with(
                connect.return_value.__enter__.return_value.dup.return_value, server_hostname=audit.QUERY_HOST)

    def test_missing_oidc_is_not_ready(self):
        with patch.dict(audit.os.environ, {}, clear=True):
            with self.assertRaisesRegex(audit.NotReadyError, "OIDC identity"):
                audit.credential_for(self.cfg)

    def test_query_checks_only_fixed_table_gateway_and_transaction(self):
        conn = Mock()
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.read.return_value = b'{"tables":[{"rows":[[1]]}]}'
        self.assertEqual(audit.read_log_count(conn, self.cfg, "synthetic"), 1)
        method, path, payload, _ = conn.request.call_args.args
        self.assertEqual((method, path), ("POST", f"/v1/workspaces/{GUID}/query"))
        self.assertIn("AGWAccessLogs", json.loads(payload)["query"])
        self.assertIn(self.cfg["gateway_id"].lower(), json.loads(payload)["query"])
        self.assertIn(GUID.replace("-", ""), json.loads(payload)["query"])

    def test_partial_query_response_is_rejected(self):
        conn = Mock()
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.read.return_value = b'{"error":{},"tables":[{"rows":[[1]]}]}'
        with self.assertRaisesRegex(audit.NotReadyError, "incomplete or partial"):
            audit.read_log_count(conn, self.cfg, "synthetic")

    def test_log_arrival_is_bounded_and_never_inferred(self):
        with patch.object(audit, "PrivateHTTPSConnection"), patch.object(audit, "read_log_count", return_value=0) as count:
            with self.assertRaisesRegex(audit.NotReadyError, "did not arrive"):
                audit.await_log(self.cfg, "10.10.10.10", "synthetic", attempts=2, sleeper=lambda _: None)
            self.assertEqual(count.call_count, 2)

    def test_supporting_control_evidence_only(self):
        data = {
            "as_of": "2026-11-17",
            "workspace_id": WORKSPACE,
            "app_insights": {"workspace_id": WORKSPACE},
            "query_role": {"scope_id": WORKSPACE, "principal_id": GUID,
                           "approved_principal_id": GUID, "role_guid": GUID, "approved_role_guid": GUID},
            "public_exceptions": [{"owner": "synthetic", "purpose": "ARM", "scope": "ARM only",
                                   "expires": "2026-11-18"}],
            "absence_alert": {"workspace_id": WORKSPACE, "enabled": True, "checks_absence": True,
                              "action_group_id": "synthetic", "approved_action_group_id": "synthetic"},
        }
        self.assertEqual(set(audit.review_supporting_controls(data).values()), {"MATCHED_OFFLINE"})
        data["app_insights"]["workspace_id"] = "wrong"
        data["query_role"]["scope_id"] = "wrong"
        data["public_exceptions"][0]["expires"] = "2026-11-17"
        data["absence_alert"]["action_group_id"] = "wrong"
        self.assertEqual(set(audit.review_supporting_controls(data).values()), {"MISMATCH_OFFLINE"})

    def test_missing_supporting_observations_remain_not_ready(self):
        report = audit.review_supporting_controls({"as_of": "2026-11-17", "workspace_id": WORKSPACE})
        self.assertEqual(set(report.values()), {"NOT_READY"})

    def test_check_config_uses_no_azure_for_dev_and_hub(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "input.json"
            for mode in ("dev", "hub"):
                cfg = configuration()
                cfg["mode"] = mode
                manifest.write_text(json.dumps(cfg))
                out = io.StringIO()
                with patch.object(audit, "run_live") as live, contextlib.redirect_stdout(out):
                    self.assertEqual(audit.main(["--check-config", "--config", str(manifest)]), 0)
                live.assert_not_called()
                self.assertEqual(json.loads(out.getvalue())["status"], "CONFIG_SHAPE_VALID_NO_AZURE")

    def test_optional_checks_observe_only_target_configuration(self):
        cfg = configuration()
        component = BASE + "/Microsoft.Insights/components/app"
        rule = BASE + "/Microsoft.Insights/scheduledQueryRules/absence"
        group = BASE + "/Microsoft.Insights/actionGroups/owner"
        criteria = {"allOf": [{"query": "approved synthetic criterion"}]}
        cfg["optional_observations"] = {
            "app_insights_id": component,
            "query_role": {"assignment_guid": GUID, "principal_id": GUID, "definition_guid": GUID},
            "absence_alert": {"rule_id": rule, "action_group_id": group,
                              "criteria_sha256": sha256(json.dumps(criteria, sort_keys=True, separators=(",", ":")).encode()).hexdigest()},
        }
        cfg = audit.read_config(cfg)
        assignment = cfg["optional_observations"]["query_role"]["assignment_id"]
        self.arm_data.update({
            component: {"WorkspaceResourceId": WORKSPACE},
            assignment: {"scope": WORKSPACE, "principalId": GUID,
                         "roleDefinitionId": f"{BASE}/Microsoft.Authorization/roleDefinitions/{GUID}"},
            rule: {"enabled": True, "criteria": criteria, "scopes": [WORKSPACE],
                   "actions": {"actionGroups": [group]}},
            group: {"enabled": True},
        })
        self.assertEqual(audit.optional_arm_checks(self.arm, cfg, self.outcome), {})
        self.assertEqual(self.outcome, {f"AZ-T31-{i:02}": "CONFIG_OBSERVED_NOT_ACCEPTED" for i in (7, 17, 21)})
        self.arm_data[component]["WorkspaceResourceId"] = WORKSPACE + "-other"
        self.arm_data[assignment]["condition"] = "unexpected"
        self.arm_data[group]["enabled"] = False
        self.outcome.clear()
        self.assertEqual(set(audit.optional_arm_checks(self.arm, cfg, self.outcome)),
                         {"AZ-T31-07", "AZ-T31-17", "AZ-T31-21"})
        self.assertEqual(self.outcome, {})
