"""L1 380 Azure/private-runner original command preflight, synthetic-only tests."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import review_live_380_preflight as review
from audit_tool_semantics_13 import load_sources
from build_execution_route_1716 import ROUTE_LIVE, build as build_routes, digest_case


class LivePreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = review.build_review(ROOT, include_cases=True)
        cls.frozen = load_sources(ROOT)
        cls.route = build_routes(ROOT, include_cases=True)

    def test_exact_380_source_cases_and_seven_exclusive_review_categories(self):
        r = self.report
        self.assertEqual(r["status"], "LIVE_EXECUTION_PRECHECK_ONLY_NOT_AUTHORIZED")
        self.assertEqual(r["source_only_live_candidates"], len(r["cases"]))
        self.assertEqual(len(r["cases"]), 380)
        self.assertEqual(r["review_priority_counts"], review.EXPECTED_COUNTS)
        self.assertEqual(r["direct_command_family_counts"], review.FAMILIES)
        self.assertEqual(sum(r["review_priority_counts"].values()), 380)
        self.assertEqual({k for k, v in self.route["cases"].items()
                          if v["route"] == ROUTE_LIVE}, set(r["cases"]))

    def test_every_case_matches_immutable_frozen_command_and_review_checklist(self):
        for case_id, row in self.report["cases"].items():
            with self.subTest(case_id=case_id):
                source = self.frozen[case_id]
                self.assertEqual(row["catalogue_contract_sha256"], digest_case(source))
                self.assertEqual(row["canonical_catalogue"],
                                 self.route["cases"][case_id]["canonical_catalogue"])
                label, head = review.classify(case_id, source["command"])
                self.assertEqual((label, head),
                                 (row["review_priority"], row["direct_command_family"]))
                self.assertEqual(row["review_checklist"], list(review.GATES[label]))
                self.assertEqual(len(row["review_checklist"]), 3)

    def test_waf_active_vectors_are_three_p0_and_not_auto_approved(self):
        ids = {i for i, row in self.report["cases"].items()
               if row["review_priority"] == review.WAF}
        self.assertEqual(ids, review.WAF_IDS)
        for i in ids:
            self.assertFalse(self.report["cases"][i]["owner_authorized_execution"])

    def test_exact_11_terraform_plans_require_state_and_backend_review(self):
        ids = [i for i, r in self.report["cases"].items()
               if r["review_priority"] == review.TERRAFORM]
        self.assertEqual(len(ids), 11)
        self.assertTrue(all("plan" in self.frozen[i]["command"] for i in ids))
        self.assertEqual(self.report["cases"]["AZ-T23-19"]["review_priority"], review.TERRAFORM)

    def test_external_dns_literal_is_not_normalized_to_private_dns(self):
        r = self.report["cases"]["AZ-T18-05"]
        self.assertEqual(r["review_priority"], review.EXTERNAL_DNS)
        self.assertEqual(r["direct_command_family"], "dig")
        with self.assertRaises(review.LiveReviewError):
            review.classify("AZ-T18-05", "dig +short \"example.invalid\"")
        with self.assertRaises(review.LiveReviewError):
            review.classify("AZ-T27-13", "dig +short @1.1.1.1 example.invalid")

    def test_waf_mutation_does_not_become_generic_probe_or_pass(self):
        original = self.frozen["AZ-T69-05"]["command"]
        with self.assertRaises(review.LiveReviewError):
            review.classify("AZ-T69-05", original.replace("--data-urlencode", "--head"))
        with self.assertRaises(review.LiveReviewError):
            review.classify("AZ-T69-05", original.replace("WAF_TEST_URL", "OTHER_TARGET"))
        with self.assertRaises(review.LiveReviewError):
            review.classify("AZ-T68-01", original)

    def test_reject_unknown_write_or_non_plan_shell_shape(self):
        for case_id, command in (
            ("AZ-T19-09", "curl --request POST -o /dev/null https://example.invalid"),
            ("AZ-T23-19", "terraform -chdir=infra apply -auto-approve"),
            ("AZ-T11-03", "az"),
            ("AZ-T48-09", "openssl req -new -key secret"),
            ("AZ-T19-05", "python3 -c 'print(1)'"),
            ("AZ-T19-09", "curl \"unterminated"),
        ):
            with self.subTest(case_id=case_id):
                with self.assertRaises(review.LiveReviewError):
                    review.classify(case_id, command)

    def test_no_executable_command_or_live_pass_approved(self):
        r = self.report
        self.assertEqual(r["owner_authorized_cases"], 0)
        self.assertEqual(r["approved_private_runner_cases"], 0)
        self.assertEqual(r["canonical_commands_executed"], 0)
        self.assertEqual(r["azure_live_passes"], 0)
        self.assertEqual(r["azure_not_ready"], 1716)
        self.assertEqual(r["release_decision"], "NO_GO")
        for row in r["cases"].values():
            self.assertFalse(row["owner_authorized_execution"])
            self.assertFalse(row["private_runner_oidc_verified"])
            self.assertFalse(row["approved_nonproduction_target_verified"])
            self.assertFalse(row["original_command_executed"])
            self.assertFalse(row["independent_reviewer_signed"])
            self.assertEqual(row["azure_live_acceptance"], "NOT_READY")

    def test_no_r41_missing_browser_or_synthetic_ids_mixed_into_live(self):
        self.assertNotIn("AZ-T64-09", self.report["cases"])
        self.assertNotIn("AZ-T20-07", self.report["cases"])
        self.assertNotIn("AZ-T74-13", self.report["cases"])
        self.assertNotIn("AZ-T01-02", self.report["cases"])

    def test_cli_exit_status_success_is_not_release_pass(self):
        script = str(ROOT / "scripts/review_live_380_preflight.py")
        for strict, want in ((False, 0), (True, 2)):
            with self.subTest(strict=strict):
                args = [sys.executable, script, "--summary-only"]
                if strict:
                    args.append("--strict")
                p = subprocess.run(args, cwd=ROOT, text=True,
                                   capture_output=True, check=False)
                self.assertEqual(p.returncode, want, p.stdout + p.stderr)
                r = json.loads(p.stdout)
                self.assertEqual(r["source_only_live_candidates"], 380)
                self.assertEqual(r["azure_live_passes"], 0)
                self.assertEqual(r["release_decision"], "NO_GO")
                self.assertNotIn("cases", r)

    def test_output_contains_no_original_commands_or_private_values(self):
        script = str(ROOT / "scripts/review_live_380_preflight.py")
        with tempfile.TemporaryDirectory(prefix="live-review-380-") as td:
            outfile = Path(td) / "live-risk-queue.json"
            p = subprocess.run([sys.executable, script, "--out", str(outfile)],
                               cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            raw = outfile.read_text(encoding="utf-8")
            r = json.loads(raw)
            self.assertEqual(len(r["cases"]), 380)
            self.assertNotIn('"command":', raw)
            self.assertNotIn("APPROVED_SQLI_VECTOR", raw)
            self.assertNotIn("STATE_SA_RESOURCE_ID", raw)
            self.assertEqual(r["release_decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
