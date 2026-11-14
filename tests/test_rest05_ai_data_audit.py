"""REST05: pure synthetic/negative checks. No Azure credentials or network calls."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import rest05_ai_data_audit as m


class REST05Tests(unittest.TestCase):
    def setUp(self):
        self.manifest,self.evidence=m.synthetic_inputs()

    def result(self, profile, role, edit, expected="FAIL_OFFLINE_POLICY_FIXTURE"):
        ev=copy.deepcopy(self.evidence)
        o=ev[profile][role]
        edit(o['observation'])
        o['evidence_sha256']=m.digest(o['observation'])
        result=m.assess_manifest(self.manifest,ev,synthetic=True)
        self.assertEqual(result['status'], expected)
        self.assertEqual(result['release_decision'],'NO_GO')
        self.assertFalse(result['private_data_plane_proven'])
        self.assertEqual(result['azure_live_passes'],0)
        self.assertNotIn('/subscriptions/',json.dumps(result))
        return result

    def test_01_selftest(self):
        self.assertEqual(m.selftest()['status'],'PASS_OFFLINE_FIXTURES_ONLY')
    def test_02_synthetic_baseline(self):
        self.assertEqual(m.assess_manifest(self.manifest,self.evidence,synthetic=True)['status'],'PASS_OFFLINE_FIXTURES_ONLY')
    def test_03_live_observation_never_acceptance(self):
        result=m.assess_manifest(self.manifest,self.evidence)
        self.assertEqual(result['status'],'OBSERVED_PENDING_PRIVATE_DATA_PLANE_AND_REVIEW')
        self.assertTrue(all(x['azure_live_acceptance']=='NOT_READY' for x in result['profiles']))
    def test_04_three_profiles(self):
        self.assertEqual(set(m.ROLES),{'azure_openai','ai_search','cosmos_nosql'})
    def test_05_wrong_manifest_schema(self):
        self.manifest['schema']='somethingelse'
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_06_unapproved_api_version(self):
        self.manifest['targets'][0]['api_version']='latest'
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_07_malicious_profile(self):
        self.manifest['targets'][0]['profile']='storage'
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_08_unknown_manifest_fields(self):
        self.manifest['targets'][0]['tenant_secret']='invalid'
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_09_wrong_id_type(self):
        self.manifest['targets'][0]['resource_id']=self.manifest['targets'][2]['resource_id']
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_10_dup_service(self):
        self.manifest['targets'][1]=copy.deepcopy(self.manifest['targets'][0])
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_11_invalid_region(self):
        self.manifest['targets'][0]['expected']['location']='https://wrong'
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_12_missing_model_version(self):
        self.manifest['targets'][0]['expected'].pop('model_version')
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_13_zero_model_capacity(self):
        self.manifest['targets'][0]['expected']['sku_capacity']=0
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_14_boolean_model_capacity(self):
        self.manifest['targets'][0]['expected']['sku_capacity']=True
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_15_free_search_rejected(self):
        self.manifest['targets'][1]['expected']['sku_name']='free'
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_16_zero_search_replica(self):
        self.manifest['targets'][1]['expected']['replica_count']=0
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_17_cosmos_periodic_backup_baseline_rejected(self):
        self.manifest['targets'][2]['expected']['backup_type']='Periodic'
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_18_cosmos_invalid_partition_path(self):
        self.manifest['targets'][2]['expected']['partition_key_paths']=['/nested/field']
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_19_missing_evidence_role(self):
        self.evidence['azure_openai'].pop('deployment')
        self.assertEqual(m.assess_manifest(self.manifest,self.evidence,synthetic=True)['status'],'NOT_READY')
    def test_20_missing_entire_service(self):
        self.evidence.pop('ai_search')
        self.assertEqual(m.assess_manifest(self.manifest,self.evidence,synthetic=True)['status'],'NOT_READY')
    def test_21_forged_evidence_digest(self):
        self.evidence['cosmos_nosql']['account']['evidence_sha256']='f'*64
        self.assertEqual(m.assess_manifest(self.manifest,self.evidence,synthetic=True)['status'],'NOT_READY')
    def test_22_wrong_observed_resource_id(self):
        obs=self.evidence['ai_search']['service']
        obs['resource_id']=obs['resource_id']+'-fake'
        self.assertEqual(m.assess_manifest(self.manifest,self.evidence,synthetic=True)['status'],'NOT_READY')
    def test_23_observation_wrong_state(self):
        self.evidence['azure_openai']['account']['state']='PASS'
        self.assertEqual(m.assess_manifest(self.manifest,self.evidence,synthetic=True)['status'],'NOT_READY')
    def test_24_openai_public(self):
        self.result('azure_openai','account',lambda d:d['properties'].update(publicNetworkAccess='Enabled'))
    def test_25_openai_auth(self):
        self.result('azure_openai','account',lambda d:d['properties'].update(disableLocalAuth=False))
    def test_26_openai_kind(self):
        self.result('azure_openai','account',lambda d:d.update(kind='TextAnalytics'))
    def test_27_openai_custom_subdomain(self):
        self.result('azure_openai','account',lambda d:d['properties'].update(customSubDomainName='wrong'))
    def test_28_openai_model_name(self):
        self.result('azure_openai','deployment',lambda d:d['properties']['model'].update(name='unapproved-model'))
    def test_29_openai_model_version(self):
        self.result('azure_openai','deployment',lambda d:d['properties']['model'].update(version='latest'))
    def test_30_openai_auto_upgrade(self):
        self.result('azure_openai','deployment',lambda d:d['properties'].update(versionUpgradeOption='OnceNewDefaultVersionAvailable'))
    def test_31_openai_deployment_capacity(self):
        self.result('azure_openai','deployment',lambda d:d['sku'].update(capacity=999))
    def test_32_openai_missing_model_version(self):
        self.result('azure_openai','deployment',lambda d:d['properties']['model'].pop('version'), 'NOT_READY')
    def test_33_openai_wrong_deployment_type(self):
        self.result('azure_openai','deployment',lambda d:d.update(type='Microsoft.Web/sites'))
    def test_34_search_public(self):
        self.result('ai_search','service',lambda d:d['properties'].update(publicNetworkAccess='Enabled'))
    def test_35_search_key_auth(self):
        self.result('ai_search','service',lambda d:d['properties'].update(disableLocalAuth=False))
    def test_36_search_network_bypass(self):
        self.result('ai_search','service',lambda d:d['properties']['networkRuleSet'].update(bypass='AzureServices'))
    def test_37_search_free_sku_observed(self):
        self.result('ai_search','service',lambda d:d['sku'].update(name='free'))
    def test_38_search_insufficient_replicas(self):
        self.result('ai_search','service',lambda d:d['properties'].update(replicaCount=0))
    def test_39_search_bool_replica_rejected(self):
        self.result('ai_search','service',lambda d:d['properties'].update(replicaCount=True))
    def test_40_search_missing_partition(self):
        self.result('ai_search','service',lambda d:d['properties'].pop('partitionCount'), 'NOT_READY')
    def test_41_cosmos_public(self):
        self.result('cosmos_nosql','account',lambda d:d['properties'].update(publicNetworkAccess='Enabled'))
    def test_42_cosmos_keys(self):
        self.result('cosmos_nosql','account',lambda d:d['properties'].update(disableLocalAuth=False))
    def test_43_cosmos_azure_services_bypass(self):
        self.result('cosmos_nosql','account',lambda d:d['properties'].update(networkAclBypass='AzureServices'))
    def test_44_cosmos_periodic_backup_observed(self):
        self.result('cosmos_nosql','account',lambda d:d['properties']['backupPolicy'].update(type='Periodic'))
    def test_45_cosmos_consistency_drift(self):
        self.result('cosmos_nosql','account',lambda d:d['properties']['consistencyPolicy'].update(defaultConsistencyLevel='Strong'))
    def test_46_cosmos_wrong_database(self):
        self.result('cosmos_nosql','database',lambda d:d['properties']['resource'].update(id='other-db'))
    def test_47_cosmos_wrong_container(self):
        self.result('cosmos_nosql','container',lambda d:d['properties']['resource'].update(id='other-container'))
    def test_48_cosmos_wrong_partition_path(self):
        self.result('cosmos_nosql','container',lambda d:d['properties']['resource']['partitionKey'].update(paths=['/other']))
    def test_49_cosmos_missing_backup_policy(self):
        self.result('cosmos_nosql','account',lambda d:d['properties'].pop('backupPolicy'), 'NOT_READY')
    def test_50_cosmos_missing_partition_paths(self):
        self.result('cosmos_nosql','container',lambda d:d['properties']['resource']['partitionKey'].pop('paths'), 'NOT_READY')
    def test_51_fake_client_does_not_reach_azure(self):
        class Fake:
            read_enabled=True
            subscriptions=['01234567-89ab-4def-8123-0123456789ab']
            def get_resource(self,rid,version):
                for t in self_manifest['targets']:
                    for role in m.ROLES[t['profile']]:
                        if m.child_resource_id(t,role)==rid:
                            return self_evidence[t['profile']][role]
                raise AssertionError('unapproved ID')
        self_manifest,self_evidence=self.manifest,self.evidence
        result=m.audit_client(Fake(),self.manifest)
        self.assertEqual(result['status'],'OBSERVED_PENDING_PRIVATE_DATA_PLANE_AND_REVIEW')
    def test_52_unapproved_client_cannot_read(self):
        class Fake:
            read_enabled=False
            subscriptions=['01234567-89ab-4def-8123-0123456789ab']
        with self.assertRaises(m.NotReadyError):m.audit_client(Fake(),self.manifest)
    def test_53_client_scope_mismatch(self):
        class Fake:
            read_enabled=True
            subscriptions=['11111111-1111-4111-8111-111111111111']
        with self.assertRaises(m.NotReadyError):m.audit_client(Fake(),self.manifest)
    def test_54_partial_client_failure(self):
        class Fake:
            read_enabled=True
            subscriptions=['01234567-89ab-4def-8123-0123456789ab']
            def get_resource(self,rid,version):raise m.NotReadyError('unavailable')
        result=m.audit_client(Fake(),self.manifest)
        self.assertEqual(result['status'],'NOT_READY')
    def test_55_unknown_extra_profile_evidence(self):
        self.evidence['other']={}
        self.assertEqual(m.assess_manifest(self.manifest,self.evidence,synthetic=True)['status'],'NOT_READY')
    def test_57_wrong_cosmos_backup_tier(self):
        self.result('cosmos_nosql','account',lambda d:d['properties']['backupPolicy']['continuousModeProperties'].update(tier='Continuous30Days'))
    def test_58_missing_cosmos_backup_tier_not_ready(self):
        self.result('cosmos_nosql','account',lambda d:d['properties']['backupPolicy'].pop('continuousModeProperties'), 'NOT_READY')
    def test_59_wrong_cosmos_kind(self):
        self.result('cosmos_nosql','account',lambda d:d.update(kind='MongoDB'))
    def test_60_invalid_baseline_cosmos_tier(self):
        self.manifest['targets'][2]['expected']['backup_tier']='Periodic'
        with self.assertRaises(ValueError):m.validate_manifest(self.manifest)
    def test_56_no_secrets_in_output(self):
        out=m.assess_manifest(self.manifest,self.evidence,synthetic=True)
        dumped=json.dumps(out)
        self.assertNotIn('synthetic-records',dumped)
        self.assertNotIn('openai-synthetic',dumped)
        self.assertNotIn('test-deploy',dumped)


if __name__=='__main__':unittest.main()
