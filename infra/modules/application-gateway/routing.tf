# GW04: azurerm_application_gateway requires all listener, probe, backend and
# rule nested blocks within ONE azurerm_application_gateway resource. The
# names below are referenced by gateway.tf rather than splitting the same
# resource across multiple Terraform files.
locals {
  private_frontend_name    = "frontend-private"
  frontend_https_port_name = "https-443"
  tls_certificate_name     = "cert-approved-vault"
  https_listener_name      = "listener-private-https"
  web_backend_pool_name    = "pool-webapp-private-endpoint"
  backend_https_name       = "setting-webapp-https"
  web_health_probe_name    = "probe-webapp-https"
  https_route_name         = "route-webapp-https"
}
