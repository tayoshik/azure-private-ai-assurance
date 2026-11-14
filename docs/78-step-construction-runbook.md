# 78-Step Azure Private AI Construction and Assurance Runbook

**Version:** Turn 02 English design translation (2026-11-14) · **Status:** DRAFT / NOT DEPLOYED · **Release:** NO-GO  
**Source:** Reviewed Japanese runbook `Azure_閉域AI基盤_構築検証手順書_20261110.md`, Sections 0–7, and English Stage 1 repository baseline.  
**Scope:** One-region private application data plane, with separately approved control-plane, identity, monitoring and software-supply-chain dependencies.

> **Crucial limitation:** This is a reviewed *procedure*, not evidence of provisioned Azure resources, passed test cases, FISC certification, or a usable Terraform module. No Azure command shown in these pages has been executed on the target subscription. All 1,716 test IDs remain `NOT_READY` for live acceptance.

## Preconditions and safety

- Confirm subscription, tenant, region, models/SKUs, IPAM, resource naming, private FQDN, certificates, retention/RTO/RPO, approved identities, RBAC and two independent reviewers.
- Fixed WSL2 workstation: source editing and offline checks; **do not rely on interactive `az login`**. Azure read-only queries run on an approved federated CI runner or approved portal. VNet tests run on a private test VM/runner.
- All names in command recipes are placeholders. **Do not execute** until the organization has approved substituted values, service limits, the pinned AzureRM schema and test scope.
- The backend bootstrap, plan approval, apply, WAF simulation, load testing, recovery and production changes are distinct explicitly approved operations. No apply or live attack is bundled in this publication.
- Prior Stage 9 synthetic checks (330/330), Stage 10 unit checks (18/18), Stage 11 unit checks (21/21) relate to tooling; Azure live passes: **0**.
- Plan, state, identity tokens, secret values, raw application traces and unredacted evidence are **not** for this public repository.

## How to use this runbook

Each step has an action, independent acceptance observation, expected evidence, failure handling, an index into read-only/controlled command recipes, and its 22 associated test IDs. Full 1,716-test case translations are separate Turn 03–07 deliverables. A documented check is not a passed check; missing implementation/baselines/evidence is `NOT_READY`.

## Architecture summary

`Corporate users → approved ER/VPN → private-only Application Gateway WAF_v2 → App Service inbound Private Endpoint → Linux App Service → outbound VNet integration → Azure OpenAI / AI Search / Cosmos DB private endpoints`. Key Vault, DNS, secure state backend, monitoring and internal runners occupy scoped networks; management/identity/control dependencies have separate routing.

## Phase 1: Steps 01–10 — Governance, private boundary and execution environments

### Step 01 — Define the private boundary

- **Action:** Record separate business, management, identity, monitoring and supply-chain planes; explicitly rule out public application ingress.
- **Verification / pass criteria:** ADR-001 describes permitted paths, exception flows and accountable approvers.
- **Evidence to retain:** ADR-001 and approved data-flow drawing.
- **If blocked or failed:** Missing boundary definition: keep NOT_READY; escalate to architecture review.
- **Related test IDs:** `AZ-T01-01` through `AZ-T01-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `boundary`](command-recipes.md#boundary). Read-only unless explicitly called out as a planned controlled change.

### Step 02 — Choose the client access method

- **Action:** Select ExpressRoute or approved S2S/P2S VPN; resolve routes and internal DNS for operators and users.
- **Verification / pass criteria:** Every client CIDR and VPN/ER DNS forward path has an approved owner.
- **Evidence to retain:** Network decision record and IPAM export.
- **If blocked or failed:** Routing/DNS ambiguity: hold network build and resolve overlaps.
- **Related test IDs:** `AZ-T02-01` through `AZ-T02-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `routes`](command-recipes.md#routes). Read-only unless explicitly called out as a planned controlled change.

### Step 03 — Approve security and regulatory requirements

- **Action:** Agree data classification, residency, availability, RTO/RPO, retention, keys, PIM and change controls.
- **Verification / pass criteria:** Signed control mapping, required retention and exception register exist.
- **Evidence to retain:** Approved security requirements matrix.
- **If blocked or failed:** Missing owner or policy: mark the gate NOT_READY.
- **Related test IDs:** `AZ-T03-01` through `AZ-T03-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `review`](command-recipes.md#review). Read-only unless explicitly called out as a planned controlled change.

### Step 04 — Validate services and regional quotas

- **Action:** Confirm selected region supports Azure OpenAI model/deployment capacity, Search SKU, Cosmos DB and WAF_v2.
- **Verification / pass criteria:** A service/SKU/region matrix records current approvals and quotas.
- **Evidence to retain:** Regional availability and quota exports.
- **If blocked or failed:** Unavailable SKU or quota: redesign before Terraform planning.
- **Related test IDs:** `AZ-T04-01` through `AZ-T04-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `review`](command-recipes.md#review). Read-only unless explicitly called out as a planned controlled change.

### Step 05 — Define AI data handling

- **Action:** Classify prompts and outputs, logging, abuse monitoring, model versions and residency obligations.
- **Verification / pass criteria:** The data-flow diagram covers prompts, responses and diagnostic capture.
- **Evidence to retain:** Approved AI/data flow and handling policy.
- **If blocked or failed:** Unapproved payload retention: do not deploy application.
- **Related test IDs:** `AZ-T05-01` through `AZ-T05-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `review`](command-recipes.md#review). Read-only unless explicitly called out as a planned controlled change.

### Step 06 — Prepare workstation tooling

- **Action:** On the fixed WSL2 workstation verify approved Git, jq, DNS tools and Terraform versions; no Azure authentication required.
- **Verification / pass criteria:** Tool versions and package provenance have been captured.
- **Evidence to retain:** Read-only version output and distribution manifest.
- **If blocked or failed:** Unapproved packages: replace from organization-approved source.
- **Related test IDs:** `AZ-T06-01` through `AZ-T06-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `localtools`](command-recipes.md#localtools). Read-only unless explicitly called out as a planned controlled change.

### Step 07 — Assign identity and execution paths

- **Action:** Keep local WSL editing separate from portal/Zscaler and federated self-hosted CI Azure operations.
- **Verification / pass criteria:** Human, CI and test identities have distinct least-privilege scopes.
- **Evidence to retain:** Identity/runner access matrix and approval.
- **If blocked or failed:** CLI unavailable on workstation: use approved CI, never bypass controls.
- **Related test IDs:** `AZ-T07-01` through `AZ-T07-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `review`](command-recipes.md#review). Read-only unless explicitly called out as a planned controlled change.

### Step 08 — Check private App Gateway feature enablement

- **Action:** Verify the targeted subscription has applicable network-isolation support and prerequisite registration through portal/approved CI.
- **Verification / pass criteria:** Prerequisite availability is confirmed for the supported deployment mode.
- **Evidence to retain:** Portal feature-state export with timestamp.
- **If blocked or failed:** Not registered: request authorized enablement; hold deployment.
- **Related test IDs:** `AZ-T08-01` through `AZ-T08-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `features`](command-recipes.md#features). Read-only unless explicitly called out as a planned controlled change.

### Step 09 — Initialize the repository structure

- **Action:** Separate bootstrap, infra, policies, external/internal tests, scripts, docs and evidence references.
- **Verification / pass criteria:** Protected main branch and independent review are recorded.
- **Evidence to retain:** Repository tree and branch rules.
- **If blocked or failed:** Missing protection: stop production promotion.
- **Related test IDs:** `AZ-T09-01` through `AZ-T09-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `repo`](command-recipes.md#repo). Read-only unless explicitly called out as a planned controlled change.

### Step 10 — Exclude sensitive material

- **Action:** Ignore state, plan, credentials, private keys, reports with tokens and build artifacts; run secret scanning.
- **Verification / pass criteria:** Git history and files contain no secrets or forbidden states.
- **Evidence to retain:** Sanitized scan findings and .gitignore review.
- **If blocked or failed:** Any leaked token: revoke, rotate, purge and investigate.
- **Related test IDs:** `AZ-T10-01` through `AZ-T10-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `secrets`](command-recipes.md#secrets). Read-only unless explicitly called out as a planned controlled change.

## Phase 2: Steps 11–20 — Terraform backend and verification strategy

### Step 11 — Separate Terraform backend bootstrap

- **Action:** Manage state RG, Storage Account and container independently from workload state.
- **Verification / pass criteria:** State backend ownership, recovery and teardown safeguards are documented.
- **Evidence to retain:** Bootstrap IaC and resource inventory.
- **If blocked or failed:** Circular backend dependency: split bootstrap from workload.
- **Related test IDs:** `AZ-T11-01` through `AZ-T11-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `state`](command-recipes.md#state). Read-only unless explicitly called out as a planned controlled change.

### Step 12 — Protect state storage

- **Action:** Enforce TLS, versioning, soft delete, deny public blob, scoped Blob data RBAC and logging.
- **Verification / pass criteria:** Approved storage protections match policy.
- **Evidence to retain:** Storage config export and RBAC review.
- **If blocked or failed:** Missing protection: deny workload initialization.
- **Related test IDs:** `AZ-T12-01` through `AZ-T12-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `state`](command-recipes.md#state). Read-only unless explicitly called out as a planned controlled change.

### Step 13 — Connect CI to state over Private Link

- **Action:** Provision approved Blob private endpoint and DNS before closing storage public network.
- **Verification / pass criteria:** Runner resolves Blob normally to a scoped private address and accesses port 443.
- **Evidence to retain:** CI DNS results, route evidence, endpoint approval.
- **If blocked or failed:** DNS failure or lockout: restore approved private route, not a public bypass.
- **Related test IDs:** `AZ-T13-01` through `AZ-T13-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `dns`](command-recipes.md#dns). Read-only unless explicitly called out as a planned controlled change.

### Step 14 — Pin Terraform and provider versions

- **Action:** Pin reviewed Terraform CLI and azurerm provider exactly, commit the provider lock file.
- **Verification / pass criteria:** CLI/provider version and lock digests match approved manifest.
- **Evidence to retain:** terraform version, lockfile and registry provenance.
- **If blocked or failed:** Version drift: re-run schema and plan review.
- **Related test IDs:** `AZ-T14-01` through `AZ-T14-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `terraform`](command-recipes.md#terraform). Read-only unless explicitly called out as a planned controlled change.

### Step 15 — Configure backend workload identity

- **Action:** Use Entra/OIDC and minimum Blob Data Contributor assignment for remote state; avoid shared keys.
- **Verification / pass criteria:** Authorized CI init succeeds without a local state file; auth scope is reviewed.
- **Evidence to retain:** Redacted init log, role assignment and remote object.
- **If blocked or failed:** Missing OIDC/Blob role: NOT_READY; never embed credentials.
- **Related test IDs:** `AZ-T15-01` through `AZ-T15-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `terraform`](command-recipes.md#terraform). Read-only unless explicitly called out as a planned controlled change.

### Step 16 — Define independent IaC gates

- **Action:** Use fmt, validate, TFLint/Checkov, unit checks and policy-over-plan in independent jobs.
- **Verification / pass criteria:** Invalid configuration fails before plan/apply approval; tests are reproducible.
- **Evidence to retain:** CI stage logs and pinned tool config.
- **If blocked or failed:** Weak or bypassed gate: block subsequent jobs.
- **Related test IDs:** `AZ-T16-01` through `AZ-T16-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `terraform`](command-recipes.md#terraform). Read-only unless explicitly called out as a planned controlled change.

### Step 17 — Protect against false green in red tests

- **Action:** Require the target to exist before interpreting failure-to-connect as an isolation success.
- **Verification / pass criteria:** Unprovisioned resource yields NOT_READY rather than PASS.
- **Evidence to retain:** Provisioned resource inventory plus negative result.
- **If blocked or failed:** No inventory: rerun only after the target is verified.
- **Related test IDs:** `AZ-T17-01` through `AZ-T17-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `negative`](command-recipes.md#negative). Read-only unless explicitly called out as a planned controlled change.

### Step 18 — Create external exposure tests

- **Action:** Combine Azure public-network configuration, DNS and external vantage-point observations.
- **Verification / pass criteria:** No public ingress or unapproved endpoint is present; a lone HTTP 403 is insufficient.
- **Evidence to retain:** PNA/public IP inventory plus external observations.
- **If blocked or failed:** Exposure findings: classify and resolve before acceptance.
- **Related test IDs:** `AZ-T18-01` through `AZ-T18-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `negative`](command-recipes.md#negative). Read-only unless explicitly called out as a planned controlled change.

### Step 19 — Create internal positive tests

- **Action:** Use an approved VNet runner for internal FQDN, TLS, auth and dependency tests.
- **Verification / pass criteria:** DNS maps to approved PE IP; private HTTPS and dependency checks succeed.
- **Evidence to retain:** Runner logs, DNS, TLS and application response.
- **If blocked or failed:** Private runner unavailable: NOT_READY, not PASS.
- **Related test IDs:** `AZ-T19-01` through `AZ-T19-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `internal`](command-recipes.md#internal). Read-only unless explicitly called out as a planned controlled change.

### Step 20 — Initialize Playwright test projects

- **Action:** Pin Node, Playwright and lockfile; define external/internal suites with JUnit and trace retention.
- **Verification / pass criteria:** npm ci and test listing are reproducible without executing live tests.
- **Evidence to retain:** Dependency lock, test listing and config.
- **If blocked or failed:** Missing app route/auth adaptor: mark tests blocked.
- **Related test IDs:** `AZ-T20-01` through `AZ-T20-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `node`](command-recipes.md#node). Read-only unless explicitly called out as a planned controlled change.

## Phase 3: Steps 21–32 — Network, DNS and observability

### Step 21 — Approve nonoverlapping address plan

- **Action:** Cross-check office, hub, VPN, DR, VNet and future subnet CIDRs against IPAM.
- **Verification / pass criteria:** No overlapped networks and all CIDRs have assigned purpose.
- **Evidence to retain:** Approved IPAM export and conflict report.
- **If blocked or failed:** Address overlap: redesign before resource creation.
- **Related test IDs:** `AZ-T21-01` through `AZ-T21-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `routes`](command-recipes.md#routes). Read-only unless explicitly called out as a planned controlled change.

### Step 22 — Author preventive Azure policies

- **Action:** Define policy on public ingress/PNA, weak auth, tags, TLS and diagnostic settings, with reviewed exceptions.
- **Verification / pass criteria:** Policy tests reject forbidden examples before deployment; audit-to-deny rollout approved.
- **Evidence to retain:** Policy assignments and exception registry.
- **If blocked or failed:** Policy conflict or wrong scope: hold enforcement.
- **Related test IDs:** `AZ-T22-01` through `AZ-T22-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `policy`](command-recipes.md#policy). Read-only unless explicitly called out as a planned controlled change.

### Step 23 — Define RG/VNet in Terraform

- **Action:** Create resource groups and network with approved tags, names, locks and IPAM-aligned ranges.
- **Verification / pass criteria:** Plan matches reviewable inventory and naming policy.
- **Evidence to retain:** Terraform plan JSON, peer review and IPAM match.
- **If blocked or failed:** Unexpected public resource or route: reject plan.
- **Related test IDs:** `AZ-T23-01` through `AZ-T23-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `plan`](command-recipes.md#plan). Read-only unless explicitly called out as a planned controlled change.

### Step 24 — Allocate private App Gateway subnet

- **Action:** Reserve dedicated capacity and apply required delegation for the supported private-deployment model.
- **Verification / pass criteria:** No unrelated resources, adequate CIDR and approved delegation.
- **Evidence to retain:** Subnet config, delegation proof and version-specific guidance.
- **If blocked or failed:** Missing delegation or capacity: hold AppGW deployment.
- **Related test IDs:** `AZ-T24-01` through `AZ-T24-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `subnets`](command-recipes.md#subnets). Read-only unless explicitly called out as a planned controlled change.

### Step 25 — Allocate App Service outbound subnet

- **Action:** Delegate outbound integration subnet to Microsoft.Web/serverFarms and separate it from web PE.
- **Verification / pass criteria:** Subnet is independently dedicated and sized per app scale requirements.
- **Evidence to retain:** Subnet delegation and app integration settings.
- **If blocked or failed:** Outbound integration subnet reused for PE: redesign.
- **Related test IDs:** `AZ-T25-01` through `AZ-T25-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `subnets`](command-recipes.md#subnets). Read-only unless explicitly called out as a planned controlled change.

### Step 26 — Allocate private endpoint subnets

- **Action:** Zone web ingress, AI/data, vault and backend PE; configure NSG/UDR support per approved policy.
- **Verification / pass criteria:** Each PE has intended subnet and correct network-policy setting.
- **Evidence to retain:** PE/NSG/route inventory and subnet config.
- **If blocked or failed:** Misplaced PE or NSG not evaluated: correct subnet policy.
- **Related test IDs:** `AZ-T26-01` through `AZ-T26-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `pe`](command-recipes.md#pe). Read-only unless explicitly called out as a planned controlled change.

### Step 27 — Design DNS resolver connectivity

- **Action:** Provision resolver inbound/outbound delegated subnets and conditional forwarding when on-premises DNS is required.
- **Verification / pass criteria:** Approved DNS paths work from corporate and VNet clients.
- **Evidence to retain:** Resolver config and conditional-forwarder tests.
- **If blocked or failed:** Split-horizon inconsistency: correct forwarders and links.
- **Related test IDs:** `AZ-T27-01` through `AZ-T27-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `dns`](command-recipes.md#dns). Read-only unless explicitly called out as a planned controlled change.

### Step 28 — Enforce App Gateway network rules

- **Action:** Allow approved corporate HTTPS and applicable Azure platform traffic for the selected private deployment; do not blindly copy legacy rules.
- **Verification / pass criteria:** Provisioning/probes healthy with minimum documented NSG exceptions.
- **Evidence to retain:** Effective NSG rules and AppGW health evidence.
- **If blocked or failed:** Required platform traffic denied: review deployment mode.
- **Related test IDs:** `AZ-T28-01` through `AZ-T28-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `nsg`](command-recipes.md#nsg). Read-only unless explicitly called out as a planned controlled change.

### Step 29 — Control application egress

- **Action:** Plan outbound NSG/UDR/firewall to identity, monitoring, certificate checks, and private services.
- **Verification / pass criteria:** Allowlist covers required dependencies and unauthorized egress is denied.
- **Evidence to retain:** Approved egress matrix and flow observations.
- **If blocked or failed:** Auth/monitor breaks: isolate missing dependency before editing deny rules.
- **Related test IDs:** `AZ-T29-01` through `AZ-T29-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `nsg`](command-recipes.md#nsg). Read-only unless explicitly called out as a planned controlled change.

### Step 30 — Link private DNS zones

- **Action:** Manage App Service, OpenAI, Search, Cosmos and Vault PE DNS zones and VNet links centrally.
- **Verification / pass criteria:** Canonical service FQDNs resolve to intended private IPs on approved networks.
- **Evidence to retain:** Private DNS zone/record/link inventory.
- **If blocked or failed:** Duplicate zones or wrong A records: remediate at DNS authority.
- **Related test IDs:** `AZ-T30-01` through `AZ-T30-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `dns`](command-recipes.md#dns). Read-only unless explicitly called out as a planned controlled change.

### Step 31 — Define Azure Monitor Private Link path

- **Action:** Where required, model AMPLS, private endpoints and DNS plus approved ingestion/query dependencies.
- **Verification / pass criteria:** Metrics/log ingress and query work over approved paths.
- **Evidence to retain:** AMPLS endpoints, DNS checks and test log.
- **If blocked or failed:** Log loss: inspect ingestion reachability and workspace mode.
- **Related test IDs:** `AZ-T31-01` through `AZ-T31-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `monitor`](command-recipes.md#monitor). Read-only unless explicitly called out as a planned controlled change.

### Step 32 — Provision observability baseline

- **Action:** Enable Log Analytics, App Insights, diagnostic settings, VNet Flow Logs and alerts with approved retention.
- **Verification / pass criteria:** Supported log types arrive and ownership, retention and costs approved.
- **Evidence to retain:** Resource diagnostic settings and dated log samples.
- **If blocked or failed:** Unsupported categories: adjust resource-specific diagnostics.
- **Related test IDs:** `AZ-T32-01` through `AZ-T32-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `monitor`](command-recipes.md#monitor). Read-only unless explicitly called out as a planned controlled change.

## Phase 4: Steps 33–45 — AI, data, identities and private endpoints

### Step 33 — Configure Azure OpenAI account

- **Action:** Select supported region and custom subdomain; disable public data-plane access; assess local auth disablement.
- **Verification / pass criteria:** PNA explicitly disabled, service location and config approved.
- **Evidence to retain:** Azure OpenAI ARM export and approval.
- **If blocked or failed:** PNA enabled or SKU invalid: block acceptance.
- **Related test IDs:** `AZ-T33-01` through `AZ-T33-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `paas`](command-recipes.md#paas). Read-only unless explicitly called out as a planned controlled change.

### Step 34 — Deploy approved AI model

- **Action:** Record model, version, deployment type, capacity, quotas and content filter settings.
- **Verification / pass criteria:** Deployed model and quota exactly match approved design.
- **Evidence to retain:** Model deployment metadata and capacity approval.
- **If blocked or failed:** Quota/region mismatch: do not silently switch model.
- **Related test IDs:** `AZ-T34-01` through `AZ-T34-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `paas`](command-recipes.md#paas). Read-only unless explicitly called out as a planned controlled change.

### Step 35 — Configure Azure AI Search

- **Action:** Use PE-compatible SKU, disabled public access and reviewed key authentication setting.
- **Verification / pass criteria:** Search SKU, PE and authorization satisfy design.
- **Evidence to retain:** Search ARM export and role assignments.
- **If blocked or failed:** Free SKU where PE required: select compatible tier.
- **Related test IDs:** `AZ-T35-01` through `AZ-T35-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `paas`](command-recipes.md#paas). Read-only unless explicitly called out as a planned controlled change.

### Step 36 — Configure Cosmos DB NoSQL

- **Action:** Disable public data-plane access; configure supported local-auth policy, backup and consistency.
- **Verification / pass criteria:** Provider schema and NoSQL role model confirmed for pinned version.
- **Evidence to retain:** Cosmos ARM export and backup settings.
- **If blocked or failed:** Wrong property version: verify schema, rerun plan.
- **Related test IDs:** `AZ-T36-01` through `AZ-T36-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `paas`](command-recipes.md#paas). Read-only unless explicitly called out as a planned controlled change.

### Step 37 — Configure Key Vault and rotation

- **Action:** Use approved PE, scoped RBAC, certificate/secret rotation and evaluate CMK requirement.
- **Verification / pass criteria:** Gateway/app can resolve and retrieve approved secrets privately.
- **Evidence to retain:** Vault access evidence and rotation schedule.
- **If blocked or failed:** Unauthorized access or expired cert: block deployment.
- **Related test IDs:** `AZ-T37-01` through `AZ-T37-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `vault`](command-recipes.md#vault). Read-only unless explicitly called out as a planned controlled change.

### Step 38 — Approve AI/data private endpoints

- **Action:** Connect OpenAI account, Search searchService, Cosmos Sql and Vault vault subresources with zone groups.
- **Verification / pass criteria:** Connections Approved; NIC/private IP/subresource/zone match.
- **Evidence to retain:** PE inventory and DNS zone group exports.
- **If blocked or failed:** Wrong PE group or IP: reconstruct correct endpoint.
- **Related test IDs:** `AZ-T38-01` through `AZ-T38-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `pe`](command-recipes.md#pe). Read-only unless explicitly called out as a planned controlled change.

### Step 39 — Provision App Service inbound PE

- **Action:** Create sites PE for web app ingress and verify SCM/Kudu private name resolution if used.
- **Verification / pass criteria:** Web and deployment endpoints resolve to approved private IPs.
- **Evidence to retain:** Web PE and SCM DNS evidence.
- **If blocked or failed:** SCM inaccessible: verify SCM DNS and runner routes.
- **Related test IDs:** `AZ-T39-01` through `AZ-T39-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `pe`](command-recipes.md#pe). Read-only unless explicitly called out as a planned controlled change.

### Step 40 — Enable private software delivery

- **Action:** Provide federated self-hosted runner access to private SCM and/or ACR without public management ports.
- **Verification / pass criteria:** Approved CI can deploy or pull images on private routes.
- **Evidence to retain:** CI connection test and role assignments.
- **If blocked or failed:** Deployment path not yet available: NOT_READY.
- **Related test IDs:** `AZ-T40-01` through `AZ-T40-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `deploy`](command-recipes.md#deploy). Read-only unless explicitly called out as a planned controlled change.

### Step 41 — Use Search shared private link if needed

- **Action:** Where Search indexer calls private source services, configure approved shared private link and approvals.
- **Verification / pass criteria:** Indexer reaches only approved source and succeeds.
- **Evidence to retain:** Indexer execution and shared link approvals.
- **If blocked or failed:** No indexer dependency: mark NOT_APPLICABLE with evidence.
- **Related test IDs:** `AZ-T41-01` through `AZ-T41-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `paas`](command-recipes.md#paas). Read-only unless explicitly called out as a planned controlled change.

### Step 42 — Assign managed identities

- **Action:** Choose app managed identity lifecycle; scope OpenAI User and Search data roles to actual operations.
- **Verification / pass criteria:** Authorized principal succeeds without embedded API key.
- **Evidence to retain:** Identity/RBAC inventory and app auth results.
- **If blocked or failed:** Principal mismatch: verify client ID, audience and role propagation.
- **Related test IDs:** `AZ-T42-01` through `AZ-T42-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `identity`](command-recipes.md#identity). Read-only unless explicitly called out as a planned controlled change.

### Step 43 — Assign Cosmos NoSQL data roles

- **Action:** Use Cosmos DB SQL data-plane roles, not only generic ARM RBAC, with minimum scopes.
- **Verification / pass criteria:** Necessary reads/writes work and excess privileges are rejected.
- **Evidence to retain:** Cosmos SQL role definition and assignment export.
- **If blocked or failed:** 403 from Cosmos: inspect data-plane role and scope.
- **Related test IDs:** `AZ-T43-01` through `AZ-T43-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `identity`](command-recipes.md#identity). Read-only unless explicitly called out as a planned controlled change.

### Step 44 — Validate provider and policy schema

- **Action:** Inspect pinned provider schema then run fmt/validate/test/scans and plan policy checks.
- **Verification / pass criteria:** No unverified HCL attributes or failing critical policy checks.
- **Evidence to retain:** Provider schema digest and CI scan logs.
- **If blocked or failed:** Schema mismatch: correct HCL before apply.
- **Related test IDs:** `AZ-T44-01` through `AZ-T44-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `terraform`](command-recipes.md#terraform). Read-only unless explicitly called out as a planned controlled change.

### Step 45 — Approve saved deployment plan

- **Action:** Two independent reviewers examine cost, public access, roles, topology and proposed diffs.
- **Verification / pass criteria:** Plan, commit SHA and approvals are bound together and retained securely.
- **Evidence to retain:** Signed plan approval record and summary (not raw plan public).
- **If blocked or failed:** No second approval or uncontrolled diff: NO-GO.
- **Related test IDs:** `AZ-T45-01` through `AZ-T45-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `plan`](command-recipes.md#plan). Read-only unless explicitly called out as a planned controlled change.

## Phase 5: Steps 46–58 — App Service, gateway, TLS and controlled deployment

### Step 46 — Select resilient App Service plan

- **Action:** Choose Linux App Service plan with validated scale, zone, capacity, SLA and cost.
- **Verification / pass criteria:** Plan supports PE+VNet integration and agreed HA requirements.
- **Evidence to retain:** SKU/capacity review and plan config.
- **If blocked or failed:** Insufficient SKU/zone: redesign prior to deploy.
- **Related test IDs:** `AZ-T46-01` through `AZ-T46-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `app`](command-recipes.md#app). Read-only unless explicitly called out as a planned controlled change.

### Step 47 — Harden Linux Web App

- **Action:** Enforce HTTPS/TLS, disabled FTP/basic publishing, managed identity, health probes and disabled public access.
- **Verification / pass criteria:** All hardened settings match approved profile; authentication verified separately.
- **Evidence to retain:** Web App ARM config and application health logs.
- **If blocked or failed:** Web app publicly reachable: block release and remediate PNA.
- **Related test IDs:** `AZ-T47-01` through `AZ-T47-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `app`](command-recipes.md#app). Read-only unless explicitly called out as a planned controlled change.

### Step 48 — Use canonical dependency FQDNs

- **Action:** Use usual service FQDNs, not privatelink names, then resolve with private DNS and TLS hostname validation.
- **Verification / pass criteria:** A/alias final address belongs to approved PE NIC and TLS host matches.
- **Evidence to retain:** App settings sans secrets; DNS and TLS observations.
- **If blocked or failed:** Name resolves publicly: fix zone links/forwarders.
- **Related test IDs:** `AZ-T48-01` through `AZ-T48-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `dns`](command-recipes.md#dns). Read-only unless explicitly called out as a planned controlled change.

### Step 49 — Avoid duplicate VNet integration ownership

- **Action:** Manage VNet integration through one supported Terraform resource/attribute only.
- **Verification / pass criteria:** No competing swift connection and web-app subnet configurations.
- **Evidence to retain:** Resource graph / Terraform planned diff.
- **If blocked or failed:** Perpetual diff: remove duplicate ownership.
- **Related test IDs:** `AZ-T49-01` through `AZ-T49-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `plan`](command-recipes.md#plan). Read-only unless explicitly called out as a planned controlled change.

### Step 50 — Configure ACR when containers are used

- **Action:** If containerized, use required ACR tier, private endpoint/DNS, managed pull identity, SBOM and image digest pinning.
- **Verification / pass criteria:** Private image pull and signature checks pass.
- **Evidence to retain:** ACR deployment and registry signature evidence.
- **If blocked or failed:** No containers: mark justified NOT_APPLICABLE.
- **Related test IDs:** `AZ-T50-01` through `AZ-T50-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `deploy`](command-recipes.md#deploy). Read-only unless explicitly called out as a planned controlled change.

### Step 51 — Configure WAF policy

- **Action:** Choose supported managed rule set (baseline DRS 2.2), tune Detection then approved Prevention; record exclusions.
- **Verification / pass criteria:** Positive business traffic passes and approved attack fixtures block with log correlation.
- **Evidence to retain:** WAF policy version, exception register and test pairs.
- **If blocked or failed:** Unexpected block: limit exclusion to exact request surface.
- **Related test IDs:** `AZ-T51-01` through `AZ-T51-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `waf`](command-recipes.md#waf). Read-only unless explicitly called out as a planned controlled change.

### Step 52 — Deploy private-only Application Gateway

- **Action:** Use dedicated subnet and private frontend only, without public frontend; verify deployment-mode restrictions.
- **Verification / pass criteria:** Public gateway frontend count is zero and private listener is healthy.
- **Evidence to retain:** Gateway ARM frontend inventory and health.
- **If blocked or failed:** Public frontend detected: reject plan, not a live edit.
- **Related test IDs:** `AZ-T52-01` through `AZ-T52-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `appgw`](command-recipes.md#appgw). Read-only unless explicitly called out as a planned controlled change.

### Step 53 — Manage TLS certificates in Key Vault

- **Action:** Use managed identity and versionless secret reference as supported, validate expiry, chain and rotation.
- **Verification / pass criteria:** Certificate trusted, correct hostname, renewal path verified.
- **Evidence to retain:** Vault secret URI without value, expiry and probe.
- **If blocked or failed:** Certificate access denied: inspect ID, DNS and vault policy.
- **Related test IDs:** `AZ-T53-01` through `AZ-T53-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `tls`](command-recipes.md#tls). Read-only unless explicitly called out as a planned controlled change.

### Step 54 — Configure listener and probes

- **Action:** Define HTTPS listener, TLS backend setting, routing rule priorities and supported /healthz probe.
- **Verification / pass criteria:** Backend marked Healthy and HTTP behavior matches policy.
- **Evidence to retain:** Listener/probe settings and timestamped health status.
- **If blocked or failed:** Unhealthy backend: isolate probe path, host and TLS.
- **Related test IDs:** `AZ-T54-01` through `AZ-T54-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `appgw`](command-recipes.md#appgw). Read-only unless explicitly called out as a planned controlled change.

### Step 55 — Align backend FQDN, SNI and Host

- **Action:** Use canonical App Service hostname in pool and match SNI, host headers and probe host to application config.
- **Verification / pass criteria:** TLS handshake and backend health both succeed via PE.
- **Evidence to retain:** DNS resolution, host/SNI config and backend health.
- **If blocked or failed:** TLS mismatch: fix expected backend host/probe.
- **Related test IDs:** `AZ-T55-01` through `AZ-T55-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `tls`](command-recipes.md#tls). Read-only unless explicitly called out as a planned controlled change.

### Step 56 — Enforce private endpoint source boundaries

- **Action:** Permit gateway-to-app and app-to-service over necessary ports, block unauthorized subnets and apply app-layer auth.
- **Verification / pass criteria:** Source-restricted reachability AND identity authorization succeed.
- **Evidence to retain:** NSG/route evidence plus 2-sided auth tests.
- **If blocked or failed:** PE access unexpectedly open: check PE network policies.
- **Related test IDs:** `AZ-T56-01` through `AZ-T56-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `nsg`](command-recipes.md#nsg). Read-only unless explicitly called out as a planned controlled change.

### Step 57 — Enable logs and alerting

- **Action:** Send Gateway, WAF, web app, identity/data and Vault diagnostics to approved workspace with alert owners.
- **Verification / pass criteria:** Expected log arrives, correlation IDs preserved and alerts fire.
- **Evidence to retain:** Sanitized log queries and notification record.
- **If blocked or failed:** Missing logs: inspect category, connector and ingestion lag.
- **Related test IDs:** `AZ-T57-01` through `AZ-T57-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `monitor`](command-recipes.md#monitor). Read-only unless explicitly called out as a planned controlled change.

### Step 58 — Apply only approved plan from CI

- **Action:** Authorized isolated CI applies the exact approved saved plan using federated identity after approval gates.
- **Verification / pass criteria:** Applied resources match approved plan; approval and provenance traceable.
- **Evidence to retain:** CI run ID, reviewer decisions, redacted apply log.
- **If blocked or failed:** Unapproved plan or credentials: stop deployment.
- **Related test IDs:** `AZ-T58-01` through `AZ-T58-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `apply`](command-recipes.md#apply). Read-only unless explicitly called out as a planned controlled change.

## Phase 6: Steps 59–68 — Postdeployment layered verification

### Step 59 — Inventory deployed controls first

- **Action:** Review public IP/PNA, roles, diagnostics and policy status from portal/Resource Graph before networking probes.
- **Verification / pass criteria:** Inventory matches approved asset IDs, subscription and expected version.
- **Evidence to retain:** Read-only resource inventory and approval baseline.
- **If blocked or failed:** Unknown assets: NOT_READY pending reconciliation.
- **Related test IDs:** `AZ-T59-01` through `AZ-T59-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `inventory`](command-recipes.md#inventory). Read-only unless explicitly called out as a planned controlled change.

### Step 60 — Inspect private endpoint wiring

- **Action:** Confirm each PE Approved and correct subnet, NIC, IP, subresource and DNS zone group.
- **Verification / pass criteria:** PE mapping agrees with accepted topology.
- **Evidence to retain:** PE map exported and reviewed.
- **If blocked or failed:** PE pending approval: resolve before functional testing.
- **Related test IDs:** `AZ-T60-01` through `AZ-T60-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `pe`](command-recipes.md#pe). Read-only unless explicitly called out as a planned controlled change.

### Step 61 — Validate internal DNS from trusted runner

- **Action:** Resolve canonical service hostnames and compare final private addresses with PE NIC inventory.
- **Verification / pass criteria:** All required FQDNs resolve privately via the approved resolver chain.
- **Evidence to retain:** dig/getent output plus expected IP manifest.
- **If blocked or failed:** Wrong resolver path: inspect conditional forwarding/link.
- **Related test IDs:** `AZ-T61-01` through `AZ-T61-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `dns`](command-recipes.md#dns). Read-only unless explicitly called out as a planned controlled change.

### Step 62 — Prove absence of public ingress

- **Action:** Combine ARM frontend and service PNA assertions with observations outside approved network.
- **Verification / pass criteria:** No unauthorized public ingress; 403 alone never counts as proof.
- **Evidence to retain:** PNA/public IP config plus external test record.
- **If blocked or failed:** Missing Azure inventory: classify observation NOT_READY.
- **Related test IDs:** `AZ-T62-01` through `AZ-T62-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `negative`](command-recipes.md#negative). Read-only unless explicitly called out as a planned controlled change.

### Step 63 — Classify denial responses rigorously

- **Action:** Distinguish genuine blocked/denied results from NXDOMAIN, 404, DNS errors, absent targets and timeouts.
- **Verification / pass criteria:** Interpretations follow service-specific expected-result matrix.
- **Evidence to retain:** Normalized outcome and target existence proof.
- **If blocked or failed:** Unexpected response: inspect DNS, target presence and TLS.
- **Related test IDs:** `AZ-T63-01` through `AZ-T63-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `negative`](command-recipes.md#negative). Read-only unless explicitly called out as a planned controlled change.

### Step 64 — Execute private E2E acceptance

- **Action:** From VNet runner check HTTPS, authentication, health, session and critical UI flows with Playwright.
- **Verification / pass criteria:** Route-specific positive checks pass; auth adaptor implemented and reviewed.
- **Evidence to retain:** JUnit/trace, backend health and redacted app logs.
- **If blocked or failed:** Missing real app/auth flow: NOT_READY, not a synthetic PASS.
- **Related test IDs:** `AZ-T64-01` through `AZ-T64-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `internal`](command-recipes.md#internal). Read-only unless explicitly called out as a planned controlled change.

### Step 65 — Verify managed identity dependency calls

- **Action:** Run safe app-owned probes to OpenAI, Search and Cosmos using managed identities and non-sensitive fixtures.
- **Verification / pass criteria:** Authorized calls succeed privately with no API key use.
- **Evidence to retain:** Dependency response + identity/PE correlation record.
- **If blocked or failed:** 403: verify audience, principal, RBAC, routing.
- **Related test IDs:** `AZ-T65-01` through `AZ-T65-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `identity`](command-recipes.md#identity). Read-only unless explicitly called out as a planned controlled change.

### Step 66 — Test unauthorized principals in isolation

- **Action:** Use isolated nonproduction principal with denied data roles alongside authorized control; never remove production roles.
- **Verification / pass criteria:** Positive and negative authorization traces show least privilege.
- **Evidence to retain:** Paired response/log proof in approved environment.
- **If blocked or failed:** Unauthorized success: security incident/change blocker.
- **Related test IDs:** `AZ-T66-01` through `AZ-T66-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `identity`](command-recipes.md#identity). Read-only unless explicitly called out as a planned controlled change.

### Step 67 — Diagnose network path within supported limits

- **Action:** Use NIC effective rules, approved flow logs, gateway health and supported Network Watcher tests; do not require unsupported private Gateway probes.
- **Verification / pass criteria:** Path and denial can be reconstructed from supported diagnostics.
- **Evidence to retain:** Flow excerpts and effective route/NSG report.
- **If blocked or failed:** Unsupported diagnostic: select supported equivalent.
- **Related test IDs:** `AZ-T67-01` through `AZ-T67-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `monitor`](command-recipes.md#monitor). Read-only unless explicitly called out as a planned controlled change.

### Step 68 — Exercise state recovery and disaster plans

- **Action:** Verify backend lock/version/permissions and drift; rehearse supported service recovery and AI Search reindex from source.
- **Verification / pass criteria:** RTO/RPO and integrity meet approved objectives.
- **Evidence to retain:** DR exercise results, restoration/reindex logs and drift plan.
- **If blocked or failed:** No original data to rebuild Search: DR gate fails.
- **Related test IDs:** `AZ-T68-01` through `AZ-T68-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `dr`](command-recipes.md#dr). Read-only unless explicitly called out as a planned controlled change.

## Phase 7: Steps 69–78 — Security simulation, operations and handover

### Step 69 — Perform approved WAF simulation

- **Action:** Run benign SQLi/XSS strings only against an authorized isolated endpoint with normal controls.
- **Verification / pass criteria:** Both normal control and selected malicious fixture behave as expected.
- **Evidence to retain:** Signed test scope, request IDs and WAF logs.
- **If blocked or failed:** Missing authorization: do not send probes.
- **Related test IDs:** `AZ-T69-01` through `AZ-T69-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `waf`](command-recipes.md#waf). Read-only unless explicitly called out as a planned controlled change.

### Step 70 — Correlate WAF block decision

- **Action:** Check HTTP status, transaction ID, matched/blocked WAF action and version; account for anomaly scoring.
- **Verification / pass criteria:** Expected prevention block and rule ID align with approved fixture.
- **Evidence to retain:** 403 + associated WAF Blocked event.
- **If blocked or failed:** 403 without correlated block: investigate, do not PASS.
- **Related test IDs:** `AZ-T70-01` through `AZ-T70-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `waf`](command-recipes.md#waf). Read-only unless explicitly called out as a planned controlled change.

### Step 71 — Trace WAF logs end-to-end

- **Action:** Use unique synthetic correlation ID across Gateway Access, Firewall and backend logs.
- **Verification / pass criteria:** Blocked request is absent at backend and event appears at expected time.
- **Evidence to retain:** Sanitized KQL query and correlated event export.
- **If blocked or failed:** Log delay/schema mismatch: retry with bounded window.
- **Related test IDs:** `AZ-T71-01` through `AZ-T71-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `monitor`](command-recipes.md#monitor). Read-only unless explicitly called out as a planned controlled change.

### Step 72 — Validate lateral isolation and RBAC

- **Action:** Compare approved subnet connectivity to unapproved subnet rejection and identity authorizations.
- **Verification / pass criteria:** Allowed flow succeeds, forbidden flow denied, RBAC independently enforced.
- **Evidence to retain:** Paired route and token/role test results.
- **If blocked or failed:** Direct PE path open: review NSG policies and authorization.
- **Related test IDs:** `AZ-T72-01` through `AZ-T72-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `nsg`](command-recipes.md#nsg). Read-only unless explicitly called out as a planned controlled change.

### Step 73 — Verify performance and failover

- **Action:** Use approved k6/Azure Load Testing job for performance and separate HA/scale/DR exercises; Playwright is functional only.
- **Verification / pass criteria:** SLOs under approved load and failover meet business targets.
- **Evidence to retain:** Load plan and metrics/SLO report.
- **If blocked or failed:** No approved load test: NOT_READY, never run against production.
- **Related test IDs:** `AZ-T73-01` through `AZ-T73-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `perf`](command-recipes.md#perf). Read-only unless explicitly called out as a planned controlled change.

### Step 74 — Reject intentionally bad Terraform plans

- **Action:** In disposable sandbox, inject PNA or broad NSG plan mutations and require policy fail before apply.
- **Verification / pass criteria:** Bad plans fail; good plan passes; nothing modified in prod.
- **Evidence to retain:** Fixture plan JSON and policy test run.
- **If blocked or failed:** Policy falsely allows bad plan: P0 open.
- **Related test IDs:** `AZ-T74-01` through `AZ-T74-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `policy`](command-recipes.md#policy). Read-only unless explicitly called out as a planned controlled change.

### Step 75 — Schedule continuous exposure checks

- **Action:** Plan periodic public IP, PNA, local auth, missing diagnostics, drift and vulnerability checks with accountable owners.
- **Verification / pass criteria:** New exposures create tickets and time-bound remediation.
- **Evidence to retain:** Periodic approved monitor report and work items.
- **If blocked or failed:** Blind spot or missing owner: operational gate fails.
- **Related test IDs:** `AZ-T75-01` through `AZ-T75-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `inventory`](command-recipes.md#inventory). Read-only unless explicitly called out as a planned controlled change.

### Step 76 — Enforce promotion pipeline sequence

- **Action:** Separate fmt/validate/scan/policy/plan approvals/apply and post-deploy security tests with immutable commit provenance.
- **Verification / pass criteria:** A failed gate blocks downstream deployment; approvals independent.
- **Evidence to retain:** Pipeline policy and executed gate history.
- **If blocked or failed:** Gate bypass: block release and investigate.
- **Related test IDs:** `AZ-T76-01` through `AZ-T76-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `ci`](command-recipes.md#ci). Read-only unless explicitly called out as a planned controlled change.

### Step 77 — Freeze handover artifacts

- **Action:** Collect approved architecture, SBOM, key inventory, RTO/RPO, test evidence, release tag and rollback plan.
- **Verification / pass criteria:** Handover package complete and independently acknowledged.
- **Evidence to retain:** Manifest, signed tag, transition checklist.
- **If blocked or failed:** Missing evidence: keep release artifact draft.
- **Related test IDs:** `AZ-T77-01` through `AZ-T77-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `handover`](command-recipes.md#handover). Read-only unless explicitly called out as a planned controlled change.

### Step 78 — Decide Go/No-Go

- **Action:** Require no critical open exposure, accepted private DNS/MI/WAF/log/DR/drift tests and independent approval.
- **Verification / pass criteria:** Formal decision has exact environment, commit, evidence and signatures.
- **Evidence to retain:** Signed change board Go/No-Go record.
- **If blocked or failed:** Any open P0 or accepted live evidence missing: NO-GO.
- **Related test IDs:** `AZ-T78-01` through `AZ-T78-22` (22 draft cases; not 22 Azure passes).
- **Command / inspection method:** [Recipe `go`](command-recipes.md#go). Read-only unless explicitly called out as a planned controlled change.

## Release gate and traceability

All 78 steps must be covered by an approved plan and designated evidence before production release, but design work alone does not satisfy that gate. **78 × 22 = 1,716 draft test IDs; positive 858 and synthetic-deviation 858.** Fail open network paths, missing real source, missing approved baseline, failed certificate/identity tests, unsupported recovery, unapproved changes or unresolved P0 -> **NO-GO**.

## Troubleshooting order

1. **Wrong resource scope?** Confirm approved subscription/region/resource IDs before interpreting any API or DNS output.
2. **Private name resolution fails?** Verify standard FQDN → privatelink alias/A → PE NIC/private IP; verify zone links, central resolver and conditional forwarder.
3. **App Gateway unhealthy?** Check private frontend mode, subnet delegation, host/SNI, backend certificate, /healthz path and NSG policies.
4. **Data API returns 403?** Separate path/PNA from principal, audience and Cosmos or Search data-plane roles; never turn on public access as a fix.
5. **State init fails?** Check runner DNS/port 443 → state Blob PE, OIDC audience and Storage Blob RBAC; do not change remote state to local silently.
6. **WAF evidence absent?** Verify diagnostic category/table, request correlation ID, mode, managed rule ID and ingestion delay; bare HTTP 403 is insufficient.
7. **Recovery cannot reach RTO/RPO?** Stop promotion; exercise backups/rebuild and reindex before changing objectives.

## References and provenance

The underlying runbook cites Microsoft Learn for Private Application Gateway, App Service private endpoint, WAF managed rule sets, Network Watcher flow log lifecycle, and HashiCorp for AzureRM remote backend. The accepted provider configuration and service-specific features must be revalidated against the actual approved environment before use; prior source review is not current deployment evidence.

**Related publications:** [Architecture detail](architecture-detailed.md) · [Threat model](threat-model.md) · [Command recipes](command-recipes.md) · [Acceptance criteria](acceptance-criteria.md) · [Current status](current-status.md).