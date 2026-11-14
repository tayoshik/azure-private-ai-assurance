# N01: Workload Resource Group; intentionally separate from bootstrap.
resource "azurerm_resource_group" "workload" {
  name     = var.name
  location = var.location
  tags     = var.tags
}
