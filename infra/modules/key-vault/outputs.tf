output "id" { value = azurerm_key_vault.workload.id }
output "vault_uri" { value = azurerm_key_vault.workload.vault_uri }
output "name" { value = azurerm_key_vault.workload.name }
output "app_reader_role_assignment_id" {
  value = try(azurerm_role_assignment.app_secrets_reader[0].id, null)
}
output "gateway_reader_role_assignment_id" {
  value = try(azurerm_role_assignment.gateway_certificate_reader[0].id, null)
}
