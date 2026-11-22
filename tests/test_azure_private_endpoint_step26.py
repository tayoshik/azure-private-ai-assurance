"""AZ-T26 synthetic contract and regression tests. No Azure or socket I/O."""
from contextlib import redirect_stdout
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, Mock, patch
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import azure_private_endpoint_step26 as audit


def fixture():
    source, observed = audit.rest04.synthetic_inputs()
    base = source["vnet_id"].split("/virtualNetworks/")[0]
    nsg = base + "/networkSecurityGroups/synthetic"
    target = {key: source[key] for key in ("private_endpoint_id", "nic_id", "service_id", "group_id", "expected_private_ips")}
    target.update(purpose="web-pe", asg_ids=[])
    entry = {"vnet_id": source["vnet_id"], "subnet_id": source["subnet_id"], "purpose": "web-pe",
             "cidrs": ["10.32.5.0/24"], "mode": "Enabled", "required_enforcement": ["nsg"],
             "nsg_id": nsg, "route_table_id": None, "expected_routes": [],
             "source_cidrs": ["10.32.6.0/24"], "source_asg_ids": [], "endpoints": [target]}
    cfg = {"schema": "azure-private-endpoint/az-t26/v1", "topology": "dev", "environment": "nonproduction",
           "approval_ref": "synthetic", "approved_private_runner": True,
           "subscriptions": [source["subnet_id"].split("/")[2]], "subnets": [entry]}
    bodies = {row["resource_id"]: deepcopy(row["observation"]) for row in observed.values()}
    for field in ("private_endpoint_id", "nic_id"):
        bodies[target[field]]["properties"]["provisioningState"] = "Succeeded"
    bodies[entry["subnet_id"]] = {"properties": {"provisioningState": "Succeeded", "addressPrefix": "10.32.5.0/24",
        "privateEndpoints": [{"id": target["private_endpoint_id"]}], "delegations": [],
        "privateEndpointNetworkPolicies": "Enabled", "networkSecurityGroup": {"id": nsg}}}
    allow = {"priority": 100, "direction": "Inbound", "access": "Allow", "protocol": "Tcp",
             "sourceAddressPrefix": "10.32.6.0/24", "sourcePortRange": "*",
             "destinationAddressPrefix": "*", "destinationPortRange": "443"}
    deny = {**allow, "priority": 200, "access": "Deny", "protocol": "*", "sourceAddressPrefix": "*",
            "destinationPortRange": "*"}
    bodies[nsg] = {"properties": {"provisioningState": "Succeeded",
                                 "securityRules": [{"properties": rule} for rule in (allow, deny)]}}
    client = Mock()
    client.get_resource.side_effect = lambda rid, _: {"observation": bodies[rid]}
    return cfg, bodies, client


def probe(config, direction="deny"):
    config["isolation_approved"] = True
    config["probe"] = {"direction": direction, "isolated_deny_approved": True,
                       "runner_approval_ref": "synthetic", "probe_approval_ref": "synthetic",
                       "subnet_index": 0, "endpoint_index": 0, "source_ip": "10.32.6.2" if direction == "allow" else "10.32.7.2",
                       "runner_cidr": "10.32.6.0/24" if direction == "allow" else "10.32.7.0/24",
                       "outside_approved_source_asgs": direction == "deny", "destination_ip": "10.32.5.9",
                       "probe_ref": "synthetic", "observed_at": datetime.now(timezone.utc).isoformat()}
    return config["probe"]


class Step26(unittest.TestCase):
    def setUp(self):
        self.cfg, self.bodies, self.client = fixture()
        self.entry = self.cfg["subnets"][0]
        self.target = self.entry["endpoints"][0]
        self.subnet = self.bodies[self.entry["subnet_id"]]["properties"]
        self.pe = self.bodies[self.target["private_endpoint_id"]]["properties"]
        self.nic = self.bodies[self.target["nic_id"]]["properties"]
        self.nsg = self.bodies[self.entry["nsg_id"]]["properties"]
        self.allow = self.nsg["securityRules"][0]["properties"]

    def findings(self):
        return audit.arm_checks(audit.validate(self.cfg), self.client)

    def paired(self, identifier, mutate):
        self.assertEqual(self.findings()[identifier][0], "CONFIG_OBSERVED_NOT_ACCEPTED")
        mutate()
        self.assertIn(self.findings()[identifier][0], ("FAIL", "NOT_READY"))

    def test_t26_02_zoning(self):
        self.paired(1, lambda: self.pe["subnet"].update(id=self.entry["subnet_id"] + "-wrong"))

    def test_t26_04_associations(self):
        self.paired(3, lambda: self.subnet["networkSecurityGroup"].update(id=self.entry["nsg_id"] + "-wrong"))

    def test_t26_06_policy(self):
        self.paired(5, lambda: self.subnet.update(privateEndpointNetworkPolicies="RouteTableEnabled"))

    def test_t26_08_route(self):
        self.paired(7, lambda: self.subnet.update(routeTable={"id": self.entry["nsg_id"]}))

    def test_t26_10_ip(self):
        self.paired(9, lambda: self.nic["ipConfigurations"][0]["properties"].update(privateIPAddress="10.32.5.20"))

    def test_t26_12_sources(self):
        self.paired(11, lambda: self.allow.update(sourceAddressPrefix="*"))

    def test_t26_14_deny(self):
        self.paired(13, lambda: self.nsg["securityRules"].pop())

    def test_t26_16_port(self):
        self.paired(15, lambda: self.allow.update(destinationPortRange="*"))

    def test_t26_18_asg(self):
        self.paired(17, lambda: self.pe.update(applicationSecurityGroups=[{"id": self.entry["nsg_id"]}]))

    def test_t26_20_flow(self):
        plan = probe(self.cfg)
        row = {**plan, "decision": "Deny", "port": 443, "protocol": "TCP"}
        doc = {"review_ref": "synthetic", "records": [row]}
        audit.review_flow(doc, plan)
        row["observed_at"] = (datetime.fromisoformat(plan["observed_at"]) - timedelta(minutes=10)).isoformat()
        with self.assertRaisesRegex(audit.NotReadyError, "correlation window"):
            audit.review_flow(doc, plan)

    def test_t26_22_isolation(self):
        plan = probe(self.cfg)
        audit.probe_input(self.cfg)
        plan["isolated_deny_approved"] = False
        with self.assertRaisesRegex(ValueError, "denial exercise approval"):
            audit.probe_input(self.cfg)

    def test_config_modes_follow_design(self):
        for mode, required in (("Disabled", []), ("NetworkSecurityGroupEnabled", ["nsg"]), ("Enabled", ["nsg"])):
            self.entry.update(mode=mode, required_enforcement=required)
            self.subnet["privateEndpointNetworkPolicies"] = mode
            self.assertEqual(self.findings()[5][0], "CONFIG_OBSERVED_NOT_ACCEPTED")
        self.entry.update(mode="RouteTableEnabled", required_enforcement=["nsg"])
        with self.assertRaisesRegex(ValueError, "required enforcement"):
            audit.validate(self.cfg)

    def test_wrong_vnet_purpose_and_outside_ip_rejected_before_arm(self):
        for field, value, reason in (("vnet_id", self.entry["vnet_id"] + "-wrong", "approved VNet"),
                                     ("purpose", "other-pe", "purpose")):
            with patch.dict(self.entry, {field: value}), self.assertRaisesRegex(ValueError, reason):
                audit.validate(self.cfg)
        self.target["expected_private_ips"] = ["10.32.8.2"]
        with self.assertRaisesRegex(ValueError, "outside subnet"):
            audit.validate(self.cfg)
        self.client.get_resource.assert_not_called()

    def test_pending_rejected_and_wrong_target_are_not_success(self):
        props = self.pe["privateLinkServiceConnections"][0]["properties"]
        for value in ("Pending", "Rejected"):
            props["privateLinkServiceConnectionState"]["status"] = value
            self.assertIn("pe.approval", self.findings()[9][1])
        props["privateLinkServiceConnectionState"]["status"] = "Approved"
        props["privateLinkServiceId"] += "-wrong"
        props["groupIds"] = ["blob"]
        self.assertIn("pe.service", self.findings()[9][1])
        self.assertIn("pe.groupIds", self.findings()[9][1])

    def test_permission_paging_and_missing_fields_never_mean_absent(self):
        self.client.get_resource.side_effect = audit.NotReadyError("ARM 403")
        self.assertTrue(all(state == "NOT_READY" for state, _ in self.findings().values()))
        self.client.get_resource.side_effect = lambda rid, _: {"observation": self.bodies[rid]}
        self.bodies[self.entry["subnet_id"]]["nextLink"] = "https://unexpected.invalid"
        self.assertEqual(self.findings()[1][0], "NOT_READY")
        self.bodies[self.entry["subnet_id"]].pop("nextLink")
        self.subnet.pop("privateEndpoints")
        self.assertEqual(self.findings()[1][0], "NOT_READY")
        self.subnet.pop("privateEndpointNetworkPolicies")
        self.assertEqual(self.findings()[5][0], "NOT_READY")

    def test_tcp_is_source_bound_and_deny_timeout_is_not_success(self):
        plan = probe(self.cfg, "allow")
        connect = MagicMock()
        sock = connect.return_value.__enter__.return_value
        sock.getsockname.return_value = (plan["source_ip"], 20001)
        sock.getpeername.return_value = (plan["destination_ip"], 443)
        self.assertEqual(audit.run_probe(self.cfg, self.client, connect)[1][0], "TCP_OBSERVED_NOT_ACCEPTED")
        connect.assert_called_once_with((plan["destination_ip"], 443), timeout=3, source_address=(plan["source_ip"], 0))
        plan = probe(self.cfg, "deny")
        sock.getsockname.return_value = (plan["source_ip"], 20001)
        self.assertEqual(audit.run_probe(self.cfg, self.client, connect)[1][0], "FAIL")
        self.assertEqual(audit.run_probe(self.cfg, self.client, Mock(side_effect=TimeoutError()))[1][0], "NOT_READY")

    def test_explicit_udr_and_entries(self):
        rid = self.entry["nsg_id"].replace("networkSecurityGroups", "routeTables")
        self.entry.update(route_table_id=rid, required_enforcement=["udr"],
                          expected_routes=[{"prefix": "10.32.6.0/24", "next_hop_type": "VirtualAppliance",
                                            "next_hop_ip": "10.32.7.5"}])
        self.subnet["routeTable"] = {"id": rid}
        route = {"addressPrefix": "10.32.6.0/24", "nextHopType": "VirtualAppliance",
                 "nextHopIpAddress": "10.32.7.5", "provisioningState": "Succeeded"}
        self.bodies[rid] = {"properties": {"provisioningState": "Succeeded", "routes": [{"properties": route}]}}
        self.assertEqual(self.findings()[7][0], "CONFIG_OBSERVED_NOT_ACCEPTED")
        route["nextHopIpAddress"] = "10.32.7.1"
        self.assertEqual(self.findings()[7][0], "FAIL")

    def test_pending_pe_never_launches_tcp(self):
        probe(self.cfg, "allow")
        self.pe["privateLinkServiceConnections"][0]["properties"]["privateLinkServiceConnectionState"]["status"] = "Pending"
        connection = Mock()
        with self.assertRaisesRegex(audit.Mismatch, "pe.approval"):
            audit.run_probe(self.cfg, self.client, connection)
        connection.assert_not_called()

    def test_config_can_check_both_topologies_without_live_io(self):
        with tempfile.TemporaryDirectory() as temporary, redirect_stdout(io.StringIO()):
            root = Path(temporary)
            config_file = root / "inputs.json"
            with patch.object(audit, "client_for") as arm:
                for topology in ("hub", "dev"):
                    self.cfg["topology"] = topology
                    config_file.write_text(json.dumps(self.cfg))
                    self.assertEqual(audit.main(["--check-config", "--config", str(config_file), "--out", str(root / topology)]), 0)
                self.assertEqual(audit.main(["--out", str(root / "no-args")]), 2)
                arm.assert_not_called()
            data = json.loads((root / "no-args/results.json").read_text())
            self.assertEqual(data["azure_accepted"], 0)
            self.assertEqual(len(data["results"]), 22)
            self.assertEqual(ET.parse(root / "dev/junit.xml").getroot().get("skipped"), "22")
            for file in root.glob("*/*"):
                self.assertNotIn("10.32", file.read_text())
                self.assertNotIn("rg-synthetic", file.read_text())


def synthetic_reports(path):
    result = {}
    for identifier in range(2, 23, 2):
        method = next(name for name in dir(Step26) if name.startswith(f"test_t26_{identifier:02}_"))
        outcome = unittest.TestResult()
        Step26(method).run(outcome)
        result[identifier] = (("MATCHED_OFFLINE", "positive and negative fixtures checked")
                              if outcome.wasSuccessful() else ("FAIL", "paired fixture regression"))
    audit.reports(result, "synthetic", path, step=26, kinds=audit.KINDS)
    return int(any(status == "FAIL" for status, _ in result.values()))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--evidence":
        raise SystemExit(synthetic_reports(Path(sys.argv[2])))
    unittest.main()
