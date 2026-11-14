output "service_plan_id" { value = azurerm_service_plan.app.id }
output "web_app_id" { value = azurerm_linux_web_app.app.id }
output "web_app_name" { value = azurerm_linux_web_app.app.name }
output "default_hostname" { value = azurerm_linux_web_app.app.default_hostname }
output "outbound_integration_subnet_id" { value = azurerm_linux_web_app.app.virtual_network_subnet_id }
