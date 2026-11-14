# W03: one VNet integration owner, via the webapp's inline attribute.
# Never also add azurerm_app_service_virtual_network_swift_connection.
locals {
  approved_outbound_integration_subnet_id = var.app_outbound_subnet_id
}
