output "id" { value = azurerm_application_gateway.private_web.id }
output "private_frontend_ip" { value = var.private_frontend_ip }
output "waf_policy_id" { value = azurerm_web_application_firewall_policy.private_web.id }
output "diagnostic_setting_id" { value = azurerm_monitor_diagnostic_setting.gateway.id }
output "business_fqdn" { value = var.business_fqdn }
output "backend_app_fqdn" { value = var.backend_app_fqdn }
