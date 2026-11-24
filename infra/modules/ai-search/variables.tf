variable "name" { type = string }
variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tags" { type = map(string) }
variable "sku" {
  type = string
  validation {
    condition     = trimspace(var.sku) != "" && lower(trimspace(var.sku)) != "free" && var.sku == trimspace(var.sku)
    error_message = "D13/A03: explicitly approve a non-free SKU without surrounding whitespace; verify region and private-link capability separately."
  }
}
variable "replica_count" {
  type = number
  validation {
    condition     = var.replica_count >= 1 && floor(var.replica_count) == var.replica_count
    error_message = "D13/A03: replicas must be a positive integer; capacity/availability remains region- and SKU-dependent."
  }
}
variable "partition_count" {
  type = number
  validation {
    condition     = var.partition_count >= 1 && floor(var.partition_count) == var.partition_count
    error_message = "D13/A03: partitions must be a positive integer; capacity/availability remains region- and SKU-dependent."
  }
}
variable "search_approved" {
  type    = bool
  default = false
}
variable "region_and_sku_approved" {
  type    = bool
  default = false
}
