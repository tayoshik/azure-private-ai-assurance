# Command and Inspection Recipes — Turn 02

**Status:** Examples for approved environments, **not commands already run against Azure**. All variables are placeholders, and the approved subscription/resource IDs, CLI versions, provider schema and RBAC must be confirmed first. Only the `localtools`, `repo`, `secrets` and offline `terraform fmt` portions are suitable for unauthenticated fixed-terminal WSL execution; remote `az` commands are for **pre-authenticated, approved CI or portal-managed automation**. App/PE probes require an **approved internal runner**.

A recorded command with no actual output is a *procedure*, not evidence. Use `NOT_READY` when resource, approved baseline or trusted execution context is absent. Raw tokens, `tfstate`, binary plans, private key material and unredacted logs must never be committed to public GitHub.

## boundary

**Read-only document inspection (WSL):**
```bash
set -Eeuo pipefail
: "${ADR_FILE:?Set path to approved ADR-001}"
test -s "$ADR_FILE"
sha256sum "$ADR_FILE"
# Reviewer still checks exact client/gateway/application, management, ID, monitoring boundaries.
```
**Pass:** verified approval and scope in ADR. **Fail/NotReady:** hash alone cannot establish approval.

## routes

**Approved internal CI or network-admin runner:**
```bash
set -Eeuo pipefail
: "${RESOURCE_GROUP:?}"; : "${VNET_NAME:?}"
az network vnet show -g "$RESOURCE_GROUP" -n "$VNET_NAME" --query '{id:id,address:addressSpace.addressPrefixes,subnets:subnets[].addressPrefix}' -o json
# Separately cross-check exported values with approved IPAM and corporate/VPN routes.
```
**Pass:** no overlapping CIDRs and documented resolver/route ownership. **If failed:** do not edit routes without change approval.

## review

```bash
set -Eeuo pipefail
: "${BASELINE_FILE:?}"
test -s "$BASELINE_FILE"
sha256sum "$BASELINE_FILE"
# Nonmechanical: verify the matching approved revision, signer, data-classification/RTO/RPO fields.
```
**Pass:** reviewed design and data owner approval; file existence is insufficient.

## localtools

```bash
set -Eeuo pipefail
uname -a
git --version
python3 --version
command -v terraform >/dev/null && terraform version || echo 'NOT_READY: Terraform unavailable'
command -v jq >/dev/null && jq --version || echo 'NOT_READY: jq unavailable'
command -v dig >/dev/null && dig -v 2>&1 || echo 'NOT_READY: dig unavailable'
```
**Pass:** binaries match pinned, approved version manifest. **No Azure login**.

## features

**Approved Azure management plane (read-only):**
```bash
: "${SUBSCRIPTION_ID:?}"
az feature show --namespace Microsoft.Network --name EnableApplicationGatewayNetworkIsolation --query '{state:properties.state,name:name}' -o json
# Verify current feature/support policy for this subscription and deployment mode.
```
**Pass:** feature and deployment mode prerequisites confirmed; do not register/alter here.

## repo

```bash
set -Eeuo pipefail
git rev-parse --show-toplevel
git status --short
git ls-files | sed -n '1,100p'
# Branch protection and reviewer independence require GitHub repository settings evidence.
```
**Pass:** source reproducible and protected under approved policy.

## secrets

```bash
set -Eeuo pipefail
git ls-files | grep -E '(^|/)(\.env$|terraform\.tfstate|[^/]+\.tfplan$|[^/]+\.pfx$|[^/]+\.pem$)' && {
  echo 'FAIL: forbidden tracked file'; exit 1;
} || true
# Execute approved gitleaks/secret scanner on all tracked files AND reachable history.
```
**Pass:** no forbidden tracked paths and a real secret scan has run; `grep` is not secret detection.

## state

**Approved CI read-only:**
```bash
: "${STATE_RESOURCE_GROUP:?}"; : "${STATE_ACCOUNT:?}"
az storage account show -g "$STATE_RESOURCE_GROUP" -n "$STATE_ACCOUNT" \
  --query '{id:id,publicNetworkAccess:publicNetworkAccess,minimumTlsVersion:minimumTlsVersion,allowSharedKeyAccess:allowSharedKeyAccess}' -o json
# Check versioning, retention, role assignments and DNS via separate evidence.
```
**Pass:** approved state protections and private CI connectivity; no state payload ever printed.

## terraform

**Offline inspection on approved source checkout (some commands need local plugins):**
```bash
set -Eeuo pipefail
: "${TF_ROOT:?}"
terraform -chdir="$TF_ROOT" fmt -check -recursive
# validate requires prior provider init; run only in a pinned, allowed build environment.
# terraform -chdir="$TF_ROOT" validate
# terraform -chdir="$TF_ROOT" providers
```
**Pass:** static checks and pinned toolchain in validated CI. `terraform test` may create cloud resources depending on run blocks; it must never be assumed offline by name alone.

## negative

**Only with known, existing, approved target:**
```bash
: "${EXTERNAL_TARGET_FQDN:?}"
getent ahostsv4 "$EXTERNAL_TARGET_FQDN" || true
curl -sS --connect-timeout 5 --max-time 12 -o /dev/null -w 'status=%{http_code} peer=%{remote_ip} verify=%{ssl_verify_result}\n' \
  "https://${EXTERNAL_TARGET_FQDN}/" || true
# Must correlate with Azure PNA/Public IP/PE inventory and known target existence.
```
**Pass:** control-plane confirms private-only and observation is consistent. A timeout, DNS failure, 403 or 404 on its own is **NOT** pass evidence.

## internal

**Approved VNet runner:**
```bash
: "${INTERNAL_APP_FQDN:?}"
getent ahostsv4 "$INTERNAL_APP_FQDN"
curl --fail-with-body --connect-timeout 10 --max-time 25 \
  -sS -o /dev/null -w 'HTTP=%{http_code} TLS_verify=%{ssl_verify_result} peer=%{remote_ip}\n' \
  "https://${INTERNAL_APP_FQDN}/healthz"
```
**Pass:** 200, TLS verified, expected PE IP, recorded backend health. Do not use `-k`.

## node

```bash
set -Eeuo pipefail
: "${TEST_ROOT:?}"
cd "$TEST_ROOT"
node --version
npm --version
npm ci
npx playwright test --list  # inventory only, NOT executed E2E
```
**Pass:** lockfile deterministic; test inventory matches intended suites. Do not claim live pass from `--list`.

## policy

```bash
set -Eeuo pipefail
: "${PLAN_JSON:?}"; : "${POLICY_DIR:?}"
test -s "$PLAN_JSON"
# Example only: policy implementation must be versioned and approved.
conftest test --policy "$POLICY_DIR" "$PLAN_JSON"
```
**Pass:** safe fixture succeeds and bad PNA/NSG fixture fails before any apply. Plan JSON may contain secrets; keep it in protected CI storage.

## plan

**Approved CI after init with reviewed backend and identity:**
```bash
set -Eeuo pipefail
: "${TF_ROOT:?}"; : "${SECURE_PLAN_PATH:?}"
# A saved plan is sensitive; path must be protected, never inside this public repo.
terraform -chdir="$TF_ROOT" plan -input=false -no-color -out="$SECURE_PLAN_PATH"
sha256sum "$SECURE_PLAN_PATH"
# Bind digest + exact commit + resource scope to two independent human reviews.
```
**Pass:** independent approvals recorded. No `terraform apply` in this recipe.

## subnets

```bash
: "${RESOURCE_GROUP:?}"; : "${VNET_NAME:?}"
az network vnet subnet list -g "$RESOURCE_GROUP" --vnet-name "$VNET_NAME" \
  --query '[].{name:name,ip:addressPrefix,delegations:delegations[].serviceName}' -o json
```
**Pass:** intended delegation and dedicated subnet verified against approved CIDR plan. A subnet existing does not prove its scale or isolation.

## pe

```bash
: "${RESOURCE_GROUP:?}"
az network private-endpoint list -g "$RESOURCE_GROUP" \
  --query '[].{id:id,subnet:subnet.id,state:privateLinkServiceConnections[].privateLinkServiceConnectionState.status,groups:privateLinkServiceConnections[].groupIds}' -o json
# Retrieve PE NIC/private IP and DNS zone-group data separately; compare to approved mapping.
```
**Pass:** all required PEs Approved with exact group/subnet/IP/DNS. Do not infer PE IP from a single arbitrary list index.

## dns

**Approved internal runner; compare every result to approved private IP list:**
```bash
set -Eeuo pipefail
: "${SERVICE_FQDN:?}"
dig +time=3 +tries=1 "$SERVICE_FQDN" CNAME
dig +time=3 +tries=1 "$SERVICE_FQDN" A
getent ahostsv4 "$SERVICE_FQDN" || true
```
**Pass:** final A record equals expected PE NIC IP; split-horizon and service hostname TLS checked. Output alone never establishes correct zone group.

## nsg

**Read-only resource scope, authorized subscription:**
```bash
: "${RESOURCE_GROUP:?}"
az network nsg list -g "$RESOURCE_GROUP" --query '[].{name:name,id:id,securityRules:securityRules}' -o json
# Compare effective rules, routes and PE network policy; test from permitted/unpermitted source.
```
**Pass:** only approved sources/ports; control-plane plus actual path tests. Avoid editing NSG to prove a negative in production.

## monitor

```bash
: "${RESOURCE_ID:?}"
az monitor diagnostic-settings list --resource "$RESOURCE_ID" -o json
# After checking workspace/table mode, query a bounded correlation ID and verify log arrival.
```
**Pass:** expected supported categories and bounded real events; availability of a diagnostic setting alone does not prove ingestion.

## paas

```bash
: "${RESOURCE_GROUP:?}"
az resource list -g "$RESOURCE_GROUP" \
  --query '[].{name:name,type:type,id:id,location:location}' -o json
# Fetch each approved service's detailed PNA/SKU/auth/deployment attributes by stable resource ID.
```
**Pass:** exact resource IDs and verified settings, not a guessed name. Property paths differ by service and API version.

## vault

```bash
: "${VAULT_NAME:?}"
az keyvault show --name "$VAULT_NAME" --query '{id:id,publicNetworkAccess:properties.publicNetworkAccess,enableRbacAuthorization:properties.enableRbacAuthorization}' -o json
# Do NOT print secret values. Inspect certificate metadata and access decisions separately.
```
**Pass:** private access/RBAC/cert expiry proven by supported configuration and tests.

## deploy

**Pre-deployment read-only check; actual deploy is a separately approved job:**
```bash
: "${APP_NAME:?}"; : "${RESOURCE_GROUP:?}"
az webapp show -g "$RESOURCE_GROUP" -n "$APP_NAME" \
  --query '{name:name,id:id,defaultHostName:defaultHostName,publicNetworkAccess:publicNetworkAccess}' -o json
# Verify internal runner SCM and ACR access before authorizing any publish job.
```
**Pass:** approved private software delivery path demonstrated.

## identity

```bash
: "${APP_NAME:?}"; : "${RESOURCE_GROUP:?}"
az webapp identity show -g "$RESOURCE_GROUP" -n "$APP_NAME" -o json
# Independently inspect approved data-plane role assignment for OpenAI/Search/Cosmos.
```
**Pass:** correct principal + scope and paired authorized/unauthorized API checks, with no embedded API keys.

## app

```bash
: "${APP_NAME:?}"; : "${RESOURCE_GROUP:?}"
az webapp show -g "$RESOURCE_GROUP" -n "$APP_NAME" \
  --query '{id:id,httpsOnly:httpsOnly,publicNetworkAccess:publicNetworkAccess,enabled:enabled}' -o json
```
**Pass:** declared web hardening plus runtime TLS/health; inspect basic publishing independently.

## appgw

```bash
: "${GATEWAY_NAME:?}"; : "${RESOURCE_GROUP:?}"
az network application-gateway show -g "$RESOURCE_GROUP" -n "$GATEWAY_NAME" \
  --query '{id:id,frontendIPConfigurations:frontendIPConfigurations,backendAddressPools:backendAddressPools}' -o json
# Confirm zero public frontend references; configuration output may contain internal IDs.
```
**Pass:** only private frontend and healthy backend observed.

## tls

**Approved internal runner only:**
```bash
: "${INTERNAL_APP_FQDN:?}"
# Use explicit host as SNI, do not skip TLS validation:
openssl s_client -connect "${INTERNAL_APP_FQDN}:443" -servername "$INTERNAL_APP_FQDN" -verify_return_error </dev/null 2>&1 | tail -25
```
**Pass:** valid chain and SAN hostname corroborated by `curl` without `-k`; inspect certificate rotation separately.

## waf

**Inspect WAF logs first. Do not transmit attack strings without explicit approved test scope.**
```kusto
AGWFirewallLogs
| where TimeGenerated > ago(1h)
| where RequestUri has "tid="
| project TimeGenerated, Hostname, RequestUri, RuleId, Action, TransactionId
| order by TimeGenerated desc
```
**Pass:** benign test request with a bound `tid`, expected rule/action and firewall/access correlation. Table names vary by workspace mode; never infer block just from HTTP 403.

## apply

**CONTROLLED CHANGE, NOT AUTOMATED BY THESE DOCUMENTS.** An authorized, isolated CI job must verify exact reviewed `plan` digest, target scope and two independent approvals. Only then may its separately approved job execute the reviewed plan. Do not put `terraform apply` inside any public convenience script.

## inventory

**Approved CI read-only Resource Graph example:**
```bash
: "${SUBSCRIPTION_ID:?}"
az graph query -q "Resources | where subscriptionId =~ '${SUBSCRIPTION_ID}' | project id, name, type, location | limit 100" -o json
# Query is illustrative; use approved asset ID allowlist and pagination for actual completeness.
```
**Pass:** no unapproved IDs; dynamic inventory is reconciled to source baseline. Avoid interpolating untrusted input into queries.

## dr

```bash
set -Eeuo pipefail
: "${DR_EXERCISE_RECORD:?}"
test -s "$DR_EXERCISE_RECORD"
sha256sum "$DR_EXERCISE_RECORD"
# An independent reviewer must inspect actual backup/reindex logs and measured RTO/RPO.
```
**Pass:** approved nonproduction restore/reindex succeeded within agreed objectives; artifact presence is only an input.

## perf

**Do not run any load test until target, rate cap, window, observers and stop conditions are approved.** An isolated `k6` or Azure Load Testing run must retain latency distribution, error rate, scaling and SLO comparison. `npx playwright test` is not a substitute for load testing.

## ci

```bash
# This reads a workflow's source only; not proof that it executed.
: "${WORKFLOW_PATH:?}"
python3 - <<'PY'
import os,pathlib
p=pathlib.Path(os.environ['WORKFLOW_PATH'])
if not p.is_file(): raise SystemExit('NOT_READY: workflow file missing')
print('workflow bytes:',p.stat().st_size)
PY
```
**Pass:** workflow *execution* shows failures block subsequent stages, approved identities and independent reviewers.

## handover

```bash
: "${RELEASE_MANIFEST:?}"
test -s "$RELEASE_MANIFEST" && sha256sum "$RELEASE_MANIFEST"
# Compare all referenced evidence to approved scope, digest, signers and release tag.
```
**Pass:** validated signatures, referenced assets and independent handover acceptance; a manifest file alone does not pass.

## go

**No command automatically authorizes production.** Governance board accepts an approved release record only with exact scope, version/commit, closed critical risks, verified environment tests, remediation tickets and rollback readiness. Stage 11 result: **all 1,716 live cases NOT_READY; live PASS=0; release NO-GO**.

## Troubleshooting and exit codes

- CLI nonzero with missing login, policy, RBAC or endpoint: **NOT_READY** (no evidence of the intended control), never silently ignore.
- A control known to be deployed that demonstrably violates approved baseline: **FAIL**.
- Correct configuration plus trusted independent operation and evidence: candidate for **REVIEW_REQUIRED**, not self-certified live PASS.
- Sensitive output discovered in CI/repo: stop publication, revoke credentials, sanitize, audit repository history and document remediation.