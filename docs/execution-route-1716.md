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

## P2.1 — local-appearing 464-case pre-execution review (no execution)

A source-only risk triage is available in `scripts/triage_local_464.py`. It reads the six **unchanged** English catalogues through `scripts/build_execution_route_1716.py`, checks each of the exact 464 local-appearing IDs against its canonical ID/command/expected fingerprint, and produces a **JSON** case-by-case priority queue without storing or executing command strings. Existing 858 synthetic / 380 live / 13 R41 / 1 odd-selftest cases are not relabeled.

The exclusive priority categories are: **P0 Shell or indirect execution review** (compound shell, redirection, substitution, nested network/indirect tools, uncertain quoting); **P1 Private input and custody review** (environment variables, evidence/plan/baseline paths, missing literal input); **P2 Source tool semantics review** (Python, Terraform, Checkov, TFLint, Node, unknown command); and **P3 Local assertion semantics review** (simple jq/test/grep/find/git/hash predicates with no *detected* higher-priority indicator). Priority refers to **review order, not permission to execute**. A shell-lexical heuristic cannot prove a command is safe, and a local `jq` can require restricted Azure-produced evidence.

Concrete source-grounded illustrations (not claimed passed):

- `AZ-T20-21` begins `cd tests && npm ... && npx`; although its first token is local, it is a compound tool invocation and must never be automatically executed. The historical browser target/source is separately unresolved.
- `AZ-T01-01` uses a Python policy script with an approved baseline environment variable. Merely having the script in Git does not establish an approved, signed baseline.
- `AZ-T21-03` begins with a JSON predicate but requires `$IPAM_JSON` from the appropriate owner; a true expression is not proof of actual network policy.
- `AZ-T45-03` hashes `$APPROVED_PLAN`; plan bytes may contain sensitive material and cannot be uploaded to public CI or read from unapproved locations.
- `AZ-T14-01` reports the Terraform CLI version. Static tool output cannot by itself satisfy live infrastructure control acceptance.

### Safe reproducible WSL procedure (read-only, no az login)

```bash
set -Eeuo pipefail
umask 077
cd "$HOME/azure-private-ai-assurance"  # trusted checkout, no raw evidence checked in
OUT="$(mktemp -d "$HOME/local-review-464-XXXXXXXX")"
chmod 700 "$OUT"
python3 scripts/triage_local_464.py --out "$OUT/local-review-464.json" > "$OUT/summary.json"
python3 -m unittest discover -s tests -p 'test_local_review_464.py' -v
python3 - "$OUT/local-review-464.json" <<'PY'
import json, sys
from collections import Counter
r = json.load(open(sys.argv[1], encoding="utf-8"))
assert r["status"] == "REVIEW_PRIORITIES_ONLY"
assert r["local_candidate_cases"] == len(r["cases"]) == 464
assert sum(r["source_only_priority_counts"].values()) == 464
assert r["commands_executed"] == r["approved_inputs_verified"] == 0
assert r["independent_approvals"] == r["azure_live_passes"] == 0
assert r["release_decision"] == "NO_GO"
assert all(not v["command_executed"] and
           not v["approved_input_verified"] and
           v["azure_live_acceptance"] == "NOT_READY" for v in r["cases"].values())
print("464 source-only priority records checked, no live acceptance")
PY
rc=0
python3 scripts/triage_local_464.py --summary-only --strict > "$OUT/strict.json" || rc=$?
test "$rc" -eq 2
```

The owner/reviewer must **individually** approve each command's purpose, complete shell parsing, dependencies, input classification, immutable checksum, expected predicate and custody **before** execution. No command is authorized by its placement in a lower numbered or lower risk queue. Never run a batch of the canonical 464 commands automatically. All 464 remain `NOT_READY`; this queue changes neither the 1,716 original catalogues nor release NO_GO. CI only runs the source-audit generator and synthetic regressions, and prints a summary instead of archiving commands or private inputs.

## P2.2 — detailed, non-executing P0 review of 149 shell-risk local cases

Following the completed P2.1 **464-case** source-only classification, a second independent source-locked review in `scripts/audit_shell_149_review.py` selects exactly **149** `P0_SHELL_OR_INDIRECT_EXECUTION_REVIEW` IDs. It reads each test's original command **as data only**, checks the canonical ID/command/expected SHA-256 fingerprint against the inherited review queue, and generates only a per-ID JSON **review checklist** (no raw shell commands or private evidence). Original tests are never invoked.

The deterministic **exclusive reviewer order** is:

| Class | Review trigger | Required independent investigation |
| --- | --- | --- |
| A Dynamic/indirect execution | Command substitution, nested network tools, indirect shells/dispatchers, dynamic Python | Review every expansion and nested command; prohibit accidental network/mutating behavior; authorize tool+identity+dependencies separately |
| B Chain/exit status | Shell `&&`, `||`, `;` and background operators after higher-priority checks | Review **all** segments, short-circuit behavior, side effects and final exit status, not merely the first command |
| C Pipeline/data flow | Shell pipelines after A/B checks | Verify every producer/consumer, confidentiality, `pipefail` semantics, actual predicate and safe destination |
| D Redirection/custody | Input/output/fd redirection after A/B/C | Verify allowed paths, no secret uploads, overwrite controls and error suppression |
| E Unparseable/unknown | Incomplete quoting, unsupported punctuation, parent lexical mismatch, or unrecognized P0 | **Do not run**; require explicit manual parsing and correction/approval |

Individual cases can have **multiple overlapping redacted flag codes**; classification is exclusive by precedence A/B/C/D/E except that unparseable/unsupported syntax is escalated to E. This classification is not an executable Bash parser: no class is certified safe, and original canonical commands might have hidden shell behavior even where not flagged.

**Illustrations from frozen source:**

- `AZ-T11-01`: a `test` command joined to `find`. Verify both predicates, whether the output is meaningful, and permissions before running.
- `AZ-T11-19`: source enumeration with an error redirection; ensure suppressed stderr cannot conceal a missing or inaccessible path.
- `AZ-T20-21`: chained `cd`/`npm`/`npx` steps. Its first-token classification as local **does not** permit package installation, browser tests or a network operation. The original Playwright references and R41 decision remain separate pending scope approval.
- `AZ-T45-03`: a direct hash of `$APPROVED_PLAN` is in the **other 464-case P1 data-custody group**, not the shell-risk 149. It still cannot be run without protected, signed inputs. Detailed P0 classification **does not** remove or downgrade that risk.

**WSL source-only check (never executes original commands):**

```bash
set -Eeuo pipefail
umask 077
cd "$HOME/azure-private-ai-assurance"    # trusted checkout of reviewed main
OUT="$(mktemp -d "$HOME/review-shell-p0-149-XXXXXXXX")"
chmod 700 "$OUT"
python3 scripts/audit_shell_149_review.py --out "$OUT/p0-149.json" \
  > "$OUT/summary.json"
python3 -m unittest discover -s tests -p 'test_shell_149_review.py' -v
python3 - "$OUT/p0-149.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1], encoding="utf-8"))
assert r["status"] == "SHELL_SOURCE_TRIAGE_ONLY"
assert r["shell_p0_count"] == len(r["cases"]) == 149
assert sum(r["review_class_counts"].values()) == 149
assert r["commands_executed"] == r["case_reviews_approved"] == 0
assert r["azure_live_passes"] == 0 and r["release_decision"] == "NO_GO"
assert all(not row["command_executed"] and
           not row["actual_command_authorized"] and
           not row["reviewer1_signed"] and
           not row["reviewer2_signed"] for row in r["cases"].values())
print("149 frozen shell-risk cases classified for review only; no execution")
PY
rc=0
python3 scripts/audit_shell_149_review.py --summary-only --strict \
  > "$OUT/strict.json" || rc=$?
test "$rc" -eq 2
```

**Closure gate per original case:** two independent reviewers confirm the exact intended assertion, current inputs/permissions, validated shell parsing, path/network/data-side effects, pinned version, baseline/evidence custody and rollback/incident behavior. Only after owner authorization may a case's actual command be considered for execution in its approved environment. The generated queue makes no acceptance decisions and cannot alter 0/1,716 Azure accepted cases or release NO_GO.

## P2.3 — restricted input / evidence review for 283 local candidates (no real input access)

After P2.1 reviewed 464 local-appearing source commands and P2.2 classified 149 shell-risk cases, the remaining **283 P1 input-and-custody review cases** are handled by `scripts/audit_approved_input_283.py`. The program checks each immutable ID/command/expected digest against its upstream route and splits **review priorities only** by coarse source-text clues. The actual input values, evidence bytes, Azure environments, reviewer approvals and full Bash execution semantics are **not accessed or verified**.

| Review class | Source hint | Minimum independent custody and control review |
| --- | --- | --- |
| A — Terraform plan, state or variable material | `*.tfplan`, `*.tfstate`, `*.tfvars`, approved-plan variables | Approved owner and encrypted private storage; immutable SHA-256, lineage, precise scope, expiry and signed baseline; no public CI uploads |
| B — Restricted observations, audit logs and scan reports | `evidence/`, observed logs, attestation/reference evidence | Recorder/collector identity, time, asset ID, redaction, integrity and separately approved custody |
| C — Network/IPAM/DNS baseline | `IPAM`, subnets/CIDRs, private DNS/VNet/network topology | Versioned owner-approved network truth, resource scope and date; never infer live connectivity from local JSON |
| D — Policy/approval/signed baseline | baseline, policy, approval / approved input | Independent policy owner, signed version, relevant resource scope and semantic expected-result review |
| E — Other environment or unknown source | Variables/inputs not covered above | Manually identify full origin, evidence protection, tool behavior and applicable control assertion |

Classes are **exclusive by A → B → C → D → E**, but evidence categories may overlap. Each case also receives multiple **coarse indicator codes** to alert reviewers to overlapping provenance or storage checks. A class name does not certify that the real input exists or belongs to its expected type; file names and JSON approval flags are not independent attestations.

### Source-based, not executed, examples

- `AZ-T45-03` hashes an environment-provided approved plan. Real Terraform plan bytes may contain secrets; its digest and actual approval cannot be established from public CI.
- `AZ-T21-03` tests a network CIDR property in a locally referenced IPAM JSON. This does not observe actual private routing.
- `AZ-T01-01` runs a policy checker referencing an approved baseline. Script existence alone does not prove the baseline came from the policy owner.
- `AZ-T58-05` references a CI plan artifact. Even a path/hash check cannot establish accepted, signed Azure state or deployment.

### Reproduce safely on WSL (no Azure login, no real input reads)

```bash
set -Eeuo pipefail
umask 077
cd "$HOME/azure-private-ai-assurance"   # trusted reviewed checkout
OUT="$(mktemp -d "$HOME/review-input-p1-283-XXXXXXXX")"
chmod 700 "$OUT"
python3 scripts/audit_approved_input_283.py --out "$OUT/283-review.json" \
  > "$OUT/summary.json"
python3 -m unittest discover -s tests -p 'test_approved_input_283.py' -v
python3 - "$OUT/283-review.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1], encoding="utf-8"))
assert r["status"] == "SOURCE_INPUT_REVIEW_ONLY"
assert len(r["cases"]) == r["restricted_input_283_candidate_count"] == 283
assert sum(r["review_input_class_counts"].values()) == 283
assert r["input_bytes_inspected"] == r["approved_inputs_verified"] == 0
assert r["source_commands_executed"] == r["independent_approvals_verified"] == 0
assert r["azure_live_passes"] == 0 and r["release_decision"] == "NO_GO"
assert all(not x["actual_input_bytes_examined"] and not x["approved_input_hash_verified"]
           and not x["independent_reviewer1_signed"] and not x["independent_reviewer2_signed"]
           and x["azure_live_acceptance"] == "NOT_READY" for x in r["cases"].values())
print("283 source-only input review records; 0 verified evidence; NO_GO")
PY
rc=0
python3 scripts/audit_approved_input_283.py --summary-only --strict \
  > "$OUT/strict.json" || rc=$?
test "$rc" -eq 2
```

**Independent approval gates:** owner supplies evidence in approved private storage with immutable hash and explicit asset scope; reviewer 1 verifies the actual bytes, provenance, rights/identities and intended predicate; reviewer 2 independently signs the evidentiary judgment; only then consider a separately authorized execution. A successful static predicate, signature-pattern match or a local environment variable value cannot promote any of the 283 to Azure PASS. No source test was executed and all 1,716 accepted live cases remain at zero; release remains NO_GO.

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
