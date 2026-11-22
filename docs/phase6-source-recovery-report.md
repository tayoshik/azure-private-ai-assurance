# Phase 6 source recovery and offline control classification (2026-11-19)

## Provenance, scope, and immutable source

- Original: `Azure_閉域AI基盤_試験設計_第6段階_20261110.zip`, member `specs/phase6_220.json`
- Original SHA-256: `ef5b39269486b293b019ef0cf8b2c9efe4b16b3ddf8b2ec7dba285a60ffd845e`
- 110 original control definitions, 220 test-case IDs, AZ-T59-01 to AZ-T68-22, 10 steps, 22 cases each.
- Original source states `live_azure_tests_passed = 0`. It also states that the actual application/infra source had not been reviewed.
- `specs/phase6_220_en.json` identifies this exact original SHA. Its **110 command differences** all point offline-synthetic even-numbered test commands to the English translation spec. No odd-numbered live command change was found.
- The new guard verifies the original SHA-256, all 110 control IDs, 220 case IDs, provenance and original test statuses before using rule metadata. A translated spec can select the existing CLI syntax, but never replace the original source authority.

## Implementation and security review

`scripts/phase6_guard.py`: typed, local fixture-only predicate checks; supports 220 `--selftest` labels, including positive and negative examples. Legacy English `--selftest AZ-Txx-yy --spec specs/phase6_220_en.json` points back to the frozen original. Missing, tampered or misdirected specs return NOT_READY, exit 2. Evaluating a locally supplied positive-looking observation yields REVIEW_REQUIRED at most; disagreement yields DIFFERENCE_REVIEW_REQUIRED, both exit 2. It never makes an Azure acceptance decision.

`scripts/phase6_result_classifier.py`: rejects untrusted/missing data, treats 403/timeout/NXDOMAIN as **NOT_READY** (not proof of isolation), and treats suspicious public IP / unauthorized HTTP 200 as DIFFERENCE_REVIEW_REQUIRED. A local or synthetic correlated denial yields REVIEW_REQUIRED at most, never Azure PASS. Ten synthetic classifier smoke cases are regression-tested. For all `--input` invocations it returns exit 2 regardless of the legacy `--expected Pass|Fail|NotReady` argument. This **intentionally differs from** the old original classifier, which could return `Pass` and exit 0 based only on self-asserted JSON values.

**Do not** commit the original Phase 6 synthetic Python-dict fixtures into the referenced `evidence/phase6/classification/` paths as though they were collected live. They are untrusted generated data, and the original fixture files use Python literal syntax rather than strict JSON. The `--selftest` option provides in-memory synthetic cases.

## Entire-catalogue literal dependency counts

| Classification | After Phase 5 | After Phase 6 |
| --- | ---: | ---: |
| Direct references to missing scripts/tests | 246 | **126** |
| References to tracked scripts/tests | 753 | **873** |
| No direct script/test reference | 717 | **717** |
| Missing literal input references | 2 | **2** |
| Independently accepted Azure live tests | 0 | **0** |
| Release decision | NO_GO | **NO_GO** |

120 original command paths become tracked: 110 `scripts/phase6_guard.py` and 10 `scripts/phase6_result_classifier.py`. This is **path restoration**, not 120 independently verified control outcomes. The remaining 126 missing code references involve Phase 7 guard/plan rules and Playwright tests/config; adding an unconditional-pass stub would defeat the purpose of the audit.

Missing inputs are the two Terraform Plan fixtures `fixtures/plan_app_pna_true.json` and `fixtures/plan_nsg_any.json`. Additional evidence paths under `evidence/` are outside the narrow literal-input regex and are NOT counted as resolved merely because no missing-input result was reported for them.

## Safe reproduction commands

~~~bash
python3 scripts/phase6_guard.py --selftest ALL --spec specs/phase6_220.json
python3 scripts/phase6_guard.py --selftest AZ-T59-02 --spec specs/phase6_220_en.json
python3 scripts/phase6_result_classifier.py --selftest
python3 -m unittest discover -s tests -p 'test_phase6_primary_source.py' -v
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py
# Expected exit=2 / NO_GO, no credentials used:
python3 scripts/release_gate.py
~~~

GitHub Actions workflow `.github/workflows/phase6-primary-source.yml` runs source integrity, negative-path tests, the 1,716 ledger and an expected NO_GO. Existing Phase 5 workflow's fixed dependency count was upgraded to a monotonic bound so later phases can restore files without falsely failing it, **without weakening the original-source or zero-live-acceptance checks**.

This PR is stacked on the unmerged Phase 5 PR #5 (which itself stacks on #4 → #3 → #2), and does not target main. No Azure credential, login, Terraform plan or apply is used.

## Next bounded work

1. Phase 7: recover 110-rule / 220-case original and two plan-policy scripts, verify SHA and source-vs-translation command changes; **do not** count synthetic fixture checks as Azure PASS.
2. Playwright: confirm real UI source, auth and selector contracts; do not create tests that can appear to pass without approved private runner/application.
3. Terraform plan fixture inputs: restore only from approved source, verify negative outcomes; never publish real Terraform state or plans.
4. Independently collect real Azure evidence in approved private/OIDC runners before release consideration.
