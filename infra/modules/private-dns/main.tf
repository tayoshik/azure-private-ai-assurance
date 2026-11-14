# N05: shared zones and VNet links. These links alone do not resolve
# on-prem client DNS or establish endpoints. PE zone groups come later.
resource "azurerm_private_dns_zone" "service" {
  for_each            = toset(var.zone_names)
  name                = each.value
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "workload" {
  for_each              = azurerm_private_dns_zone.service
  name                  = "link-workload-${replace(each.key, ".", "-")}"
  resource_group_name   = var.resource_group_name
  private_dns_zone_name = each.value.name
  virtual_network_id    = var.virtual_network_id
  registration_enabled  = false
  tags                  = var.tags
}
