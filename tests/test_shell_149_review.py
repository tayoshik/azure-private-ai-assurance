"""Synthetic shell-grammar mutations and exact-source 149-case review tests."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_shell_149_review as audit
import triage_local_464 as parent


class P0ShellReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = audit.build_review(ROOT, include_cases=True)
        cls.parent = parent.make_queue(ROOT, include_cases=True)

    def test_exact_p0_149_cases_match_parent_without_status_promotion(self):
        r = self.report
        inherited = {i for i, c in self.parent["cases"].items()
                     if c["review_priority"] == parent.PRIORITY_SHELL}
        self.assertEqual(set(r["cases"]), inherited)
        self.assertEqual(len(inherited), 149)
        self.assertEqual(r["shell_p0_count"], 149)
        self.assertEqual(sum(r["review_class_counts"].values()), 149)
        self.assertEqual(sum(sum(v.values()) for v in
                             r["phase_review_counts"].values()), 149)
        self.assertEqual(set(r["review_class_counts"]), set(audit.CLASSES))

    def test_every_case_requires_two_reviews_and_no_azure_pass(self):
        for ident, row in self.report["cases"].items():
            with self.subTest(ident=ident):
                self.assertFalse(row["command_executed"])
                self.assertFalse(row["actual_command_authorized"])
                self.assertFalse(row["source_dependencies_or_approved_inputs_verified"])
                self.assertFalse(row["semantic_expected_result_verified"])
                self.assertFalse(row["reviewer1_signed"])
                self.assertFalse(row["reviewer2_signed"])
                self.assertEqual(row["azure_live_acceptance"], "NOT_READY")
                self.assertEqual(len(row["contract_sha256"]), 64)
                self.assertEqual(row["review_checklist"],
                                 list(audit.NEXT_REVIEW[row["detailed_review_class"]]))
        self.assertEqual(self.report["commands_executed"], 0)
        self.assertEqual(self.report["case_reviews_approved"], 0)
        self.assertEqual(self.report["azure_live_passes"], 0)
        self.assertEqual(self.report["release_decision"], "NO_GO")

    def test_report_never_stores_raw_commands_or_evidence_paths(self):
        for row in self.report["cases"].values():
            for forbidden in ("command", "command_text", "expected", "credential",
                              "input_references", "script_references", "raw_path"):
                self.assertNotIn(forbidden, row)
        self.assertFalse(any("https://" in json.dumps(x) for x in self.report["cases"].values()))

    def test_and_conditionals_require_full_segment_review(self):
        typ, flags = audit.classify("test -f a && test -f b",
                                    ["SHELL_OPERATOR_OR_REDIRECTION"])
        self.assertEqual(typ, audit.CHAIN)
        self.assertIn("CHAIN_OR_CONDITIONAL_EXIT_STATUS", flags)

    def test_boolean_or_and_sequence_are_not_automatic(self):
        for text in ("test -f a || echo fail", "echo a; echo b", "echo a & echo b"):
            with self.subTest(text=text):
                self.assertEqual(audit.classify(text, ["SHELL_OPERATOR_OR_REDIRECTION"])[0],
                                 audit.CHAIN)

    def test_pipeline_requires_full_exit_and_dataflow_review(self):
        typ, flags = audit.classify("cat local.json | jq .",
                                    ["SHELL_OPERATOR_OR_REDIRECTION"])
        self.assertEqual(typ, audit.PIPE)
        self.assertIn("PIPELINE_DATAFLOW", flags)

    def test_redirect_and_fd_do_not_run_by_default(self):
        typ, flags = audit.classify("find infra -name '*.tf' 2>/dev/null",
                                    ["SHELL_OPERATOR_OR_REDIRECTION"])
        self.assertEqual(typ, audit.REDIRECT)
        self.assertIn("REDIRECTION_OR_DESCRIPTOR", flags)

    def test_indirect_network_after_safe_prefix_is_highest_priority(self):
        typ, flags = audit.classify(
            "cd tests && npx --no-install playwright test --list",
            ["SHELL_OPERATOR_OR_REDIRECTION", "NESTED_NETWORK_OR_INDIRECT_TOOL"])
        self.assertEqual(typ, audit.DYNAMIC)
        self.assertIn("NESTED_REMOTE_TOOL_NEEDS_REVIEW", flags)
        self.assertIn("CHAIN_OR_CONDITIONAL_EXIT_STATUS", flags)

    def test_shell_substitution_never_evaluated(self):
        typ, flags = audit.classify(
            "test -f $(curl https://example.invalid)", ["SHELL_EXPANSION_OR_MULTILINE"])
        self.assertEqual(typ, audit.DYNAMIC)
        self.assertIn("COMMAND_SUBSTITUTION_OR_MULTILINE", flags)

    def test_dynamic_python_cannot_be_implicitly_approved(self):
        typ, flags = audit.classify(
            "python3 -c 'print(1)'", ["DYNAMIC_PYTHON_INVOCATION_REVIEW"])
        self.assertEqual(typ, audit.DYNAMIC)
        self.assertIn("DYNAMIC_PYTHON_OR_MODULE", flags)

    def test_malformed_shell_lexer_fails_closed(self):
        typ, flags = audit.classify("jq 'unclosed", ["SHELL_LEXING_UNCERTAIN"])
        self.assertEqual(typ, audit.UNKNOWN)
        self.assertIn("LEXER_COULD_NOT_PARSE", flags)

    def test_quoted_operators_do_not_count_as_bash_operators(self):
        typ, flags = audit.classify("jq -e '.a | length > 1' state.json", [])
        self.assertEqual(typ, audit.UNKNOWN)  # this helper only gets real P0 from parent
        self.assertNotIn("PIPELINE_DATAFLOW", flags)
        self.assertNotIn("REDIRECTION_OR_DESCRIPTOR", flags)

    def test_unknown_shell_operators_escalate(self):
        typ, flags = audit.classify("echo foo |& tee output.log",
                                    ["SHELL_OPERATOR_OR_REDIRECTION"])
        self.assertIn(typ, (audit.PIPE, audit.UNKNOWN))
        self.assertTrue(flags)

    def test_output_strict_mode_refuses_acceptance(self):
        script = ROOT / "scripts" / "audit_shell_149_review.py"
        cmd = [sys.executable, str(script), "--summary-only"]
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, 0, p.stderr)
        result = json.loads(p.stdout)
        self.assertEqual(result["shell_p0_count"], 149)
        self.assertEqual(result["release_decision"], "NO_GO")
        q = subprocess.run(cmd + ["--strict"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        self.assertEqual(q.returncode, 2, q.stderr)
        self.assertEqual(json.loads(q.stdout)["azure_live_passes"], 0)


if __name__ == "__main__":
    unittest.main()
