# Private Runner and Terraform state execution

This prepares B05/G07. The workflow in ci/private-terraform.CANDIDATE.yml is inactive. Azure acceptance is **0/1,716**, independent signatures **0**, release **NO_GO**.

## First bootstrap and ownership

The normal Runner needs private state access, but using that state to provision its network and identities would first require the Runner. Break the cycle with an approved bootstrap operator and an independent management network. Terraform prepares the private state path and identity resources. The Runner host, registration, peering/forwarding, and GitHub protections remain owner-operated.

| Asset | Bootstrap-owned | Existing owner-managed |
|---|---|---|
| Blob state | Private account and container, Blob PE, HTTPS, no public access or shared keys. Supply approved state_runner_cidrs for the PE NSG. | Supply exact approved account, container, key and PE addresses. Verify equivalent controls without an unreviewed import. |
| DNS | Dev creates its own zone and VNet link in an isolated view. | Hub supplies exact existing_blob_dns_zone_id; Hub owns VNet links and forwarding. |
| CI identities | manage_ci_identities creates three UAMIs, their exact GitHub federated credentials and container-scoped state grants. | Administrator verifies separate existing identities, federation, container grants and workload scopes. |
| Bootstrap state | Encrypted local management workspace until there is a separately owned backend. | Preserve established ownership, backup and state lineage. |

1. Put the approved bootstrap source, lock and restricted inputs in an encrypted management workspace outside Git. Use the authorized operator's Azure management-plane identity in a separate approved window. This root uses local state and does not point to the Blob account it provisions. Review and authorize its first plan before applying.
2. Provision the independent ephemeral Runner and route it to the approved Blob PE. The DNS owner verifies exact DNS responses and prevents duplicates with the Monitor or bootstrap Blob zones. Moved blocks preserve the legacy DNS and role addresses when configured. Omit ci_principal_object_id on a new install; preserve an existing value until approved migration is complete. Changing DNS ownership needs a reviewed state migration.
3. Protect bootstrap state, encrypted backups and lineage outside Git. To migrate it, stop all writers, verify the backup and destination ownership and use reviewed terraform init -migrate-state from the protected source workspace to an independently managed backend. Compare remote lineage/resource parity before retiring the old copy. Never migrate bootstrap state into its own storage account. Use equivalent controls to move any existing workload state into the approved private container. For an empty workload, explicitly allow its named Blob to be absent until initialized, then revert that permission.
4. The administrator pre-registers providers and assigns target scopes. To keep workload permissions RG-scoped, establish the RG and import the approved foundation resource where necessary in a separately reviewed procedure. Terraform-managed role assignments still require a separately authorized administrative grant or an explicitly delegated scope. Avoid subscription Owner as a shortcut.

## Trust and roles

The candidate has only workflow_dispatch. Each job checks the exact repository, protected main, requested SHA and dedicated Environment. The Environment and trusted Runner group must be configured before placing the file under .github/workflows. Set required reviewers, prevent self-review, restrict bypass and restrict the runner group to this approved workflow on protected main. The repository is public; keep the candidate inactive unless those protections are available. Use single-job Linux x64 ephemeral Runners and avoid all pull request triggers or checkout refs. The protected credentials are unrelated to application Entra sign-in and App Service UAMI.

| Environment | GitHub subject suffix | State container grant | Workload grant |
|---|---|---|---|
| nonprod-read | environment:nonprod-read | Storage Blob Data Reader | Scoped read plus approved read-only test permissions |
| nonprod-plan | environment:nonprod-plan | Storage Blob Data Contributor for lease and possible empty-state initialization | Scoped read/discovery, no provider auto-registration |
| nonprod-apply | environment:nonprod-apply | Storage Blob Data Contributor | Scoped deployment with separately controlled RBAC |

Subjects use repo:tayoshik/azure-private-ai-assurance: plus the suffix. The GitHub issuer is token.actions.githubusercontent.com and exchange audience is api://AzureADTokenExchange. A Storage audience access token is obtained separately. AzureRM 4.66.0 / Terraform 1.9.8 linux_amd64 and approved azure-identity must be installed. The plan/apply image must lack Azure CLI because the pinned backend has a CLI fallback. Credential/config overrides are discarded and provider registration is disabled in the candidate.

## Normal workflow and recovery

1. Fill specs/private-terraform-ci.example.json in restricted storage and run python3 -B scripts/private_terraform_ci.py --check-config /restricted/contract.json. Passing only validates declared inputs.
2. After separately approving activation, dispatch read on the approved commit. Verify the exact private DNS IP set, hostname TLS, Storage OIDC exchange and container/state Blob HEAD separately. It reads metadata only. HEAD proves neither lease/write permissions nor state contents. 403, unexpected 404 and mismatches stop the phase. Only the explicitly approved first-write case may accept BlobNotFound from an accessible container.
3. Dispatch plan on the same reviewed commit. Configure APPROVED_PLAN_VOLUME as an approved encrypted restricted mount with audited access and no untrusted write path. Supply TF_PRIVATE_CONTRACT and TF_PRIVATE_TFVARS through each applicable protected Environment. The runner keeps a fresh data directory, applies readonly provider locks and uses a finite lock timeout. It keeps the plan out of general artifacts. Its manifest binds exact plan/hash, contract/backend, tfvars, provider lock, commit/run/environment, post-plan state ETag hash and a two-hour expiry.
4. The reviewer inspects the restricted plan and supplies TF_PRIVATE_PLAN_APPROVAL to the apply Environment: manifest_sha256, plan_sha256, commit, environment, run_id, approval_ref and timezone-aware approved_at. Dispatch apply with the approved plan run ID and commit. The runner stages and verifies the exact bytes and repeats the expiry check after init. Shared workflow concurrency serializes the phases; Terraform's native lease and stale-plan checks remain in place. No implicit replan.
5. After an independently authorized apply, run the scoped deployed inventory and AZ-T26/28/29/30/31 from the protected read path. Collect sanitized results. The end-to-end deployment/test sequence still needs its first approved execution.

On DNS/TLS failure, check the route, NSG, DNS view, PE approval and CA trust. On authorization failure, verify the Container data-plane role and OIDC subject/audience. Do not switch to public, key or SAS access. Expired, mismatched or partially applied plans require a fresh review and plan. Confirm the lock holder before any separately approved recovery or unlock. Restore only from a reviewed backup with valid lineage. Investigate raw Terraform errors in the authorized management workspace, and keep plans, logs, tfvars and state out of GitHub output/artifacts.

References: [Terraform AzureRM backend](https://developer.hashicorp.com/terraform/language/backend/azurerm), [Terraform 1.9.8 backend](https://github.com/hashicorp/terraform/tree/v1.9.8/internal/backend/remote-state/azure), [Blob container HEAD](https://learn.microsoft.com/en-us/rest/api/storageservices/get-container-properties), [GitHub protected environments](https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments).
