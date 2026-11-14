output "account_id" { value = azurerm_cosmosdb_account.no_sql.id }
output "account_name" { value = azurerm_cosmosdb_account.no_sql.name }
output "database_name" { value = azurerm_cosmosdb_sql_database.app.name }
output "container_name" { value = azurerm_cosmosdb_sql_container.app.name }
output "account_endpoint" { value = azurerm_cosmosdb_account.no_sql.endpoint }
