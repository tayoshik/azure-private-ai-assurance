#!/usr/bin/env python3
"""I01-I03 source checks. Textual fail-closed regression, NOT terraform validate."""
from pathlib import Path
import json
import re
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_terraform_stage1 import lexical_balance
from check_terraform_n04 import find_resource

REQUIRED=[
'identity/main.tf','identity/variables.tf','identity/outputs.tf',
'key-vault/main.tf','key-vault/variables.tf','key-vault/outputs.tf',
'private-endpoints/key-vault.tf','private-endpoints/variables.tf','private-endpoints/outputs.tf',
]

def check(root=ROOT):
    root=Path(root)
    errors=[]
    modules=root/'infra/modules'
    missing=[str(p) for p in REQUIRED if not (modules/p).is_file()]
    if missing:
        return {'state':'FAIL','errors':['missing: '+p for p in missing], 'azure_live_passes':0, 'terraform_cli_validation':'NOT_EXECUTED','release_decision':'NO_GO'}
    files=list((root/'infra').rglob('*.tf'))
    for p in files:
        if not lexical_balance(p.read_text(encoding='utf8')):
            errors.append('unbalanced HCL: '+str(p.relative_to(root)))
    idtext=(modules/'identity/main.tf').read_text()
    kvtext=(modules/'key-vault/main.tf').read_text()
    petext=(modules/'private-endpoints/key-vault.tf').read_text()
    def has(rtype,name,text,required_tokens):
        block=find_resource(text,rtype,name)
        if block is None:
            errors.append('missing resource '+rtype+'.'+name);return
        for token in required_tokens:
            if not re.search(token,block,re.S):
                errors.append(rtype+'.'+name+': absent '+token)
    has('azurerm_user_assigned_identity','app',idtext,[r'resource_group_name\s*=\s*var\.resource_group_name',r'location\s*=\s*var\.location'])
    has('azurerm_user_assigned_identity','gateway',idtext,[r'resource_group_name\s*=\s*var\.resource_group_name'])
    has('azurerm_key_vault','workload',kvtext,[
        r'rbac_authorization_enabled\s*=\s*true',r'public_network_access_enabled\s*=\s*false',
        r'purge_protection_enabled\s*=\s*true',r'soft_delete_retention_days\s*=\s*90',
        r'default_action\s*=\s*"Deny"',r'bypass\s*=\s*"None"',
        r'prevent_destroy\s*=\s*true',r'condition\s*=\s*var\.key_vault_configuration_approved'])
    for name,role,principal,gate in [
        ('app_secrets_reader','Key Vault Secrets User','app_principal_id','app_secrets_reader_approved'),
        ('gateway_certificate_reader','Key Vault Secrets User','gateway_principal_id','gateway_certificate_reader_approved')]:
        has('azurerm_role_assignment',name,kvtext,[
            r'role_definition_name\s*=\s*"'+re.escape(role)+'"',
            r'principal_id\s*=\s*var\.'+principal,
            r'scope\s*=\s*azurerm_key_vault\.workload\.id',
            r'count\s*=\s*var\.'+gate,
            r'condition\s*=\s*var\.role_assignment_approval_confirmed'])
    has('azurerm_private_endpoint','key_vault',petext,[
        r'subnet_id\s*=\s*var\.subnet_id',
        r'private_connection_resource_id\s*=\s*var\.key_vault_id',
        r'subresource_names\s*=\s*\["vault"\]',
        r'private_dns_zone_ids\s*=\s*\[var\.key_vault_dns_zone_id\]',
        r'condition\s*=\s*var\.key_vault_private_endpoint_approved',
        r'privatelink\.vaultcore\.azure\.net'])
    rootmain=(root/'infra/environments/dev/main.tf').read_text()
    for name in ('identity','key_vault','key_vault_private_endpoint'):
        if not re.search(rf'module\s+"{name}"\s*\{{',rootmain):errors.append('root unwired: '+name)
    for token in ('module.network.data_private_endpoint_subnet_id',
                  'module.private_dns.zone_ids["privatelink.vaultcore.azure.net"]',
                  'module.identity.app_principal_id','module.identity.gateway_principal_id',
                  'module.key_vault.id'):
        if token not in rootmain:errors.append('missing root reference: '+token)
    rootvars=(root/'infra/environments/dev/variables.tf').read_text()
    modulevars=(modules/'key-vault/variables.tf').read_text()
    example=(root/'infra/environments/dev/terraform.tfvars.example').read_text()
    for var in ('key_vault_configuration_approved','key_vault_private_endpoint_approved',
                'app_secrets_reader_approved','gateway_certificate_reader_approved',
                'role_assignment_approval_confirmed'):
        for path,s in [('root',rootvars),('example',example),('module',modulevars if var!='key_vault_private_endpoint_approved' else (modules/'private-endpoints/variables.tf').read_text())]:
            if path=='example':
                if not re.search(rf'(?m)^\s*{var}\s*=\s*false\s*$',s):errors.append(var+': not FALSE in example')
            else:
                m=re.search(rf'variable\s+"{var}"\s*\{{[^}}]*\}}',s,re.S)
                if not m or not re.search(r'default\s*=\s*false',m.group()):errors.append(var+': not FALSE by default in '+path)
        if not re.search(rf'(?m)^\s*{var}\s*=\s*var\.{var}\s*$',rootmain):errors.append(var+': root forwarding missing')
    for s in (idtext,kvtext,petext):
        if re.search(r'(?m)^\s*(?:password|client_secret|value|certificate_contents)\s*=\s*".+"',s):errors.append('hard-coded secret or credential value')
        if re.search(r'(?m)^\s*public_network_access_enabled\s*=\s*true\b',s):errors.append('public access enabled')
    if re.search(r'resource\s+"azurerm_key_vault_(?:secret|certificate|key)"',kvtext):errors.append('secret/certificate/key material must be provisioned separately')
    for checktext in ((modules/'identity/outputs.tf').read_text(),(modules/'key-vault/outputs.tf').read_text(),
                      (modules/'private-endpoints/outputs.tf').read_text()):
        if not checktext.strip():errors.append('missing module outputs')
    return {'state':'PASS_OFFLINE_I01_I03_TEXT_ONLY' if not errors else 'FAIL',
            'terraform_file_count':len(files), 'identity_count':2,'key_vault_count':1,'key_vault_private_endpoint_count':1,
            'azure_live_passes':0,'live_acceptance_not_ready':1716,'terraform_cli_validation':'NOT_EXECUTED',
            'terraform_plan':'NOT_EXECUTED','terraform_apply':'NOT_EXECUTED','release_decision':'NO_GO','errors':errors}

if __name__=='__main__':
    report=check();print(json.dumps(report,indent=2));sys.exit(bool(report['errors']))
