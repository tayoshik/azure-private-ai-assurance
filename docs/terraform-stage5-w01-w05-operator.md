# Terraform Stage 5 — W01–W05 Linux App Service and Private Connectivity

**Status:** Source created / offline checks only. **Azure live PASS: 0. Release: NO-GO.**

## 1. Traceability and architecture
| Node | Terraform source | Original runbook step | Function |
|---|---|---|---|
| W01 | `infra/modules/app-service/plan.tf` | 46 | Linux Premium App Service Plan |
| W02 | `infra/modules/app-service/webapp.tf` | 47 | Hardened Linux Web App, MI and HTTPS |
| W03 | `infra/modules/app-service/outbound-vnet.tf` + webapp inline property | 49 | Outbound VNet Integration |
| W04 | `infra/modules/webapp-private-endpoint/webapp.tf` | 39, 56 | Inbound sites PE, DNS zone group / SCM |
| W05 | `infra/modules/app-service/app-settings.tf` | 48, 65 | Canonical AI endpoints and managed identity |

Inbound **Private Endpoint** and outbound **VNet integration** use different subnet IDs. The Web App manages outbound integration *only* with `virtual_network_subnet_id`, never the standalone Swift connection resource. The inbound PE uses `sites` subresource and `privatelink.azurewebsites.net` DNS zone; SCM must also be resolved privately.

The existing Key Vault PE and AI-data PE remain independent. App settings contain nonsecret endpoint identifiers and a UAMI client ID, not API keys. The Python 3.11 example is **not** verified against actual application source. Actual app, health endpoint, Entra EasyAuth, private deploy workflow, and Gateway are outstanding implementation dependencies.

## 2. Execution environments and prerequisites
- **Fixed WSL2 machine:** Git and Python static/offline tests only. **No interactive `az login`.**
- **Approved build runner:** pinned Terraform and AzureRM 4.66.0 provider; approved provider mirror/cache. Repository does not contain a reviewed `.terraform.lock.hcl`.
- **Approved private CI:** read-only Azure inventory and PE/DNS checks only after authorized nonproduction deployment.
- **Separate approved CI apply job:** only after G07 environment, B05 remote state, Q03 saved plan and Q04 two independent approvals.
- Seven stage-5 approval variables default to **false**, and the example tfvars cannot authorize an apply.

## 3. WSL tests — no Azure authentication
```bash
set -Eeuo pipefail
cd "$HOME/azure-private-ai-assurance"
git pull --ff-only
python3 scripts/check_terraform_stage1.py
python3 scripts/check_terraform_n04.py
python3 scripts/check_terraform_i01_i03.py
python3 scripts/check_terraform_a01_a06.py
python3 scripts/check_terraform_w01_w05.py
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v
```

**Expected:** source-only static checks PASS, 91 Terraform unit tests PASS (69 inherited + 22 new), without Azure credentials. These are synthetic regression tests and **not** real Terraform parsing, provider validation, or cloud security evidence.

## 4. Provider-aware static validation — approved offline builder
```bash
set -Eeuo pipefail
terraform version
terraform fmt -check -recursive infra
terraform -chdir=infra/environments/dev init -backend=false -input=false -lockfile=readonly
terraform -chdir=infra/environments/dev validate -no-color
terraform -chdir=infra/environments/dev providers
```
**NOT EXECUTED for this stage** because Terraform CLI and approved provider lock were unavailable. Generate/pin/review the lock file in the controlled dependency acquisition process; a missing lock means `NOT_READY`, not permission to fetch arbitrary provider versions. Review and commit any required `terraform fmt` corrections. `init -backend=false` is not a deployment.

## 5. Detailed Azure read-only procedures (authorized runner only)

**W01 — Service Plan**
```bash
: "${RG:?}" "${PLAN_NAME:?}"
az appservice plan show -g "$RG" -n "$PLAN_NAME" \
  --query '{id:id,kind:kind,sku:sku.name,numberOfWorkers:numberOfWorkers}' -o json
```
Confirm exact signed resource ID, Linux SKU/availability, capacity and cost approval. NotReady if any prerequisite is absent.

**W02 — Web App hardening**
```bash
: "${RG:?}" "${WEBAPP_NAME:?}"
az webapp show -g "$RG" -n "$WEBAPP_NAME" \
  --query '{id:id,httpsOnly:httpsOnly,publicNetworkAccess:publicNetworkAccess,hostNames:hostNames}' -o json
az webapp config show -g "$RG" -n "$WEBAPP_NAME" \
  --query '{minTlsVersion:minTlsVersion,ftpsState:ftpsState,healthCheckPath:healthCheckPath,vnetRouteAllEnabled:vnetRouteAllEnabled}' -o json
```
Require PNA Disabled, HTTPS only, reviewed TLS, no FTP/publish Basic Auth, correct identity and health path. Verify actual API version if CLI projection omits a field; missing is NOT_READY, never PASS.

**W03 — Outbound integration and routing**
```bash
az webapp vnet-integration list -g "$RG" -n "$WEBAPP_NAME" -o json
```
Match exactly to the *approved outbound integration subnet*, effective NSG/UDR, dependency DNS and required Entra/monitoring/certificate-validation egress. Do not weaken public access or keys to correct connectivity.

**W04 — Inbound PE, zone group, DNS/SCM**
```bash
: "${WEB_PE_RG:?}" "${WEB_PE_NAME:?}"
az network private-endpoint show -g "$WEB_PE_RG" -n "$WEB_PE_NAME" \
  --query '{id:id,subnet:subnet.id,connections:privateLinkServiceConnections[].{group:groupIds,state:privateLinkServiceConnectionState.status}}' -o json
az network private-endpoint dns-zone-group list -g "$WEB_PE_RG" \
  --endpoint-name "$WEB_PE_NAME" -o json
```
On the **approved internal runner**, not the fixed workstation:
```bash
: "${WEBAPP_FQDN:?}" "${WEBAPP_SCM_FQDN:?}"
dig +short "$WEBAPP_FQDN" A
dig +short "$WEBAPP_SCM_FQDN" A
curl --fail-with-body --silent --show-error --max-time 15 \
  "https://${WEBAPP_FQDN}/healthz"
```
Require PE `Approved`, `sites`, exact inbound subnet and PE NIC address for *both* regular and SCM hostnames. The app must be deployed before `/healthz` can pass. Authentication-required SCM responses need a separate reviewed expectation.

**W05 — Identity and dependencies**
Confirm UAMI and service-specific data RBAC scopes. Reconcile app setting names with the actual app source, then make allowed and denied managed-identity requests privately. Correlate application, gateway and PaaS logs with approved test IDs. Never substitute API keys.

## 6. Evidence / failure triage
For every `AZ-T46-*`, `AZ-T47-*`, `AZ-T48-*`, `AZ-T49-*`, `AZ-T39-*`, `AZ-T64-*`: preserve test ID, UTC, source SHA, exact asset ID, approved baseline, runner, exit code, sanitized evidence digest and independent reviewer.

| Symptom | Primary checks | Classification |
|---|---|---|
| `terraform fmt` or `validate` fails | Formatter, approved provider and module arguments | NOT_READY |
| No `/healthz` implementation | Actual app source and deployment missing | NOT_READY |
| App 403/404 or TLS error | Auth, hostname, PE/DNS, SNI, access scope | NOT_READY or verified FAIL, never PASS on its own |
| App cannot reach AI/Search/Cosmos | UAMI, data RBAC, PE IP, DNS, egress allowlist | Investigate; do not enable keys |
| SCM deployment fails | Private SCM DNS, private runner, published credentials disabled | NOT_READY; no public bypass |
| PE DNS resolves public | Zone links, zone group, conditional forwarding and NIC | FAIL/NOT_READY depending on verified scope |

**Next:** GW01–GW05 private Gateway/WAF/TLS code, then Q01–Q02 policy and provider checks. Live `plan`/`apply` requires new human input at G07/B05/Q03.

References: [App Service Private Endpoint](https://learn.microsoft.com/en-us/azure/app-service/networking/private-endpoint); [Terraform Linux Web App](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_web_app); [Project 78-step runbook](78-step-construction-runbook.md).
