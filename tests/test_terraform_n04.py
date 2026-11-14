"""N04 mutation regression, deliberately without Terraform CLI or Azure auth."""
from pathlib import Path
from shutil import copytree
from tempfile import TemporaryDirectory
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_terraform_n04 import check, find_resource

class N04Tests(unittest.TestCase):
    def test_source_pass(self):
        self.assertEqual(check()['state'],'PASS_OFFLINE_N04_TEXT_ONLY')
    def test_azure_not_pass(self):
        d=check()
        self.assertEqual(d['azure_live_passes'],0)
        self.assertEqual(d['live_acceptance_not_ready'],1716)
        self.assertEqual(d['release_decision'],'NO_GO')
        self.assertEqual(d['terraform_cli_validation'],'NOT_EXECUTED')
    def mutate(self,rel,old,new):
        with TemporaryDirectory() as d:
            copytree(ROOT/'infra',Path(d)/'infra')
            p=Path(d)/rel
            self.assertIn(old,p.read_text())
            p.write_text(p.read_text().replace(old,new,1))
            return check(d)['state']
    def test_unapproved_client_source_broadening(self):
        self.assertEqual(self.mutate('infra/modules/network/policy.tf','source_address_prefixes     = var.approved_client_cidrs','source_address_prefixes     = ["0.0.0.0/0"]'),'FAIL')
    def test_missing_platform_probe(self):
        self.assertEqual(self.mutate('infra/modules/network/policy.tf','"AzureLoadBalancer"','"OtherSource"'),'FAIL')
    def test_missing_gateway_deny(self):
        self.assertEqual(self.mutate('infra/modules/network/policy.tf','resource "azurerm_network_security_rule" "gateway_deny_other_inbound"','resource "azurerm_network_security_rule" "gateway_deny_REMOVED"'),'FAIL')
    def test_missing_app_egress_deny(self):
        self.assertEqual(self.mutate('infra/modules/network/policy.tf','resource "azurerm_network_security_rule" "app_deny_other_outbound"','resource "azurerm_network_security_rule" "REMOVED"'),'FAIL')
    def test_wrong_web_pe_source(self):
        self.assertEqual(self.mutate('infra/modules/network/policy.tf','source_address_prefix       = var.subnet_cidrs.app_gateway','source_address_prefix       = "0.0.0.0/0"'),'FAIL')
    def test_disable_pe_network_policies(self):
        self.assertEqual(self.mutate('infra/modules/network/main.tf','private_endpoint_network_policies = "Enabled"','private_endpoint_network_policies = "Disabled"'),'FAIL')
    def test_missing_gateway_feature_gate(self):
        self.assertEqual(self.mutate('infra/modules/network/policy.tf','var.gateway_network_isolation_approved && ','true && '),'FAIL')
    def test_unapproved_default_true(self):
        self.assertEqual(self.mutate('infra/modules/network/variables.tf','variable "network_policy_approved" {\n  type        = bool\n  default     = false','variable "network_policy_approved" {\n  type        = bool\n  default     = true'),'FAIL')
    def test_unwired_policy_variable(self):
        self.assertEqual(self.mutate('infra/environments/dev/main.tf','network_policy_approved = var.network_policy_approved','network_policy_approved = true'),'FAIL')
    def test_gateway_udr_forbidden(self):
        self.assertEqual(self.mutate('infra/modules/network/policy.tf','resource "azurerm_subnet_route_table_association" "app_outbound"','resource "azurerm_subnet_route_table_association" "app_gateway"'),'FAIL')
    def test_no_az_login_apply_in_n04_script(self):
        s=(ROOT/'scripts/check_terraform_n04.py').read_text()
        self.assertNotIn('subprocess.run(',s)
        self.assertNotIn('os.system(',s)
    def test_nsg_count(self):
        self.assertEqual(check()['nsg_count'],4)
    def test_find_resource(self):
        s=(ROOT/'infra/modules/network/policy.tf').read_text()
        self.assertIn('AllowApprovedClients443',find_resource(s,'azurerm_network_security_rule','gateway_client_https'))

if __name__=='__main__':unittest.main()
