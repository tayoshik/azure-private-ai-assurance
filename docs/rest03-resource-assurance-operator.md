# REST03 — Azure Resource Graph & ARM Configuration Assurance

**Date:** 2026-11-14 · **Scope:** source and synthetic/offline validation only · **Azure live accepted:** **0** · **1,716 test IDs:** **NOT_READY** · **Release:** **NO-GO**.

## 1. What this phase actually implements

This layer builds upon the exact REST01/REST02 GitHub source. It does **not** recreate the 1,716 test IDs or alter their acceptance state.

- REST01: route 1,716 existing test IDs to proposed execution methods; 312 currently flagged `REST_CANDIDATE`, not implemented or accepted.
- REST02: existing allowlisted **read-only** ARM GET and Resource Graph POST client, explicit subscription scope, federated Workload Identity provider (requires preprovisioned token file), bounded response sizes, retries, and incomplete-result handling.
- REST03: compare REST02 observations to a **short, fixed list of defensive invariants** for 7 top-level Azure resource types. Read-only. A normal observation with all selected controls healthy returns `OBSERVED_PENDING_INDEPENDENT_REVIEW`, never live `PASS`. Missing properties/evidence return `NOT_READY`. A verified mismatch is `FAIL_POLICY_OBSERVED`; selftests distinguish `FAIL_OFFLINE_POLICY_FIXTURE`.
- No original catalogue test ID is automatically considered implemented/closed by REST03. REST03 is the *shared assessment engine* for subsequent individually mapped control IDs.

### Seven resource profiles and exact tested properties

| Profile | ARM resource type | Selected checks (not exhaustive) |
|---|---|---|
| `web_app` | `Microsoft.Web/sites` | `properties.publicNetworkAccess=Disabled`, `properties.httpsOnly=true` |
| `azure_openai` | `Microsoft.CognitiveServices/accounts` | `kind=OpenAI`, public network disabled, `properties.disableLocalAuth=true` |
| `ai_search` | `Microsoft.Search/searchServices` | public network disabled, `properties.disableLocalAuth=true` |
| `cosmos_nosql` | `Microsoft.DocumentDB/databaseAccounts` | public network disabled, `properties.disableLocalAuth=true` |
| `key_vault` | `Microsoft.KeyVault/vaults` | public network disabled, RBAC enabled, purge protection enabled |
| `private_endpoint` | `Microsoft.Network/privateEndpoints` | all returned connections `Approved`, expected private-link group IDs |
| `application_gateway` | `Microsoft.Network/applicationGateways` | every frontend has no public IP, private IP is present and statically allocated, WAF policy ID present |

**Limitation:** these properties alone do not prove zero external exposure, correct data-plane identity, actual PE DNS/IP, healthy routing, backend TLS, WAF enforcement, or complete resource inventory. Different API versions can use different schemas. The approved per-resource `api_version` must be confirmed before running. Treat missing or different schema as `NOT_READY`, not as an opportunity to weaken checks.

## 2. Runner decision (2026-11-14)

**User confirmed there is currently no self-hosted CI runner.** Design and CI must account for that fact:

- **Now:** GitHub-hosted Ubuntu runs mock tests, source QA, and Terraform offline regression **without Azure credentials**. This is safe and useful.
- **Later, with explicit security approval:** a GitHub-hosted runner *may* run read-only ARM management and Resource Graph API checks over its normal outbound connection if the subscription, federated OIDC principal, scopes and organization egress policy are approved. It cannot be assumed to access private data-plane endpoints.
- **Not available yet:** internal Private Endpoint DNS/HTTPS, Key Vault data-plane, private Azure OpenAI/Search/Cosmos data-plane, private App Service/SCM, and real Playwright tests. These require a managed execution environment with approved private routing, such as an organization-managed self-hosted runner, a scoped ephemeral VM/job inside the VNet, or another approved equivalent. The choice needs security ownership, network routing and funding approval.
- No `az login` from the fixed WSL terminal. Do not put OIDC tokens, secrets, raw response bodies, private IPs, full ARM resource IDs, or live evidence in a public GitHub artifact.

**Important OIDC integration blocker:** `WorkloadIdentityCredential` in REST02 expects an `AZURE_FEDERATED_TOKEN_FILE` populated by an approved token-exchange step. Simply setting `permissions: id-token: write` on GitHub Actions does **not** provide that file by itself. The follow-on REST04/runner design must implement and review this bridge or use another independently reviewed OIDC integration. Do not pretend the current offline workflow authenticates to Azure.

## 3. WSL2 offline verification — one paste, no Azure credentials

```bash
cat <<'CATEOF' > /tmp/run_rest03_offline.sh
#!/usr/bin/env bash
set -Eeuo pipefail
REPO="$HOME/azure-private-ai-assurance"
OUT="$HOME/azure-private-ai-assurance-qa/rest03"
mkdir -p "$OUT"
cd "$REPO"

git pull --ff-only
git rev-parse HEAD | tee "$OUT/commit.txt"

# Never connects to Azure.
python3 scripts/rest03_resource_audit.py --selftest \
  | tee "$OUT/rest03-selftest.json"
python3 scripts/rest01_catalogue.py --summary \
  | tee "$OUT/rest01-1716-summary.json"
python3 -m unittest discover -s tests -p 'test_*rest*.py' -v \
  2>&1 | tee "$OUT/rest03-rest-unittests.log"
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v \
  2>&1 | tee "$OUT/rest03-terraform-regression.log"
sha256sum "$OUT"/* | tee "$OUT/checksums.sha256"
echo 'SUCCESS: offline REST03 regression only; no Azure live acceptance'
CATEOF
bash /tmp/run_rest03_offline.sh
```

Expected `--selftest` JSON:

```json
{
  "status": "PASS_OFFLINE_FIXTURES_ONLY",
  "good": "PASS_OFFLINE_FIXTURE_ONLY",
  "bad": "FAIL_OFFLINE_POLICY_FIXTURE",
  "missing": "NOT_READY",
  "azure_live_passes": 0,
  "release_decision": "NO_GO"
}
```

The offline Python tests include 7 profile baselines and negative cases for public access, key auth, Key Vault purge/RBAC, unauthorized Private Endpoint group, unapproved PE state, public Gateway frontend, missing property, duplicate inventory IDs, missing/wrong SHA-256 and invalid resource IDs. Live test counts remain zero even when all tests succeed.

## 4. Local synthesized observation fixtures (optional, no Azure calls)

The following file structure supports fully offline review of a known synthetic fixture:

```json
{
  "targets": [
    {
      "resource_id": "/subscriptions/01234567-89ab-4def-8123-0123456789ab/resourceGroups/rg-synthetic/providers/Microsoft.Web/sites/web-synthetic",
      "profile": "web_app",
      "api_version": "2024-04-01"
    }
  ],
  "observations": [
    {
      "state": "OBSERVED_NOT_ACCEPTED",
      "resource_id": "/subscriptions/01234567-89ab-4def-8123-0123456789ab/resourceGroups/rg-synthetic/providers/Microsoft.Web/sites/web-synthetic",
      "observation": {
        "id": "/subscriptions/01234567-89ab-4def-8123-0123456789ab/resourceGroups/rg-synthetic/providers/Microsoft.Web/sites/web-synthetic",
        "type": "Microsoft.Web/sites",
        "properties": {"publicNetworkAccess": "Disabled", "httpsOnly": true}
      },
      "evidence_sha256": "<SHA256_OF_CANONICAL_OBSERVATION_JSON>"
    }
  ]
}
```

The digest must be computed as SHA-256 over `json.dumps(observation, sort_keys=True, ensure_ascii=False, separators=(',', ':'))`. A missing/mismatched digest returns `NOT_READY`. This hash detects inconsistency; it is **not a signature** or independent proof of origin. Do not use synthetic fixtures to assert the real Azure state.

Run a local fixture after generating the canonical digest:

```bash
python3 scripts/rest03_resource_audit.py --fixture /path/to/approved-synthetic-fixture.json
```

Expected: `PASS_OFFLINE_FIXTURES_ONLY` for a correct synthetic fixture; `FAIL_OFFLINE_POLICY_FIXTURE` with a nonzero exit status for a known violation; `NOT_READY` with nonzero exit for incomplete evidence.

## 5. Future, separately approved management-plane collection (do **not** run now)

Only after environment scope, exact resource IDs, API versions, OIDC, read-only RBAC and execution approval exist:

```python
from scripts.azure_rest_reader import AzureReadOnlyClient, workload_identity_token_provider
from scripts.rest03_resource_audit import audit_client

# approved_manifest is stored outside public GitHub, independently reviewed.
# Fields: subscription_id, targets (resource_id, profile, api_version, PE group IDs).
client = AzureReadOnlyClient(
    [approved_manifest["subscription_id"]],
    workload_identity_token_provider(),
    read_enabled=True,
)
result = audit_client(client, approved_manifest["targets"])
# Store only redacted results in approved restricted evidence storage.
# "OBSERVED_PENDING_INDEPENDENT_REVIEW" is not a released PASS.
```

**Note:** this illustrative code is not a standalone job. The real CI job needs secure approval enforcement, deployment of the required OIDC token-file bridge, and independent evidence retention. Those are deliberately not present in the public no-credentials workflow.

## 6. Detailed failure classification and next actions

| Condition | Classification | Safe next action |
|---|---|---|
| Public network Enabled or local auth enabled | `FAIL_POLICY_OBSERVED` or synthetic fixture failure | Record exact approved target/commit/evidence privately; assign remediation owner; do not auto-change Azure |
| Public IP frontend on App Gateway | `FAIL_POLICY_OBSERVED` | Independently compare ARM settings and effective network reachability |
| PE state Pending/Rejected or group mismatch | `FAIL_POLICY_OBSERVED` | Check PE approval and correct subresource; verify PE NIC/DNS separately |
| Missing property, insufficient RBAC, 401/403/404 | `NOT_READY` | Check approved resource ID, API version, assigned identity and permissions |
| Resource Graph incomplete/duplicate/truncated | `NOT_READY` | Review scope/page tokens, Graph limits, eventual consistency and filtering |
| ARM 429 or transient 5xx | REST02 bounded retry then `NOT_READY` | Inspect throttling, concurrency and retry budget; never remove scope controls |
| Evidence digest wrong/absent | `NOT_READY` | Restore complete, unmodified observation, UTC, runner identity, audit trail |
| Good synthetic fixture | `PASS_OFFLINE_FIXTURE_ONLY` | Proceed to next source-development node; do not mark Azure live tests PASS |
| Healthy-looking live ARM observations | `OBSERVED_PENDING_INDEPENDENT_REVIEW` | Correlate private network evidence, RBAC, logs, signed baseline and independent review |

### Evidence chain required for eventual live acceptance

Test ID → source commit SHA → approved manifest & reviewer signatures → federated runner identity → exact resource IDs and pinned API versions → UTC → response/evidence SHA-256 → independent analysis → `PASS/FAIL/NOT_READY`. Evidence is kept in restricted storage; no live secrets in this public repository.

## 7. Next DAG nodes and interaction forecast

- **Next turn (REST04 design and implementation):** Private Endpoint control-plane inspection, DNS correlation, and a **synthetic-only** runner readiness matrix. No user action.
- **Following turn (REST05/CI OIDC bridge):** service-specific API checks, Azure-hosted OIDC read-only CI design, provenance; still possible without user action for code/fixtures.
- **First live management-plane turn (earliest 2–3 turns after this one):** user/organization must supply or approve subscription scope, read-only federated identity, GitHub Actions OIDC trust, API egress policy and exact target resources. No self-hosted runner is necessary *for public ARM management endpoints* if policy permits.
- **First private data-plane/Playwright turn:** a privately routed test execution environment is required; **none currently exists**, so no date/turn is promised until an approved runner or ephemeral VNet job is available.
