# D16: approval-gated, RG-scoped Audit policy only. No paid Defender
# resource, subscription-wide policy, deny, modify or DINE permitted here.
# By default enable_audit_assignments=false => zero governance resources.
# This candidate has not passed terraform fmt/validate on the pinned provider.
resource "terraform_data" "d16_approval_gate" {
  count = var.enable_audit_assignments ? 1 : 0
  input = "D16 approved audit scope"
  lifecycle {
    precondition {
      condition     = var.scope_owner_approved && var.policy_definition_effects_verified && var.independent_review_approved && var.d15_no_diagnostic_ownership_collision_approved && length(var.audit_policies) > 0 && can(regex("^[a-fA-F0-9]{64}$", var.approved_evidence_sha256)) && var.approved_evidence_sha256 != "0000000000000000000000000000000000000000000000000000000000000000" && startswith(lower(var.resource_group_id), "/subscriptions/${lower(var.subscription_id)}/resourcegroups/")
      error_message = "D16: exact RG, definition effect, existing assignments, D15 ownership, 2-person review and evidence are mandatory."
    }
  }
}

resource "azurerm_resource_group_policy_assignment" "audit_only" {
  for_each             = var.enable_audit_assignments ? var.audit_policies : {}
  name                 = each.key
  resource_group_id    = var.resource_group_id
  policy_definition_id = each.value.definition_id
  display_name         = "D16 reviewed audit - ${each.key}"
  description          = "Auditing only, owner approved; D15 owns diagnostic settings."
  enforce              = false

  depends_on = [terraform_data.d16_approval_gate]

  lifecycle {
    prevent_destroy = true
    precondition {
      condition     = var.scope_owner_approved && var.policy_definition_effects_verified && var.independent_review_approved && var.d15_no_diagnostic_ownership_collision_approved && contains(["Audit", "AuditIfNotExists"], each.value.independently_verified_effect)
      error_message = "D16: never assign a policy without independent audit-only effect attestation."
    }
  }
}
