#!/usr/bin/env python3
"""Offline text contracts for proposed gateway code. Never Azure/Provider proof."""
import json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={
 "gateway": "infra/modules/application-gateway/gateway.tf",
 "waf": "infra/modules/application-gateway/waf-policy.tf",
 "routing": "infra/modules/application-gateway/routing.tf",
 "logging": "infra/modules/application-gateway/diagnostics.tf",
 "gw_vars": "infra/modules/application-gateway/variables.tf",
 "monitor": "infra/modules/monitoring/main.tf",
 "root_main": "infra/environments/dev/main.tf",
 "root_vars": "infra/environments/dev/variables.tf",
 "example": "infra/environments/dev/terraform.tfvars.example",
 "network": "infra/modules/network/main.tf",
 "nsg": "infra/modules/network/policy.tf",
 "vault": "infra/modules/key-vault/main.tf",
}
def no_comments(s):
    return "\n".join(line.split('#',1)[0] for line in s.splitlines() if not line.lstrip().startswith(('//','#')))
def check(root=ROOT):
    root=Path(root); errors=[]; txt={}
    for key,rel in FILES.items():
        p=root/rel
        if not p.is_file():errors.append("missing: "+rel);txt[key]="";continue
        txt[key]=no_comments(p.read_text(encoding='utf-8'))
    def require(key,regex,name):
        if not re.search(regex,txt[key],re.M|re.S):errors.append("missing/unexpected: "+name)
    def forbid(key,regex,name):
        if re.search(regex,txt[key],re.M|re.S):errors.append("forbidden: "+name)
    require("gateway",r'resource\s+"azurerm_application_gateway"\s+"private_web"',"private gateway resource")
    require("gateway",r'private_ip_address_allocation\s*=\s*"Static"',"static private frontend")
    require("gateway",r'private_ip_address\s*=\s*var.private_frontend_ip',"frontend from IPAM variable")
    require("gateway",r'firewall_policy_id\s*=\s*azurerm_web_application_firewall_policy.private_web.id',"WAF association")
    require("gateway",r'(?m)^\s*name\s*=\s*"WAF_v2"',"WAF_v2 SKU")
    require("gateway",r'(?m)^\s*tier\s*=\s*"WAF_v2"',"WAF_v2 tier")
    forbid("gateway",r'\bpublic_ip_address_id\b|\bpublic_ip_address\s*=',"public Gateway frontend")
    require("gateway",r'identity\s*\{\s*type\s*=\s*"UserAssigned"\s*identity_ids\s*=\s*\[var.gateway_identity_id\]',"gateway identity")
    require("gateway",r'key_vault_secret_id\s*=\s*var.key_vault_certificate_secret_versionless_id',"Key Vault TLS reference")
    forbid("gateway",r'(?m)^\s*(data|password)\s*=',"PFX private key/password in Terraform")
    require("gateway",r'(?m)^\s*fqdns\s*=\s*\[var.backend_app_fqdn\]',"canonical App Service backend")
    require("gateway",r'(?m)^\s*protocol\s*=\s*"Https"',"TLS backend")
    require("gateway",r'(?m)^\s*host_name\s*=\s*var.backend_app_fqdn',"backend Host/SNI")
    require("gateway",r'(?m)^\s*host\s*=\s*var.backend_app_fqdn',"probe Host")
    require("gateway",r'(?m)^\s*path\s*=\s*var.health_check_path',"health path")
    require("gateway",r'(?m)^\s*host_name\s*=\s*var.business_fqdn',"business listener Host")
    require("gateway",r'(?m)^\s*prevent_destroy\s*=\s*true',"prevent destroy")
    require("gateway",r'var.private_gateway_feature_approved\s*&&\s*var.gateway_ipam_and_routes_approved',"network isolation approval gate")
    require("gateway",r'var.backend_dns_tls_approved\s*&&\s*var.certificate_import_and_rbac_approved',"certificate, DNS and TLS gate")
    require("waf",r'azurerm_web_application_firewall_policy',"WAF policy")
    require("waf",r'(?m)^\s*type\s*=\s*"Microsoft_DefaultRuleSet"',"Microsoft DRS")
    require("waf",r'(?m)^\s*version\s*=\s*var.waf_drs_version',"reviewed DRS version")
    require("waf",r'(?m)^\s*mode\s*=\s*var.waf_mode',"WAF mode variable")
    require("waf",r'var.waf_mode\s*==\s*"Detection"\s*\|\|\s*var.waf_prevention_approved',"Prevention approval")
    require("routing",r'local[s]?\s*\{',"routing canonical names")
    require("logging",r'log_analytics_destination_type\s*=\s*"Dedicated"',"dedicated log tables")
    require("logging",r'category\s*=\s*"ApplicationGatewayAccessLog"',"access log")
    require("logging",r'category\s*=\s*"ApplicationGatewayFirewallLog"',"firewall log")
    require("logging",r'var.logging_route_approved',"ingestion approval")
    require("monitor",r'internet_ingestion_enabled\s*=\s*false',"workspace public ingestion disabled")
    require("monitor",r'internet_query_enabled\s*=\s*false',"workspace public query disabled")
    require("monitor",r'var.monitoring_and_private_ingestion_approved',"AMPLS prerequisite gate")
    require("root_main",r'module\s+"application_gateway"',"root Gateway module")
    require("root_main",r'module\s+"monitoring"',"root monitoring module")
    require("root_main",r'backend_app_fqdn\s*=\s*module.app_service.default_hostname',"TLS backend wiring")
    require("root_main",r'gateway_subnet_id\s*=\s*module.network.app_gateway_subnet_id',"Gateway subnet wiring")
    require("root_main",r'gateway_identity_id\s*=\s*module.identity.gateway_identity_id',"Gateway identity wiring")
    require("root_main",r'depends_on\s*=\s*\[module.network,\s*module.webapp_private_endpoint,',"private backend dependency")
    require("network",r'Microsoft.Network/applicationGateways',"gateway subnet delegation")
    require("nsg",r'(?m)^\s*source_address_prefix\s*=\s*"AzureLoadBalancer"',"platform probe")
    require("vault",r'role_definition_name\s*=\s*"Key Vault Secrets User"',"Vault minimum certificate role")
    for k in ["private_gateway_feature_approved","gateway_ipam_and_routes_approved","gateway_backend_dns_tls_approved","gateway_certificate_import_rbac_approved","gateway_waf_policy_approved","gateway_waf_prevention_approved","gateway_logging_route_approved","monitoring_private_ingestion_approved"]:
        require("example",rf'(?m)^\s*{k}\s*=\s*false\s*$',k+" example false")
        require("root_vars",rf'variable\s+"{k}"\s*\{{\s*type\s*=\s*bool\s*default\s*=\s*false\s*\}}',k+" var default false")
    forbid("gw_vars",r'(?m)^\s*[^#\n]+;\s*default\s*=',"semicolon-delimited HCL attributes")
    return {'status':'PASS_OFFLINE_TEXT_ONLY' if not errors else 'FAIL','errors':errors,'azure_live_passes':0,'release_decision':'NO_GO','checked_file_count':len(FILES)}
if __name__=='__main__':
    out=check();print(json.dumps(out,indent=2));raise SystemExit(bool(out['errors']))
