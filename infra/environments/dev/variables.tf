variable "subscription_id" {
  type        = string
  description = "Approved target subscription; supply via restricted CI variables."
  validation {
    condition     = can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", var.subscription_id)) && lower(var.subscription_id) != "00000000-0000-0000-0000-000000000000"
    error_message = "An approved non-placeholder subscription UUID is required."
  }
}
variable "location" {
  type = string
}
variable "resource_group_name" {
  type = string
}
variable "vnet_name" {
  type = string
}
variable "vnet_cidr" {
  type = string
}
variable "subnet_cidrs" {
  type = object({
    app_gateway           = string
    app_outbound          = string
    web_private_endpoint  = string
    data_private_endpoint = string
  })
}
variable "private_dns_zone_names" {
  type    = list(string)
  default = [
    "privatelink.azurewebsites.net",
    "privatelink.openai.azure.com",
    "privatelink.search.windows.net",
    "privatelink.documents.azure.com",
    "privatelink.vaultcore.azure.net"
  ]
}
variable "common_tags" {
  type = map(string)
  default = {
    workload     = "azure-private-ai-assurance"
    sensitivity  = "restricted"
  }
}

# The dev root never approves network controls implicitly.
variable "approved_client_cidrs" {
  type        = list(string)
  description = "Signed client IPAM; no default."
}
variable "approved_dns_resolver_ips" {
  type        = list(string)
  default     = []
}
variable "approved_test_runner_cidrs" {
  type        = list(string)
  default     = []
}
variable "gateway_extra_egress_rules" {
  type = map(object({
    destination_cidr = string
    destination_port = number
    priority         = number
  }))
  default = {}
}
variable "app_extra_egress_rules" {
  type = map(object({
    destination_cidr = string
    destination_port = number
    priority         = number
  }))
  default = {}
}
variable "network_policy_approved" {
  type    = bool
  default = false
}
variable "gateway_network_isolation_approved" {
  type    = bool
  default = false
}
variable "gateway_egress_profile_approved" {
  type    = bool
  default = false
}
variable "app_egress_profile_approved" {
  type    = bool
  default = false
}
variable "enable_app_forced_tunnel" {
  type    = bool
  default = false
}
variable "approved_firewall_next_hop_ip" {
  type     = string
  default  = null
  nullable = true
}
