variable "name" { type = string }
variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tags" { type = map(string) }
variable "gateway_subnet_id" { type = string }
variable "gateway_subnet_cidr" { type = string }
variable "private_frontend_ip" {
  type = string
  validation {
    condition = can(cidrhost("${var.private_frontend_ip}/32", 0))
    error_message = "Gateway frontend must be an IPv4 address. It must also match approved subnet IPAM."
  }
}
variable "gateway_identity_id" { type = string }
variable "key_vault_certificate_secret_versionless_id" {
  type = string
  description = "Existing, separately approved Key Vault secret versionless ID. NEVER embed certificate bytes or an access token."
  validation {
    condition = can(regex("^https://[a-zA-Z0-9-]+\\.vault\\.azure\\.net/secrets/[a-zA-Z0-9-]+$", var.key_vault_certificate_secret_versionless_id))
    error_message = "Use a versionless HTTPS Key Vault secret ID; no certificate material or version segment."
  }
}
variable "business_fqdn" { type = string }
variable "backend_app_fqdn" {
  type = string
  validation {
    condition = endswith(var.backend_app_fqdn, ".azurewebsites.net") && !startswith(var.backend_app_fqdn, "https://")
    error_message = "Backend must be the canonical default App Service hostname, without a scheme."
  }
}
variable "health_check_path" {
  type = string
  default = "/healthz"
  validation {
    condition = startswith(var.health_check_path, "/") && !strcontains(var.health_check_path, "?")
    error_message = "A stable absolute health path without query string is required."
  }
}
variable "gateway_capacity" {
  type = number
  default = 2
  validation {
    condition = var.gateway_capacity >= 2 && var.gateway_capacity <= 10 && floor(var.gateway_capacity) == var.gateway_capacity
    error_message = "Use approved WAF_v2 fixed capacity of 2–10 instances for this baseline."
  }
}
variable "waf_mode" {
  type = string
  default = "Detection"
  validation {
    condition = contains(["Detection", "Prevention"], var.waf_mode)
    error_message = "WAF mode must be Detection or Prevention."
  }
}
variable "waf_drs_version" {
  type = string
  default = "2.2"
  validation {
    condition = var.waf_drs_version == "2.2"
    error_message = "DRS2.2 is the target; confirm SKU/region/API availability before plan."
  }
}
variable "private_gateway_feature_approved" {
  type = bool
  default = false
}
variable "gateway_ipam_and_routes_approved" {
  type = bool
  default = false
}
variable "backend_dns_tls_approved" {
  type = bool
  default = false
}
variable "certificate_import_and_rbac_approved" {
  type = bool
  default = false
}
variable "waf_policy_approved" {
  type = bool
  default = false
}
variable "waf_prevention_approved" {
  type = bool
  default = false
}
variable "log_analytics_workspace_id" { type = string }
variable "logging_route_approved" {
  type = bool
  default = false
}
