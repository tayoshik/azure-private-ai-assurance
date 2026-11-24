variable "name" { type = string }
variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tags" { type = map(string) }
variable "database_name" {
  type = string
  validation {
    condition     = length(trimspace(var.database_name)) > 0 && var.database_name == trimspace(var.database_name) && length(var.database_name) <= 255 && alltrue([for x in ["/", "\\", "?", "#"] : !strcontains(var.database_name, x)])
    error_message = "D13/A04: database name must be nonblank, <=255 chars, without surrounding whitespace or / backslash ? #."
  }
}
variable "container_name" {
  type = string
  validation {
    condition     = length(trimspace(var.container_name)) > 0 && var.container_name == trimspace(var.container_name) && length(var.container_name) <= 255 && alltrue([for x in ["/", "\\", "?", "#"] : !strcontains(var.container_name, x)])
    error_message = "D13/A04: container name must be nonblank, <=255 chars, without surrounding whitespace or / backslash ? #."
  }
}
variable "partition_key_paths" {
  type = list(string)
  validation {
    condition     = length(var.partition_key_paths) == 1 && alltrue([for p in var.partition_key_paths : length(p) > 1 && startswith(p, "/") && !endswith(p, "/") && !strcontains(p, "//") && !strcontains(p, "?") && !strcontains(p, "#") && !strcontains(p, "\\") && p == trimspace(p)])
    error_message = "D13/A04: exactly one reviewed absolute partition key path is required; reject empty/trailing/double slash and ? # backslash."
  }
}
variable "consistency_level" {
  type = string
  validation {
    condition     = contains(["Session", "Strong", "Eventual", "ConsistentPrefix"], var.consistency_level)
    error_message = "Approved Cosmos consistency must be explicit."
  }
}
variable "backup_tier" {
  type = string
  validation {
    condition     = contains(["Continuous7Days", "Continuous30Days"], var.backup_tier)
    error_message = "Choose an explicitly approved continuous backup tier."
  }
}
variable "cosmos_account_approved" {
  type    = bool
  default = false
}
variable "backup_and_budget_approved" {
  type    = bool
  default = false
}
