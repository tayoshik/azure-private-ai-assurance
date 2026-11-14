# I02: Private-only Key Vault with immutable protection and RBAC.
# No azurerm_key_vault_secret, certificate private keys, or plaintext values
# are stored in Terraform state; import and rotate secrets out of band.
resource "azurerm_key_vault" "workload" {
  name                          = var.name
  location                      = var.location
  resource_group_name           = var.resource_group_name
  tenant_id                     = var.tenant_id
  sku_name                      = "standard"
  rbac_authorization_enabled    = true
  public_network_access_enabled = false
  purge_protection_enabled      = true
  soft_delete_retention_days    = 90
  tags                          = var.tags

  network_acls {
    default_action = "Deny"
    bypass         = "None"
  }

  lifecycle {
    prevent_destroy = true
    precondition {
      condition     = var.key_vault_configuration_approved
      error_message = "G07/I02: signed Key Vault name, retention, tenant, network and operations approval is required before an Azure plan."
    }
  }
}

# I02: Bound only to the vault and a read-only data-plane role.
# No generic Contributor/Owner role and no data-plane administrator grant.
resource "azurerm_role_assignment" "app_secrets_reader" {
  count                = var.app_secrets_reader_approved ? 1 : 0
  scope                = azurerm_key_vault.workload.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = var.app_principal_id
  lifecycle {
    precondition {
      condition     = var.role_assignment_approval_confirmed
      error_message = "An approved role-assignment ticket is mandatory before provisioning App Service secret read access."
    }
  }
}

resource "azurerm_role_assignment" "gateway_certificate_reader" {
  count                = var.gateway_certificate_reader_approved ? 1 : 0
  scope                = azurerm_key_vault.workload.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = var.gateway_principal_id
  lifecycle {
    precondition {
      condition     = var.role_assignment_approval_confirmed
      error_message = "An approved role-assignment ticket is mandatory before provisioning Gateway certificate secret read access."
    }
  }
}
