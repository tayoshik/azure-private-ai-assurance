# Phase 3 (264 IDs): frozen-source recovery and fail-closed offline checker

**Date:** 2026-11-19 JST

**Status:** source restored; synthetic-only checks operate; no Azure acceptance; **NO_GO**.

This change is **stacked on draft PR #2**, `fix/phase12-primary-sources-20261119`, which is itself based on `feat/monitoring-private-link`. Merge/rebase only after the parent PR is independently reviewed. Neither branch is main.

## Provenance

The primary archive `Azure_閉域AI基盤_試験設計_第3段階_20261110.zip` contains `specs/phase3_264.json`, `scripts/phase3_guard.py` and synthetic IPAM fixtures. The frozen JSON SHA-256 is:

`66d389a459bd0abc6ce930a1995e6d1328b087c3532849957f2bc458f7336c14`

The English published `specs/phase3_264_en.json` independently records the same source digest.

- Source scope: **264 ID-stable tests** (steps 21–32; 22 cases/step), backed by **132 control fixture records**.
- The English publication preserves the same 264 IDs. Four command strings were explicitly reviewed/edited in English: `AZ-T21-13`, `AZ-T29-19`, `AZ-T31-01`, and `AZ-T31-19`. The other 260 commands are identical. Edits correct quoting/escaping; do not silently overwrite the original source.
- Synthetic fixture rules: 80 `eq`, 46 `nonempty`, 2 `is_succeeded`, one each `no_overlap`, `minimum`, `is_true`, `private_ip`.
- **126/132 rules are generic equality/presence smoke predicates**, not complete tests of each Azure control. Claims of 264 independently verified security controls are prohibited.

The original Phase 3 guard was inspected and used as a functional reference, but the checked-in `scripts/phase3_guard.py` is **a hardened replacement**, not a byte-for-byte copy. It requires the pinned source SHA-256, validates the exact step/polarity/ID structure, distinguishes Python bool vs int, handles unsupported rules safely, and never turns local IPAM matches or mismatches into authoritative Azure acceptance results. An absent/malformed source is NOT_READY.

## Measured literal dependencies (not test implementation coverage)

| Category | After Phase 1/2 | After Phase 3 |
| --- | ---: | ---: |
| Direct missing script/test path | 669 | **536** |
| Direct tracked script/test path | 330 | **463** |
| No direct script/test path | 717 | **717** |
| Cases missing a literal input path | 277 | **145** |
| Canonical IDs | 1,716 | 1,716 |
| Real Azure accepted PASS | 0 | **0** |
| Release | NO_GO | **NO_GO** |

133 cases now resolve `scripts/phase3_guard.py` (132 synthetic commands plus one positive local IPAM-review command); 132 synthetic cases now resolve `specs/phase3_264.json`. The mapping does not mean the original requirement is implemented end-to-end.

Known remaining code dependencies: Phase 4/5/6/7 guards, Phase 6 result classifier, plan policy guards and browser E2E scripts. Remaining input dependencies: `specs/phase4_286.json` and two plan policy fixtures.

## Safe operator and CI checks

From the checked-out branch:

~~~bash
sha256sum specs/phase3_264.json
python3 scripts/phase3_guard.py --selftest ALL
python3 scripts/phase3_guard.py --selftest AZ-T21-02
python3 -m unittest discover -s tests -p 'test_phase3_source_recovery.py' -v
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py
# Both must exit 2, because no live approval exists:
python3 scripts/phase3_guard.py --cidr-check fixtures/ipam_ok.json
python3 scripts/release_gate.py
~~~

The source-bound selftest checks 264 **fixture labels**, not 264 live deployments. IPAM `--cidr-check` returns `REVIEW_REQUIRED` (no structural deviation), `DIFFERENCE_REVIEW_REQUIRED` (structural deviation) or `NOT_READY` (missing/invalid); all exit 2. The fixtures use reserved dummy addresses only; no credential or Azure CLI call is needed.

CI: `.github/workflows/phase3-source-recovery.yml` enforces SHA integrity, 264 fixture smoke tests, negative IPAM paths, original/English four-command variance, the exact 1,716-case ledger, and the fail-closed release gate. The canonical dependency audit regression was updated to use a still-missing Phase 4 path rather than an already restored Phase 3 path.

**Next step:** Phase 4 source and its 143 missing guard/143 missing source references. Verify the primary source and do not fabricate policy or evidence.
