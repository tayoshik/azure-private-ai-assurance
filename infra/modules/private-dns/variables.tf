variable "resource_group_name" {
  type = string
}
variable "virtual_network_id" {
  type = string
}
variable "zone_names" {
  type = list(string)
  validation {
    condition     = length(var.zone_names) == length(distinct(var.zone_names)) && length(var.zone_names) > 0
    error_message = "Private DNS zones must be non-empty and unique."
  }
}
variable "tags" {
  type = map(string)
}
