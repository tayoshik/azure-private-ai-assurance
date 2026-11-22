"""Synthetic-only regression tests for AzureRM provider lockfile pin preflight."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_terraform_lock_consistency",
    ROOT / "scripts/verify_terraform_lock_consistency.py",
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class LockConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="terraform-lock-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for rel in module.ROOTS:
            target = self.root / rel
            target.mkdir(parents=True)
            for filename in ("versions.tf", ".terraform.lock.hcl"):
                shutil.copyfile(ROOT / rel / filename, target / filename)

    def f(self, rel, filename):
        return self.root / rel / filename

    def replace(self, rel, filename, before, after):
        path = self.f(rel, filename)
        original = path.read_text(encoding="utf-8")
        self.assertIn(before, original)
        path.write_text(original.replace(before, after, 1), encoding="utf-8")

    def assert_invalid(self):
        result = module.inspect(self.root)
        self.assertEqual(result["classification"], "FAIL_SOURCE")
        self.assertTrue(result["errors"])
        self.assertEqual(result["azure_live_passes"], 0)
        self.assertEqual(result["release_decision"], "NO_GO")

    def test_unmodified_two_lockfiles_match(self):
        result = module.inspect(self.root)
        self.assertEqual(result["classification"], "PASS_SOURCE_LOCK_CONSISTENCY_ONLY")
        self.assertEqual(result["errors"], [])
        self.assertEqual(set(result["locks"]), set(module.ROOTS))
        self.assertEqual(len(set(row["sha256"] for row in result["locks"].values())), 1)
        self.assertEqual(result["terraform_init"], "NOT_EXECUTED_BY_THIS_SCRIPT")
        self.assertEqual(result["terraform_validate"], "NOT_EXECUTED_BY_THIS_SCRIPT")
        self.assertEqual(result["terraform_plan"], "NOT_EXECUTED")
        self.assertEqual(result["terraform_apply"], "NOT_EXECUTED")
        self.assertEqual(result["azure_live_passes"], 0)
        self.assertEqual(result["release_decision"], "NO_GO")

    def test_missing_bootstrap_lock_rejected(self):
        self.f(module.ROOTS[0], ".terraform.lock.hcl").unlink()
        self.assert_invalid()

    def test_missing_dev_lock_rejected(self):
        self.f(module.ROOTS[1], ".terraform.lock.hcl").unlink()
        self.assert_invalid()

    def test_missing_versions_file_rejected(self):
        self.f(module.ROOTS[1], "versions.tf").unlink()
        self.assert_invalid()

    def test_provider_source_is_not_accepted_if_changed(self):
        self.replace(module.ROOTS[0], "versions.tf",
                     'source  = "hashicorp/azurerm"',
                     'source  = "notapproved/azurerm"')
        self.assert_invalid()

    def test_provider_version_pin_in_terraform_config_required(self):
        self.replace(module.ROOTS[0], "versions.tf",
                     'version = "= 4.66.0"', 'version = "= 5.0.0"')
        self.assert_invalid()

    def test_terraform_cli_version_constraint_required(self):
        self.replace(module.ROOTS[0], "versions.tf",
                     'required_version = ">= 1.9.0, < 2.0.0"',
                     'required_version = ">= 1.8.0"')
        self.assert_invalid()

    def test_lockfile_version_drift_rejected(self):
        self.replace(module.ROOTS[1], ".terraform.lock.hcl",
                     'version     = "4.66.0"',
                     'version     = "5.0.0"')
        self.assert_invalid()

    def test_lockfile_constraint_drift_rejected(self):
        self.replace(module.ROOTS[0], ".terraform.lock.hcl",
                     'constraints = "4.66.0"',
                     'constraints = ">= 4.0.0"')
        self.assert_invalid()

    def test_wrong_provider_namespace_rejected(self):
        self.replace(module.ROOTS[0], ".terraform.lock.hcl",
                     'provider "registry.terraform.io/hashicorp/azurerm"',
                     'provider "registry.terraform.io/other/azurerm"')
        self.assert_invalid()

    def test_loss_of_h1_digest_rejected(self):
        content = self.f(module.ROOTS[0], ".terraform.lock.hcl")
        rows = [line for line in content.read_text(encoding="utf-8").splitlines()
                if '"h1:' not in line]
        content.write_text("\n".join(rows) + "\n", encoding="utf-8")
        self.assert_invalid()

    def test_loss_of_zh_digest_rejected(self):
        content = self.f(module.ROOTS[0], ".terraform.lock.hcl")
        rows = [line for line in content.read_text(encoding="utf-8").splitlines()
                if '"zh:' not in line]
        content.write_text("\n".join(rows) + "\n", encoding="utf-8")
        self.assert_invalid()

    def test_duplicate_digest_rejected(self):
        path = self.f(module.ROOTS[0], ".terraform.lock.hcl")
        body = path.read_text(encoding="utf-8")
        digest = next(line for line in body.splitlines() if '"zh:' in line)
        path.write_text(body.replace(digest, digest + "\n" + digest, 1),
                        encoding="utf-8")
        self.assert_invalid()

    def test_malformed_checksum_rejected(self):
        path = self.f(module.ROOTS[0], ".terraform.lock.hcl")
        body = path.read_text(encoding="utf-8")
        path.write_text(body.replace('"zh:00f3d73192f7d7824daaccf9732ff228f40ff9910aab4aba608dd2bd96f0c8b4"',
                                     '"zh:bad"', 1), encoding="utf-8")
        self.assert_invalid()

    def test_two_valid_but_different_locks_need_review(self):
        path = self.f(module.ROOTS[1], ".terraform.lock.hcl")
        body = path.read_text(encoding="utf-8")
        # Still a syntactically valid checksum, but different from bootstrap.
        original = "zh:00f3d73192f7d7824daaccf9732ff228f40ff9910aab4aba608dd2bd96f0c8b4"
        self.assertIn(original, body)
        path.write_text(body.replace(original, "zh:" + "0" * 64, 1),
                        encoding="utf-8")
        self.assert_invalid()

    def test_adding_second_provider_is_rejected(self):
        path = self.f(module.ROOTS[0], ".terraform.lock.hcl")
        path.write_text(path.read_text(encoding="utf-8") +
                        '\nprovider "registry.terraform.io/hashicorp/random" {\n'
                        '  version = "3.6.0"\n  hashes = ["zh:' + "a" * 64 + '"]\n}\n',
                        encoding="utf-8")
        self.assert_invalid()


if __name__ == "__main__":
    unittest.main()
