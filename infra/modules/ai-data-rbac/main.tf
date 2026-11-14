# A06: minimal Azure data-plane roles for application MI.
resource "azurerm_role_assignment" "openai_user" {
  scope                = var.openai_account_id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = var.app_principal_id
  lifecycle {
    precondition {
      condition     = var.rbac_approved
      error_message = "A06/G07: approved OpenAI app identity and least-privilege scope required."
    }
  }
}

resource "azurerm_role_assignment" "search_reader" {
  scope                = var.search_service_id
  role_definition_name = "Search Index Data Reader"
  principal_id         = var.app_principal_id
  lifecycle {
    precondition {
      condition     = var.rbac_approved
      error_message = "A06/G07: approved Search index reader RBAC required."
    }
  }
}

# Built-in Cosmos SQL data roles differ from Azure management-plane role assignments.
# Scope is narrowed to the provisioned database/container.
locals {
  cosmos_role_guid = var.cosmos_write_approved ? "00000000-0000-0000-0000-000000000002" : "00000000-0000-0000-0000-000000000001"
}
resource "azurerm_cosmosdb_sql_role_assignment" "app" {
  resource_group_name = var.resource_group_name
  account_name        = var.cosmos_account_name
  principal_id        = var.app_principal_id
  role_definition_id  = "${var.cosmos_account_id}/sqlRoleDefinitions/${local.cosmos_role_guid}"
  scope               = "${var.cosmos_account_id}/dbs/${var.cosmos_database_name}/colls/${var.cosmos_container_name}"
  lifecycle {
    precondition {
      condition     = var.rbac_approved
      error_message = "A06/G07: approved Cosmos SQL role and exact data scope required."
    }
    precondition {
      condition     = !var.cosmos_write_approved || var.cosmos_write_justification_approved
      error_message = "A06: Cosmos data writer requires separate approved justification."
    }
  }
}
