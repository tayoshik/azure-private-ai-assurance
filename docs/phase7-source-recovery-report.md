# Phase 7 source recovery, conservative Plan triage and 1,716-case audit (2026-11-19)

## Authoritative original and immutable digests

Original ZIP: `Azure_閉域AI基盤_試験設計_第7段階_20261110.zip` (November 10, 2026).
The `specs/phase7_220.json` member has exactly **484,125 bytes**, **110 controls**, **220 test IDs** (AZ-T69-01 to AZ-T78-22), and SHA-256:

`27aac2b85153f1ff6c4dc253bcd27960f9454d562d1440e9d99d3a985f8dbb94`

GitHub blob SHA-1 `933013b7782bfa76847b97959c968749221774ba` was compared against the independent local source ZIP. The Phase 7 original refers to Phase 6 SHA-256 `ef5b39269486b293b019ef0cf8b2c9efe4b16b3ddf8b2ec7dba285a60ffd845e`, records 0 Azure passes and notes that live source/application access was not established when drafted.

The English publication `specs/phase7_220_en.json` identifies the same original source SHA and identical 220 test IDs. Precisely 110 command strings differ: *even-numbered synthetic tests* point to the translated spec path; the original 110 odd-numbered positive/review commands remain unchanged. The translated file is not used as the rule authority.

The following approved-original **synthetic fixture** bytes are now tracked:

| Path | SHA-256 |
| --- | --- |
| `fixtures/plan_app_pna_true.json` | `031237e2a65ce3f3b565dd2a20e4a1befb91c1661ba27606b65d18eaeadf028f` |
| `fixtures/plan_nsg_any.json` | `3ecf5a685feef279a2aaf53302fb9bb160c835efbb1b72816d9614ebe5d9a1fe` |
| `fixtures/plan_safe.json` | `5d7f77d66b6e667a0c69208bd793656db1521bc5e6dd35dd473f266a6b7f3653` |

## Why the original source scripts were NOT copied verbatim

The original `scripts/phase7_guard.py` could return exit zero from an unauthenticated local equality comparison. This is not independent Azure acceptance. The new `scripts/phase7_guard.py` is based on the previously hardened Phase 6 guard, pins original Phase 7 SHA-256 and 110/220 identities, denies arbitrary spec paths, supports 220 original synthetic fixture labels, and makes *all local observation* outcomes review-only with exit 2.

The original `scripts/phase7_plan_policy.py` reported `Pass` for minimally specified Terraform plans and returned exit zero when caller-supplied `--expect` matched. The replacement is intentionally incompatible for live acceptance: it only checks narrow local resource attributes; mismatches return `DIFFERENCE_REVIEW_REQUIRED`, incomplete plans return `NOT_READY`, and predicate-compatible plans return `REVIEW_REQUIRED`. Every `--plan` path returns exit code **2**, ignoring `--expect` as an acceptance authority. `--selftest` may return 0 only for three fully synthetic original fixture checks. It has no Terraform or Azure execution.

The three published Plan commands (AZ-T74-01, AZ-T74-03, AZ-T74-13) are *not* independently accepted application/plan policies. The two fixture paths are real files, not evidence of approved Terraform plans.

## Whole-catalogue literal dependency status

| Classification | After Phase 6 | After Phase 7 |
| --- | ---: | ---: |
| Missing direct local code/test path | 126 | **13** |
| Existing direct code/test path | 873 | **986** |
| No direct code/test path | 717 | **717** |
| Cases with missing direct input path | 2 | **0** |
| Independently verified Azure live passes | 0 | **0** |
| Release verdict | NO_GO | **NO_GO** |

The remaining **13** script references are Playwright: `tests/phase6/phase6.spec.ts` (9 cases) and `tests/playwright.config.ts` (4 cases). A file existing is not evidence of test behavior. The 717 cases without a direct local script may be valid Azure CLI, OIDC-runner, or manually reviewed commands. Literal audit cannot validate dynamic paths, missing `evidence/` files, or live security effectiveness.

## CI and safe recheck

~~~bash
python3 scripts/phase7_guard.py --selftest ALL --spec specs/phase7_220.json
python3 scripts/phase7_guard.py --selftest AZ-T69-02 --spec specs/phase7_220_en.json
python3 scripts/phase7_plan_policy.py --selftest
python3 -m unittest discover -s tests -p 'test_phase7_primary_source.py' -v
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py
# Expected refusal: exit 2, NO_GO
python3 scripts/release_gate.py
~~~

`.github/workflows/phase7-primary-source.yml` runs these checks without Azure credentials, and saves sanitized audit evidence for 14 days. The legacy missing-input assertions in `tests/test_catalogue_dependencies.py` were updated to match the restored original fixture files; the strict dependency audit and NO_GO remain enforced.

## Next blockers and review

1. Playwright's actual app source, approved private URL, SSO/identity, selectors, test runner and 9 real test semantics need to be established. Do not create fake browser tests that silently report PASS.
2. Independent review of this branch, and orderly review/merge of stacked draft PR #2 → #3 → #4 → #5 → #6 → this PR #7. Do not merge without explicit review authorization.
3. An approved read-only/isolated Azure test plan and a separately authorized release gate are still required. **No real Azure access was performed during this repair.**
