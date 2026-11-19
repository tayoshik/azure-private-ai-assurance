"""Phase 3 original source, synthetic-predicate and fail-closed IPAM tests."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import phase3_guard as guard
from scripts.audit_catalogue_dependencies import audit

ROOT = Path(__file__).resolve().parents[1]
ENGLISH = ROOT / "specs/phase3_264_en.json"


class Phase3RecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = guard.load_source()
        cls.published = json.loads(ENGLISH.read_text(encoding="utf-8"))

    def run_cli(self, *args):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/phase3_guard.py"), *args],
            cwd=ROOT, capture_output=True, text=True, check=False
        )
        self.assertTrue(result.stdout, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_exact_source_identity_and_264_cases(self):
        self.assertEqual(self.original["schema"], "azure-phase3-264/v1")
        self.assertEqual(len(self.original["tests"]), 264)
        self.assertEqual(len(self.original["controls"]), 132)
        self.assertEqual(self.original["live_azure_successes"], 0)
        self.assertEqual(
            {x["id"] for x in self.original["tests"]},
            {f"AZ-T{step:02}-{n:02}" for step in range(21, 33) for n in range(1, 23)}
        )

    def test_original_and_published_commands_only_four_reviewed_edits(self):
        original = {x["id"]: x for x in self.original["tests"]}
        published = {x["id"]: x for x in self.published["tests"]}
        self.assertEqual(set(original), set(published))
        self.assertEqual(self.published["source_phase3_spec_sha256"], guard.SPEC_SHA256)
        edited = {"AZ-T21-13", "AZ-T29-19", "AZ-T31-01", "AZ-T31-19"}
        changed = {
            tid for tid in original if original[tid]["command"] != published[tid]["command"]
        }
        self.assertEqual(changed, edited)
        self.assertEqual(
            {tid for tid, x in published.items() if x["command_edited_from_source"]},
            edited
        )

    def test_264_frozen_fixture_smokes_and_no_azure_pass(self):
        report = guard.offline_selftest(self.original, "ALL")
        self.assertEqual(report["checked_test_ids"], 264)
        self.assertEqual(report["detector_smoke_pass"], 264)
        self.assertEqual(report["detector_smoke_fail"], 0)
        self.assertEqual(report["azure_live_passes"], 0)
        self.assertEqual(report["release_decision"], "NO_GO")
        code, cli = self.run_cli("--selftest", "ALL")
        self.assertEqual(code, 0)
        self.assertEqual(cli["detector_smoke_pass"], 264)

    def test_individual_negative_id_not_live_acceptance(self):
        code, cli = self.run_cli("--selftest", "AZ-T21-02")
        self.assertEqual(code, 0)
        self.assertEqual(cli["detector_smoke_pass"], 1)
        self.assertEqual(cli["azure_live_passes"], 0)

    def test_unknown_id_and_mutated_source_rejected(self):
        code, cli = self.run_cli("--selftest", "AZ-T99-99")
        self.assertEqual(code, 2)
        self.assertEqual(cli["result"], "NOT_READY")
        with tempfile.TemporaryDirectory() as folder:
            tampered = Path(folder) / "spec.json"
            tampered.write_text(
                (ROOT / "specs/phase3_264.json").read_text().replace(
                    '"schema": "azure-phase3-264/v1"',
                    '"schema": "tampered-source/v1"',
                    1,
                ),
                encoding="utf-8",
            )
            code, cli = self.run_cli("--selftest", "ALL", "--spec", str(tampered))
            self.assertEqual(code, 2)
            self.assertEqual(cli["result"], "NOT_READY")

    def test_bool_int_and_unexpected_types_are_not_equal(self):
        self.assertEqual(guard.evaluate("eq", {"expected": True}, 1), guard.MISMATCH)
        self.assertEqual(guard.evaluate("eq", {"expected": {"x": [True]}},
                                        {"x": [1]}), guard.MISMATCH)
        self.assertEqual(guard.evaluate("minimum", {"expected": 10}, True), guard.MISMATCH)
        self.assertEqual(guard.evaluate("is_true", {}, 1), guard.MISMATCH)
        self.assertEqual(guard.evaluate("maximum", {"expected": 10}, float("nan")), guard.MISMATCH)
        self.assertEqual(guard.evaluate("strange_new_rule", {}, "a"), guard.NOT_READY)

    def test_cidr_good_requires_review_and_exit_two(self):
        code, report = self.run_cli("--cidr-check", "fixtures/ipam_ok.json")
        self.assertEqual(code, 2)
        self.assertEqual(report["result"], "REVIEW_REQUIRED")
        self.assertEqual(report["azure_live_passes"], 0)

    def test_cidr_bad_requires_independent_review_and_exit_two(self):
        code, report = self.run_cli("--cidr-check", "fixtures/ipam_bad.json")
        self.assertEqual(code, 2)
        self.assertEqual(report["result"], "DIFFERENCE_REVIEW_REQUIRED")
        self.assertGreaterEqual(len(report["findings"]), 2)
        self.assertEqual(report["release_decision"], "NO_GO")

    def test_cidr_missing_or_malformed_is_not_ready(self):
        code, report = self.run_cli("--cidr-check", "/definitely/missing/ipam.json")
        self.assertEqual(code, 2)
        self.assertEqual(report["result"], "NOT_READY")
        with tempfile.TemporaryDirectory() as folder:
            f = Path(folder) / "malformed.json"
            f.write_text('{"networks":{"vnet":{"cidrs":["not-a-network"]}}}')
            code, report = self.run_cli("--cidr-check", str(f))
            self.assertEqual(code, 2)
            self.assertEqual(report["result"], "NOT_READY")

    def test_ref_inventory_decreases_without_promoting_live_pass(self):
        report = audit()
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["canonical_test_ids"], 1716)
        self.assertEqual(report["literal_script_reference"]["MISSING_SCRIPT_REFERENCE"], 536)
        self.assertEqual(report["literal_script_reference"]["TRACKED_SCRIPT_REFERENCE"], 463)
        self.assertEqual(report["literal_script_reference"]["NO_DIRECT_SCRIPT_REFERENCE"], 717)
        self.assertEqual(report["cases_with_missing_input"], 145)
        self.assertEqual(report["azure_live_passes_verified"], 0)
        self.assertEqual(report["release_decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
