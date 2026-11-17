# O02 Azure Monitor Private Link

This is a substantive Terraform and Azure assurance change for construction Step 31. Release remains **NO_GO** with **0/1,716 Azure acceptance** and zero independent signatures. Step 32 monitoring coverage and end-to-end application tests remain separate work.

## Topology and ownership

The baseline documents require an approved AMPLS/DNS design and describe the optional O02 building block. No approved Hub IDs or DNS ownership decision were found. Set the dev root input `monitoring_private_link.mode` to `hub` or `dev` only after the topology has been reviewed. The default `disabled` retains the existing workspace and its public query/ingestion restrictions without creating Private Link resources. The existing `monitoring_private_ingestion_approved` and Gateway diagnostics prerequisites still apply.

| Mode | Workload Terraform owns | Deployment dependencies |
|---|---|---|
| `hub` | Workspace association to the supplied AMPLS. | Hub owner supplies AMPLS, already-approved PE, and all five zone IDs. The Hub owner maintains zone-group records, VNet links/forwarding and access mode. The association uses the AzureRM provider's subscription, so the Hub scope must be in that subscription. Cross-subscription scope onboarding belongs in a separately authorized owning stack. |
| `dev` | AMPLS, Workspace association, dedicated PE subnet and NSG, manual-by-default PE to subresource `azuremonitor`, five Private DNS zones and their workload VNet links. | Approved IPv4 subnet CIDR within the workload VNet, /27 or larger, outside existing subnets, scoped HTTPS client CIDRs, and a genuinely isolated DNS boundary. Reserve PE IP capacity. Approve forwarders/routes for any peered Runner and ensure public outbound Monitor access follows policy. |

The five zones are `privatelink.monitor.azure.com`, `privatelink.oms.opinsights.azure.com`, `privatelink.ods.opinsights.azure.com`, `privatelink.agentsvc.azure-automation.net`, and `privatelink.blob.core.windows.net`. Check the Blob zone against the separate state bootstrap network as well as the Hub DNS. Creating duplicate zones in a shared DNS view can break Monitor or state resolution. In Hub mode, review any endpoint overrides and DNS consumers before linking the Workspace. In dev mode, set `dev_isolated_dns` only after confirming these boundaries. The PE uses a zone group, so Azure manages endpoint DNS records. Zone links have registration disabled.

New AMPLS instances default to PrivateOnly for both ingestion and query. The Workspace blocks public data-plane ingestion and query in every mode. ARM and Entra access have separate egress/identity requirements. Gateway diagnostic settings deliver logs through an Azure-managed path. Seeing those logs does not demonstrate that an agent has ingested through AMPLS; independently verify any approved Application Insights, DCE or client-ingestion flow when applicable.

### Configuration examples

Use reviewed variables in a protected environment. The following sketches intentionally omit actual deployment inputs and leave approvals false.

```hcl
# Existing Hub topology
monitoring_private_link = {
  mode              = "hub"
  topology_approved = false
  hub_scope_id      = null # Approved AMPLS ARM ID
  hub_endpoint_id   = null # Approved existing Private Endpoint ARM ID
  hub_zone_ids      = {}   # Map of all five zone names to approved ARM IDs
}
```

```hcl
# Dedicated dev topology
monitoring_private_link = {
  mode                = "dev"
  topology_approved   = false
  dev_isolated_dns     = false
  dev_subnet_cidr      = null # Approved /27 or larger subnet inside the workload VNet
  dev_client_cidrs     = []   # Approved clients including the Private Runner
  dev_manual_approval  = true
}
```

Explicit approval must exist before requesting any real infrastructure change. The dev PE defaults to manual approval. Its connection being present or the configuration being valid is insufficient for live checks. Request automated approval only when the owner has authorized the provisioning identity's permissions. Treat mode transitions as migrations; review the consequences for the association, DNS ownership, and any change affecting the existing PE or Workspace before accepting a plan.

The `monitoring_private_link` output gives the selected mode, scope and scoped Workspace IDs, PE ID, DNS zone IDs, and dedicated dev subnet ID. The existing Workspace and Gateway diagnostic settings retain their addresses. Take target GUIDs and endpoint IPs from the authorized Azure inventory. Keep environment outputs and state in restricted storage.

## Tool versions and offline checks

Terraform **1.9.8** is the workflow pin. Both `infra/bootstrap/.terraform.lock.hcl` and `infra/environments/dev/.terraform.lock.hcl` adopt the existing R5 lock candidate for **HashiCorp AzureRM 4.66.0**. Provider installation verified the signed distribution on linux_amd64. Keep both locks read-only during normal CI. This schema compatibility check leaves target subscription/region readiness and provider upgrades to their separate reviews.

```bash
python3 -B scripts/validate_package.py
python3 -B -m unittest discover -s tests -p 'test_azure_monitor_private_audit.py' -v
terraform fmt -check -recursive infra/modules/monitoring
terraform fmt -check -recursive infra/environments/dev/tests
terraform fmt -check infra/environments/dev/main.tf infra/environments/dev/monitoring-private-link*.tf
for root in infra/bootstrap infra/environments/dev; do
  terraform -chdir="$root" init -backend=false -input=false -lockfile=readonly
  terraform -chdir="$root" validate
done
terraform -chdir=infra/environments/dev test -filter=tests/monitoring_private_link.tftest.hcl
```

These Terraform tests use only the mocked provider with `command = plan` and do not run an Azure plan. The read-only [offline workflow](../.github/workflows/azure-monitor-private-link-offline.yml) runs on relevant pushes and manual dispatch. Use [the Step 31 assignment table](azure-monitor-step31-mapping.md) and [the sanitized implementation report](azure-monitor-implementation-report.md) for the evidence boundary.

## Private Runner live run

1. Use an approved nonproduction Runner with an approved workload identity, Azure CLI-free OIDC federation with `azure-identity`, and routes to the listed PE addresses. Pin/install `azure-identity` from the organization's approved dependency source. Provide `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_FEDERATED_TOKEN_FILE` via protected configuration. The identity needs reads on the explicit ARM resources and Log Analytics query privileges for the Workspace and table. Review effective RBAC separately.
2. Copy `specs/azure-monitor-private-audit.example.json` to restricted storage. Populate the topology, allowed subscriptions, approved tenant and application client ID, approved Run/Query/log-source references, exact AMPLS, Workspace, association, PE, DNS zone-group and Gateway ARM IDs. Supply the exact five approved zone IDs and endpoint RFC1918 IPv4 addresses from the approved PE. Use canonical ARM paths starting with lowercase `/subscriptions/`. The Workspace GUID is the Workspace's customer ID. The transaction GUID is the approved Gateway transaction identifier. Use a recent transaction from an approved test flow; the audit never generates a transaction or sends a log.
3. Run `python3 -B scripts/azure_monitor_private_audit.py --live --config "$APPROVED_MONITOR_CONFIG"`. Execution without explicit arguments exits 2. The runner checks control-plane configuration, then resolves the canonical Logs API and workspace OMS/ODS names to approved IPs, verifies TCP/TLS with hostname validation, and issues a bounded read-only Logs query over that same pinned private path. It correlates the Gateway ARM ID and transaction GUID in `AGWAccessLogs`. The output includes control IDs and status only. Keep raw credentials, Azure IDs, raw service responses and diagnostic logs out of the repository.
4. `OBSERVED_NOT_ACCEPTED` means the listed runtime observations completed. Missing auth, targets, approvals, approved DNS, connectivity or the expected record produce exit 2 with a reason. Independent review is still required to award acceptance. No cases earn Azure PASS through this script. Use Playwright for the separately approved authenticated application flows.

### Required input and validation

| Input | Hub shared | Dev new | How to check before requesting execution |
|---|---|---|---|
| Tenant/subscription | Workspace and Hub scope in provider subscription; list any other approved read subscriptions. | Approved nonproduction provider subscription. | Check Azure resource IDs and OIDC tenant; use C below. |
| AMPLS and Workspace | Owner supplies existing scope, monitored Workspace and scoped association. | Terraform creates scope and association. | Review scope mode, enrollment permissions and access overrides. |
| DNS owner and 5 zone IDs | Hub manages zones, PE zone group, VNet links and forwarding. | Workload DNS owner confirms isolation, including bootstrap Blob DNS, before links are created. | Compare exact zone IDs and check canonical resolution from actual Runner. |
| VNet/subnet and clients | Hub controls existing PE subnet; confirm peering and routes. | Dedicated /27-or-larger IPv4 subnet in workload VNet, scoped HTTPS CIDRs. | Review IPAM and overlap against VNet and bootstrap; Terraform mock checks input contract only. |
| Runner route and IPs | Reach the existing PE and route to approved ARM/Entra endpoints. | Reach provisioned PE from approved client CIDRs. | In restricted config, supply exact PE IPs. Live probe checks DNS, TLS and connection. |
| OIDC / log queries | Approved tenant, client identity, protected token file, ARM/Law reader and marker. | Same. | Check federation subject and effective scopes; verify no CI secret enters source. |
| PE approval | Hub owner supplies existing approved connection. | Default is manual approval by the scope/network owner. | Live ARM must observe Approved for the exact PE/AMPLS subresource. DNS or an existing PE alone does not establish approval. |

Before live execution, use `python3 -B scripts/azure_monitor_private_audit.py --check-config --config "$APPROVED_MONITOR_CONFIG"`. The checked-in example is intentionally incomplete. This validates typed topology, exact resource IDs and subscription allowlists without accessing Azure. The `hub` and `dev` Terraform sketches above plus their mocked tests validate separate creation contracts.

Optional read-only observations take `optional_observations.app_insights_id`, `query_role` (assignment_guid, principal_id, definition_guid), and `absence_alert` (rule_id, action_group_id, criteria_sha256). Hash the reviewed ARM criteria object using UTF-8 JSON with sorted keys and compact separators. Use protected inputs. App Insights binding, exact direct assignment, and enabled alert wiring are configuration observations. Review role inheritance and actual alert delivery independently.

### Deletion and changes in ownership

Hub mode changes the workspace association in the shared scope. It does not manage Hub zones, links, scope settings or endpoint. Linking or unlinking the Workspace changes which assets and DNS records the Hub publishes; coordinate such changes with its owner. Dev manages the isolated DNS records, links, subnet/NSG and PE, so removal can interrupt monitoring queries. The workspace, association and managed scope/PE/DNS resources use prevent_destroy with their declarations in place; decommissioning or crossing topologies requires a reviewed migration. Remove the scope association before attempting Workspace deletion. Review destroys across state operations, because removing the resource declaration also removes its lifecycle guard. Pending manual PE approval and logged diagnostics never imply working private queries.

### Troubleshooting

| Symptom | Investigate |
|---|---|
| Scope, association, or publicly reachable Workspace mismatch | Check Hub enrollment, API visibility, correct workspace customer ID, public query/ingestion flags, and AMPLS access modes/overrides. |
| Pending PE or mismatched zone group | Ask the owner to check the expected AMPLS ID and `azuremonitor` subresource. Confirm all five zone IDs and the private DNS forwarding chain. |
| Public or unexpected DNS, or TLS failure | Check split DNS/VNet links, resolution from the actual Runner, endpoint IPs, NSG/routes, proxy bypass for Monitor data-plane traffic, and TLS trust/SNI. Preserve hostname validation and private-only controls. |
| HTTP 401/403 or missing log | Check workload identity binding and Workspace/table privileges, approval and time window, diagnostic category, table mode and transaction ID. Retry after addressing the observed cause; the query window and retries are bounded. |

References: [Azure Monitor Private Link configuration](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/private-link-configure), [topology and access modes](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/private-link-design), [Logs REST authentication](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/api/access-api), and [AGWAccessLogs columns](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/agwaccesslogs).
