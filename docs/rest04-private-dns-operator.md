# REST04 — Private Endpoint / Private DNS Read-only Assurance

**Date:** 2026-11-14  
**State:** OFFLINE SYNTHETIC PASS ONLY; live Azure accepted = **0**; all original 1,716 live test cases = **NOT_READY**; release = **NO-GO**.  
**Runner decision:** No self-hosted CI runner exists. GitHub-hosted runners execute **only offline fixtures** in this stage.

## 1. Purpose and source reuse

Use the existing REST01 six source catalogues (1,716 IDs), REST02 `AzureReadOnlyClient` and REST03 digest/assessment conventions. No duplicate or replacement canonical test catalogue is introduced. REST04 is a *reusable assessor*, not a claim that any individual catalogue ID has been implemented or accepted. The six original test sources and existing Terraform validation remain untouched.

### Trust boundaries

- The collector can compare only **ARM control-plane configuration**. Correct configuration is not proof that approved users resolve private addresses or that TLS/HTTPS reaches the backend.
- Each target explicitly specifies exact PE, NIC, DNS zone group, DNS zone, Private DNS A-record, and DNS VNet link resource IDs, plus service, subnet, VNet, Private Link group, expected A-record FQDN and RFC1918 IPs.
- The manifest is approved and stored privately **outside public GitHub** for real environments; `specs/rest04-manifest.example.json` uses synthetic identifiers only.
- All six REST GET operations use `get_resource()` from REST02 with pinned `api-version` and approved subscription scope; no write methods or arbitrary URLs. The CLI itself has **no live mode**.
- ARM responses are digested and scoped to resource IDs. Only hash values and generic check names are emitted, not ARM payloads, access tokens, actual private IPs or resource IDs.
- API versions in the initial profile: Network and NIC and DNS zone group **2025-05-01**; Private DNS zone, A record and VNet link **2018-09-01**. Confirm provider/cloud/version applicability before any real collection.

### Supported service/zone bindings (public Azure cloud)

| Private Link group | Service ARM type | Expected private DNS zone |
|---|---|---|
| `sites` | `Microsoft.Web/sites` | `privatelink.azurewebsites.net` |
| `account` | `Microsoft.CognitiveServices/accounts` | `privatelink.openai.azure.com` |
| `searchService` | `Microsoft.Search/searchServices` | `privatelink.search.windows.net` |
| `Sql` | `Microsoft.DocumentDB/databaseAccounts` | `privatelink.documents.azure.com` |
| `vault` | `Microsoft.KeyVault/vaults` | `privatelink.vaultcore.azure.net` |
| `blob` | `Microsoft.Storage/storageAccounts` | `privatelink.blob.core.windows.net` |

Other clouds, cross-subscription DNS hubs, multi-NIC endpoints, multi-zone configurations, and IPv6 are **not yet supported by this strict assessor**. Record an explicit `NOT_READY` design extension rather than falsely passing.

## 2. Detailed validation checks

| Check | ARM GET source and properties | Expected | Failure handling |
|---|---|---|---|
| PE target and authorization | `privateEndpoints/{pe}` → `privateLinkServiceConnections[]` / `manualPrivateLinkServiceConnections[]` | Approved; exact target ID and single approved `groupIds` | `FAIL_POLICY_OBSERVED` for a proven mismatch, `NOT_READY` for missing fields |
| PE subnet and NIC reference | PE `properties.subnet.id` / `networkInterfaces[].id` | Exact approved subnet and NIC | No inference from an arbitrary NIC list index |
| NIC PE reference and IP | `networkInterfaces/{nic}` → `properties.privateEndpoint.id`, `ipConfigurations[]` | Exact PE and subnet, exact RFC1918 IP set, no configured public IP | Keep expected IPs in approved restricted baseline |
| DNS Zone Group | `privateEndpoints/{pe}/privateDnsZoneGroups/{group}` → `privateDnsZoneConfigs[]` | Exact approved private DNS zone, provisioning succeeded | A zone group alone is insufficient |
| DNS Zone | `privateDnsZones/{zone}` | Exact resource ID and type | Missing/incorrect evidence => `NOT_READY` |
| Private A-record | `privateDnsZones/{zone}/A/{record}` → `aRecords[].ipv4Address` | Exact same approved NIC IP set | Extra, public, or mismatched IP => failure |
| VNet Link | `privateDnsZones/{zone}/virtualNetworkLinks/{link}` | Approved VNet ID, completed/succeeded, no auto registration | Confirm central/hub resolver design separately |
| Read integrity | Each REST02 `OBSERVED_NOT_ACCEPTED` object and SHA-256 | Six complete, same approved scope, exact expected types | Missing/inconsistent => `NOT_READY` |

**Status semantics:** `PASS_OFFLINE_FIXTURE_ONLY` is only for synthetic known-good fixture. Actual observed safe ARM config returns `OBSERVED_PENDING_PRIVATE_DNS_PROBE` with `azure_live_acceptance=NOT_READY`; any verified unsafe value returns `FAIL_POLICY_OBSERVED`; missing data returns `NOT_READY`. The same control must be independently reviewed before acceptance. Never promote synthetic PASS to live PASS.

## 3. WSL2 offline procedure — one paste, no Azure account access

```bash
cat <<'CATEOF' > /tmp/run_rest04_offline.sh
#!/usr/bin/env bash
set -Eeuo pipefail
REPO="$HOME/azure-private-ai-assurance"
OUT="$HOME/azure-private-ai-assurance-qa/rest04"
mkdir -p "$OUT"
cd "$REPO"
git pull --ff-only
printf '%s\n' "$(git rev-parse HEAD)" > "$OUT/commit.txt"

# 1. Selftest: good fixture, denied connection, missing SHA and no DNS-runner proof
python3 scripts/rest04_private_dns_audit.py --selftest | tee "$OUT/selftest.json"

# 2. Full six-resource synthetic fixture; no HTTP and no Azure credentials
python3 scripts/rest04_private_dns_audit.py \
  --fixture specs/rest04-synthetic-fixture.json | tee "$OUT/fixture.json"

# 3. REST01–REST04 regression including REST02's HTTP 403/429 mocks
python3 -m unittest discover -s tests -p 'test_*rest*.py' -v 2>&1 \
  | tee "$OUT/rest-unittest.log"

# 4. Existing Terraform regressions, preserving prior success history
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v 2>&1 \
  | tee "$OUT/terraform-regression.log"

# 5. Catalogue integrity and independent evidence digest
python3 scripts/verify_publication.py | tee "$OUT/catalogue.log"
(cd "$OUT" && sha256sum commit.txt selftest.json fixture.json \
    rest-unittest.log terraform-regression.log catalogue.log) \
  | tee "$OUT/SHA256SUMS.txt"
echo 'PASS_OFFLINE_REST04_ONLY: Azure live acceptance remains NOT_READY'
CATEOF
bash /tmp/run_rest04_offline.sh
```

**Expected:** `--selftest.status=PASS_OFFLINE_FIXTURES_ONLY` and `good=PASS_OFFLINE_FIXTURE_ONLY`, `bad=FAIL_OFFLINE_POLICY_FIXTURE`, `missing=NOT_READY`; fixture-only `PASS_OFFLINE_FIXTURES_ONLY`. Regression test counts depend on the checked-out commit; verify all tests `OK`. `verify_publication.py` must retain 1,716 IDs. Logs and checksums are stored outside the public repository.

## 4. Failure and troubleshooting matrix

| Symptom | Investigation | Correct action |
|---|---|---|
| Missing a GET response, HTTP 403/404 | OIDC role scope, resource exists, version, runner allowed network | `NOT_READY`; no public bypass |
| 429 or 5xx | REST02 bounded retries and `Retry-After`; service transient | If still incomplete, `NOT_READY` |
| PE connection state `Pending` | Approval owner and target private link resource | Record verified configuration mismatch; do not approve automatically |
| PE NIC not in approved subnet | Actual NIC/subnet relationship, IaC drift, PE IPAM | `FAIL_POLICY_OBSERVED` if verified |
| A-record differs from NIC IP | DNS zone group, private DNS A record, multiple endpoints, approved IPAM | Inspect without mutating DNS automatically |
| Zone group points to another zone | Zone ownership and expected service/group mapping | `FAIL_POLICY_OBSERVED`; review design |
| VNet link wrong or unprovisioned | Hub/spoke topology, forwarding, link ownership | `FAIL` on verified mismatch or `NOT_READY` on missing |
| Correct ARM values but client DNS fails | Forwarders, zone link, private resolver, split-horizon and NIC | Requires separately approved VNet/corporate resolver test |
| `/healthz` unreachable despite correct DNS | NSG/UDR, backend Host/SNI, App Service, authorization and gateway health | Requires private runner and TLS/HTTP evidence |

## 5. Future approved ARM-only read job (NOT AVAILABLE YET)

This section is **design guidance**, not a ready-to-run CI job. After authorization and an OIDC token-file bridge are independently approved, a management-plane read may run on an authorized GitHub-hosted runner. Private data-plane checks still require an approved VNet-connected runner or ephemeral VM.

```python
import json
from scripts.azure_rest_reader import AzureReadOnlyClient, workload_identity_token_provider
from scripts.rest04_private_dns_audit import audit_client

# Read approved_manifest from RESTRICTED storage, not public GitHub.
# It includes exact resource IDs / approved IPs and excludes credentials.
manifest = json.load(open("/restricted/approved-rest04.json", encoding="utf-8"))
client = AzureReadOnlyClient(
    ["<approved-subscription-uuid>"],
    workload_identity_token_provider(),
    read_enabled=True,
)
result = audit_client(client, manifest)
print(result["status"])  # no raw response values
```

**OIDC caveat:** GitHub `permissions: id-token: write` alone does not create `AZURE_FEDERATED_TOKEN_FILE`. REST02's `WorkloadIdentityCredential` requires an approved token-file bridge. Do not treat an unauthenticated run as a successful test.

## 6. Future private DNS / HTTPS checks (separate gate)

On an approved private network runner only, using independently approved canonical service FQDNs and the PE NIC IP baseline:

```bash
set -Eeuo pipefail
: "${APPROVED_FQDN:?}" "${EXPECTED_PRIVATE_IP:?}"
dig +time=3 +tries=1 "$APPROVED_FQDN" CNAME
dig +time=3 +tries=1 "$APPROVED_FQDN" A
getent ahostsv4 "$APPROVED_FQDN"
# Reviewer must compare final A answers to PE NIC inventory (not just RFC1918).
# Only after the target exists and test scope is authorized:
curl --fail-with-body --proto '=https' --tlsv1.2 \
  --connect-timeout 5 --max-time 20 -I "https://${APPROVED_FQDN}/healthz"
```

These commands are not included in offline CI. A `403`, `404`, DNS timeout, or TLS error alone never proves isolation or security. Preserve UTC, approved commit, scoped resource IDs in **restricted evidence**, runner origin, certificate details, request correlation, reviewer names and evidence digests. A runner with only public Internet connectivity cannot prove private DNS forwarding.

## 7. Upstream docs and verified Microsoft REST references

- [Private Endpoint GET](https://learn.microsoft.com/en-us/rest/api/virtualnetwork/private-endpoints/get?view=rest-virtualnetwork-2025-05-01)
- [Private DNS Zone Group GET](https://learn.microsoft.com/en-us/rest/api/virtualnetwork/private-dns-zone-groups/get?view=rest-virtualnetwork-2025-05-01)
- [Network Interface GET](https://learn.microsoft.com/en-us/rest/api/virtualnetwork/network-interfaces/get?view=rest-virtualnetwork-2025-05-01)
- [Private DNS VNet Link GET](https://learn.microsoft.com/en-us/rest/api/dns/privatedns/virtual-network-links/get?view=rest-dns-privatedns-2018-09-01)
- [Private Endpoint DNS integration](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns-integration)

Next: REST05 service-specific AI/data checks, additional cross-subscription/hub DNS support only after review, then formal test-ID mapping and evidence-gated automation. At the earliest, the **next 1–2 turns are user-operation-free**, while real ARM reads need OIDC scope/approval and private DNS E2E requires a private runner. The existence or absence of a self-hosted runner must never block offline source development.
