"""Thirteen frozen tool-semantics case IDs: source-only, mutation, NO_GO tests."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_tool_semantics_13 as review
from triage_local_464 import make_queue, PRIORITY_TOOL, TriageError


class ToolSemantics13Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = review.build_review(ROOT)
        cls.parent = make_queue(ROOT)

    def test_all_13_exact_original_ids_and_group_counts(self):
        ids = {i for i, row in self.parent["cases"].items()
               if row["review_priority"] == PRIORITY_TOOL}
        self.assertEqual(ids, set(review.EXPECTED))
        self.assertEqual(set(self.result["cases"]), ids)
        self.assertEqual(self.result["tool_review_cases"], 13)
        self.assertEqual(self.result["group_counts"], review.EXPECTED_COUNTS)
        self.assertEqual(sum(sum(g.values()) for g in
                             self.result["source_group_counts"].values()), 13)

    def test_original_source_hashes_and_case_groups_stay_bound(self):
        for ident, row in self.result["cases"].items():
            with self.subTest(ident=ident):
                self.assertEqual(row["contract_sha256"],
                                 self.parent["cases"][ident]["contract_sha256"])
                self.assertEqual(row["tool_semantics_group"], review.EXPECTED[ident])
                self.assertEqual(row["review_checks"],
                                 list(review.REVIEW_CHECKS[row["tool_semantics_group"]]))
                self.assertEqual(len(row["contract_sha256"]), 64)

    def test_all_cases_remain_not_ready_and_unauthorized(self):
        self.assertEqual(self.result["original_commands_executed"], 0)
        self.assertEqual(self.result["approved_tool_environments_verified"], 0)
        self.assertEqual(self.result["approved_evidence_verified"], 0)
        self.assertEqual(self.result["independent_review_signatures"], 0)
        self.assertEqual(self.result["azure_live_passes"], 0)
        self.assertEqual(self.result["release_decision"], "NO_GO")
        for row in self.result["cases"].values():
            for k in ("owner_approved_execution_environment",
                      "network_and_backend_approval_verified",
                      "pinned_toolchain_and_source_verified",
                      "assertion_semantics_verified", "approved_evidence_verified",
                      "reviewer1_signed", "reviewer2_signed",
                      "original_command_executed"):
                self.assertFalse(row[k], k)
            self.assertEqual(row["azure_live_acceptance"], "NOT_READY")

    def test_no_original_shell_or_sensitive_plan_in_json(self):
        encoded = json.dumps(self.result, ensure_ascii=False)
        for secret_like in ("terraform init -input", "terraform -chdir=infra",
                            "fixtures/plan_app_pna_true.json",
                            "fixtures/plan_nsg_any.json", "$APPROVED_PLAN"):
            with self.subTest(secret_like=secret_like):
                self.assertNotIn(secret_like, encoded)
        for row in self.result["cases"].values():
            for key in ("command", "expected", "raw_input_path", "env_value",
                        "private_path", "command_text"):
                self.assertNotIn(key, row)

    def test_init_has_network_backend_dependency_risk(self):
        row = self.result["cases"]["AZ-T15-17"]
        self.assertEqual(row["tool_semantics_group"], review.INIT)
        self.assertTrue(row["possible_network_or_dependency_side_effects"])
        self.assertIn("PROHIBIT_UNAUTHORIZED_BACKEND_ACCESS_OR_DOWNLOADS",
                      row["review_checks"])

    def test_readonly_lockfile_is_not_offline_authorization(self):
        self.assertEqual(review.categorize(
            "terraform init -input=false -lockfile=readonly -no-color"), review.INIT)

    def test_terraform_fmt_is_style_not_azure_acceptance(self):
        for ident in ("AZ-T16-01", "AZ-T44-05"):
            self.assertEqual(self.result["cases"][ident]["tool_semantics_group"], review.FMT)
            self.assertFalse(self.result["cases"][ident]["possible_network_or_dependency_side_effects"])

    def test_validate_requires_pinned_preinitialized_context(self):
        for ident in ("AZ-T16-03", "AZ-T44-07"):
            row = self.result["cases"][ident]
            self.assertEqual(row["tool_semantics_group"], review.VALIDATE)
            self.assertTrue(row["possible_network_or_dependency_side_effects"])

    def test_tflint_checkov_have_dependency_policy_gates(self):
        for ident in ("AZ-T16-07", "AZ-T44-11", "AZ-T16-09", "AZ-T44-13"):
            with self.subTest(ident=ident):
                self.assertTrue(self.result["cases"][ident][
                    "possible_network_or_dependency_side_effects"])

    def test_fixture_negative_assertions_do_not_prove_live_azure(self):
        for ident in ("AZ-T74-01", "AZ-T74-03"):
            row = self.result["cases"][ident]
            self.assertEqual(row["tool_semantics_group"], review.PY_NEGATIVE)
            self.assertEqual(row["azure_live_acceptance"], "NOT_READY")
        with self.assertRaises(TriageError):
            review.categorize(
                "python3 scripts/phase7_plan_policy.py --plan fixtures/unknown.json --expect Fail")

    def test_node_version_only_measures_tool_revision(self):
        self.assertEqual(self.result["cases"]["AZ-T20-03"]["tool_semantics_group"],
                         review.NODE)
        with self.assertRaises(TriageError):
            review.categorize("node --version --other")

    def test_unknown_or_mutating_terraform_commands_rejected(self):
        for command in ("terraform apply -auto-approve", "terraform destroy",
                        "terraform plan", "terraform import foo bar"):
            with self.subTest(command=command), self.assertRaises(TriageError):
                review.categorize(command)

    def test_injected_shell_expansion_or_multiple_commands_rejected(self):
        for command in ("terraform init && curl https://example.invalid",
                        "node --version; rm -rf /tmp/irrelevant",
                        "terraform fmt > result.txt",
                        "python3 scripts/x.py --plan $(echo unsafe)",
                        "terraform \x60echo init\x60", "terraform init\nterraform apply"):
            with self.subTest(command=command), self.assertRaises(TriageError):
                review.categorize(command)

    def test_unknown_command_or_empty_input_rejected(self):
        for cmd in ("", None, "az group list", "python3 arbitrary.py", "npm install"):
            with self.subTest(cmd=cmd), self.assertRaises(TriageError):
                review.categorize(cmd)

    def test_summary_cli_success_but_strict_denial(self):
        script = ROOT / "scripts/audit_tool_semantics_13.py"
        args = [sys.executable, str(script), "--summary-only"]
        p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        x = json.loads(p.stdout)
        self.assertEqual(x["tool_review_cases"], 13)
        self.assertEqual(x["group_counts"], review.EXPECTED_COUNTS)
        self.assertEqual(x["release_decision"], "NO_GO")
        p2 = subprocess.run(args + ["--strict"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p2.returncode, 2, p2.stderr)
        self.assertEqual(json.loads(p2.stdout)["azure_live_passes"], 0)


if __name__ == "__main__":
    unittest.main()
