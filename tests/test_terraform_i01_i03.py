import sys
import tempfile
import unittest
from pathlib import Path
from shutil import copytree
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_terraform_i01_i03 import check

class Stage3Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        copytree(ROOT/'infra',self.root/'infra')
    def tearDown(self):self.tmp.cleanup()
    def rewrite(self,name,old,new):
        p=self.root/name
        s=p.read_text()
        assert old in s,old
        p.write_text(s.replace(old,new))
    def detected(self):
        r=check(self.root)
        self.assertEqual(r['state'],'FAIL',r)
        self.assertTrue(r['errors'])
    def test_unmodified_pass(self):
        r=check(self.root)
        self.assertEqual(r['state'],'PASS_OFFLINE_I01_I03_TEXT_ONLY',r)
        self.assertEqual(r['azure_live_passes'],0)
        self.assertEqual(r['release_decision'],'NO_GO')
        self.assertEqual(r['terraform_cli_validation'],'NOT_EXECUTED')
    def test_missing_file(self):
        (self.root/'infra/modules/identity/main.tf').unlink();self.detected()
    def test_missing_app_identity(self):
        self.rewrite('infra/modules/identity/main.tf','azurerm_user_assigned_identity" "app','azurerm_user_assigned_identity" "other');self.detected()
    def test_missing_gateway_identity(self):
        self.rewrite('infra/modules/identity/main.tf','azurerm_user_assigned_identity" "gateway','azurerm_user_assigned_identity" "other');self.detected()
    def test_vault_public_access(self):
        self.rewrite('infra/modules/key-vault/main.tf','public_network_access_enabled = false','public_network_access_enabled = true');self.detected()
    def test_vault_without_purge(self):
        self.rewrite('infra/modules/key-vault/main.tf','purge_protection_enabled      = true','purge_protection_enabled      = false');self.detected()
    def test_vault_legacy_auth(self):
        self.rewrite('infra/modules/key-vault/main.tf','rbac_authorization_enabled    = true','rbac_authorization_enabled    = false');self.detected()
    def test_vault_acl_bypass(self):
        self.rewrite('infra/modules/key-vault/main.tf','bypass         = "None"','bypass         = "AzureServices"');self.detected()
    def test_missing_role_scope(self):
        self.rewrite('infra/modules/key-vault/main.tf','scope                = azurerm_key_vault.workload.id','scope                = var.resource_group_name');self.detected()
    def test_broad_role(self):
        self.rewrite('infra/modules/key-vault/main.tf','role_definition_name = "Key Vault Secrets User"','role_definition_name = "Owner"');self.detected()
    def test_default_approval_true(self):
        self.rewrite('infra/environments/dev/terraform.tfvars.example','key_vault_configuration_approved    = false','key_vault_configuration_approved    = true');self.detected()
    def test_private_endpoint_wrong_group(self):
        self.rewrite('infra/modules/private-endpoints/key-vault.tf','subresource_names              = ["vault"]','subresource_names              = ["blob"]');self.detected()
    def test_private_endpoint_wrong_dns(self):
        self.rewrite('infra/environments/dev/main.tf','privatelink.vaultcore.azure.net','privatelink.blob.core.windows.net');self.detected()
    def test_missing_private_endpoint_approval(self):
        self.rewrite('infra/modules/private-endpoints/key-vault.tf','condition     = var.key_vault_private_endpoint_approved','condition     = true');self.detected()
    def test_missing_role_approval(self):
        self.rewrite('infra/modules/key-vault/main.tf','condition     = var.role_assignment_approval_confirmed','condition     = true');self.detected()
    def test_missing_root_connection(self):
        self.rewrite('infra/environments/dev/main.tf','module "key_vault_private_endpoint"','module "wrong"');self.detected()
    def test_detect_certificate_material_resource(self):
        p=self.root/'infra/modules/key-vault/main.tf';p.write_text(p.read_text()+'\nresource "azurerm_key_vault_secret" "bad" { name="oops" }\n');self.detected()
    def test_failure_on_unbalanced_hcl(self):
        p=self.root/'infra/modules/key-vault/main.tf';p.write_text(p.read_text()+'{\n');self.detected()

if __name__=='__main__':unittest.main()
