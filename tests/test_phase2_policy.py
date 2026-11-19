"""Phase 2 safety tests. A local minimal spec fixture is NOT canonical evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import phase2_policy_check as p

ROOT = Path(__file__).resolve().parents[1]


class Phase2GuardTests(unittest.TestCase):
    def test_expected_ids(self):
        self.assertEqual(len(p.EXPECTED), 220)
        self.assertEqual(sum(int(x[-2:]) % 2 == 0 for x in p.EXPECTED), 110)

    def test_typed_comparisons(self):
        self.assertEqual(p.compare(True, 1), "MISMATCH")
        self.assertEqual(p.compare({"value": [True]}, {"value": [1]}), "MISMATCH")
        self.assertEqual(p.compare({"a": 1}, {"a": 1}), "MATCH")
        self.assertEqual(p.compare(None, 0), "NOT_READY")
        self.assertEqual(p.compare(float("nan"), float("nan")), "MISMATCH")

    def test_synthetic_checks_are_not_live_pass(self):
        for i in sorted(x for x in p.EXPECTED if int(x[-2:]) % 2 == 0):
            result = p.selftest(i)
            self.assertEqual(result["status"], "SELFTEST_PASS", i)
            self.assertFalse(result["azure_live_pass"])

    def test_untrusted_fixture_rejected(self):
        item = dict(asset_id="asset", collector="collector", collected_at="2026-11-19T00:00:00Z",
                    source_sha256="0"*64, baseline_sha256="1"*64, authorization_ticket="ticket",
                    fixture=True, observed=True, approved=True)
        self.assertEqual(p.triage(item)[0], "NOT_READY")

    def test_forged_equality_is_review_only(self):
        item = dict(asset_id="asset", collector="collector", collected_at="2026-11-19T00:00:00Z",
                    source_sha256="0"*64, baseline_sha256="1"*64, authorization_ticket="ticket",
                    fixture=False, observed=True, approved=True)
        self.assertEqual(p.triage(item)[0], "REVIEW_REQUIRED")
        self.assertEqual(p.triage({**item, "observed": False})[0], "DIFFERENCE_REVIEW_REQUIRED")

    def test_unpinned_evidence_rejected(self):
        item = dict(asset_id="asset", collector="collector", collected_at="no time",
                    source_sha256="0"*64, baseline_sha256="1"*64, authorization_ticket="ticket",
                    fixture=False, observed=True, approved=True)
        self.assertEqual(p.triage(item)[0], "NOT_READY")

    def make_synthetic_spec(self, folder):
        path = Path(folder) / "test-only-phase2.json"
        path.write_text(json.dumps({"tests": [
            {"id": x, "step": int(x[4:6]), "command": "echo synthetic-fixture-only",
             "azure_live_pass": False}
            for x in sorted(p.EXPECTED)
        ]}), encoding="utf-8")
        return path

    def test_structural_spec_validation_with_fixture(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.make_synthetic_spec(folder)
            self.assertEqual(len(p.load_spec(path)["tests"]), 220)
            data = json.loads(path.read_text())
            data["tests"][0]["azure_live_pass"] = True
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                p.load_spec(path)

    def test_offline_cli_all_110_fixture_only(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.make_synthetic_spec(folder)
            result = subprocess.run([sys.executable, str(ROOT/"scripts/phase2_policy_check.py"),
                                     "--selftest", "ALL", "--spec", str(path)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            response = json.loads(result.stdout)
            self.assertEqual(response["selftest_pass"], 110)
            self.assertEqual(response["azure_live_passes"], 0)

    def test_check_never_exit_zero(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.make_synthetic_spec(folder)
            evidence = Path(folder) / "untrusted-evidence.json"
            evidence.write_text(json.dumps({
                "asset_id": "asset", "collector": "c", "collected_at": "2026-11-19T00:00:00Z",
                "source_sha256": "0"*64, "baseline_sha256": "1"*64,
                "authorization_ticket": "ticket", "fixture": False,
                "observed": "x", "approved": "x",
            }), encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT/"scripts/phase2_policy_check.py"),
                                     "--check", "AZ-T11-01", "--spec", str(path),
                                     "--evidence", str(evidence)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["result"], "REVIEW_REQUIRED")

    def test_missing_real_source_is_not_ready(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, str(ROOT/"scripts/phase2_policy_check.py"),
                                     "--selftest", "ALL", "--spec",
                                     str(Path(folder)/"missing-canonical-source.json")],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["result"], "NOT_READY")


if __name__ == "__main__":
    unittest.main()
