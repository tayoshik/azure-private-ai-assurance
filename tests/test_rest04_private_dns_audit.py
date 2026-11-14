"""REST04 negative/positive fixtures, no Azure calls or credentials."""
import copy
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('rest04_private_dns_audit', ROOT/'scripts/rest04_private_dns_audit.py')
a=importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def fixture():
    t,o=a.synthetic_inputs()
    return copy.deepcopy(t),copy.deepcopy(o)


def refresh(o,role):
    o[role]['evidence_sha256']=a.digest(o[role]['observation'])


class REST04Tests(unittest.TestCase):
    def assess(self, edit=None, expected='FAIL_OFFLINE_POLICY_FIXTURE'):
        t,o=fixture()
        if edit is not None:
            role, fn=edit
            fn(o[role]['observation'])
            refresh(o,role)
        r=a.assess_target(t,o,synthetic=True)
        self.assertEqual(r['status'],expected)
        self.assertEqual(r['azure_live_acceptance'],'NOT_READY')
        self.assertEqual(r['azure_live_passes'],0)
        self.assertFalse(r['private_dns_runtime_proven'])
        self.assertNotIn('10.32.5.9',str(r))
        self.assertNotIn(t['private_endpoint_id'],str(r))
        return r

    def test_selftest(self):
        self.assertEqual(a.selftest()['status'],'PASS_OFFLINE_FIXTURES_ONLY')
    def test_baseline_valid(self):
        self.assess(expected='PASS_OFFLINE_FIXTURE_ONLY')
    def test_healthy_live_observation_is_not_acceptance(self):
        t,o=fixture()
        r=a.assess_target(t,o)
        self.assertEqual(r['status'],'OBSERVED_PENDING_PRIVATE_DNS_PROBE')
        self.assertEqual(r['azure_live_acceptance'],'NOT_READY')
    def test_pe_pending(self):
        self.assess(('pe',lambda d:d['properties']['privateLinkServiceConnections'][0]['properties']['privateLinkServiceConnectionState'].update(status='Pending')))
    def test_service_id_tamper(self):
        self.assess(('pe',lambda d:d['properties']['privateLinkServiceConnections'][0]['properties'].update(privateLinkServiceId=d['id'])))
    def test_wrong_group(self):
        self.assess(('pe',lambda d:d['properties']['privateLinkServiceConnections'][0]['properties'].update(groupIds=['vault'])))
    def test_wrong_subnet(self):
        self.assess(('pe',lambda d:d['properties'].update(subnet={'id':d['id']})))
    def test_mismatched_nic_id(self):
        self.assess(('pe',lambda d:d['properties'].update(networkInterfaces=[{'id':d['id']}])))
    def test_extra_unreviewed_nic_not_ready(self):
        self.assess(('pe',lambda d:d['properties']['networkInterfaces'].append({'id':d['id']})), 'NOT_READY')
    def test_no_connection_not_ready(self):
        self.assess(('pe',lambda d:d['properties'].update(privateLinkServiceConnections=[])), 'NOT_READY')
    def test_nic_belongs_to_other_pe(self):
        self.assess(('nic',lambda d:d['properties'].update(privateEndpoint={'id':d['id']})))
    def test_nic_wrong_ip(self):
        self.assess(('nic',lambda d:d['properties']['ipConfigurations'][0]['properties'].update(privateIPAddress='10.32.5.10')))
    def test_nic_public_ip(self):
        self.assess(('nic',lambda d:d['properties']['ipConfigurations'][0]['properties'].update(publicIPAddress={'id':'some-public-ip'})))
    def test_nic_wrong_subnet(self):
        self.assess(('nic',lambda d:d['properties']['ipConfigurations'][0]['properties'].update(subnet={'id':d['id']})))
    def test_nic_missing_ip_not_ready(self):
        self.assess(('nic',lambda d:d['properties']['ipConfigurations'][0]['properties'].pop('privateIPAddress')), 'NOT_READY')
    def test_nic_nonprivate_address(self):
        self.assess(('nic',lambda d:d['properties']['ipConfigurations'][0]['properties'].update(privateIPAddress='8.8.8.8')))
    def test_pe_provisioning_failed(self):
        self.assess(('pe',lambda d:d['properties'].update(provisioningState='Failed')))
    def test_zone_group_wrong_zone(self):
        self.assess(('zone_group',lambda d:d['properties']['privateDnsZoneConfigs'][0]['properties'].update(privateDnsZoneId=d['id'])))
    def test_zone_group_not_succeeded(self):
        self.assess(('zone_group',lambda d:d['properties'].update(provisioningState='Failed')))
    def test_zone_group_missing_config_not_ready(self):
        self.assess(('zone_group',lambda d:d['properties'].update(privateDnsZoneConfigs=[])), 'NOT_READY')
    def test_zone_group_records_mismatch(self):
        t,o=fixture();o['zone_group']['observation']['properties']['privateDnsZoneConfigs'][0]['properties']['recordSets']=[{'fqdn':t['expected_record_fqdn'],'ipAddresses':['10.32.5.10']}]
        refresh(o,'zone_group')
        self.assertEqual(a.assess_target(t,o,synthetic=True)['status'],'FAIL_OFFLINE_POLICY_FIXTURE')
    def test_dns_a_record_wrong_ip(self):
        self.assess(('a_record',lambda d:d['properties']['aRecords'][0].update(ipv4Address='10.32.5.10')))
    def test_dns_a_record_extra_public(self):
        self.assess(('a_record',lambda d:d['properties']['aRecords'].append({'ipv4Address':'8.8.8.8'})))
    def test_dns_missing_a_records_not_ready(self):
        self.assess(('a_record',lambda d:d['properties'].pop('aRecords')), 'NOT_READY')
    def test_dns_vnet_link_wrong_network(self):
        self.assess(('vnet_link',lambda d:d['properties'].update(virtualNetwork={'id':d['id']})))
    def test_dns_vnet_link_registration(self):
        self.assess(('vnet_link',lambda d:d['properties'].update(registrationEnabled=True)))
    def test_dns_vnet_link_failed(self):
        self.assess(('vnet_link',lambda d:d['properties'].update(provisioningState='Failed')))
    def test_dns_vnet_link_missing_net_not_ready(self):
        self.assess(('vnet_link',lambda d:d['properties'].pop('virtualNetwork')), 'NOT_READY')
    def test_dns_vnet_link_not_complete(self):
        self.assess(('vnet_link',lambda d:d['properties'].update(virtualNetworkLinkState='Failed')))
    def test_missing_one_observation_not_ready(self):
        t,o=fixture();o.pop('nic')
        self.assertEqual(a.assess_target(t,o,synthetic=True)['status'],'NOT_READY')
    def test_missing_evidence_sha_not_ready(self):
        t,o=fixture();o['pe']['evidence_sha256']='a'*64
        self.assertEqual(a.assess_target(t,o,synthetic=True)['status'],'NOT_READY')
    def test_wrong_observed_id_not_ready(self):
        t,o=fixture();o['nic']['observation']['id']+='-other';refresh(o,'nic')
        self.assertEqual(a.assess_target(t,o,synthetic=True)['status'],'NOT_READY')
    def test_wrong_observed_type_not_ready(self):
        t,o=fixture();o['nic']['observation']['type']='Microsoft.Web/sites';refresh(o,'nic')
        self.assertEqual(a.assess_target(t,o,synthetic=True)['status'],'NOT_READY')
    def test_wrong_connection_type_not_ready(self):
        t,o=fixture();o['nic']['state']='PASS'
        self.assertEqual(a.assess_target(t,o,synthetic=True)['status'],'NOT_READY')
    def test_cross_subscription_manifest_rejected(self):
        t,_=fixture();t['nic_id']=t['nic_id'].replace('01234567','11111111')
        with self.assertRaises(ValueError):a.validate_target(t)
    def test_wrong_zone_manifest_rejected(self):
        t,_=fixture();t['dns_zone_id']=t['dns_zone_id'].replace('privatelink.azurewebsites.net','privatelink.vaultcore.azure.net')
        with self.assertRaises(ValueError):a.validate_target(t)
    def test_wrong_group_manifest_rejected(self):
        t,_=fixture();t['group_id']='vault'
        with self.assertRaises(ValueError):a.validate_target(t)
    def test_bad_fqdn_manifest_rejected(self):
        t,_=fixture();t['expected_record_fqdn']='foo.privatelink.azurewebsites.net'
        with self.assertRaises(ValueError):a.validate_target(t)
    def test_nonprivate_approved_ip_rejected(self):
        t,_=fixture();t['expected_private_ips']=['8.8.8.8']
        with self.assertRaises(ValueError):a.validate_target(t)
    def test_duplicate_targets_rejected(self):
        t,_=fixture();m={'schema':'azure-private-ai-assurance/rest04-manifest/v1','targets':[t,t]}
        with self.assertRaises(ValueError):a.validate_manifest(m)
    def test_no_targets_rejected(self):
        with self.assertRaises(ValueError):a.validate_manifest({'schema':'azure-private-ai-assurance/rest04-manifest/v1','targets':[]})
    def test_synthetic_integration_assessor_only_get(self):
        t,o=fixture()
        class FakeClient:
            def __init__(self):self.calls=[]
            def get_resource(self,rid,api):
                self.calls.append((rid,api))
                return next(x for x in o.values() if x['resource_id']==rid)
        fake=FakeClient()
        r=a.audit_client(fake,{'schema':'azure-private-ai-assurance/rest04-manifest/v1','targets':[t]})
        self.assertEqual(r['status'],'OBSERVED_PENDING_PRIVATE_DNS_PROBE')
        self.assertEqual(len(fake.calls),6)
        self.assertEqual(r['azure_live_passes'],0)
        self.assertEqual({api for rid,api in fake.calls},{'2025-05-01','2018-09-01'})
    def test_403_from_client_not_ready(self):
        t,_=fixture()
        class Deny:
            def get_resource(self,*args):raise a.NotReadyError('not authorized')
        r=a.audit_client(Deny(),{'schema':'azure-private-ai-assurance/rest04-manifest/v1','targets':[t]})
        self.assertEqual(r['status'],'NOT_READY')
        self.assertNotIn('not authorized',str(r))
    def test_cli_selftest_offline(self):
        import subprocess
        p=subprocess.run([sys.executable,str(ROOT/'scripts/rest04_private_dns_audit.py'),'--selftest'],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn('PASS_OFFLINE_FIXTURES_ONLY',p.stdout)
    def test_missing_or_fake_live_switch(self):
        import subprocess
        p=subprocess.run([sys.executable,str(ROOT/'scripts/rest04_private_dns_audit.py'),'--live'],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)

if __name__=='__main__':unittest.main()
