# GW05: Application Gateway resource-specific logs; dedicated Log Analytics
# tables AGWAccessLogs / AGWFirewallLogs. Validate service categories on the
# pinned provider and approved workspace. No live log ingestion claim.
resource "azurerm_monitor_diagnostic_setting" "gateway" {
  name                           = "diag-${var.name}-gateway"
  target_resource_id             = azurerm_application_gateway.private_web.id
  log_analytics_workspace_id     = var.log_analytics_workspace_id
  log_analytics_destination_type = "Dedicated"

  enabled_log {
    category = "ApplicationGatewayAccessLog"
  }

  enabled_log {
    category = "ApplicationGatewayFirewallLog"
  }

  lifecycle {
    precondition {
      condition     = var.logging_route_approved
      error_message = "GW05: Log Analytics ingestion path, role, retention and alert ownership must be approved."
    }
  }
}
