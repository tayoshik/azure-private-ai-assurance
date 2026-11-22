"""Source-locked 283-input queue: no private data or acceptance in test fixtures."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_approved_input_283 as audit
from triage_local_464 import PRIORITY_INPUT, make_queue, TriageError


class ApprovedInputReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = audit.build_review(ROOT)
        cls.upstream = make_queue(ROOT)

    def test_exact_283_case_source_locked_partition(self):
        report = self.review
        inherited = {id_ for id_, row in self.upstream["cases"].items()
                     if row["review_priority"] == PRIORITY_INPUT}
        self.assertEqual(len(inherited), 283)
        self.assertEqual(set(report["cases"]), inherited)
        self.assertEqual(report["restricted_input_283_candidate_count"], 283)
        self.assertEqual(sum(report["review_input_class_counts"].values()), 283)
        self.assertEqual(set(report["review_input_class_counts"]), set(audit.CLASSES))
        self.assertEqual(sum(sum(p.values()) for p in
                             report["source_class_counts"].values()), 283)

    def test_every_input_remains_unchecked_and_no_go(self):
        r = self.review
        self.assertEqual(r["input_bytes_inspected"], 0)
        self.assertEqual(r["approved_inputs_verified"], 0)
        self.assertEqual(r["source_commands_executed"], 0)
        self.assertEqual(r["independent_approvals_verified"], 0)
        self.assertEqual(r["azure_live_passes"], 0)
        self.assertEqual(r["release_decision"], "NO_GO")
        for ident, row in r["cases"].items():
            with self.subTest(ident=ident):
                for key in ("input_source_identified", "actual_input_bytes_examined",
                            "approved_input_hash_verified", "access_and_custody_approved",
                            "expected_control_semantics_reviewed",
                            "independent_reviewer1_signed", "independent_reviewer2_signed",
                            "command_executed"):
                    self.assertFalse(row[key])
                self.assertEqual(row["azure_live_acceptance"], "NOT_READY")
                self.assertEqual(len(row["contract_sha256"]), 64)

    def test_no_raw_commands_input_values_or_paths_in_report(self):
        for row in self.review["cases"].values():
            for forbidden in ("command", "command_text", "raw_path", "input_path",
                              "input_references", "script_references", "expected",
                              "raw_observation", "env_name", "access_token"):
                self.assertNotIn(forbidden, row)
            self.assertEqual(row["required_review_checks"],
                             list(audit.NEXT_REVIEW[row["review_input_class"]]))
        self.assertNotIn("APPROVED_PLAN", json.dumps(self.review))
        self.assertNotIn("evidence/ci/", json.dumps(self.review))

    def test_plan_has_highest_priority(self):
        group, flags = audit.classify_input('sha256sum "$APPROVED_PLAN"', [])
        self.assertEqual(group, audit.PLAN)
        self.assertIn("ENV_REFERENCE_UNVERIFIED", flags)

    def test_state_and_tfvars_not_safe(self):
        for source in ("terraform show infra/secret.tfstate", "jq . infra/dev.tfvars.json"):
            with self.subTest(source=source):
                self.assertEqual(audit.classify_input(source, [])[0], audit.PLAN)

    def test_real_evidence_paths_are_restricted(self):
        for source in ('jq -e .pass evidence/ci/results.json',
                       'jq -e .valid "$EVIDENCE_JSON"'):
            with self.subTest(source=source):
                self.assertEqual(audit.classify_input(source, [])[0], audit.EVIDENCE)

    def test_network_ipam_source_is_not_live_network_acceptance(self):
        group, flags = audit.classify_input(
            'jq -e ".networks.hub.cidrs | length > 0" "$IPAM_JSON"', [])
        self.assertEqual(group, audit.NETWORK)
        self.assertIn("ENV_REFERENCE_UNVERIFIED", flags)

    def test_signed_policy_baseline_requires_owner(self):
        group, _ = audit.classify_input(
            'python3 scripts/phase1_policy_check.py --baseline "$APPROVED_BASELINE_JSON"', [])
        self.assertEqual(group, audit.POLICY)

    def test_unknown_environment_input_needs_manual_review(self):
        group, flags = audit.classify_input('jq . "$UNRECOGNIZED_FILE"', [])
        self.assertEqual(group, audit.OTHER)
        self.assertIn("NO_KNOWN_INPUT_KIND_MANUAL_REVIEW", flags)

    def test_multiple_input_classes_overlap_not_hidden(self):
        group, flags = audit.classify_input(
            'jq . "$APPROVED_PLAN" evidence/ci/results.json', [])
        self.assertEqual(group, audit.PLAN)
        self.assertIn("MULTIPLE_INPUT_CLASSES_REQUIRE_INDEPENDENT_REVIEW", flags)

    def test_missing_literal_paths_never_count_as_verified(self):
        group, flags = audit.classify_input(
            "test -s local-input.json", ["MISSING_LITERAL_INPUT_PATH"])
        self.assertEqual(group, audit.OTHER)
        self.assertIn("MISSING_LITERAL_INPUT_REFERENCE", flags)

    def test_invalid_command_fails_closed(self):
        for bad in ("", "  ", None):
            with self.subTest(bad=bad):
                with self.assertRaises(TriageError):
                    audit.classify_input(bad, [])

    def test_283_cannot_be_promoted_by_changing_parent(self):
        self.assertEqual(self.review["status"], "SOURCE_INPUT_REVIEW_ONLY")
        self.assertTrue(all(r["azure_live_acceptance"] == "NOT_READY"
                            for r in self.review["cases"].values()))

    def test_strict_cli_exit_is_two_without_azure_acceptance(self):
        cmd = [sys.executable, str(ROOT/"scripts/audit_approved_input_283.py"),
               "--summary-only"]
        run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result["restricted_input_283_candidate_count"], 283)
        self.assertEqual(result["release_decision"], "NO_GO")
        strict = subprocess.run(cmd+["--strict"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(strict.returncode, 2, strict.stderr)
        self.assertEqual(json.loads(strict.stdout)["approved_inputs_verified"], 0)


if __name__ == "__main__":
    unittest.main()
