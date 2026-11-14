#!/usr/bin/env python3
"""Textual fail-closed Terraform A01-A06 regression, NOT a provider/schema/live validator."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_terraform_stage1 import lexical_balance
from check_terraform_n04 import find_resource

RESOURCE_GATES = [
    ('azure-openai/main.tf', 'azurerm_cognitive_account', 'openai', [
        r'kind\s*=\s*"OpenAI"', r'sku_name\s*=\s*"S0"',
        r'public_network_access_enabled\s*=\s*false', r'local_auth_enabled\s*=\s*false',
        r'custom_subdomain_name\s*=\s*var\.custom_subdomain_name',
        r'condition\s*=\s*var\.openai_account_approved\s*&&\s*var\.region_and_quota_approved']),
    ('azure-openai/main.tf', 'azurerm_cognitive_deployment', 'model', [
        r'cognitive_account_id\s*=\s*azurerm_cognitive_account\.openai\.id',
        r'version_upgrade_option\s*=\s*"NoAutoUpgrade"',
        r'format\s*=\s*"OpenAI"', r'version\s*=\s*var\.model_version',
        r'condition\s*=\s*var\.model_deployment_approved']),
    ('ai-search/main.tf', 'azurerm_search_service', 'search', [
        r'public_network_access_enabled\s*=\s*false',
        r'local_authentication_enabled\s*=\s*false',
        r'network_rule_bypass_option\s*=\s*"None"',
        r'condition\s*=\s*var\.search_approved\s*&&\s*var\.region_and_sku_approved']),
    ('cosmos-db/main.tf', 'azurerm_cosmosdb_account', 'no_sql', [
        r'kind\s*=\s*"GlobalDocumentDB"',
        r'public_network_access_enabled\s*=\s*false',
        r'local_authentication_enabled\s*=\s*false',
        r'network_acl_bypass_for_azure_services\s*=\s*false',
        r'type\s*=\s*"Continuous"',
        r'condition\s*=\s*var\.cosmos_account_approved\s*&&\s*var\.backup_and_budget_approved']),
    ('cosmos-db/main.tf','azurerm_cosmosdb_sql_database','app', [
        r'account_name\s*=\s*azurerm_cosmosdb_account\.no_sql\.name']),
    ('cosmos-db/main.tf','azurerm_cosmosdb_sql_container','app', [
        r'database_name\s*=\s*azurerm_cosmosdb_sql_database\.app\.name',
        r'partition_key_paths\s*=\s*var\.partition_key_paths']),
    ('ai-private-endpoints/main.tf','azurerm_private_endpoint','openai', [
        r'subnet_id\s*=\s*var\.subnet_id',r'subresource_names\s*=\s*\["account"\]',
        r'private_dns_zone_ids\s*=\s*\[var\.openai_zone_id\]',
        r'var\.private_endpoints_approved',r'/privatelink\.openai\.azure\.com']),
    ('ai-private-endpoints/main.tf','azurerm_private_endpoint','search', [
        r'subresource_names\s*=\s*\["searchService"\]',
        r'private_dns_zone_ids\s*=\s*\[var\.search_zone_id\]',
        r'var\.private_endpoints_approved',r'/privatelink\.search\.windows\.net']),
    ('ai-private-endpoints/main.tf','azurerm_private_endpoint','cosmos', [
        r'subresource_names\s*=\s*\["Sql"\]',
        r'private_dns_zone_ids\s*=\s*\[var\.cosmos_zone_id\]',
        r'var\.private_endpoints_approved',r'/privatelink\.documents\.azure\.com']),
    ('ai-data-rbac/main.tf','azurerm_role_assignment','openai_user', [
        r'role_definition_name\s*=\s*"Cognitive Services OpenAI User"',
        r'principal_id\s*=\s*var\.app_principal_id', r'condition\s*=\s*var\.rbac_approved']),
    ('ai-data-rbac/main.tf','azurerm_role_assignment','search_reader', [
        r'role_definition_name\s*=\s*"Search Index Data Reader"',
        r'principal_id\s*=\s*var\.app_principal_id',r'condition\s*=\s*var\.rbac_approved']),
    ('ai-data-rbac/main.tf','azurerm_cosmosdb_sql_role_assignment','app', [
        r'principal_id\s*=\s*var\.app_principal_id',
        r'role_definition_id\s*=\s*"\$\{var\.cosmos_account_id\}/sqlRoleDefinitions/',
        r'/dbs/\$\{var\.cosmos_database_name\}/colls/\$\{var\.cosmos_container_name\}',
        r'condition\s*=\s*var\.rbac_approved',r'var\.cosmos_write_justification_approved']),
]
ROOT_MODULES = ('azure_openai','ai_search','cosmos_db','ai_data_private_endpoints','ai_data_rbac')
APPROVALS = (
    'openai_account_approved','openai_region_quota_approved',
    'openai_model_deployment_approved','search_service_approved',
    'search_region_sku_approved','cosmos_account_approved',
    'cosmos_backup_budget_approved','ai_private_endpoints_approved',
    'ai_data_rbac_approved','cosmos_data_write_approved',
    'cosmos_write_justification_approved',
)

def check(root=ROOT):
    root=Path(root)
    errors=[]
    modules=root/'infra/modules'
    for module in ['azure-openai','ai-search','cosmos-db','ai-private-endpoints','ai-data-rbac']:
        for file in ('main.tf','variables.tf','outputs.tf'):
            if not(modules/module/file).is_file(): errors.append('missing '+module+'/'+file)
    if errors: return {'state':'FAIL','errors':errors,'azure_live_passes':0}
    files=list((root/'infra').rglob('*.tf'))
    for p in files:
        if not lexical_balance(p.read_text(encoding='utf8')):
            errors.append('unbalanced HCL '+str(p.relative_to(root)))
    for filename,rtype,name,patterns in RESOURCE_GATES:
        text=(modules/filename).read_text(encoding='utf8')
        block=find_resource(text,rtype,name)
        if block is None:
            errors.append('missing '+rtype+'.'+name)
            continue
        for pattern in patterns:
            if not re.search(pattern,block,re.S):errors.append(rtype+'.'+name+' lacks '+pattern)
    main=(root/'infra/environments/dev/main.tf').read_text(encoding='utf8')
    vars_=(root/'infra/environments/dev/variables.tf').read_text(encoding='utf8')
    ex=(root/'infra/environments/dev/terraform.tfvars.example').read_text(encoding='utf8')
    output=(root/'infra/environments/dev/outputs.tf').read_text(encoding='utf8')
    for module in ROOT_MODULES:
        if not re.search(r'module\s+"'+module+r'"\s*\{',main):
            errors.append('missing root module '+module)
    for reference in [
        'module.identity.app_principal_id',
        'module.network.data_private_endpoint_subnet_id',
        'module.private_dns.zone_ids["privatelink.openai.azure.com"]',
        'module.private_dns.zone_ids["privatelink.search.windows.net"]',
        'module.private_dns.zone_ids["privatelink.documents.azure.com"]',
        'module.azure_openai.account_id','module.ai_search.id',
        'module.cosmos_db.account_id','depends_on                 = [module.network]']:
        if reference not in main:errors.append('root reference missing '+reference)
    approval_forward = {
       'openai_region_quota_approved':'region_and_quota_approved',
       'openai_model_deployment_approved':'model_deployment_approved',
       'search_service_approved':'search_approved',
       'search_region_sku_approved':'region_and_sku_approved',
       'cosmos_backup_budget_approved':'backup_and_budget_approved',
       'ai_private_endpoints_approved':'private_endpoints_approved',
       'ai_data_rbac_approved':'rbac_approved',
       'cosmos_data_write_approved':'cosmos_write_approved',
    }
    for key in APPROVALS:
        if not re.search(r'variable\s+"'+key+r'"\s*\{[\s\S]*?default\s*=\s*false',vars_):
            errors.append('root approval has no false default '+key)
        if not re.search(r'(?m)^'+key+r'\s*=\s*false\s*$',ex):
            errors.append('example approval not false '+key)
        if not re.search(r'\b'+approval_forward.get(key,key)+r'\s*=\s*var\.'+key+r'\b',main):
            errors.append('approval not forwarded '+key)
    # Read-only Cosmos by default; written data needs explicit second signoff.
    roles=(modules/'ai-data-rbac/main.tf').read_text()
    if '00000000-0000-0000-0000-000000000001' not in roles or '00000000-0000-0000-0000-000000000002' not in roles:
        errors.append('Cosmos SQL built-in data role mapping missing')
    if not re.search(r'cosmos_role_guid\s*=\s*var\.cosmos_write_approved\s*\?',roles):
        errors.append('Cosmos writer defaults incorrectly')
    for p in files:
        s=p.read_text(encoding='utf8')
        if re.search(r'(?m)^\s*(?:local_auth_enabled|local_authentication_enabled|public_network_access_enabled)\s*=\s*true\b',s):
            errors.append('unsafe public/key auth in '+str(p))
        if re.search(r'-----BEGIN [A-Z ]+PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{25,}',s):
            errors.append('credential disclosure in '+str(p))
    return {'state':'PASS_OFFLINE_A01_A06_TEXT_ONLY' if not errors else 'FAIL',
            'terraform_file_count':len(files),
            'covered_nodes':['A01','A02','A03','A04','A05','A06'],
            'resources_checked':len(RESOURCE_GATES),
            'azure_live_passes':0,'azure_live_acceptance':'NOT_READY',
            'terraform_fmt':'NOT_EXECUTED','terraform_validate':'NOT_EXECUTED',
            'terraform_plan':'NOT_EXECUTED','terraform_apply':'NOT_EXECUTED',
            'release_decision':'NO_GO','errors':errors}

if __name__=='__main__':
    report=check()
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(bool(report['errors']))
