"""Synthetic AZ-T28 coverage. Every ARM and socket observation is mocked."""
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import azure_gateway_step28 as audit


def rule(priority=100, direction="Inbound", access="Allow", protocol="Tcp", source="10.25.0.0/24",
         destination="*", ports="443"):
    return {"properties": {"priority": priority, "direction": direction, "access": access,
                           "protocol": protocol, "sourceAddressPrefix": source, "destinationAddressPrefix": destination,
                           "sourcePortRange": "*", "destinationPortRange": ports}}


def fixture():
    sid = "00000000-0000-0000-0000-000000000000"
    base = f"/subscriptions/{sid}/resourceGroups/synthetic/providers/Microsoft.Network"
    vnet, gateway, nsg = (base + path for path in ("/virtualNetworks/v", "/applicationGateways/g", "/networkSecurityGroups/n"))
    subnet = vnet + "/subnets/gateway"
    frontend = gateway + "/frontendIPConfigurations/frontend"
    port = gateway + "/frontendPorts/https"
    cfg = {"schema": "azure-private-gateway/az-t28/v1", "environment": "nonproduction", "topology": "dev",
           "approved_private_runner": True, "approval_ref": "synthetic", "network_isolation_review_ref": "synthetic",
           "egress_review_ref": "synthetic", "profile": "private_waf_v2_network_isolation", "subscriptions": [sid],
           "gateway_id": gateway, "vnet_id": vnet, "subnet_id": subnet, "nsg_id": nsg, "route_table_id": None,
           "expected_routes": [], "cidrs": ["10.24.0.0/24"], "frontend_ip": "10.24.0.10",
           "client_cidrs": ["10.25.0.0/24"], "deny_test_cidrs": ["10.26.0.0/24"],
           "approved_priorities": {"Inbound": [100, 110, 4090], "Outbound": [100, 4090]},
           "egress": [{"protocol": "tcp", "port": 443, "destinations": ["10.28.0.0/24"], "purpose": "synthetic"}]}
    gw = {"properties": {"provisioningState": "Succeeded", "operationalState": "Running",
                         "sku": {"name": "WAF_v2", "tier": "WAF_v2"},
                         "gatewayIPConfigurations": [{"properties": {"subnet": {"id": subnet}}}],
                         "frontendIPConfigurations": [{"id": frontend, "properties": {
                             "subnet": {"id": subnet}, "privateIPAllocationMethod": "Static", "privateIPAddress": "10.24.0.10"}}],
                         "frontendPorts": [{"id": port, "properties": {"port": 443}}],
                         "httpListeners": [{"properties": {"protocol": "Https", "frontendPort": {"id": port},
                                                          "frontendIPConfiguration": {"id": frontend}}}]}}
    sn = {"properties": {"provisioningState": "Succeeded", "addressPrefix": "10.24.0.0/24",
                         "networkSecurityGroup": {"id": nsg}, "delegations": [
                             {"properties": {"serviceName": "Microsoft.Network/applicationGateways"}}],
                         "applicationGatewayIPConfigurations": [{"id": gateway + "/gatewayIPConfigurations/config"}]}}
    rules = [
        rule(), rule(priority=110, protocol="*", source="AzureLoadBalancer", ports="*"),
        rule(priority=4090, access="Deny", protocol="*", source="*", ports="*"),
        rule(direction="Outbound", source="*", destination="10.28.0.0/24"),
        rule(priority=4090, direction="Outbound", access="Deny", protocol="*", source="*", ports="*")
    ]
    defaults = []
    for direction, names in audit.DEFAULT.items():
        for name, priority in names.items():
            deny = name.startswith("deny")
            src = "AzureLoadBalancer" if "loadbalancer" in name else "VirtualNetwork" if "vnet" in name else "*"
            defaults.append({**rule(priority, direction, "Deny" if deny else "Allow", "*", src,
                                    "Internet" if "internet" in name else "*", "*"), "name": name})
    ns = {"properties": {"provisioningState": "Succeeded", "securityRules": rules, "defaultSecurityRules": defaults}}
    return cfg, gw, sn, ns


class Gateway28(unittest.TestCase):
    def setUp(self):
        self.cfg, self.gateway, self.subnet, self.nsg = fixture()
        self.rules = self.nsg["properties"]["securityRules"]

    def results(self):
        return audit.policy_results(audit.validate(self.cfg), self.gateway, self.subnet, self.nsg, None)

    def pair(self, case, mutate):
        self.assertEqual(self.results()[case][0], "CONFIG_OBSERVED_NOT_ACCEPTED")
        mutate()
        self.assertIn(self.results()[case][0], ("FAIL", "NOT_READY"))

    def test_t28_02_shadowed_client(self):
        def shadow():
            self.rules[0]["properties"]["priority"] = 105
            self.rules.append(rule(priority=100, access="Deny", source="10.25.0.0/25"))

        self.pair(1, shadow)

    def test_t28_04_cidr(self):
        self.pair(3, lambda: self.rules[0]["properties"].update(sourceAddressPrefix="10.0.0.0/8"))

    def test_t28_06_lb_priority(self):
        self.pair(5, lambda: self.rules.append(rule(priority=102, access="Deny", source="168.63.129.16", ports="443")))

    def test_t28_08_isolation(self):
        source = {"topology_ref": "synthetic", "sku": "WAF_v2", "network_isolation": True,
                  "gateway_manager_required": False}
        audit.review_policy(self.cfg, source)
        source["gateway_manager_required"] = True
        with self.assertRaises(audit.NotReadyError):
            audit.review_policy(self.cfg, source)

    def test_t28_10_egress(self):
        self.pair(9, lambda: self.rules[3]["properties"].update(destinationAddressPrefix="*"))

    def test_t28_12_default_precedence(self):
        self.pair(11, lambda: self.rules.pop(2))

    def test_t28_14_duplicate_priorities(self):
        self.pair(13, lambda: self.rules[1]["properties"].update(priority=100))

    def test_t28_16_gateway_health(self):
        self.pair(15, lambda: self.gateway["properties"].update(operationalState="Stopped"))

    def test_t28_18_backend(self):
        rg = self.cfg["gateway_id"]
        self.cfg["backend"] = {"pool_id": rg + "/backendAddressPools/p", "settings_id": rg + "/backendHttpSettingsCollection/s",
                               "address": "synthetic.invalid", "hostname": "synthetic.invalid"}
        doc = {**self.cfg["backend"], "gateway_id": rg, "scope_complete": True, "health": "Healthy",
               "configured_hostname": "synthetic.invalid", "configured_sni": "synthetic.invalid"}
        audit.review_backend(self.cfg, doc)
        doc["configured_sni"] = "wrong.invalid"
        with self.assertRaises(audit.Mismatch):
            audit.review_backend(self.cfg, doc)

    def test_t28_20_approved_boundary(self):
        doc = {"topology_ref": "synthetic", "sku": "WAF_v2", "network_isolation": True, "gateway_manager_required": False,
               "change_controls": {"no_production_nsg_mutations": True, "nonproduction_boundary_approved": True,
                                   "approval_ref": "synthetic"}}
        audit.review_policy(self.cfg, doc)
        doc["change_controls"]["no_production_nsg_mutations"] = False
        with self.assertRaises(audit.NotReadyError):
            audit.review_policy(self.cfg, doc)

    def test_t28_22_activity_ticket(self):
        start = datetime.now(timezone.utc)
        end = start + timedelta(minutes=5)
        ticket = {"event_id": "synthetic", "actor_ref": "approved", "operation": "synthetic_write", "ticket_ref": "ticket"}
        self.cfg["changes"] = {"start": start.isoformat(), "end": end.isoformat(), "tickets": [ticket]}
        doc = {"start": start.isoformat(), "end": end.isoformat(), "collection_complete": True, "review_ref": "synthetic",
               "events": [{**ticket, "observed_at": start.isoformat(), "status": "Succeeded", "resource_id": self.cfg["nsg_id"]}]}
        audit.review_changes(self.cfg, doc)
        doc["events"][0]["actor_ref"] = "wrong"
        with self.assertRaises(audit.Mismatch):
            audit.review_changes(self.cfg, doc)

    def test_unknown_asg_and_service_tag_are_not_assumed_disjoint(self):
        for source in ({"sourceApplicationSecurityGroups": [{"id": "synthetic"}]}, {"sourceAddressPrefix": "SomeTag"}):
            before = rule(priority=101, access="Deny")
            before["properties"].pop("sourceAddressPrefix")
            before["properties"].update(source)
            self.rules[0]["properties"]["priority"] = 105
            self.rules.append(before)
            self.assertEqual(self.results()[1][0], "NOT_READY")
            self.rules.pop()

    def test_missing_default_inventory_and_paged_nsg(self):
        self.nsg["properties"]["defaultSecurityRules"].pop()
        self.assertEqual(self.results()[1][0], "NOT_READY")
        self.nsg["nextLink"] = "https://incomplete.invalid"
        self.assertEqual(self.results()[13][0], "NOT_READY")

    def test_subnet_missing_association_and_wrong_vnet(self):
        self.subnet["properties"].pop("networkSecurityGroup")
        self.assertEqual(self.results()[9][0], "FAIL")
        self.cfg["vnet_id"] += "-other"
        with self.assertRaisesRegex(ValueError, "approved VNet"):
            audit.validate(self.cfg)

    def test_port_direction_and_source_port(self):
        for field, value in (("destinationPortRange", "80"), ("direction", "Outbound"), ("sourcePortRange", "2000-2999")):
            with patch.dict(self.rules[0]["properties"], {field: value}):
                self.assertEqual(self.results()[1][0], "FAIL")

    def test_route_table_association_and_default_route_are_checked_as_config_only(self):
        route_id = self.cfg["nsg_id"].replace("networkSecurityGroups", "routeTables")
        self.cfg.update(route_table_id=route_id, expected_routes=[
            {"prefix": "0.0.0.0/0", "next_hop_type": "VirtualAppliance", "next_hop_ip": "10.24.2.4"}])
        self.subnet["properties"]["routeTable"] = {"id": route_id}
        props = {"addressPrefix": "0.0.0.0/0", "nextHopType": "VirtualAppliance",
                 "nextHopIpAddress": "10.24.2.4", "provisioningState": "Succeeded"}
        route = {"properties": {"provisioningState": "Succeeded", "routes": [{"properties": props}]}}
        cfg = audit.validate(self.cfg)
        state, reason = audit.policy_results(cfg, self.gateway, self.subnet, self.nsg, route)[9]
        self.assertEqual(state, "CONFIG_OBSERVED_NOT_ACCEPTED")
        self.assertIn("effective route", reason)
        props["nextHopIpAddress"] = "10.24.2.7"
        self.assertEqual(audit.policy_results(cfg, self.gateway, self.subnet, self.nsg, route)[9][0], "FAIL")

    def test_permission_is_not_nonexistence(self):
        client = Mock()
        client.get_resource.side_effect = audit.NotReadyError("403")
        self.assertTrue(all(state == "NOT_READY" for state, _ in audit.observe_arm(self.cfg, client).values()))

    def test_output_and_denied_tcp_timeout(self):
        self.cfg["probe"] = {"approval_ref": "synthetic", "vantage_approved": True, "isolated_deny_approved": True,
                             "direction": "deny", "source_ip": "10.26.0.20", "runner_cidr": "10.26.0.0/24",
                             "destination_ip": "10.24.0.10"}
        client = Mock()
        client.get_resource.side_effect = [{"observation": self.gateway}, {"observation": self.subnet}]
        wire = Mock(side_effect=TimeoutError())
        self.assertEqual(audit.probe(self.cfg, client, wire)[0], "NOT_READY")
        wire.assert_called_once_with(("10.24.0.10", 443), timeout=3, source_address=("10.26.0.20", 0))
        with tempfile.TemporaryDirectory() as folder, redirect_stdout(io.StringIO()):
            out = Path(folder) / "unexecuted"
            with patch.object(audit, "client_for") as auth:
                self.assertEqual(audit.main(["--out", str(out)]), 2)
            auth.assert_not_called()
            evidence = (out / "results.json").read_text()
            self.assertEqual(len(json.loads(evidence)["results"]), 22)
            self.assertNotIn("10.24.", evidence)
            self.assertNotIn("rg-synthetic", (out / "junit.xml").read_text())


def write_synthetic(path):
    results = {}
    for case in range(2, 23, 2):
        test = next(name for name in dir(Gateway28) if name.startswith(f"test_t28_{case:02}_"))
        outcome = unittest.TestResult()
        Gateway28(test).run(outcome)
        results[case] = (("MATCHED_OFFLINE", "positive and negative fixtures checked") if outcome.wasSuccessful()
                         else ("FAIL", "paired fixture regression"))
    audit.reports(results, "synthetic", path, step=28, kinds=audit.KINDS)
    return int(any(status == "FAIL" for status, _ in results.values()))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--evidence":
        raise SystemExit(write_synthetic(Path(sys.argv[2])))
    unittest.main()
