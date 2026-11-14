# REST01–REST02 Operator Runbook: Azure REST Assurance

**Status:** source implementation and offline fixtures only; Azure live acceptance **0**; 1,716 test IDs **NOT_READY**; release **NO-GO**.
**Scope:** REST01 routes the existing six English catalogues without inventing REST endpoints. REST02 provides a **read-only** Azure Resource Manager and Resource Graph Python client, gated on explicit approved OIDC runner context. This package does not deploy resources or assert network isolation.

## A. Source inventory and preservation

Read the existing catalogue files (do not create a parallel canonical catalogue):

| Source | Step interval | Cases |
|---|---:|---:|
| `specs/english_tests_001_440.json` | 01–20 | 440 |
| `specs/phase3_264_en.json` | 21–32 | 264 |
| `specs/phase4_286_en.json` | 33–45 | 286 |
| `specs/phase5_286_en.json` | 46–58 | 286 |
| `specs/phase6_220_en.json` | 59–68 | 220 |
| `specs/phase7_220_en.json` | 69–78 | 220 |

REST01 validates every `AZ-TNN-MM`, the 22 cases per construction step and all six catalogue counts. It records source file SHA-256 and the **original command**. A `REST_CANDIDATE` is not a verified REST mapping or completed live test. Specific verified request paths and API versions will be added by REST03–REST07; do not invent them in this phase. Route classification uses command/execution metadata; an assessor must independently review candidate semantics and permissions.

## B. WSL offline workflow: safe, reproducible, no Azure login

```bash
set -Eeuo pipefail
cd "$HOME/azure-private-ai-assurance"
git pull --ff-only
mkdir -p "$HOME/azure-private-ai-assurance-qa/rest"
python3 scripts/rest01_catalogue.py --summary \
  > "$HOME/azure-private-ai-assurance-qa/rest/routing-summary.json"
python3 scripts/rest01_catalogue.py --test-id AZ-T33-01
python3 scripts/rest01_catalogue.py --test-id AZ-T64-01
python3 scripts/rest01_catalogue.py \
  --output "$HOME/azure-private-ai-assurance-qa/rest/1716-routing.json"
python3 -m unittest discover -s tests -p 'test_*rest*.py' -v
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v
sha256sum "$HOME/azure-private-ai-assurance-qa/rest/"*.json
```

**Pass for offline scope:** complete 1,716 unique IDs, every step has 22 cases, `azure_live_passes: 0`, no case classified as live implemented, tests all green. **Fail:** duplicate/missing ID, invalid step, missing catalogue, unexpected write-method acceptance, token disclosure, out-of-scope subscription. On failure, preserve the error and source commit; do not skip cases or change canonical IDs to make totals match.

The routing JSON contains the original commands and may mention example/private resource names. Keep operational evidence in an approved restricted location; do not commit live command results or private identifiers.

## C. REST02 read-only design and security contract

- **Auth:** `azure.identity.WorkloadIdentityCredential` on approved CI using `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_FEDERATED_TOKEN_FILE`; no interactive `az login`, client secret or CLI fallback. `azure-identity` must be installed from the approved dependency mirror.
- **Endpoint:** fixed `https://management.azure.com` only. GET is limited to explicit subscription-scoped resource IDs and pinned API versions. POST is permitted **only** for the fixed Resource Graph query endpoint. PUT/PATCH/DELETE are rejected; redirects are not followed with Bearer tokens.
- **Scope:** UUID subscription allowlist; curated resource types. Query is generated from a fixed template, and all pages must be collected without repeated `$skipToken`. Results include a digest; do not treat the digest or a successful HTTP response as independent acceptance.
- **Throttling:** retry only 429 and transient 5xx, with bounded attempts and `Retry-After` handling. 401/403/404 are NOT_READY; incomplete pages, unsupported API version, malformed JSON or out-of-scope results are NOT_READY or FAIL as appropriate.
- **State:** successful read returns `OBSERVED_NOT_ACCEPTED`. Only approved baselines, actual private vantage-point checks, corroborated evidence and independent review can determine an Azure `PASS`.

### Example for a separately authorized CI runner only (do not execute from fixed WSL)

```python
import os
from scripts.azure_rest_reader import AzureReadOnlyClient, workload_identity_token_provider

client = AzureReadOnlyClient(
    [os.environ["AZURE_SUBSCRIPTION_ID"]],
    workload_identity_token_provider(),
    read_enabled=True,  # Only in separately approved READ-ONLY CI job
)
result = client.resource_graph_inventory([
    "microsoft.web/sites",
    "microsoft.cognitiveservices/accounts",
    "microsoft.search/searchservices",
    "microsoft.documentdb/databaseaccounts",
])
# Never print access tokens or unrestricted resource properties to public CI logs.
print(result["state"], len(result["rows"]), result["evidence_sha256"])
```

This example is **not** a ready-to-run public GitHub workflow. Real CI first requires G07 scope approval, a federated read-only identity, the correct private runner, evidence retention, and the installed `azure-identity` package. No live access is attempted by the committed offline CI workflow.

## D. Detailed test cases / expected classification

| Test | Procedure | Expected | Failure action |
|---|---|---|---|
| R01-001 | Run `rest01_catalogue.py --summary` | Exactly 1,716 IDs, 78×22 | Stop on source mismatch |
| R01-002 | Run `--test-id AZ-T33-01` | `REST_CANDIDATE`, not PASS | Investigate changed source and command |
| R01-003 | Run `--test-id AZ-T64-01` | `PLAYWRIGHT_TOOL` | Do not mis-map browser behavior to ARM GET |
| R01-004 | Duplicate a case ID in a temporary copy | Nonzero exit | Preserve source copy; reject publication |
| R02-001 | Simulate valid scoped ARM GET | `OBSERVED_NOT_ACCEPTED` | Check ID/version/JSON shape |
| R02-002 | Test out-of-scope subscription | Rejected before HTTP | Escalate scope mismatch |
| R02-003 | Simulate ARM HTTP 403 | `NotReadyError` | Check CI RBAC, not a PASS |
| R02-004 | Simulate ARM HTTP 404 | `NotReadyError` | Verify actual asset; never claim secure absence |
| R02-005 | Simulate 429 then 200 | One bounded retry after `Retry-After` | Check request pacing |
| R02-006 | Simulate repeated 429 | `NotReadyError` after retry cap | Rate-limit and escalate |
| R02-007 | Simulate Graph multi-page result | All pages, SHA-256, correct scope | Inspect continuation tokens |
| R02-008 | Simulate Graph partial result | `NotReadyError` | Do not claim inventory completeness |
| R02-009 | Request PUT/DELETE / arbitrary POST | `ValueError` before HTTP | Reject write path |
| R02-010 | Omit OIDC environment variables | `NotReadyError` | Configure approved runner, never use client secret |
| R02-011 | Simulate redirect to unrelated domain | No redirected Bearer request | Investigate endpoint/security |
| R02-012 | Simulate oversized response | `NotReadyError` | Narrow query/approved pagination |

## E. Future DAG and user hand-off

- REST03: signed inventory and resource graph / ARM endpoint registry, tested per approved API version.
- REST04: Network/PE/DNS observation and exact NIC-IP comparison from an authorized internal runner.
- REST05: Azure OpenAI/Search/Cosmos data-plane checks with identities, privacy and costs approved.
- REST06–07: Key Vault, IAM, Monitor Logs and correlation evidence.
- REST08: Playwright private E2E; REST09–10: evidence manifest and signed independent acceptance.
- REST11: formal release decision. Not an automatic approval.

**No user operation in REST01/REST02.** Real API reads need approved subscription UUID, federated CI identity and network access. Credentials, tokens, resource IDs and unredacted evidence must not be committed to this public repository.

## References

- Microsoft Resource Graph REST query and `$skipToken`: https://learn.microsoft.com/en-us/azure/governance/resource-graph/first-query-rest-api
- Azure Identity `WorkloadIdentityCredential`: https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.workloadidentitycredential
- ARM throttling, 429 and Retry-After: https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/request-limits-and-throttling
