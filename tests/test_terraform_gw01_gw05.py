"""Offline mutation/review tests. No Azure, Terraform provider or network calls."""
from pathlib import Path
import shutil,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_terraform_gw01_gw05 import check
from terraform_test_helpers import replace_mutation
class TestGatewayStage6(unittest.TestCase):
    def test_clean_baseline(self):
        r=check(ROOT);self.assertFalse(r['errors'],r['errors'])
        self.assertEqual(r['status'],'PASS_OFFLINE_TEXT_ONLY')
    def mutate(self,rel,before,after):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);shutil.copytree(ROOT/'infra',root/'infra')
            p=root/rel;s=p.read_text()
            p.write_text(replace_mutation(s,before,after))
            r=check(root);self.assertEqual(r['status'],'FAIL',(rel,before,r))
            self.assertEqual(r['azure_live_passes'],0)
    def test_public_frontend(self):self.mutate('infra/modules/application-gateway/gateway.tf','private_ip_address_allocation = "Static"','private_ip_address_allocation = "Dynamic"')
    def test_public_ip_field(self):self.mutate('infra/modules/application-gateway/gateway.tf','private_ip_address            = var.private_frontend_ip','public_ip_address_id = var.test_public_id')
    def test_gateway_identity(self):self.mutate('infra/modules/application-gateway/gateway.tf','identity_ids = [var.gateway_identity_id]','identity_ids = []')
    def test_tls_cert_reference(self):self.mutate('infra/modules/application-gateway/gateway.tf','key_vault_secret_id = var.key_vault_certificate_secret_versionless_id','key_vault_secret_id = ""')
    def test_backend_fqdn(self):self.mutate('infra/modules/application-gateway/gateway.tf','fqdns = [var.backend_app_fqdn]','fqdns = ["8.8.8.8"]')
    def test_backend_host(self):self.mutate('infra/modules/application-gateway/gateway.tf','host_name             = var.backend_app_fqdn','host_name             = "wrong.invalid"')
    def test_probe_host(self):self.mutate('infra/modules/application-gateway/gateway.tf','host                                      = var.backend_app_fqdn','host                                      = "wrong.invalid"')
    def test_approved_feature(self):self.mutate('infra/modules/application-gateway/gateway.tf','var.private_gateway_feature_approved && var.gateway_ipam_and_routes_approved','true')
    def test_approved_tls(self):self.mutate('infra/modules/application-gateway/gateway.tf','var.backend_dns_tls_approved && var.certificate_import_and_rbac_approved','true')
    def test_waf_prevention_gate(self):self.mutate('infra/modules/application-gateway/waf-policy.tf','var.waf_mode == "Detection" || var.waf_prevention_approved','true')
    def test_waf_drs(self):self.mutate('infra/modules/application-gateway/waf-policy.tf','type    = "Microsoft_DefaultRuleSet"','type    = "OWASP"')
    def test_waf_log(self):self.mutate('infra/modules/application-gateway/diagnostics.tf','category = "ApplicationGatewayFirewallLog"','category = "ApplicationGatewayPerformanceLog"')
    def test_dedicated_logs(self):self.mutate('infra/modules/application-gateway/diagnostics.tf','log_analytics_destination_type = "Dedicated"','log_analytics_destination_type = "AzureDiagnostics"')
    def test_monitor_public_ingestion(self):self.mutate('infra/modules/monitoring/main.tf','internet_ingestion_enabled = false','internet_ingestion_enabled = true')
    def test_approval_default(self):self.mutate('infra/environments/dev/terraform.tfvars.example','gateway_waf_prevention_approved = false','gateway_waf_prevention_approved = true')
    def test_root_wiring(self):self.mutate('infra/environments/dev/main.tf','backend_app_fqdn = module.app_service.default_hostname','backend_app_fqdn = "wrong.invalid"')
    def test_gateway_network_delegation(self):self.mutate('infra/modules/network/main.tf','Microsoft.Network/applicationGateways','Microsoft.Web/serverFarms')
    def test_gateway_platform_probe(self):self.mutate('infra/modules/network/policy.tf','source_address_prefix       = "AzureLoadBalancer"','source_address_prefix       = "Internet"')
if __name__=='__main__':unittest.main()
