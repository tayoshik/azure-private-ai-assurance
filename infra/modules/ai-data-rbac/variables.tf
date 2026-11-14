variable "resource_group_name" { type = string }
variable "openai_account_id" { type = string }
variable "search_service_id" { type = string }
variable "cosmos_account_id" { type = string }
variable "cosmos_account_name" { type = string }
variable "cosmos_database_name" { type = string }
variable "cosmos_container_name" { type = string }
variable "app_principal_id" { type = string }
variable "rbac_approved" {
  type    = bool
  default = false
}
variable "cosmos_write_approved" {
  type    = bool
  default = false
}
variable "cosmos_write_justification_approved" {
  type    = bool
  default = false
}
