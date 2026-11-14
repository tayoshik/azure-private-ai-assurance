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
