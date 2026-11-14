output "private_endpoint_id" { value = azurerm_private_endpoint.web_app.id }
output "private_endpoint_name" { value = azurerm_private_endpoint.web_app.name }
output "private_ip" { value = azurerm_private_endpoint.web_app.private_service_connection[0].private_ip_address }
