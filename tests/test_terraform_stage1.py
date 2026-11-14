"""Purely offline text-guard regression. No Azure calls or Terraform CLI."""
import sys
import tempfile
import unittest
from pathlib import Path
from shutil import copytree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_terraform_stage1 import EXPECTED, check, lexical_balance


class TerraformStage1Tests(unittest.TestCase):
    def test_source_tree_passes(self):
        self.assertEqual(check()["state"], "PASS_OFFLINE_TEXT_REVIEW_ONLY")

    def test_no_real_success_claim(self):
        r = check()
        self.assertEqual(r["azure_live_passes"], 0)
        self.assertEqual(r["release_decision"], "NO_GO")
        self.assertEqual(r["terraform_cli_validation"], "NOT_EXECUTED")

    def test_all_contract_files(self):
        self.assertEqual(len(EXPECTED), 10)

    def test_detect_missing_file(self):
        with tempfile.TemporaryDirectory() as td:
            copytree(ROOT / "infra", Path(td) / "infra")
            (Path(td) / "infra/bootstrap/main.tf").unlink()
            self.assertEqual(check(td)["state"], "FAIL")

    def test_detect_public_storage(self):
        with tempfile.TemporaryDirectory() as td:
            copytree(ROOT / "infra", Path(td) / "infra")
            p = Path(td) / "infra/bootstrap/main.tf"
            p.write_text(p.read_text().replace('public_network_access_enabled   = false', 'public_network_access_enabled   = true'))
            self.assertEqual(check(td)["state"], "FAIL")

    def test_detect_key_auth(self):
        with tempfile.TemporaryDirectory() as td:
            copytree(ROOT / "infra", Path(td) / "infra")
            p=Path(td)/"infra/bootstrap/main.tf"
            p.write_text(p.read_text().replace('shared_access_key_enabled       = false','shared_access_key_enabled       = true'))
            self.assertEqual(check(td)["state"],"FAIL")

    def test_detect_bad_subnet_delegation(self):
        with tempfile.TemporaryDirectory() as td:
            copytree(ROOT / "infra", Path(td) / "infra")
            p=Path(td)/"infra/modules/network/main.tf"
            p.write_text(p.read_text().replace('Microsoft.Web/serverFarms','Microsoft.Web/WRONG'))
            self.assertEqual(check(td)["state"],"FAIL")

    def test_detect_bootstrap_self_backend(self):
        with tempfile.TemporaryDirectory() as td:
            copytree(ROOT / "infra", Path(td) / "infra")
            p=Path(td)/"infra/bootstrap/versions.tf"
            p.write_text(p.read_text()+'\nterraform { backend "azurerm" {} }\n')
            self.assertEqual(check(td)["state"],"FAIL")

    def test_detect_missing_dns_zone(self):
        with tempfile.TemporaryDirectory() as td:
            copytree(ROOT / "infra", Path(td) / "infra")
            p=Path(td)/"infra/environments/dev/variables.tf"
            p.write_text(p.read_text().replace('privatelink.documents.azure.com','some.bad.domain'))
            self.assertEqual(check(td)["state"],"FAIL")

    def test_syntax_balancing_good(self):
        self.assertTrue(lexical_balance('resource "example" "x" { name = "ok" }'))

    def test_syntax_balancing_bad(self):
        self.assertFalse(lexical_balance('resource "example" "x" { name = "ok" '))

    def test_syntax_balancing_comments(self):
        self.assertTrue(lexical_balance('# not a brace: }\nlocals { x = "\\\"{\\\"" /* } */ }'))

    def test_no_real_environment_settings(self):
        p=(ROOT/"infra/environments/dev/terraform.tfvars.example").read_text()
        self.assertIn('00000000-0000-0000-0000-000000000000',p)

    def test_restricted_backend_example(self):
        p=(ROOT/"infra/environments/dev/backend.azurerm.example.hcl").read_text()
        self.assertIn('use_oidc             = true',p)
        self.assertNotIn('client_secret',p)


if __name__ == '__main__':
    unittest.main()
