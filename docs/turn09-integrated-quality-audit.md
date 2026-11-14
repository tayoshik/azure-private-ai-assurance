# Turn 09 — Integrated English Quality Audit of 1,716 Test Cases

**Date:** 2026-11-14  
**Repository:** [`tayoshik/azure-private-ai-assurance`](https://github.com/tayoshik/azure-private-ai-assurance) (public)  
**Scope:** English documentation, offline test scripts, provenance, command syntax, and dependency closure.  
**Release decision:** **NO-GO**. **Azure live passes: 0.** **Production deployment: not verified.**

## 1. Objective and final intended outcome

The project documents a private-data-plane Azure AI application with private-only Application Gateway WAF_v2, App Service inbound Private Endpoint and outbound VNet integration, private Azure OpenAI / Azure AI Search / Cosmos DB, managed identities, private DNS, monitoring, protected Terraform state, and approved CI. The intended endpoint is an **independently reviewable deployment and release decision**, not a claim that the design is already implemented.

This **Turn 09** audit combines the previously generated English specifications for 78 construction steps and 1,716 canonical test identifiers. The review explicitly separates **858 configuration/evidence review procedures** from **858 synthetic deviation-detector tests**. Neither category currently has accepted Azure live results.

## 2. Measured cross-phase results

| Phase | Steps | Test IDs | Design/configuration review cases | Synthetic cases | Offline regression |
|---|---|---:|---:|---:|---|
| P1 | 01–10 | 220 | 110 | 110 | 110 policy controls self-tested; all good/bad/missing fixture branches passed in the source revision |
| P2 | 11–20 | 220 | 110 | 110 | 220/220 synthetic self-tests |
| P3 | 21–32 | 264 | 132 | 132 | 264/264 fixture self-tests |
| P4 | 33–45 | 286 | 143 | 143 | 286/286 fixture self-tests |
| P5 | 46–58 | 286 | 143 | 143 | 286/286 fixture self-tests |
| P6 | 59–68 | 220 | 110 | 110 | 220/220 fixture self-tests |
| P7 | 69–78 | 220 | 110 | 110 | 220/220 fixture self-tests |
| **Total** | **01–78** | **1,716** | **858** | **858** | **Offline checks only** |

All test IDs from `AZ-T01-01` through `AZ-T78-22` were found **once** and ordered correctly. All 1,716 source commands passed `bash -n` **syntax** checking, and all 1,716 entries have nonempty command, procedure, prerequisites, evidence and an acceptance-criterion field. The six published catalogue digests match the Turn 08 SHA-256 index. This does **not** establish cloud CLI version correctness, real authorization, control coverage or operational safety.

Existing Turn 08 signed-evidence unit tests: **27/27 passed**. Additional Turn 09 integrated QA unit tests: **13/13 passed**. These exercise local logic, rejection behavior and tamper detection; they are **not independent Azure acceptance**.

## 3. Findings and resolution status

| Finding | Priority | Evidence | Action | Status |
|---|---|---|---|---|
| T09-01: Missing offline dependency files in the English publication workspace | P1 | 20 unique internal paths are referenced by test commands; required versioned scripts and data were not all bundled previously | Include frozen Phase 1–7 guards, policy specifications, source-linked catalogue, and evidence tools in the reproducible package | **Corrected in Turn 09 package**; repository verification separately required |
| T09-02: Real application Playwright configuration and lockfile not supplied | P0 | References to `tests/package-lock.json`, `tests/playwright.config.ts`, and `tests/phase6/phase6.spec.ts` cannot be fulfilled by the supplied artifacts | Obtain app test source and dependency lockfile; pin dependencies and use approved internal CI; never replace real E2E with a passing stub | **OPEN / NOT_READY** |
| T09-03: No real Terraform/application/CI implementation source, approved asset IDs or cloud evidence | P0 | Source corpus is design artifacts and offline synthetic checks | Supply source commit, approved baseline, specific non-production inventory, CI runner identity and authorized observation logs | **OPEN / NOT_READY** |
| T09-04: Japanese provenance labels retained in two English JSON specifications | P2 | 330 rows contain Japanese characters in `original_source_focus_ja` or `source_focus_ja`; these are archival source-provenance attributes | Preserve signed original catalogue SHA values; publish a separate English-only 1,716-row traceability projection | **Compensated**; source-provenance fields intentionally retained |
| T09-05: Shell syntax does not imply an effective control predicate | P1 | 1,716 commands parse, but some commands only inspect a file or existence and must be joined to approved signed baselines and independent observation | Require independent scoped evidence + control-specific predicate + reviewer sign-off; do not self-certify based on file existence, HTTP 403 or timeout | **OPEN until approved implementation and review** |
| T09-06: Public GitHub publication risks revealing internal data | P0 (preventive) | Public repository, no approved production source or live evidence | Only publish design text, synthetic fixtures, public-safe tools and SHA-256 digests; exclude secrets, state, subscriptions, customer data and raw logs | **Publication scope restricted** |

`AZ-T74-01` retains the corrected `OFFLINE_POLICY_REVIEW` execution class and **does not count as a live Azure control success**. The original frozen English catalogues are not silently rewritten; any upstream change must undergo review and a new signed manifest.

## 4. Assurance semantics

| Output | What it means | May establish live Azure PASS? |
|---|---|---|
| `PASS` from `validate_catalogue.py` | Identifiers, catalogue digest and documented coverage match | **No** |
| `PASS_WITH_PROJECT_SOURCE_BLOCKERS` from `turn09_audit.py` | Published specifications and frozen source-linked tools are internally coherent; real project-owned tests are still missing | **No** |
| `PASS` from synthetic guard | Artificially constructed valid/invalid examples classified as expected | **No** |
| `REVIEW_REQUIRED` from `evidence_gate.py` | Integrity envelope and externally supplied scope metadata check passed | **No** — control semantics and signoff remain pending |
| `NOT_READY` | No approved baseline, actual resource, authorized runner, evidence or completion criteria | **No** |
| `FAIL` | Approved evidence shows a violated assertion (only after verifying applicability) | **No** |
| `NO_GO` from `release_gate.py` | Independent acceptance conditions remain unmet | **Correct current release state** |

The evidence signature verifier **does not attest the collector hardware, source system, independent scope approval, or actual Azure state**. Source metadata and scopes must be authenticated through separate, trusted channels. Missing independent evidence is not to be interpreted as a secure denial.

## 5. Reproduce the offline audit on WSL2

```bash
set -Eeuo pipefail
REPO="$HOME/azure-private-ai-assurance"
git clone https://github.com/tayoshik/azure-private-ai-assurance.git "$REPO" || test -d "$REPO/.git"
cd "$REPO"
python3 scripts/validate_catalogue.py --root .
python3 scripts/turn09_audit.py --root .
python3 -m unittest discover -s tests -p 'test_turn08.py' -v
python3 -m unittest discover -s tests -p 'test_turn09.py' -v
bash scripts/turn09_offline_regression.sh
python3 scripts/release_gate.py --root .
```

**Expected output:** metadata checks pass; unit tests pass; full synthetic fixture regression succeeds; `turn09_audit.py` reports a named project-source blocker set; release decision remains **NO-GO** and live passes remain **0**. If a public file has not yet been added to GitHub, run the equivalent command from the checksum-verified Turn 09 ZIP only; do not claim the remote command succeeded until verified.

To require the actual application test source and fail on the three outstanding dependencies:

```bash
python3 scripts/turn09_audit.py --root . --strict-source
# Exit code 2 and NOT_READY are expected until project code is supplied.
```

Never run `az login` from the fixed WSL workstation. Azure read-only observations, if explicitly approved in a future phase, are performed on an authorized CI runner using organization-approved identity and private network access. These scripts do not invoke Azure or mutate any real resource.

## 6. Release gates that remain open

1. Pin signed implementation source, Terraform and application revisions, approved regions/SKUs, external dependencies and policies.
2. Recover real Playwright tests for login, session revocation and E2E; resolve project-owned files cited above.
3. Review the 858 proposed observation/review cases for applicability and evidence availability, then execute **only approved relevant controls** in non-production.
4. Validate private gateway, private endpoint routing/DNS, PNA, WAF correlation, managed identity and RBAC, logging, recovery, drift and operational access with independent review.
5. Preserve protected evidence provenance and verify signer trust against an independently approved source, not a key packaged with test data.
6. Independently close critical blockers, document exceptions, and obtain change-board authorization before any production rollout.

**Current conclusion:** English test documentation is cross-linked and offline QA is reproducible, but the system remains **unverified and NO-GO**. The next turn, Turn 10, should issue the final publication manifest, reconcile GitHub commits and workflow results, and hand over a precise source/evidence acquisition checklist. Publishing English documents requires no further user operation; **Azure live acceptance** will require input and explicit approval.