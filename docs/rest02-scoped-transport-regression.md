# REST02 — offline transport-boundary regression (priority #3)

**Date:** 2026-11-22. **Target:** `scripts/azure_rest_reader.py`, the read-only Azure Resource Manager / Resource Graph client. **No Azure environment is needed or used.**

## Scope and observed source gap

`AzureReadOnlyClient.get_resource()` checked subscription scope, but its internal `_send("GET", path)` transport method previously accepted **any string starting with** `/subscriptions/`. A future internal caller could therefore construct a GET path to a different subscription, add unapproved query arguments, or bypass a pinned API-version check. The `resource_graph_inventory()` response validator checked each row's `subscriptionId` and `type`, but did **not corroborate** them against the returned row's own resource `id`.

Those are *source-derived trust-boundary weaknesses*, not evidence that an actual Azure deployment was breached. The project has no approved live Azure environment or accepted Azure test results.

## Source changes

- Require a full ARM resource ID and **exact one** `api-version=YYYY-MM-DD[-preview]` query in every `_send("GET", ...)` call. Check that the parsed subscription UUID belongs to the configured allowlist **before obtaining any token or sending any transport request**.
- Reject path dot-segments (`/./`, `/../`) before URI construction for direct GET and `get_resource()`.
- For every Resource Graph row, require a valid scoped ARM resource `id`, and verify its embedded subscription and provider type against the row's `subscriptionId` and `type`. Missing/mismatched data results in `NOT_READY`.
- Keep read-only behavior: no ARM PUT/PATCH/DELETE, no broad POST; Resource Graph remains the only fixed read-query POST exception.
- Preserve `OBSERVED_NOT_ACCEPTED` for successful mock/ARM reads; never promote response status to independent security acceptance.

## Added targeted test cases

17 new Python `unittest` cases in `tests/test_rest02_scope_boundary.py` cover:
- Unauthorized cross-subscription GET and malformed or unpinned URI rejection **before token/transport**.
- URI path dot-segments, forbidden HTTP methods and GET bodies.
- Normal scoped GET, fake token, fake network and response classification.
- Resource Graph missing/mismatched ID, subscription, provider type and path traversal, plus valid synthetic observation.
- Invalid JSON; empty/unavailable OIDC tokens; unauthorized 401; bounded retry on 503; network exhaustion; read-disabled state.
- No real HTTP, SDK credential, GitHub OIDC, Azure CLI or Terraform calls occur.

The existing `tests/test_azure_rest_reader.py` stays unchanged and continues to exercise pagination, 403/404, 429, response-size cap, no redirect, API version and opt-in checks. Other REST03/REST05 tests remain in the full offline suite.

## Reproduction

```bash
python3 -m unittest discover -s tests -p 'test_rest02_scope_boundary.py' -v
python3 -m unittest discover -s tests -p 'test_azure_rest_reader.py' -v
python3 -m unittest discover -s tests -v
python3 scripts/release_gate.py  # expected NO_GO, exit code 2; not a CI failure
```

CI evidence: the always-on `offline-main-gate` runs the full tests on every PR; `offline-catalogue` verifies the immutable 1,716-case publication. Do not add a new globally required check that only runs on path-filtered PRs.

## Status and remaining work

| Scope | State |
| --- | --- |
| REST02 GET and Resource Graph offline boundary hardening | Proposed in a PR; close after CI + merge |
| 17 new synthetic, no-network unit tests | Proposed in a PR; close after CI + merge |
| R41 13-case proposal / scope-change authorization | Proposal recorded; approval **OPEN** |
| Azure OpenAI, AI Search, Cosmos data-plane mock request/response contracts | **NEXT**, separate controlled implementation |
| Actual Azure DNS/TLS/OIDC/private data-plane behavior | **NOT_READY**; nonproduction Azure and approvals absent |
| Canonical 1,716 tests | Unmodified |
| Accepted Azure live passes | **0** |
| Production release | **NO_GO** |

**Acceptance criteria for this slice:** 17 added tests and pre-existing tests pass on GitHub Actions; no frozen-catalogue changes; no new live authorization; head SHA is verified before merging.
