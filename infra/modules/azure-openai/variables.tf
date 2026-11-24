variable "name" {
  type = string
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$", var.name))
    error_message = "Use a reviewed lowercase Azure OpenAI resource name (2-64 DNS-safe characters)."
  }
}
variable "custom_subdomain_name" {
  type = string
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$", var.custom_subdomain_name))
    error_message = "Approved custom subdomain must be 3-63 lowercase DNS-safe characters."
  }
}
variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tags" { type = map(string) }
variable "model_deployment_name" {
  type = string
  validation {
    condition     = can(regex("^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$", var.model_deployment_name))
    error_message = "Model deployment name must be a reviewed nonempty identifier without URI or whitespace."
  }
}
variable "model_name" {
  type = string
  validation {
    condition     = can(regex("^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$", var.model_name)) && var.model_name != "REPLACE_MODEL_NAME"
    error_message = "Use an explicitly approved model name, not a placeholder or URI."
  }
}
variable "model_version" {
  type = string
  validation {
    condition     = can(regex("^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$", var.model_version)) && var.model_version != "REPLACE_EXACT_VERSION"
    error_message = "Use an approved exact model version, not a placeholder or URI."
  }
}
variable "model_sku" {
  type = string
  validation {
    condition     = can(regex("^[A-Za-z][A-Za-z0-9_-]{0,63}$", var.model_sku))
    error_message = "Use an explicit model SKU identifier; availability and quota require separate approval."
  }
}
variable "model_capacity" {
  type = number
  validation {
    condition     = var.model_capacity > 0 && floor(var.model_capacity) == var.model_capacity
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
