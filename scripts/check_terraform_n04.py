#!/usr/bin/env python3
"""N04 structural/fail-closed controls (text-only; NOT terraform validate)."""
from pathlib import Path
import json
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_terraform_stage1 import lexical_balance

RESOURCES = {
  'azurerm_network_security_group': ['app_gateway','app_outbound','web_pe','data_pe'],
  'azurerm_subnet_network_security_group_association': ['app_gateway','app_outbound','web_pe','data_pe'],
  'azurerm_network_security_rule': [
    'gateway_client_https','gateway_platform_probe','gateway_deny_other_inbound',
    'gateway_to_web_pe','gateway_to_data_pe','gateway_dns_udp','gateway_dns_tcp',
    'gateway_approved_egress','gateway_deny_other_outbound',
    'app_to_data_pe','app_dns_udp','app_dns_tcp','app_approved_egress','app_deny_other_outbound',
    'web_pe_from_gateway','web_pe_from_tests','web_pe_deny_other_inbound',
    'data_pe_from_app','data_pe_from_gateway','data_pe_deny_other_inbound'],
  'azurerm_route_table':['app_outbound'],
  'azurerm_subnet_route_table_association':['app_outbound']
}


def find_resource(source: str, rtype: str, name: str):
    pattern=rf'\bresource\s+"{re.escape(rtype)}"\s+"{re.escape(name)}"\s*\{{'
    m=re.search(pattern,source)
    if not m:
        return None
    depth=0
    quote=False
    escaped=False
    for i in range(m.end()-1,len(source)):
        c=source[i]
        if quote:
            if escaped:
                escaped=False
            elif c=='\\':
                escaped=True
            elif c=='"':
                quote=False
            continue
        if c=='"':quote=True
        elif c=='{':depth+=1
        elif c=='}':
            depth-=1
            if depth==0:return source[m.start():i+1]
    return None


def check(root=ROOT):
    root=Path(root)
    errors=[]
    policy_path=root/'infra/modules/network/policy.tf'
    if not policy_path.is_file():
        return {'state':'FAIL','errors':['missing policy.tf'],'azure_live_passes':0,
                'terraform_cli_validation':'NOT_EXECUTED','release_decision':'NO_GO'}
    policy=policy_path.read_text(encoding='utf-8')
    files=list((root/'infra').rglob('*.tf'))
    if len(files)<19:errors.append('expected at least 19 Terraform files')
    for p in files:
        if not lexical_balance(p.read_text(encoding='utf8')):
            errors.append(f'unbalanced HCL lexical delimiters: {p.relative_to(root)}')
    for kind,names in RESOURCES.items():
        for name in names:
            block=find_resource(policy,kind,name)
            if not block:
                errors.append(f'missing {kind}.{name}')
    def must(block_type,name,patterns):
        block=find_resource(policy,block_type,name)
        if block is None:return
        for p in patterns:
            if not re.search(p,block,re.S):
                errors.append(f'{block_type}.{name}: missing {p}')
    NSG='azurerm_network_security_rule'
    must(NSG,'gateway_client_https',[r'source_address_prefixes\s*=\s*var\.approved_client_cidrs',r'destination_port_range\s*=\s*"443"',r'priority\s*=\s*100'])
    must(NSG,'gateway_platform_probe',[r'source_address_prefix\s*=\s*"AzureLoadBalancer"',r'priority\s*=\s*110'])
    for n in ('gateway_deny_other_inbound','gateway_deny_other_outbound','app_deny_other_outbound','web_pe_deny_other_inbound','data_pe_deny_other_inbound'):
        must(NSG,n,[r'access\s*=\s*"Deny"',r'priority\s*=\s*4090',r'destination_address_prefix\s*=\s*"\*"'])
    for n in ('web_pe_from_gateway','data_pe_from_gateway'):
        must(NSG,n,[r'source_address_prefix\s*=\s*var\.subnet_cidrs\.app_gateway',r'destination_port_range\s*=\s*"443"'])
    must(NSG,'data_pe_from_app',[r'source_address_prefix\s*=\s*var\.subnet_cidrs\.app_outbound',r'destination_port_range\s*=\s*"443"'])
    for n,dst in [('gateway_to_web_pe','web_private_endpoint'),('gateway_to_data_pe','data_private_endpoint'),('app_to_data_pe','data_private_endpoint')]:
        must(NSG,n,[rf'destination_address_prefix\s*=\s*var\.subnet_cidrs\.{dst}'])
    for n in ('gateway_dns_udp','app_dns_udp'):
        must(NSG,n,[r'destination_port_range\s*=\s*"53"',r'protocol\s*=\s*"Udp"'])
    for n in ('gateway_dns_tcp','app_dns_tcp'):
        must(NSG,n,[r'destination_port_range\s*=\s*"53"',r'protocol\s*=\s*"Tcp"'])
    if re.search(r'(?m)^\s*source_address_prefix\s*=\s*\"GatewayManager\"', policy):errors.append('legacy GatewayManager source rule in active policy')
    must('azurerm_subnet_network_security_group_association','app_gateway',[
        r'var\.network_policy_approved',r'var\.gateway_network_isolation_approved',r'var\.gateway_egress_profile_approved'])
    must('azurerm_subnet_network_security_group_association','app_outbound',[
        r'var\.network_policy_approved',r'var\.app_egress_profile_approved'])
    for n,target in [('app_gateway','app_gateway'),('app_outbound','app_outbound'),('web_pe','web_private_endpoint'),('data_pe','data_private_endpoint')]:
        must('azurerm_subnet_network_security_group_association',n,[rf'subnet_id\s*=\s*azurerm_subnet\.{target}\.id',rf'azurerm_network_security_group\.{n}\.id'])
    must('azurerm_subnet_route_table_association','app_outbound',[
        r'subnet_id\s*=\s*azurerm_subnet\.app_outbound\.id',r'var\.enable_app_forced_tunnel'])
    if re.search(r'resource\s+"azurerm_subnet_route_table_association"\s+"app_gateway"',policy):
        errors.append('Gateway subnet UDR requires independent architecture approval, not in N04')
    must('azurerm_route_table','app_outbound',[
        r'var\.network_policy_approved',r'var\.approved_firewall_next_hop_ip\s*!=\s*null',r'0\.0\.0\.0/0'])
    env=(root/'infra/environments/dev/main.tf').read_text(encoding='utf8')
    variables=(root/'infra/modules/network/variables.tf').read_text(encoding='utf8')
    devvars=(root/'infra/environments/dev/variables.tf').read_text(encoding='utf8')
    example=(root/'infra/environments/dev/terraform.tfvars.example').read_text(encoding='utf8')
    for var in ('approved_client_cidrs','gateway_extra_egress_rules','app_extra_egress_rules',
                'gateway_network_isolation_approved','gateway_egress_profile_approved',
                'app_egress_profile_approved','network_policy_approved','approved_firewall_next_hop_ip',
                'enable_app_forced_tunnel','approved_dns_resolver_ips','approved_test_runner_cidrs'):
        if not re.search(rf'variable\s+"{var}"',variables):errors.append(f'missing module variable {var}')
        if not re.search(rf'variable\s+"{var}"',devvars):errors.append(f'missing dev variable {var}')
        if not re.search(rf'^\s*{var}\s*=\s*var\.{var}\s*$',env,re.M):errors.append(f'unwired variable {var}')
    for var in ('gateway_network_isolation_approved','gateway_egress_profile_approved','app_egress_profile_approved','network_policy_approved'):
        block=re.search(rf'variable\s+"{var}"\s*\{{[^}}]*\}}',variables,re.S)
        if not block or not re.search(r'default\s*=\s*false',block.group()):errors.append(f'{var} must default false')
        if not re.search(rf'^\s*{var}\s*=\s*false\s*$',example,re.M):errors.append(f'{var} example must be false')
    if '0.0.0.0/0" is forbidden' in variables:pass
    if not re.search(r'c\s*!=\s*"0\.0\.0\.0/0"',variables):errors.append('missing CIDR /0 validation')
    subnet=(root/'infra/modules/network/main.tf').read_text(encoding='utf8')
    for n in ('web_private_endpoint','data_private_endpoint'):
        block=find_resource(subnet,'azurerm_subnet',n)
        if not block or not re.search(r'private_endpoint_network_policies\s*=\s*"Enabled"',block):
            errors.append(f'{n}: PE NSG network policies missing')
    if re.search(r'(?im)^\s*public_network_access_enabled\s*=\s*true\b',policy):errors.append('forbidden public network true')
    if re.search(r'(?i)(client_secret|access_key|sas_token)\s*=\s*"[^"\s]+"',policy):errors.append('suspected embedded secret')
    return {'state':'PASS_OFFLINE_N04_TEXT_ONLY' if not errors else 'FAIL',
            'terraform_cli_validation':'NOT_EXECUTED','terraform_plan':'NOT_EXECUTED','terraform_apply':'NOT_EXECUTED',
            'azure_live_passes':0,'live_acceptance_not_ready':1716,'release_decision':'NO_GO',
            'terraform_file_count':len(files),'nsg_count':4,'nsg_rule_count':20,
            'errors':errors}

if __name__=='__main__':
    x=check();print(json.dumps(x,indent=2));sys.exit(bool(x['errors']))
