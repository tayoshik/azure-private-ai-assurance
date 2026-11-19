"""Offline Phase 4 guard safety tests. Synthetic fixture is not canonical source."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import phase4_guard as g

ROOT = Path(__file__).resolve().parents[1]


def synthetic_phase4():
    controls, tests = [], []
    for step in range(33, 46):
        for slot in range(1, 23, 2):
            ident = f"AZ-T{step:02}-{slot:02}"
            controls.append({
                "control_id": ident, "step": step,
                "rule_type": "is_true", "rule_args": {},
                "good_fixture": True, "bad_fixture": False,
            })
            for case_slot in (slot, slot + 1):
                tests.append({
                    "id": f"AZ-T{step:02}-{case_slot:02}",
                    "step": str(step), "status": "未実行",
                    "command": "synthetic offline fixture only",
                    "expected": "fixture has intended result",
                    "evidence": "synthetic input",
                    "procedure": "do not use for real Azure acceptance",
                })
    return {"schema": "azure-phase4-286/v1", "controls": controls,
            "tests": tests, "live_azure_successes": 0}


class Phase4FailClosedTests(unittest.TestCase):
    def test_source_missing_or_invalid_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                g.load_source(Path(d) / "missing.json")
            fixture = synthetic_phase4()
            fixture["live_azure_successes"] = 1
            p = Path(d) / "invalid.json"
            p.write_text(json.dumps(fixture), encoding="utf-8")
            with self.assertRaises(ValueError):
                g.load_source(p)

    def test_all_286_synthetic_ids_only(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "synthetic-only.json"
            p.write_text(json.dumps(synthetic_phase4()))
            controls, cases = g.load_source(p)
            self.assertEqual(len(controls), 143)
            self.assertEqual(len(cases), 286)
            result, status = g.selftest(controls, cases, "ALL")
            self.assertEqual(status, 0, result)
            self.assertEqual(result["case_labels_tested"], 286)
            self.assertEqual(result["synthetic_checks_succeeded"], 286)
            self.assertEqual(result["azure_live_passes"], 0)
            self.assertEqual(result["release_decision"], "NO_GO")

    def test_duplicate_control_and_wrong_case_id_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.json"
            for mutation in ("duplicate", "bad_id", "missing"):
                spec = synthetic_phase4()
                if mutation == "duplicate":
                    spec["controls"][1]["control_id"] = spec["controls"][0]["control_id"]
                elif mutation == "bad_id":
                    spec["tests"][0]["id"] = "AZ-T99-99"
                else:
                    spec["tests"].pop()
                p.write_text(json.dumps(spec))
                with self.assertRaises(ValueError, msg=mutation):
                    g.load_source(p)

    def test_predicates_use_strict_types_and_missing_is_unknown(self):
        self.assertEqual(g.verdict("eq", {"expected": True}, 1), "MISMATCH")
        self.assertEqual(g.verdict("eq", {"expected": {"flag": True}}, {"flag": 1}), "MISMATCH")
        self.assertEqual(g.verdict("eq", {"expected": [1, [True]]}, [1, [1]]), "MISMATCH")
        self.assertEqual(g.verdict("eq", {"expected": float("nan")}, float("nan")), "MISMATCH")
        self.assertEqual(g.verdict("eq", {"expected": "OpenAI"}, "OpenAI"), "MATCH")
        self.assertEqual(g.verdict("eq", {"expected": "OpenAI"}, "Other"), "MISMATCH")
        self.assertEqual(g.verdict("is_true", {}, True), "MATCH")
        self.assertEqual(g.verdict("is_false", {}, False), "MATCH")
        self.assertEqual(g.verdict("minimum", {"expected": 2}, True), "NOT_READY")
        self.assertEqual(g.verdict("minimum", {"expected": 2}, float("nan")), "NOT_READY")
        self.assertEqual(g.verdict("nonempty", {}, []), "MISMATCH")
        self.assertEqual(g.verdict("private_ip", {"subnet": "10.0.0.0/24"}, "10.0.0.5"), "MATCH")
        self.assertEqual(g.verdict("private_ip", {"subnet": "10.0.0.0/24"}, "8.8.8.8"), "MISMATCH")
        self.assertEqual(g.verdict("private_ip", {"subnet": "10.0.0.0/24"}, "bad-address"), "NOT_READY")
        self.assertEqual(g.verdict("eq", {"expected": 1}, None), "NOT_READY")
        self.assertEqual(g.verdict("unknown", {}, 5), "NOT_READY")

    def test_observation_never_issues_live_pass(self):
        controls, cases = g.load_source(self._write_temp_source())
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "observation.json"
            record = {
                "source": "unsigned-json", "resource_id": "/subscriptions/fake",
                "collected_at_utc": "2026-11-19T00:00:00Z",
                "baseline_id": "review-only", "reviewer": "unit-tester",
                "observation": True,
            }
            for val, expected in ((True, "REVIEW_REQUIRED"),
                                  (False, "DIFFERENCE_REVIEW_REQUIRED")):
                record["observation"] = val
                p.write_text(json.dumps(record))
                output, code = g.review_observation(controls, "AZ-T33-01", p)
                self.assertEqual(code, 2)
                self.assertEqual(output["result"], expected)
            record["source"] = "synthetic-fixture"
            p.write_text(json.dumps(record))
            output, code = g.review_observation(controls, "AZ-T33-01", p)
            self.assertEqual(code, 2)
            self.assertEqual(output["result"], "NOT_READY")

    def _write_temp_source(self):
        # Independently construct a test-only fixture; it never replaces
        # the 600,202-byte frozen Japanese source in the release process.
        if not hasattr(self, "_fixtures"):
            self._fixtures = tempfile.TemporaryDirectory()
            self.addCleanup(self._fixtures.cleanup)
        p = Path(self._fixtures.name) / "fixture.json"
        p.write_text(json.dumps(synthetic_phase4()))
        return p

    def test_cli_rejects_missing_source(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "missing-source.json"
            run = subprocess.run([
                sys.executable, str(ROOT / "scripts/phase4_guard.py"),
                "--selftest", "ALL", "--spec", str(p)
            ], cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(json.loads(run.stdout)["result"], "NOT_READY")

    def test_published_english_source_remains_not_approved(self):
        e = json.loads((ROOT / "specs/phase4_286_en.json").read_text())
        self.assertEqual(e["total"], 286)
        self.assertEqual(e["azure_live_pass_count"], 0)
        self.assertEqual(sum(bool(x["synthetic_only"]) for x in e["tests"]), 143)
        self.assertEqual({x["id"] for x in e["tests"]}, g.EXPECTED)


if __name__ == "__main__":
    unittest.main()
