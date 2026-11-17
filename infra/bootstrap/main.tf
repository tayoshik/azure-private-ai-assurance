# B01/B02: Separate bootstrap lifecycle. DO NOT configure this root to use its
# own Azure Blob backend: that creates a first-run state dependency.
resource "azurerm_resource_group" "bootstrap" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_storage_account" "state" {
  name                            = var.storage_account_name
  resource_group_name             = azurerm_resource_group.bootstrap.name
  location                        = azurerm_resource_group.bootstrap.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS" # Change only after approved DR/RPO review.
  account_kind                    = "StorageV2"
  https_traffic_only_enabled      = true
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = false
  public_network_access_enabled   = false
  default_to_oauth_authentication = true
  tags                            = var.tags

  blob_properties {
    versioning_enabled = true
    delete_retention_policy {
      days = var.blob_retention_days
    }
    container_delete_retention_policy {
      days = var.blob_retention_days
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}

# In pinned AzureRM 4.66, storage_account_id uses ARM for container creation.
# It does NOT prove Blob data-plane connectivity from the CI runner.
resource "azurerm_storage_container" "state" {
  name                  = var.state_container_name
  storage_account_id    = azurerm_storage_account.state.id
  container_access_type = "private"

  lifecycle {
    prevent_destroy = true
  }
}

moved {
  from = azurerm_role_assignment.ci_state_data
  to   = azurerm_role_assignment.ci_state_data[0]
}

resource "azurerm_role_assignment" "ci_state_data" {
  count                = var.ci_principal_object_id == null ? 0 : 1
  scope                = azurerm_storage_container.state.resource_manager_id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = var.ci_principal_object_id
}
