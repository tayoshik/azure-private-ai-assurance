output "bootstrap_resource_group_name" {
  value = azurerm_resource_group.bootstrap.name
}

output "state_storage_account_name" {
  value = azurerm_storage_account.state.name
}

output "state_container_name" {
  value = azurerm_storage_container.state.name
}

output "state_container_arm_id" {
  value = azurerm_storage_container.state.resource_manager_id
}

output "bootstrap_vnet_id" {
  value = azurerm_virtual_network.bootstrap.id
}

output "state_private_endpoint_id" {
  value = azurerm_private_endpoint.state_blob.id
}

output "state_blob_fqdn" {
  value = "${azurerm_storage_account.state.name}.blob.core.windows.net"
}
