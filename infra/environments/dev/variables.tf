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
