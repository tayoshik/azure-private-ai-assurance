"""Phase 4 recovered original source integrity. Offline-only, no Azure calls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import phase4_guard as guard

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "specs/phase4_286.json"
ENGLISH = ROOT / "specs/phase4_286_en.json"
PIN = "b221babf4a1b7a17763723d06229e868b943748cbbf6c1b0726e8f07465fcf36"


class Phase4PrimarySourceTests(unittest.TestCase):
    def test_source_digest_and_143_286_identity(self):
        raw = SOURCE.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), PIN)
        controls, tests = guard.load_source(SOURCE)
        self.assertEqual(len(controls), 143)
        self.assertEqual(len(tests), 286)
        self.assertEqual(set(tests), guard.EXPECTED)

    def test_english_37_edits_only_and_no_false_live_pass(self):
        original = json.loads(SOURCE.read_text(encoding="utf-8"))
        english = json.loads(ENGLISH.read_text(encoding="utf-8"))
        published = {x["id"]: x for x in english["tests"]}
        src = {x["id"]: x for x in original["tests"]}
        self.assertEqual(english["source_spec_sha256"], PIN)
        self.assertEqual(original["live_azure_successes"], 0)
        self.assertEqual(english["azure_live_pass_count"], 0)
        self.assertEqual(set(src), guard.EXPECTED)
        differences = {k for k in src if src[k]["command"] != published[k]["command"]}
        documented = {x["id"] for x in english["command_edits"]}
        self.assertEqual(differences, documented)
        self.assertEqual(len(differences), 37)

    def test_all_286_primary_source_synthetic_cases_pass(self):
        controls, cases = guard.load_source(SOURCE)
        output, code = guard.selftest(controls, cases, "ALL")
        self.assertEqual(code, 0, output)
        self.assertEqual(output["case_labels_tested"], 286)
        self.assertEqual(output["synthetic_checks_succeeded"], 286)
        self.assertEqual(output["azure_live_passes"], 0)
        self.assertEqual(output["release_decision"], "NO_GO")

    def test_malformed_or_tampered_primary_source_rejected(self):
        original = json.loads(SOURCE.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "tampered.json"
            for tamper in ("duplicate", "fictitious_pass", "incomplete"):
                spec = json.loads(json.dumps(original))
                if tamper == "duplicate":
                    spec["tests"][0]["id"] = spec["tests"][1]["id"]
                elif tamper == "fictitious_pass":
                    spec["live_azure_successes"] = 1
                else:
                    spec["controls"].pop()
                p.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
                with self.subTest(tamper=tamper):
                    with self.assertRaises(ValueError):
                        guard.load_source(p)

    def test_untrusted_observation_is_review_only_and_exit_2(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "observation.json"
            p.write_text(json.dumps({
                "source": "operator-supplied-unsigned",
                "resource_id": "/subscriptions/placeholder",
                "collected_at_utc": "2026-11-19T00:00:00Z",
                "baseline_id": "not-independently-approved",
                "reviewer": "untrusted-operator",
                "observation": "OpenAI"
            }), encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts/phase4_guard.py"),
                "--evaluate", "AZ-T33-01", "--spec", str(SOURCE),
                "--observation", str(p)
            ], capture_output=True, text=True, cwd=ROOT, check=False)
            self.assertEqual(result.returncode, 2)
            response = json.loads(result.stdout)
            self.assertEqual(response["result"], "REVIEW_REQUIRED")
            self.assertEqual(response["azure_live_passes"], 0)
            self.assertEqual(response["release_decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
