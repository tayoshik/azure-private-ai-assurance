# 1,716-case semantic readiness audit (2026-11-19)

**Purpose:** separate catalogue coverage, checked-in file paths, offline detector correctness, and independently accepted Azure control outcomes. Never infer a GO from a green offline workflow.

## Source scope and methodology

The audit reads the same six tracked published English catalogues used by `scripts/audit_catalogue_dependencies.py` and the full 1,716-ID reference inventory. It does not execute any command string from the catalogues.

Odd-numbered cases are designed for configuration/design/evidence review or approved observation. Even-numbered cases are designed for offline synthetic deviation checks. These categories are **design intent**, not independently completed execution. Phase 1–7 source files and offline guards are present on the stacked PR, but a tracked script is neither proof of complete semantics nor evidence of cloud acceptance.

### Measured current classification

| Category | IDs | Status |
| --- | ---: | --- |
| Even-numbered synthetic detector labels | **858** | OFFLINE_SYNTHETIC_ONLY, does not certify Azure |
| Odd-numbered non-synthetic procedures without independently accepted observations | **844** | UNVERIFIED_NON_SYNTHETIC_PROCEDURE |
| Odd-numbered cases with a missing literal script/test reference | **13** | SOURCE_REFERENCE_MISSING (Playwright) |
| Odd-numbered case whose command runs only `--selftest` | **1** | ODD_SELFTEST_REQUIRES_SEMANTIC_REVIEW |
| **Total** | **1,716** | All Azure acceptance NOT_READY |

The unusual odd-ID selftest is **AZ-T74-13**: `python3 scripts/phase7_plan_policy.py --selftest`. It can be a deliberate offline source selftest rather than an implementation bug; it must not be counted as a validated runtime security outcome. Its test owner should explicitly clarify the intended assertion and evidence type. Do not silently edit the frozen published catalogue.

All 13 remaining missing script references are the known Playwright references: four to `tests/playwright.config.ts` and nine to `tests/phase6/phase6.spec.ts`. The original 717 no-direct-script-reference cases are not classified as automatically unimplemented: commands can legitimately be Azure CLI, Terraform, DNS, file review or manual observation. The 986 tracked script references likewise are not certified as semantically complete simply because the file exists. The narrow literal audit has **zero missing local input references**, not zero runtime inputs.

## Extra per-ID flags generated for review

The audit also reports overlapping, non-exclusive review flags. **The initial GitHub Actions report identified 160 odd-case artifact-presence commands** requiring explicit comparison with approved expected content and control baselines; this is a review queue, not 160 proven failures:

- `REAL_APP_AUTH_AND_RUNNER_REQUIRED` for all 13 browser-related cases.
- `ODD_ID_RUNS_SELFTEST_NOT_RUNTIME_EVIDENCE` for AZ-T74-13.
- `ARTIFACT_PRESENCE_NEEDS_CONTENT_AND_BASELINE_REVIEW` for odd commands beginning with file existence, grep, find or sha256sum; successful exit is not proof of the control's meaning.
- `NO_LOCAL_SCRIPT_REF_CLI_OR_MANUAL_REVIEW` for 717 no-direct-reference cases. This is a **review routing hint**, not evidence of missing or passed tests.
- `EVEN_ID_NO_EXPLICIT_SELFTEST_OPTION`, if future source edits lose a synthetic selftest designation.
- `UNRESOLVED_LITERAL_PATH` for any missing script or input.

The `--cases` output contains one row per ID with phase, published execution class, file references, semantic readiness and reviewer flags. The job uploads its generated JSON as a 14-day, offline-only artifact. Do not republish live observations, subscription IDs, tokens, Terraform state, or customer materials to this public repository.

## Gates and boundaries

`scripts/audit_semantic_readiness.py` supports ordinary reporting (exit 0 if the **source inventory** is structurally valid) and `--strict` (exit 2 because independently accepted Azure evidence is not established). The strict gate deliberately cannot issue GO. Existing independent `scripts/release_gate.py` must also return exit 2 and decision NO_GO.

```bash
python3 scripts/audit_semantic_readiness.py --cases --out /tmp/semantic-readiness-1716.json
python3 -m unittest discover -s tests -p 'test_semantic_readiness.py' -v
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py
# Expected refusal, exit code 2:
python3 scripts/audit_semantic_readiness.py --strict
python3 scripts/release_gate.py
```

This is an **automated pre-review index**. Reviewers must still establish whether each test actually checks its approved, sufficiently precise security requirement. File presence, shell syntax, HTTP 403, a green CI job, a successful synthetic fixture, or a self-asserted JSON status cannot provide live acceptance.

## Suggested next review DAG (all currently OPEN)

1. **SA-01 / owner decision** — AZ-T74-13: confirm whether the odd-numbered Plan Policy selftest should remain an explicitly labelled local-only case or whether a separate evidence procedure is required. Do not change immutable source without approval.
2. **SA-02 / security reviewer** — Prioritize odd cases using existence-only checks and determine required content/criterion/baseline comparisons. Keep the source command as historical reference until revised and independently reviewed.
3. **SA-03 / app and CI owners** — Supply real app source/immutable artifact, HTTPS hostname, Entra login/session, page selectors, safe test data and approved private & external runners for the 13 Playwright IDs; use the PR #9 strict intake contract.
4. **SA-04 / independent reviewers** — Complete source-to-criterion semantic checks for the other 844 odd procedures and add actual approved evidence when available. A successful offline source inspection is not acceptance.
5. **SA-05 / PR integrator** — Independently review and integrate the draft PR chain #2 through #10 in order, rerun all offline checks, and retain protected live acceptance outside this repository until approved.

**Snapshot:** 1,716 IDs, 858 synthetic, 844 non-synthetic unverified, 13 missing browser references, 1 odd selftest, 0 verified Azure live PASS, release NO_GO. No Azure login, Terraform plan/apply, browser, network probes or GitHub merges were performed.
