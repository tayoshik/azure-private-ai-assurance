variable "private_link" {
  description = "Azure Monitor Private Link topology. Hub assets require owner approval."
  type = object({
    mode                = optional(string, "disabled")
    topology_approved   = optional(bool, false)
    hub_scope_id        = optional(string)
    hub_endpoint_id     = optional(string)
    hub_zone_ids        = optional(map(string), {})
    dev_subnet_cidr     = optional(string)
    dev_client_cidrs    = optional(list(string), [])
    dev_manual_approval = optional(bool, true)
    dev_isolated_dns    = optional(bool, false)
  })
  default  = {}
  nullable = false

  validation {
    condition = contains(["disabled", "hub", "dev"], var.private_link.mode) && (
      var.private_link.mode == "disabled" || var.private_link.topology_approved
    )
    error_message = "Choose disabled, hub, or dev, and approve the concrete topology before enabling Private Link."
  }

  validation {
    condition = var.private_link.mode == "hub" ? (
      can(regex("(?i)^/subscriptions/[0-9a-f-]{36}/resourceGroups/[^/]+/providers/Microsoft[.]Insights/privateLinkScopes/[^/]+$", var.private_link.hub_scope_id)) &&
      can(regex("(?i)^/subscriptions/[0-9a-f-]{36}/resourceGroups/[^/]+/providers/Microsoft[.]Network/privateEndpoints/[^/]+$", var.private_link.hub_endpoint_id)) &&
      toset(keys(var.private_link.hub_zone_ids)) == toset([
        "privatelink.monitor.azure.com",
        "privatelink.oms.opinsights.azure.com",
        "privatelink.ods.opinsights.azure.com",
        "privatelink.agentsvc.azure-automation.net",
        "privatelink.blob.core.windows.net",
      ]) &&
      alltrue([for name, id in var.private_link.hub_zone_ids :
        try(lower(split("/", id)[8]) == name, false) &&
        can(regex("(?i)^/subscriptions/[0-9a-f-]{36}/resourceGroups/[^/]+/providers/Microsoft[.]Network/privateDnsZones/[^/]+$", id))
      ])
      ) : (
      var.private_link.hub_scope_id == null && var.private_link.hub_endpoint_id == null &&
      length(var.private_link.hub_zone_ids) == 0
    )
    error_message = "Hub mode requires an existing AMPLS, PE and all five named Monitor Private DNS zone IDs. Other modes must omit Hub IDs."
  }

  validation {
    condition = var.private_link.mode == "dev" ? (
      var.private_link.dev_isolated_dns &&
      try(cidrnetmask(var.private_link.dev_subnet_cidr) != "" &&
      tonumber(split("/", var.private_link.dev_subnet_cidr)[1]) <= 27, false) &&
      length(var.private_link.dev_client_cidrs) > 0 &&
      alltrue([for cidr in var.private_link.dev_client_cidrs :
        try(cidrnetmask(cidr) != "" && !endswith(cidr, "/0"), false)
      ])
    ) : var.private_link.dev_subnet_cidr == null && length(var.private_link.dev_client_cidrs) == 0 && !var.private_link.dev_isolated_dns
    error_message = "Dev mode requires an approved IPv4 PE CIDR (/27 or larger), scoped client CIDRs and isolated DNS without a Monitor/Blob DNS collision."
  }
}

variable "workload_vnet_id" { type = string }
variable "subscription_id" { type = string }
