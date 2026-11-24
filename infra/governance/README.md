# D16 candidate Terraform governance root (disabled by default)

This directory is **not installed** in `tayoshik/azure-private-ai-assurance`. It is a review-only candidate. It has no `azurerm_security_center_subscription_pricing` resource. Foundational CSPM is a separately approved subscription-owner opt-in, not automatically enabled.

- `enable_audit_assignments = false` means zero managed governance resources.
- When true, the `terraform_data` guard must reject unset owner/effect/independent review/D15 collision approvals, empty policies, invalid SHA or scope mismatch.
- Audit policy assignment is RG-scoped and `enforce = false`. The **actual existing policy definition and its effective `policyRule.then.effect` MUST be independently verified** before approved execution. Operator input `independently_verified_effect` does not magically inspect Azure.
- No MCSB initiative, Defender plan, remediation job, `deny`, `modify`, or `deployIfNotExists` is created here. Existing assigned initiatives and management group inherited policies require a read-only inventory.
- Resource-group Policy assignments can affect deployed resources when enabled. Even `enforce=false` is not permission to deploy; also, standalone remediation tasks can still exist.
- Use a separately approved protected backend key (`governance.tfstate` candidate), never the workload/bootstrap state key, and independently locked plan/artifacts.
- AzureRM is pinned to 4.66.0; no local Terraform provider tests are claimed. Copy the **verified repo lock file** into the approved local candidate workspace prior to `init -backend=false -lockfile=readonly` after the two-person review.
