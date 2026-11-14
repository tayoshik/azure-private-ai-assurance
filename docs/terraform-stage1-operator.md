# Terraform Stage 1 — English Operator Runbook

**Release state:** SOURCE CREATED, TEXT CHECKS PASS; Terraform CLI syntax / provider schema / Azure live acceptance **NOT READY**. This runbook does not authorize a deploy.

## 1. Scope, design and deliverables

- Scope: DAG G05/G06, B01/B02/B04 **source definition**, N01/N02/N03/N05 **source definition**, Q01 *text-only preliminary regression*.
- Bootstrap is a standalone configuration root. Its initial state is local to the approved CI workspace; that state must be encrypted, access-controlled, backed up, and deliberately migrated per organizational procedure. **Never leave it on an unmanaged workstation or public GitHub**.
- Bootstrap provisions a distinct management VNet/subnet, Blob private endpoint, private DNS zone/link, a keyless/private state storage account, private container and scoped CI Blob Data Contributor assignment. The existence of those resources does *not* prove the CI network reaches them.
- Dev is a separate configuration root with an `azurerm` backend placeholder. `init` with an actual backend must be blocked until B05 verifies both DNS and network connectivity, scoped OIDC/RBAC and supported tooling.
- This slice only defines RG/VNet/subnets/DNS for the application workload. It does not implement N04 firewall/NSG/UDR or any PaaS resource.

## 2. Local WSL2 workflow (NO Azure credentials)

### Step 2.1 — Obtain files and record source SHA

```bash
set -Eeuo pipefail
git clone https://github.com/tayoshik/azure-private-ai-assurance.git
cd azure-private-ai-assurance
git rev-parse HEAD
find infra -type f \( -name '*.tf' -o -name '*.example' \) | sort
```

If already cloned, run `git pull --ff-only` after checking `git status --short`. **Expected**: Terraform files listed in the bootstrap and `dev` root. **If missing**: ensure the Stage 1 commit is present; do not fabricate source paths.

### Step 2.2 — Run the static source contracts and tests

```bash
python3 scripts/check_terraform_stage1.py
python3 -m unittest discover -s tests -p 'test_terraform_stage1.py' -v
```

**Expected**: `PASS_OFFLINE_TEXT_REVIEW_ONLY`, 14 tests `OK`, `terraform_cli_validation=NOT_EXECUTED`, `azure_live_passes=0`. **If FAIL**: inspect the path and missing property, correct the HCL, rerun and require two-person code review. **These tests do not compile HCL**.

### Step 2.3 — Verify exact toolchain without Azure login

```bash
command -v terraform || echo 'NOT_READY: Terraform CLI not available'
terraform version    # only when installed via organization-approved source
terraform fmt -check -recursive infra/
```

**Expected**: clean HCL formatting. If CLI is unavailable or `fmt` fails, record `NOT_READY` and execute an approved CI job. Do **not** treat Python contract checks as a substitute.

## 3. Controlled provider validation (approved CI, not WSL)

### Step 3.1 — Validate isolated bootstrap root

```bash
set -Eeuo pipefail
terraform -chdir=infra/bootstrap init -backend=false -input=false -no-color
terraform -chdir=infra/bootstrap validate -no-color
terraform -chdir=infra/bootstrap providers
```

**Preconditions**: approved Terraform binary hash, approved provider registry/mirror, exact version constraint reviewed at G03, CI identity limited to target subscription. `init -backend=false` does not authenticate or deploy, but downloads provider packages unless a trusted mirror is present. Save toolchain versions and provider lockfile in source control after independent review. **A successful `validate` establishes schema/syntax only; not configuration safety or Azure availability.**

### Step 3.2 — Validate dev root without remote backend access

```bash
terraform -chdir=infra/environments/dev init -backend=false -input=false -no-color
terraform -chdir=infra/environments/dev validate -no-color
terraform -chdir=infra/environments/dev providers
```

**Expected**: configuration validates without reading Azure resources. **If blocked**: record exact provider error and version; compare pinned schema, correct code, rerun static tests. Never call `az login` from the restricted workstation.

## 4. Explicit bootstrap and private-backend gates

### Step 4.1 — Approve inputs before any `plan`

Gather from secured sources, never commit to public GitHub: subscription and tenant, approved region, **management** and **workload** VNet CIDRs, approved PE subnet, CI principal **object ID**, certificate/DNS ownership, service resource names, recovery plan and independent reviewers.

Use `.tfvars.example` files as **nonworking samples**, not real values. The all-zero subscription and principal UUIDs are blocked by validations. IPAM overlap verification must use the signed corporate IPAM register; Terraform CIDR syntax alone does not prove nonoverlap.

### Step 4.2 — Bootstrap plan/apply, separately authorized

The bootstrap root deliberately uses local state. The following are *runbook commands*, not commands executed by this project:

```bash
# Approved private CI only, under explicit human authorization.
# Values are supplied by restricted CI; do NOT write real .tfvars to public source.
: "${SECURE_PLAN_DIR:?approved restricted artifact directory required}"
terraform -chdir=infra/bootstrap plan -input=false -no-color \
  -out="${SECURE_PLAN_DIR}/bootstrap.tfplan"
sha256sum "${SECURE_PLAN_DIR}/bootstrap.tfplan"
# STOP. Obtain independent reviews of plan+SHA, exact target, and rollout/rollback.
# Only a distinct authorized job may apply the exact reviewed plan.
```

**Before apply**: confirm management VNet will be reachable from the runner after creation (ExpressRoute/VPN/peering and DNS forwarding), and protect local bootstrap state. **Do not turn on public Blob access or account keys to bypass a failed private connection.**

### Step 4.3 — Verify B05 (private state readiness)

From an **approved network-connected CI runner** (not default WSL):

```bash
: "${STATE_BLOB_FQDN:?must be approved exact storage hostname}"
: "${EXPECTED_STATE_PE_IP:?must match NIC inventory}"
dig +short "$STATE_BLOB_FQDN" A
getent ahostsv4 "$STATE_BLOB_FQDN"
# Compare the final A record to exact EXPECTED_STATE_PE_IP and PE NIC inventory.
# Inspect account public access = Disabled; Shared Key = Disabled; PE = Approved.
# Use an approved workload-federated CI identity to exercise scoped Blob operations.
```

**Pass requires** the exact approved IP, PE subresource `blob`, scoped CI route, HTTPS/TLS, token authorization and Blob read/write appropriate to state role; include UTC time, runner identity, request correlation and sealed evidence. DNS resolving to *any* RFC1918 address is insufficient. 401/403/timeout **alone is never PASS**. If B05 is not satisfied: `NOT_READY`; stop before dev backend init/plan.

### Step 4.4 — Dev remote backend activation (after B05 only)

```bash
# Approved runner only; generate backend config from protected approved inputs.
: "${SECURE_BACKEND_HCL:?approved restricted backend config required}"
terraform -chdir=infra/environments/dev init -input=false -no-color \
  -backend-config="$SECURE_BACKEND_HCL"
terraform -chdir=infra/environments/dev validate -no-color
# Further plan requires separate G07 approval and policy/peer review.
```

`ARM_USE_OIDC=true`, `ARM_USE_AZUREAD=true`, client ID, tenant ID and subscription ID must come from the sanctioned CI identity flow. No saved credentials or state shall be uploaded to the public repository.

## 5. Verification mapping and troubleshooting

| Control / DAG | Evidence / expected result | If failure |
| --- | --- | --- |
| G05/G06 | Repo and module contracts; no secrets; exact HCL files | Correct source path/module references, rerun offline check |
| B01/B02 | Storage HTTPS, TLS1.2, Shared Key off, public access off, versioning, soft-delete and lock | Correct account attributes; require approved provider version |
| B04 | Separate management VNet/PE/zone/link and protected state account; no workload VNet dependency | Correct PE NIC/Private DNS link/route/association; do not open public access |
| B05 | Confirm actual private CI route/DNS/Blob access plus scoped OIDC; *not achievable offline* | `NOT_READY`; obtain network/runbook evidence and approvals |
| N01/N02 | Workload RG/VNet vs signed IPAM | Fix approved names/IPAM, don't change CIDRs unilaterally |
| N03 | Dedicated AppGW subnet delegation and App Service outbound delegation; PE subnet isolation | Reconcile supported feature/subnet delegation and NSG design |
| N05 | Canonical zones and VNet links; no cross-zone duplicates | Resolve central DNS ownership and forwarders before deployment |
| Q01 | `fmt`, `init -backend=false`, `validate`, static policy checks | `NOT_READY` if Terraform/provider unavailable |

## 6. Nonclaims, upcoming work and approvals

- Current source HCL: 18 files. Source lines can be audited; **no Terraform CLI** was installed in the authoring environment, so no Terraform init/validate was executed there.
- No approved resource group, vnet, storage account, endpoint or CI principal is asserted to exist.
- Not included yet: NSG/UDR, DNS Resolver, managed identity, Key Vault, OpenAI, Search, Cosmos, App Service, Application Gateway, diagnostics, Playwright. These remain `PLANNED` DAG nodes.
- Model and region selection, SKU/quota support and exact provider schema must be independently confirmed during G03/G07.
- Upcoming authoring slices can proceed without user action. The **first live CI plan** requires organization-approved target details, runner network, OIDC/RBAC and two reviewers.

### Official attribute references (version-specific verification targets)

- [Storage account v4.66](https://registry.terraform.io/providers/hashicorp/azurerm/4.66.0/docs/resources/storage_account)
- [Storage container v4.66](https://registry.terraform.io/providers/hashicorp/azurerm/4.66.0/docs/resources/storage_container)
- [Private Endpoint](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/private_endpoint)
- [Private Application Gateway](https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-private-deployment)
