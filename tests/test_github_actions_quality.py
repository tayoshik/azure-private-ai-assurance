"""Offline mutation regressions for GitHub Actions status/Ruleset quality gates."""
from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_github_actions_quality as quality


class WorkflowQualityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workflow-quality-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / quality.WORKFLOWS, self.root / quality.WORKFLOWS)
        manifest = self.root / quality.PINS_MANIFEST
        manifest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / quality.PINS_MANIFEST, manifest)

    def source(self, name):
        return self.root / quality.WORKFLOWS / name

    def mutate(self, name, old, new):
        path = self.source(name)
        content = path.read_text(encoding="utf-8")
        self.assertIn(old, content)
        path.write_text(content.replace(old, new, 1), encoding="utf-8")

    def reject(self):
        result = quality.inspect(self.root, include_workflows=False)
        self.assertEqual(result["status"], "INVALID_WORKFLOW_POLICY")
        self.assertTrue(result["errors"])
        self.assertEqual(result["azure_live_passes_verified"], 0)
        self.assertEqual(result["release_decision"], "NO_GO")
        return result

    def test_34_workflows_and_all_check_contexts_are_unique(self):
        report = quality.inspect(self.root)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["status"], "SOURCE_WORKFLOW_POLICY_VERIFIED_ONLY")
        self.assertEqual(report["workflow_count"], 35)
        self.assertEqual(report["total_job_definitions"], 37)
        self.assertEqual(report["unique_job_contexts"], 37)
        self.assertEqual(report["duplicate_status_contexts"], [])
        self.assertEqual(len(report["workflows"]), 35)

    def test_exact_two_unfiltered_ruleset_jobs_are_retained(self):
        result = quality.inspect(self.root)
        self.assertEqual(result["required_ruleset_status_contexts"],
                         ["offline-main-gate", "offline-catalogue"])
        for name in ("offline-validation.yml", "publication-integrity.yml"):
            row = result["workflows"][name]
            self.assertEqual(row["events"], ["pull_request", "push"])
            self.assertFalse(row["path_filtered_push"])
            self.assertFalse(row["path_filtered_pull_request"])

    def test_named_scoped_jobs_are_unique_and_trigger_on_changed_workflow(self):
        report = quality.inspect(self.root)
        for name, job in quality.SCOPED_JOBS.items():
            with self.subTest(name=name):
                row = report["workflows"][name]
                self.assertEqual(row["jobs"], [job])
                self.assertEqual(row["events"],
                                 ["pull_request", "push", "workflow_dispatch"]
                                 if name != "terraform-stage5-webapp-static.yml"
                                 else ["pull_request", "push"])
                self.assertTrue(row["path_filtered_pull_request"])
                self.assertTrue(row["path_filtered_push"])

    def test_all_34_automated_pushes_are_main_only(self):
        report = quality.inspect(self.root)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["remaining_unscoped_push_workflows"], [])
        self.assertEqual(report["main_only_push_workflow_count"], 34)
        for name, workflow in report["workflows"].items():
            if "push" in workflow["events"]:
                self.assertIn("pull_request", workflow["events"], name)

    def test_nine_historically_unfiltered_pr_workflows_remain_broad(self):
        report = quality.inspect(self.root)
        self.assertEqual(len(quality.BROAD_PR_NO_FILTER), 9)
        for name in quality.BROAD_PR_NO_FILTER:
            with self.subTest(name=name):
                self.assertFalse(report["workflows"][name]["path_filtered_pull_request"])

    def test_old_feature_push_trigger_is_blocked(self):
        self.mutate("phase3-source-recovery.yml",
                    "  push:\n    branches: [main]\n",
                    "  push:\n")
        self.reject()

    def test_push_branch_set_to_feature_is_blocked(self):
        self.mutate("terraform-stage1-static.yml",
                    "    branches: [main]", "    branches: [feature/test]")
        self.reject()

    def test_duplicate_main_and_feature_push_branches_are_blocked(self):
        self.mutate("terraform-q01-q02-offline.yml",
                    "    branches: [main]", "    branches: [main, test]")
        self.reject()

    def test_filtered_pr_path_cannot_omit_original_source(self):
        self.mutate("english-catalogue-validation.yml",
                    "  pull_request:\n    paths:\n      - 'docs/phase1-220-english-tests.md'",
                    "  pull_request:\n    paths:\n      - 'not-a-test-path.md'")
        self.reject()

    def test_filtered_pr_must_self_trigger_on_workflow_edits(self):
        self.mutate("terraform-stage4-ai-data-static.yml",
                    "      - '.github/workflows/terraform-stage4-ai-data-static.yml'\n  workflow_dispatch:",
                    "  workflow_dispatch:")
        self.reject()

    def test_previous_broad_pr_must_not_be_narrowed(self):
        self.mutate("azure-rest03-offline.yml",
                    "  pull_request:\n  workflow_dispatch:\n",
                    "  pull_request:\n    paths:\n      - 'scripts/rest03_resource_audit.py'\n  workflow_dispatch:\n")
        self.reject()

    def test_missing_workflow_is_not_silent_success(self):
        self.source("publication-integrity.yml").unlink()
        self.reject()

    def test_renaming_required_check_fails(self):
        self.mutate("offline-validation.yml", "  offline-main-gate:",
                    "  changed-required-check:")
        self.reject()

    def test_existing_unscoped_check_name_collision_fails(self):
        self.mutate("terraform-stage6-gateway-static.yml",
                    "  stage6-gateway-contracts:", "  stage3-identity-vault-contracts:")
        report = self.reject()
        self.assertTrue(any("duplicate status context" in x for x in report["errors"]))

    def test_required_checkout_cannot_use_mutable_version_tag(self):
        self.mutate("offline-validation.yml", quality.CHECKOUT,
                    "actions/checkout@v4")
        self.reject()

    def test_required_checkout_credentials_must_be_disabled(self):
        self.mutate("publication-integrity.yml",
                    "persist-credentials: false", "persist-credentials: true")
        self.reject()

    def test_required_pull_request_must_not_be_path_filtered(self):
        self.mutate("offline-validation.yml",
                    "  pull_request:\npermissions:",
                    "  pull_request:\n    paths:\n      - 'docs/**'\npermissions:")
        self.reject()

    def test_required_main_branch_must_be_targeted(self):
        self.mutate("publication-integrity.yml", "branches: [main]",
                    "branches: [develop]")
        self.reject()

    def test_required_offline_command_cannot_be_removed(self):
        self.mutate("offline-validation.yml", "python3 scripts/validate_package.py",
                    "echo skip validation")
        self.reject()

    def test_required_ignore_failure_is_denied(self):
        self.mutate("offline-validation.yml",
                    "      - name: Validate package metadata",
                    "      - continue-on-error: true\n        name: Validate package metadata")
        self.reject()

    def test_push_on_feature_branch_does_not_replace_pr_check(self):
        self.mutate("terraform-stage5-webapp-static.yml",
                    "    branches: [main]\n", "")
        self.reject()

    def test_scoped_pr_path_filter_must_match_push_paths(self):
        self.mutate("terraform-stage6-gateway-static.yml",
                    "  pull_request:\n    paths:\n      - 'infra/modules/application-gateway/**'",
                    "  pull_request:\n    paths:\n      - 'some-other-path/**'")
        self.reject()

    def test_scoped_workflow_must_self_trigger(self):
        self.mutate("terraform-stage3-identity-vault-static.yml",
                    "      - '.github/workflows/terraform-stage3-identity-vault-static.yml'",
                    "      - '.github/workflows/other-workflow.yml'")
        self.reject()

    def test_no_pull_request_target(self):
        self.mutate("terraform-stage5-webapp-static.yml",
                    "  pull_request:\n", "  pull_request_target:\n")
        self.reject()

    def test_no_write_contents_permission(self):
        self.mutate("publication-integrity.yml",
                    "  contents: read", "  contents: write")
        self.reject()

    def test_manual_provider_validation_remains_dispatch_only(self):
        self.mutate("terraform-stage4-provider-validate.yml",
                    "  workflow_dispatch:\n", "  push:\n    branches: [main]\n")
        self.reject()

    def test_all_actions_are_approved_full_sha_pins(self):
        result = quality.inspect(self.root)
        self.assertEqual(result["remaining_unpinned_action_workflows"], [])
        self.assertEqual(result["approved_sha_pin_count"], 5)
        self.assertEqual(result["sha_pin_manifest"], quality.PINS_MANIFEST)
        self.assertEqual(result["status"], "SOURCE_WORKFLOW_POLICY_VERIFIED_ONLY")

    def test_unapproved_action_even_with_a_sha_is_denied(self):
        self.mutate("terraform-stage1-static.yml",
                    quality.CHECKOUT,
                    "actions/checkout@" + "0" * 40)
        self.reject()

    def test_mutable_tag_in_optional_workflow_is_denied(self):
        self.mutate("azure-rest04-offline.yml",
                    quality.CHECKOUT, "actions/checkout@v4")
        self.reject()

    def test_untrusted_external_action_is_denied(self):
        self.mutate("azure-rest03-offline.yml",
                    quality.CHECKOUT,
                    "untrusted/checkout@" + "a" * 40)
        self.reject()

    def test_optional_checkout_must_not_persist_credentials(self):
        self.mutate("terraform-stage1-static.yml",
                    "persist-credentials: false", "persist-credentials: true")
        self.reject()

    def test_individual_multistep_checkouts_must_disable_credentials(self):
        self.mutate("terraform-provider-schema-real.yml",
                    "persist-credentials: false", "persist-credentials: true")
        self.reject()

    def test_pinned_actions_manifest_tampering_is_denied(self):
        path = self.root / quality.PINS_MANIFEST
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["approved_refs"][0]["uses"] = "actions/checkout@" + "f" * 40
        path.write_text(json.dumps(manifest), encoding="utf-8")
        self.reject()

    def test_missing_action_pin_manifest_is_denied(self):
        (self.root / quality.PINS_MANIFEST).unlink()
        self.reject()

    def test_strict_denies_azure_acceptance_while_static_audit_passes(self):
        with redirect_stdout(io.StringIO()) as captured:
            self.assertEqual(quality.main(["--root", str(self.root), "--summary-only"]), 0)
        report = json.loads(captured.getvalue())
        self.assertEqual(report["source_workflows_executed"], 0)
        self.assertEqual(report["azure_live_passes_verified"], 0)
        self.assertEqual(report["release_decision"], "NO_GO")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(quality.main(
                ["--root", str(self.root), "--summary-only", "--strict"]), 2)


if __name__ == "__main__":
    unittest.main()
