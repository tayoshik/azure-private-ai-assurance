# N04 Implementation Self-Review — 2026-11-14

**Scope:** stage-one code reused without re-proving the previous 14/14 offline tests. N04 adds four NSGs, explicit rules and associations, optional App integration UDR, variable contracts and review gates.

## Review findings

| ID | Severity | Topic | Outcome |
|---|---|---|---|
| N04-R01 | P0 | Gateway feature/approved egress before restrictive NSG | Code gated by `gateway_network_isolation_approved`, `gateway_egress_profile_approved`, `network_policy_approved` (default false). NOT a live approved control. |
| N04-R02 | P0 | App outbound deny all can break identity/monitor/package/CRL and platform health | Gated by `app_egress_profile_approved` and `network_policy_approved`. Must not apply until real dependencies documented and tested. |
| N04-R03 | P1 | PE NSG cannot replace data-plane authorization | Separate web/data PE NSGs; actual app/AI RBAC testing remains OPEN. |
| N04-R04 | P1 | Forced tunnelling may alter paths | Optional App integration subnet only; no Gateway UDR. Firewall IP and owner approval required. |
| N04-R05 | P1 | CIDR overlap is not proven by HCL `cidrhost` | Signed IPAM required and cross-checked later with actual route/subnet inventory. |
| N04-R06 | P1 | Dev tfvars example contains hypothetical CIDRs | All flags false and zero subscription. Example must not be used for apply. |
| N04-R07 | P1 | `azurerm` pinned provisionally at 4.66.0 | No Terraform executable/provider packages installed here; only lexical/contract validation, NOT `fmt/validate/plan`. |
| N04-R08 | P1 | PE subnet policy must be Enabled for PE NSGs | Stage1 resource declarations retained; static test checks this. Verify effective policies in real Azure. |
| N04-R09 | P2 | DNS source to Azure platform DNS depends on topology | Custom resolver addresses optional; review chosen VNet DNS behavior and logs prior to rollout. |
| N04-R10 | P1 | Bootstrap local state custody still needs secure CI procedure | No self-referential backend. B05 remains NOT_READY; no real backend migration or apply. |

## Test boundary

Static tests can demonstrate contract texts, unique priorities, separate subnet associations and refusal of unsafe source changes. They **cannot** prove service reachability, effective NSG rules, provider schema compatibility, quota, actual deployment or platform health. `Azure live PASS = 0`, `1,716 tests = NOT_READY`, `release = NO-GO`.
