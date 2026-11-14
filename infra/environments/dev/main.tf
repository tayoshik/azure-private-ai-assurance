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
