# Step 29 Entra outbound dependencies

This overlay maps the 22 original Step 29 cases in specs/phase3_264_en.json. Runtime paths were prepared and mocked. No DNS or HTTPS dependency probe, Azure read, token request, login, deployment or policy change was performed for this work. Azure acceptance is **0/1,716**, independent signatures **0**, release **NO_GO**.

## Cloud and identity boundaries

| Flow | Initiator and destination | Scope and evidence |
|---|---|---|
| Application Entra sign-in | Browser to the approved tenant authority and back to the actual app redirect URI. Protocol/host traffic for server-side callback and metadata depends on the chosen app auth mechanism. | Tenant, app registration, exact issuer and audience, redirect URI, approved user/group/roles and real application route. The repository supplies infrastructure and a configurable health probe, with no verified Entra UI integration or deployed login/redirect contract. The observer accepts protected evidence extracts only for this flow. |
| App Service Managed Identity | App process to the platform-provided local IDENTITY_ENDPOINT using its protected identity header. It then reaches the approved service's private endpoint with that service's token audience. | Existing UAI/RBAC declarations establish intended principal and roles, not actual token acquisition or authorized service behavior. Do not expose the platform header or use the GitHub audience here. The observer accepts protected, normalized evidence without touching the App Service identity endpoint. |
| GitHub Actions workload identity | Approved Runner obtains its GitHub OIDC assertion through the runner-provided mechanism. Separately, Azure Public tenant discovery and token exchange use login.microsoftonline.com, and ARM reads use management.azure.com. | A reviewed exact GitHub issuer, subject and api://AzureADTokenExchange audience define federation. ARM scope is https://management.azure.com/.default and requires scoped read permission on the actual nonproduction target. The assertion audience and resource token scope serve different purposes. Keep id-token: write limited to an approved live job. The offline workflow has no Azure token or OIDC call. |

The executable profile is AzurePublic. Use a tenant-scoped v2 issuer. Government and China use separate authorities/endpoints, identity registrations, audiences and service availability, so this tool returns NOT_READY for those profiles until a separately reviewed dependency map is available. The Azure Public Entra hostname above comes from Microsoft documentation. Monitor ingest/query destinations, certificate CRL/OCSP, discovery key URLs or browser/CDN dependencies depend on the selected product, actual certificate chain, workload and policy. Owners enumerate exact reviewed destinations. The implementation does not insert fixed public IPs or wildcard permits. [National clouds](https://learn.microsoft.com/en-us/entra/identity-platform/authentication-national-cloud) · [Tenant OIDC metadata](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc) · [App Service identity](https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity) · [GitHub to Azure federation](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure-openid-connect)

NSG observations check IP-level limits and precedence using AZ-T28. FQDN allowance comes from a reviewed, normalized Firewall/Proxy policy export for the correct DNS view and source path. A UDR next hop is useful as configuration evidence; actual forwarding must be observed. The export check compares actor, category, exact host, port and control against the approved dependencies; reviewers verify collection completeness, policy processing order and that DNS or a direct route cannot bypass enforcement. [Firewall FQDN filtering](https://learn.microsoft.com/en-us/azure/firewall/domain-filtering-overview) · [Firewall rule processing](https://learn.microsoft.com/en-us/azure/firewall/infrastructure-fqdns)

## Inputs and execution

Start with specs/azure-entra-step29.example.json. Fill it in protected storage only. Hub shared and dev new both require explicit approval, scope reference, subscription and tenant, the private Runner check, exact owned dependencies and the right DNS view. The [prioritized build checklist](azure-build-readiness-inputs.md) gives the current owners' inputs and blockers.

Use a new output directory per mode. Set CFG, EVIDENCE and OUT to secure paths. Commands below are prepared for approved execution; only S and target-free configuration/mocked tests are part of Hosted CI.

```bash
# C: offline input shape
python3 -B scripts/azure_entra_step29.py --check-config --config "$CFG" --out "$OUT/config"
# A: scoped ARM GET
python3 -B scripts/azure_entra_step29.py --live-arm --config "$CFG" --out "$OUT/arm"
# D/H: exact Private Runner DNS or private HTTPS
python3 -B scripts/azure_entra_step29.py --live-dns --config "$CFG" --out "$OUT/dns"
python3 -B scripts/azure_entra_step29.py --live-health --config "$CFG" --out "$OUT/health"
# P/E/F/X: protected extract content only
python3 -B scripts/azure_entra_step29.py --review-policy --config "$CFG" --evidence "$EVIDENCE" --out "$OUT/policy"
python3 -B scripts/azure_entra_step29.py --review-hop --config "$CFG" --evidence "$EVIDENCE" --out "$OUT/hop"
python3 -B scripts/azure_entra_step29.py --review-denied --config "$CFG" --evidence "$EVIDENCE" --out "$OUT/flow"
python3 -B scripts/azure_entra_step29.py --review-auth --config "$CFG" --evidence "$EVIDENCE" --out "$OUT/identity"
# G: future explicitly approved public-cloud GitHub OIDC/ARM read only
python3 -B scripts/azure_entra_step29.py --live-auth --config "$CFG" --out "$OUT/github"
# S: grade paired synthetic examples only
python3 -B tests/test_azure_entra_step29.py --evidence "$OUT/synthetic"
```

- **A:** network requires exact subnet_id, nsg_id, route_table_id or null, ipv4 cidrs, paas_pe_cidrs, expected_routes, and approved egress legs (protocol, port, destinations). It checks configured IP-level rules and approved next hops. Unsupported Service Tags/ASGs, incomplete responses, and inaccessible resources remain NOT_READY under the shared AZ-T28 evaluator. PaaS service acceptance and end-to-end enforcement remain separate.
- **D/H:** private_target requires host, exact ordered chain, resolver_ip, ips, cidrs, health_path and health_status. H first checks exact DNS then connects to the pinned private IP with certificate hostname verification and a single unauthenticated GET per approved IP. It does not follow redirects or send cookies, and does not validate authenticated application behavior.
- **P:** Complete normalized export includes scope_ref, collection_ref, complete, no_bypass_reviewed, dns_view_reviewed, default_unapproved_deny and allows with exact dependency keys. Reconcile the official endpoints with actual firewall/proxy precedence and FQDN approvals. Contents matching leaves the owner cases NOT_READY until review.
- **E:** effective_next_hop declares source_ip, destination_ip, hop_ip and hop_type. Export includes the same fields plus scope_ref, complete and collection_ref. Obtain an approved actual effective-route/next-hop observation separately.
- **F:** deny_evidence includes the protected Step 26 flow tuple/timing fields plus isolated_scope_approved and approval_ref. The declared source is private and the already observed destination is an exact public IPv4. Receipt must have source_type vnet_flow or firewall_flow, scope_ref, complete, collection_ref, review_ref and one correlated TCP/443 denied record. This tool sends no deny probe. Timeout and ARM activity logs cannot establish network denial. Correlation does not authenticate the source.
- **X:** protected normalized identity extract includes flow (app, managed or github), scope_ref, collector_ref, cloud, tenant_id, target_audience, and flow-specific issuer/subject/exchange_audience or managed client_id. The three stage fields transport, token_acquisition and target_authorization take observed, not_run, unavailable or denied. Do not include credential material. Missing earlier stages prevent later observed statuses from being credited. Confirm collection provenance independently.
- **G:** github_auth_probe requires explicit_auth_approved, auth_approval_ref, direct_https_approved and one approved Microsoft.Web/sites ARM read ID within subscriptions. Supply AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_FEDERATED_TOKEN_FILE through a protected Runner and an approved azure-identity install. The assertion is checked locally for the expected issuer/subject/audience before Entra validates it. Transport to v2 discovery, actual token exchange and target ARM authorization are separately reported. Direct HTTPS mode is only for a reviewed path; an explicit Proxy-specific protocol is not implemented. ARM GET mode also binds the same approved identity. The tool does not run a browser login or Managed Identity acquisition.

JSON/JUnit contain only case IDs, status, mode and sanitized reasons, with Azure acceptance fixed at zero. Code 1 denotes mismatch; code 2 denotes missing or unverified prerequisites. Exit 0 denotes completion of the selected observation only. Permission errors and TLS/DNS failures are not successes. Token failure never substitutes for an authorization check.

## Original case mapping

All real observations below are NOT_RUN. The S fixture pairs exercise the detectors; they do not complete their source requirements.

| ID | Original requirement | Command | Expected result / evidence still needed |
|---|---|---|---|
| AZ-T29-01 | Entra authentication endpoint dependencies have authorized route and egress policy | Owner + P; G/X supplemental | Approved per-actor tenant and effective FQDN policy. G/X separately show authentication stages; owner proves full route and scope. |
| AZ-T29-02 | Entra authentication endpoint dependencies have authorized route and egress policy | S | Synthetic missing authority route fails. |
| AZ-T29-03 | Monitoring ingestion/query dependencies have authorized route and egress policy | Owner + P | Approved Monitor ingestion/query destinations and effective policy export; actual ingestion/query belongs to AZ-T31. |
| AZ-T29-04 | Monitoring ingestion/query dependencies have authorized route and egress policy | S | Synthetic wildcard Monitor destination rejected. |
| AZ-T29-05 | Internal DNS returns expected PE IP from the right resolver and subnet | D | Approved resolver, exact host/aliases and private PE address set from actual Runner; sanitized DNS observation. |
| AZ-T29-06 | Internal DNS returns expected PE IP from the right resolver and subnet | S | Synthetic wrong address rejected. |
| AZ-T29-07 | Certificate revocation/OCSP dependencies are enumerated and approved | Owner + P | Owner establishes actual served certificate chain and CRL/OCSP requirements; export must match. |
| AZ-T29-08 | Certificate revocation/OCSP dependencies are enumerated and approved | S | Synthetic wrong protocol port rejected. |
| AZ-T29-09 | Private PaaS data-plane 443 flows are allowed only to the intended PE destinations | A | Scoped NSG configuration and intended private PE CIDRs; peer policy and TCP/acceptance separately. |
| AZ-T29-10 | Private PaaS data-plane 443 flows are allowed only to the intended PE destinations | S | Synthetic broad allow is rejected. |
| AZ-T29-11 | Actual effective next hop equals the approved firewall/NVA path | E | Effective next-hop extract agrees with approved source/destination/firewall; verify collection and authentication independently. |
| AZ-T29-12 | Actual effective next hop equals the approved firewall/NVA path | S | Synthetic wrong next hop rejected. |
| AZ-T29-13 | Route table and active firewall paths agree with network topology | A + P/E | ARM route attachment matches; approved effective-path and Firewall/Proxy evidence needed to verify actual use. |
| AZ-T29-14 | Route table and active firewall paths agree with network topology | S | Synthetic unexpected route association rejected. |
| AZ-T29-15 | Unapproved public internet traffic is denied and validated beyond NSG rule existence | F | Correlated scoped public-egress deny evidence; operator certifies isolated vantage and collection; no probe/timeout treated as deny. |
| AZ-T29-16 | Unapproved public internet traffic is denied and validated beyond NSG rule existence | S | Synthetic Allow record rejected for expected denial. |
| AZ-T29-17 | Every required external dependency has a business purpose, owner and approved exception | Owner + P | Owner, purpose, expiry and approval for every declaration; verify real completeness, scope and approved change. |
| AZ-T29-18 | Every required external dependency has a business purpose, owner and approved exception | S | Synthetic missing owner rejected. |
| AZ-T29-19 | Approved internal test returns expected HTTPS health with valid TLS and private remote IP | H | Approved private FQDN/IP, TLS hostname verification and expected unauthenticated health HTTP status; app auth remains open. |
| AZ-T29-20 | Approved internal test returns expected HTTPS health with valid TLS and private remote IP | S | Synthetic unexpected status and TLS failure rejected or NOT_READY. |
| AZ-T29-21 | Denied traffic is visible in appropriate flow/firewall logs; ARM activity logs alone are insufficient | F | Scoped VNet Flow or Firewall denial record connects to actual approved tuple/time; authenticity requires review. |
| AZ-T29-22 | Denied traffic is visible in appropriate flow/firewall logs; ARM activity logs alone are insufficient | S | Synthetic ARM activity log rejected as network denial evidence. |
