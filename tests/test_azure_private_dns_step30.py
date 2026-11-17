"""Synthetic and mocked tests. No subprocess DNS or Azure transport is used."""
import contextlib
from copy import deepcopy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import azure_private_dns_step30 as audit


def fixture():
    web, _ = audit.rest04.synthetic_inputs()
    scm = {**web, "a_record_id": web["a_record_id"] + ".scm",
           "expected_record_fqdn": web["expected_record_fqdn"].replace(".privatelink.", ".scm.privatelink.")}
    targets = {}
    for profile, arm in (("web", web), ("scm", scm)):
        ordinary = arm["expected_record_fqdn"].replace(".privatelink.", ".")
        targets[profile] = {"arm": arm, "ordinary_name": ordinary, "private_name": arm["expected_record_fqdn"],
                            "expected_cidrs": ["10.32.5.0/24"], "cname_chain": [ordinary, arm["expected_record_fqdn"]]}
    return {"schema": "azure-private-dns/az-t30/v1", "topology": "dev", "approval_ref": "synthetic",
            "approved_private_runner": True, "resolver_ips": ["10.32.5.53"], "targets": targets}


class PrivateDNSStage30(unittest.TestCase):
    def test_all_eleven_paired_detectors(self):
        checks = audit.synthetic_checks()
        self.assertEqual(sorted(checks), list(range(2, 23, 2)))
        self.assertTrue(all(checks.values()))

    def test_config_checks_web_and_scm_in_both_topologies(self):
        for topology in ("hub", "dev"):
            self.assertEqual(audit.validate({**fixture(), "topology": topology})["topology"], topology)

    def test_scm_requires_distinct_record_and_same_pe(self):
        cfg = fixture()
        cfg["targets"]["scm"]["arm"]["subnet_id"] += "-different"
        with self.assertRaisesRegex(ValueError, "same approved PE"):
            audit.validate(cfg)
        cfg = fixture()
        cfg["targets"]["scm"]["ordinary_name"] = cfg["targets"]["web"]["ordinary_name"]
        with self.assertRaisesRegex(ValueError, "service class"):
            audit.validate(cfg)

    def test_expected_ip_must_match_approved_cidr(self):
        cfg = fixture()
        cfg["targets"]["web"]["expected_cidrs"] = ["10.32.6.0/24"]
        with self.assertRaisesRegex(ValueError, "outside the approved CIDRs"):
            audit.validate(cfg)

    def test_empty_approval_inputs_do_not_launch_network(self):
        cfg = fixture()
        cfg["resolver_ips"] = []
        with self.assertRaisesRegex(ValueError, "resolver"):
            audit.validate(cfg)

    def test_complete_multiple_ips_allow_reordering(self):
        target = "p.example.invalid"
        rows = [(target, "A", "10.0.0.2"), (target, "A", "10.0.0.1")]
        audit.check_addresses(rows, [target], ["10.0.0.1", "10.0.0.2"])

    def test_wrong_extra_missing_unrelated_and_duplicate_answers(self):
        owner = "p.example.invalid"
        expected = [(owner, "A", "10.0.0.1"), (owner, "A", "10.0.0.2")]
        for rows in (expected[:1], expected + [(owner, "A", "10.0.0.3")], expected + [expected[0]],
                     [(owner, "A", "8.8.8.8"), expected[1]],
                     [("different.example.invalid", "A", "10.0.0.1"), expected[1]]):
            with self.subTest(rows=len(rows)), self.assertRaises(audit.Mismatch):
                audit.check_addresses(rows, [owner], ["10.0.0.1", "10.0.0.2"])

    def test_cname_redirect_and_loop_are_rejected(self):
        ordinary, private = "w.example.invalid", "p.example.invalid"
        for bad in ("other.example.invalid", ordinary):
            with self.subTest(bad=bad), self.assertRaises(audit.Mismatch):
                audit.check_aliases(lambda *_: [(ordinary, "CNAME", bad)], "resolver", [ordinary, private])

    def test_empty_a_is_not_ready(self):
        with self.assertRaisesRegex(audit.NotReadyError, "empty"):
            audit.check_addresses([], ["p.example.invalid"], ["10.0.0.1"])

    def test_nxdomain_servfail_refused_and_timeout_sanitized(self):
        for status in ("NXDOMAIN", "SERVFAIL", "REFUSED"):
            runner = Mock(return_value=subprocess.CompletedProcess([], 0, f";; status: {status}, id: 10\n"))
            with patch.object(audit.subprocess, "run", runner), self.assertRaisesRegex(audit.NotReadyError, status):
                audit.dig_query("10.32.5.53", "private.example.invalid", "A")
        with patch.object(audit.subprocess, "run", side_effect=subprocess.TimeoutExpired(["private.example.invalid"], 5)):
            with self.assertRaisesRegex(audit.NotReadyError, "^DNS query timed out$"):
                audit.dig_query("10.32.5.53", "private.example.invalid", "A")

    def test_dig_uses_explicit_address_absolute_name_and_tcp(self):
        out = ";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 1\np.example.invalid. 10 IN A 10.0.0.1\n"
        with patch.object(audit.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, out)) as run:
            self.assertEqual(audit.dig_query("10.32.5.53", "p.example.invalid", "A"),
                             [("p.example.invalid", "A", "10.0.0.1")])
        self.assertEqual(run.call_args.args[0][:5], ["dig", "-r", "@10.32.5.53", "p.example.invalid.", "A"])
        self.assertIn("+tcp", run.call_args.args[0])

    def test_pending_pe_blocks_only_related_control_plane_and_bound_a_checks(self):
        cfg = fixture()
        with patch.object(audit, "assess_arm", return_value={
                "web": {"issues": ["pe.approval"]}, "scm": {"issues": ["pe.approval"]}}):
            result = audit.findings(cfg, Mock(), lambda *_: [])
        self.assertEqual(result[1][0], "OBSERVED_NOT_ACCEPTED")
        self.assertEqual(result[11][0], "FAIL")
        self.assertEqual(result[21][0], "FAIL")
        self.assertEqual(result[13][0], "NOT_READY")  # other required services missing
        self.assertNotIn("web-synthetic", result[21][1])

    def test_group_and_link_categories_do_not_mask_each_other(self):
        observations = {"issues": ["vnetLink.registrationEnabled must be false", "dns.aRecord != approved NIC IP set"]}
        self.assertEqual(audit.arm_status(observations, "link")[0], "FAIL")
        self.assertEqual(audit.arm_status(observations, "group")[0], "OBSERVED_NOT_ACCEPTED")
        self.assertEqual(audit.arm_status({"missing": ["complete, scoped, digest-verified REST02 observations"]},
                                          "group")[0], "NOT_READY")

    def test_ownership_duplicates_only_within_same_view(self):
        entry = {"dns_view": "one", "zone": "p.example.invalid", "zone_resource_id": "fixture", "owner": "fixture"}
        audit.owner_inventory({"complete_for_review": True, "zones": [entry, {**entry, "dns_view": "two"}]})
        with self.assertRaises(audit.Mismatch):
            audit.owner_inventory({"complete_for_review": True, "zones": [entry, {**entry, "dns_view": "ONE"}]})

    def test_opt_in_modes_emit_separate_json_and_junit_without_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "input.json"
            config.write_text(json.dumps(fixture()))
            with patch.object(audit, "workload_identity_token_provider") as auth, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(audit.main(["--out", str(root / "missing")]), 2)
                self.assertEqual(audit.main(["--check-config", "--config", str(config), "--out", str(root / "shape")]), 0)
                self.assertEqual(audit.main(["--selftest", "--out", str(root / "offline")]), 0)
            auth.assert_not_called()
            report = json.loads((root / "offline/results.json").read_text())
            self.assertEqual(report["mode"], "synthetic")
            self.assertEqual(report["azure_accepted"], 0)
            self.assertEqual(len(report["results"]), 11)
            xml = ET.parse(root / "missing/junit.xml").getroot()
            self.assertEqual(xml.get("skipped"), "22")
            for path in root.glob("*/*"):
                text = path.read_text()
                self.assertNotIn("web-synthetic", text)
                self.assertNotIn("10.32.5.", text)

    def test_missing_identity_writes_reasons_for_all_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "input.json"
            config.write_text(json.dumps(fixture()))
            with patch.object(audit, "workload_identity_token_provider", side_effect=audit.NotReadyError("OIDC unavailable")), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(audit.main(["--live", "--config", str(config), "--out", str(root / "live")]), 2)
            report = json.loads((root / "live/results.json").read_text())
            self.assertEqual(len(report["results"]), 22)
            self.assertTrue(all(item["reason"] == "OIDC unavailable" for item in report["results"]))

    def test_all_six_service_paths_can_produce_observations_without_acceptance(self):
        cfg = fixture()
        for profile in ("openai", "search", "cosmos", "vault"):
            group, suffix, _ = audit.PROFILES[profile]
            provider, zone = audit.rest04.SERVICE_PROFILES[group]
            def converted(obj):
                return json.loads(json.dumps(obj).replace("privatelink.azurewebsites.net", zone)
                                  .replace("/providers/Microsoft.Web/sites/", provider)
                                  .replace('"sites"', json.dumps(group)).replace("web-synthetic", profile + "-synthetic"))
            entry = converted(cfg["targets"]["web"])
            entry["ordinary_name"] = profile + "-synthetic." + suffix
            entry["cname_chain"][0] = entry["ordinary_name"]
            cfg["targets"][profile] = entry
        audit.validate(cfg)
        by_name = {name: entry for entry in cfg["targets"].values() for name in entry["cname_chain"]}

        def query(_, host, kind):
            entry = by_name[host]
            ordinary, private = entry["cname_chain"]
            alias = [(ordinary, "CNAME", private)] if host == ordinary else []
            return alias if kind == "CNAME" else alias + [(private, "A", "10.32.5.9")]

        with patch.object(audit, "assess_arm", return_value={k: {} for k in cfg["targets"]}):
            findings = audit.findings(cfg, Mock(), query)
        observed = {i for i, (value, _) in findings.items() if value == "OBSERVED_NOT_ACCEPTED"}
        self.assertEqual(observed, set(audit.KINDS) - {17})

    def test_hub_link_vnet_can_differ_from_endpoint_subnet_vnet(self):
        target, wrapped = audit.rest04.synthetic_inputs()
        linked_vnet = target["vnet_id"] + "-shared"
        target["expected_link_vnet_id"] = linked_vnet
        link = wrapped["vnet_link"]["observation"]
        link["properties"]["virtualNetwork"]["id"] = linked_vnet
        wrapped["vnet_link"]["evidence_sha256"] = audit.rest04.digest(link)
        self.assertEqual(audit.rest04.assess_target(target, wrapped)["status"], "OBSERVED_PENDING_PRIVATE_DNS_PROBE")
        target.pop("expected_link_vnet_id")
        self.assertIn("vnetLink.vnet", audit.rest04.assess_target(target, wrapped)["issues"])
        target["expected_link_vnet_id"] = target["subnet_id"]
        with self.assertRaisesRegex(ValueError, "exact VNet"):
            audit.rest04.validate_target(target)
