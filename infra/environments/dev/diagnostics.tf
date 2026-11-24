# D15 candidate only. Never merge/plan/apply until signed G07 + monitoring gates.
# All five resource keys are static; no unapproved implicit category collection.
# Dedicated destination type is omitted to preserve provider-default AzureDiagnostics
# until a validated per-category table routing decision is approved.
locals {
  d15_diagnostic_target_ids = {
    openai      = module.azure_openai.account_id
    search      = module.ai_search.id
    cosmos      = module.cosmos_db.account_id
    app_service = module.app_service.web_app_id
    key_vault   = module.key_vault.id
  }
}

resource "azurerm_monitor_diagnostic_setting" "approved_resource_logs" {
  for_each                   = local.d15_diagnostic_target_ids
  name                       = "diag-private-${each.key}-audit"
  target_resource_id         = each.value
  log_analytics_workspace_id = module.monitoring.workspace_id

  # Category names must come from the actual resource's diagnostic category API,
  # not a guessed allLogs/audit group or service display label.
  dynamic "enabled_log" {
    for_each = toset(try(var.diagnostic_profiles[each.key].categories, []))
    content {
      category = enabled_log.value
    }
  }

  lifecycle {
    prevent_destroy = true
    precondition {
      condition = try(
        var.diagnostic_profiles[each.key].category_api_verified &&
        var.diagnostic_profiles[each.key].privacy_review_approved &&
        var.diagnostic_profiles[each.key].cost_review_approved &&
        var.diagnostic_profiles[each.key].workspace_destination_approved &&
        var.diagnostic_profiles[each.key].operator_approved,
        false
      )
      error_message = "D15/G07: diagnostics require category API evidence, privacy, cost, workspace destination, and owner approvals for every service."
    }
    precondition {
      condition = try(
        length(var.diagnostic_profiles[each.key].categories) > 0 &&
        length(distinct(var.diagnostic_profiles[each.key].categories)) == length(var.diagnostic_profiles[each.key].categories),
        false
      )
      error_message = "D15: an explicit nonempty unique list of verified categories is required; no silent default."
    }
  }
}
