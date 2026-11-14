# REST05 Operator Runbook — Azure OpenAI, AI Search and Cosmos DB (ARM read-only)

**Status:** implemented assessor and synthetic regression tests only. Azure live accepted tests: **0 / 1,716**. Decision **NO-GO**. No self-hosted private runner exists. REST05 therefore does **not** test private data-plane traffic, inference, search queries, Cosmos documents, runtime identity, TLS, quota availability or billing.

## 1. Scope and source inheritance

REST05 deliberately reuses REST01's immutable 1,716-case catalogue, REST02's fixed-host/read-only/OIDC ARM client, REST03's digest and no-PASS discipline, REST04's PE/DNS topology checks and the A01–A06 Terraform source. No earlier live claims are invented or modified. The three service profiles correspond to A01/A02 (Azure OpenAI account and model deployment), A03 (AI Search) and A04 (Cosmos for NoSQL account, SQL database and container). REST05 is not REST06 RBAC or REST04 private network verification.

Authoritative ARM GET contracts verified at design time (2026-11):

| Resource | GET ARM path suffix | Pinned API version | Evidence used |
|---|---|---|---|
| Azure OpenAI account | `/providers/Microsoft.CognitiveServices/accounts/{name}` | `2024-10-01` | kind, location, PNA, local auth, custom subdomain |
| OpenAI deployment | `/providers/Microsoft.CognitiveServices/accounts/{name}/deployments/{deployment}` | `2024-10-01` | exact model name/version/format, upgrade policy, SKU/capacity |
| Azure AI Search | `/providers/Microsoft.Search/searchServices/{name}` | `2025-05-01` | PNA, local auth, bypass, approved SKU and minimum units |
| Cosmos DB account | `/providers/Microsoft.DocumentDB/databaseAccounts/{name}` | `2025-10-15` | PNA, local auth, bypass, continuous backup tier, consistency |
| Cosmos SQL database | `/providers/Microsoft.DocumentDB/databaseAccounts/{name}/sqlDatabases/{database}` | `2025-10-15` | database identity |
| Cosmos SQL container | `/providers/Microsoft.DocumentDB/databaseAccounts/{name}/sqlDatabases/{database}/containers/{container}` | `2025-10-15` | container identity and partition-key path |

All paths are prefixed with `https://management.azure.com/subscriptions/{approved-subscription-id}/resourceGroups/{approved-rg}`. The expected Cosmos backup tier is explicitly approved (`Continuous7Days` or `Continuous30Days`). No read operation invokes `listKeys`, `POST` inference/query, `PUT`, `PATCH` or `DELETE`. **REST02 validates the explicit subscription allowlist**; get_resource returns raw data to the in-process assessor and only digest/status are emitted. Review API version support and ARM fields during G03 before running against real resources, especially after service updates.

Official Microsoft Learn: [OpenAI deployments GET](https://learn.microsoft.com/en-us/rest/api/aiservices/accountmanagement/deployments/get?view=rest-aiservices-accountmanagement-2024-10-01), [Search service GET](https://learn.microsoft.com/en-us/rest/api/searchmanagement/services/get?view=rest-searchmanagement-2025-05-01), [Cosmos account GET](https://learn.microsoft.com/en-us/rest/api/cosmos-db-resource-provider/database-accounts/get?view=rest-cosmos-db-resource-provider-2025-10-15), [Cosmos container GET](https://learn.microsoft.com/en-us/rest/api/cosmos-db-resource-provider/sql-resources/get-sql-container?view=rest-cosmos-db-resource-provider-2025-10-15).

## 2. WSL — one-paste reproducible offline procedure

No `az login`, tenant ID, subscription ID, application credentials, VNet, Azure provider or live resources are required.

```bash
cat <<'CATEOF' > /tmp/run_azure_rest05_offline.sh
#!/usr/bin/env bash
set -Eeuo pipefail
REPO="$HOME/azure-private-ai-assurance"
OUT="$HOME/azure-private-ai-assurance-qa/rest05"
test -d "$REPO/.git" || { echo 'ERROR: Clone the existing repo first'; exit 1; }
mkdir -p "$OUT"
cd "$REPO"
echo 'STEP 1/7 — Source update and revision'
git pull --ff-only
git rev-parse HEAD | tee "$OUT/commit.txt"
echo 'STEP 2/7 — REST05 selftest (safe / unsafe / missing)'
python3 scripts/rest05_ai_data_audit.py --selftest | tee "$OUT/selftest.json"
echo 'STEP 3/7 — Three-service fixture integration'
python3 scripts/rest05_ai_data_audit.py --fixture specs/rest05-synthetic-fixture.json | tee "$OUT/fixture.json"
echo 'STEP 4/7 — All REST01–REST05 regression tests'
python3 -m unittest discover -s tests -p 'test_*rest*.py' -v 2>&1 | tee "$OUT/rest-tests.log"
echo 'STEP 5/7 — Existing Terraform regression tests'
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v 2>&1 | tee "$OUT/terraform-tests.log"
echo 'STEP 6/7 — Confirm no Azure acceptance was claimed'
python3 - "$OUT" <<'PY'
import json,sys
from pathlib import Path
base=Path(sys.argv[1])
for name in ['selftest.json','fixture.json']:
    r=json.loads((base/name).read_text())
    assert r['status'].startswith('PASS_OFFLINE_')
    assert r['azure_live_passes']==0 and r['release_decision']=='NO_GO'
    assert r.get('private_data_plane_proven') is False or 'private_data_plane_proven' not in r
print('PASS: offline tests have not been promoted to Azure live PASS')
PY
echo 'STEP 7/7 — Integrity evidence (local only)'
(cd "$OUT"; sha256sum commit.txt selftest.json fixture.json rest-tests.log terraform-tests.log) | tee "$OUT/SHA256SUMS.txt"
echo "SUCCESS_OFFLINE_ONLY: $OUT"
CATEOF
bash /tmp/run_azure_rest05_offline.sh
```

**Expected:** `--selftest` prints good=`PASS_OFFLINE_FIXTURES_ONLY`, unsafe=`FAIL_OFFLINE_POLICY_FIXTURE`, missing=`NOT_READY`, Azure passes=0, release=`NO_GO`; the three-service fixture returns `PASS_OFFLINE_FIXTURES_ONLY`. A failure must abort before the success message. Real target identifiers and raw Azure response bodies **must not** be committed to the public repository.

## 3. Detailed synthetic test plan

| Test ID | Input mutation | Expected result | Troubleshooting |
|---|---|---|---|
| R05-001 | All 3 synthetic profiles unchanged | `PASS_OFFLINE_FIXTURES_ONLY` only | Examine baseline schema and fixture hashes |
| R05-002 | OpenAI PNA `Enabled` or `disableLocalAuth=false` | `FAIL_OFFLINE_POLICY_FIXTURE` | Check public/auth policy and ARM field casing |
| R05-003 | OpenAI model version drift or auto-upgrade on | `FAIL_OFFLINE_POLICY_FIXTURE` | Require pinned model version and upgrade policy |
| R05-004 | OpenAI deployment response omitted | `NOT_READY` | Verify deployed model resource and read permissions |
| R05-005 | Search bypass `AzureServices`, public enabled or keys enabled | `FAIL_OFFLINE_POLICY_FIXTURE` | Check Search network and auth controls |
| R05-006 | Search SKU/capacity falls below approved baseline | `FAIL_OFFLINE_POLICY_FIXTURE` | Review allocation, SKU/cost approval |
| R05-007 | Search `partitionCount` missing | `NOT_READY` | Inspect REST projection/API version |
| R05-008 | Cosmos backup `Periodic`, wrong retention tier, local key auth or network bypass | `FAIL_OFFLINE_POLICY_FIXTURE` | Validate account properties and policy |
| R05-009 | Cosmos SQL DB/container names or partition path drift | `FAIL_OFFLINE_POLICY_FIXTURE` | Match approved data design; do not read user documents |
| R05-010 | Cosmos partition configuration missing | `NOT_READY` | Compare API response shape and account SKU |
| R05-011 | Forged body/hash or scope mismatches | `NOT_READY` | Investigate source identity, URI, collection integrity |
| R05-012 | Healthy observational ARM data in non-synthetic mode | `OBSERVED_PENDING_PRIVATE_DATA_PLANE_AND_REVIEW` | Schedule approved private-data-plane and 2-person review |

The test module `tests/test_rest05_ai_data_audit.py` includes additional negative variations, approval gates, model role/ID consistency, and synthetic errors. These R05 labels are **module-level test identifiers**, **not** substitutes for existing `AZ-TNN-MM` acceptance IDs. Mapping to canonical IDs remains a separate REST01/REST09 evidence task.

## 4. Future approved OIDC ARM-only runner (NOT configured or run)

Only after approval of subscription scope, source revisions, read-only Azure role, GitHub OIDC trust, audited dependency mirror and evidence location:

```python
# Approved private/CI job only. DO NOT place in the public offline GitHub Actions job.
import json, os
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'scripts'))
from azure_rest_reader import AzureReadOnlyClient, workload_identity_token_provider
from rest05_ai_data_audit import audit_client

manifest=json.load(open('secure/rest05-approved-manifest.json'))
client=AzureReadOnlyClient(
    [os.environ['AZURE_SUBSCRIPTION_ID']],
    workload_identity_token_provider(),
    read_enabled=True,
)
result=audit_client(client,manifest)
# Status/digests only, no secret value, token, raw ARM properties, prompt or document.
print(result['status'],result['release_decision'],result['azure_live_passes'])
```

Never publish `secure/rest05-approved-manifest.json`, ARM response bodies, internal names/IPs, Cosmos documents, real model prompts, auth files or tokens. The example expects execution from the repository root in a separately approved runner with the Python dependencies installed; it is **not** an executable committed CI workflow and is explicitly unauthorized on the fixed WSL workstation.

## 5. Interpretation, controls and blocked paths

- `FAIL_POLICY_OBSERVED` = a reviewed baseline conflicts with an observed ARM configuration; preserve evidence, raise corrective ticket. **Do not auto-remediate.**
- `NOT_READY` = absent target, 401/403/404, unsupported API projection, incomplete digest, missing role, missing private runner or incomplete evidence. Fail closed; do not falsely mark PASS.
- `OBSERVED_PENDING_PRIVATE_DATA_PLANE_AND_REVIEW` = management configuration appears to match selected controls, but DNS, PE NIC, SNI/TLS, actual Managed Identity and AI data-plane access remain unproven. Independent reviewers assign canonical test dispositions later.
- Existing REST04 checks PE/NIC/DNS **ARM configuration only**. Without a VNet runner, cannot verify private DNS resolution, HTTPS, Azure OpenAI inference, Search query or Cosmos document access. These remain `NOT_READY`.
- Model name/version, region, SKU and Cosmos throughput/backup retention must have *real environment-specific approvals* before real test runs. The synthetic model `synthetic-model` does not purport to be offered in Japan East.
- Search result coverage, safety response evaluation, content filtering, exact model availability, cost, DR restore and Cosmos data-role access are outside the REST05 scope and must not become PASS solely from metadata.

## 6. Next work and human action timing

REST06 adds identity/Key Vault/RBAC read-only policy checks without real Azure access. REST07 adds Monitor Logs and completeness checks. An **approved Azure management REST read** requires organizational authorization, explicit subscription scope, federated read-only identity and a permitted CI runner even if using a GitHub-hosted runner. Private endpoint **data plane** requires a VNet-connected runner, which is not currently installed. No autonomous Azure creation or approval bypass is permitted.
