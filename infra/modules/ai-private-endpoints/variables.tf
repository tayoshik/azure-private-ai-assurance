variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tags" { type = map(string) }
variable "subnet_id" { type = string }
variable "openai_pe_name" { type = string }
variable "search_pe_name" { type = string }
variable "cosmos_pe_name" { type = string }
variable "openai_account_id" { type = string }
variable "search_service_id" { type = string }
variable "cosmos_account_id" { type = string }
variable "openai_zone_id" { type = string }
variable "search_zone_id" { type = string }
variable "cosmos_zone_id" { type = string }
variable "private_endpoints_approved" {
  type    = bool
  default = false
}
