# AZ-T28 Gateway ingress, egress and evidence

Step 28 uses the Gateway and N04 Terraform contract and the scoped ARM and redacted reporting helpers from Step 26/30. No deployment, Azure runtime check, or independent acceptance was performed. Azure acceptance is **0/1,716**, signatures **0**, and release **NO_GO**.

## Configuration checks

The executable profile is the repository's private-only WAF_v2 with Network Isolation. The approved scope ties the exact Gateway, delegated subnet, private static frontend, HTTPS listener and associated NSG to the target VNet. The environment owner must review feature/region support and supply an isolation reference. The observer does not infer feature enablement from the SKU. Non-isolated GatewayManager and outbound Internet rules differ, so other profiles remain NOT_READY. The supported isolation profile requires AzureLoadBalancer, lacks a legacy GatewayManager dependency, and checks bounded egress dependencies individually.

Rules are read from the exact NSG; available custom and standard default rules are sorted by direction and numeric priority. The inventory distinguishes default rules from custom rules, rejects priority collisions, compares the approved priority list, and requires a custom fallback deny ahead of inherited defaults. An allow must cover the entire approved CIDR/port region in this checker. An earlier opposite rule intersecting even part of the region fails. Matching fragments split across several rules may need manual review. Exact labels and the documented IPv4 AzureLoadBalancer probe address are understood. Dynamic Service Tag or ASG membership that might affect precedence returns NOT_READY, pending a reviewed expansion. No live effective NIC rules, AVNM rules, peering/BGP or platform routes are inferred from this check.

Egress permits must match explicit reviewed purpose, destination, protocol and port. A route table may be null if that is the approved design. Associated custom routes and next hops are compared to the declared baseline, including a declared default route. Effective forced tunneling, BGP-learned defaults, route propagation, return-path behavior and Gateway SKU/regional support require source-side observations and owner review. The current Terraform puts optional forced tunneling on the App Service outbound subnet, not the Gateway subnet.

References: [Private Application Gateway deployment](https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-private-deployment), [Application Gateway infrastructure configuration](https://learn.microsoft.com/en-us/azure/application-gateway/configuration-infrastructure), [service tags](https://learn.microsoft.com/en-us/azure/virtual-network/service-tags-overview).

## Input and execution

Use the incomplete public template specs/azure-gateway-step28.example.json in protected storage and populate only approved nonproduction inputs. IDs, CIDRs, private IPs, priorities and dependency destinations must be explicit. The complete [build-input checklist](azure-build-readiness-inputs.md) records owner decisions and which tests they block. ARM modes require workload identity with exact approved subscriptions/targets. Unreadable, missing or paged data is NOT_READY, and 403/404 does not establish absence. Each mode writes a new directory with sanitized results.json and junit.xml, including test IDs, types and reasons with no hostnames, IPs, resource IDs or raw responses.

```bash
# C: offline input shape
python3 -B scripts/azure_gateway_step28.py --check-config --config "$GATEWAY_CONFIG" --out "$OUT/config"
# A: explicitly enabled ARM GET, no writes
python3 -B scripts/azure_gateway_step28.py --live --config "$GATEWAY_CONFIG" --out "$OUT/arm"
# P: one authorized source-bound TCP/443 connection
python3 -B scripts/azure_gateway_step28.py --probe --config "$GATEWAY_CONFIG" --out "$OUT/tcp"
# F: content-only flow evidence review
python3 -B scripts/azure_gateway_step28.py --review-flow --config "$GATEWAY_CONFIG" --evidence "$FLOW_EXTRACT" --out "$OUT/flow"
# B: protected backend health and hostname/SNI configuration extract
python3 -B scripts/azure_gateway_step28.py --review-backend --config "$GATEWAY_CONFIG" --evidence "$BACKEND_EXTRACT" --out "$OUT/backend"
# Q: protected approved NSG change activity extract
python3 -B scripts/azure_gateway_step28.py --review-changes --config "$GATEWAY_CONFIG" --evidence "$CHANGE_EXTRACT" --out "$OUT/changes"
# R: review platform and isolation fields; decisions still belong to the owner
python3 -B scripts/azure_gateway_step28.py --review-policy --config "$GATEWAY_CONFIG" --evidence "$REVIEW_EXTRACT" --out "$OUT/review"
# S: no Azure and no network
python3 -B tests/test_azure_gateway_step28.py --evidence "$OUT/synthetic"
```

- **P/F:** Protected probe fields are direction, approval_ref, vantage_approved, source_ip, runner_cidr and destination_ip. Destination must match the approved frontend. Deny requires isolated_deny_approved and an explicitly approved test CIDR outside the permitted client ranges. If no connection is established, result is NOT_READY, including timeouts. An unexpected connection from an isolated denied source is FAIL. A TCP connection does not measure HTTPS. For F, use the [Step 26 extract contract](azure-private-endpoint-step26.md#execution) with observed_at and probe_ref in the same config. It checks tuple, time and expected decision. Actual flow collection, authenticity and coverage still require review.
- **B:** Config backend includes pool_id, settings_id, address and hostname. The approved extract includes gateway_id, scope_complete, pool_id, settings_id, address, health, configured_hostname and configured_sni. This compares a protected extract from a separately authorized backend-health run, and does not invoke the Azure backend-health action or verify actual TLS SNI on the wire.
- **Q:** Config changes includes offset-qualified start/end and tickets, each with event_id, actor_ref, operation and ticket_ref. Approved extract includes the same start/end, review_ref, collection_complete and events with those correlation fields plus resource_id, observed_at and status. Matching rows leave collection completeness, signature and actor authenticity to the reviewer.
- **R:** Extract fields topology_ref, sku, network_isolation and gateway_manager_required describe the reviewed deployment profile. Optional change_controls must mark no_production_nsg_mutations and nonproduction_boundary_approved true, with an approval_ref. Human approval remains NOT_READY in this tool.

## 22 original cases

S is executed in offline CI. ARM/TCP observations and reviewed operational evidence are NOT_RUN. No configuration observation, synthetic result, or successful extract is counted as Azure acceptance.

| ID | Original requirement | Route | Expected evidence / unmet scope |
|---|---|---|---|
| AZ-T28-01 | Only approved corporate CIDRs can initiate required gateway HTTPS traffic | A + P | Approved Gateway and client CIDRs; config evidence verifies region and precedence. Single allow TCP is distinct. |
| AZ-T28-02 | Only approved corporate CIDRs can initiate required gateway HTTPS traffic | S | Synthetic earlier partial deny must be detected. |
| AZ-T28-03 | All 443 allow-rule source ranges match the signed client CIDR list | A | Exact signed inbound client source list; no wildcard permit. |
| AZ-T28-04 | All 443 allow-rule source ranges match the signed client CIDR list | S | Synthetic broad CIDR rejected. |
| AZ-T28-05 | Required AzureLoadBalancer control traffic is supported and rule precedence checked | A | Platform tag/source matched and earlier covering rules evaluated. |
| AZ-T28-06 | Required AzureLoadBalancer control traffic is supported and rule precedence checked | S | Synthetic earlier probe-source deny rejected. |
| AZ-T28-07 | GatewayManager treatment matches network isolation feature state and current supported deployment profile | Owner + R | Owner approves actual SKU/feature support and disposition; R validates declared profile only. |
| AZ-T28-08 | GatewayManager treatment matches network isolation feature state and current supported deployment profile | S | Synthetic inappropriate GatewayManager requirement rejected. |
| AZ-T28-09 | Necessary gateway control-plane egress is present without broad exceptions | A | Scoped destination/port matches with precedence and UDR entries; effective routes remain separate. |
| AZ-T28-10 | Necessary gateway control-plane egress is present without broad exceptions | S | Synthetic wildcard outbound destination rejected. |
| AZ-T28-11 | Effective NSG rule precedence blocks unapproved traffic before it can reach gateway | A + P + F | Approved client and deny ranges plus NSG fallback; TCP timeouts never prove deny; correlated flow needed. |
| AZ-T28-12 | Effective NSG rule precedence blocks unapproved traffic before it can reach gateway | S | Synthetic absent fallback and drift caught; no default bypass. |
| AZ-T28-13 | NSG priority values are unique, valid and ordered as approved | A | Complete default/custom rules and exact approved custom ordering. |
| AZ-T28-14 | NSG priority values are unique, valid and ordered as approved | S | Synthetic priority collision rejected. |
| AZ-T28-15 | Provisioning and operational states meet the healthy baseline | A | Gateway ARM Succeeded/Running; no implied backend reachability. |
| AZ-T28-16 | Provisioning and operational states meet the healthy baseline | S | Synthetic stopped Gateway rejected. |
| AZ-T28-17 | Backend-health result proves intended target is Healthy and hostname/SNI are correct | B | Approved backend export and address/Host/SNI configuration. Running data and TLS wire evidence still needed. |
| AZ-T28-18 | Backend-health result proves intended target is Healthy and hostname/SNI are correct | S | Synthetic wrong SNI in supplied health export rejected. |
| AZ-T28-19 | Negative tests do not mutate production NSGs; approvals define isolated test scope | Owner + R | Owner approves isolation, no production changes and real observer locations. |
| AZ-T28-20 | Negative tests do not mutate production NSGs; approvals define isolated test scope | S | Synthetic unauthorized scope rejected. |
| AZ-T28-21 | Recent NSG changes map to signed tickets and identifiable actors | Q | Approved bounded activity export matches actor/operation/ticket; collection and signatures independently reviewed. |
| AZ-T28-22 | Recent NSG changes map to signed tickets and identifiable actors | S | Synthetic wrong actor rejected. |
