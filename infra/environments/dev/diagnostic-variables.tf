# D15 candidate only. All approvals absent by default; plans must fail closed.
# Never put log payloads, user data, secrets or real subscription IDs in Git.
variable "diagnostic_profiles" {
  description = "Five exact service profiles from signed Azure category API evidence, privacy review, FinOps and workspace approval. Empty is intentionally unapproved."
  type = map(object({
    categories                     = list(string)
    category_api_verified          = bool
    privacy_review_approved        = bool
    cost_review_approved           = bool
    workspace_destination_approved = bool
    operator_approved              = bool
  }))
  default  = {}
  nullable = false

  validation {
    condition = length(var.diagnostic_profiles) == 0 || (
      length(var.diagnostic_profiles) == 5 &&
      alltrue([for service in keys(var.diagnostic_profiles) : contains(["openai", "search", "cosmos", "app_service", "key_vault"], service)])
    )
    error_message = "D15: either leave ALL diagnostic profiles unapproved, or explicitly configure all five services."
  }

  validation {
    condition = alltrue([for service, profile in var.diagnostic_profiles :
      length(profile.categories) > 0 &&
      length(profile.categories) == length(distinct(profile.categories)) &&
      alltrue([for category in profile.categories :
        can(regex("^[A-Za-z][A-Za-z0-9_]{0,79}$", category)) &&
        !contains(["allLogs", "audit"], category)
      ])
    ])
    error_message = "D15: explicit unique API categories only; no category groups, duplicates, empty categories, wildcards or invalid strings."
  }
}
