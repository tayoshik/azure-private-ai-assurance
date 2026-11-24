# Not part of the current repository until independently reviewed.
variable "subscription_id" {
  type = string
  validation {
    condition     = can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", var.subscription_id)) && var.subscription_id != "00000000-0000-0000-0000-000000000000"
    error_message = "Supply signed, non-placeholder subscription UUID."
  }
}
variable "resource_group_id" {
  type = string
  validation {
    condition     = can(regex("(?i)^/subscriptions/[0-9a-f-]{36}/resourcegroups/[^/]+$", var.resource_group_id))
    error_message = "Only an exact approved resource group scope is supported."
  }
}
variable "enable_audit_assignments" {
  type    = bool
  default = false
}
variable "scope_owner_approved" {
  type    = bool
  default = false
}
variable "policy_definition_effects_verified" {
  type    = bool
  default = false
}
variable "independent_review_approved" {
  type    = bool
  default = false
}
variable "d15_no_diagnostic_ownership_collision_approved" {
  type    = bool
  default = false
}
variable "approved_evidence_sha256" {
  type    = string
  default = ""
}

# No built-in policy IDs are invented in this candidate. Each needs a recorded
# tenant/region definition API lookup and independent signature.
variable "audit_policies" {
  type = map(object({
    definition_id                 = string
    independently_verified_effect = string
    evidence_sha256               = string
    approved_change_ticket        = string
    control_domain                = string
  }))
  default = {}
  validation {
    condition = alltrue([for k, v in var.audit_policies :
      can(regex("^[A-Za-z0-9][A-Za-z0-9_-]{1,45}$", k)) &&
      can(regex("(?i)^(?:/providers/Microsoft[.]Authorization/policyDefinitions/|/subscriptions/[0-9a-f-]{36}/providers/Microsoft[.]Authorization/policyDefinitions/)[^/]+$", v.definition_id)) &&
      contains(["Audit", "AuditIfNotExists"], v.independently_verified_effect) &&
      can(regex("^[a-fA-F0-9]{64}$", v.evidence_sha256)) && v.evidence_sha256 != "0000000000000000000000000000000000000000000000000000000000000000" &&
      length(trimspace(v.approved_change_ticket)) >= 8 &&
      contains(["network", "identity", "data", "compute"], v.control_domain)
    ])
    error_message = "Only signed single audit policy definitions (not DINE/modify/diagnostic owners) are permitted."
  }
}
