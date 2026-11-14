variable "name" { type = string }
variable "custom_subdomain_name" { type = string }
variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tags" { type = map(string) }
variable "model_deployment_name" { type = string }
variable "model_name" { type = string }
variable "model_version" { type = string }
variable "model_sku" { type = string }
variable "model_capacity" {
  type = number
  validation {
    condition     = var.model_capacity > 0
    error_message = "Model capacity must be positive and quota-approved."
  }
}
variable "openai_account_approved" {
  type    = bool
  default = false
}
variable "region_and_quota_approved" {
  type    = bool
  default = false
}
variable "model_deployment_approved" {
  type    = bool
  default = false
}
