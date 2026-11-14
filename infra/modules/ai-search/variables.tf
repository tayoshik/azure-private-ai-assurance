variable "name" { type = string }
variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "tags" { type = map(string) }
variable "sku" { type = string }
variable "replica_count" { type = number }
variable "partition_count" { type = number }
variable "search_approved" {
  type    = bool
  default = false
}
variable "region_and_sku_approved" {
  type    = bool
  default = false
}
