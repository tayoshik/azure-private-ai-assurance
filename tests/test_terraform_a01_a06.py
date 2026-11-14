"""A01-A06 static mutation regression. NOT an Azure integration test."""
from pathlib import Path
import sys
import tempfile
import shutil
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_terraform_a01_a06 import check
from terraform_test_helpers import replace_mutation

class TestAIData(unittest.TestCase):
    def test_baseline(self):
        self.assertFalse(check(ROOT)['errors'])

    def mutate(self,path,old,new):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)
            shutil.copytree(ROOT/'infra',target/'infra')
            p=target/path
            source=p.read_text()
            p.write_text(replace_mutation(source,old,new))
            report=check(target)
            self.assertNotEqual(report['errors'],[],(path,old))
            self.assertEqual(report['azure_live_passes'],0)

    def test_openai_public(self):self.mutate('infra/modules/azure-openai/main.tf','public_network_access_enabled = false','public_network_access_enabled = true')
    def test_openai_local_auth(self):self.mutate('infra/modules/azure-openai/main.tf','local_auth_enabled             = false','local_auth_enabled             = true')
    def test_openai_model_unpinned(self):self.mutate('infra/modules/azure-openai/main.tf','version_upgrade_option = "NoAutoUpgrade"','version_upgrade_option = "OnceNewDefaultVersionAvailable"')
    def test_openai_model_missing_gate(self):self.mutate('infra/modules/azure-openai/main.tf','var.model_deployment_approved','true')
    def test_search_public(self):self.mutate('infra/modules/ai-search/main.tf','public_network_access_enabled = false','public_network_access_enabled = true')
    def test_search_key_auth(self):self.mutate('infra/modules/ai-search/main.tf','local_authentication_enabled  = false','local_authentication_enabled  = true')
    def test_search_bypass(self):self.mutate('infra/modules/ai-search/main.tf','network_rule_bypass_option    = "None"','network_rule_bypass_option    = "AzureServices"')
    def test_cosmos_public(self):self.mutate('infra/modules/cosmos-db/main.tf','public_network_access_enabled = false','public_network_access_enabled = true')
    def test_cosmos_key_auth(self):self.mutate('infra/modules/cosmos-db/main.tf','local_authentication_disabled = true','local_authentication_disabled = false')
    def test_cosmos_wrong_provider_attribute(self):self.mutate('infra/modules/cosmos-db/main.tf','local_authentication_disabled = true','local_authentication_enabled = false')
    def test_cosmos_backup(self):self.mutate('infra/modules/cosmos-db/main.tf','type = "Continuous"','type = "Periodic"')
    def test_openai_pe_subresource(self):self.mutate('infra/modules/ai-private-endpoints/main.tf','subresource_names              = ["account"]','subresource_names              = ["sites"]')
    def test_search_pe_subresource(self):self.mutate('infra/modules/ai-private-endpoints/main.tf','subresource_names              = ["searchService"]','subresource_names              = ["wrong"]')
    def test_cosmos_pe_subresource(self):self.mutate('infra/modules/ai-private-endpoints/main.tf','subresource_names              = ["Sql"]','subresource_names              = ["MongoDB"]')
    def test_dns_mismatch(self):self.mutate('infra/modules/ai-private-endpoints/main.tf','/privatelink.documents.azure.com','/privatelink.mongo.cosmos.azure.com')
    def test_openai_role_escalated(self):self.mutate('infra/modules/ai-data-rbac/main.tf','"Cognitive Services OpenAI User"','"Owner"')
    def test_search_role_escalated(self):self.mutate('infra/modules/ai-data-rbac/main.tf','"Search Index Data Reader"','"Contributor"')
    def test_cosmos_role_escalated(self):self.mutate('infra/modules/ai-data-rbac/main.tf','var.cosmos_write_approved ?','true ?')
    def test_cosmos_scope_broadened(self):self.mutate('infra/modules/ai-data-rbac/main.tf','/dbs/${var.cosmos_database_name}/colls/${var.cosmos_container_name}','')
    def test_example_approval_default(self):self.mutate('infra/environments/dev/terraform.tfvars.example','ai_data_rbac_approved              = false','ai_data_rbac_approved              = true')
    def test_root_wiring_removed(self):self.mutate('infra/environments/dev/main.tf','module "ai_data_rbac"','module "renamed"')
    def test_root_network_dependency(self):self.mutate('infra/environments/dev/main.tf','depends_on                 = [module.network]','depends_on                 = []')

if __name__=='__main__':unittest.main()
