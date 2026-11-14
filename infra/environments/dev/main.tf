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
  source              = "../../modules/network"
  name                = var.vnet_name
  resource_group_name = module.foundation.name
  location            = module.foundation.location
  vnet_cidr           = var.vnet_cidr
  subnet_cidrs        = var.subnet_cidrs
  approved_client_cidrs = var.approved_client_cidrs
  approved_test_runner_cidrs = var.approved_test_runner_cidrs
  approved_dns_resolver_ips = var.approved_dns_resolver_ips
  gateway_extra_egress_rules = var.gateway_extra_egress_rules
  app_extra_egress_rules = var.app_extra_egress_rules
  network_policy_approved = var.network_policy_approved
  gateway_network_isolation_approved = var.gateway_network_isolation_approved
  gateway_egress_profile_approved = var.gateway_egress_profile_approved
  app_egress_profile_approved = var.app_egress_profile_approved
  enable_app_forced_tunnel = var.enable_app_forced_tunnel
  approved_firewall_next_hop_ip = var.approved_firewall_next_hop_ip
  tags                = local.tags
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
