variable "monitoring_private_link" {
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

}
