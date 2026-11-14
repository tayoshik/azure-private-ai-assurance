variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tags" { type = map(string) }
variable "app_identity_name" {
  type = string
  validation {
    condition     = length(var.app_identity_name) > 2 && length(var.app_identity_name) <= 128
    error_message = "Provide a reviewed App Service user-assigned identity name."
  }
}
variable "gateway_identity_name" {
  type = string
  validation {
    condition     = length(var.gateway_identity_name) > 2 && length(var.gateway_identity_name) <= 128
    error_message = "Provide a reviewed Application Gateway user-assigned identity name."
  }
}
