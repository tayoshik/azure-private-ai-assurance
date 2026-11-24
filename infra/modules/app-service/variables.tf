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
variable "health_check_path" {
  type = string
  validation {
    condition     = can(regex("^/[A-Za-z0-9/_-]+$", var.health_check_path)) && !strcontains(var.health_check_path, "//") && trimspace(var.health_check_path) == var.health_check_path
    error_message = "Use an approved absolute health-check path; query, fragment, credentials and control characters are forbidden."
  }
}
variable "app_identity_id" { type = string }
variable "app_identity_client_id" { type = string }
variable "app_outbound_subnet_id" { type = string }
variable "web_inbound_pe_subnet_id" { type = string }
variable "openai_endpoint" {
  type = string
  validation {
    condition     = can(regex("^https://[a-z0-9][a-z0-9-]*[.]openai[.]azure[.]com/?$", lower(var.openai_endpoint))) && trimspace(var.openai_endpoint) == var.openai_endpoint
    error_message = "Require an approved AzurePublic OpenAI HTTPS endpoint without credentials, query or fragment."
  }
}
variable "openai_deployment_name" { type = string }
variable "search_hostname" {
  type = string
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]*[.]search[.]windows[.]net$", lower(var.search_hostname))) && trimspace(var.search_hostname) == var.search_hostname && !startswith(lower(var.search_hostname), "privatelink.")
    error_message = "Require an approved canonical AI Search hostname without scheme, credentials, path or query."
  }
}
variable "cosmos_endpoint" {
  type = string
  validation {
    condition     = can(regex("^https://[a-z0-9][a-z0-9-]*[.]documents[.]azure[.]com(:443)?/?$", lower(var.cosmos_endpoint))) && trimspace(var.cosmos_endpoint) == var.cosmos_endpoint
    error_message = "Require an approved Cosmos NoSQL HTTPS endpoint without credentials, query or fragment."
  }
}
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
