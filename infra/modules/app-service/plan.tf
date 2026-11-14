# W01: Linux plan. SKU and capacity require G03/G07 approval.
resource "azurerm_service_plan" "app" {
  name                = var.service_plan_name
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = var.service_plan_sku
  tags                = var.tags
  lifecycle {
    precondition {
      condition     = var.app_service_plan_approved && var.region_and_capacity_approved
      error_message = "W01: Linux plan/SKU/quota/cost review is required."
    }
    precondition {
      condition     = startswith(upper(var.service_plan_sku), "P") && length(var.service_plan_name) > 3
      error_message = "W01: only a reviewed Premium Linux plan is in scope."
    }
  }
}
