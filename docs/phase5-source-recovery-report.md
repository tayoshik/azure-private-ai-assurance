# Phase 5 primary source restoration (2026-11-19)

## Exact source and scope

Original source package: `Azure_閉域AI基盤_試験設計_第5段階_20261110.zip`.
Original JSON: `specs/phase5_286.json` (623,475 bytes).
Original SHA-256: `e1a24b145ec7bdd66f3cbe123644e9f060354c7d1aa8d93c193214122d346de3`.
Git blob SHA-1: `6c4b1748bdfd5013c5099ca3232d06ca0c472acc`.
Exactly **143 source-defined control predicates / 286 test IDs**, steps 46–58. The source itself records `live_azure_tests_passed=0`.

The original Phase 5 guard from the archived Japanese source was NOT copied verbatim. In observation mode it returned success exit 0 when a locally supplied value matched, even though its data declared acceptance NotReady. That return code could be misinterpreted as an approved real Azure test. A new `scripts/phase5_guard.py` was implemented with exact source SHA-256 verification, typed values, strict ID coverage and mandatory review-only observation handling. Its only success exit 0 is for explicitly labelled **offline synthetic selftests**. No Azure CLI, credentials or network interactions occur.

The published `specs/phase5_286_en.json` includes source provenance and 286 commands, but it does **not** contain the original source-rule fixture records. A command using `--spec specs/phase5_286_en.json` is now supported as a compatibility entry point only if it verifies the English publication provenance AND loads the exact pinned Japanese original source to evaluate its offline fixtures.

## Translation differences requiring independent review

Among 286 original and published Phase 5 commands, **197 differ**:
- 143 synthetic tests (even-numbered IDs) switch the `--spec` path from the original Japanese JSON to the English publication JSON. The new guard resolves this to the original pinned rules.
- 54 positive/review commands (odd-numbered IDs) differ. Many are jq shell-quoting repairs, but these 54 command changes are **not approved as semantically equivalent by this restoration**. Review the exact command pairs before any authorized execution.

Do not describe the synthetic fixture outcomes as a production acceptance test or proof of 286 independently verified cloud controls.

## Literal dependencies in entire 1,716-case catalogue

| Category | Before Phase 5 | After Phase 5 |
| --- | ---: | ---: |
| Missing code references | 389 | **246** |
| Tracked code references | 610 | **753** |
| No direct code reference | 717 | **717** |
| Missing literal input references | 2 | **2** |
| Azure independently accepted live tests | 0 | **0** |
| Release gate | NO_GO | **NO_GO** |

Source-referenced Phase 5 synthetic tests are now executable. This does NOT mean that Phase 5 positive/read-only Azure steps have been deployed or verified. Two existing missing fixture paths (`fixtures/plan_app_pna_true.json` and `fixtures/plan_nsg_any.json`) remain and are unrelated to the Phase 5 source.

## Offline verification

~~~bash
python3 -m unittest discover -s tests -p 'test_phase5_primary_source.py' -v
python3 scripts/phase5_guard.py --selftest ALL --spec specs/phase5_286.json
python3 scripts/phase5_guard.py --selftest AZ-T46-02 --spec specs/phase5_286_en.json
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py
# The following intentionally refuses release with exit code 2:
python3 scripts/release_gate.py
~~~

CI: `.github/workflows/phase5-original-source.yml`; only local fixture parsing and JSON checks. No Azure permissions or tokens are required.

## Next needed work

Recover Phase 6 and 7 guard paths and any source-dependent steps from frozen sources, plus the two missing plan fixtures. Maintain source provenance and fail-closed result boundaries. Seek independent live Azure observations and approved release evidence only after the implementation dependencies and authorization are complete. The stacked PR remains a draft until review.
