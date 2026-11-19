"""Offline regression tests for 1,716-ID dependency audit and fail-closed release."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.audit_catalogue_dependencies import (
    EXPECTED_IDS, audit, literal_refs, path_exists,
)
from scripts.release_gate import decide

ROOT = Path(__file__).resolve().parents[1]


class DependencyAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = audit(ROOT, include_cases=True)

    def test_exact_canonical_coverage(self):
        self.assertEqual(self.report["errors"], [])
        self.assertEqual(self.report["canonical_test_ids"], 1716)
        self.assertEqual(set(self.report["cases"]), EXPECTED_IDS)
        self.assertEqual(sum(self.report["catalogue_counts"].values()), 1716)

    def test_every_id_classified_without_false_azure_pass(self):
        counts = self.report["literal_script_reference"]
        self.assertEqual(sum(counts.values()), 1716)
        for row in self.report["cases"].values():
            self.assertEqual(row["azure_acceptance"], "NOT_READY")
            self.assertIn(row["literal_script_state"], counts)
        self.assertEqual(self.report["release_decision"], "NO_GO")
        self.assertEqual(self.report["azure_live_passes_verified"], 0)

    def test_current_missing_references_are_reported(self):
        self.assertGreater(self.report["cases_with_unresolved_literal_dependencies"], 0)
        self.assertIn("scripts/phase1_policy_check.py", self.report["missing_script_paths"])
        self.assertIn("specs/phase1_policies_110.json", self.report["missing_input_paths"])
        self.assertIn("AZ-T01-01", self.report["unresolved_ids"])

    def test_literal_parser_does_not_misclassify_azure_cli(self):
        command = 'az network vnet show -g "$RG" -n "$NAME" --query id'
        self.assertEqual(literal_refs(command), ([], []))

    def test_known_missing_and_present_paths(self):
        scripts, inputs = literal_refs(
            'python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json'
        )
        self.assertEqual(scripts, ["scripts/phase1_policy_check.py"])
        self.assertEqual(inputs, ["specs/phase1_policies_110.json"])
        self.assertTrue(path_exists(ROOT, "scripts/release_gate.py"))
        self.assertFalse(path_exists(ROOT, "../untrusted.py"))
        self.assertFalse(path_exists(ROOT, "scripts/phase1_policy_check.py"))

    def test_modified_claim_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "specs").mkdir()
            (root / "specs/english_tests_001_440.json").write_text(json.dumps({
                "cases": [{
                    "id": "AZ-T01-01", "step": 1, "command": "az version",
                    "azure_live_pass": True,
                }]
            }))
            report = audit(root)
            self.assertEqual(report["status"], "INVALID_CATALOGUE")
            self.assertTrue(any("live acceptance" in x for x in report["errors"]))
            self.assertEqual(report["release_decision"], "NO_GO")

    def test_strict_audit_returns_nonzero_for_missing_dependencies(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/audit_catalogue_dependencies.py"),
             "--strict"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 2)
        report = json.loads(proc.stdout)
        self.assertEqual(report["canonical_test_ids"], 1716)

    def test_release_gate_no_go_and_exit_code(self):
        report = decide(ROOT)
        self.assertEqual(report["decision"], "NO_GO")
        self.assertEqual(report["catalogue_test_ids"], 1716)
        self.assertEqual(report["recorded_azure_live_passes"], 0)
        self.assertEqual(report["verified_live_azure_passes"], 0)
        self.assertGreater(report["dependency_unresolved_ids"], 0)
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/release_gate.py")],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout)["decision"], "NO_GO")

    def test_release_gate_fails_closed_on_missing_root(self):
        with tempfile.TemporaryDirectory() as folder:
            report = decide(Path(folder))
            self.assertEqual(report["decision"], "NO_GO")
            self.assertGreaterEqual(len(report["reasons"]), 2)
            self.assertEqual(report["verified_live_azure_passes"], 0)


if __name__ == "__main__":
    unittest.main()
