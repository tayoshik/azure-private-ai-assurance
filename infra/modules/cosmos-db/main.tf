# A04: Cosmos DB for NoSQL, Entra-only data access and continuous backup.
# The G07 gate must approve regional availability, consistency, backup and budget.
resource "azurerm_cosmosdb_account" "no_sql" {
  name                                  = var.name
  location                              = var.location
  resource_group_name                   = var.resource_group_name
  offer_type                            = "Standard"
  kind                                  = "GlobalDocumentDB"
  public_network_access_enabled         = false
  local_authentication_disabled         = true
  network_acl_bypass_for_azure_services = false
  automatic_failover_enabled            = false
  tags                                  = var.tags

  consistency_policy {
    consistency_level = var.consistency_level
  }
  geo_location {
    location          = var.location
    failover_priority = 0
  }
  backup {
    type = "Continuous"
    tier = var.backup_tier
  }
  lifecycle {
    precondition {
      condition     = var.cosmos_account_approved && var.backup_and_budget_approved
      error_message = "A04/G07: approved region, backup retention, data controls and RU/s budget required."
    }
  }
}

resource "azurerm_cosmosdb_sql_database" "app" {
  name                = var.database_name
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.no_sql.name
}

resource "azurerm_cosmosdb_sql_container" "app" {
  name                = var.container_name
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.no_sql.name
  database_name       = azurerm_cosmosdb_sql_database.app.name
  partition_key_paths = var.partition_key_paths
  lifecycle {
    precondition {
      condition     = length(var.partition_key_paths) == 1 && startswith(try(var.partition_key_paths[0], ""), "/")
      error_message = "A04: a single reviewed absolute NoSQL partition-key path is mandatory."
    }
  }
}
