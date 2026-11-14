variable "subscription_id" {
  description = "Approved Azure subscription UUID; never publish real values in this repository."
  type        = string
  validation {
    condition     = can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", var.subscription_id)) && lower(var.subscription_id) != "00000000-0000-0000-0000-000000000000"
    error_message = "Supply an approved non-placeholder subscription UUID via secured CI."
  }
}

variable "location" {
  type        = string
  description = "Approved Azure region; no default."
}

variable "resource_group_name" {
  type        = string
  description = "Independent bootstrap resource group."
}

variable "storage_account_name" {
  type        = string
  description = "Globally unique, lower-case storage account name."
  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.storage_account_name))
    error_message = "Storage account name must be 3–24 lowercase letters/digits."
  }
}

variable "state_container_name" {
  type        = string
  default     = "tfstate"
  description = "Private state Blob container name."
}

variable "bootstrap_vnet_name" {
  type        = string
  description = "Independent, management-only bootstrap VNet."
}

variable "bootstrap_vnet_cidr" {
  type        = string
  description = "Approved non-overlapping management VNet IPv4 CIDR."
  validation {
    condition     = can(cidrhost(var.bootstrap_vnet_cidr, 0))
    error_message = "Set an approved IPv4 CIDR."
  }
}

variable "bootstrap_pe_subnet_name" {
  type    = string
  default = "snet-bootstrap-pe"
}

variable "bootstrap_pe_subnet_cidr" {
  type        = string
  description = "Approved Private Endpoint subnet wholly within bootstrap VNet."
  validation {
    condition     = can(cidrhost(var.bootstrap_pe_subnet_cidr, 0))
    error_message = "Set an approved IPv4 CIDR."
  }
}

variable "ci_principal_object_id" {
  type        = string
  description = "Approved federated CI service principal Object ID (not client ID)."
  validation {
    condition     = can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", var.ci_principal_object_id)) && lower(var.ci_principal_object_id) != "00000000-0000-0000-0000-000000000000"
    error_message = "Supply approved CI principal object UUID via restricted CI."
  }
}

variable "blob_retention_days" {
  description = "Approved soft-delete retention; organization policy may require longer."
  type        = number
  default     = 30
  validation {
    condition     = var.blob_retention_days >= 7 && var.blob_retention_days <= 365
    error_message = "Retention must be 7–365 days for this baseline."
  }
}

variable "tags" {
  type        = map(string)
  description = "Organization-approved nonsecret tags."
  default = {
    workload    = "azure-private-ai-assurance"
    environment = "bootstrap"
    managed_by  = "terraform"
    sensitivity = "restricted"
  }
}
