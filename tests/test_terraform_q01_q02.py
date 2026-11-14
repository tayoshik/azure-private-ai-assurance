"""Fail-closed, synthetic-only regression tests for Q01/Q02."""
import copy
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def get_module(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


q01 = get_module('q01', 'scripts/terraform_q01_integrated.py')
q02 = get_module('q02', 'scripts/terraform_q02_plan_guard.py')


class Q01Tests(unittest.TestCase):
    def test_existing_six_contract_checkers(self):
        report = q01.review(ROOT)
        self.assertEqual(report['status'], 'PASS_OFFLINE_CONTRACT_ONLY')
        self.assertEqual(len(report['checkers']), 6)
        self.assertGreaterEqual(report['terraform_file_count'], 61)
        self.assertEqual(report['azure_live_passes'], 0)
        self.assertEqual(report['terraform_validate'], 'NOT_EXECUTED')

    def test_no_terraform_cli_success_claim(self):
        report = q01.review(ROOT)
        self.assertEqual(report['terraform_plan'], 'NOT_EXECUTED')
        self.assertEqual(report['terraform_apply'], 'NOT_EXECUTED')
        self.assertEqual(report['release_decision'], 'NO_GO')
        self.assertEqual(report['live_acceptance_not_ready'], 1716)

    def test_reject_incomplete_empty_source_root(self):
        with tempfile.TemporaryDirectory() as folder:
            report = q01.review(Path(folder))
            self.assertEqual(report['status'], 'FAIL')
            self.assertTrue(any('source' in x for x in report['errors']))

    def test_reject_secret_pattern(self):
        with tempfile.TemporaryDirectory() as folder:
            dest=Path(folder)
            (dest/'infra').mkdir()
            # Test the pattern directly; never include valid credentials.
            self.assertIsNotNone(q01.FORBIDDEN_SECRET.search('-----BEGIN ' + 'PRIVATE KEY-----'))


class Q02Tests(unittest.TestCase):
    def setUp(self):
        self.plan = q02.fixture('dev')

    def rec(self, typ):
        return next(r for r in self.plan['planned_values']['root_module']['resources'] if r['type']==typ)

    def status(self):
        return q02.review(self.plan, 'dev', synthetic=True)['status']

    def test_approved_synthetic_only(self):
        self.assertEqual(self.status(), 'PASS_OFFLINE_POLICY_ONLY')
        self.assertEqual(q02.review(self.plan,'dev')['status'], 'NOT_READY')

    def test_reject_openai_public(self):
        self.rec('azurerm_cognitive_account')['values']['public_network_access_enabled']=True
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_reject_openai_keys(self):
        self.rec('azurerm_cognitive_account')['values']['local_auth_enabled']=True
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_reject_search_public(self):
        self.rec('azurerm_search_service')['values']['public_network_access_enabled']=True
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_reject_search_key_auth(self):
        self.rec('azurerm_search_service')['values']['local_authentication_enabled']=True
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_reject_cosmos_local_auth(self):
        self.rec('azurerm_cosmosdb_account')['values']['local_authentication_disabled']=False
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_cosmos_auth_missing_not_ready(self):
        del self.rec('azurerm_cosmosdb_account')['values']['local_authentication_disabled']
        self.assertEqual(self.status(), 'NOT_READY')

    def test_reject_vault_public(self):
        self.rec('azurerm_key_vault')['values']['public_network_access_enabled']=True
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_reject_vault_purge_disabled(self):
        self.rec('azurerm_key_vault')['values']['purge_protection_enabled']=False
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_reject_web_app_public(self):
        self.rec('azurerm_linux_web_app')['values']['public_network_access_enabled']=True
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_reject_web_app_http(self):
        self.rec('azurerm_linux_web_app')['values']['https_only']=False
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_reject_web_app_tls_1_0(self):
        self.rec('azurerm_linux_web_app')['values']['site_config'][0]['minimum_tls_version']='1.0'
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_reject_gateway_public(self):
        self.rec('azurerm_application_gateway')['values']['frontend_ip_configuration'][0]['public_ip_address_id']='/fake/publicip'
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_reject_gateway_inline_cert(self):
        self.rec('azurerm_application_gateway')['values']['ssl_certificate'][0]['password']='unsafe-fixture-placeholder'
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_waiver_not_automatic_for_waf_prevention(self):
        self.rec('azurerm_web_application_firewall_policy')['values']['policy_settings'][0]['mode']='Prevention'
        self.assertEqual(self.status(), 'NOT_READY')

    def test_missing_pe_dns_is_not_ready(self):
        del self.rec('azurerm_private_endpoint')['values']['private_dns_zone_group']
        self.assertEqual(self.status(), 'NOT_READY')

    def test_missing_critical_boolean_is_not_ready(self):
        del self.rec('azurerm_cosmosdb_account')['values']['public_network_access_enabled']
        self.assertEqual(self.status(), 'NOT_READY')

    def test_unknown_bool_is_not_ready(self):
        address = self.rec('azurerm_linux_web_app')['address']
        self.plan['resource_changes']=[{'address':address,'change':{'after_unknown':{'public_network_access_enabled': True},'actions':['create']}}]
        self.assertEqual(self.status(), 'NOT_READY')

    def test_protected_delete_is_fail(self):
        self.plan['resource_changes']=[{'type':'azurerm_cosmosdb_account','change':{'actions':['delete']}}]
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_missing_entire_resource_type_not_ready(self):
        self.plan['planned_values']['root_module']['resources']=[r for r in self.plan['planned_values']['root_module']['resources'] if r['type']!='azurerm_key_vault']
        self.assertEqual(self.status(), 'NOT_READY')

    def test_recursive_child_modules(self):
        root=self.plan['planned_values']['root_module']
        r=root.pop('resources')
        root['child_modules']=[{'address':'module.inner','resources':r}]
        self.assertEqual(self.status(), 'PASS_OFFLINE_POLICY_ONLY')

    def test_reject_broad_rbac(self):
        self.plan['planned_values']['root_module']['resources'].append({'type':'azurerm_role_assignment','address':'r.a','values':{'role_definition_name':'Owner'}})
        self.assertEqual(self.status(), 'FAIL_POLICY')

    def test_bootstrap_safe_and_unsafe(self):
        boot=q02.fixture('bootstrap')
        self.assertEqual(q02.review(boot,'bootstrap',synthetic=True)['status'], 'PASS_OFFLINE_POLICY_ONLY')
        boot['planned_values']['root_module']['resources'][0]['values']['shared_access_key_enabled']=True
        self.assertEqual(q02.review(boot,'bootstrap',synthetic=True)['status'], 'FAIL_POLICY')

    def test_bootstrap_storage_tls(self):
        boot=q02.fixture('bootstrap')
        boot['planned_values']['root_module']['resources'][0]['values']['min_tls_version']='TLS1_0'
        self.assertEqual(q02.review(boot,'bootstrap',synthetic=True)['status'], 'FAIL_POLICY')


if __name__ == '__main__':
    unittest.main()
