# P5 — Full 1,716-case execution route / prerequisites inventory

**Prepared:** 2026-11-22. **Environment:** no authorized Azure infrastructure available. This is a read-only, **source-based routing audit**, not execution, semantic acceptance, deployment or release authorization.

## Source-of-truth boundaries

Read exactly six original English catalogues in `scripts/audit_catalogue_dependencies.py`:

1. `specs/english_tests_001_440.json` — Phase 1 and 2, 440 cases.
2. `specs/phase3_264_en.json` — Phase 3, 264 cases.
3. `specs/phase4_286_en.json` — Phase 4, 286 cases.
4. `specs/phase5_286_en.json` — Phase 5, 286 cases.
5. `specs/phase6_220_en.json` — Phase 6, 220 cases.
6. `specs/phase7_220_en.json` — Phase 7, 220 cases.

Join the **existing**, separately tested `scripts/audit_semantic_readiness.py` and `scripts/audit_catalogue_dependencies.py` reports with the **R41 unapproved 13-case crosswalk** (`scripts/audit_rest_r41_rescope.py`). Do not reinterpret missing files as proof of unsafe service or replace browser tests with fabricated API tests.

## Existing mutually exclusive semantic partition

| Frozen semantic classification | Count | Meaning |
| --- | ---: | --- |
| `OFFLINE_SYNTHETIC_ONLY` | 858 | Even-numbered detector-design cases; execution not proven |
| `UNVERIFIED_NON_SYNTHETIC_PROCEDURE` | 844 | Odd-numbered non-synthetic commands without approved runtime evidence |
| `SOURCE_REFERENCE_MISSING` | 13 | Original Playwright references; R41 changes still unapproved |
| `ODD_SELFTEST_REQUIRES_SEMANTIC_REVIEW` | 1 | `AZ-T74-13`; an odd selftest is not live evidence |
| **TOTAL** | **1,716** | **0 Azure passes, 1,716 NOT_READY, release NO_GO** |

Historical literal-path audit: 13 references to two missing `.ts` paths, 986 cases with a tracked script reference and 717 cases with no direct local script reference. The 717 may be Azure CLI, manual, or approved review procedures and **must not automatically be called unimplemented**.

## New execution routing (independent axis, one exclusive lane per ID)

| Lane | Source rule | Minimum prerequisites | Next action |
| --- | --- | --- | --- |
| `OFFLINE_SYNTHETIC_CANDIDATE` | Exactly 858 even-numbered synthetic IDs; requires Python candidate command | Pinned dependency-free runner, synthetic baseline, control-specific assertion review | Run & review offline detector; **do not** count as Azure PASS |
| `LOCAL_APPROVED_INPUT_AND_REVIEW` | Odd, non-synthetic IDs whose *leading* command is not a live network/plan command | Approved plan/baseline/evidence file, comparison beyond file presence, independent review | Owner supplies verified input and reviewer confirms exact semantic predicate |
| `AZURE_OR_PRIVATE_RUNNER_REQUIRED` | Odd commands led by `az`, `dig`, `curl`, `getent`, `openssl`, `npx`, or Terraform `plan/apply/refresh/import/state` | Authorized Azure nonprod resource + protected OIDC/private-network runner + independently signed baseline | **Defer direct command** until environment and approval exist |
| `LEGACY_R41_SCOPE_DECISION_REQUIRED` | Exactly 13 unmodified Playwright references | Individual owner-approved R41 disposition and versioned replacement/N/A, real app or API contract | Approve/reject the scope change; do **not** auto-credit a REST mock |
| `ODD_SELFTEST_SEMANTIC_DECISION_REQUIRED` | Exactly `AZ-T74-13` | Owner decides whether odd selftest can satisfy its original predicate | Keep review open; no implied runtime evidence |

**Counts of the two 844-ID lanes are computed from the frozen commands by `scripts/build_execution_route_1716.py`. They are not manually guessed or hardcoded.**

Routing is deliberately *only a scheduling hint*. Commands that start with a local tool can still reference externally produced Azure artifacts, and compound shell commands are **not** exhaustively safety-parsed. A case placed in the local lane is **not certified runnable now**: `approved_inputs_verified=false` and `source_test_executed=false` for every ID. The script NEVER executes command strings.

## P2 — verified split of 844 unapproved non-synthetic cases

On 2026-11-22 the six original English catalogues were read (not executed) and reconciled with the existing command-prefix routing rules in `scripts/build_execution_route_1716.py`. This *does not* change the frozen catalogues or create a new acceptance class.

| Frozen catalogue | Total | Offline synthetic candidate | Local approved input/review | Azure/private runner | R41 decision | Odd selftest |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Phase 1–2 (`english_tests_001_440.json`) | 440 | 220 | 171 | 45 | 4 | 0 |
| Phase 3 (`phase3_264_en.json`) | 264 | 132 | 29 | 103 | 0 | 0 |
| Phase 4 (`phase4_286_en.json`) | 286 | 143 | 59 | 84 | 0 | 0 |
| Phase 5 (`phase5_286_en.json`) | 286 | 143 | 64 | 79 | 0 | 0 |
| Phase 6 (`phase6_220_en.json`) | 220 | 110 | 49 | 52 | 9 | 0 |
| Phase 7 (`phase7_220_en.json`) | 220 | 110 | 92 | 17 | 0 | 1 |
| **Total** | **1,716** | **858** | **464** | **380** | **13** | **1** |

The 464 local *candidate* command prefixes are `jq` **159**, `test` **138**, `python3` **127**, and **40 other** commands. The 380 Azure/private-network *candidate* prefixes are `az` **321**, `dig` **33**, `curl` **11**, `terraform` **11**, `openssl` **3**, and `getent` **1**. **Command prefixes are scheduling hints, not executable-safety evidence**. A local command may read sensitive Azure-produced plan/state/log data. A compound shell command may contain remote calls after the first token.

### Execution queue and evidence gates (no automatic live execution)

1. **Route inventory (source-only):** Generate the existing 1,716-ID JSON report, verify all five mutually exclusive lane counts, verify unique source fingerprints and do not execute the stored command strings. This metadata audit itself cannot grant Azure acceptance.
2. **Offline synthetic candidate review (858):** Verify original predicate, safe/unsafe fixture, pinned dependency and full command safety before an authorized offline execution. Store signed synthetic evidence separately; mark *synthetic only*, not live PASS.
3. **Local approved-input queue (464):** Verify that each exact input/baseline file exists in approved private storage; pin original command and expected assertion; confirm scope, exit-code interpretation, logs, reviewer and immutable input checksum. Do not run all `jq`/`test` commands by default. An existence or grep success is insufficient evidence for a real control. Prioritize 159 JSON-assertion, 138 existence/predicate and 127 Python commands for *manual semantic review*, not automatic PASS.
4. **Azure/private-runner queue (380):** Require G07 approved target, B05 private state readiness, exact resource IDs, approved federated identity and isolated runner, signed expected baseline and separate reviewer authorization. Fixed WSL does **not** run `az login`, `terraform plan/apply` or unapproved network probes. Actual Azure test evidence stays in restricted approved storage.
5. **Frozen-scope blockers (14):** R41 has 13 proposed but unapproved browser-to-REST substitutions. `AZ-T74-13` is an odd policy selftest whose original criterion is only synthetic safe/failing fixtures; this does not establish live behavior. Both remain NOT_READY until a versioned owner decision and independent reviewer signoff.
6. **Acceptance gate:** Reconcile per-case result, UTC, approved baseline, evidence hashes and independent reviewers. NO_GO until actual owner-approved independent acceptance has been completed; no synthetic or static success can count toward 1,716 Azure live PASSES.

### WSL offline-only reproduction

```bash
set -Eeuo pipefail
umask 077
cd "$HOME/azure-private-ai-assurance"  # verified trusted repository checkout
OUT="$(mktemp -d "$HOME/azure-route-review-XXXXXXXX")"
chmod 700 "$OUT"
python3 scripts/build_execution_route_1716.py --out "$OUT/execution-route-1716.json" > "$OUT/summary.json"
python3 -m unittest discover -s tests -p 'test_execution_route_1716.py' -v
python3 - "$OUT/execution-route-1716.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1], encoding="utf-8"))
expected = {
  "OFFLINE_SYNTHETIC_CANDIDATE": 858,
  "LOCAL_APPROVED_INPUT_AND_REVIEW": 464,
  "AZURE_OR_PRIVATE_RUNNER_REQUIRED": 380,
  "LEGACY_R41_SCOPE_DECISION_REQUIRED": 13,
  "ODD_SELFTEST_SEMANTIC_DECISION_REQUIRED": 1,
}
assert r["status"] == "ROUTING_INVENTORY_ONLY" and not r["errors"]
assert r["route_counts"] == expected
assert len(r["cases"]) == 1716
assert r["source_cases_executed_by_this_report"] == 0
assert r["azure_live_passes_verified"] == 0
assert r["release_decision"] == "NO_GO"
print("1716 source routes verified, 0 Azure acceptance: NO_GO")
PY
rc=0
python3 scripts/build_execution_route_1716.py --summary-only --strict \
  > "$OUT/strict.json" || rc=$?
test "$rc" -eq 2
```

**Review boundary:** All outputs above remain private source-only routing evidence. The command cannot run Azure, and it does not sign off any case. No restricted customer information should be copied into the public repository or public GitHub Actions logs.

## Per-ID JSON schema

Generate an output-only JSON object with exactly 1,716 `cases` entries. Every entry contains:

- Canonical ID (JSON map key), source file, phase, original `execution_class`, odd/even polarity and semantic readiness.
- SHA-256 of canonical ID + command + expected criterion (fingerprint only, **not an independent source signature**).
- Command family, local script/input literal references, unresolved paths, assigned route and proposed—not actually assigned—owner role.
- Exact prerequisite class list, proposed next action, `source_test_executed=false`, `approved_inputs_verified=false`, `independent_reviewer_signed=false`, `azure_live_acceptance=NOT_READY`.
- R41 scope approval remains false for only those historical 13 IDs; no canonical records are edited.

The report also records route counts and phase counts, zero Azure passes and `NO_GO`. The **entire output is metadata-only** and omits command text, raw observations, token values, tenant IDs, customer data, and Azure resource identifiers. Do not publish actual live evidence as public CI artifacts.

## Reproduce (offline, no Azure, no az login)

```bash
set -Eeuo pipefail
python3 scripts/build_execution_route_1716.py --out /tmp/execution-route-1716.json
python3 scripts/build_execution_route_1716.py --summary-only > /tmp/execution-route-summary.json
python3 -m unittest discover -s tests -p 'test_execution_route_1716.py' -v
python3 scripts/audit_semantic_readiness.py --cases --out /tmp/semantic-readiness.json > /tmp/semantic-readiness-summary.json
python3 scripts/audit_catalogue_dependencies.py --out /tmp/literal-dependencies.json
# The stricter assurance condition MUST refuse incomplete Azure acceptance:
rc=0
python3 scripts/build_execution_route_1716.py --summary-only --strict > /tmp/execution-route-strict.json || rc=$?
test "$rc" -eq 2
```

The normal command returns zero for **internally consistent routing inventory**, **not test execution success**. The strict command deliberately returns 2 while independent evidence is missing. Output is JSON, not CSV. GitHub Actions retains the offline summary and 1,716-row metadata inventory for **14 days**.

## Dependency-oriented follow-up DAG

- **P5-01:** Source audit + deterministic route metadata for all 1,716 IDs — close only when GitHub CI passes and all counts align with both old audits.
- **P5-02:** Resolve odd `AZ-T74-13` selftest semantic question with an owner-approved disposition.
- **P5-03:** Review local command cases requiring approved artifacts or existence-only/grep checks; compare real control meaning, not just exit status.
- **P5-04:** Approve/reject R41 13-case requirement changes individually, and keep the old catalogue immutable until a versioned successor is approved.
- **P5-05:** Maintain the Azure/private-runner queue as `NOT_READY`; attach approved nonprod resource scopes and private runner/OIDC evidence after the environment is available.
- **P5-06:** Final independent case-by-case semantic and runbook review; no release GO from this audit.

The next global priority after this deterministic inventory is **#6: DAG file path and repository source consistency**, without Azure access.

**Safety invariant:** Azure live accepted = **0**; historical 1,716 cases **unchanged**; release **NO_GO**.
