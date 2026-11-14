"""W01-W05 mutation regressions. Do not interpret as real Terraform or Azure passes."""
from pathlib import Path
import shutil,tempfile,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from check_terraform_w01_w05 import check

MUTATIONS=[
 ("infra/modules/app-service/webapp.tf","public_network_access_enabled = false","public_network_access_enabled = true"),
 ("infra/modules/app-service/webapp.tf","https_only                    = true","https_only                    = false"),
 ("infra/modules/app-service/webapp.tf","ftp_publish_basic_authentication_enabled       = false","ftp_publish_basic_authentication_enabled       = true"),
 ("infra/modules/app-service/webapp.tf","webdeploy_publish_basic_authentication_enabled = false","webdeploy_publish_basic_authentication_enabled = true"),
 ("infra/modules/app-service/webapp.tf",'ftps_state                        = "Disabled"','ftps_state                        = "AllAllowed"'),
 ("infra/modules/app-service/webapp.tf",'minimum_tls_version               = "1.2"','minimum_tls_version               = "1.0"'),
 ("infra/modules/app-service/webapp.tf",'scm_minimum_tls_version           = "1.2"','scm_minimum_tls_version           = "1.0"'),
 ("infra/modules/app-service/webapp.tf","vnet_route_all_enabled            = true","vnet_route_all_enabled            = false"),
 ("infra/modules/app-service/webapp.tf","identity_ids = [var.app_identity_id]","identity_ids = []"),
 ("infra/modules/app-service/webapp.tf","var.application_contract_approved","true"),
 ("infra/modules/app-service/webapp.tf","var.outbound_integration_approved","true"),
 ("infra/modules/app-service/plan.tf",'os_type             = "Linux"','os_type             = "Windows"'),
 ("infra/modules/webapp-private-endpoint/webapp.tf",'subresource_names              = ["sites"]','subresource_names              = ["scm"]'),
 ("infra/modules/webapp-private-endpoint/webapp.tf","private_dns_zone_ids = [var.webapp_private_dns_zone_id]","private_dns_zone_ids = []"),
 ("infra/modules/webapp-private-endpoint/webapp.tf","var.web_private_endpoint_approved","true"),
 ("infra/modules/app-service/webapp.tf","var.app_outbound_subnet_id != var.web_inbound_pe_subnet_id","var.app_outbound_subnet_id == var.web_inbound_pe_subnet_id"),
 ("infra/modules/webapp-private-endpoint/webapp.tf","var.web_inbound_pe_subnet_id != var.app_outbound_subnet_id","var.web_inbound_pe_subnet_id == var.app_outbound_subnet_id"),
 ("infra/environments/dev/main.tf",'module.private_dns.zone_ids["privatelink.azurewebsites.net"]','module.private_dns.zone_ids["privatelink.vaultcore.azure.net"]'),
 ("infra/environments/dev/main.tf",'module "app_service"','module "missing_app"'),
 ("infra/environments/dev/terraform.tfvars.example","application_contract_approved    = false","application_contract_approved    = true"),
]
class TestW01W05(unittest.TestCase):
 def test_baseline(self):
  r=check(ROOT)
  self.assertFalse(r["errors"],r["errors"])
  self.assertEqual(r["azure_live_passes"],0)
 def run_mutation(self,path,old,new):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   shutil.copytree(ROOT/"infra",root/"infra")
   p=root/path
   contents=p.read_text()
   self.assertIn(old,contents,(path,old))
   p.write_text(contents.replace(old,new,1))
   r=check(root)
   self.assertEqual(r["status"],"FAIL",(path,r))
   self.assertEqual(r["azure_live_passes"],0)
for i,mutation in enumerate(MUTATIONS):
 def make(m):
  return lambda self:self.run_mutation(*m)
 setattr(TestW01W05,f"test_mutation_{i:02d}",make(mutation))
def test_legacy_swift(self):
 with tempfile.TemporaryDirectory() as d:
  root=Path(d)
  shutil.copytree(ROOT/"infra",root/"infra")
  (root/"infra/modules/app-service/conflict.tf").write_text('resource "azurerm_app_service_virtual_network_swift_connection" "bad" {}')
  self.assertEqual(check(root)["status"],"FAIL")
setattr(TestW01W05,"test_mutation_20",test_legacy_swift)
if __name__=="__main__":unittest.main()
