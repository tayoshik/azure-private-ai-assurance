#!/usr/bin/env python3
"""Offline W01-W05 text-contract checker; not Terraform parsing, plan or Azure acceptance."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RULES={
 "infra/modules/app-service/plan.tf":[
 r'resource\s+"azurerm_service_plan"\s+"app"',r'os_type\s*=\s*"Linux"',
 r'var\.app_service_plan_approved\s*&&\s*var\.region_and_capacity_approved'],
 "infra/modules/app-service/webapp.tf":[
 r'resource\s+"azurerm_linux_web_app"\s+"app"',
 r'(?m)^\s*https_only\s*=\s*true',
 r'(?m)^\s*public_network_access_enabled\s*=\s*false',
 r'(?m)^\s*ftp_publish_basic_authentication_enabled\s*=\s*false',
 r'(?m)^\s*webdeploy_publish_basic_authentication_enabled\s*=\s*false',
 r'(?m)^\s*ftps_state\s*=\s*"Disabled"',
 r'(?m)^\s*minimum_tls_version\s*=\s*"1\.2"',
 r'(?m)^\s*scm_minimum_tls_version\s*=\s*"1\.2"',
 r'(?m)^\s*vnet_route_all_enabled\s*=\s*true',
 r'identity_ids\s*=\s*\[var\.app_identity_id\]',
 r'virtual_network_subnet_id\s*=\s*local\.approved_outbound_integration_subnet_id',
 r'var\.web_app_configuration_approved\s*&&\s*var\.outbound_integration_approved',
 r'var\.application_contract_approved',
 r'var\.app_outbound_subnet_id\s*!=\s*var\.web_inbound_pe_subnet_id'],
 "infra/modules/app-service/app-settings.tf":[
 r'AZURE_CLIENT_ID\s*=\s*var\.app_identity_client_id',
 r'AZURE_OPENAI_ENDPOINT\s*=\s*var\.openai_endpoint',
 r'AZURE_SEARCH_ENDPOINT\s*=\s*"https://',
 r'COSMOS_DB_ENDPOINT\s*=\s*var\.cosmos_endpoint'],
 "infra/modules/app-service/outbound-vnet.tf":[
 r'approved_outbound_integration_subnet_id\s*=\s*var\.app_outbound_subnet_id'],
 "infra/modules/webapp-private-endpoint/webapp.tf":[
 r'resource\s+"azurerm_private_endpoint"\s+"web_app"',
 r'subresource_names\s*=\s*\["sites"\]',
 r'private_dns_zone_ids\s*=\s*\[var\.webapp_private_dns_zone_id\]',
 r'var\.web_private_endpoint_approved\s*&&\s*var\.private_dns_and_scm_approved',
 r'var\.web_inbound_pe_subnet_id\s*!=\s*var\.app_outbound_subnet_id'],
 "infra/environments/dev/main.tf":[
 r'module\s+"app_service"\s*\{',r'module\s+"webapp_private_endpoint"\s*\{',
 r'webapp_private_dns_zone_id\s*=\s*module\.private_dns\.zone_ids\["privatelink\.azurewebsites\.net"\]',
 r'app_outbound_subnet_id\s*=\s*module\.network\.app_outbound_subnet_id',
 r'web_inbound_pe_subnet_id\s*=\s*module\.network\.web_private_endpoint_subnet_id',
 r'depends_on\s*=\s*\[module\.network,\s*module\.ai_data_rbac\]'],
 "infra/environments/dev/outputs.tf":[
 r'output\s+"app_web_private_endpoint_ip"',r'output\s+"app_web_default_hostname"']
}
GATES=['app_service_plan_approved','app_region_capacity_approved',
'web_app_configuration_approved','app_outbound_integration_approved',
'application_contract_approved','web_private_endpoint_approved','web_private_dns_scm_approved']

def check(root=ROOT):
 root=Path(root)
 errors=[]
 for path,rules in RULES.items():
  f=root/path
  if not f.is_file():errors.append("missing: "+path);continue
  s=f.read_text(encoding="utf8")
  for pattern in rules:
   if not re.search(pattern,s):errors.append(path+" requires "+pattern)
 variables=root/"infra/environments/dev/variables.tf"
 example=root/"infra/environments/dev/terraform.tfvars.example"
 if variables.is_file() and example.is_file():
  v=variables.read_text(encoding="utf8")
  x=example.read_text(encoding="utf8")
  for gate in GATES:
   if not re.search(r'variable\s+"'+gate+r'"\s*\{\s*type\s*=\s*bool\s*default\s*=\s*false\s*\}',v):
    errors.append("fail-closed root variable: "+gate)
   if not re.search(r'(?m)^'+gate+r'\s*=\s*false\s*$',x):
    errors.append("fail-closed sample: "+gate)
 else:errors.append("missing root vars or tfvars example")
 for f in (root/"infra").rglob("*.tf"):
  s=f.read_text(encoding="utf8")
  if re.search(r'(?m)^(?!\s*#)\s*resource\s+"azurerm_app_service_virtual_network_swift_connection"',s):
   errors.append("conflicting Swift VNet ownership")
  if re.search(r'variable\s+"[\w-]+"\s*\{\s*type\s*=[^}]*[,;]\s*default\s*=',s):
   errors.append("invalid compact HCL multiattribute block: "+f.name)
 return {"status":"PASS_OFFLINE_TEXT_ONLY" if not errors else "FAIL",
         "errors":errors,"azure_live_passes":0,"terraform_cli_validate":False}
if __name__=="__main__":
 r=check()
 print(json.dumps(r,indent=2))
 raise SystemExit(bool(r["errors"]))
