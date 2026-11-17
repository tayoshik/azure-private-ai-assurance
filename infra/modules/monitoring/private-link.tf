locals {
  private_link = var.private_link
  create_ampls = local.private_link.mode == "dev"
  share_ampls  = local.private_link.mode == "hub"

  monitor_zone_names = toset([
    "privatelink.monitor.azure.com",
    "privatelink.oms.opinsights.azure.com",
    "privatelink.ods.opinsights.azure.com",
    "privatelink.agentsvc.azure-automation.net",
    "privatelink.blob.core.windows.net",
  ])
  monitor_zone_ids = local.share_ampls ? local.private_link.hub_zone_ids : {
    for name, zone in azurerm_private_dns_zone.monitor : name => zone.id
  }
  scope_name           = local.share_ampls ? try(split("/", local.private_link.hub_scope_id)[8], null) : one(azurerm_monitor_private_link_scope.monitor[*].name)
  scope_resource_group = local.share_ampls ? try(split("/", local.private_link.hub_scope_id)[4], null) : var.resource_group_name
}

resource "azurerm_monitor_private_link_scope" "monitor" {
  count                 = local.create_ampls ? 1 : 0
  name                  = "${var.name}-ampls"
  resource_group_name   = var.resource_group_name
  ingestion_access_mode = "PrivateOnly"
  query_access_mode     = "PrivateOnly"
  tags                  = var.tags
}

resource "azurerm_monitor_private_link_scoped_service" "workspace" {
  count               = local.private_link.mode == "disabled" ? 0 : 1
  name                = var.name
  scope_name          = local.scope_name
  resource_group_name = local.scope_resource_group
  linked_resource_id  = azurerm_log_analytics_workspace.audit.id

  lifecycle {
    precondition {
      condition     = !local.share_ampls || try(lower(split("/", local.private_link.hub_scope_id)[2]) == lower(var.subscription_id), false)
      error_message = "The hub scope must be in the provider subscription; cross-subscription associations must be owned by a separate stack."
    }
  }
}

resource "azurerm_private_dns_zone" "monitor" {
  for_each            = local.create_ampls ? local.monitor_zone_names : toset([])
  name                = each.key
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "monitor" {
  for_each              = azurerm_private_dns_zone.monitor
  name                  = "monitor-workload"
  private_dns_zone_name = each.value.name
  resource_group_name   = var.resource_group_name
  virtual_network_id    = var.workload_vnet_id
  registration_enabled  = false
  tags                  = var.tags
}

resource "azurerm_subnet" "monitor" {
  count                             = local.create_ampls ? 1 : 0
  name                              = "snet-monitor-pe"
  resource_group_name               = var.resource_group_name
  virtual_network_name              = split("/", var.workload_vnet_id)[8]
  address_prefixes                  = [local.private_link.dev_subnet_cidr]
  private_endpoint_network_policies = "Enabled"
}

resource "azurerm_network_security_group" "monitor" {
  count               = local.create_ampls ? 1 : 0
  name                = "${var.name}-ampls-pe-nsg"
  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = var.tags

  security_rule {
    name                       = "approved-monitor-https"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefixes    = local.private_link.dev_client_cidrs
    destination_address_prefix = local.private_link.dev_subnet_cidr
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
    destination_address_prefix = local.private_link.dev_subnet_cidr
  }
}

resource "azurerm_subnet_network_security_group_association" "monitor" {
  count                     = local.create_ampls ? 1 : 0
  subnet_id                 = azurerm_subnet.monitor[0].id
  network_security_group_id = azurerm_network_security_group.monitor[0].id
}

resource "azurerm_private_endpoint" "monitor" {
  count               = local.create_ampls ? 1 : 0
  name                = "${var.name}-ampls-pe"
  resource_group_name = var.resource_group_name
  location            = var.location
  subnet_id           = azurerm_subnet.monitor[0].id
  tags                = var.tags

  private_service_connection {
    name                           = "azure-monitor"
    private_connection_resource_id = azurerm_monitor_private_link_scope.monitor[0].id
    subresource_names              = ["azuremonitor"]
    is_manual_connection           = local.private_link.dev_manual_approval
    request_message                = local.private_link.dev_manual_approval ? "Approve Azure Monitor Private Link for the workload." : null
  }

  depends_on = [azurerm_subnet_network_security_group_association.monitor]

  private_dns_zone_group {
    name                 = "azure-monitor"
    private_dns_zone_ids = values(local.monitor_zone_ids)
  }
}
