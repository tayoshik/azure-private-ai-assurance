output "app_identity_id" { value = azurerm_user_assigned_identity.app.id }
output "app_client_id" { value = azurerm_user_assigned_identity.app.client_id }
output "app_principal_id" { value = azurerm_user_assigned_identity.app.principal_id }
output "gateway_identity_id" { value = azurerm_user_assigned_identity.gateway.id }
output "gateway_client_id" { value = azurerm_user_assigned_identity.gateway.client_id }
output "gateway_principal_id" { value = azurerm_user_assigned_identity.gateway.principal_id }
