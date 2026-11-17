"""Synthetic tests for the G03/Q01 source preflight (not provider verification)."""
from __future__ import annotations
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('terraform_provider_preflight', ROOT/'scripts/terraform_provider_preflight.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ProviderPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root/'infra').mkdir()
        shutil.copytree(ROOT/'infra', self.root/'infra', dirs_exist_ok=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_baseline_reports_unverified(self):
        result = MODULE.audit(self.root)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['status'], 'PASS_SOURCE_WITH_PROVIDER_GATES_NOT_READY')
        self.assertEqual(result['azure_live_passes'], 0)
        self.assertEqual(result['release_decision'], 'NO_GO')
        self.assertEqual(result['validate'], 'NOT_EXECUTED')

    def test_source_contains_both_reviewed_candidate_locks(self):
        result = MODULE.audit(self.root)
        self.assertEqual(set(result['lockfiles'].values()), {'PRESENT_UNVERIFIED'})
        self.assertEqual(result['release_decision'], 'NO_GO')

    def test_strict_is_not_ready(self):
        (self.root/'infra/bootstrap/.terraform.lock.hcl').unlink(missing_ok=True)
        self.assertEqual(MODULE.audit(self.root, require_lock=True)['status'], 'NOT_READY_PROVIDER_GATES')

    def test_changed_provider_pin_is_rejected(self):
        p = self.root/'infra/bootstrap/versions.tf'
        p.write_text(p.read_text().replace('4.66.0', '5.0.0'))
        self.assertTrue(MODULE.audit(self.root)['errors'])

    def test_bootstrap_self_remote_backend_rejected(self):
        p = self.root/'infra/bootstrap/versions.tf'
        p.write_text(p.read_text() + '\nterraform { backend "azurerm" {} }\n')
        # Detection requires a standalone backend declaration in the source.
        self.assertTrue(MODULE.audit(self.root)['errors'])

    def test_dev_remote_backend_required(self):
        p = self.root/'infra/environments/dev/versions.tf'
        p.write_text(p.read_text().replace('backend "azurerm" {}', ''))
        self.assertTrue(MODULE.audit(self.root)['errors'])

    def test_missing_root_is_rejected(self):
        p = self.root/'infra/bootstrap/versions.tf'
        p.unlink()
        self.assertTrue(MODULE.audit(self.root)['errors'])

    def test_fake_lock_version_rejected(self):
        p = self.root/'infra/bootstrap/.terraform.lock.hcl'
        p.write_text('provider "registry.terraform.io/hashicorp/azurerm" {\n version="5.0.0"\n hashes=["zh:fake"]\n}\n')
        self.assertTrue(MODULE.audit(self.root)['errors'])

    def test_missing_lock_keeps_no_go(self):
        for root in MODULE.ROOTS:
            (self.root/root/'.terraform.lock.hcl').unlink(missing_ok=True)
        obj = MODULE.audit(self.root)
        self.assertEqual(obj['lockfiles']['infra/bootstrap'], 'MISSING')
        self.assertEqual(obj['lockfiles']['infra/environments/dev'], 'MISSING')
        self.assertEqual(obj['release_decision'], 'NO_GO')


if __name__ == '__main__':
    unittest.main()