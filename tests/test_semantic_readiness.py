"""Regression for cross-phase readiness classification; synthetic != live."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import audit_semantic_readiness as p

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BY_PHASE = {"P1": 220, "P2": 220, "P3": 264, "P4": 286,
                     "P5": 286, "P6": 220, "P7": 220}


class SemanticReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = p.review(ROOT, include_cases=True)

    def test_1716_unique_ids_and_exact_phase_coverage(self):
        x = self.report
        self.assertEqual(x["errors"], [])
        self.assertEqual(x["catalogue_cases_reviewed"], 1716)
        self.assertEqual(set(x["cases"]), p.EXPECTED_IDS)
        self.assertEqual({k: v["cases"] for k, v in x["by_phase"].items()}, EXPECTED_BY_PHASE)

    def test_parity_is_exactly_858_review_and_858_synthetic(self):
        c = self.report["classification"]
        self.assertEqual(c["ODD_PROCEDURES"], 858)
        self.assertEqual(c["EVEN_SYNTHETIC_LABELS"], 858)
        for case_id, row in self.report["cases"].items():
            odd = int(case_id[-2:]) % 2 == 1
            self.assertEqual(row["case_polarity"],
                             "ODD_REVIEW_OR_OBSERVATION" if odd else "EVEN_SYNTHETIC")

    def test_13_missing_paths_not_erased_and_no_azure_claims(self):
        c = self.report["classification"]
        self.assertEqual(c["SOURCE_REFERENCE_MISSING"], 13)
        self.assertEqual(self.report["literal_dependency_snapshot"]["MISSING_SCRIPT_REFERENCE"], 13)
        self.assertEqual(self.report["literal_dependency_snapshot"]["MISSING_INPUT_CASES"], 0)
        self.assertEqual(self.report["literal_dependency_snapshot"]["TRACKED_SCRIPT_REFERENCE"], 986)
        self.assertEqual(self.report["literal_dependency_snapshot"]["NO_DIRECT_SCRIPT_REFERENCE"], 717)
        self.assertEqual(self.report["independently_approved_azure_passes"], 0)
        self.assertEqual(self.report["release_decision"], "NO_GO")
        for v in self.report["cases"].values():
            self.assertIs(v["accepted_live_evidence"], False)
            self.assertEqual(v["azure_acceptance"], "NOT_READY")

    def test_synthetic_selftests_are_not_runtime_acceptance(self):
        classes = self.report["classification"]
        self.assertEqual(classes["OFFLINE_SYNTHETIC_ONLY"], 858)
        self.assertEqual(classes["ODD_SELFTEST_REQUIRES_SEMANTIC_REVIEW"], 1)
        self.assertEqual(classes["UNVERIFIED_NON_SYNTHETIC_PROCEDURE"], 844)
        self.assertEqual(set(self.report["flag_case_ids"]["ODD_ID_RUNS_SELFTEST_NOT_RUNTIME_EVIDENCE"]),
                         {"AZ-T74-13"})
        self.assertEqual(self.report["cases"]["AZ-T74-13"]["azure_acceptance"], "NOT_READY")

    def test_file_presence_not_semantic_coverage(self):
        example = self.report["cases"]["AZ-T01-01"]
        self.assertEqual(example["source_reference"], "TRACKED_SCRIPT_REFERENCE")
        self.assertEqual(example["assurance_readiness"], "UNVERIFIED_NON_SYNTHETIC_PROCEDURE")
        self.assertIn("AZ-T20-01", self.report["flag_case_ids"][
            "ARTIFACT_PRESENCE_NEEDS_CONTENT_AND_BASELINE_REVIEW"
        ])

    def test_browser_contract_is_separate_blocker(self):
        ids = self.report["flag_case_ids"]["REAL_APP_AUTH_AND_RUNNER_REQUIRED"]
        self.assertEqual(set(ids), p.BROWSER)
        self.assertEqual(len(ids), 13)
        self.assertTrue(all(self.report["cases"][i]["assurance_readiness"] ==
                            "SOURCE_REFERENCE_MISSING" for i in ids))
        self.assertTrue(all(self.report["cases"][i]["azure_acceptance"] == "NOT_READY"
                            for i in ids))

    def test_no_direct_script_does_not_mean_no_test(self):
        ids = self.report["flag_case_ids"]["NO_LOCAL_SCRIPT_REF_CLI_OR_MANUAL_REVIEW"]
        self.assertEqual(len(ids), 717)
        self.assertTrue(all(self.report["cases"][i]["source_reference"] ==
                            "NO_DIRECT_SCRIPT_REFERENCE" for i in ids))

    def test_distribution_covers_exact_1716_without_double_count(self):
        c = self.report["classification"]
        cats=("SOURCE_REFERENCE_MISSING","OFFLINE_SYNTHETIC_ONLY",
              "ODD_SELFTEST_REQUIRES_SEMANTIC_REVIEW",
              "UNVERIFIED_NON_SYNTHETIC_PROCEDURE")
        self.assertEqual(sum(c[key] for key in cats), 1716)
        self.assertEqual(sum(self.report["published_execution_class_distribution"].values()), 1716)

    def test_normal_audit_is_success_but_strict_never_approves(self):
        for strict in (False, True):
            args = [sys.executable, str(ROOT/"scripts/audit_semantic_readiness.py")]
            if strict:
                args.append("--strict")
            result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2 if strict else 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["independently_approved_azure_passes"], 0)
            self.assertEqual(data["release_decision"], "NO_GO")
            self.assertEqual(data["catalogue_cases_reviewed"], 1716)

    def test_missing_root_is_an_invalid_inventory_and_denied(self):
        with tempfile.TemporaryDirectory() as d:
            x = p.review(Path(d))
            self.assertGreater(len(x["errors"]), 0)
            self.assertEqual(x["release_decision"], "NO_GO")
            self.assertEqual(x["independently_approved_azure_passes"], 0)

    def test_cli_writes_full_per_case_json_safely(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)/"semantic.json"
            result = subprocess.run(
                [sys.executable,str(ROOT/"scripts/audit_semantic_readiness.py"),
                 "--out",str(output),"--cases"],
                cwd=ROOT,capture_output=True,text=True,check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            obj=json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(len(obj["cases"]),1716)
            self.assertEqual(obj["cases"]["AZ-T64-15"]["assurance_readiness"],
                             "SOURCE_REFERENCE_MISSING")


if __name__ == "__main__":
    unittest.main()
