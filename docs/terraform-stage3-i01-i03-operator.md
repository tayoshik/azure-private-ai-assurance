# Terraform Stage 3 — I01/I02/I03 Operator Runbook

**Version:** 2026-11-14. **Scope:** User-assigned Managed Identity, private Key Vault, vault Private Endpoint and private DNS zone group. **Status:** Source implemented / offline structural test only; Terraform CLI and Azure are **NOT_EXECUTED**. All 1,716 live acceptance IDs remain `NOT_READY`; release `NO_GO`.

## 1. Design baseline and source lineage

Built on the previously checked Stage 1 bootstrap / Stage 2 N04 modules in the same public repository. This implementation does not replace or re-run their original research. Existing N04 NSG rules permit scoped Gateway/App requests to the *data Private Endpoint subnet*, not to an unrestricted public vault.

The vault has `rbac_authorization_enabled=true`, `public_network_access_enabled=false`, `purge_protection_enabled=true`, `soft_delete_retention_days=90`, and network ACL `Deny` / `None`. These are intentional security defaults. Key Vault name must be globally available. Purge protection cannot be reversed while active; **never attempt to destroy or purge a protected vault as a cleanup shortcut**.

The App and Gateway have **separate user-assigned managed identities**. Runtime secret-reading roles are assigned at the exact Key Vault resource scope only after explicit approvals. Vault certificate private keys, secrets, API keys, Terraform plan files and raw logs are **not stored** in this repository. The Application Gateway's eventual certificate binding is a separate DAG node (`GW02`) and has not been implemented here.

The vault's canonical API host is `<vault>.vault.azure.net`; its private DNS zone is `privatelink.vaultcore.azure.net`. The endpoint uses subresource `vault`, with a zone group attached to the existing managed private DNS zone. Network policies on the dedicated `data_private_endpoint` subnet were enabled by Stage 1.

## 2. Added / changed files

| Component | Terraform paths | Relation to DAG |
|---|---|---|
| Two user-assigned identities | `infra/modules/identity/{main,variables,outputs}.tf` | I01, Steps 42, 47, 53 |
| Vault and scoped data-plane roles | `infra/modules/key-vault/{main,variables,outputs}.tf` | I02, Steps 37, 42 |
| Vault Private Endpoint | `infra/modules/private-endpoints/{key-vault,variables,outputs}.tf` | I03, Steps 26, 30, 37, 38 |
| Root composition | `infra/environments/dev/{main,variables,outputs}.tf` | Reuses N01/N03/N05 |
| Public placeholder values | `infra/environments/dev/terraform.tfvars.example` | G07 NOT_READY |
| Offline contract checker | `scripts/check_terraform_i01_i03.py` | Q01 (text-only) |
| Negative/mutation tests | `tests/test_terraform_i01_i03.py` | 18 additional checks |

## 3. WSL2 — repeatable offline review (NO Azure authentication)

Execute on the fixed approved workstation. This is non-mutating, requires only Python 3 and Git and needs no `az login`.

```bash
set -Eeuo pipefail
cd "$HOME/azure-private-ai-assurance"
git pull --ff-only

git rev-parse HEAD
find infra -name '*.tf' -type f | sort
python3 scripts/check_terraform_stage1.py
python3 scripts/check_terraform_n04.py
python3 scripts/check_terraform_i01_i03.py
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v
```

**Expected:** `PASS_OFFLINE_I01_I03_TEXT_ONLY`, 28 Terraform files, two identities, one vault, one vault PE, no live Azure PASS, tests 47/47 PASS on the fixed source. No `terraform` CLI test was executed by the authoring environment.

**Failure response:** File missing → inspect Git commit and module paths. An approval variable changed from `false` → revert and require signed G07 ticket. A security setting changed → open a design review. Do **not** change PNA/RBAC/purge requirements to make tests green.

## 4. Terraform syntax / provider-schema gate — only when approved CLI exists

The project pins `azurerm = 4.66.0` **provisionally**; the lockfile and exact provider schema still need authorization. `terraform` is not installed in the document-authoring environment. On a workstation with an organization-approved Terraform binary and approved provider mirror/cache:

```bash
set -Eeuo pipefail
command -v terraform
terraform version
terraform -chdir=infra/environments/dev fmt -check -recursive
# Initialization is allowed only through the approved provider mirror/cache:
terraform -chdir=infra/environments/dev init -backend=false -input=false
terraform -chdir=infra/environments/dev validate -no-color
terraform -chdir=infra/environments/dev providers
```

**Expected:** exit 0 and exactly the reviewed provider selection. `init` can reach a provider registry; follow the corporate software-supply-chain route. **Do not treat lexical checks as HCL schema validation.** Do not run `terraform test` without inspecting `run` blocks: they may provision resources. Avoid saving real credentials or backend config into public Git.

## 5. Azure target observations — approved, pre-authenticated private CI only

Before beginning, the environment owner must provide a signed inventory containing tenant/subscription ID, resource group, actual vault name, vault ID, PE name, authorized runner VNet, expected PE NIC IP, DNS resolver, and review ID. These are not recorded in this public repository.

### 5.1 Verify identities (I01)

```bash
set -Eeuo pipefail
: "${RG:?}" "${APP_IDENTITY_NAME:?}" "${GW_IDENTITY_NAME:?}"
az identity show -g "$RG" -n "$APP_IDENTITY_NAME" \
  --query '{id:id,clientId:clientId,principalId:principalId,tenantId:tenantId}' -o json
az identity show -g "$RG" -n "$GW_IDENTITY_NAME" \
  --query '{id:id,clientId:clientId,principalId:principalId,tenantId:tenantId}' -o json
```

**Acceptance:** both identity resource IDs equal approved inventory; distinct identities and service principal IDs; application/gateway runtime principals correctly attached in later modules. Missing identity → `NOT_READY`, unexpected identity → investigate before accepting.

### 5.2 Verify vault (I02) — metadata only

```bash
set -Eeuo pipefail
: "${RG:?}" "${VAULT_NAME:?}"
az keyvault show -g "$RG" -n "$VAULT_NAME" \
  --query '{id:id,location:location,tenantId:properties.tenantId,publicNetworkAccess:properties.publicNetworkAccess,enableRbacAuthorization:properties.enableRbacAuthorization,enablePurgeProtection:properties.enablePurgeProtection,softDeleteRetentionInDays:properties.softDeleteRetentionInDays,networkAcls:properties.networkAcls}' -o json
```

**Acceptance:** actual vault is the approved object; public access Disabled, RBAC enabled, purge protection enabled, retention 90, ACL deny by default; compare to approved baseline and current API JSON schema. A successful CLI exit **does not** constitute PASS. Do not read or print secret values.

### 5.3 Verify scoped role grants (I02)

```bash
set -Eeuo pipefail
: "${VAULT_ARM_ID:?}"
az role assignment list --scope "$VAULT_ARM_ID" --include-inherited false \
  --query '[].{principalId:principalId,role:roleDefinitionName,scope:scope}' -o json
```

**Acceptance:** only explicitly approved principals receive `Key Vault Secrets User` at the vault scope, and no unexpected data-plane elevated roles. If approval flags are false, the Terraform module is designed to create **zero** reader assignments. Do not treat role assignment presence as proof that network access or token audience is correct.

### 5.4 Verify Private Endpoint and DNS (I03)

```bash
set -Eeuo pipefail
: "${RG:?}" "${KV_PE_NAME:?}" "${VAULT_NAME:?}" "${VAULT_PRIVATE_IP:?}"
az network private-endpoint show -g "$RG" -n "$KV_PE_NAME" \
  --query '{id:id,subnet:subnet.id,connection:privateLinkServiceConnections[].{groupIds:groupIds,status:privateLinkServiceConnectionState.status},nics:networkInterfaces[].id}' -o json
az network private-endpoint dns-zone-group list -g "$RG" --endpoint-name "$KV_PE_NAME" -o json
# On a VNet-attached and authorized test VM / runner, not an arbitrary internet host:
dig +short "${VAULT_NAME}.vault.azure.net" A
```

**Acceptance:** `Approved` connection, subresource `vault`, data-PE subnet ID, zone group `privatelink.vaultcore.azure.net`, and final canonical DNS A address **exactly equals** the independently approved PE NIC private IP. `dig` resolving any arbitrary RFC1918 address is insufficient; correlate NIC and IPAM. DNS NXDOMAIN or 403 alone does not prove an effective perimeter.

### 5.5 Approved negative tests (separate authorization)

Do not execute live intrusion probes to infer security. For an explicitly approved nonproduction vault, compare ARM PNA settings **and** controlled observations from trusted internal and external vantage points. Missing target existence, correct identity, DNS provenance or logs → `NOT_READY`. Unexpected live public access → `FAIL` and remediation ticket.

## 6. Evidence, trust and troubleshooting

For every applied test ID (e.g. `AZ-T37-*`, `AZ-T38-*`, `AZ-T42-*`, `AZ-T53-*`), save the exact Git commit, signed baseline reference, subscription/resource IDs, tool/Provider versions, UTC timestamp, CI job identity, expected/observed values, exit code, evidence SHA-256, and reviewer decision in **restricted** evidence storage. The English catalogue is draft until independently accepted.

| Symptom | Investigation order | Safe disposition |
|---|---|---|
| `terraform validate` rejects an argument | exact AzureRM 4.66 schema → HCL type/attribute → module inputs | FAIL source quality; never deploy |
| Plan fails approval precondition | G07 signed decision → model/SKU/region → Key Vault retention / NSG | NOT_READY until approved |
| Vault name unavailable / soft-deleted | global DNS name → retention policy → restore authority | Re-design name; do not purge to clear quickly |
| Key Vault PE connection not approved | PE service/group → scope → subnet → approved link | NOT_READY / FAIL per evidence |
| Vault FQDN resolves public | zone group → VNet link → DNS forwarders → PE NIC IP | FAIL private DNS gate; no network bypass |
| Gateway cannot retrieve certificate | gateway UAI attachment → vault role → DNS/PE → secret ID/versionless URI → logs | Pending GW02; don't enable public vault |
| Vault 403 | target existence → private endpoint/DNS → token audience → scoped RBAC → correlation logs | Cannot infer effective security from HTTP status alone |
| Unexpected role elevation | inherited role assignments → identity ownership → approval tickets | P0 review, no automatic escalation |

## 7. Boundaries and next user checkpoint

- `I01–I03` are **implemented source only**; actual Terraform provider schema, Azure deployment, private DNS, identities and vault role assignments remain unverified.
- Role assignment permission changes require independent approval and a least-privilege IAM owner. The CI identity is separate from the application and gateway user-assigned identities.
- The next source implementation is A01–A06 (Azure OpenAI, Search, Cosmos DB and scoped data-plane RBAC). **No user action required to draft it**.
- Earliest user input requirement is G07/B05 for **actual Azure plan** (approved nonproduction tenant/subscription, globally unique vault name, IPAM, DNS/network routing, runner/identity and security tickets). The number of conversational turns before that gate is not fixed; it occurs after module and provider checks, not after a promised delay.

## 8. References already checked, no duplicate research required

- Terraform Registry, `azurerm_key_vault`: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault
- Terraform Registry, `azurerm_user_assigned_identity`: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/user_assigned_identity
- Microsoft Learn, private endpoint DNS: https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns
- Microsoft Learn, Key Vault private-link diagnostics: https://learn.microsoft.com/en-us/azure/key-vault/general/private-link-diagnostics
- Microsoft Learn, App Gateway certificates: https://learn.microsoft.com/en-us/azure/application-gateway/key-vault-certs
