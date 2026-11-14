output "openai_user_assignment_id" { value = azurerm_role_assignment.openai_user.id }
output "search_reader_assignment_id" { value = azurerm_role_assignment.search_reader.id }
output "cosmos_sql_assignment_id" { value = azurerm_cosmosdb_sql_role_assignment.app.id }
