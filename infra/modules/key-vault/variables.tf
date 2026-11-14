variable "name" {
  type = string
  validation {
    condition     = can(regex("^[a-zA-Z][a-zA-Z0-9-]{1,22}[a-zA-Z0-9]$", var.name)) && !can(regex("--", var.name))
    error_message = "Key Vault name must be reviewed, globally unique, 3-24 characters and follow Azure naming rules."
  }
}
variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tenant_id" {
  type = string
  validation {
    condition     = can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", var.tenant_id)) && lower(var.tenant_id) != "00000000-0000-0000-0000-000000000000"
    error_message = "Provide a genuine approved tenant UUID from restricted CI configuration."
  }
}
variable "tags" { type = map(string) }
variable "app_principal_id" { type = string }
variable "gateway_principal_id" { type = string }
variable "key_vault_configuration_approved" {
  type    = bool
  default = false
}
variable "app_secrets_reader_approved" {
  type    = bool
  default = false
}
variable "gateway_certificate_reader_approved" {
  type    = bool
  default = false
}
variable "role_assignment_approval_confirmed" {
  type    = bool
  default = false
}
