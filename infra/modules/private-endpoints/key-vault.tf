# I03: Private Endpoint is on the existing data-PE subnet with NSG policy.
# Canonical hostname is {vault}.vault.azure.net, not a privatelink hostname.
resource "azurerm_private_endpoint" "key_vault" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id
  tags                = var.tags

  private_service_connection {
    name                           = "key-vault"
    private_connection_resource_id = var.key_vault_id
    subresource_names              = ["vault"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "key-vault-zone"
    private_dns_zone_ids = [var.key_vault_dns_zone_id]
  }

  lifecycle {
    precondition {
      condition     = var.key_vault_private_endpoint_approved
      error_message = "G07/I03: approved data-PE subnet, NSG, DNS, zone group and internal runner path are mandatory before plan."
    }
    precondition {
      condition     = endswith(lower(var.key_vault_dns_zone_id), "/privatelink.vaultcore.azure.net")
      error_message = "Key Vault must use the exact privatelink.vaultcore.azure.net Private DNS zone ID."
    }
  }
}
