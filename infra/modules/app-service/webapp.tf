# W02/W03/W05 - Hardened Linux Web App using a *single* outbound VNet method.
# W04 (inbound PE) is a separate module/subnet and does not depend on this setting.
resource "azurerm_linux_web_app" "app" {
  name                                           = var.web_app_name
  resource_group_name                            = var.resource_group_name
  location                                       = var.location
  service_plan_id                                = azurerm_service_plan.app.id
  https_only                                     = true
  public_network_access_enabled                  = false
  ftp_publish_basic_authentication_enabled       = false
  webdeploy_publish_basic_authentication_enabled = false
  virtual_network_subnet_id                      = local.approved_outbound_integration_subnet_id
  key_vault_reference_identity_id                = var.app_identity_id
  app_settings                                   = local.app_settings
  tags                                           = var.tags

  identity {
    type         = "UserAssigned"
    identity_ids = [var.app_identity_id]
  }

  site_config {
    always_on                           = true
    http2_enabled                       = true
    ftps_state                          = "Disabled"
    minimum_tls_version                 = "1.2"
    scm_minimum_tls_version             = "1.2"
    vnet_route_all_enabled              = true
    health_check_path                   = var.health_check_path
    ip_restriction_default_action       = "Deny"
    scm_ip_restriction_default_action   = "Deny"

    application_stack {
      python_version = var.python_version
    }
  }

  lifecycle {
    precondition {
      condition     = var.web_app_configuration_approved && var.outbound_integration_approved
      error_message = "W02/W03/G07: reviewed runtime, identity, outbound routes, egress dependencies and approved plan required."
    }
    precondition {
      condition     = var.application_contract_approved
      error_message = "W05: application source, dependency endpoint and environment-variable contract must be reviewed first."
    }
    precondition {
      condition     = var.app_outbound_subnet_id != var.web_inbound_pe_subnet_id
      error_message = "W03/W04: inbound PE and outbound integration must use separate subnets."
    }
    precondition {
      condition     = startswith(var.health_check_path, "/") && !strcontains(var.health_check_path, "?")
      error_message = "W02: require an approved stable health path without a query string."
    }
  }
}
