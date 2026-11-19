# 1,716 canonical test dependency audit and release-gate recovery

**Status: AUDIT IMPLEMENTED; TEST DEPENDENCIES NOT FULLY RESTORED; LIVE ACCEPTANCE 0/1,716; NO_GO.**

## Why this change exists

The former release_gate.py imported a nonexistent validate_catalogue.py and read a nonexistent catalogue_index_1716.json. Its output could not be trusted as a functioning release decision. The replacement reads the tracked six source catalogues (440+264+286+286+220+220) and always returns NO_GO with exit code 2.

> **2026-11-19 update after Phase 1/2 restoration:** The table immediately below is the frozen **pre-restoration** snapshot, retained for historical traceability. The current snapshot has **669 missing script/test references**, **330 tracked script/test references**, **717 cases with no direct script path**, and **277 cases referencing missing inputs**. See [Phase 1/2 source recovery](phase12-source-recovery-report.md). The Azure live acceptance count remains 0/1,716 and release decision NO_GO.

## Initial snapshot: 2026-11-19

| Literal command classification | Cases | Note |
| --- | ---: | --- |
| Missing direct script/test reference | 999 | Referenced script or test not tracked |
| No direct script/test reference | 717 | Could be valid Azure CLI/manual procedure, not necessarily missing |
| Existing direct script/test reference | 0 | None of the original referenced local scripts resolve |
| Missing literal input reference | 607 | Overlaps the above counts |

Missing code paths (12 distinct, number = referring cases):

| Path | Referring cases |
| --- | ---: |
| scripts/phase1_policy_check.py | 220 |
| scripts/phase4_guard.py | 143 |
| scripts/phase5_guard.py | 143 |
| scripts/phase3_guard.py | 133 |
| scripts/phase2_policy_check.py | 110 |
| scripts/phase6_guard.py | 110 |
| scripts/phase7_guard.py | 110 |
| scripts/phase6_result_classifier.py | 10 |
| tests/phase6/phase6.spec.ts | 9 |
| tests/playwright.config.ts | 4 |
| scripts/plan_policy_guard.py | 4 |
| scripts/phase7_plan_policy.py | 3 |

Missing literal input paths (6 distinct): specs/phase1_policies_110.json (220), specs/phase4_286.json (143), specs/phase3_264.json (132), specs/phase2_220.json (110), fixtures/plan_app_pna_true.json (1), fixtures/plan_nsg_any.json (1).

Empty placeholder files would be a false repair. For each path, recover approved rules and data, implement a genuine control-specific predicate, add good/bad/missing negative regression coverage, and validate evidence scope. Step 26/28/29/30/31 overlays are only partial alternative mappings, not proof the original catalogue commands are implemented.

## Operators: safe commands

~~~bash
python3 scripts/verify_publication.py
python3 scripts/audit_catalogue_dependencies.py --cases --out dependency-audit.json
python3 -m unittest discover -s tests -p 'test_catalogue_dependencies.py' -v
# Expected exit 2 until the missing scripts and inputs are genuinely restored:
python3 scripts/audit_catalogue_dependencies.py --strict
# Expected exit 2 even after catalogue repair, until independent live acceptance:
python3 scripts/release_gate.py
~~~

The default audit exits zero for a structurally valid catalogue while reporting unresolved references. It does not execute any of the 1,716 commands or connect to Azure. The strict audit exits 2 for missing dependencies. The release gate is deliberately incapable of issuing GO; no independently signed live evidence or release authorization has been verified.

The JSON output identifies the exact missing paths, every test ID, and NOT_READY for Azure acceptance. The new GitHub Actions workflow validates it and checks an expected nonzero release-gate status; green CI is *not* proof of a deployed secure platform.

## Remaining independent work

1. Recover and review the original Phase 1/2 policy datasets and implement their criteria.
2. Implement Phase 3–7 guards from authoritative versions of their rule predicates with synthetic good/bad/missing fixture triplets.
3. Implement Step 6 result classifier and the genuine Terraform plan policy checks.
4. Supply real application code, approved private URL, identity and selectors before enabling Playwright tests.
5. Close every missing reference with code/tests and re-run the inventory; still retain NOT_READY for Azure live acceptance.
6. After authorized deployment, collect real scoped observations and seek independent security/release signoff.

## Limitations

Only literal local paths found in catalogue command strings are inspected. Dynamic commands/variable-expanded paths are not resolved. A file that exists is not necessarily executable, correct, or authorized. The catalogue's recorded azure_live_pass=false is a source claim, not independent Azure evidence.

CI: .github/workflows/catalogue-dependency-audit.yml (offline; least-privilege contents:read; 14-day sanitized audit artifact).
