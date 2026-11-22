"""Offline mutation tests for the exact 55-node/147-edge Terraform DAG map."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
import io

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_terraform_dag_paths as dag


class SourceMapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dag-source-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "infra", self.root / "infra")
        for relative in (dag.DAG, dag.MAP):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)

    def load_map(self):
        return json.loads((self.root / dag.MAP).read_text(encoding="utf-8"))

    def save_map(self, manifest):
        (self.root / dag.MAP).write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    def replace(self, rel, before, after):
        path = self.root / rel
        old = path.read_text(encoding="utf-8")
        self.assertIn(before, old)
        path.write_text(old.replace(before, after, 1), encoding="utf-8")

    def assert_invalid(self):
        x = dag.inspect(self.root)
        self.assertEqual(x["status"], "INVALID_DAG_SOURCE")
        self.assertTrue(x["errors"])
        self.assertEqual(x["azure_live_passes"], 0)
        self.assertEqual(x["release_decision"], "NO_GO")

    def test_baseline_55_nodes_147_edges_and_exact_class_counts(self):
        x = dag.inspect(self.root)
        self.assertEqual(x["status"], "SOURCE_PATHS_RECONCILED_NOT_ACCEPTED", x["errors"])
        self.assertEqual(x["errors"], [])
        self.assertEqual(x["dag_node_count"], 55)
        self.assertEqual(x["dag_edge_count"], 147)
        self.assertEqual(x["reported_nodes"], 55)
        self.assertEqual(x["source_classes"], dag.EXPECTED_CLASSES)
        self.assertEqual(sum(x["source_classes"].values()), 55)

    def test_all_code_nodes_have_real_source_but_are_not_accepted(self):
        x = dag.inspect(self.root)
        code = {id: v for id, v in x["nodes"].items()
                if v["source_state"] == "CODE_SOURCE_PRESENT_ONLY"}
        self.assertEqual(len(code), 30)
        self.assertTrue(all(v["declared_path_present"] for v in code.values()))
        self.assertTrue(all(not v["node_closed_or_approved"] for v in code.values()))
        self.assertEqual(x["code_nodes_approved"], 0)
        self.assertEqual(x["independent_review_approvals"], 0)

    def test_exact_reconciled_paths_have_source_anchors(self):
        x = dag.inspect(self.root)
        for ident, expected in dag.RECONCILED.items():
            with self.subTest(node=ident):
                self.assertEqual(x["nodes"][ident]["deliverable"], expected)
                self.assertTrue(x["nodes"][ident]["declared_path_present"])
                self.assertFalse((self.root / dag.LEGACY_ABSENT[ident]).exists())

    def test_optional_partial_and_absent_remain_explicit(self):
        x = dag.inspect(self.root)
        self.assertEqual(x["nodes"]["O02"]["source_state"], "OPTIONAL_AMPLS_PARTIAL")
        self.assertTrue(x["nodes"]["O02"]["declared_path_present"])
        for ident in ("N06", "A07", "W06"):
            self.assertEqual(x["nodes"][ident]["source_state"], "OPTIONAL_DECISION_PENDING")
            self.assertFalse(x["nodes"][ident]["declared_path_present"])

    def test_all_live_evidence_stays_uncreated_and_no_go(self):
        x = dag.inspect(self.root)
        self.assertEqual(x["source_classes"]["LIVE_APPROVAL_NOT_READY"], 14)
        self.assertEqual(x["azure_live_passes"], 0)
        self.assertEqual(x["release_decision"], "NO_GO")
        self.assertTrue(all(v["azure_acceptance"] == "NOT_READY" for v in x["nodes"].values()))
        self.assertEqual(sum(not v["declared_path_present"] for v in x["nodes"].values()), 24)

    def test_break_reconciled_code_resource_anchor(self):
        self.replace("infra/modules/ai-private-endpoints/main.tf",
                     'resource "azurerm_private_endpoint" "cosmos" {',
                     'resource "azurerm_private_endpoint" "not_cosmos" {')
        self.assert_invalid()

    def test_missing_g06_source_index_rejected(self):
        (self.root / "infra/modules/README.md").unlink()
        self.assert_invalid()

    def test_missing_gateway_source_rejected(self):
        (self.root / "infra/modules/application-gateway/gateway.tf").unlink()
        self.assert_invalid()

    def test_legacy_path_injected_rejected(self):
        legacy = self.root / dag.LEGACY_ABSENT["N02"]
        legacy.write_text('resource "azurerm_virtual_network" "workload" {}\n',
                          encoding="utf-8")
        self.assert_invalid()

    def test_dag_path_mutation_rejected(self):
        self.replace(dag.DAG, "infra/modules/azure-openai/main.tf",
                     "infra/modules/azure-openai/deployment.tf")
        self.assert_invalid()

    def test_declared_map_path_mutation_rejected(self):
        m = self.load_map()
        n = next(n for n in m["nodes"] if n["id"] == "B02")
        n["declared_path"] = "infra/bootstrap/storage_security.tf"
        self.save_map(m)
        self.assert_invalid()

    def test_unknown_map_node_and_missing_node_rejected(self):
        m = self.load_map()
        m["nodes"].pop()
        self.save_map(m)
        self.assert_invalid()

    def test_false_azure_success_in_manifest_rejected(self):
        m = self.load_map()
        m["azure_live_passes"] = 1716
        m["release_decision"] = "GO"
        self.save_map(m)
        self.assert_invalid()

    def test_fake_protected_live_evidence_requires_review(self):
        path = self.root / "evidence/restricted/nonprod-plan-manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{"approved":true}', encoding="utf-8")
        self.assert_invalid()

    def test_dependency_cycle_rejected(self):
        self.replace(dag.DAG, "| **G01** Deployment inputs and IPAM template | — |",
                     "| **G01** Deployment inputs and IPAM template | B01 |")
        self.assert_invalid()

    def test_unknown_dependency_rejected(self):
        self.replace(dag.DAG, "| **G01** Deployment inputs and IPAM template | — |",
                     "| **G01** Deployment inputs and IPAM template | Z99 |")
        self.assert_invalid()

    def test_cli_summary_and_expected_strict_refusal(self):
        with redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(dag.main(["--root", str(self.root),
                                       "--summary-only"]), 0)
        data = json.loads(stdout.getvalue())
        self.assertEqual(data["dag_node_count"], 55)
        self.assertEqual(data["release_decision"], "NO_GO")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(dag.main(["--root", str(self.root),
                                       "--summary-only", "--strict"]), 2)


if __name__ == "__main__":
    unittest.main()
