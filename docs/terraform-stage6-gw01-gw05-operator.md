# Terraform Stage 6 — Private Application Gateway WAF_v2 (GW01–GW05)

**Status:** CODE DRAFT / offline contract tests only. **Azure live PASS: 0**. **Release: NO-GO**. This document applies to the source snapshot supplied in the Stage 6 ZIP and (once verified) the matching GitHub commit.

## 1. Exact architectural scope

- **GW01**: `azurerm_web_application_firewall_policy` with Microsoft DRS 2.2, default `Detection`, Prevention gated by separate approval.
- **GW02**: separate Gateway user-assigned identity, **existing** Key Vault certificate *versionless secret ID*. No certificate/PFX bytes or passwords in Terraform state. The certificate and real Key Vault RBAC must be provisioned/confirmed out of band before planning.
- **GW03**: **private-only** `azurerm_application_gateway` WAF_v2, single static private frontend on dedicated `Microsoft.Network/applicationGateways` delegated subnet. No public frontend.
- **GW04**: HTTPS 443 listener on approved business FQDN; HTTPS App Service default hostname backend, matching `host_name` and `/healthz` probe. TLS name and chain require an independent runtime test.
- **GW05**: resource-specific Application Gateway Access and Firewall diagnostic logs to an approved Log Analytics Workspace. **O01 workspace is included; O02 AMPLS/private ingestion/query path is NOT built yet.** The workspace explicitly has public log ingestion and query disabled, so logs cannot be considered operational until approved O02 is connected.

### Dependencies

`G03/G07` feature/region/SKU/IPAM approval → `N03/N04` gateway subnet/NSG/egress → `I01/I02/I03` identity, vault and private key path → `W04` App Service private endpoint → `GW01–GW04` listener and health → `O01/O02 + GW05` ingestion and diagnostics → `Q01/Q02` provider/plan policy → `Q03/Q04/Q05` actual approved CI plan/review/apply → `V01–V09` acceptance.

The single Terraform `azurerm_application_gateway` resource contains listener, routing and probe nested blocks. It cannot be split into independent Terraform resources merely to match DAG names. `routing.tf` defines canonical local names used by `gateway.tf`.

## 2. Supported execution places

| Executor | Allowed | Not allowed |
|---|---|---|
| Fixed Windows WSL2 | Git, Python offline checks, approved local `terraform fmt`, source review | `az login`, production Azure queries, `plan` or `apply` |
| Approved pinned build runner | `terraform init -backend=false`, `fmt`, `validate`, `providers schema -json`, offline plan policy fixture | Azure mutations without G07/Q04 approval |
| Approved private CI runner | Explicitly permitted read-only inventory of deployed nonproduction Azure resources | Unreviewed `apply`, live WAF attacks, unauthorized logs |
| Authorized internal nonproduction test runner | DNS/TLS/backend health and bounded safe WAF smoke testing | External scanning or traffic from unknown networks |

## 3. WSL: one-paste source checkout and regression

Execute **inside WSL**, not at `C:\>` (type `wsl` first if needed). The Stage 5 ZIP can remain as an archived SHA-256 reference; the Stage 6 code comes from this package or the updated GitHub repository.

```bash
set -Eeuo pipefail
REPO="$HOME/azure-private-ai-assurance"
if [[ -e "$REPO" && ! -d "$REPO/.git" ]]; then
  echo "NOT_READY: target directory exists but is not a Git checkout: $REPO" >&2
  exit 2
fi
if [[ ! -d "$REPO/.git" ]]; then
  git clone https://github.com/tayoshik/azure-private-ai-assurance.git "$REPO"
fi
git -C "$REPO" pull --ff-only
cd "$REPO"
git rev-parse HEAD
python3 scripts/check_terraform_gw01_gw05.py
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v
```

**Expected:** `PASS_OFFLINE_TEXT_ONLY` for the GW code checks; 110/110 Python tests in the frozen Stage 6 package. Counts in newer revisions can differ. This does not execute Azure nor validate provider semantics.

**If failed:** distinguish missing clone/network/auth from a genuine checker failure. Never delete or reset an existing working tree without its owner.

## 4. Approved build runner: Terraform syntax/provider schema (NOT YET RUN)

The Terraform executable is not present in the authoring environment. The following commands are **instructions**, not claimed results. Provider 4.66.0 is provisionally pinned in `infra/environments/dev/versions.tf`; verify the approved version and its schema.

```bash
set -Eeuo pipefail
cd "$HOME/azure-private-ai-assurance"
command -v terraform >/dev/null || { echo 'NOT_READY: approved Terraform CLI missing'; exit 2; }
terraform version
terraform fmt -check -recursive infra
terraform -chdir=infra/environments/dev init -backend=false -input=false
terraform -chdir=infra/environments/dev validate
terraform -chdir=infra/environments/dev providers
terraform -chdir=infra/environments/dev providers schema -json > "$SECURE_ARTIFACT_DIR/provider-schema.json"
sha256sum "$SECURE_ARTIFACT_DIR/provider-schema.json"
```

**Pass:** exit 0, independently reviewed provider schema and lock file, verified `azurerm_application_gateway`, `azurerm_web_application_firewall_policy`, `azurerm_monitor_diagnostic_setting` and `azurerm_log_analytics_workspace` resource support. Never interpret failed `init` as insecure cloud configuration; it may mean network/package mirror is inaccessible.

## 5. Approved CI: read-only Azure inspection after authorized deployment (NOT RUN)

Set `$RESOURCE_GROUP`, `$APPGW_NAME`, `$VAULT_NAME`, `$WORKSPACE_ID`, `$BUSINESS_FQDN` and `$APP_DEFAULT_HOSTNAME` **only within the approved protected runner**. The preauthenticated runner uses federated identity; do not run `az login` on the fixed WSL computer.

```bash
set -Eeuo pipefail
: "${RESOURCE_GROUP:?}" "${APPGW_NAME:?}" "${WORKSPACE_ID:?}"
az network application-gateway show -g "$RESOURCE_GROUP" -n "$APPGW_NAME" \
  --query '{id:id,sku:sku,frontend:frontendIPConfigurations,identity:identity,policy:firewallPolicy}' -o json
az network application-gateway show-backend-health -g "$RESOURCE_GROUP" -n "$APPGW_NAME" -o json
az monitor diagnostic-settings list --resource \
  "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.Network/applicationGateways/${APPGW_NAME}" -o json
```

**Pass conditions:** target resource exists under approved subscription; gateway frontend references **no public IP**; private frontend is the authorized IP; managed identity and Key Vault certificate link are approved; backend health is `Healthy` for the exact expected FQDN; diagnostic categories and workspace target match signed design. Resource existence or command exit 0 alone is never PASS.

**Failure triage:** 404 → wrong resource or missing deployment (`NOT_READY`), 403 → CI permissions/scope, `Unhealthy` → Private DNS resolution, TLS/SNI, probe path, backend app and Key Vault certificate chain. Diagnose without weakening public-network controls.

## 6. Approved internal runner: DNS and HTTPS (NOT RUN)

```bash
set -Eeuo pipefail
: "${BUSINESS_FQDN:?}" "${APP_DEFAULT_HOSTNAME:?}" "${EXPECTED_GATEWAY_PRIVATE_IP:?}" "${EXPECTED_APP_PE_IP:?}"
for fqdn in "$BUSINESS_FQDN" "$APP_DEFAULT_HOSTNAME"; do
  printf '== %s ==\n' "$fqdn"
  dig +time=3 +tries=1 +short "$fqdn" CNAME
  dig +time=3 +tries=1 +short "$fqdn" A
done
# Review: compare resolved A records EXACTLY against signed expected IPs.
# Use ordinary hostname and TLS verification (do not use curl -k).
curl --fail --silent --show-error --connect-timeout 10 \
  "https://${BUSINESS_FQDN}/healthz" -o /dev/null \
  -w 'HTTP=%{http_code} TLS_VERIFY=%{ssl_verify_result} REMOTE_IP=%{remote_ip}\n'
```

**Pass conditions:** gateway private IP and App Service PE private IP are independently matched to their real NIC/IP inventory, TLS verification succeeds and `/healthz` returns the approved response. A failed lookup/timeout alone does not prove the external boundary is protected.

## 7. WAF and diagnostic correlation (approved NONPROD only)

1. Keep `waf_mode=Detection` initially.
2. Run approved benign controls and narrowly scoped synthetic WAF patterns on the approved **nonproduction** endpoint only, recording a unique request ID. No attacker payloads or customer data are supplied in the public repo.
3. In Log Analytics resource-specific mode verify the selected Gateway resource and time window:

```kusto
AGWFirewallLogs
| where TimeGenerated > ago(1h)
| where _ResourceId =~ "<approved-gateway-resource-id>"
| project TimeGenerated, TransactionId, Action, RuleId, RequestUri
| order by TimeGenerated desc
```

4. Verify policy mode, related access records and expected backend observations; Detection events must **not** be called blocked traffic.
5. Escalate to Prevention only after a documented false-positive review and a separate approval; verify both expected blocks and legitimate requests. Retention, log delivery time, and data minimization are independent gates.

**Troubleshooting:** No logs → verify O02 private ingestion route/AMPLS, workspace access, resource categories, ingestion latency and identity/RBAC. Do not enable public ingestion merely to make a test green.

## 8. Acceptance and release

| Control | Evidence | State at publication |
|---|---|---|
| GW01 WAF mode and managed rules | Provider schema + approved policy + WAF sample logs | NOT_READY |
| GW02 TLS/Key Vault | Separate certificate import, RBAC, hostname/chain and expiry | NOT_READY |
| GW03 private-only frontend | Azure resource, NSG, IPAM and off-network observations | NOT_READY |
| GW04 health and listener | Private DNS, backend health, 200-series response, TLS | NOT_READY |
| GW05 diagnostics | Workspace, O02 private ingestion and correlated log arrival | NOT_READY |

No Terraform `plan`, `apply`, live WAF requests, Playwright or Azure connectivity were performed for this Stage 6 package. All 1,716 project live acceptance cases remain `NOT_READY`; production remains **NO-GO**.

## Sources checked for design

- Microsoft Learn: Private Application Gateway deployment — https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-private-deployment
- Microsoft Learn: Application Gateway diagnostics — https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-diagnostics
- Terraform Registry: Application Gateway — https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/application_gateway
- Terraform Registry: WAF Policy — https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/web_application_firewall_policy
