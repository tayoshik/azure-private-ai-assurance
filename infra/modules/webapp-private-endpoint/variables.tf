variable "private_endpoint_name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "web_inbound_pe_subnet_id" { type = string }
variable "app_outbound_subnet_id" { type = string }
variable "web_app_id" { type = string }
variable "webapp_private_dns_zone_id" { type = string }
variable "tags" { type = map(string) }
variable "web_private_endpoint_approved" {
  type    = bool
  default = false
}
variable "private_dns_and_scm_approved" {
  type    = bool
  default = false
}
