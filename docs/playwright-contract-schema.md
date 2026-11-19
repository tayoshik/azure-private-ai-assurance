# Playwright contract validation handoff (offline, no app deployment)

**Date:** 2026-11-19. **Scope:** draft PR #9 on top of draft PR #8; private application source is not verified.

## Discovery result

The connected GitHub installation exposed 30 repositories to the current connection. The target `tayoshik/azure-private-ai-assurance` tree contains Azure Terraform resource definitions and source-catalogue tests, but no verifiable application UI source, approved app release, authentication implementation, DOM selectors, or a private browser test runner. Other accessible repositories are not to be relabeled as this application's implementation without authoritative identity/provenance. The absence of an artifact in this GitHub installation does **not** prove it does not exist elsewhere.

## Delivered

- `scripts/validate_playwright_contract.py` is an offline JSON-shape verifier for the app source digest, HTTPS hostname, TLS hostname, internal and external runner separation, EntraOIDC protected identity reference, UI selectors, synthetic test data, evidence custody, and **nine exact AZ-T64 assertion kinds**.
- `tests/test_playwright_contract.py` includes good-format synthetic document (still *unapproved*), malicious secret keys, invalid URLs/commits, wrong TLS/SNI, same runner, invalid selectors, incorrect case kind, missing input and malformed JSON.
- `.github/workflows/playwright-contract.yml` runs the synthetic validator tests plus exact 1,716-case and 13-missing dependency guards without Azure, browser or credentials.
- `docs/playwright-contract.template.json` is an **intentionally invalid** placeholder-only intake template, not a live artifact, and never sufficient evidence.

**Return and trust boundary:** Even a syntactically complete document returns `CONTRACT_STRUCTURE_VALID_EXTERNAL_VERIFICATION_REQUIRED`, **exit code 2**. It can never emit READY, Azure PASS, or release GO. The tool does not load, validate, execute or attest the actual application source or Runner. Raw identities, tokens, passwords, cookies, source code, sanitized CI output or actual tenant/subscription IDs must not be stored in this public repo.

## Nine browser journeys and implementation criteria

| Case ID | Required assertion kind | Source-aware expected observation |
| --- | --- | --- |
| AZ-T64-01 | internal_https_response | HTTPS response from intended internal Gateway via approved route |
| AZ-T64-03 | tls_chain_and_hostname | Actual certificate chain, hostname and expiry validation; no TLS bypass |
| AZ-T64-05 | authorized_sign_in | Real approved application sign-in with protected test identity |
| AZ-T64-07 | authenticated_health_status | Live `/healthz` status and authentication policy |
| AZ-T64-09 | verified_dom_render | Main page and required real DOM selectors |
| AZ-T64-11 | synthetic_search_result | Approved synthetic search request, known result and correct UI |
| AZ-T64-13 | safe_chat_and_redaction | Safe synthetic chat and no protected content in logs/traces |
| AZ-T64-15 | expired_or_revoked_session_rejected | Explicit session expiry/revocation tested with rejected re-use |
| AZ-T64-17 | protected_data_absent_on_error | Controlled error path redaction of credentials, prompts and stack traces |

Four additional AZ-T20 checks cover separate internal/external Playwright projects, JUnit and trace data handling. Real Playwright code must not be written as a meaningless stub to make the file-path inventory turn green.

## Contract intake procedure (local protected storage only)

1. Copy `docs/playwright-contract.template.json` **outside the public GitHub repo** to an approved restricted workspace. This is not a credentials storage mechanism.
2. Obtain immutable real application repository and commit, artifact SHA-256, approved private TLS hostname, actual path/router semantics, private runner group and separate external vantage point.
3. Obtain reviewed Entra sign-in/session contract and *reference* to a protected test identity (not a password/token), six actual UI selectors, synthetic datasets and independent evidence retention roles. Collect only the minimum needed; keep restricted routing data out of public issues and artifacts.
4. Fill `scenarios` with the exact source-criteria mapping (no generic `page loads` assertions). A structural parse does **not** verify that the mapping implements those criteria.
5. Run offline preflight. It will return **exit 2 even if structurally complete** until a separate authorized reviewer confirms the source/runner/evidence. Never override this result with `|| true` in a release pipeline.
6. Only after review should a separate, protected, independently authorized workflow implement `tests/playwright.config.ts` and `tests/phase6/phase6.spec.ts` against the actual application. No browser tests are added by this PR.

### Read-only operator commands

~~~bash
python3 -m unittest discover -s tests -p 'test_playwright_contract.py' -v
# Template must be rejected, expected exit 2:
python3 scripts/validate_playwright_contract.py --contract docs/playwright-contract.template.json
# An owner-provided candidate must also exit 2, even if structurally valid:
python3 scripts/validate_playwright_contract.py --contract /restricted/qa/playwright-contract.json
python3 scripts/audit_playwright_readiness.py --strict     # expected exit 2
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/release_gate.py                           # expected exit 2
~~~

No `az login`, no Terraform `plan` or `apply`, no private URL probe, no Playwright browser or synthetic authentication is executed here.

## Remaining backlog

The code-path inventory **still must report 13 missing browser file references**, with 986 tracked, 717 no direct script and zero literal missing JSON inputs. Genuine Playwright implementation remains blocked on owner-supplied application artifacts, private runner/identity, selector and retention contracts. Independent reviewer approval and PR stack #2 through #9 remain separate work. All 1,716 live acceptance claims are NOT_READY; release decision remains NO_GO.
