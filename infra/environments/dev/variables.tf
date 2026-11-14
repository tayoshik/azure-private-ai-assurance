variable "subscription_id" {
  type        = string
  description = "Approved target subscription; supply via restricted CI variables."
  validation {
    condition     = can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", var.subscription_id)) && lower(var.subscription_id) != "00000000-0000-0000-0000-000000000000"
    error_message = "An approved non-placeholder subscription UUID is required."
  }
}
variable "location" {
  type = string
}
variable "resource_group_name" {
  type = string
}
variable "vnet_name" {
  type = string
}
variable "vnet_cidr" {
  type = string
}
variable "subnet_cidrs" {
  type = object({
    app_gateway           = string
    app_outbound          = string
    web_private_endpoint  = string
    data_private_endpoint = string
  })
}
variable "private_dns_zone_names" {
  type    = list(string)
  default = [
    "privatelink.azurewebsites.net",
    "privatelink.openai.azure.com",
    "privatelink.search.windows.net",
    "privatelink.documents.azure.com",
    "privatelink.vaultcore.azure.net"
  ]
}
variable "common_tags" {
  type = map(string)
  default = {
    workload     = "azure-private-ai-assurance"
    sensitivity  = "restricted"
  }
}

# The dev root never approves network controls implicitly.
variable "approved_client_cidrs" {
  type        = list(string)
  description = "Signed client IPAM; no default."
}
variable "approved_dns_resolver_ips" {
  type        = list(string)
  default     = []
}
variable "approved_test_runner_cidrs" {
  type        = list(string)
  default     = []
}
variable "gateway_extra_egress_rules" {
  type = map(object({
    destination_cidr = string
    destination_port = number
    priority         = number
  }))
  default = {}
}
variable "app_extra_egress_rules" {
  type = map(object({
    destination_cidr = string
    destination_port = number
    priority         = number
  }))
  default = {}
}
variable "network_policy_approved" {
  type    = bool
  default = false
}
variable "gateway_network_isolation_approved" {
  type    = bool
  default = false
}
variable "gateway_egress_profile_approved" {
  type    = bool
  default = false
}
variable "app_egress_profile_approved" {
  type    = bool
  default = false
}
variable "enable_app_forced_tunnel" {
  type    = bool
  default = false
}
variable "approved_firewall_next_hop_ip" {
  type     = string
  default  = null
  nullable = true
}


# I01-I03: Values come from G01/G03/G07 approvals, never a public tfvars file.
variable "tenant_id" {
  type = string
}
variable "app_identity_name" { type = string }
variable "gateway_identity_name" { type = string }
variable "key_vault_name" { type = string }
variable "key_vault_private_endpoint_name" { type = string }
variable "key_vault_configuration_approved" {
  type    = bool
  default = false
}
variable "key_vault_private_endpoint_approved" {
  type    = bool
  default = false
}
variable "app_secrets_reader_approved" {
  type    = bool
  default = false
}
variable "gateway_certificate_reader_approved" {
  type    = bool
  default = false
}
variable "role_assignment_approval_confirmed" {
  type    = bool
  default = false
}


# A01-A06 inputs: no deployable defaults for location, model or resource names.
variable "openai_account_name" { type = string }
variable "openai_custom_subdomain" { type = string }
variable "openai_deployment_name" { type = string }
variable "openai_model_name" { type = string }
variable "openai_model_version" { type = string }
variable "openai_model_sku" { type = string }
variable "openai_model_capacity" { type = number }
variable "search_service_name" { type = string }
variable "search_sku" { type = string }
variable "search_replica_count" { type = number }
variable "search_partition_count" { type = number }
variable "cosmos_account_name" { type = string }
variable "cosmos_database_name" { type = string }
variable "cosmos_container_name" { type = string }
variable "cosmos_partition_key_paths" { type = list(string) }
variable "cosmos_consistency_level" { type = string }
variable "cosmos_backup_tier" { type = string }
variable "openai_private_endpoint_name" { type = string }
variable "search_private_endpoint_name" { type = string }
variable "cosmos_private_endpoint_name" { type = string }
variable "openai_account_approved" {
  type    = bool
  default = false
}
variable "openai_region_quota_approved" {
  type    = bool
  default = false
}
variable "openai_model_deployment_approved" {
  type    = bool
  default = false
}
variable "search_service_approved" {
  type    = bool
  default = false
}
variable "search_region_sku_approved" {
  type    = bool
  default = false
}
variable "cosmos_account_approved" {
  type    = bool
  default = false
}
variable "cosmos_backup_budget_approved" {
  type    = bool
  default = false
}
variable "ai_private_endpoints_approved" {
  type    = bool
  default = false
}
variable "ai_data_rbac_approved" {
  type    = bool
  default = false
}
variable "cosmos_data_write_approved" {
  type    = bool
  default = false
}
variable "cosmos_write_justification_approved" {
  type    = bool
  default = false
}


# W01-W05: approval defaults deliberately deny planning.
variable "app_service_plan_name" { type = string }
variable "app_service_plan_sku" { type = string }
variable "app_web_name" { type = string }
variable "app_python_version" { type = string }
variable "app_health_check_path" { type = string }
variable "app_web_private_endpoint_name" { type = string }
variable "app_service_plan_approved" {
  type    = bool
  default = false
}
variable "app_region_capacity_approved" {
  type    = bool
  default = false
}
variable "web_app_configuration_approved" {
  type    = bool
  default = false
}
variable "app_outbound_integration_approved" {
  type    = bool
  default = false
}
variable "application_contract_approved" {
  type    = bool
  default = false
}
variable "web_private_endpoint_approved" {
  type    = bool
  default = false
}
variable "web_private_dns_scm_approved" {
  type    = bool
  default = false
}


# GW01-GW05 / O01: all deployment approvals start FALSE.
variable "application_gateway_name" { type = string }
variable "gateway_private_frontend_ip" { type = string }
variable "gateway_certificate_secret_versionless_id" { type = string }
variable "gateway_business_fqdn" { type = string }
variable "application_gateway_capacity" {
  type = number
  default = 2
}
variable "application_gateway_waf_mode" {
  type = string
  default = "Detection"
}
variable "application_gateway_waf_drs_version" {
  type = string
  default = "2.2"
}
variable "monitor_workspace_name" { type = string }
variable "monitor_retention_days" {
  type = number
  default = 30
}
variable "monitoring_private_ingestion_approved" {
  type = bool
  default = false
}
variable "private_gateway_feature_approved" {
  type = bool
  default = false
}
variable "gateway_ipam_and_routes_approved" {
  type = bool
  default = false
}
variable "gateway_backend_dns_tls_approved" {
  type = bool
  default = false
}
variable "gateway_certificate_import_rbac_approved" {
  type = bool
  default = false
}
variable "gateway_waf_policy_approved" {
  type = bool
  default = false
}
variable "gateway_waf_prevention_approved" {
  type = bool
  default = false
}
variable "gateway_logging_route_approved" {
  type = bool
  default = false
}
