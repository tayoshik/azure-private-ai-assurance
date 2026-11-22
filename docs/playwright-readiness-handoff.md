# Playwright readiness: 13 unresolved references, not 13 passing tests

**Review date:** 2026-11-19. **Boundary:** offline repository inspection only, no browser, network access, Azure login or live acceptance. Base: Phase 7 draft PR #7. This handoff is source-aware and deliberately refuses to "fix" the dependency ledger with dummy .ts files.

## Exact unresolved literal references

| Catalogue | Tests affected | Missing referenced path | Cases |
| --- | --- | --- | ---: |
| Phase 2, Step 20 | AZ-T20-07 external project; 09 internal project; 15 JUnit; 17 tracing | `tests/playwright.config.ts` | 4 |
| Phase 6, Step 64 | AZ-T64-01 HTTPS; 03 TLS; 05 authorized login; 07 healthz; 09 DOM; 11 search; 13 chat; 15 revoked session; 17 secure errors | `tests/phase6/phase6.spec.ts` | 9 |
| **Total** | | **2 distinct paths** | **13** |

The full repository source tree was checked. These two files were not tracked at the base commit. There is no verified application UI/source contract, routing, authentication flow, test identity, or private runner execution approval. This repository contains Terraform modules for App Service and the gateway; **infrastructure modules do not implement the application UI**.

The literal-dependency inventory is unchanged at **13 missing script/test references, 986 tracked, 717 with no direct reference, zero missing inputs, 1,716 canonical cases**. 717 no-direct-reference cases may use Azure CLI, external tools or manual procedures; they are not assumed failed, passed or implemented. Other runtime files, such as `tests/package.json`, `tests/package-lock.json` and `docs/test-data-handling.md`, are absent but are not counted by the narrow literal script/input audit; these are additional prerequisites, not invented test cases.

## What was implemented now

- `scripts/audit_playwright_readiness.py`: read-only enumeration of the exact 13 IDs, actual path existence, separately unverified owner prerequisites, explicit `NOT_READY` per case and overall `NO_GO`.
- `tests/test_playwright_readiness.py`: tests IDs, command references, source absence, unavailable approvals, corrupt catalogue and a malicious/dummy file that must not lead to readiness.
- `.github/workflows/playwright-readiness.yml`: Ubuntu offline job (no Playwright install or browser, no Azure secrets). Requires 13 missing to be reported; checks 1,716 ledger and expected release denial.
- The script's default exit 0 means **the inventory process itself completed**, not readiness. With `--strict` it returns 2; the overall release gate separately exits 2.

No unresolved file was added to make the missing-reference count look smaller. No screenshot, token, application content or user data should be committed to GitHub.

## External owner inputs required before true Playwright implementation

1. **Versioned application source or an approved immutable artifact**: identify actual web entry point, health endpoint, search/chat components, live UI DOM and expected responses. A Terraform App Service resource is insufficient.
2. **Approved nonproduction private URL, exact TLS/SNI and certificate criteria**: do not use localhost or public substitutes.
3. **Private internal runner and distinct approved external vantage point**: runner group, private DNS routing, reachability and authorization. A public GitHub-hosted runner must not run the live private-side test. An external denial alone never proves isolation.
4. **Authentication/session contract and test identity**: approved Entra auth settings, redirect/audience, secrets in protected runner vault, session revocation/expiry mechanism; no username/password/token in repository.
5. **Approved selectors, workflows and synthetic test data**: actual screen route, verified DOM/test IDs, search fixtures, chat scenario, data retention, screenshots, JUnit and traces.
6. **Independent collection and reviewer contract**: authorized ticket, resource IDs, UTC, TLS/HTTP evidence, protected output retention, two independent reviews. A local observation must remain review-only.

The application repository or external artifact **may** be separate; it has not been supplied or verified in the accessible project materials. Avoid conflating this limitation with proof that no application exists anywhere.

## Security acceptance boundaries

- `AZ-T64-01`: a successful HTTP response is not proof it travelled the approved private route.
- `AZ-T64-03`: TLS bypass (for example, `ignoreHTTPSErrors: true`) is prohibited for hostname/chain validation.
- `AZ-T64-05` and `AZ-T64-15`: login and revoked-session reuse require real application integration, approved identities and bounded observational evidence.
- `AZ-T64-17`: failure paths must avoid logging credentials or protected prompts.
- `AZ-T20-17`: traces and screenshots must be restricted and sanitized; recording them into public CI artifacts without approval is not acceptable.
- **Never** convert a static source audit or HTTP 403/timeout/NXDOMAIN into an Azure security PASS.

## Reproduction (no cloud credentials)

~~~bash
python3 scripts/audit_playwright_readiness.py --out /tmp/playwright-readiness.json
python3 -m unittest discover -s tests -p 'test_playwright_readiness.py' -v
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py
# Expected exit 2, NOT_READY / NO_GO:
python3 scripts/audit_playwright_readiness.py --strict
python3 scripts/release_gate.py
~~~

## Next test-implementation acceptance criteria

Create `tests/playwright.config.ts` and `tests/phase6/phase6.spec.ts` **only once** application source, identity, test fixtures and approved execution topology are verified. Every original AZ-T64 test must assert its specific observable condition (not a generic page-load smoke test), and negative/error/expired-session cases must fail on unexpected success. Browser/runner actions belong to separately authorized nonproduction CI, never in this offline workflow. Full integration still needs human review and a release process; even perfect CI remains Azure-live acceptance 0/1716 today.
