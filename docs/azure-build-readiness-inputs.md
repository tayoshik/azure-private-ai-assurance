# Build and live-test input checklist

The code fixes the resource roles, scopes and test shape. Inputs below require the environment owner. No real ID, approval, network value or application contract was inferred.

| Input owner must supply | Confirmed in source | Blocked until confirmed |
|---|---|---|
| Nonproduction subscription, region, tenant and scoped owner approvals | Bootstrap/dev roots, AzureRM 4.66.0 locks, WAF_v2 private profile | Actual provider/region feature readiness, backend, real plan and deploy |
| Hub shared or new dev monitor design; AMPLS, DNS zone IDs, owner and forwarding | Terraform supports both modes. Dev uses separate monitor PE subnet and private DNS links | Deploy monitoring, AZ-T30 effective resolution, AZ-T31 query/ingestion |
| Workload VNet, subnet role, non-overlapping CIDRs, approved client and deny ranges, fixed frontend IP | Separate Gateway, Web PE, data PE, outbound App Service subnets; optional new dev Monitor subnet | Terraform IPAM inputs, AZ-T26 zoning and isolated probes, AZ-T28 TCP/443 |
| Network Isolation compatibility, approved NSG ordering/source ranges, DNS/Key Vault/control egress, UDR/default/BGP | N04 per-subnet NSG model, forced-tunnel example belongs to App outbound; Gateway probe posture is isolated WAF_v2 | Real Gateway deployment; AZ-T28 policy scope/effective route tests |
| State DNS/route and bootstrap access, private Runner network and source addresses, OIDC app/tenant/federation subject and least-privilege scopes | Provider pins, separate bootstrap, scoped ARM and explicit Runner entry points | Real backend init, Azure reads and live tests AZ-T26/28/30/31 |
| PE approver and exact deployed target IDs/approved PE NIC IP sets | New dev Monitor PE defaults to manual approval and observers check target/approval | PE-bound DNS and TCP checks against actual assets |
| Logging/flow capture and authentic export format, change approver and backend-health evidence collector | Sanitized JSON/JUnit contracts and offline extract checks | Verified denial, operational logs, alert delivery, backend health and authoritative change records |
| Deployed app, private URL, actual login/identity flow, one real main screen/action and expected result | Configurable Gateway and App Service health paths. Stage 5 identifies app and auth prerequisites; no executable app UI contract was found | Playwright config/spec and authenticated end-to-end journey |

Collect operational inputs in restricted storage. Local input checks are available in [Step 26](azure-private-endpoint-step26.md), [Step 28](azure-gateway-step28.md), [Step 30](azure-private-dns-step30.md) and [Step 31](azure-monitor-private-link-operator.md). They check declared scope and consistency before any actual operation.

## Priority order for owner decisions

1. **P0 — Nonproduction scope and private execution**. Approve subscription/tenant/region, scoped Runner placement, source and DNS/route, backend state access, GitHub OIDC subject and separate roles for read/plan/apply. This unlocks the private bootstrap/backend gate and the first authorized construction pipeline.
2. **P0 — Topology and dependencies**. Select Hub/dev and DNS/PE approval owners, approve CIDRs, actor-specific Entra/Monitor/certificate destinations, Firewall/Proxy and default routing. Code fixes the Azure Public authority/profile and the test input shape. Actual FIC, IPs, route, ID and bypass review remain owner inputs. This blocks real AZ-T26/28/29/30/31.
3. **P1 — Real app and test account contract**. Provide deployed artifact/commit, actual private URL and health path, Entra registration/redirect and audience, approved test account or identity flow, one real screen route/selector, action and expected result. Current Terraform only wires infrastructure, UAI and configurable health paths; Stage 5 records the app, EasyAuth and deployment dependencies as outstanding. Thus there is no verified UI to turn into a Playwright spec.
4. **P1 — Evidence access and supply**. Assign owners of required flow/alert telemetry, independent reviews and REST23 dependency supply. This blocks acceptance and integrated tests.
