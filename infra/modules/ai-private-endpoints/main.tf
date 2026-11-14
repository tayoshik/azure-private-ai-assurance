# A05: independent of the existing Key Vault private-endpoints module.
# Do not resolve application FQDNs directly to privatelink.* hosts.
resource "azurerm_private_endpoint" "openai" {
  name                = var.openai_pe_name
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id
  tags                = var.tags
  private_service_connection {
    name                           = "openai"
    private_connection_resource_id = var.openai_account_id
    subresource_names              = ["account"]
    is_manual_connection           = false
  }
  private_dns_zone_group {
    name                 = "openai-dns"
    private_dns_zone_ids = [var.openai_zone_id]
  }
  lifecycle {
    precondition {
      condition     = var.private_endpoints_approved && endswith(lower(var.openai_zone_id), "/privatelink.openai.azure.com")
      error_message = "A05: approved OpenAI PE and exact private DNS zone are required."
    }
  }
}

resource "azurerm_private_endpoint" "search" {
  name                = var.search_pe_name
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id
  tags                = var.tags
  private_service_connection {
    name                           = "search"
    private_connection_resource_id = var.search_service_id
    subresource_names              = ["searchService"]
    is_manual_connection           = false
  }
  private_dns_zone_group {
    name                 = "search-dns"
    private_dns_zone_ids = [var.search_zone_id]
  }
  lifecycle {
    precondition {
      condition     = var.private_endpoints_approved && endswith(lower(var.search_zone_id), "/privatelink.search.windows.net")
      error_message = "A05: approved Search PE and exact private DNS zone are required."
    }
  }
}

resource "azurerm_private_endpoint" "cosmos" {
  name                = var.cosmos_pe_name
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id
  tags                = var.tags
  private_service_connection {
    name                           = "cosmos"
    private_connection_resource_id = var.cosmos_account_id
    subresource_names              = ["Sql"]
    is_manual_connection           = false
  }
  private_dns_zone_group {
    name                 = "cosmos-dns"
    private_dns_zone_ids = [var.cosmos_zone_id]
  }
  lifecycle {
    precondition {
      condition     = var.private_endpoints_approved && endswith(lower(var.cosmos_zone_id), "/privatelink.documents.azure.com")
      error_message = "A05: approved NoSQL PE and exact private DNS zone are required."
    }
  }
}
