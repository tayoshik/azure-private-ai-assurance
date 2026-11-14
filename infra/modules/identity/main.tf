# I01: Two isolated user-assigned identities. No passwords or client secrets.
resource "azurerm_user_assigned_identity" "app" {
  name                = var.app_identity_name
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_user_assigned_identity" "gateway" {
  name                = var.gateway_identity_name
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}
