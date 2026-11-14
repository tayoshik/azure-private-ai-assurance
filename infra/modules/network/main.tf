# N02/N03: VNet, Gateway-only subnet, App Service outbound subnet,
# and distinct inbound/data PE subnets. These resources do not themselves
# prove any user traffic path or implement the N04 NSG/UDR controls.
resource "azurerm_virtual_network" "workload" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  address_space       = [var.vnet_cidr]
  tags                = var.tags
}

resource "azurerm_subnet" "app_gateway" {
  name                 = "snet-appgw"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.workload.name
  address_prefixes     = [var.subnet_cidrs.app_gateway]

  # Private App Gateway requires compatible feature and deployment mode.
  # This must be independently checked in target subscription (G03/G07).
  delegation {
    name = "appgw-delegation"
    service_delegation {
      name = "Microsoft.Network/applicationGateways"
    }
  }
}

resource "azurerm_subnet" "app_outbound" {
  name                 = "snet-appsvc-outbound"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.workload.name
  address_prefixes     = [var.subnet_cidrs.app_outbound]

  delegation {
    name = "appsvc-delegation"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "web_private_endpoint" {
  name                              = "snet-web-pe"
  resource_group_name               = var.resource_group_name
  virtual_network_name              = azurerm_virtual_network.workload.name
  address_prefixes                  = [var.subnet_cidrs.web_private_endpoint]
  private_endpoint_network_policies = "Enabled"
}

resource "azurerm_subnet" "data_private_endpoint" {
  name                              = "snet-data-pe"
  resource_group_name               = var.resource_group_name
  virtual_network_name              = azurerm_virtual_network.workload.name
  address_prefixes                  = [var.subnet_cidrs.data_private_endpoint]
  private_endpoint_network_policies = "Enabled"
}
