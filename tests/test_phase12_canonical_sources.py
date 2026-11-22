"""Source provenance and fail-closed regression for recovered Phase 1/2.

Source exists and passes synthetic tests != real Azure security acceptance.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import phase1_policy_check as phase1
from scripts import phase2_policy_check as phase2
from scripts.audit_catalogue_dependencies import audit

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "specs/phase1_policies_110.json"
SPEC2 = ROOT / "specs/phase2_220.json"
PUBLISHED = ROOT / "specs/english_tests_001_440.json"


class SourceAndSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = json.loads(RULES.read_text(encoding="utf-8"))
        cls.spec2 = phase2.load_spec(SPEC2)
        cls.published = {
            x["id"]: x for x in json.loads(PUBLISHED.read_text(encoding="utf-8"))["cases"]
        }

    def run_phase1(self, *args):
        proc = subprocess.run([sys.executable, str(ROOT / "scripts/phase1_policy_check.py"),
                               "--rules", str(RULES), *args],
                              cwd=ROOT, capture_output=True, text=True, check=False)
        return proc, json.loads(proc.stdout)

    def test_phase1_source_110_rules_and_exact_220_ids(self):
        ids = {identifier for r in self.rules for identifier in
               (r["positive_id"], r["negative_id"])}
        self.assertEqual(len(self.rules), 110)
        self.assertEqual(len({r["field_path"] for r in self.rules}), 110)
        self.assertEqual(ids, {f"AZ-T{s:02}-{n:02}" for s in range(1, 11) for n in range(1, 23)})
        self.assertEqual({r["operator"] for r in self.rules},
                         {"eq", "enum", "positive", "nonempty", "list_nonempty"})
        for r in self.rules:
            self.assertIn(r["positive_id"], self.published)
            self.assertIn(r["negative_id"], self.published)

    def test_phase1_all_synthetic_good_bad_missing(self):
        for r in self.rules:
            sample = phase1.selftest(r)
            self.assertEqual(sample["selftest_status"], "SELFTEST_PASS", r["negative_id"])
            self.assertEqual(sample["good_fixture"], "PASS")
            self.assertEqual(sample["bad_fixture"], "FAIL")
            self.assertEqual(sample["missing_fixture"], "NOT_READY")
            self.assertTrue(sample["synthetic_only"])

    def test_phase1_synthetic_cli_does_not_claim_azure_acceptance(self):
        result, obj = self.run_phase1("--selftest", "--all")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(obj["summary"]["SELFTEST_PASS"], 110)
        self.assertEqual(obj["azure_live_pass_count"], 0)

    def test_phase1_baseline_match_is_review_required(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "example.json"
            p.write_text(json.dumps({"network": {"data_plane": {"private_only": True}}}))
            proc, obj = self.run_phase1("--baseline", str(p), "--test-id", "AZ-T01-01")
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(obj["summary"]["REVIEW_REQUIRED"], 1)
            self.assertEqual(obj["azure_live_pass_count"], 0)

    def test_phase1_mismatch_not_authoritative_fail(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "example.json"
            p.write_text(json.dumps({"network": {"data_plane": {"private_only": False}}}))
            proc, obj = self.run_phase1("--baseline", str(p), "--test-id", "AZ-T01-01")
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(obj["summary"]["DIFFERENCE_REVIEW_REQUIRED"], 1)

    def test_phase1_synthetic_or_malformed_baseline_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "example.json"
            for value in ({"_synthetic_fixture": True,
                           "network": {"data_plane": {"private_only": True}}}, [1, 2]):
                p.write_text(json.dumps(value))
                proc, obj = self.run_phase1("--baseline", str(p), "--test-id", "AZ-T01-01")
                self.assertEqual(proc.returncode, 2)
                self.assertEqual(obj["summary"]["NOT_READY"], 1)

    def test_phase1_negative_id_cannot_be_approved_baseline(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "example.json"
            p.write_text("{}")
            proc, obj = self.run_phase1("--baseline", str(p), "--test-id", "AZ-T01-02")
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(obj["result"], "NOT_READY")

    def test_phase2_source_220_ids_and_original_commands(self):
        cases = self.spec2["tests"]
        self.assertEqual(len(cases), 220)
        self.assertEqual({x["id"] for x in cases},
                         {f"AZ-T{s:02}-{n:02}" for s in range(11,21) for n in range(1,23)})
        for item in cases:
            with self.subTest(id=item["id"]):
                self.assertEqual(item["command"], self.published[item["id"]]["command"])
                self.assertIs(item["azure_live_pass"], False)

    def test_phase2_real_source_has_110_synthetic_cases(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/phase2_policy_check.py"),
             "--selftest", "ALL", "--spec", str(SPEC2)],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["synthetic_cases"], 110)
        self.assertEqual(result["selftest_pass"], 110)
        self.assertEqual(result["azure_live_passes"], 0)

    def test_dependency_ledger_reduced_from_original_snapshot(self):
        data = audit(ROOT)
        self.assertFalse(data["errors"], data["errors"])
        self.assertEqual(data["canonical_test_ids"], 1716)
        refs = data["literal_script_reference"]
        self.assertLessEqual(refs["MISSING_SCRIPT_REFERENCE"], 669)
        self.assertLessEqual(data["cases_with_missing_input"], 277)
        self.assertNotIn("scripts/phase1_policy_check.py", data["missing_script_paths"])
        self.assertNotIn("scripts/phase2_policy_check.py", data["missing_script_paths"])
        self.assertNotIn("specs/phase1_policies_110.json", data["missing_input_paths"])
        self.assertNotIn("specs/phase2_220.json", data["missing_input_paths"])
        self.assertEqual(data["release_decision"], "NO_GO")
        self.assertEqual(data["azure_live_passes_verified"], 0)


if __name__ == "__main__":
    unittest.main()
