# AZ-T26 Private Endpoint subnet and trust boundaries

The Step 26 overlay uses the original 22 cases in specs/phase3_264_en.json. It adds scoped ARM GET checks, a separately enabled TCP probe and an offline flow-extract checker. There was no Azure deployment, no Azure runtime observation and no independent acceptance in this change. Azure acceptance **0/1,716**, independent signatures **0**, release **NO_GO**.

## Approved scope and input check

Copy specs/azure-private-endpoint-step26.example.json to protected storage and fill it from the owner's reviewed inventory. Do not commit a filled manifest. The repo references the dev web ingress PE subnet, the data/Key Vault PE subnet, the separate state bootstrap PE path and, in new-dev mode, the dedicated Monitor PE subnet. Workload web and data subnets have explicit NSG associations; the existing workload forced-tunnel route association is on the **App Service outbound** subnet. A route table on that outbound subnet does not make it a PE-subnet UDR. Available PE policy values are Disabled, Enabled, NetworkSecurityGroupEnabled and RouteTableEnabled. Specify exact approved values and separately name the mechanisms that must apply. An enabled mode by itself establishes neither a rule nor an effective route.

| Decision/input | Existing Hub example | New dev example |
|---|---|---|
| Scope and approver | topology hub, environment nonproduction, approved subscription IDs, owner-approved scope reference | topology dev, nonproduction, approved subscription IDs and owner approval |
| VNet, private subnets and purpose | Owner supplies actual Hub/workload relationship, non-overlapping CIDRs and subnet IDs for each approved purpose | Populate from the Terraform modules and approved IPAM. Separate web, data and optional dedicated monitoring purposes and IDs. Bootstrap owned separately |
| DNS owner | Hub owns its shared DNS and details of VNet forwarding/visibility. Use the [AZ-T30 input and ownership contract](azure-private-dns-step30.md) | Dev owns its isolated DNS view and must check overlap with bootstrap and Hub records |
| PE/NIC/approval | Exact PE, NIC, service, group, private IP list and network owner responsible for PE approval | Use the new resources' resulting IDs and actual approved IPs. Keep manual approvals pending until Azure reports Approved |
| NSG, ASG and UDR | Record exact associated IDs or explicit null; list expected custom routes, source CIDRs and ASG IDs, tested scope and policy mode | Derive planned roles from Terraform; owners approve actual CIDRs, applied policies and the route/next-hop baseline |
| Private Runner/OIDC | Owner supplies federation subject, Azure ARM reader scope, protected token and isolated allow/deny vantages | Same, for the approved dev network. Verify source addresses are bound locally and other routes are understood |
| Effectiveness and flow logging | Identify source-side effective routes/policies and approved flow capture/equivalent | Decide whether VNet Flow Logs or an approved equivalent will provide evidence; no flow resources are created by this work |

The input contract is strict about canonical IDs, target service/subresource, CIDRs within RFC1918, declared endpoint purpose, unique PE/NIC/IP placement and overlapping subnets within one VNet. The code does not infer environment names, IDs or approval values. Where a rule uses an ASG, the approved source/destination references and PE/NIC membership are checked within the scoped inventory. Effective privileges, source membership and other layers of network policy remain separate checks.

## Execution

Use a distinct new output directory for each command:

```bash
# C: syntax/approval fields only; no network or secrets
python3 -B scripts/azure_private_endpoint_step26.py --check-config --config "$APPROVED_PE_CONFIG" --out "$OUT/config"
# A: only explicit scoped ARM GET; configure Azure workload identity outside the repository
python3 -B scripts/azure_private_endpoint_step26.py --live --config "$APPROVED_PE_CONFIG" --out "$OUT/arm"
# P: one explicit protected endpoint and explicitly authorized isolated vantage only
python3 -B scripts/azure_private_endpoint_step26.py --probe --config "$APPROVED_PE_CONFIG" --out "$OUT/tcp"
# F: offline comparison against an approved flow extract; no Azure access
python3 -B scripts/azure_private_endpoint_step26.py --review-flow --config "$APPROVED_PE_CONFIG" --flow "$APPROVED_FLOW_EXTRACT" --out "$OUT/flow"
# S: synthetic cases with paired positive/negative fixtures and per-ID evidence
python3 -B tests/test_azure_private_endpoint_step26.py --evidence "$OUT/synthetic"
```

A and P require the REST02 workload-identity environment (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_FEDERATED_TOKEN_FILE and approved azure-identity dependency). A uses exact resource IDs and never lists an entire subscription or follows an unexpected nextLink. The subnet's PE inventory, NSG rules and UDR entries must be supplied by complete resource responses. Missing properties, unreadable resources and paged/incomplete projections stay NOT_READY. A 403 or 404 can mean scope/permissions and cannot establish absence. The implementation compares exact approved associations, NSG allow sources and TCP/443 destinations, explicit fallback denies, route entries and ASG references. Scope is limited to the declared dedicated PE subnets and approved resources.

P requires isolation_approved true and a protected probe object with direction allow or deny, runner_approval_ref, probe_approval_ref, zero-based subnet_index and endpoint_index, source_ip, runner_cidr and exact destination_ip from the approved PE inventory. For allow use an approved source CIDR or source_asg_id. For deny, use isolated_deny_approved and outside_approved_source_asgs true, with a source outside approved allow CIDRs. Establish membership and location through the owner first. Only one source-bound TCP/443 connection is attempted after ARM confirms PE, NIC and subnet; it sends no application data. Failure to connect is NOT_READY, including a deny-side timeout. A deny-side connection is an explicit mismatch. Neither case measures effective route selection, TLS, HTTP or broader reachability.

F takes the same probe input plus observed_at (ISO timestamp with offset) and probe_ref (protected correlation reference). Supply an approved JSON extract with review_ref and records containing probe_ref, source_ip, destination_ip, port, protocol, decision and observed_at. It checks a single scoped record within two minutes of the approved probe time and requires the probe timestamp within the review window. Owners still need actual flow-log collection, provenance and completeness. Do not infer a denial from a manual label or use this checker as a substitute for collecting the flow records.

Outputs are JSON and JUnit with ID, check type, result and reason. The report distinguishes configuration, TCP, flow-extract and synthetic modes, and omits resource IDs, names, IPs and raw responses. Exit 1 indicates a mismatch, exit 2 a missing prerequisite or unresolved observation. Successful command completion does not assign Azure acceptance.

## 22-case mapping

All live rows are NOT_RUN. The two TCP probes augment configuration checks for 11 and 13; they do not cover every source address. The manual isolation approval for case 21 remains an owner decision preflighted by C/P.

| ID | Original requirement | Route | Expected evidence and remaining scope |
|---|---|---|---|
| AZ-T26-01 | Private endpoints are assigned to trust-zone subnets per approved service segmentation | A | Subnet CIDR, declared purpose and full in-scope PE list agree; PE/NIC placement is checked. |
| AZ-T26-02 | Private endpoints are assigned to trust-zone subnets per approved service segmentation | S | Synthetic wrong subnet rejected. |
| AZ-T26-03 | PE subnet has intended NSG and routing policy association | A | Exact approved NSG and UDR association or explicit absence. |
| AZ-T26-04 | PE subnet has intended NSG and routing policy association | S | Synthetic wrong association rejected. |
| AZ-T26-05 | Private endpoint network-policy mode enables required enforcement and is reviewed for platform support | A | Observed mode matches approved mechanisms and subnet policy; platform approval remains an input. |
| AZ-T26-06 | Private endpoint network-policy mode enables required enforcement and is reviewed for platform support | S | Synthetic wrong enforcement mode rejected. |
| AZ-T26-07 | UDR association and effective routing preserve intended private paths | A | Exact association and approved UDR route entries; effective source NIC route needs independent evidence. |
| AZ-T26-08 | UDR association and effective routing preserve intended private paths | S | Synthetic wrong route association rejected; regression also covers wrong next hop. |
| AZ-T26-09 | Every endpoint has a unique private IP in the approved range and matches its NIC | A | Exact scoped NIC addresses inside CIDRs and unique in each VNet, approved connection/subresource. |
| AZ-T26-10 | Every endpoint has a unique private IP in the approved range and matches its NIC | S | Synthetic wrong private IP rejected. |
| AZ-T26-11 | Only approved source CIDRs/ASGs can reach the PE according to effective policy and tests | A + P | Approved NSG source sets; source-bound allow probe observes a single tuple when approved. |
| AZ-T26-12 | Only approved source CIDRs/ASGs can reach the PE according to effective policy and tests | S | Synthetic overbroad source rule rejected. |
| AZ-T26-13 | Unapproved source paths are rejected by effective rules and isolated runtime observations | A + P + F | Explicit NSG fallback deny; isolated deny probe fails on any connection. Collect corroborating flow evidence. |
| AZ-T26-14 | Unapproved source paths are rejected by effective rules and isolated runtime observations | S | Synthetic missing fallback deny rejected; runtime timeout is not accepted. |
| AZ-T26-15 | Allowed PE traffic uses approved ports and has no unexpected broad permit | A | Scoped TCP/443 allow configuration only, with approved sources and destinations. |
| AZ-T26-16 | Allowed PE traffic uses approved ports and has no unexpected broad permit | S | Synthetic broad port allowance rejected. |
| AZ-T26-17 | ASG membership agrees with PE NICs and NSG source/destination references | A | Approved endpoint and NIC ASG membership and configured inbound references; effective source membership requires reviewed inventory. |
| AZ-T26-18 | ASG membership agrees with PE NICs and NSG source/destination references | S | Synthetic mismatched ASG rejected. |
| AZ-T26-19 | VNet Flow Logs or approved equivalent demonstrate scoped PE-path traffic outcomes | F | Protected extract contains the actual approved probe tuple, time and expected decision; collection/provenance remain manual or separate integration. |
| AZ-T26-20 | VNet Flow Logs or approved equivalent demonstrate scoped PE-path traffic outcomes | S | Synthetic valid and stale timestamp extracts checked. |
| AZ-T26-21 | All deny tests are confined to isolated non-production targets with authorization | Owner + C | Owner signs nonproduction isolation approval and independent allow/deny vantages before P. The checker can require fields, but cannot approve the exercise. |
| AZ-T26-22 | All deny tests are confined to isolated non-production targets with authorization | S | Synthetic missing deny approval rejected. |

Design references: [Azure PE network policy configuration](https://learn.microsoft.com/en-us/azure/private-link/disable-private-endpoint-network-policy), [Azure PE connectivity diagnosis](https://learn.microsoft.com/en-us/troubleshoot/azure/private-link/troubleshoot-private-endpoint-connectivity-failure), and the repository's infra/modules/network and infra/modules/monitoring.
