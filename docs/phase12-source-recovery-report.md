# Phase 1 / Phase 2 primary-source recovery: 2026-11-19

## Provenance and unchanged release boundary

This patch restores **verified, frozen Phase 1 and 2 source files** and maintains an OFFLINE-ONLY, fail-closed release boundary. PR #1 was merged into feat/monitoring-private-link at 2026-11-19T04:23:58Z. This change is a new PR based on that feature branch, not main.

| File | Source and SHA-256 |
| --- | --- |
| specs/phase1_policies_110.json | Phase 9 corrected and English Turn 03: ba0fb3899f32d71ac40dad01aebb536d11094f38abd9bbe77245ac69dad3c37d |
| scripts/phase1_policy_check.py | Original Phase 9/English Turn 03 source SHA-256 8c1ac9ab207d4689598f80c80fc51cf292ef7e950941e567d3cc6861c3b1d662; the checked-in version has been **security hardened** |
| specs/phase2_220.json | English Turn 03 SHA-256 6a8ad751e772b180ad0af337180eb8236d3c507efdc86e0c5f20e45689d68906; 220 IDs and commands exactly match the Japanese Phase 2 source and the published English catalogue |
| scripts/phase2_policy_check.py | Hardened in the merged PR #1; used instead of the unsafe original script |

The original Phase 2 checker is NOT restored: its local equality check could falsely imply PASS. Phase 2 runs 110 ID-labeled smoke checks of a common typed-comparison operator; these are NOT 110 independently implemented per-control validators.

The Phase 1 checker now treats unsigned local equality as REVIEW_REQUIRED, local deviation as DIFFERENCE_REVIEW_REQUIRED, missing/synthetic data as NOT_READY. Baseline-mode exits 2 in every case. Only synthetic selftest mode exits 0 when every test succeeds.

## Literal command dependency status

| Category | Before restoration | After restoration |
| --- | ---: | ---: |
| Direct missing script/test references | 999 | **669** |
| Direct existing script/test references | 0 | **330** |
| No direct script/test reference | 717 | **717** |
| Cases with missing input reference | 607 | **277** |
| Canonical test IDs | 1,716 | **1,716** |
| Independently accepted Azure live tests | 0 | **0** |
| Release verdict | NO_GO | **NO_GO** |

Restoring a file reference does not mean its full test procedure or control semantics is verified. Existing monitored workflow checks expected ledger formatting; specs/test-automation-ledger.json was regenerated without changing the historical baseline.

## Offline commands and CI

~~~bash
python3 scripts/verify_english_tests.py
python3 scripts/verify_publication.py
python3 scripts/phase1_policy_check.py --selftest --all
python3 scripts/phase2_policy_check.py --selftest ALL
python3 -m unittest discover -s tests -p 'test_phase12_canonical_sources.py' -v
python3 -m unittest discover -s tests -p 'test_phase2_policy.py' -v
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py
# Expected exit code 2, NO_GO
python3 scripts/release_gate.py
~~~

The Phase 1-2 source CI does not authenticate to Azure. GitHub Monitor offline CI also runs the automation ledger consistency gate. Existing fail-closed scripts must not be bypassed to obtain green status.

## Remaining dependencies and next action

Phase 3–7 guard implementations, Phase 3/4 source-specific rule JSON, Phase 6 result classifier, plan-policy guards, and Playwright assets remain pending. The next source task is Phase 3 (264 IDs): restore primary guard and its rule inputs, compare exact commands, test control-specific deviation rules, and keep all Azure live acceptance NOT_READY. No operator needs to execute Azure CLI login, Terraform plan or apply for this offline source repair.
