output "id" { value = azurerm_search_service.search.id }
output "name" { value = azurerm_search_service.search.name }
output "hostname" { value = "${azurerm_search_service.search.name}.search.windows.net" }
