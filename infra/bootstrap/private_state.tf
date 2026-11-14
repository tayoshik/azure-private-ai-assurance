# B04: management network is independent from the workload VNet/subnets.
# CI reachability to this VNet requires a separate approved route/runner gate.
resource "azurerm_virtual_network" "bootstrap" {
  name                = var.bootstrap_vnet_name
  resource_group_name = azurerm_resource_group.bootstrap.name
  location            = azurerm_resource_group.bootstrap.location
  address_space       = [var.bootstrap_vnet_cidr]
  tags                = var.tags
}

resource "azurerm_subnet" "state_pe" {
  name                              = var.bootstrap_pe_subnet_name
  resource_group_name               = azurerm_resource_group.bootstrap.name
  virtual_network_name              = azurerm_virtual_network.bootstrap.name
  address_prefixes                  = [var.bootstrap_pe_subnet_cidr]
  private_endpoint_network_policies = "Enabled"
}

resource "azurerm_private_dns_zone" "blob" {
  name                = "privatelink.blob.core.windows.net"
  resource_group_name = azurerm_resource_group.bootstrap.name
  tags                = var.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "bootstrap" {
  name                  = "bootstrap-blob-link"
  resource_group_name   = azurerm_resource_group.bootstrap.name
  private_dns_zone_name = azurerm_private_dns_zone.blob.name
  virtual_network_id    = azurerm_virtual_network.bootstrap.id
  registration_enabled  = false
  tags                  = var.tags
}

resource "azurerm_private_endpoint" "state_blob" {
  name                = "pe-${var.storage_account_name}-blob"
  resource_group_name = azurerm_resource_group.bootstrap.name
  location            = azurerm_resource_group.bootstrap.location
  subnet_id           = azurerm_subnet.state_pe.id
  tags                = var.tags

  private_service_connection {
    name                           = "state-blob"
    private_connection_resource_id = azurerm_storage_account.state.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "blob"
    private_dns_zone_ids = [azurerm_private_dns_zone.blob.id]
  }
}
