# A01/A02: Private Azure OpenAI account and version-pinned model deployment.
# Region/model/quota must be verified by the approved G03 compatibility gate.
resource "azurerm_cognitive_account" "openai" {
  name                          = var.name
  location                      = var.location
  resource_group_name           = var.resource_group_name
  kind                          = "OpenAI"
  sku_name                      = "S0"
  custom_subdomain_name         = var.custom_subdomain_name
  public_network_access_enabled = false
  local_auth_enabled             = false
  tags                          = var.tags

  lifecycle {
    precondition {
      condition     = var.openai_account_approved && var.region_and_quota_approved
      error_message = "A01/G03/G07: approved account, region, model quota and compliance profile are required."
    }
    precondition {
      condition     = length(trimspace(var.custom_subdomain_name)) > 2
      error_message = "A01: a non-empty custom subdomain is mandatory for private endpoint and Entra auth."
    }
  }
}

resource "azurerm_cognitive_deployment" "model" {
  name                 = var.model_deployment_name
  cognitive_account_id = azurerm_cognitive_account.openai.id
  version_upgrade_option = "NoAutoUpgrade"

  model {
    format  = "OpenAI"
    name    = var.model_name
    version = var.model_version
  }
  sku {
    name     = var.model_sku
    capacity = var.model_capacity
  }
  lifecycle {
    precondition {
      condition     = var.model_deployment_approved && var.region_and_quota_approved && var.model_capacity > 0
      error_message = "A02: model, version, quota, SKU, residency and capacity require approval before plan."
    }
  }
}
