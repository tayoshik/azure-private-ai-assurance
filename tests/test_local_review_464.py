"""Synthetic mutations and exact-source, non-executing 464-case queue checks."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import triage_local_464 as local


class Local464SourceReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = local.make_queue(ROOT)

    def test_exact_464_cases_and_partition(self):
        r = self.report
        self.assertEqual(r["status"], "REVIEW_PRIORITIES_ONLY")
        self.assertEqual(r["original_total_cases"], 1716)
        self.assertEqual(r["local_candidate_cases"], 464)
        self.assertEqual(len(r["cases"]), 464)
        self.assertEqual(sum(r["source_only_priority_counts"].values()), 464)
        self.assertEqual(set(r["source_only_priority_counts"]), set(local.PRIORITIES))
        self.assertEqual(sum(sum(x.values()) for x in r["phase_priority_counts"].values()), 464)

    def test_all_464_remain_unexecuted_unreviewed_and_no_go(self):
        self.assertEqual(self.report["commands_executed"], 0)
        self.assertEqual(self.report["approved_inputs_verified"], 0)
        self.assertEqual(self.report["independent_approvals"], 0)
        self.assertEqual(self.report["azure_live_passes"], 0)
        self.assertEqual(self.report["release_decision"], "NO_GO")
        for k, r in self.report["cases"].items():
            with self.subTest(id=k):
                self.assertFalse(r["command_executed"])
                self.assertFalse(r["approved_input_verified"])
                self.assertFalse(r["semantic_assertion_reviewed"])
                self.assertFalse(r["independent_reviewer_signed"])
                self.assertEqual(r["azure_live_acceptance"], "NOT_READY")
                self.assertEqual(len(r["contract_sha256"]), 64)

    def test_no_raw_canonical_commands_leak_into_queue(self):
        for row in self.report["cases"].values():
            self.assertNotIn("command", row)
            self.assertNotIn("input_references", row)
            self.assertNotIn("script_references", row)
        self.assertFalse(self.report["review_queue_has_executable_commands"])

    def test_compound_shell_hidden_network_is_escalated(self):
        prio, why = local.inspect_command(
            "cd tests && npm ci --offline && npx playwright test --list", "cd", [])
        self.assertEqual(prio, local.PRIORITY_SHELL)
        self.assertIn("SHELL_OPERATOR_OR_REDIRECTION", why)
        self.assertIn("NESTED_NETWORK_OR_INDIRECT_TOOL", why)

    def test_compound_command_starting_looks_safe_is_not_assumed_safe(self):
        priority, reasons = local.inspect_command(
            "echo hello && curl https://example.invalid", "echo", [])
        self.assertEqual(priority, local.PRIORITY_SHELL)
        self.assertIn("NESTED_NETWORK_OR_INDIRECT_TOOL", reasons)

    def test_quoted_jq_pipe_is_not_a_shell_pipe(self):
        p, flags = local.inspect_command(
            """jq -e '.networks.onprem.cidrs | length > 0' "$IPAM_JSON" """.strip(),
            "jq", [])
        self.assertEqual(p, local.PRIORITY_INPUT)
        self.assertNotIn("SHELL_OPERATOR_OR_REDIRECTION", flags)
        self.assertIn("ENVIRONMENT_INPUT_UNVERIFIED", flags)

    def test_unquoted_redirection_cannot_be_auto_executed(self):
        p, reasons = local.inspect_command(
            "find infra -name x 2>/dev/null", "find", [])
        self.assertEqual(p, local.PRIORITY_SHELL)
        self.assertIn("SHELL_OPERATOR_OR_REDIRECTION", reasons)

    def test_sensitive_saved_plan_is_not_ready(self):
        p, flags = local.inspect_command(
            'sha256sum "$APPROVED_PLAN"', "sha256sum", [])
        self.assertEqual(p, local.PRIORITY_INPUT)
        self.assertIn("POSSIBLE_RESTRICTED_OR_APPROVED_INPUT", flags)

    def test_simple_jq_expression_still_requires_semantic_review(self):
        p, reasons = local.inspect_command("jq -e '.enabled == true' status.json", "jq", [])
        self.assertEqual(p, local.PRIORITY_ASSERTION)
        self.assertEqual(reasons, [])

    def test_unexpected_external_tool_requires_escalation(self):
        p, reasons = local.inspect_command("sudo bash -c 'echo unsafe'", "sudo", [])
        self.assertEqual(p, local.PRIORITY_SHELL)
        self.assertIn("INDIRECT_TOP_LEVEL_COMMAND", reasons)

    def test_unknown_plain_tool_remains_manual_review(self):
        p, reasons = local.inspect_command("mytool --status", "mytool", [])
        self.assertEqual(p, local.PRIORITY_TOOL)
        self.assertIn("UNRECOGNIZED_LOCAL_COMMAND_FAMILY", reasons)

    def test_malformed_shell_is_reviewed_not_run(self):
        p, reasons = local.inspect_command("jq 'unclosed", "jq", [])
        self.assertEqual(p, local.PRIORITY_SHELL)
        self.assertIn("SHELL_LEXING_UNCERTAIN", reasons)

    def test_strict_mode_denies_azure_acceptance(self):
        args = [sys.executable, str(ROOT/"scripts/triage_local_464.py"), "--summary-only"]
        r = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        payload = json.loads(r.stdout)
        self.assertEqual(payload["local_candidate_cases"], 464)
        self.assertEqual(payload["release_decision"], "NO_GO")
        r2 = subprocess.run(args + ["--strict"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r2.returncode, 2, r2.stderr)
        self.assertEqual(json.loads(r2.stdout)["azure_live_passes"], 0)


if __name__ == "__main__":
    unittest.main()
