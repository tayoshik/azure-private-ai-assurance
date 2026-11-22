# Azure AI data-plane REST — synthetic contract checks only

**2026-11-22 / priority #3, slice 2 / Azure environment unavailable**

This work introduces `scripts/rest_data_plane_contracts.py` and `tests/test_rest_data_plane_contracts.py` to test bounded, **synthetic** REST request and response **contracts** for Azure OpenAI, Azure AI Search, and Azure Cosmos DB NoSQL. It complements, but does **not replace**, REST05 ARM configuration inspection. It does not provide a deployed app or any HTTP client, token handling, or cloud authentication. No actual Azure requests, private connectivity, model inference, database reads, Terraform plan/apply, or acceptance decisions are performed.

## API contract sources and intentional limits

| Profile | Illustrative fixed synthetic request | Expected response fixture | Microsoft documentation |
| --- | --- | --- | --- |
| `azure_openai` | `POST /openai/v1/chat/completions`; v1; fake Entra bearer identity marker; one fixed synthetic nonstreaming prompt | `choices[0].message.role/content`, `finish_reason`, optional token usage accounting | [Azure OpenAI / Foundry Chat REST](https://learn.microsoft.com/en-us/rest/api/microsoft-foundry/azureopenai/chat) |
| `ai_search` | `POST /indexes('synthetic-index')/docs/search.post.search?api-version=2025-09-01`, fixed synthetic query | `value` and `@odata.count`, optional continuation metadata is **not followed** | [Search Documents — POST, API 2025-09-01](https://learn.microsoft.com/en-us/rest/api/searchservice/documents/search-post?view=rest-searchservice-2025-09-01) |
| `cosmos_nosql` | `POST /dbs/{db}/colls/{coll}/docs`, fixed parameterized `SELECT TOP 1` and Cosmos query headers; illustrative `2018-12-31` request-version pin | `Documents` and `_count`; no live query or partition/continuation handling | [Cosmos DB Query Documents REST](https://learn.microsoft.com/en-us/rest/api/cosmos-db/query-documents) |

The code's separate `api_version` field is a **test-envelope field**, not a wire-level query string. For Search and OpenAI, a future real transport must compose and validate an actual URI and appropriate Entra audience; this code intentionally cannot do so. The fixed `id` field on Search result documents is an **example index schema**, not a statement that every actual index has that key. Cosmos request-version `2018-12-31` here is an offline fixture assumption; a real deployment needs its own version compatibility confirmation.

## Hard safety boundaries

- All input envelopes require `execution_class=OFFLINE_MOCK_ONLY`, `auth_mode=entra_bearer_placeholder`. Raw Authorization or API keys are explicitly rejected; no `azure-identity` or transport is imported.
- POST is used **only as a simulated query** for the three exact, reviewable routes. The library has **no HTTP method executor**, no authentication, no network sockets and no actual remote side effects.
- The synthetic OpenAI sample explicitly refuses streaming and real prompts. The Search sample is a bounded, fixed query and Cosmos uses one literal parameterized query. Do not treat this as coverage for all API schema variants, model versions, actual identity policy or service availability.
- Mock responses with HTTP 200 are labelled `OFFLINE_RESPONSE_CONTRACT_MATCH_ONLY`, **never Azure PASS**.
- Synthetic 401/403 responses produce `OFFLINE_DENIAL_NOT_ISOLATION_EVIDENCE`; they do not prove network isolation or permissions.
- 429/503 plus numeric retry metadata yield `OFFLINE_RETRY_HINT_NOT_EXECUTED`; the tool does not retry.
- Search continuation metadata yields `OFFLINE_CONTINUATION_NOT_FOLLOWED`; never request a `nextLink` supplied in a fixture.
- The only output fields are fixed contract metadata, classification, `network_requests=0`, pending scope approval, `verified_azure_live_passes=0`, `release_decision=NO_GO`. No request body, response body, tokens, URLs or protected user data are printed.
- The fixture envelope is bounded to 65,536 JSON UTF-8 bytes. Invalid/missing/extra fields, malformed result JSON types, incorrect header/version, oversized and nonfinite data fail closed via `ContractError`.

## Offline commands

```bash
python3 -m unittest discover -s tests -p 'test_rest_data_plane_contracts.py' -v
python3 -m unittest discover -s tests -v
python3 scripts/audit_rest_r41_rescope.py --strict  # expected exit 2: NOT APPROVED
python3 scripts/release_gate.py --root .        # expected exit 2: NO_GO
```

Do not put a strict expected-failure gate under `set -e` without capturing/checking its expected exit status. The existing always-on GitHub `offline-main-gate` runs the entire Python test suite and `offline-catalogue` checks immutable canonical test sources.

## Source trace and required further work

- Existing `specs/r41-rest-api-rescope-proposal.json` remains **PROPOSED_NOT_APPROVED**. Historical 13 Playwright references and **all 1,716 original IDs remain unchanged**.
- This slice is an **offline mock contract test artifact** only and does not count as an implementation of a live Azure data-plane client.
- Further approved design work: explicit endpoint inventory, version and authentication contract, permitted operations, complete pagination and continuation handling, safe log redaction and a real private test runner.
- Azure acceptance count **0**. Release decision **NO_GO**.
