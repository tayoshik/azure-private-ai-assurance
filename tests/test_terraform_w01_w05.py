"""Mutation tests for W01-W05. Text and fixture-only; never Azure or Terraform provider proof."""
from pathlib import Path
import tempfile,shutil,unittest,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_terraform_w01_w05 import check
from terraform_test_helpers import replace_mutation

class TestStage5(unittest.TestCase):
    def test_baseline(self):
        r=check(ROOT);self.assertFalse(r['errors'],r['errors'])
        self.assertEqual(r['azure_live_passes'],0)
    def mutate(self,path,old,new):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            shutil.copytree(ROOT/'infra',root/'infra')
            p=root/path;s=p.read_text()
            p.write_text(replace_mutation(s,old,new))
            r=check(root)
            self.assertEqual(r['status'],'FAIL',(path,old,r))
            self.assertEqual(r['azure_live_passes'],0)
    def test_private_ingress(self):self.mutate('infra/modules/app-service/webapp.tf','public_network_access_enabled = false','public_network_access_enabled = true')
    def test_https(self):self.mutate('infra/modules/app-service/webapp.tf','https_only                    = true','https_only                    = false')
    def test_ftp(self):self.mutate('infra/modules/app-service/webapp.tf','ftp_publish_basic_authentication_enabled       = false','ftp_publish_basic_authentication_enabled       = true')
    def test_webdeploy(self):self.mutate('infra/modules/app-service/webapp.tf','webdeploy_publish_basic_authentication_enabled = false','webdeploy_publish_basic_authentication_enabled = true')
    def test_tls(self):self.mutate('infra/modules/app-service/webapp.tf','minimum_tls_version                 = "1.2"','minimum_tls_version                 = "1.0"')
    def test_scm_tls(self):self.mutate('infra/modules/app-service/webapp.tf','scm_minimum_tls_version             = "1.2"','scm_minimum_tls_version             = "1.0"')
    def test_vnet_route(self):self.mutate('infra/modules/app-service/webapp.tf','vnet_route_all_enabled              = true','vnet_route_all_enabled              = false')
    def test_no_identity(self):self.mutate('infra/modules/app-service/webapp.tf','identity_ids = [var.app_identity_id]','identity_ids = []')
    def test_app_approval(self):self.mutate('infra/modules/app-service/webapp.tf','var.application_contract_approved','true')
    def test_egress_approval(self):self.mutate('infra/modules/app-service/webapp.tf','var.outbound_integration_approved','true')
    def test_service_sku(self):self.mutate('infra/modules/app-service/plan.tf','os_type             = "Linux"','os_type             = "Windows"')
    def test_pe_subresource(self):self.mutate('infra/modules/webapp-private-endpoint/webapp.tf','subresource_names              = ["sites"]','subresource_names              = ["scm"]')
    def test_pe_dns(self):self.mutate('infra/modules/webapp-private-endpoint/webapp.tf','private_dns_zone_ids = [var.webapp_private_dns_zone_id]','private_dns_zone_ids = []')
    def test_pe_approval(self):self.mutate('infra/modules/webapp-private-endpoint/webapp.tf','var.web_private_endpoint_approved','true')
    def test_app_subnet_sep(self):self.mutate('infra/modules/app-service/webapp.tf','var.app_outbound_subnet_id != var.web_inbound_pe_subnet_id','var.app_outbound_subnet_id == var.web_inbound_pe_subnet_id')
    def test_pe_subnet_sep(self):self.mutate('infra/modules/webapp-private-endpoint/webapp.tf','var.web_inbound_pe_subnet_id != var.app_outbound_subnet_id','var.web_inbound_pe_subnet_id == var.app_outbound_subnet_id')
    def test_root_pe_dns(self):self.mutate('infra/environments/dev/main.tf','module.private_dns.zone_ids["privatelink.azurewebsites.net"]','module.private_dns.zone_ids["privatelink.vaultcore.azure.net"]')
    def test_root_module(self):self.mutate('infra/environments/dev/main.tf','module "app_service"','module "missing_app"')
    def test_example_approval(self):self.mutate('infra/environments/dev/terraform.tfvars.example','application_contract_approved   = false','application_contract_approved   = true')
    def test_legacy_swift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);shutil.copytree(ROOT/'infra',root/'infra')
            p=root/'infra/modules/app-service/legacy.tf'
            p.write_text('resource "azurerm_app_service_virtual_network_swift_connection" "legacy" {}')
            self.assertTrue(check(root)['errors'])
    def test_legacy_bad_inline_hcl(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);shutil.copytree(ROOT/'infra',root/'infra')
            p=root/'infra/modules/app-service/variables.tf'
            p.write_text(p.read_text()+'\nvariable "x" { type = bool; default = false }\n')
            self.assertTrue(check(root)['errors'])

if __name__=='__main__':unittest.main()
