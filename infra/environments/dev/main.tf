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
