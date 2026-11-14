# Terraform Stage 4 — A01–A06 AI/Data Deployment and Assurance Runbook

**Status:** Source implementation and offline contract checks only. **Azure live passes: 0; all live cases NOT_READY; release NO-GO.**

## 1. Scope, dependencies, and source provenance

This slice extends the owner-selected public `tayoshik/azure-private-ai-assurance` repository after the I01–I03 Stage 3 implementation (commit `86ae6535590635f9501f1f901e27b7ffec1c84d2`). It maps to construction Steps **33–45** and the existing Phase 4, 286-case English catalogue. It **does not replace** those test IDs or count offline detector outcomes as Azure live acceptance.

- **A01** `infra/modules/azure-openai/`: a Cognitive Account with `kind="OpenAI"`, public network access and local-key auth disabled, and mandatory custom subdomain.
- **A02** the same module contains a model deployment with pinned model version, explicit SKU/capacity, and `NoAutoUpgrade`.
- **A03** `infra/modules/ai-search/`: a paid/PE-capable Search service, public access and key authentication disabled, no trusted-service bypass.
- **A04** `infra/modules/cosmos-db/`: Cosmos DB NoSQL account, database/container, account keys disabled for the app, approved continuous backup policy.
- **A05** `infra/modules/ai-private-endpoints/`: separate Private Endpoints and DNS zone groups using subresources `account`, `searchService`, `Sql`. They share the approved existing **data Private Endpoint subnet** and wait for the Stage 2 network module to complete NSG attachments.
- **A06** `infra/modules/ai-data-rbac/`: App Managed Identity receives `Cognitive Services OpenAI User`, `Search Index Data Reader`, and scoped Cosmos **SQL data-plane** Reader by default. Cosmos Contributor requires a separate approval.

The Stage 3 `infra/modules/private-endpoints` for Key Vault is **not modified**. There are no API keys, connection strings, certificates or tenant-specific secrets in this public code.

## 2. Stage 4 preflight — fixed WSL workstation (NO Azure login)

```bash
set -Eeuo pipefail
cd "$HOME/azure-private-ai-assurance"
git pull --ff-only
git rev-parse HEAD
find infra/modules -type f -name '*.tf' | sort
python3 scripts/check_terraform_stage1.py
python3 scripts/check_terraform_n04.py
python3 scripts/check_terraform_i01_i03.py
python3 scripts/check_terraform_a01_a06.py
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v
```

**Expected:** Stage 4 prints `PASS_OFFLINE_A01_A06_TEXT_ONLY`, 43 `.tf` files, 12 checked Azure resource blocks, `azure_live_passes=0`, `NO_GO`; 69 total offline regression tests pass. This proves **only** that the source matches the frozen static safety assertions.

## 3. Terraform parser/provider validation — no Azure credentials

The managed workstation must use an organization-approved Terraform CLI and a trusted provider mirror; do **not** call `az login` here. The frozen existing root pins `hashicorp/azurerm = 4.66.0`, pending G03 formal schema verification. Commands below are **operator instructions, not results achieved in this turn**.

```bash
set -Eeuo pipefail
cd "$HOME/azure-private-ai-assurance"
command -v terraform || { echo 'NOT_READY: approved Terraform CLI absent'; exit 2; }
terraform version
terraform fmt -check -recursive infra
# Only with an approved provider mirror/cache and provider-source policy:
terraform -chdir=infra/environments/dev init -backend=false -input=false -no-color
terraform -chdir=infra/environments/dev validate -no-color
terraform -chdir=infra/environments/dev providers
terraform -chdir=infra/environments/dev providers schema -json \
  > /secure-artifacts/azurerm-stage4-schema.json
```

**Acceptance:** exact provider schema supports `azurerm_cognitive_account`, `azurerm_cognitive_deployment`, `azurerm_search_service`, `azurerm_cosmosdb_account`, `azurerm_cosmosdb_sql_container`, `azurerm_private_endpoint`, and `azurerm_cosmosdb_sql_role_assignment`; no unsupported attributes; `fmt`, `init`, `validate` exit 0. If GitHub Actions instead performs the syntax check, record its job URL and exact commit SHA. **`terraform init -backend=false` does not create/validate private remote state or authorize an apply.**

## 4. Inputs and approval checkpoint

The public `terraform.tfvars.example` uses **dummy values**. Before real planning, keep actual names, subscription, tenant, region, CIDRs and internal FQDNs in an approved restricted CI configuration. The real region is NOT assumed to be `japaneast` simply because the example displays it. G03/G07 must attest:

1. Region/model exact version, deployment SKU, capacity, quota, use case and residency.
2. Search SKU/replica/partition count, Private Link support, query/RBAC mode, cost budget.
3. Cosmos NoSQL API, capacity/RU/s, partition key, continuous backup tier and actual RTO/RPO.
4. Subnet policy, PE NICs, central Private DNS links and internal test-runner DNS route.
5. App identity principal ID, Search query permissions and Cosmos SQL data-role scope. Default role is **Reader**; an application that writes chat history must request a justified Contributor grant rather than silently escalating.
6. Two independent reviewers and an authorized private self-hosted runner, with proper state access and scoped workload identity.

**Fail closed:** `openai_account_approved`, `openai_region_quota_approved`, `openai_model_deployment_approved`, `search_service_approved`, `search_region_sku_approved`, `cosmos_account_approved`, `cosmos_backup_budget_approved`, `ai_private_endpoints_approved`, `ai_data_rbac_approved`, `cosmos_data_write_approved`, and `cosmos_write_justification_approved` all default `false`. No automation should set them to `true` without signed approvals.

## 5. Read-only Azure inspection — approved, pre-authenticated CI runner ONLY

These are illustrative commands **to be run later** on the organization-approved read-only Azure runner; they are **not** appropriate for an unauthenticated fixed WSL workstation. Do not write raw outputs containing organization-specific resource IDs to a public repository.

```bash
set -Eeuo pipefail
: "${RG:?approved resource group}" "${OPENAI_ACCOUNT:?}" "${SEARCH_SERVICE:?}" "${COSMOS_ACCOUNT:?}" "${APP_PRINCIPAL_ID:?}"
az cognitiveservices account show --resource-group "$RG" --name "$OPENAI_ACCOUNT" \
  --query '{id:id,kind:kind,publicNetworkAccess:properties.publicNetworkAccess}' -o json
az search service show --resource-group "$RG" --name "$SEARCH_SERVICE" \
  --query '{id:id,sku:sku.name,publicNetworkAccess:publicNetworkAccess}' -o json
az cosmosdb show --resource-group "$RG" --name "$COSMOS_ACCOUNT" \
  --query '{id:id,publicNetworkAccess:publicNetworkAccess,disableLocalAuth:disableLocalAuth,backupPolicy:backupPolicy}' -o json
az network private-endpoint list --resource-group "$RG" \
  --query '[].{id:id,subnet:subnet.id,connections:privateLinkServiceConnections[].privateLinkServiceConnectionState.status}' -o json
az role assignment list --assignee "$APP_PRINCIPAL_ID" --all \
  --query '[].{role:roleDefinitionName,scope:scope}' -o json
az cosmosdb sql role assignment list --resource-group "$RG" --account-name "$COSMOS_ACCOUNT" -o json
```

**Required result:** approved **actual resource IDs** exist; PNA disabled; local-key auth disabled; all three PE connections `Approved` and attached to the approved subnet; assigned data-plane roles match their exact scopes. The CLI's output shape varies by API version, so first check the raw schema. An empty output, API 403, failure to reach a resource, or `null` field is **NOT_READY**, never a PASS. Record exact CLI version, UTC, source SHA and evidence digest.

## 6. DNS and TLS validation — approved internal runner ONLY

```bash
set -Eeuo pipefail
: "${OPENAI_FQDN:?}" "${SEARCH_FQDN:?}" "${COSMOS_FQDN:?}"
for fqdn in "$OPENAI_FQDN" "$SEARCH_FQDN" "$COSMOS_FQDN"; do
  echo "=== $fqdn ==="
  dig +time=3 +tries=1 "$fqdn" CNAME
  dig +time=3 +tries=1 "$fqdn" A
  getent ahostsv4 "$fqdn" || true
done
```

**Acceptance:** inspect DNS aliases, then compare the **final A record** to the correct PE NIC's actual private IP and approved inventory. Do not count an arbitrary RFC1918 address as PASS. When the application exists, perform safe Managed Identity API calls and a denied-principal negative test from an isolated non-production identity, with logs and consent. Avoid test data containing confidential prompts or records.

## 7. Negative tests and triage

| Failure | Expected classification | Investigation |
|---|---|---|
| Account/PE not deployed | NOT_READY | G07 approvals and IaC apply gate, never fake a successful denial |
| OpenAI model missing or quota refused | NOT_READY/FAIL by signed criterion | region, SKU/capacity, exact model version and quota |
| Private DNS gives wrong A record | FAIL only with real signed baseline | Zone, VNet link, central DNS forwarder, NIC IP, stale cache |
| PNA enabled or API keys accepted | FAIL after verified observation | resource/network attributes, policy drift; no production mutation during test |
| OpenAI/Search 403 | NOT_READY until cause known | wrong token audience/MI, app data roles, PNA/PE routing |
| Cosmos SDK 403 | NOT_READY until scoped evidence | native SQL data roles, metadata permissions and database/container scope |
| Search indexer cannot reach private source | NOT_READY | consider optional Search Shared Private Link (A07), approvals |
| `terraform init`/`validate` fails | FAIL offline build; Azure state unchanged | provider version, mirror, schema/API breaking changes, auth-independent static issues |

## 8. Source-to-test traceability and evidence

Map new resources to the existing `AZ-T33-01`–`AZ-T45-22` IDs; preserve all 286 original Phase 4 entries and classify synthetic deviations separately from live controls. The acceptance overlay is not generated until runner identity, exact asset IDs, UTC, approval, raw sanitized output SHA-256 and independent reviewers exist.

Store restricted evidence in the organization's approved private evidence repository, not GitHub. No `terraform apply`, Azure mutating calls, WAF simulation, performance load or negative identity mutations are included in these scripts.

## 9. Next implementation work and user checkpoint

The next **source-only** turn can implement W01–W05 (App Service Plan, Linux Web App, outbound VNet Integration, inbound PE and configuration) with no user action. Then GW01–GW05 and Q01/Q02 follow, again as source+offline QA. Before **any real `plan`**, the user/environment owner must provide approved region/model/version/quota, exact subscription/RG/CIDR/FQDN values, scoped CI state connectivity, cost/DR decisions and change approval. Until then the formal state is NO-GO.
