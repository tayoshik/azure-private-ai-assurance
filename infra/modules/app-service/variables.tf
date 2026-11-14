variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "tags" { type = map(string) }
variable "service_plan_name" { type = string }
variable "service_plan_sku" { type = string }
variable "web_app_name" { type = string }
variable "python_version" {
  type = string
  validation {
    condition     = contains(["3.11", "3.12", "3.13"], var.python_version)
    error_message = "Pin and approve a supported Python runtime."
  }
}
variable "health_check_path" { type = string }
variable "app_identity_id" { type = string }
variable "app_identity_client_id" { type = string }
variable "app_outbound_subnet_id" { type = string }
variable "web_inbound_pe_subnet_id" { type = string }
variable "openai_endpoint" { type = string }
variable "openai_deployment_name" { type = string }
variable "search_hostname" { type = string }
variable "cosmos_endpoint" { type = string }
variable "cosmos_database_name" { type = string }
variable "cosmos_container_name" { type = string }
variable "app_service_plan_approved" {
  type    = bool
  default = false
}
variable "region_and_capacity_approved" {
  type    = bool
  default = false
}
variable "web_app_configuration_approved" {
  type    = bool
  default = false
}
variable "outbound_integration_approved" {
  type    = bool
  default = false
}
variable "application_contract_approved" {
  type    = bool
  default = false
}
