output "vnet_id" {
  value = azurerm_virtual_network.workload.id
}
output "app_gateway_subnet_id" {
  value = azurerm_subnet.app_gateway.id
}
output "app_outbound_subnet_id" {
  value = azurerm_subnet.app_outbound.id
}
output "web_private_endpoint_subnet_id" {
  value = azurerm_subnet.web_private_endpoint.id
}
output "data_private_endpoint_subnet_id" {
  value = azurerm_subnet.data_private_endpoint.id
}
