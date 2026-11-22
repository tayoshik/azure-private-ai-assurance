# O01 prerequisite for GW05. Public query and ingestion remain disabled.
resource "azurerm_log_analytics_workspace" "audit" {
  name                       = var.name
  resource_group_name        = var.resource_group_name
  location                   = var.location
  sku                        = "PerGB2018"
  retention_in_days          = var.retention_in_days
  internet_ingestion_enabled = false
  internet_query_enabled     = false
  tags                       = var.tags

  lifecycle {
    prevent_destroy = true
    precondition {
      condition     = var.monitoring_and_private_ingestion_approved
      error_message = "O01/O02: Monitoring access, AMPLS/private ingestion/query path, retention and budget must be approved."
    }
  }
}
