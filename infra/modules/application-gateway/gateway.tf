# GW02–GW04: private-only WAF_v2. No public_ip_address_id, no public frontend,
# no PFX data/password, no TLS certificate import into Terraform state.
# Key Vault secret must already exist and must be reachable from the gateway.
resource "azurerm_application_gateway" "private_web" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
  enable_http2        = true
  firewall_policy_id  = azurerm_web_application_firewall_policy.private_web.id

  sku {
    name     = "WAF_v2"
    tier     = "WAF_v2"
    capacity = var.gateway_capacity
  }

  gateway_ip_configuration {
    name      = "gateway-ipcfg"
    subnet_id = var.gateway_subnet_id
  }

  frontend_ip_configuration {
    name                          = local.private_frontend_name
    private_ip_address            = var.private_frontend_ip
    private_ip_address_allocation = "Static"
    subnet_id                     = var.gateway_subnet_id
  }

  frontend_port {
    name = local.frontend_https_port_name
    port = 443
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [var.gateway_identity_id]
  }

  ssl_certificate {
    name                = local.tls_certificate_name
    key_vault_secret_id = var.key_vault_certificate_secret_versionless_id
  }

  backend_address_pool {
    name  = local.web_backend_pool_name
    fqdns = [var.backend_app_fqdn]
  }

  backend_http_settings {
    name                  = local.backend_https_name
    port                  = 443
    protocol              = "Https"
    cookie_based_affinity = "Disabled"
    request_timeout       = 30
    host_name             = var.backend_app_fqdn
    probe_name            = local.web_health_probe_name
  }

  probe {
    name                                      = local.web_health_probe_name
    protocol                                  = "Https"
    path                                      = var.health_check_path
    host                                      = var.backend_app_fqdn
    interval                                  = 30
    timeout                                   = 30
    unhealthy_threshold                       = 3
    pick_host_name_from_backend_http_settings = false
    match {
      status_code = ["200-399"]
    }
  }

  http_listener {
    name                           = local.https_listener_name
    frontend_ip_configuration_name = local.private_frontend_name
    frontend_port_name             = local.frontend_https_port_name
    protocol                       = "Https"
    host_name                      = var.business_fqdn
    ssl_certificate_name           = local.tls_certificate_name
  }

  request_routing_rule {
    name                       = local.https_route_name
    rule_type                  = "Basic"
    priority                   = 100
    http_listener_name         = local.https_listener_name
    backend_address_pool_name  = local.web_backend_pool_name
    backend_http_settings_name = local.backend_https_name
  }

  lifecycle {
    prevent_destroy = true
    precondition {
      condition = var.private_gateway_feature_approved && var.gateway_ipam_and_routes_approved
      error_message = "GW03/G07: Private Gateway feature, delegated subnet, IPAM and approved egress/NSG must be verified."
    }
    precondition {
      condition = var.backend_dns_tls_approved && var.certificate_import_and_rbac_approved
      error_message = "GW02/GW04: Key Vault certificate, TLS host/probe/DNS and identity access require prior independent review."
    }
    precondition {
      condition = trimspace(var.business_fqdn) != "" && var.business_fqdn != var.backend_app_fqdn
      error_message = "Private business listener FQDN and App Service backend FQDN must be independently configured."
    }
    precondition {
      condition = can(cidrhost("${var.private_frontend_ip}/32", 0))
      error_message = "Private frontend address must be valid IPv4 and match signed IPAM."
    }
  }
}
