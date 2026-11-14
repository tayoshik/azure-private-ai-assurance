variable "name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "subnet_id" { type = string }
variable "key_vault_id" { type = string }
variable "key_vault_dns_zone_id" { type = string }
variable "tags" { type = map(string) }
variable "key_vault_private_endpoint_approved" {
  type    = bool
  default = false
}
