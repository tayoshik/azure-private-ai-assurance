"""Per-ID routing audit tests: source provenance and no false execution/acceptance."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_execution_route_1716 as route


class RoutingInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = route.build(ROOT, include_cases=True)

    def test_complete_exact_canonical_1716_id_coverage(self):
        report = self.inventory
        self.assertEqual(report["status"], "ROUTING_INVENTORY_ONLY", report["errors"])
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["canonical_test_ids"], 1716)
        self.assertEqual(set(report["cases"]), route.EXPECTED_IDS)
        self.assertEqual(sum(report["route_counts"].values()), 1716)
        self.assertEqual(sum(sum(c.values()) for c in
                             report["phase_route_counts"].values()), 1716)

    def test_exact_inherited_semantic_partitions(self):
        c = self.inventory["route_counts"]
        self.assertEqual(c[route.ROUTE_SYNTHETIC], 858)
        self.assertEqual(c[route.ROUTE_R41], 13)
        self.assertEqual(c[route.ROUTE_SELFTEST], 1)
        self.assertEqual(c[route.ROUTE_LIVE] + c[route.ROUTE_LOCAL], 844)
        self.assertEqual(c[route.ROUTE_LOCAL], 464)
        self.assertEqual(c[route.ROUTE_LIVE], 380)
        self.assertEqual(self.inventory["original_missing_script_count"], 13)
        self.assertEqual(self.inventory["r41_status"], "PROPOSED_NOT_APPROVED")

    def test_all_routes_have_provenance_hash_and_next_action(self):
        for case_id, row in self.inventory["cases"].items():
            with self.subTest(case_id=case_id):
                self.assertEqual(len(row["catalogue_contract_sha256"]), 64)
                self.assertEqual(set(row["catalogue_contract_sha256"]) <=
                                 set("0123456789abcdef"), True)
                self.assertIn(row["route"], route.PREREQUISITES)
                self.assertEqual(row["prerequisite_classes"],
                                 list(route.PREREQUISITES[row["route"]]))
                self.assertEqual(row["proposed_owner_role"], route.OWNER_LANE[row["route"]])
                self.assertEqual(row["next_action"], route.NEXT_ACTION[row["route"]])
                self.assertEqual(row["azure_live_acceptance"], "NOT_READY")
                self.assertFalse(row["source_test_executed"])
                self.assertFalse(row["approved_inputs_verified"])
                self.assertFalse(row["independent_reviewer_signed"])

    def test_not_even_one_azure_pass_or_source_execution_is_inferred(self):
        x = self.inventory
        self.assertEqual(x["source_cases_executed_by_this_report"], 0)
        self.assertEqual(x["azure_live_passes_verified"], 0)
        self.assertEqual(x["azure_not_ready"], 1716)
        self.assertEqual(x["independent_review_approvals_verified"], 0)
        self.assertEqual(x["release_decision"], "NO_GO")
        self.assertFalse(any(r["azure_live_acceptance"] != "NOT_READY"
                             for r in x["cases"].values()))

    def test_13_browser_cases_remain_unresolved_and_not_approved(self):
        ids = set(route.R41_IDS)
        self.assertEqual(len(ids), 13)
        self.assertEqual({i for i, r in self.inventory["cases"].items()
                          if r["route"] == route.ROUTE_R41}, ids)
        self.assertEqual({i for i, r in self.inventory["cases"].items()
                          if r["missing_script_paths"]}, ids)
        for case_id in ids:
            row = self.inventory["cases"][case_id]
            self.assertFalse(row["r41_scope_approved"])
            self.assertEqual(row["semantic_readiness"], "SOURCE_REFERENCE_MISSING")
            self.assertTrue(row["missing_script_paths"])

    def test_odd_selftest_is_only_target_74_13(self):
        ids = {i for i, r in self.inventory["cases"].items()
               if r["route"] == route.ROUTE_SELFTEST}
        self.assertEqual(ids, {"AZ-T74-13"})
        self.assertEqual(self.inventory["cases"]["AZ-T74-13"]["azure_live_acceptance"],
                         "NOT_READY")

    def test_direct_local_and_live_command_examples(self):
        r = self.inventory["cases"]
        self.assertEqual(r["AZ-T01-01"]["route"], route.ROUTE_LOCAL)
        self.assertEqual(r["AZ-T01-02"]["route"], route.ROUTE_SYNTHETIC)
        self.assertEqual(r["AZ-T21-01"]["route"], route.ROUTE_LIVE)
        self.assertEqual(r["AZ-T23-19"]["route"], route.ROUTE_LIVE)
        self.assertTrue(r["AZ-T21-01"]["direct_execution_requires_azure_or_private_runner"])
        self.assertFalse(r["AZ-T01-01"]["direct_execution_requires_azure_or_private_runner"])

    def test_not_all_local_appearance_is_runnable_without_approved_baseline(self):
        case = self.inventory["cases"]["AZ-T01-01"]
        self.assertEqual(case["route"], route.ROUTE_LOCAL)
        self.assertIn("APPROVED_SOURCE_ARTIFACT_OR_BASELINE",
                      case["prerequisite_classes"])
        self.assertFalse(case["approved_inputs_verified"])
        self.assertFalse(case["source_test_executed"])

    def test_command_routing_does_not_execute_malicious_shell(self):
        s = {"assurance_readiness": "UNVERIFIED_NON_SYNTHETIC_PROCEDURE"}
        examples = (
            ("az group list --query foo", route.ROUTE_LIVE),
            ("dig +short internal.example.invalid", route.ROUTE_LIVE),
            ("terraform -chdir=infra plan -refresh-only", route.ROUTE_LIVE),
            ("terraform -chdir=infra show -json approval.tfplan", route.ROUTE_LOCAL),
            ("jq -e '.approved' local.json", route.ROUTE_LOCAL),
            ("echo malicious && curl https://example.invalid", route.ROUTE_LOCAL),
        )
        for command, want in examples:
            with self.subTest(command=command):
                lane, _ = route.route_case("AZ-T71-01", command, s)
                self.assertEqual(lane, want)
        # This tests prefix-only classification, NOT shell safety or execution.
        # The entire catalogue is *never* executed by this inventory.

    def test_no_synthetic_false_promotion_from_command_or_odd_case(self):
        s = {"assurance_readiness": "OFFLINE_SYNTHETIC_ONLY"}
        with self.assertRaises(route.InventoryError):
            route.route_case("AZ-T01-02", "az group list", s)
        with self.assertRaises(route.InventoryError):
            route.route_case("AZ-T01-01", "python3 script.py --selftest", s)

    def test_unexpected_source_missing_cannot_be_relabelled_r41(self):
        source = {"assurance_readiness": "SOURCE_REFERENCE_MISSING"}
        with self.assertRaises(route.InventoryError):
            route.route_case("AZ-T71-01", "python3 absent.py", source)
        with self.assertRaises(route.InventoryError):
            route.route_case("AZ-T64-01", "npx playwright test absent", {
                "assurance_readiness": "UNVERIFIED_NON_SYNTHETIC_PROCEDURE"
            })

    def test_odd_unexpected_selftest_is_not_silently_allowed(self):
        with self.assertRaises(route.InventoryError):
            route.route_case("AZ-T71-01", "python3 script.py --selftest",
                            {"assurance_readiness": "ODD_SELFTEST_REQUIRES_SEMANTIC_REVIEW"})

    def test_frozen_contract_digest_changes_when_expected_changes(self):
        a = {"id": "AZ-T01-01", "command": "python3 x.py", "expected": "A"}
        b = deepcopy(a)
        b["expected"] = "B"
        self.assertNotEqual(route.digest_case(a), route.digest_case(b))
        self.assertEqual(len(route.digest_case(a)), 64)

    def test_cli_summary_succeeds_strict_expected_denial(self):
        for strict in (False, True):
            args = [sys.executable, str(ROOT/"scripts/build_execution_route_1716.py"),
                    "--summary-only"]
            if strict:
                args.append("--strict")
            with self.subTest(strict=strict):
                p = subprocess.run(args, cwd=ROOT, capture_output=True,
                                   text=True, check=False)
                self.assertEqual(p.returncode, 2 if strict else 0, p.stderr)
                data = json.loads(p.stdout)
                self.assertEqual(data["canonical_test_ids"], 1716)
                self.assertEqual(data["azure_not_ready"], 1716)
                self.assertEqual(data["release_decision"], "NO_GO")
                self.assertEqual(data["errors"], [])

    def test_cli_writes_1716_rows_json_not_csv(self):
        with tempfile.TemporaryDirectory(prefix="route-json-") as td:
            path = Path(td) / "execution-route-1716.json"
            p = subprocess.run([sys.executable, str(ROOT/"scripts/build_execution_route_1716.py"),
                                "--out", str(path)], cwd=ROOT,
                               capture_output=True, text=True, check=False)
            self.assertEqual(p.returncode, 0, p.stderr)
            report = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(len(report["cases"]), 1716)
            self.assertEqual(report["source_cases_executed_by_this_report"], 0)
            self.assertEqual(report["release_decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
