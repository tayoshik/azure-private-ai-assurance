variable "name" { type = string }
variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tags" { type = map(string) }
variable "retention_in_days" {
  type = number
  default = 30
  validation {
    condition = var.retention_in_days >= 30 && var.retention_in_days <= 730
    error_message = "Retention needs a separate approval within provider/SKU limits."
  }
}
variable "monitoring_and_private_ingestion_approved" {
  type = bool
  default = false
}
