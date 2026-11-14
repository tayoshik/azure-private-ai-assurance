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
  tags                = local.tags
}

module "private_dns" {
  source              = "../../modules/private-dns"
  resource_group_name = module.foundation.name
  virtual_network_id  = module.network.vnet_id
  zone_names          = var.private_dns_zone_names
  tags                = local.tags
}
