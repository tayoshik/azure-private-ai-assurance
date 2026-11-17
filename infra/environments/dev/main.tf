# Workload root: no actual resources should be planned or applied until
# G07 approved inputs AND B05 private backend access have been attested.
locals {
  tags = merge(var.common_tags, {
    environment = "dev"
    managed_by  = "terraform"
  })
}

module "foundation" {
  source   = "../../modules/foundation"
  name     = var.resource_group_name
  location = var.location
  tags     = local.tags
}

module "network" {
  source                             = "../../modules/network"
  name                               = var.vnet_name
  resource_group_name                = module.foundation.name
  location                           = module.foundation.location
  vnet_cidr                          = var.vnet_cidr
  subnet_cidrs                       = var.subnet_cidrs
  approved_client_cidrs              = var.approved_client_cidrs
  approved_test_runner_cidrs         = var.approved_test_runner_cidrs
  approved_dns_resolver_ips          = var.approved_dns_resolver_ips
  gateway_extra_egress_rules         = var.gateway_extra_egress_rules
  app_extra_egress_rules             = var.app_extra_egress_rules
  network_policy_approved            = var.network_policy_approved
  gateway_network_isolation_approved = var.gateway_network_isolation_approved
  gateway_egress_profile_approved    = var.gateway_egress_profile_approved
  app_egress_profile_approved        = var.app_egress_profile_approved
  enable_app_forced_tunnel           = var.enable_app_forced_tunnel
  approved_firewall_next_hop_ip      = var.approved_firewall_next_hop_ip
  tags                               = local.tags
}

module "private_dns" {
  source              = "../../modules/private-dns"
  resource_group_name = module.foundation.name
  virtual_network_id  = module.network.vnet_id
  zone_names          = var.private_dns_zone_names
  tags                = local.tags
}


# I01: Independent managed identities for the web app and Gateway.
module "identity" {
  source                = "../../modules/identity"
  resource_group_name   = module.foundation.name
  location              = module.foundation.location
  app_identity_name     = var.app_identity_name
  gateway_identity_name = var.gateway_identity_name
  tags                  = local.tags
}

# I02: No secret or certificate material is committed to Terraform state.
module "key_vault" {
  source                              = "../../modules/key-vault"
  name                                = var.key_vault_name
  resource_group_name                 = module.foundation.name
  location                            = module.foundation.location
  tenant_id                           = var.tenant_id
  tags                                = local.tags
  app_principal_id                    = module.identity.app_principal_id
  gateway_principal_id                = module.identity.gateway_principal_id
  key_vault_configuration_approved    = var.key_vault_configuration_approved
  app_secrets_reader_approved         = var.app_secrets_reader_approved
  gateway_certificate_reader_approved = var.gateway_certificate_reader_approved
  role_assignment_approval_confirmed  = var.role_assignment_approval_confirmed
}

# I03: existing data Private Endpoint subnet, matching vault DNS zone.
module "key_vault_private_endpoint" {
  source                              = "../../modules/private-endpoints"
  name                                = var.key_vault_private_endpoint_name
  location                            = module.foundation.location
  resource_group_name                 = module.foundation.name
  subnet_id                           = module.network.data_private_endpoint_subnet_id
  key_vault_id                        = module.key_vault.id
  key_vault_dns_zone_id               = module.private_dns.zone_ids["privatelink.vaultcore.azure.net"]
  key_vault_private_endpoint_approved = var.key_vault_private_endpoint_approved
  tags                                = local.tags
}


# A01/A02: OpenAI model, exact version and quota are approval-controlled.
module "azure_openai" {
  source                    = "../../modules/azure-openai"
  name                      = var.openai_account_name
  custom_subdomain_name     = var.openai_custom_subdomain
  location                  = module.foundation.location
  resource_group_name       = module.foundation.name
  tags                      = local.tags
  model_deployment_name     = var.openai_deployment_name
  model_name                = var.openai_model_name
  model_version             = var.openai_model_version
  model_sku                 = var.openai_model_sku
  model_capacity            = var.openai_model_capacity
  openai_account_approved   = var.openai_account_approved
  region_and_quota_approved = var.openai_region_quota_approved
  model_deployment_approved = var.openai_model_deployment_approved
}

# A03: Azure AI Search is private-only and forbids shared API-key auth.
module "ai_search" {
  source                  = "../../modules/ai-search"
  name                    = var.search_service_name
  location                = module.foundation.location
  resource_group_name     = module.foundation.name
  tags                    = local.tags
  sku                     = var.search_sku
  replica_count           = var.search_replica_count
  partition_count         = var.search_partition_count
  search_approved         = var.search_service_approved
  region_and_sku_approved = var.search_region_sku_approved
}

# A04: Cosmos for NoSQL only (Entra auth; no account keys for app).
module "cosmos_db" {
  source                     = "../../modules/cosmos-db"
  name                       = var.cosmos_account_name
  location                   = module.foundation.location
  resource_group_name        = module.foundation.name
  tags                       = local.tags
  database_name              = var.cosmos_database_name
  container_name             = var.cosmos_container_name
  partition_key_paths        = var.cosmos_partition_key_paths
  consistency_level          = var.cosmos_consistency_level
  backup_tier                = var.cosmos_backup_tier
  cosmos_account_approved    = var.cosmos_account_approved
  backup_and_budget_approved = var.cosmos_backup_budget_approved
}

# A05: Dedicated PE module keeps earlier Key Vault PE ownership unchanged.
module "ai_data_private_endpoints" {
  source                     = "../../modules/ai-private-endpoints"
  location                   = module.foundation.location
  resource_group_name        = module.foundation.name
  tags                       = local.tags
  subnet_id                  = module.network.data_private_endpoint_subnet_id
  openai_pe_name             = var.openai_private_endpoint_name
  search_pe_name             = var.search_private_endpoint_name
  cosmos_pe_name             = var.cosmos_private_endpoint_name
  openai_account_id          = module.azure_openai.account_id
  search_service_id          = module.ai_search.id
  cosmos_account_id          = module.cosmos_db.account_id
  openai_zone_id             = module.private_dns.zone_ids["privatelink.openai.azure.com"]
  search_zone_id             = module.private_dns.zone_ids["privatelink.search.windows.net"]
  cosmos_zone_id             = module.private_dns.zone_ids["privatelink.documents.azure.com"]
  private_endpoints_approved = var.ai_private_endpoints_approved
  depends_on                 = [module.network] # NSG/policy attachments must exist before PE resources.
}

# A06: explicit app MI and three service-specific data roles.
module "ai_data_rbac" {
  source                              = "../../modules/ai-data-rbac"
  resource_group_name                 = module.foundation.name
  app_principal_id                    = module.identity.app_principal_id
  openai_account_id                   = module.azure_openai.account_id
  search_service_id                   = module.ai_search.id
  cosmos_account_id                   = module.cosmos_db.account_id
  cosmos_account_name                 = module.cosmos_db.account_name
  cosmos_database_name                = module.cosmos_db.database_name
  cosmos_container_name               = module.cosmos_db.container_name
  rbac_approved                       = var.ai_data_rbac_approved
  cosmos_write_approved               = var.cosmos_data_write_approved
  cosmos_write_justification_approved = var.cosmos_write_justification_approved
}


# W01-W03/W05: single App Service module with managed identity, no keys.
module "app_service" {
  source                         = "../../modules/app-service"
  location                       = module.foundation.location
  resource_group_name            = module.foundation.name
  tags                           = local.tags
  service_plan_name              = var.app_service_plan_name
  service_plan_sku               = var.app_service_plan_sku
  web_app_name                   = var.app_web_name
  python_version                 = var.app_python_version
  health_check_path              = var.app_health_check_path
  app_identity_id                = module.identity.app_identity_id
  app_identity_client_id         = module.identity.app_client_id
  app_outbound_subnet_id         = module.network.app_outbound_subnet_id
  web_inbound_pe_subnet_id       = module.network.web_private_endpoint_subnet_id
  openai_endpoint                = module.azure_openai.endpoint
  openai_deployment_name         = module.azure_openai.deployment_name
  search_hostname                = module.ai_search.hostname
  cosmos_endpoint                = module.cosmos_db.account_endpoint
  cosmos_database_name           = module.cosmos_db.database_name
  cosmos_container_name          = module.cosmos_db.container_name
  app_service_plan_approved      = var.app_service_plan_approved
  region_and_capacity_approved   = var.app_region_capacity_approved
  web_app_configuration_approved = var.web_app_configuration_approved
  outbound_integration_approved  = var.app_outbound_integration_approved
  application_contract_approved  = var.application_contract_approved
  depends_on                     = [module.network, module.ai_data_rbac]
}

# W04: inbound Web App PE on a different subnet; same private DNS authority.
module "webapp_private_endpoint" {
  source                        = "../../modules/webapp-private-endpoint"
  private_endpoint_name         = var.app_web_private_endpoint_name
  location                      = module.foundation.location
  resource_group_name           = module.foundation.name
  web_inbound_pe_subnet_id      = module.network.web_private_endpoint_subnet_id
  app_outbound_subnet_id        = module.network.app_outbound_subnet_id
  web_app_id                    = module.app_service.web_app_id
  webapp_private_dns_zone_id    = module.private_dns.zone_ids["privatelink.azurewebsites.net"]
  web_private_endpoint_approved = var.web_private_endpoint_approved
  private_dns_and_scm_approved  = var.web_private_dns_scm_approved
  tags                          = local.tags
  depends_on                    = [module.network]
}


# O01/O02: Workload audit workspace and opt-in Monitor Private Link.
module "monitoring" {
  source                                    = "../../modules/monitoring"
  name                                      = var.monitor_workspace_name
  location                                  = module.foundation.location
  resource_group_name                       = module.foundation.name
  retention_in_days                         = var.monitor_retention_days
  monitoring_and_private_ingestion_approved = var.monitoring_private_ingestion_approved
  private_link                              = var.monitoring_private_link
  workload_vnet_id                          = module.network.vnet_id
  subscription_id                           = var.subscription_id
  tags                                      = local.tags
}

# GW01–GW05: private-only WAF_v2, UAI/KV TLS, backend health and diagnostics.
# The app's default hostname is used for backend TLS Host/SNI; the private
# business FQDN is used ONLY for the gateway listener and on-prem DNS.
module "application_gateway" {
  source                                      = "../../modules/application-gateway"
  name                                        = var.application_gateway_name
  location                                    = module.foundation.location
  resource_group_name                         = module.foundation.name
  tags                                        = local.tags
  gateway_subnet_id                           = module.network.app_gateway_subnet_id
  gateway_subnet_cidr                         = var.subnet_cidrs.app_gateway
  private_frontend_ip                         = var.gateway_private_frontend_ip
  gateway_identity_id                         = module.identity.gateway_identity_id
  key_vault_certificate_secret_versionless_id = var.gateway_certificate_secret_versionless_id
  business_fqdn                               = var.gateway_business_fqdn
  backend_app_fqdn                            = module.app_service.default_hostname
  health_check_path                           = var.app_health_check_path
  gateway_capacity                            = var.application_gateway_capacity
  waf_mode                                    = var.application_gateway_waf_mode
  waf_drs_version                             = var.application_gateway_waf_drs_version
  log_analytics_workspace_id                  = module.monitoring.workspace_id
  private_gateway_feature_approved            = var.private_gateway_feature_approved
  gateway_ipam_and_routes_approved            = var.gateway_ipam_and_routes_approved
  backend_dns_tls_approved                    = var.gateway_backend_dns_tls_approved
  certificate_import_and_rbac_approved        = var.gateway_certificate_import_rbac_approved
  waf_policy_approved                         = var.gateway_waf_policy_approved
  waf_prevention_approved                     = var.gateway_waf_prevention_approved
  logging_route_approved                      = var.gateway_logging_route_approved
  depends_on = [module.network, module.webapp_private_endpoint,
  module.key_vault_private_endpoint, module.key_vault, module.monitoring]
}
