# W04: inbound sites Private Endpoint; zone group handles App + SCM records.
resource "azurerm_private_endpoint" "web_app" {
  name                = var.private_endpoint_name
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.web_inbound_pe_subnet_id
  tags                = var.tags
  private_service_connection {
    name                           = "psc-${var.private_endpoint_name}"
    private_connection_resource_id = var.web_app_id
    subresource_names              = ["sites"]
    is_manual_connection           = false
  }
  private_dns_zone_group {
    name                 = "zone-group-webapp"
    private_dns_zone_ids = [var.webapp_private_dns_zone_id]
  }
  lifecycle {
    precondition {
      condition     = var.web_private_endpoint_approved && var.private_dns_and_scm_approved
      error_message = "W04/G07: inbound PE, DNS, SCM and runner approvals required."
    }
    precondition {
      condition     = var.web_inbound_pe_subnet_id != var.app_outbound_subnet_id
      error_message = "W04: inbound PE must not share the outbound integration subnet."
    }
    precondition {
      condition     = endswith(lower(var.webapp_private_dns_zone_id), "/privatelink.azurewebsites.net")
      error_message = "W04: Web App PE requires the exact privatelink.azurewebsites.net zone ID."
    }
  }
}
