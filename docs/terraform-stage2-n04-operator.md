# N04 — Private Subnet NSGs and Optional App Outbound Route: Operator Runbook

**Status: Code authored; NOT Terraform/provider-validated; NOT Azure deployed.**

## Source mapping

- DAG: N04 depends on N03 and G02; G03/G07 approvals are explicit gate conditions.
- Construction: Step 22 (policy), Step 24 (Gateway subnet), Step 25 (App integration subnet), Step 26 (PE subnet), Step 28 (Gateway NSG), Step 29 (egress), Step 56 (PE boundaries), Step 59/60 (inventory), Step 67 (path diagnosis).
- Example test IDs: AZ-T28-01..22, AZ-T29-01..22, AZ-T56-01..22, AZ-T67-01..22. Actual test ID contents are in the existing Phase3/5/6 English catalogues; this document **does not redefine** them.

## Safe network policy contract

1. Gateway subnet: authorized source CIDRs -> TCP443, AzureLoadBalancer -> health, deny other inbound; outbound to Web and data PE subnets TCP443, optional **approved** DNS/service CIDRs, deny all other outbound.
2. App Service outbound integration: allow data-PE TCP443, approved DNS/service CIDRs, deny other outbound. Inbound NSG rules do not provide App Service ingress restrictions.
3. Web inbound PE subnet: gateway subnet -> TCP443, optional approved private testers -> TCP443, deny other inbound. **Separate** from integration subnet; `private_endpoint_network_policies = "Enabled"`.
4. AI/data/Key Vault PE subnet: App integration and Gateway -> TCP443, deny other inbound. This alone is not RBAC; test identity separately.
5. Optional UDR: only on App integration subnet; `0.0.0.0/0 -> VirtualAppliance` with an approved private NVA/Firewall IP. Gateway subnet is left without a UDR in this slice.

**Hard stop:** A restrictive egress policy may disrupt Entra tokens, Key Vault certificate fetching, CRL/OCSP, package supply, monitoring, application boot, platform health and control traffic. A full signed dependency list + private runner test is required. The four `*_approved` flags default to FALSE; gateway/app NSG associations cannot be planned/applied unless explicitly approved.

## 1. Local WSL2 pre-flight (NO Azure authentication)

```bash
set -Eeuo pipefail
cd "$HOME/azure-private-ai-assurance"
git pull --ff-only
python3 scripts/check_terraform_stage1.py
python3 scripts/check_terraform_n04.py
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v
command -v terraform || echo 'NOT_READY: Terraform CLI not installed; provider validation cannot run'
```

## 2. Optional version-pinned Terraform check (only when approved toolchain exists)

```bash
set -Eeuo pipefail
terraform version
terraform -chdir=infra/environments/dev fmt -check -recursive
# Use only an approved provider mirror / dependency cache; no backend credentials here.
terraform -chdir=infra/environments/dev init -backend=false -input=false -lockfile=readonly
terraform -chdir=infra/environments/dev validate -no-color
# Inspect actual provider schema for azurerm_network_security_rule,
# azurerm_subnet_network_security_group_association, route_table and associations.
terraform -chdir=infra/environments/dev providers schema -json > /approved-restricted-artifacts/dev-provider-schema.json
```

`terraform validate` can check syntax/provider shape, but does not guarantee Azure API success. Provider version `=4.66.0` in this baseline is provisional and the exact lock/approval at G03 has not occurred.

## 3. Read-only network verification from approved Azure CI

Do **NOT** run `az login` from the fixed WSL workstation. Obtain target IDs from the signed restricted inventory; run only in a pre-authenticated least-privilege private CI runner.

```bash
set -Eeuo pipefail
: "${RESOURCE_GROUP:?approved target required}"
: "${VNET_NAME:?approved target required}"
: "${APPGW_NAME:?approved gateway required}"

az network vnet subnet list --resource-group "$RESOURCE_GROUP" \
  --vnet-name "$VNET_NAME" \
  --query '[].{id:id,name:name,nsg:networkSecurityGroup.id,routeTable:routeTable.id,delegations:delegations[].serviceName,pePolicies:privateEndpointNetworkPolicies}' -o json

az network nsg list --resource-group "$RESOURCE_GROUP" \
  --query '[].{id:id,name:name,securityRules:securityRules[].{name:name,direction:direction,access:access,priority:priority}}' -o json

az network application-gateway show --resource-group "$RESOURCE_GROUP" \
  --name "$APPGW_NAME" \
  --query '{id:id,frontendIPConfigurations:frontendIPConfigurations,sku:sku}' -o json
```

**Acceptance:** Compare exact resource IDs and approved CIDRs to IPAM; verify four independent NSG associations, correct priorities/effective rules; assert no unapproved public frontend, unexpected routes or broader sources. Validate PE NIC actual addresses, expected DNS and approved subresources separately. Never treat empty lists or request failures as PASS.

## 4. Approved private runner traffic and DNS tests

```bash
set -Eeuo pipefail
: "${APP_PRIVATE_FQDN:?approved FQDN required}"
: "${APP_EXPECTED_PE_IP:?approved PE NIC IP required}"
actual="$(dig +short "$APP_PRIVATE_FQDN" A | tail -n1)"
if [[ "$actual" != "$APP_EXPECTED_PE_IP" ]]; then
  echo "FAIL: DNS is not the approved Web PE IP" >&2
  exit 2
fi
curl --fail --silent --show-error --max-time 15 \
  --resolve "${APP_PRIVATE_FQDN}:443:${APP_EXPECTED_PE_IP}" \
  "https://${APP_PRIVATE_FQDN}/healthz"
```

The command is **not** valid acceptance evidence unless resource ownership, signed baseline, TLS/SNI, CI vantage point, route/NSG, backend health and logs are independently reviewed. Do not bypass certificate checks. A failed unauthorized test is also NOT_READY if the intended target cannot be proven to exist.

## 5. Drift/nonproduction plan (separate approved CI only)

```bash
# A saved plan is sensitive and must stay outside public GitHub.
: "${APPROVED_PLAN_PATH:?approved protected path required}"
terraform -chdir=infra/environments/dev plan -input=false -out="$APPROVED_PLAN_PATH"
sha256sum "$APPROVED_PLAN_PATH"
# STOP: two independent approvers must attest exact commit, plan digest,
# target resource IDs, feature state, egress allowlist, cost, rollback.
# No terraform apply is provided by this documentation workflow.
```

## Troubleshooting

| Symptom | Triage | Safe correction |
|---|---|---|
| Gateway backend Unhealthy | private DNS, PE NIC, NSG effective rule, SNI/Host, gateway feature | Fix source/host/probe; do not open public frontend |
| Private endpoint inaccessible | `private_endpoint_network_policies`, NIC IP, subnet NSG and route, RBAC | Correct scoped rules; verify source and identity separately |
| App token/monitor failures | egress deny, Entra/Monitor/CRL dependencies, route-all, Firewall DNS | Restore *reviewed* dependency rules; never widen to all Internet |
| CI state backend blocked | Bootstrap VNet/PE DNS, private CI reachability, OIDC Blob RBAC | Keep B05 NOT_READY until approved private path works |
| `plan` fails on precondition | G03/G07 or egress approval not established | Record NOT_READY; collect signed feature/dependency approvals |
| Terraform schema fails | Pinned azurerm schema, resource arguments, toolchain | Fix/upgrade only with reviewed provider version and new lock digest |

## Bootstrap P0 dependency review

`infra/bootstrap` intentionally uses **no self-hosted backend**. It defines management VNet, state Storage with public access and shared keys disabled, Blob PE, DNS and RBAC. The initial bootstrap state requires separately approved **restricted** custody on CI, with encryption, rollback and recovery. `infra/environments/dev` uses AzureRM remote backend only once the private runner can resolve the state Blob FQDN to the correct PE IP and authorize with OIDC + scoped Data Contributor. **A Storage container resource created by ARM does not alone prove Blob data-plane accessibility.**

The initial state handoff and any later backend migration are authorized change tasks—not actions performed by this offline test suite. Store state files, plans and real resource IDs out of the public repository.

## Authoritative references checked for N04 review

- https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-private-deployment
- https://learn.microsoft.com/en-us/azure/app-service/overview-vnet-integration
- https://learn.microsoft.com/en-us/azure/app-service/configure-vnet-integration-routing
- https://learn.microsoft.com/en-us/azure/private-link/disable-private-endpoint-network-policy
- https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet_network_security_group_association
