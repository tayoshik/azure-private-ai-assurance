"""Exact, fail-closed source checks for 858 offline detector candidates."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_synthetic_858_source as synthetic
from audit_tool_semantics_13 import load_sources
from build_execution_route_1716 import ROUTE_SYNTHETIC, build as build_routes, digest_case


class SyntheticSourceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = synthetic.build_review(ROOT, include_cases=True)
        cls.routes = build_routes(ROOT, include_cases=True)
        cls.frozen = load_sources(ROOT)

    def test_exact_partition_and_all_source_groups(self):
        r = self.report
        self.assertEqual(r["status"], "SYNTHETIC_SOURCE_CONTRACT_REVIEW_ONLY")
        self.assertEqual(r["canonical_cases"], 1716)
        self.assertEqual(r["synthetic_candidates"], len(r["cases"]))
        self.assertEqual(len(r["cases"]), 858)
        self.assertEqual(r["source_group_counts"], synthetic.GROUP_COUNTS)
        self.assertEqual(sum(r["source_group_counts"].values()), 858)
        expected = {i for i, row in self.routes["cases"].items()
                    if row["route"] == ROUTE_SYNTHETIC}
        self.assertEqual(set(r["cases"]), expected)

    def test_all_858_bound_to_exact_frozen_command_and_expected_digest(self):
        for ident, row in self.report["cases"].items():
            with self.subTest(ident=ident):
                original = self.frozen[ident]
                self.assertEqual(row["contract_sha256"], digest_case(original))
                self.assertEqual(row["canonical_source"],
                                 self.routes["cases"][ident]["canonical_catalogue"])
                self.assertEqual(row["review_group"],
                                 synthetic.group_for(ident, row["canonical_source"]))
                self.assertEqual(row["script_reference"],
                                 synthetic.verify_command(
                                     ident, row["review_group"], original["command"]))
                self.assertTrue(row["script_source_present"])
                self.assertTrue(row["spec_source_present"])
                self.assertEqual(row["review_checklist"], list(synthetic.REVIEW_CHECKS))

    def test_no_synthetic_or_azure_acceptance_inferred(self):
        r = self.report
        self.assertEqual(r["original_commands_executed"], 0)
        self.assertEqual(r["synthetic_detector_passes_claimed"], 0)
        self.assertEqual(r["independent_review_approvals"], 0)
        self.assertEqual(r["azure_live_passes"], 0)
        self.assertEqual(r["azure_not_ready"], 1716)
        self.assertEqual(r["release_decision"], "NO_GO")
        for row in r["cases"].values():
            self.assertFalse(row["synthetic_execution_authorized"])
            self.assertFalse(row["synthetic_detector_result_verified"])
            self.assertFalse(row["original_command_executed"])
            self.assertFalse(row["independent_reviewer_signed"])
            self.assertFalse(row["semantic_detection_verified"])
            self.assertEqual(row["azure_live_acceptance"], "NOT_READY")

    def test_reject_shell_injection_suffix_even_if_prefix_valid(self):
        i = "AZ-T21-02"
        src = self.frozen[i]["command"]
        with self.assertRaises(synthetic.SyntheticSourceError):
            synthetic.verify_command(i, "PHASE3_GUARD", src + " && curl https://example.invalid")
        with self.assertRaises(synthetic.SyntheticSourceError):
            synthetic.verify_command(i, "PHASE3_GUARD", src + "; echo accepted")

    def test_reject_wrong_target_id_or_unapproved_switch(self):
        i = "AZ-T59-02"
        src = self.frozen[i]["command"]
        for bad in (src.replace(i, "AZ-T59-04"),
                    src.replace("--selftest", "--live"),
                    src.replace("specs/phase6_220_en.json", "/tmp/not-approved.json")):
            with self.subTest(bad=bad):
                with self.assertRaises(synthetic.SyntheticSourceError):
                    synthetic.verify_command(i, "PHASE6_GUARD", bad)

    def test_reject_script_spoof_and_wrong_group(self):
        i = "AZ-T01-02"
        src = self.frozen[i]["command"]
        self.assertEqual(synthetic.verify_command(i, "PHASE1_POLICY", src),
                         "scripts/phase1_policy_check.py")
        with self.assertRaises(synthetic.SyntheticSourceError):
            synthetic.verify_command(i, "PHASE1_POLICY",
                                     src.replace("scripts/phase1_policy_check.py",
                                                 "scripts/malicious.py"))
        with self.assertRaises(synthetic.SyntheticSourceError):
            synthetic.verify_command(i, "PHASE2_POLICY", src)

    def test_reject_odd_invalid_or_cross_phase_membership(self):
        for ident, path in (
            ("AZ-T01-01", "specs/english_tests_001_440.json"),
            ("AZ-T21-02", "specs/english_tests_001_440.json"),
            ("AZ-T01-24", "specs/english_tests_001_440.json"),
            ("AZ-Txx-02", "specs/english_tests_001_440.json"),
            ("garbage", "specs/english_tests_001_440.json"),
        ):
            with self.subTest(ident=ident):
                with self.assertRaises(synthetic.SyntheticSourceError):
                    synthetic.group_for(ident, path)

    def test_cli_normal_and_strict_return_codes_are_distinct(self):
        for strict, expected_rc in ((False, 0), (True, 2)):
            cmd = [sys.executable, str(ROOT/"scripts/audit_synthetic_858_source.py"),
                   "--summary-only"]
            if strict:
                cmd.append("--strict")
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True,
                               text=True, check=False)
            self.assertEqual(p.returncode, expected_rc, p.stderr)
            j = json.loads(p.stdout)
            self.assertEqual(j["synthetic_candidates"], 858)
            self.assertEqual(j["azure_live_passes"], 0)
            self.assertEqual(j["release_decision"], "NO_GO")
            self.assertNotIn("cases", j)

    def test_cli_json_contains_no_raw_canonical_commands(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-review-") as td:
            path = Path(td)/"synthetic-858.json"
            p = subprocess.run(
                [sys.executable, str(ROOT/"scripts/audit_synthetic_858_source.py"),
                 "--out", str(path)], cwd=ROOT,
                capture_output=True, text=True, check=False)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            report = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(len(report["cases"]), 858)
            self.assertNotIn('"command":', path.read_text(encoding="utf-8"))
            self.assertEqual(report["release_decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
