output "openai_private_endpoint_id" { value = azurerm_private_endpoint.openai.id }
output "search_private_endpoint_id" { value = azurerm_private_endpoint.search.id }
output "cosmos_private_endpoint_id" { value = azurerm_private_endpoint.cosmos.id }
output "openai_private_ip" { value = azurerm_private_endpoint.openai.private_service_connection[0].private_ip_address }
output "search_private_ip" { value = azurerm_private_endpoint.search.private_service_connection[0].private_ip_address }
output "cosmos_private_ip" { value = azurerm_private_endpoint.cosmos.private_service_connection[0].private_ip_address }
