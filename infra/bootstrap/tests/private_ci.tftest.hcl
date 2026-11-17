# Synthetic plan only; Terraform never connects to an Azure backend in this suite.
mock_provider "azurerm" {}

variables {
  subscription_id          = "01234567-89ab-4def-8123-0123456789ab"
  location                 = "eastus"
  resource_group_name      = "rg-synthetic"
  storage_account_name     = "syntheticstatestorage"
  bootstrap_vnet_name      = "synthetic-bootstrap"
  bootstrap_vnet_cidr      = "10.20.0.0/16"
  bootstrap_pe_subnet_cidr = "10.20.10.0/24"
}

run "private_storage_without_legacy_principal_by_default" {
  command = plan

  assert {
    condition     = !azurerm_storage_account.state.public_network_access_enabled && !azurerm_storage_account.state.shared_access_key_enabled && length(azurerm_role_assignment.ci_state_data) == 0
    error_message = "State must remain private and avoid the legacy grant for a new installation."
  }
}

run "split_identities_and_reuse_shared_zone" {
  command = plan

  variables {
    manage_ci_identities      = true
    state_runner_cidrs        = ["10.44.8.0/24"]
    existing_blob_dns_zone_id = "/subscriptions/01234567-89ab-4def-8123-0123456789ab/resourceGroups/synthetic-dns/providers/Microsoft.Network/privateDnsZones/privatelink.blob.core.windows.net"
  }

  assert {
    condition     = length(azurerm_private_dns_zone.blob) == 0 && length(azurerm_private_dns_zone_virtual_network_link.bootstrap) == 0 && length(azurerm_subnet_network_security_group_association.state_pe) == 1
    error_message = "Existing Hub DNS must not be duplicated; the configured Runner restriction must be present."
  }

  assert {
    condition     = length(azurerm_federated_identity_credential.ci) == 3 && azurerm_federated_identity_credential.ci["apply"].subject == "repo:tayoshik/azure-private-ai-assurance:environment:nonprod-apply"
    error_message = "Federation must distinguish all three mandatory environments."
  }

  assert {
    condition     = azurerm_role_assignment.ci_container["read"].role_definition_name == "Storage Blob Data Reader" && azurerm_role_assignment.ci_container["plan"].role_definition_name == "Storage Blob Data Contributor"
    error_message = "Read may not receive write privileges; plan needs its own state lease grant."
  }
}

run "reject_split_identities_without_approved_runner_cidrs" {
  command = plan

  variables {
    manage_ci_identities = true
  }

  expect_failures = [azurerm_user_assigned_identity.ci]
}
