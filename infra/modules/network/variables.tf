variable "name" {
  type = string
}
variable "resource_group_name" {
  type = string
}
variable "location" {
  type = string
}
variable "vnet_cidr" {
  type = string
  validation {
    condition     = can(cidrhost(var.vnet_cidr, 0))
    error_message = "Enter an approved VNet CIDR."
  }
}
variable "subnet_cidrs" {
  type = object({
    app_gateway          = string
    app_outbound         = string
    web_private_endpoint = string
    data_private_endpoint = string
  })
  # All subnet ranges must be approved and confirmed non-overlapping by IPAM.
}
variable "tags" {
  type = map(string)
}

# N04 policy contract. Defaults intentionally block network association via
# Terraform preconditions until approved environment-specific dependencies.
variable "approved_client_cidrs" {
  type        = list(string)
  description = "Explicit signed corporate/VPN address ranges allowed to private gateway port 443."
  validation {
    condition     = length(var.approved_client_cidrs) > 0 && length(var.approved_client_cidrs) == length(distinct(var.approved_client_cidrs)) && alltrue([for c in var.approved_client_cidrs : can(cidrhost(c, 0)) && c != "0.0.0.0/0"])
    error_message = "Provide distinct reviewed CIDRs; unrestricted 0.0.0.0/0 is forbidden."
  }
}

variable "approved_test_runner_cidrs" {
  type        = list(string)
  description = "Private runner source CIDRs, when tests/SCM access actually requires them."
  default     = []
  validation {
    condition     = alltrue([for c in var.approved_test_runner_cidrs : can(cidrhost(c, 0)) && c != "0.0.0.0/0"])
    error_message = "Approved test runner sources must be scoped CIDRs."
  }
}

variable "approved_dns_resolver_ips" {
  type        = list(string)
  description = "Approved DNS resolver IPv4 addresses; platform DNS behavior must be separately reviewed."
  default     = []
  validation {
    condition     = length(var.approved_dns_resolver_ips) == length(distinct(var.approved_dns_resolver_ips)) && alltrue([for ip in var.approved_dns_resolver_ips : can(cidrhost("${ip}/32", 0))])
    error_message = "Provide distinct approved resolver IPv4 addresses."
  }
}

variable "gateway_extra_egress_rules" {
  type = map(object({
    destination_cidr = string
    destination_port = number
    priority         = number
  }))
  default     = {}
  description = "Reviewed gateway egress exceptions; use IP destinations only, NOT FQDN. Include Key Vault/CRL or route via approved firewall where required."
  validation {
    condition = alltrue([for k,v in var.gateway_extra_egress_rules :
      can(regex("^[A-Za-z0-9]{1,45}$", k)) && can(cidrhost(v.destination_cidr, 0)) && v.destination_cidr != "0.0.0.0/0" && v.destination_port >= 1 && v.destination_port <= 65535 && v.priority >= 300 && v.priority <= 999
    ]) && length(distinct([for v in values(var.gateway_extra_egress_rules) : v.priority])) == length(var.gateway_extra_egress_rules)
    error_message = "Gateway exceptions require distinct priorities 300-999, scoped CIDRs, ports and valid names."
  }
}

variable "app_extra_egress_rules" {
  type = map(object({
    destination_cidr = string
    destination_port = number
    priority         = number
  }))
  default     = {}
  description = "Approved App Service egress; identity, CRL, artifact supply, monitoring and runtime dependencies MUST be covered."
  validation {
    condition = alltrue([for k,v in var.app_extra_egress_rules :
      can(regex("^[A-Za-z0-9]{1,45}$", k)) && can(cidrhost(v.destination_cidr, 0)) && v.destination_cidr != "0.0.0.0/0" && v.destination_port >= 1 && v.destination_port <= 65535 && v.priority >= 300 && v.priority <= 999
    ]) && length(distinct([for v in values(var.app_extra_egress_rules) : v.priority])) == length(var.app_extra_egress_rules)
    error_message = "App exceptions require distinct priorities 300-999, scoped CIDRs, ports and valid names."
  }
}

variable "gateway_network_isolation_approved" {
  type        = bool
  default     = false
  description = "Set TRUE only after portal approval of actual private Application Gateway Network Isolation feature and supported mode."
}
variable "gateway_egress_profile_approved" {
  type        = bool
  default     = false
  description = "Set TRUE only after independent review of Gateway backend, Key Vault, certificate revocation, DNS and management dependencies."
}
variable "app_egress_profile_approved" {
  type        = bool
  default     = false
  description = "Set TRUE only after independent review of App Service runtime, deployment, identity, monitoring, DNS and certificate egress dependencies."
}
variable "network_policy_approved" {
  type        = bool
  default     = false
  description = "G07 security approval required before any NSG subnet association."
}
variable "enable_app_forced_tunnel" {
  type        = bool
  default     = false
  description = "Optional outbound App Integration 0/0 route via approved firewall, never a Gateway subnet route."
}
variable "approved_firewall_next_hop_ip" {
  type        = string
  default     = null
  nullable    = true
  description = "Validated private IP of approved Azure Firewall/NVA, if forced tunnel is enabled."
  validation {
    condition     = var.approved_firewall_next_hop_ip == null ? true : can(cidrhost("${var.approved_firewall_next_hop_ip}/32", 0))
    error_message = "Supply an approved IPv4 next-hop address or null."
  }
}
