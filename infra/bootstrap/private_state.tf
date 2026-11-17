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

moved {
  from = azurerm_private_dns_zone.blob
  to   = azurerm_private_dns_zone.blob[0]
}

moved {
  from = azurerm_private_dns_zone_virtual_network_link.bootstrap
  to   = azurerm_private_dns_zone_virtual_network_link.bootstrap[0]
}

resource "azurerm_private_dns_zone" "blob" {
  count               = var.existing_blob_dns_zone_id == null ? 1 : 0
  name                = "privatelink.blob.core.windows.net"
  resource_group_name = azurerm_resource_group.bootstrap.name
  tags                = var.tags

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_private_dns_zone_virtual_network_link" "bootstrap" {
  count                 = var.existing_blob_dns_zone_id == null ? 1 : 0
  name                  = "bootstrap-blob-link"
  resource_group_name   = azurerm_resource_group.bootstrap.name
  private_dns_zone_name = azurerm_private_dns_zone.blob[0].name
  virtual_network_id    = azurerm_virtual_network.bootstrap.id
  registration_enabled  = false
  tags                  = var.tags

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_private_endpoint" "state_blob" {
  name                = "pe-${var.storage_account_name}-blob"
  resource_group_name = azurerm_resource_group.bootstrap.name
  location            = azurerm_resource_group.bootstrap.location
  subnet_id           = azurerm_subnet.state_pe.id
  tags                = var.tags

  depends_on = [azurerm_subnet_network_security_group_association.state_pe]

  private_service_connection {
    name                           = "state-blob"
    private_connection_resource_id = azurerm_storage_account.state.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "blob"
    private_dns_zone_ids = [var.existing_blob_dns_zone_id != null ? var.existing_blob_dns_zone_id : azurerm_private_dns_zone.blob[0].id]
  }
}

variable "state_runner_cidrs" {
  description = "Approved private management/Runner IPv4 sources for Blob HTTPS. Empty preserves the legacy layout."
  type        = list(string)
  default     = []

  validation {
    condition     = alltrue([for cidr in var.state_runner_cidrs : try(cidrnetmask(cidr) != "" && !endswith(cidr, "/0"), false)])
    error_message = "Supply explicit approved IPv4 Runner CIDRs."
  }
}

resource "azurerm_network_security_group" "state_pe" {
  count               = length(var.state_runner_cidrs) > 0 ? 1 : 0
  name                = "nsg-state-pe"
  resource_group_name = azurerm_resource_group.bootstrap.name
  location            = azurerm_resource_group.bootstrap.location
  tags                = var.tags

  security_rule {
    name                       = "approved-blob-https"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefixes    = var.state_runner_cidrs
    destination_address_prefix = var.bootstrap_pe_subnet_cidr
  }

  security_rule {
    name                       = "deny-other-inbound"
    priority                   = 200
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = var.bootstrap_pe_subnet_cidr
  }
}

resource "azurerm_subnet_network_security_group_association" "state_pe" {
  count                     = length(var.state_runner_cidrs) > 0 ? 1 : 0
  subnet_id                 = azurerm_subnet.state_pe.id
  network_security_group_id = azurerm_network_security_group.state_pe[0].id
}
