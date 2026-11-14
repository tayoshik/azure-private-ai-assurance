variable "name" { type = string }
variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tags" { type = map(string) }
variable "database_name" { type = string }
variable "container_name" { type = string }
variable "partition_key_paths" { type = list(string) }
variable "consistency_level" {
  type = string
  validation {
    condition = contains(["Session", "Strong", "Eventual", "ConsistentPrefix"], var.consistency_level)
    error_message = "Approved Cosmos consistency must be explicit."
  }
}
variable "backup_tier" {
  type = string
  validation {
    condition = contains(["Continuous7Days", "Continuous30Days"], var.backup_tier)
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
