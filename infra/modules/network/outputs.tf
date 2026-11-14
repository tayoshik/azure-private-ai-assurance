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

output "network_security_group_ids" {
  description = "Scoped NSG IDs for configuration/evidence review."
  value = {
    app_gateway  = azurerm_network_security_group.app_gateway.id
    app_outbound = azurerm_network_security_group.app_outbound.id
    web_pe       = azurerm_network_security_group.web_pe.id
    data_pe      = azurerm_network_security_group.data_pe.id
  }
}
output "app_outbound_route_table_id" {
  description = "Null unless approved forced tunnel is enabled."
  value       = var.enable_app_forced_tunnel ? azurerm_route_table.app_outbound[0].id : null
}
