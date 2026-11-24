variable "manage_ci_identities" {
  description = "Opt into three dedicated GitHub OIDC identities and container-scoped RBAC."
  type        = bool
  default     = false

  # Terraform 1.9+ supports variable validations referring to other variables.
  # Do not establish split CI grants before the legacy grant is decommissioned.
  validation {
    condition     = !(var.manage_ci_identities && var.ci_principal_object_id != null)
    error_message = "Legacy CI principal and split CI identities must not coexist; complete an approved state/RBAC migration first."
  }
}

variable "existing_blob_dns_zone_id" {
  description = "Use the approved exact shared Hub Blob zone ID. Its owner manages VNet links and forwarding."
  type        = string
  default     = null

  validation {
    condition     = var.existing_blob_dns_zone_id == null || can(regex("(?i)^/subscriptions/[0-9a-f-]{36}/resourceGroups/[^/]+/providers/Microsoft[.]Network/privateDnsZones/privatelink[.]blob[.]core[.]windows[.]net$", var.existing_blob_dns_zone_id))
    error_message = "Supply the exact approved Azure Public Blob private DNS zone ARM ID or null for a separately owned zone."
  }
}

locals {
  ci_state_roles = var.manage_ci_identities ? {
    read  = "Storage Blob Data Reader"
    plan  = "Storage Blob Data Contributor"
    apply = "Storage Blob Data Contributor"
  } : {}
}

resource "azurerm_user_assigned_identity" "ci" {
  for_each            = local.ci_state_roles
  name                = "${var.resource_group_name}-ci-${each.key}"
  location            = azurerm_resource_group.bootstrap.location
  resource_group_name = azurerm_resource_group.bootstrap.name
  tags                = var.tags

  lifecycle {
    precondition {
      condition     = length(var.state_runner_cidrs) > 0
      error_message = "Approved Runner source CIDRs are required before creating dedicated CI identities."
    }
  }
}

resource "azurerm_federated_identity_credential" "ci" {
  for_each                  = local.ci_state_roles
  name                      = "github-nonprod-${each.key}"
  user_assigned_identity_id = azurerm_user_assigned_identity.ci[each.key].id
  issuer                    = "https://token.actions.githubusercontent.com"
  audience                  = ["api://AzureADTokenExchange"]
  subject                   = "repo:tayoshik/azure-private-ai-assurance:environment:nonprod-${each.key}"
}

resource "azurerm_role_assignment" "ci_container" {
  for_each             = local.ci_state_roles
  scope                = azurerm_storage_container.state.resource_manager_id
  role_definition_name = each.value
  principal_id         = azurerm_user_assigned_identity.ci[each.key].principal_id
}

output "ci_principals" {
  description = "Publish to restricted configuration; target ARM permissions are assigned separately."
  value = {
    for role, principal in azurerm_user_assigned_identity.ci : role => {
      client_id    = principal.client_id
      principal_id = principal.principal_id
      environment  = "nonprod-${role}"
    }
  }
}
