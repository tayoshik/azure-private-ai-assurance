"""Offline Playwright readiness coverage; file-presence alone never becomes PASS."""
import json
from pathlib import Path
from unittest import mock
import subprocess
import sys
import tempfile
import unittest

from scripts import audit_playwright_readiness as p

ROOT = Path(__file__).resolve().parents[1]


class PlaywrightReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = p.inspect(ROOT)

    def test_all_thirteen_expected_case_ids_and_no_azure_pass(self):
        expected = {
            "AZ-T20-07", "AZ-T20-09", "AZ-T20-15", "AZ-T20-17",
            *(f"AZ-T64-{n:02}" for n in range(1, 18, 2)),
        }
        self.assertEqual(set(p.EXPECTED_REFERENCES), expected)
        self.assertEqual(set(self.report["cases"]), expected)
        self.assertEqual(self.report["case_references_reviewed"], 13)
        self.assertEqual(self.report["canonical_case_ids"], 1716)
        self.assertEqual(self.report["approved_live_azure_passes"], 0)
        self.assertEqual(self.report["release_decision"], "NO_GO")
        self.assertFalse(self.report["errors"])

    def test_all_missing_paths_are_explicitly_blocked(self):
        self.assertEqual(self.report["case_path_missing"], 13)
        self.assertEqual(self.report["case_source_review_required"], 0)
        self.assertEqual(
            {row["state"] for row in self.report["cases"].values()},
            {"SOURCE_MISSING"},
        )
        self.assertTrue(all(
            row["azure_acceptance"] == "NOT_READY"
            for row in self.report["cases"].values()
        ))

    def test_two_distinct_paths_and_real_semantic_requirements(self):
        self.assertEqual(set(p.EXPECTED_REFERENCES.values()), {p.CONFIG, p.SPEC})
        self.assertEqual(sum(path == p.CONFIG for path in p.EXPECTED_REFERENCES.values()), 4)
        self.assertEqual(sum(path == p.SPEC for path in p.EXPECTED_REFERENCES.values()), 9)
        for id_ in ("AZ-T64-05", "AZ-T64-15", "AZ-T64-17", "AZ-T64-03"):
            self.assertTrue(self.report["cases"][id_]["criterion"])

    def test_external_runtime_inputs_not_self_attested_by_repo(self):
        self.assertIn("approved_private_base_url", self.report["independent_prerequisites"])
        self.assertIn("approved_encrypted_test_identity", self.report["independent_prerequisites"])
        self.assertIn("approved_internal_runner", self.report["independent_prerequisites"])
        self.assertIn("approved_external_vantage", self.report["independent_prerequisites"])
        self.assertEqual({v["state"] for v in self.report["independent_prerequisites"].values()},
                         {"UNVERIFIED_EXTERNAL_OWNER_INPUT"})

    def test_empty_placeholder_files_cannot_turn_into_ready(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in (p.CONFIG, p.SPEC):
                dest = root / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text("// empty, unapproved placeholder\n", encoding="utf-8")
            fake = {"errors": [], "canonical_test_ids": 1716, "cases": {
                id_: {"script_refs": [path]} for id_, path in p.EXPECTED_REFERENCES.items()
            }}
            with mock.patch.object(p, "audit", return_value=fake):
                report = p.inspect(root)
            self.assertEqual(report["case_path_missing"], 0)
            self.assertEqual(report["case_source_review_required"], 13)
            self.assertEqual(report["readiness"], "BLOCKED_UNVERIFIED_APP_AND_RUNNERS")
            self.assertEqual(report["approved_live_azure_passes"], 0)
            self.assertEqual(report["release_decision"], "NO_GO")
            self.assertNotIn("READY", {x["state"] for x in report["cases"].values()})

    def test_catalogue_reference_tamper_detected(self):
        fake = {"errors": [], "canonical_test_ids": 1716, "cases": {
            id_: {"script_refs": [path]} for id_, path in p.EXPECTED_REFERENCES.items()
        }}
        fake["cases"]["AZ-T64-15"]["script_refs"] = ["tests/fake.spec.ts"]
        with mock.patch.object(p, "audit", return_value=fake):
            report = p.inspect(ROOT)
        self.assertEqual(report["readiness"], "INVALID_INVENTORY")
        self.assertTrue(any("AZ-T64-15" in err for err in report["errors"]))
        self.assertEqual(report["release_decision"], "NO_GO")

    def test_strict_mode_reports_blocker_and_exits_two(self):
        process = subprocess.run(
            [sys.executable, str(ROOT / "scripts/audit_playwright_readiness.py"), "--strict"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(process.returncode, 2, process.stderr)
        report = json.loads(process.stdout)
        self.assertEqual(report["case_path_missing"], 13)
        self.assertEqual(report["release_decision"], "NO_GO")

    def test_read_only_inventory_mode_succeeds_without_claiming_pass(self):
        process = subprocess.run(
            [sys.executable, str(ROOT / "scripts/audit_playwright_readiness.py")],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        report = json.loads(process.stdout)
        self.assertEqual(report["readiness"], "BLOCKED_UNVERIFIED_APP_AND_RUNNERS")
        self.assertEqual(report["approved_live_azure_passes"], 0)


if __name__ == "__main__":
    unittest.main()
