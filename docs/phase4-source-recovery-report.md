# Phase 4 guard and original rule data restored (2026-11-19)

## Scope and provenance

This is an **offline code-only recovery** stacked on draft PR #3 (which is stacked on draft PR #2). No Azure subscription, workload, or operational acceptance was touched.

Frozen original:
- Archive: Azure_閉域AI基盤_試験設計_第4段階_20261110.zip (saved in ChatGPT conversation files)
- Original rule/test JSON: specs/phase4_286.json
- Original JSON SHA-256: b221babf4a1b7a17763723d06229e868b943748cbbf6c1b0726e8f07465fcf36
- Count: 143 control rules / 286 test IDs (AZ-T33-01 to AZ-T45-22)
- Source claim: live_azure_successes = 0
- Original guard script SHA-256: 7bc94a9f3c5bc4d8ce8e65becbd4f3c67635d1b2f6dfa75a40cd710bb8bc9d8a
- The original script runs 286 synthetic checks successfully **but** observation mode returns exit 0 on locally matched values even though its output says NotReady. That exit code could be misconstrued by a CI consumer.

The replacement scripts/phase4_guard.py uses typed predicates, strict 286 ID / 143 control assertions, rejection of malformed/synthetic provenance, and makes every observation-mode result exit 2 with REVIEW_REQUIRED, DIFFERENCE_REVIEW_REQUIRED, or NOT_READY. Only successful synthetic fixture selftests may return exit 0. Never promote them to Azure acceptance.

**The exact 600,202-byte original JSON is now committed** at `specs/phase4_286.json`; its Git blob SHA-1 is `27f497770afac4bf34076b3c7df23d8508fff542`, verified against the original frozen source. The source SHA-256 is pinned in the workflow. The publication file `specs/phase4_286_en.json` retains source-era metadata and 37 documented command edits; it is not a substitute for the original predicates. `python3 scripts/phase4_guard.py --selftest ALL` now runs all 286 frozen synthetic checks on GitHub. Synthetic success still cannot provide real Azure PASS.

## Actual current dependency status

| Category | Before Phase 4 guard | Now |
| --- | ---: | ---: |
| Cases referencing a missing code path | 536 | **389** |
| Cases referencing a tracked code path | 463 | **610** |
| Cases with no direct script path | 717 | 717 |
| Cases referencing missing literal input file | 145 | **2** |
| Azure live accepted passes | 0 | 0 |
| Release | NO_GO | NO_GO |

**The source-rule input has also been restored.** Phase 4 now runs 143 frozen control rules and all 286 associated synthetic labels. The two remaining missing literal files are `fixtures/plan_app_pna_true.json` and `fixtures/plan_nsg_any.json` (separate plan-policy regressions). No Azure execution or independent live acceptance has occurred.

## Stage 45 plan guard provenance and release behavior

The Stage 45 plan-policy source in English Turn 05 (original SHA-256 d5ca30c66a6024fa4d52b967c9c5c2e95a00cd86d404375025b8768446538b71) has been independently reviewed and hardened. The original returned exit 0 on REVIEW_REQUIRED; the replacement always exits 2 on REVIEW_REQUIRED/NOT_READY and exits 1 for an observed synthetic policy FAIL. It parses a read-only local plan JSON and requires a pinned plan hash and approved scope, but cannot independently attest those records or approve a deployment. Four canonical Phase 4 commands for AZ-T45-09/11/13/15 now resolve to this tracked script. Source-specific regressions cover public IP creation, PaaS public access, broad RBAC, diagnostics removal, malformed or absent evidence, and forced NO_GO. No Terraform plan or apply is executed.

## Read-only local source review

After acquiring the exact primary source ZIP (do not execute code from the archive directly), verify hash and unpack only the trusted JSON to specs/phase4_286.json. From the checkout:

~~~bash
sha256sum specs/phase4_286.json
# Expected:
# b221babf4a1b7a17763723d06229e868b943748cbbf6c1b0726e8f07465fcf36

python3 scripts/phase4_guard.py --selftest ALL --spec specs/phase4_286.json
python3 -m unittest discover -s tests -p 'test_phase4_guard_recovery.py' -v
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py
# Expected refusal (exit 2):
python3 scripts/release_gate.py
~~~

The ledger is unchanged by adding the input JSON because it classifies executable script references; the independent dependency audit now reports two missing plan input references. The source-pending CI was replaced by a SHA-pinned original-source 286-case assertion; missing data is never ignored.

## Next actions

1. Review source-preserving original JSON blob and the 37 documented command edits. Synthetic pass is not deployed-resource evidence.
2. Recover the two missing plan fixture files from their frozen original sources, with negative-path tests.
3. Continue Phase 5 guard recovery and source identity for steps 46–58, preserving NO_GO until independent live acceptance.
