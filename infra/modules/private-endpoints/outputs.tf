output "key_vault_private_endpoint_id" { value = azurerm_private_endpoint.key_vault.id }
output "key_vault_private_endpoint_name" { value = azurerm_private_endpoint.key_vault.name }
output "key_vault_private_endpoint_private_ip" { value = azurerm_private_endpoint.key_vault.private_service_connection[0].private_ip_address }
