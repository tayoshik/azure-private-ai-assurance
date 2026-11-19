"""Phase 6 frozen-source, synthetic detector and fail-closed classifier tests.

All statuses under test are OFFLINE; none are Azure live acceptance.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest

from scripts import phase6_guard as guard
from scripts import phase6_result_classifier as classifier
from scripts.audit_catalogue_dependencies import audit

ROOT = Path(__file__).resolve().parents[1]


class Phase6RecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controls, cls.cases = guard.load_original()
        cls.translation = guard.published_translation()
        cls.source = json.loads(guard.SOURCE.read_text(encoding="utf-8"))

    def test_frozen_source_digest_and_canonical_case_ids(self):
        self.assertEqual(hashlib.sha256(guard.SOURCE.read_bytes()).hexdigest(), guard.SOURCE_SHA256)
        self.assertEqual(len(self.controls), 110)
        self.assertEqual(len(self.cases), 220)
        self.assertEqual(set(self.controls), guard.CONTROL_IDS)
        self.assertEqual(set(self.cases), guard.EXPECTED)
        self.assertEqual(self.source["live_azure_tests_passed"], 0)
        self.assertEqual(self.source["prior_phase5_spec_sha256"], guard.PHASE5_SHA256)

    def test_translation_references_exact_frozen_source(self):
        en = self.translation
        self.assertEqual(en["source"]["original_spec_sha256"], guard.SOURCE_SHA256)
        en_cases = {r["id"]: r for r in en["tests"]}
        self.assertEqual(len(en_cases), 220)
        differences = {i for i in self.cases if self.cases[i]["command"] != en_cases[i]["command"]}
        expected = {i for i in guard.EXPECTED if int(i[-2:]) % 2 == 0}
        self.assertEqual(differences, expected)
        self.assertTrue(all(en_cases[i]["command"].endswith("specs/phase6_220_en.json")
                            for i in expected))
        self.assertEqual(en["azure_live_passes"], 0)

    def test_220_synthetic_cases_but_no_azure_acceptance(self):
        report, status = guard.synthetic_check(self.controls, "ALL")
        self.assertEqual(status, 0, report)
        self.assertEqual(report["case_labels_tested"], 220)
        self.assertEqual(report["synthetic_checks_succeeded"], 220)
        self.assertEqual(report["azure_live_passes"], 0)
        self.assertEqual(report["release_decision"], "NO_GO")

    def test_legacy_english_command_uses_pinned_japanese_source(self):
        p = subprocess.run(
            [sys.executable, str(ROOT/"scripts/phase6_guard.py"),
             "--selftest", "AZ-T59-02", "--spec", "specs/phase6_220_en.json"],
            cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, 0, p.stderr)
        o = json.loads(p.stdout)
        self.assertEqual(o["synthetic_checks_succeeded"], 1)
        self.assertEqual(o["azure_live_passes"], 0)

    def test_true_one_is_not_typed_equality(self):
        self.assertEqual(guard.predicate("eq", {"expected": True}, 1), "MISMATCH")
        self.assertEqual(guard.predicate("eq", {"expected": {"a": [True]}}, {"a": [1]}), "MISMATCH")
        self.assertEqual(guard.predicate("eq", {"expected": 0}, 0), "MATCH")
        self.assertEqual(guard.predicate("eq", {"expected": 0}, None), "NOT_READY")
        self.assertEqual(guard.predicate("private_ip", {"subnet": "10.1.0.0/16"}, "8.8.8.8"), "MISMATCH")
        self.assertEqual(guard.predicate("private_ip", {"subnet": "10.1.0.0/16"}, "bad_ip"), "NOT_READY")

    def test_unsigned_matching_observation_is_review_only_exit_2(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "observation.json"
            data = {
                "source": "locally-uploaded-untrusted", "resource_id": "/fake/resource",
                "collected_at_utc": "2026-11-19T00:00:00Z", "baseline_id": "unapproved",
                "reviewer": "local", "fixture": False, "observation": 0
            }
            path.write_text(json.dumps(data))
            o,code = guard.review_observation(self.controls, "AZ-T59-01", path)
            self.assertEqual(code, 2)
            self.assertEqual(o["result"], "REVIEW_REQUIRED")
            data["observation"] = 1
            path.write_text(json.dumps(data))
            o,code = guard.review_observation(self.controls, "AZ-T59-01", path)
            self.assertEqual(code, 2)
            self.assertEqual(o["result"], "DIFFERENCE_REVIEW_REQUIRED")
            data["fixture"] = True
            path.write_text(json.dumps(data))
            o,code = guard.review_observation(self.controls, "AZ-T59-01", path)
            self.assertEqual(code, 2)
            self.assertEqual(o["result"], "NOT_READY")
            o,code = guard.review_observation(self.controls, "AZ-T59-02", path)
            self.assertEqual(code, 2)
            self.assertEqual(o["result"], "NOT_READY")

    def test_tampered_or_missing_primary_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fake-source.json"
            path.write_text(json.dumps(self.source), encoding="utf-8")
            with self.assertRaises(ValueError):
                guard.load_original(path)
            p = subprocess.run([sys.executable, str(ROOT/"scripts/phase6_guard.py"),
                                "--selftest", "ALL", "--spec", str(path)],
                               capture_output=True, text=True, check=False)
            self.assertEqual(p.returncode, 2)
            self.assertEqual(json.loads(p.stdout)["result"], "NOT_READY")

    def test_classifier_blocks_negative_transport_as_proof_of_isolation(self):
        for outcome in ("http_403", "timeout", "nxdomain", "connection_refused", "tls_error"):
            r = dict(asset_exists=True, baseline_approved=True,
                     evidence_present=True, observation=outcome)
            self.assertEqual(classifier.classify(r), "NOT_READY", outcome)
        for outcome in ("unexpected_public_ip", "unauthorized_http_200"):
            r = dict(asset_exists=True, baseline_approved=True,
                     evidence_present=True, observation=outcome)
            self.assertEqual(classifier.classify(r), "DIFFERENCE_REVIEW_REQUIRED")
        r = dict(asset_exists=True, baseline_approved=True, evidence_present=True,
                 observation="denied_with_control_plane", control_plane_private_confirmed=True,
                 external_network_confirmed=True, resource_id="/fake", collected_at_utc="now")
        self.assertEqual(classifier.classify(r), "REVIEW_REQUIRED")
        self.assertEqual(classifier.classify({**r, "source": "SYNTHETIC"}), "NOT_READY")
        self.assertEqual(classifier.classify({**r, "asset_exists": 1}), "NOT_READY")
        self.assertEqual(classifier.classify({**r, "control_plane_private_confirmed": 1}), "NOT_READY")

    def test_classifier_synthetic_selftest_and_observation_never_exit_zero(self):
        p = subprocess.run([sys.executable, str(ROOT/"scripts/phase6_result_classifier.py"),
                            "--selftest"], capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, 0, p.stderr)
        j = json.loads(p.stdout)
        self.assertEqual(j["synthetic_cases"], 10)
        self.assertEqual(j["azure_live_passes"], 0)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "input.json"
            path.write_text(json.dumps({"asset_exists": True, "baseline_approved": True,
                                        "evidence_present": True, "observation": "denied_with_control_plane",
                                        "control_plane_private_confirmed": True, "external_network_confirmed": True,
                                        "resource_id": "fake", "collected_at_utc": "now"}))
            p = subprocess.run([sys.executable, str(ROOT/"scripts/phase6_result_classifier.py"),
                                "--input", str(path), "--expected", "Pass"],
                               capture_output=True, text=True, check=False)
            self.assertEqual(p.returncode, 2)
            self.assertEqual(json.loads(p.stdout)["result"], "REVIEW_REQUIRED")

    def test_1716_dependency_ledger_and_release_stay_no_go(self):
        r = audit(ROOT, include_cases=True)
        self.assertFalse(r["errors"], r["errors"])
        self.assertEqual(r["canonical_test_ids"], 1716)
        self.assertEqual(r["literal_script_reference"]["MISSING_SCRIPT_REFERENCE"], 126)
        self.assertEqual(r["literal_script_reference"]["TRACKED_SCRIPT_REFERENCE"], 873)
        self.assertEqual(r["literal_script_reference"]["NO_DIRECT_SCRIPT_REFERENCE"], 717)
        self.assertEqual(r["cases_with_missing_input"], 2)
        self.assertNotIn("scripts/phase6_guard.py", r["missing_script_paths"])
        self.assertNotIn("scripts/phase6_result_classifier.py", r["missing_script_paths"])
        self.assertEqual(r["azure_live_passes_verified"], 0)
        self.assertEqual(r["release_decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
