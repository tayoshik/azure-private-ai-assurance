output "workspace_id" { value = azurerm_log_analytics_workspace.audit.id }
output "workspace_name" { value = azurerm_log_analytics_workspace.audit.name }

output "private_link" {
  description = "Selected Monitor Private Link resources for operator-side assurance."
  value = {
    mode                = local.private_link.mode
    scope_id            = local.share_ampls ? local.private_link.hub_scope_id : one(azurerm_monitor_private_link_scope.monitor[*].id)
    scoped_workspace_id = one(azurerm_monitor_private_link_scoped_service.workspace[*].id)
    endpoint_id         = local.share_ampls ? local.private_link.hub_endpoint_id : one(azurerm_private_endpoint.monitor[*].id)
    dev_subnet_id       = one(azurerm_subnet.monitor[*].id)
    dns_zone_ids        = local.monitor_zone_ids
  }
}
