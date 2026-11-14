#!/usr/bin/env python3
"""Q02: fail-closed planned-values policy audit; never certifies Azure resources.

Input is trusted only as Terraform `show -json` *syntax*, not as live proof. The
JSON plan is sensitive; use restricted storage and never publish it to GitHub.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

BOOL_FALSE = {
    'azurerm_storage_account': ['public_network_access_enabled', 'shared_access_key_enabled', 'allow_nested_items_to_be_public'],
    'azurerm_key_vault': ['public_network_access_enabled'],
    'azurerm_cognitive_account': ['public_network_access_enabled', 'local_auth_enabled'],
    'azurerm_search_service': ['public_network_access_enabled', 'local_authentication_enabled'],
    'azurerm_cosmosdb_account': ['public_network_access_enabled', 'local_authentication_enabled', 'network_acl_bypass_for_azure_services'],
    'azurerm_linux_web_app': ['public_network_access_enabled', 'ftp_publish_basic_authentication_enabled', 'webdeploy_publish_basic_authentication_enabled'],
    'azurerm_log_analytics_workspace': ['internet_ingestion_enabled', 'internet_query_enabled'],
}
BOOL_TRUE = {
    'azurerm_storage_account': ['https_traffic_only_enabled'],
    'azurerm_key_vault': ['rbac_authorization_enabled', 'purge_protection_enabled'],
    'azurerm_linux_web_app': ['https_only'],
}
REQUIRED_DEV_TYPES = {
    'azurerm_application_gateway',
    'azurerm_web_application_firewall_policy',
    'azurerm_linux_web_app',
    'azurerm_cognitive_account',
    'azurerm_search_service',
    'azurerm_cosmosdb_account',
    'azurerm_key_vault',
    'azurerm_private_endpoint',
}
REQUIRED_BOOTSTRAP_TYPES = {'azurerm_storage_account', 'azurerm_storage_container'}
PROTECTED_TYPES = REQUIRED_DEV_TYPES | REQUIRED_BOOTSTRAP_TYPES


def children(block):
    if not isinstance(block, dict):
        return
    for item in block.get('resources', []):
        if isinstance(item, dict):
            yield item
    for child in block.get('child_modules', []):
        yield from children(child)


def first_block(value):
    return value[0] if isinstance(value, list) and value else value if isinstance(value, dict) else {}


def has_unknown(tree, key):
    if isinstance(tree, dict):
        if tree.get(key) is True:
            return True
        return any(has_unknown(v, key) for v in tree.values())
    if isinstance(tree, list):
        return any(has_unknown(v, key) for v in tree)
    return False


def review(doc: dict, scope: str = 'dev', *, synthetic=False) -> dict:
    problems, missing, observations = [], [], []
    if not isinstance(doc, dict):
        return {'status': 'NOT_READY', 'errors': [], 'missing': ['unreadable plan object'], 'observed': 0}
    if not synthetic and doc.get('synthetic_fixture'):
        return {'status': 'NOT_READY', 'errors': [], 'missing': ['synthetic fixture cannot be reviewed as real plan'], 'observed': 0}
    root = doc.get('planned_values', {}).get('root_module') if isinstance(doc.get('planned_values'), dict) else None
    if not isinstance(root, dict):
        missing.append('planned_values.root_module absent')
        records = []
    else:
        records = list(children(root))
    types = {r.get('type') for r in records}
    expected = REQUIRED_DEV_TYPES if scope == 'dev' else REQUIRED_BOOTSTRAP_TYPES
    for t in sorted(expected - types):
        missing.append(f'expected planned resource type absent: {t}')
    unknown_by_addr = {
        r.get('address'): r.get('change', {}).get('after_unknown', {})
        for r in doc.get('resource_changes', []) if isinstance(r, dict)
    }
    for change in doc.get('resource_changes', []):
        if not isinstance(change, dict):
            continue
        ops = change.get('change', {}).get('actions', [])
        if 'delete' in ops and change.get('type') in PROTECTED_TYPES:
            problems.append(f"{change.get('type')}: destructive change blocked by Q02")
    for r in records:
        typ = r.get('type', '')
        address = r.get('address', 'unknown-address')
        val = r.get('values', {})
        if not isinstance(val, dict):
            missing.append(f'{address}: resource values missing')
            continue
        unk = unknown_by_addr.get(address, {})
        observations.append(typ)
        for field in BOOL_FALSE.get(typ, []):
            if has_unknown(unk, field) or field not in val or val[field] is None:
                missing.append(f'{typ}.{field}: unresolved')
            elif val[field] is not False:
                problems.append(f'{typ}.{field}: must be false')
        for field in BOOL_TRUE.get(typ, []):
            if has_unknown(unk, field) or field not in val or val[field] is None:
                missing.append(f'{typ}.{field}: unresolved')
            elif val[field] is not True:
                problems.append(f'{typ}.{field}: must be true')
        if typ == 'azurerm_storage_account':
            if val.get('min_tls_version') is None or has_unknown(unk, 'min_tls_version'):
                missing.append('storage TLS version unresolved')
            elif val['min_tls_version'] != 'TLS1_2':
                problems.append('storage must require TLS1_2')
        elif typ == 'azurerm_linux_web_app':
            site = first_block(val.get('site_config'))
            if not site or has_unknown(unk, 'site_config'):
                missing.append('web app site_config unresolved')
            else:
                if site.get('minimum_tls_version') not in ('1.2', '1.3'):
                    problems.append('web app site TLS below 1.2 or absent')
                if site.get('scm_minimum_tls_version') not in ('1.2', '1.3'):
                    problems.append('web app SCM TLS below 1.2 or absent')
                if site.get('ftps_state') != 'Disabled':
                    problems.append('web app FTPS must be disabled')
                if site.get('vnet_route_all_enabled') is not True:
                    problems.append('web app VNet route-all missing')
            if val.get('virtual_network_subnet_id') is None or has_unknown(unk, 'virtual_network_subnet_id'):
                missing.append('web app outbound subnet unresolved')
            identity = first_block(val.get('identity'))
            if 'UserAssigned' not in (identity.get('type') or ''):
                problems.append('web app requires user-assigned identity')
        elif typ == 'azurerm_application_gateway':
            configs = val.get('frontend_ip_configuration')
            if has_unknown(unk, 'frontend_ip_configuration') or not isinstance(configs, list) or not configs:
                missing.append('gateway frontend config unresolved')
            else:
                for fc in configs:
                    if not isinstance(fc, dict):
                        missing.append('gateway frontend config incomplete')
                        continue
                    if fc.get('public_ip_address_id'):
                        problems.append('gateway public frontend forbidden')
                    if fc.get('private_ip_address_allocation') != 'Static' or not fc.get('private_ip_address'):
                        missing.append('gateway static private IP or reservation unresolved')
            sku = first_block(val.get('sku'))
            if sku.get('name') != 'WAF_v2' or sku.get('tier') != 'WAF_v2':
                problems.append('gateway must be WAF_v2')
            cert = first_block(val.get('ssl_certificate'))
            if cert.get('data') or cert.get('password'):
                problems.append('gateway inline PFX/password forbidden')
            if not cert.get('key_vault_secret_id'):
                missing.append('gateway Key Vault TLS certificate reference unresolved')
        elif typ == 'azurerm_web_application_firewall_policy':
            settings = first_block(val.get('policy_settings'))
            mode = settings.get('mode')
            if mode not in ('Detection', 'Prevention'):
                missing.append('WAF mode unresolved')
            elif mode == 'Prevention':
                missing.append('WAF Prevention needs external signed approval')
        elif typ == 'azurerm_private_endpoint':
            groups = first_block(val.get('private_service_connection'))
            dns = first_block(val.get('private_dns_zone_group'))
            if not groups.get('subresource_names') or not groups.get('private_connection_resource_id'):
                missing.append('private endpoint group and target unresolved')
            if not dns.get('private_dns_zone_ids'):
                missing.append('private endpoint DNS zone unresolved')
            if not val.get('subnet_id') or has_unknown(unk, 'subnet_id'):
                missing.append('private endpoint subnet unresolved')
        elif typ == 'azurerm_role_assignment':
            if val.get('role_definition_name') in ('Owner', 'Contributor', 'User Access Administrator'):
                problems.append('broad management role assignment forbidden')
    if problems:
        state = 'FAIL_POLICY'
    elif missing:
        state = 'NOT_READY'
    else:
        # This is the maximum rating possible with plan JSON: it is NOT live acceptance.
        state = 'PASS_OFFLINE_POLICY_ONLY' if synthetic else 'REVIEW_REQUIRED'
    return {
        'status': state, 'scope': scope, 'resource_count': len(records),
        'resource_types': sorted(t for t in types if isinstance(t, str)),
        'error_count': len(problems), 'missing_count': len(missing),
        'errors': sorted(set(problems)), 'missing': sorted(set(missing)),
        'azure_live_passes': 0, 'release_decision': 'NO_GO',
    }


def fixture(scope='dev'):
    """Synthetic data only; never represent as an Azure observation."""
    values = [
        ('azurerm_cognitive_account', {'public_network_access_enabled': False, 'local_auth_enabled': False}),
        ('azurerm_search_service', {'public_network_access_enabled': False, 'local_authentication_enabled': False}),
        ('azurerm_cosmosdb_account', {'public_network_access_enabled': False, 'local_authentication_enabled': False, 'network_acl_bypass_for_azure_services': False}),
        ('azurerm_key_vault', {'public_network_access_enabled': False, 'rbac_authorization_enabled': True, 'purge_protection_enabled': True}),
        ('azurerm_linux_web_app', {'public_network_access_enabled': False, 'ftp_publish_basic_authentication_enabled': False, 'webdeploy_publish_basic_authentication_enabled': False, 'https_only': True, 'virtual_network_subnet_id': '/subnets/app-egress', 'identity': [{'type': 'UserAssigned'}], 'site_config': [{'minimum_tls_version':'1.2','scm_minimum_tls_version':'1.2','ftps_state':'Disabled','vnet_route_all_enabled':True}]}),
        ('azurerm_application_gateway', {'frontend_ip_configuration':[{'private_ip_address':'10.0.1.10','private_ip_address_allocation':'Static','public_ip_address_id':None}], 'sku':[{'name':'WAF_v2','tier':'WAF_v2'}], 'ssl_certificate':[{'key_vault_secret_id':'https://placeholder.invalid/secrets/cert'}]}),
        ('azurerm_web_application_firewall_policy', {'policy_settings':[{'mode':'Detection'}]}),
        ('azurerm_private_endpoint', {'subnet_id':'/subnets/pe','private_service_connection':[{'private_connection_resource_id':'/resources/safe','subresource_names':['sites']}],'private_dns_zone_group':[{'private_dns_zone_ids':['/dns/approved']}]}),
    ] if scope == 'dev' else [
        ('azurerm_storage_account', {'public_network_access_enabled':False,'shared_access_key_enabled':False,'allow_nested_items_to_be_public':False,'https_traffic_only_enabled':True,'min_tls_version':'TLS1_2'}),
        ('azurerm_storage_container', {'container_access_type':'private'}),
    ]
    return {'synthetic_fixture': True, 'planned_values': {'root_module': {'resources': [
        {'address': f'{t}.synthetic_{i}', 'type':t,'values':v} for i,(t,v) in enumerate(values)
    ]}}, 'resource_changes':[]}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan', type=Path, help='Restricted terraform show -json output (never publish)')
    p.add_argument('--scope', choices=('dev','bootstrap'), default='dev')
    p.add_argument('--selftest', action='store_true', help='Test synthetic safe and violation fixtures only')
    args = p.parse_args()
    if args.selftest and args.plan:
        p.error('--selftest and --plan are mutually exclusive')
    if args.selftest:
        good=fixture(args.scope)
        good_report=review(good,args.scope,synthetic=True)
        import copy
        bad=copy.deepcopy(good)
        target=bad['planned_values']['root_module']['resources'][0]['values']
        target['public_network_access_enabled']=True
        bad_report=review(bad,args.scope,synthetic=True)
        missing=copy.deepcopy(good)
        del missing['planned_values']['root_module']['resources'][0]['values']['public_network_access_enabled']
        missing_report=review(missing,args.scope,synthetic=True)
        ok=(good_report['status']=='PASS_OFFLINE_POLICY_ONLY' and bad_report['status']=='FAIL_POLICY' and missing_report['status']=='NOT_READY')
        result={'status':'PASS_OFFLINE_FIXTURES_ONLY' if ok else 'FAIL','good':good_report['status'],'unsafe':bad_report['status'],'missing':missing_report['status'],'azure_live_passes':0,'release_decision':'NO_GO'}
        print(json.dumps(result,indent=2));return 0 if ok else 1
    if args.plan is None:
        p.error('specify --selftest or --plan <restricted-json>')
    try:
        with args.plan.open(encoding='utf-8') as file:
            obj=json.load(file)
    except (OSError, ValueError) as exc:
        print(json.dumps({'status':'NOT_READY','reason':'plan could not be read or parsed','error_type':type(exc).__name__}));return 2
    result=review(obj,args.scope,synthetic=False)
    print(json.dumps(result,indent=2))
    return 1 if result['status']=='FAIL_POLICY' else 2 if result['status']=='NOT_READY' else 0


if __name__=='__main__':
    raise SystemExit(main())
