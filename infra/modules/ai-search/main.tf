# A03: Search query identity uses RBAC, never API keys.
resource "azurerm_search_service" "search" {
  name                          = var.name
  resource_group_name           = var.resource_group_name
  location                      = var.location
  sku                           = var.sku
  replica_count                 = var.replica_count
  partition_count               = var.partition_count
  public_network_access_enabled = false
  local_authentication_enabled  = false
  network_rule_bypass_option    = "None"
  tags                          = var.tags

  lifecycle {
    precondition {
      condition = var.search_approved && var.region_and_sku_approved
      error_message = "A03/G03/G07: approved Search SKU, region, PE capability and budget are required."
    }
    precondition {
      condition = var.sku != "free" && var.replica_count >= 1 && var.partition_count >= 1
      error_message = "A03: private-capable SKU and positive capacity required."
    }
  }
}
