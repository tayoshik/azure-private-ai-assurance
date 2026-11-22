"""Nineteen source-only grep/find/git/jq assertion review regressions."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_assertion_semantics_19 as audit
from triage_local_464 import PRIORITY_ASSERTION, TriageError, make_queue


class AssertionSemantics19Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = audit.build_review(ROOT)
        cls.upstream = make_queue(ROOT)

    def test_exact_19_ids_partition_against_parent(self):
        target = {i for i, v in self.upstream["cases"].items()
                  if v["review_priority"] == PRIORITY_ASSERTION}
        self.assertEqual(target, set(audit.EXPECTED))
        self.assertEqual(set(self.review["cases"]), target)
        self.assertEqual(self.review["simple_assertion_cases"], 19)
        self.assertEqual(self.review["review_class_counts"], audit.EXPECTED_COUNTS)
        self.assertEqual(sum(sum(v.values()) for v in
                             self.review["source_group_counts"].values()), 19)

    def test_per_id_original_contract_fingerprint_and_review_checklist(self):
        for ident, row in self.review["cases"].items():
            with self.subTest(ident=ident):
                self.assertEqual(row["contract_sha256"],
                                 self.upstream["cases"][ident]["contract_sha256"])
                self.assertEqual(row["semantic_review_class"], audit.EXPECTED[ident])
                self.assertEqual(row["review_checklist"],
                                 list(audit.CHECKS[audit.EXPECTED[ident]]))
                self.assertEqual(row["additional_case_specific_check"],
                                 audit.CASE_SPECIAL_CHECKS.get(ident))
                self.assertEqual(len(row["contract_sha256"]), 64)

    def test_no_case_executed_approved_or_live_accepted(self):
        r = self.review
        self.assertEqual(r["original_commands_executed"], 0)
        self.assertEqual(r["independent_approval_signatures"], 0)
        self.assertEqual(r["approved_input_bytes_inspected"], 0)
        self.assertEqual(r["azure_live_passes"], 0)
        self.assertEqual(r["release_decision"], "NO_GO")
        for row in r["cases"].values():
            for name in ("source_control_contract_verified",
                         "approved_source_revision_verified",
                         "input_custody_and_signatures_verified",
                         "effective_assertion_semantics_verified",
                         "owner_authorized_command_execution",
                         "original_command_executed",
                         "reviewer1_signed", "reviewer2_signed"):
                self.assertFalse(row[name], name)
            self.assertEqual(row["azure_live_acceptance"], "NOT_READY")

    def test_no_original_command_or_private_input_values_in_report(self):
        encoded = json.dumps(self.review, ensure_ascii=False)
        for value in ("grep -R -n", "find infra/tests", "git rev-parse HEAD",
                      "jq -e '.ticket", "docs/qa/waf-test-approval.json"):
            with self.subTest(value=value):
                self.assertNotIn(value, encoded)
        for item in self.review["cases"].values():
            for key in ("command", "command_text", "input_references", "raw_path", "expected"):
                self.assertNotIn(key, item)

    def test_grep_presence_does_not_prove_hcl_backend_semantics(self):
        self.assertEqual(self.review["cases"]["AZ-T15-01"]["semantic_review_class"],
                         audit.GREP)
        self.assertIn("CHECK_NESTED_QUOTE_REGEX",
                      self.review["cases"]["AZ-T15-01"]["additional_case_specific_check"])

    def test_grep_http_tls_boolean_presence_is_not_safe_assertion(self):
        self.assertEqual(self.review["cases"]["AZ-T20-13"]["semantic_review_class"],
                         audit.GREP)
        self.assertIn("VERIFY_TLS_IGNORE_HTTP_ERRORS_IS_DISABLED",
                      self.review["cases"]["AZ-T20-13"]["additional_case_specific_check"])

    def test_find_exit_zero_with_no_files_is_not_proof(self):
        for ident in ("AZ-T16-05", "AZ-T16-11", "AZ-T16-15", "AZ-T44-09"):
            self.assertEqual(self.review["cases"][ident]["semantic_review_class"], audit.FIND)
            self.assertIn("PROVE_MATCH_COUNT_GREATER_THAN_ZERO_NOT_JUST_FIND_EXIT_ZERO",
                          self.review["cases"][ident]["review_checklist"])

    def test_git_hash_requires_approved_source_and_plan_relation(self):
        self.assertEqual(self.review["cases"]["AZ-T45-05"]["semantic_review_class"], audit.GIT)
        self.assertEqual(self.review["cases"]["AZ-T14-07"]["semantic_review_class"], audit.GIT)
        self.assertEqual(self.review["cases"]["AZ-T45-05"]["additional_case_specific_check"],
                         "MATCH_GIT_SHA_TO_SIGNED_PLAN_GENERATION_SOURCE_REVISION")

    def test_waf_approval_field_is_not_a_signed_authorization(self):
        for ident in ("AZ-T69-03", "AZ-T69-11", "AZ-T69-13", "AZ-T69-15"):
            self.assertEqual(self.review["cases"][ident]["semantic_review_class"], audit.JQ)
            self.assertFalse(self.review["cases"][ident]["input_custody_and_signatures_verified"])
        self.assertEqual(audit.categorize(
            "jq -e '.scope.approved == true' docs/qa/test.json"), audit.JQ)

    def test_quoted_jq_pipe_is_not_shell_pipeline(self):
        s = "jq -e '.requests | length > 0' docs/qa/request.json"
        self.assertEqual(audit.categorize(s), audit.JQ)

    def test_shell_chains_or_redirections_must_be_escalated(self):
        for s in ("grep -R foo infra && curl https://example.invalid",
                  "find infra -type f > artifact.log",
                  "git rev-parse HEAD | tee report.txt",
                  "jq -e .ok test.json; echo success"):
            with self.subTest(s=s), self.assertRaises(TriageError):
                audit.categorize(s)

    def test_environment_expansion_substitution_rejected(self):
        for s in ("jq -e .ok $UNVERIFIED",
                  "grep -R $(curl https://example.invalid) infra",
                  "git rev-parse \x60echo HEAD\x60", "find infra\nrm bad"):
            with self.subTest(s=s), self.assertRaises(TriageError):
                audit.categorize(s)

    def test_jq_without_e_must_not_substitute_boolean_exit_assertion(self):
        with self.assertRaises(TriageError):
            audit.categorize("jq '.ok' docs/qa/test.json")

    def test_grep_nonrecursive_scope_requires_new_review(self):
        with self.assertRaises(TriageError):
            audit.categorize("grep keyword infra/main.tf")

    def test_unrecognized_or_malformed_command_rejected(self):
        for s in (None, "", "  ", "sed -n 1p infra/main.tf", "jq 'unclosed"):
            with self.subTest(s=s), self.assertRaises(TriageError):
                audit.categorize(s)

    def test_cli_strict_denial_zero_azure(self):
        argv = [sys.executable, str(ROOT/"scripts/audit_assertion_semantics_19.py"),
                "--summary-only"]
        p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        x = json.loads(p.stdout)
        self.assertEqual(x["simple_assertion_cases"], 19)
        self.assertEqual(x["review_class_counts"], audit.EXPECTED_COUNTS)
        self.assertEqual(x["azure_live_passes"], 0)
        self.assertEqual(x["release_decision"], "NO_GO")
        p2 = subprocess.run(argv+["--strict"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p2.returncode, 2, p2.stderr)
        self.assertEqual(json.loads(p2.stdout)["original_commands_executed"], 0)


if __name__ == "__main__":
    unittest.main()
