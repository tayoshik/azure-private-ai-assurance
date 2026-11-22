# Terraform module source and interface index (G06)

**Snapshot:** 2026-11-22. This is a repository source map, **not** evidence of deployment, model availability, Azure acceptance, or organizational sign-off.

The two separately initialized Terraform roots are `infra/bootstrap` and `infra/environments/dev`. Module **inputs and outputs** are declared in each module's `variables.tf` and `outputs.tf` (or adjacent HCL), not in this README. The DEV root `infra/environments/dev/main.tf` is the authoritative module-composition reference; the provider version is pinned by both roots to AzureRM 4.66.0.

| Module path | Current source purpose / DAG nodes | Principal HCL |
| --- | --- | --- |
| `foundation/` | Workload resource group (N01) | `main.tf` |
| `network/` | Workload VNet, dedicated subnets (N02/N03), NSG/egress rules (N04) | `main.tf`, `policy.tf` |
| `private-dns/` | Private zones and VNet links (N05) | `main.tf` |
| `monitoring/` | Log Analytics and private-link/AMPLS component (O01/O02 partial) | `main.tf`, `private-link.tf` |
| `identity/` | Managed app/gateway identities (I01) | `main.tf` |
| `key-vault/` | Key Vault and identity permissions (I02) | `main.tf` |
| `private-endpoints/` | **Key Vault** private endpoint only (I03) | `key-vault.tf` |
| `azure-openai/` | Cognitive account and model deployment declarations (A01/A02) | `main.tf` |
| `ai-search/` | Azure AI Search service (A03) | `main.tf` |
| `cosmos-db/` | Cosmos DB NoSQL account/data model (A04) | `main.tf` |
| `ai-private-endpoints/` | Distinct OpenAI/Search/Cosmos private endpoints (A05) | `main.tf` |
| `ai-data-rbac/` | OpenAI/Search/Cosmos least-privilege application role bindings (A06) | `main.tf` |
| `app-service/` | Linux App Service plan, app, outbound VNet connection, settings (W01/W02/W03/W05) | `plan.tf`, `webapp.tf`, `outbound-vnet.tf`, `app-settings.tf` |
| `webapp-private-endpoint/` | Separate inbound Web App sites private endpoint (W04) | `webapp.tf` |
| `application-gateway/` | WAF policy and private Application Gateway with Key Vault secret reference, HTTPS routing and diagnostics (GW01–GW05) | `waf-policy.tf`, `gateway.tf`, `routing.tf`, `diagnostics.tf` |

The bootstrap root implements B01/B02 with **`infra/bootstrap/main.tf`**, B04 with `infra/bootstrap/private_state.tf`, and optional identity/federated trust declarations in `infra/bootstrap/ci_execution.tf`. A written bootstrap/private CI workflow is available at `docs/private-terraform-execution.md`, but live B03/B05 readiness is **unverified**. Do not treat a source-declared identity as a registered, reachable or authorized runner.

**Open/partial decisions:** N06 optional DNS resolver not present; O02 has an AMPLS source file, but the planned VNet flow-log component is not proven; A07 optional Search shared private link not present; W06 optional private container registry not present. G07 environment, approved network, CIDR, model/region support, private routing, TLS/Key Vault certificate, state access and authorized runner are **NOT_READY**. The uncreated optional branches must be explicitly selected or marked N/A by owner approval.

To verify module interfaces without credentials:

```bash
find infra/modules -name '*.tf' -type f | sort
python3 scripts/audit_terraform_dag_paths.py
python3 -m unittest discover -s tests -p 'test_terraform_dag_paths.py' -v
# Provider-backed but Azure-offline CI (requires provider registry connectivity):
terraform fmt -check -diff -recursive infra
terraform -chdir=infra/environments/dev init -backend=false -lockfile=readonly -input=false
terraform -chdir=infra/environments/dev validate
```

**Acceptance boundary:** Source presence and offline provider validation are not `terraform plan/apply` or live Azure acceptance. Canonical 1,716 cases remain `NOT_READY`; release `NO_GO`. See `docs/terraform-implementation-dag.md` and its node-by-node audited status.
