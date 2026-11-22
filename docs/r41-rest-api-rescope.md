# R41 — Azure REST API unit-test rescope (proposal, NOT approved)

**Snapshot:** 2026-11-22. **Intent:** prioritize Azure REST API **unit/contract tests**, not UI/browser E2E. This is an operator-review proposal only; it **does not change** the 1,716 frozen test catalogue records, their commands, historical classification, or release acceptance. R41 source: `R41_REST_API_13_CASE_REBASELINE_PROPOSAL.json` dated 2026-11-20, transcribed to `specs/r41-rest-api-rescope-proposal.json` without altering 13 per-ID proposal records.

## Why

The published Phase 2/6 canonical catalogue cites two unavailable Playwright references for **13 IDs**. The older browser journeys depend on application source, selectors, authentication and authorized private runner that are not available in this public repository. Creating empty `.ts` stubs would conceal the deficiency, not solve it. R41 proposes a new API-centric requirement baseline, pending explicit scope-change approval. The existing `scripts/audit_playwright_readiness.py` and `scripts/audit_catalogue_dependencies.py` must continue to report the original references until that approval and a versioned revised catalogue exist.

## Exact 13-case disposition

| Frozen ID(s) | Proposed API-focused scope | Current decision |
| --- | --- | --- |
| AZ-T20-07, AZ-T20-09 | Separate approved external/internal REST test origins, identities, DNS/routes and role contracts; mocks cannot prove connectivity | Runner topology **proposal** |
| AZ-T20-15 | JUnit XML plus sanitized JSON, with explicit unit/mock versus live classification | Evidence contract **proposal** |
| AZ-T20-17 | HTTP metadata-only trace, credential and payload redaction, protected custody | Evidence custody **proposal** |
| AZ-T64-01 | HTTP response + route/asset correlation when authorized; offline unit verifies only mock transport/response | REST integration **proposal** |
| AZ-T64-03 | Approved TLS peer identity, certificate chain, hostname and expiry (live runner eventually required) | TLS integration **proposal** |
| AZ-T64-05 | Entra audience/scope and expected HTTP 401/403 authorization behavior | REST authorization **proposal** |
| AZ-T64-07 | Replace app-only `/healthz` expectation with a **service-specific** applicable health/readiness endpoint, if such endpoint exists | Needs endpoint decision |
| AZ-T64-09 | DOM rendering cannot be demonstrated by any REST assertion; seek explicit N/A or approved new schema-contract ID | **UI-only; no automatic substitution** |
| AZ-T64-11 | Azure AI Search API request/response schema, safe synthetic result, 4xx/429 and pagination if appropriate | Data-plane **conditional** |
| AZ-T64-13 | Azure OpenAI API response, error policy, safe synthetic input and redaction | Data-plane **conditional** |
| AZ-T64-15 | Expiry/scope/authorization rejection; revocation semantics need an approved identity contract | Auth integration **proposal** |
| AZ-T64-17 | Safe HTTP errors and sanitized logs without tokens, protected prompts or stack traces | Negative/redaction **proposal** |

**Source of truth:** Exact original command, expected criterion, full wording and every individual disposition/qualification remain in `specs/r41-rest-api-rescope-proposal.json`. Do not reinterpret a mock test as live route/TLS, Azure AD token, data-plane authorization, private path or acceptance evidence.

## API surface partition and non-Azure implementation route

1. **Management plane (ARM / Resource Graph):** `scripts/azure_rest_reader.py`, `scripts/rest03_resource_audit.py`, `scripts/rest05_ai_data_audit.py`. Existing scripts are constrained read-only. Write independent mock/fixture unit tests for path allowlisting, subscription ID, RBAC failures (401/403), missing resources (404), response-shape errors, size limits, retry 429/5xx, bounded paging, missing continuation token, and redaction. Resource Graph fixed POST is a read-only graph-query exception; do not conflate it with a mutation API.
2. **Service data plane:** Azure OpenAI, Azure AI Search and Cosmos DB each need **independent endpoint, API-version, scope/audience, request/response and error contracts**. Pure mock tests can exercise these contracts, but there is no validated live data-plane client or target service revision in this repository. Do not claim implemented live OpenAI/Search/Cosmos calls or invent credentials.
3. **Integration / network:** DNS resolution to approved PE NICs, TLS chain, private/internal runner, distinct authorized external vantage, Entra identity, actual HTTP response, logs and evidence custody all stay `NOT_READY` until nonproduction assets and approval exist. A 403, timeout or NXDOMAIN alone does not prove isolation.
4. **UI-only:** The legacy DOM rendering requirement cannot be passed by a REST unit test. Keep it open for owner scope decision, N/A by approved change control, or a separately specified service schema contract.

## Current acceptance status (not altered)

- 78 steps / 22 IDs each = **1,716 frozen canonical IDs**.
- Exactly 13 proposed historical references across `tests/playwright.config.ts` (4) and `tests/phase6/phase6.spec.ts` (9).
- `approval_status: PROPOSED_NOT_APPROVED`; all 13 approval fields `PENDING_SCOPE_CHANGE_APPROVAL`.
- API unit-test passes **0** in this crosswalk document (it is a specification/audit, **not an executable API unit-test suite**).
- Azure accepted live passes **0**, release **NO_GO**.
- Repo main branch protection remains an independent open task (Issue #17); this document cannot close it.

## Reproducible local verification (no Azure environment)

```bash
python3 scripts/audit_rest_r41_rescope.py --out /tmp/r41-crosswalk-audit.json
python3 -m unittest discover -s tests -p 'test_rest_r41_rescope.py' -v
python3 scripts/audit_catalogue_dependencies.py > /tmp/canonical-deps.json
# A strict gate MUST refuse incomplete scope approval, exit 2:
set +e
python3 scripts/audit_rest_r41_rescope.py --strict > /tmp/r41-strict.json
rc=$?
set -e
test "$rc" -eq 2
```

This produces an **offline source-crosswalk validation only**, not approval. A `0` exit from the ordinary audit means the proposal is internally consistent against the frozen records, never a REST functional pass.

## Change-control / next work

- **R41-01 CLOSED when merged:** Preserve source-grounded 13-ID proposal and machine-audit exactly against frozen catalogue. Do not silently modify legacy test sources.
- **R41-02 OPEN:** Independent owner approves or rejects each required disposition and its applicability. In particular, approve the `AZ-T64-09` N/A/substitution and the `AZ-T64-07` endpoint choice; no synthetic approval.
- **R41-03 NEXT:** Implement independent Azure REST transport and data-plane mock contract tests with malformed data/negative cases (priority #3), without changing historical commands, live acceptance or release state.
- **R41-04 LATER:** After explicit approval, prepare a **versioned** new canonical catalogue and compatibility crosswalk, preserved SHA, signed independent evidence requirements, and revised quality gates. Existing frozen files remain immutable.
- **R41-05 DEFERRED:** Only when approved Azure nonproduction resources and independent private runner are available, execute read-only integration tests with actual resource scopes and evidence. Live PASS is never inferred from mock tests.

**Definition of done for this priority:** Crosswalk exactly 13 IDs, command and expected criterion match frozen source, approval is visibly pending, mutation tests refuse tampering, and GitHub Actions CI passes. Scope-change approval and genuine Azure testing remain separate gates.
