# AZ-T30 Private DNS execution and evidence

Read-only automation for the 22 original Step 30 cases in `specs/phase3_264_en.json`. Azure acceptance is **0/1,716**, independent signatures **0**, release **NO_GO**. This change implements test routes and synthetic detectors. Live Azure and Private Runner testing is **NOT_RUN**.

## Inputs and execution

Copy `specs/azure-private-dns-step30.example.json` into protected storage. The checked-in example deliberately contains no real FQDN, Azure resource ID, resolver IP, or approval. Transfer actual values from the reviewed Terraform DNS/Private Endpoint configuration and Azure inventory. Keep this filled file out of Git and ordinary CI artifacts.

| Input | Hub shared example | New dev example |
|---|---|---|
| `topology`, `approval_ref`, `approved_private_runner` | `hub`, owner approval record and Runner confirmation | `dev`, environment approval record and Runner confirmation |
| `resolver_ips` | Approved hub/forwarding resolvers for this Runner's DNS view | Approved isolated dev resolvers for this Runner's DNS view |
| `targets.*.arm.vnet_id` and `subnet_id` | Actual PE VNet and subnet; set optional `expected_link_vnet_id` when the approved zone link points to a separate hub VNet | Dev PE VNet and subnet; omit `expected_link_vnet_id` if the expected link is to that VNet |
| Zone, link, PE, NIC, service, zone group and record IDs | Use the shared owners' actual scoped IDs | Use dev Terraform outputs and resulting ARM IDs |
| `ordinary_name`, `private_name`, `cname_chain` | Approved normal name and exact ordered aliases ending at the private record | Same. App Service `web` and `scm` are separate records on one PE |
| `expected_private_ips`, `expected_cidrs` | Use approved exact NIC/A-record addresses and allowed RFC1918 CIDRs | Same; neither inferred from environment |
| Workload identity | Protected `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_FEDERATED_TOKEN_FILE` and approved ARM read scope | Same |

The six profile keys are `web`, `scm`, `openai`, `search`, `cosmos`, and `vault`. Fill all profiles for the complete verification route. Partial input marks relevant cases NOT_READY. REST04 verifies the Azure service/subresource, zone/A record, exact link, PE/NIC and address consistency. Mark outputs from active Azure reads as observations for review. The REST04 contract supports one subscription per target graph and an exact approved IPv4 set for that target. Cross-subscription graph support, more than one record/endpoint per non-App profile, IPv6, and Cosmos deployments where a region-specific record represents only part of a NIC's address set require a separately validated mapping. A forwarded lookup does not prove who owns or approves the DNS forwarding configuration.

Commands used by the per-ID mapping below. Use a new output directory for each invocation:

```bash
# C: input shape only; no credentials or network used
python3 -B scripts/azure_private_dns_step30.py --check-config --config "$APPROVED_DNS_CONFIG" --out "$OUT/config"
# L: approved Private Runner only; dig (TCP/53), azure-identity and ARM read scope required
python3 -B scripts/azure_private_dns_step30.py --live --config "$APPROVED_DNS_CONFIG" --out "$OUT/live"
# S: synthetic positive/negative fixtures
python3 -B scripts/azure_private_dns_step30.py --selftest --out "$OUT/synthetic"
# O: optional review of declared ownership evidence
python3 -B scripts/azure_private_dns_step30.py --review-ownership --config "$APPROVED_OWNERSHIP_EXTRACT" --out "$OUT/ownership"
```

Provide the ownership extract as JSON with `complete_for_review: true` and a `zones` list of objects containing `zone`, `dns_view`, `zone_resource_id`, and `owner`. The extract checker rejects duplicates in one visibility domain. A DNS owner must separately attest inventory completeness and confirm that the supplied views really are distinct.

The Runner asks the configured resolver(s) using absolute names, bounded TCP queries, and no user dig configuration. It compares the full A-answer set and owners to approved expected values, separately follows CNAME hops, then checks direct private A records against the approved REST04 PE/NIC. Extra, missing, duplicate or wrong answers fail according to the case, while empty response, NXDOMAIN, SERVFAIL, timeout and inaccessible approved inputs yield NOT_READY with a reason. A pending PE fails the PE/zone-group control and prevents a matching direct private A record from being treated as a PE-bound observation. Successful DNS does not prove TLS, HTTPS, or application behavior.

Every command writes sanitized `results.json` and `junit.xml`. The outputs record test ID, check kind, result and reason without FQDNs, IPs, tokens or raw responses. Synthetic, input-check, ownership and live reports are labeled separately. Exit 0 denotes successful synthetic checks, input shape validation or completed automatic observations. Exit 1 denotes observed mismatches; exit 2 identifies missing prerequisites or pending manual review. The manual ownership row stays NOT_READY in the live report. Use actual protected source records for independent acceptance; these outputs never award Azure acceptance.

## One-to-one case mapping

| ID | Original requirement | Command | Expected evidence and prerequisite |
|---|---|---|---|
| AZ-T30-01 | Private DNS zone privatelink.azurewebsites.net exists and links to required VNet | L | ARM zone objects and exact VNet links for both App Service and SCM; approved records and REST04 input required. |
| AZ-T30-02 | Private DNS zone privatelink.azurewebsites.net exists and links to required VNet | S | Synthetic App Service zone graph, wrong zone identity rejected; JSON/JUnit offline row. |
| AZ-T30-03 | Private DNS zone privatelink.openai.azure.com exists and is appropriately linked | L | ARM zone and approved VNet link for OpenAI; approved REST04 input required. |
| AZ-T30-04 | Private DNS zone privatelink.openai.azure.com exists and is appropriately linked | S | Synthetic OpenAI zone graph, wrong zone identity rejected; JSON/JUnit offline row. |
| AZ-T30-05 | Private DNS zone privatelink.search.windows.net exists and is appropriately linked | L | ARM zone and approved VNet link for Search; approved REST04 input required. |
| AZ-T30-06 | Private DNS zone privatelink.search.windows.net exists and is appropriately linked | S | Synthetic Search zone graph, wrong zone identity rejected; JSON/JUnit offline row. |
| AZ-T30-07 | Private DNS zone privatelink.documents.azure.com exists and is appropriately linked | L | ARM zone and approved VNet link for Cosmos DB; approved REST04 input required. |
| AZ-T30-08 | Private DNS zone privatelink.documents.azure.com exists and is appropriately linked | S | Synthetic Cosmos DB zone graph, wrong zone identity rejected; JSON/JUnit offline row. |
| AZ-T30-09 | Private DNS zone privatelink.vaultcore.azure.net exists and is appropriately linked | L | ARM zone and approved VNet link for Vault; approved REST04 input required. |
| AZ-T30-10 | Private DNS zone privatelink.vaultcore.azure.net exists and is appropriately linked | S | Synthetic Vault zone graph, wrong zone identity rejected; JSON/JUnit offline row. |
| AZ-T30-11 | PE DNS zone group points at the correct private zone and endpoint subresource | L | ARM correct PE service/subresource, approval and DNS zone group; all configured profiles and ARM identity required. |
| AZ-T30-12 | PE DNS zone group points at the correct private zone and endpoint subresource | S | Synthetic zone group referencing the wrong zone is rejected. |
| AZ-T30-13 | VNet links and registration settings match the intended hostnames and network topology | L | ARM linked VNet, registration disabled and successful link provisioning for each approved zone. |
| AZ-T30-14 | VNet links and registration settings match the intended hostnames and network topology | S | Synthetic registration-enabled link is rejected. |
| AZ-T30-15 | Resolver resolves approved ordinary service FQDN to expected private IP | L | On approved resolver(s), each ordinary name's full answer path ends in the exact approved private IP set; explicit FQDNs/IPs/CIDRs and reachable resolver required. |
| AZ-T30-16 | Resolver resolves approved ordinary service FQDN to expected private IP | S | Synthetic missing alias in recursive A answer is rejected. |
| AZ-T30-17 | DNS ownership prevents duplicate conflicting zones across resolvers/VNets | O + owner | Human owner confirms topology completeness and DNS visibility, plus duplicate rejection from O. Keep signed review in protected evidence. |
| AZ-T30-18 | DNS ownership prevents duplicate conflicting zones across resolvers/VNets | S | Synthetic duplicate zone in one DNS view is rejected. |
| AZ-T30-19 | Normal service FQDN follows the expected CNAME chain to private endpoint DNS | L | Explicit CNAME lookup traverses the exact approved aliases for each ordinary name; unexpected final alias rejected. |
| AZ-T30-20 | Normal service FQDN follows the expected CNAME chain to private endpoint DNS | S | Synthetic missing CNAME hop rejected; redirect and loop covered by unit tests. |
| AZ-T30-21 | A response from the internal runner equals the approved PE private IP, never public | L | Direct private record returns exact IP set; REST04 has already checked PE/NIC, approval and pinned A record. Wrong-address, extra and duplicate answers rejected. |
| AZ-T30-22 | A response from the internal runner equals the approved PE private IP, never public | S | Synthetic wrong private A address is rejected; JSON/JUnit offline row. |

All live rows are NOT_RUN. Rows exercised in the synthetic suite are separate from Azure records.
