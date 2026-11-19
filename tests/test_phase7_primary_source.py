"""Phase 7 original SHA, 220 offline fixtures, plan triage and 1716 references.

No fixture or unsigned observation is evidence of deployed Azure acceptance.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import phase7_guard as g
from scripts import phase7_plan_policy as plan
from scripts.audit_catalogue_dependencies import audit
from scripts.release_gate import decide

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FIXTURES = {
    "plan_app_pna_true.json": "031237e2a65ce3f3b565dd2a20e4a1befb91c1661ba27606b65d18eaeadf028f",
    "plan_nsg_any.json": "3ecf5a685feef279a2aaf53302fb9bb160c835efbb1b72816d9614ebe5d9a1fe",
    "plan_safe.json": "5d7f77d66b6e667a0c69208bd793656db1521bc5e6dd35dd473f266a6b7f3653",
}


class Phase7SourceSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controls, cls.cases = g.load_original()
        cls.translation = g.published_translation()

    def test_source_pin_and_complete_case_coverage(self):
        self.assertEqual(hashlib.sha256(g.SOURCE.read_bytes()).hexdigest(), g.SOURCE_SHA256)
        self.assertEqual(len(self.controls), 110)
        self.assertEqual(len(self.cases), 220)
        self.assertEqual(set(self.controls), g.CONTROL_IDS)
        self.assertEqual(set(self.cases), g.EXPECTED)
        self.assertEqual(g.SOURCE_SHA256,
                         self.translation["source"]["original_spec_sha256"])
        doc = json.loads(g.SOURCE.read_text(encoding="utf-8"))
        self.assertEqual(doc["prior_phase6_spec_sha256"], g.PHASE6_SHA256)
        self.assertFalse(doc["source_code_found"])
        self.assertEqual(doc["live_azure_tests_passed"], 0)
        self.assertEqual(self.translation["azure_live_passes"], 0)

    def test_110_documented_translation_command_changes(self):
        published = {row["id"]: row for row in self.translation["tests"]}
        self.assertEqual(set(published), g.EXPECTED)
        changed = {i for i in g.EXPECTED if self.cases[i]["command"] != published[i]["command"]}
        expected = {i for i in g.EXPECTED if int(i[-2:]) % 2 == 0}
        self.assertEqual(changed, expected)
        for ident in expected:
            self.assertIn("--spec specs/phase7_220_en.json", published[ident]["command"])

    def test_all_220_original_synthetic_labels_and_no_live_pass(self):
        out, code = g.synthetic_check(self.controls, "ALL")
        self.assertEqual(code, 0, out)
        self.assertEqual(out["case_labels_tested"], 220)
        self.assertEqual(out["synthetic_checks_succeeded"], 220)
        self.assertEqual(out["azure_live_passes"], 0)
        self.assertEqual(out["release_decision"], "NO_GO")

    def test_all_individual_odd_even_and_unknown_ids(self):
        for ident in sorted(g.EXPECTED):
            with self.subTest(ident=ident):
                out, status = g.synthetic_check(self.controls, ident)
                self.assertEqual(status, 0, out)
                self.assertEqual(out["case_labels_tested"], 1)
        for invalid in ("AZ-T68-22", "AZ-T79-01", "AZ-T70-00"):
            self.assertEqual(g.synthetic_check(self.controls, invalid)[1], 2)

    def test_strict_typed_predicates_and_missing_values(self):
        self.assertEqual(g.predicate("eq", {"expected": True}, 1), "MISMATCH")
        self.assertEqual(g.predicate("eq", {"expected": 403}, 403), "MATCH")
        self.assertEqual(g.predicate("eq", {"expected": 403}, "403"), "MISMATCH")
        self.assertEqual(g.predicate("is_true", {}, True), "MATCH")
        self.assertEqual(g.predicate("is_true", {}, None), "NOT_READY")
        self.assertEqual(g.predicate("eq", {"expected": 403}, None), "NOT_READY")

    def test_translation_cli_resolves_original_not_english_fixture(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT/"scripts/phase7_guard.py"), "--selftest",
             "AZ-T69-02", "--spec", "specs/phase7_220_en.json"],
            cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["synthetic_checks_succeeded"], 1)
        self.assertEqual(out["azure_live_passes"], 0)

    def test_tampered_source_never_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            changed = Path(d)/"altered.json"
            changed.write_text(json.dumps({"schema": "azure-phase7-220/v1"}))
            with self.assertRaises(ValueError):
                g.load_original(changed)
            proc = subprocess.run(
                [sys.executable, str(ROOT/"scripts/phase7_guard.py"), "--selftest",
                 "ALL", "--spec", str(changed)],
                cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(json.loads(proc.stdout)["result"], "NOT_READY")

    def test_unsigned_matching_and_mismatch_observations_are_review_only(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"sample.json"
            obs = {"source": "untrusted-local", "resource_id": "example",
                   "collected_at_utc": "2026-11-19T00:00:00Z",
                   "baseline_id": "unsigned", "reviewer": "local",
                   "fixture": False, "observation": True}
            path.write_text(json.dumps(obs))
            matched, status = g.review_observation(self.controls, "AZ-T69-01", path)
            self.assertEqual(status, 2)
            self.assertEqual(matched["result"], "REVIEW_REQUIRED")
            obs["observation"] = False
            path.write_text(json.dumps(obs))
            mismatched, status = g.review_observation(self.controls, "AZ-T69-01", path)
            self.assertEqual(status, 2)
            self.assertEqual(mismatched["result"], "DIFFERENCE_REVIEW_REQUIRED")
            obs["synthetic"] = True
            path.write_text(json.dumps(obs))
            refused, status = g.review_observation(self.controls, "AZ-T69-01", path)
            self.assertEqual(status, 2)
            self.assertEqual(refused["result"], "NOT_READY")

    def test_original_terraform_fixtures_are_sha_pinned(self):
        for name, expected_hash in EXPECTED_FIXTURES.items():
            content = (ROOT/"fixtures"/name).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), expected_hash)
            self.assertIsInstance(json.loads(content), dict)

    def test_plan_selftest_3_and_no_acceptance(self):
        result, code = plan.synthetic_tests()
        self.assertEqual(code, 0, result)
        self.assertEqual(result["synthetic_cases"], 3)
        self.assertEqual(result["selftest_pass"], 3)
        self.assertEqual(result["azure_live_passes"], 0)
        self.assertEqual(result["release_decision"], "NO_GO")

    def test_real_plan_exit_never_zero_even_when_expect_matches(self):
        for file_name, expected in (
                ("plan_app_pna_true.json", "DIFFERENCE_REVIEW_REQUIRED"),
                ("plan_nsg_any.json", "DIFFERENCE_REVIEW_REQUIRED"),
                ("plan_safe.json", "REVIEW_REQUIRED")):
            source = ROOT/"fixtures"/file_name
            state, _ = plan.inspect(json.loads(source.read_text(encoding="utf-8")))
            self.assertEqual(state, expected)
            for expected_arg in ("Pass", "Fail", "NotReady"):
                proc = subprocess.run(
                    [sys.executable, str(ROOT/"scripts/phase7_plan_policy.py"),
                     "--plan", str(source), "--expect", expected_arg],
                    cwd=ROOT, capture_output=True, text=True, check=False)
                self.assertEqual(proc.returncode, 2)
                out = json.loads(proc.stdout)
                self.assertEqual(out["classification"], expected)
                self.assertEqual(out["azure_live_passes"], 0)

    def test_incomplete_plan_does_not_get_a_success(self):
        for candidate in (
                {}, {"planned_values": {}, "resource_changes": []},
                {"planned_values": {}, "resource_changes": [{}]},
                {"planned_values": {}, "resource_changes": [
                    {"type": "unknown_type", "change": {"actions": ["create"], "after": {}}}]},
                {"planned_values": {}, "resource_changes": [
                    {"type": "azurerm_linux_web_app", "change": {"actions": ["create"], "after": {}}}]}):
            self.assertEqual(plan.inspect(candidate)[0], "NOT_READY")
        self.assertEqual(plan.inspect({"resource_changes": []})[0], "NOT_READY")

    def test_1716_catalogue_13_missing_code_and_zero_missing_input(self):
        result = audit(ROOT)
        self.assertFalse(result["errors"], result["errors"])
        self.assertEqual(result["canonical_test_ids"], 1716)
        self.assertEqual(result["literal_script_reference"]["MISSING_SCRIPT_REFERENCE"], 13)
        self.assertEqual(result["literal_script_reference"]["TRACKED_SCRIPT_REFERENCE"], 986)
        self.assertEqual(result["literal_script_reference"]["NO_DIRECT_SCRIPT_REFERENCE"], 717)
        self.assertEqual(result["cases_with_missing_input"], 0)
        self.assertNotIn("scripts/phase7_guard.py", result["missing_script_paths"])
        self.assertNotIn("scripts/phase7_plan_policy.py", result["missing_script_paths"])
        self.assertNotIn("fixtures/plan_app_pna_true.json", result["missing_input_paths"])
        self.assertNotIn("fixtures/plan_nsg_any.json", result["missing_input_paths"])
        self.assertEqual(result["release_decision"], "NO_GO")
        self.assertEqual(result["azure_live_passes_verified"], 0)

    def test_release_refuses_even_after_113_path_repairs(self):
        result = decide(ROOT)
        self.assertEqual(result["decision"], "NO_GO")
        self.assertEqual(result["verified_live_azure_passes"], 0)
        self.assertEqual(result["dependency_unresolved_ids"], 13)


if __name__ == "__main__":
    unittest.main()
