# Phase 4 guard restoration, original rule data pending (2026-11-19)

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

**The 600,202-byte original JSON has NOT been committed yet.** It is provided separately as a SHA-256-checked source file in the companion conversation artifact. The English publication specs/phase4_286_en.json is already tracked but lacks the 143 original fixture predicates and cannot replace the frozen original. Do not fabricate or generate placeholder JSON. The default Phase 4 guard therefore correctly returns NOT_READY.

## Actual current dependency status

| Category | Before Phase 4 guard | Now |
| --- | ---: | ---: |
| Cases referencing a missing code path | 536 | 393 |
| Cases referencing a tracked code path | 463 | 606 |
| Cases with no direct script path | 717 | 717 |
| Cases referencing missing literal input file | 145 | 145 |
| Azure live accepted passes | 0 | 0 |
| Release | NO_GO | NO_GO |

**This restores only the script path, not the 143 control-specific rule input references or their Azure execution.** The program is not ready for 286 original-case selftests on GitHub until the exact source is checked in.

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

The ledger and CI need regenerating once the genuine source JSON is present, and the source-pending CI's expected refusal assertion must be replaced by an original-source 286-case selftest assertion (not by ignoring missing data).

## Next actions

1. Move the exact source bytes into the repository via an approved GitHub binary/file-transfer path; do not transcribe or re-create the original.
2. Add source hash validation in CI and run all original 286 synthetic tests. Compare all 286 original command strings with the 286 English publications; review documented jq quote edits.
3. Review the existing Stage 45 plan-policy original guard separately. Its review-required CLI returns 0 and therefore needs a fail-closed exit convention before restoration; avoid treating mere plan-file existence as compliance.
4. Restore independent baseline and review evidence for real Azure tests only through approved CI/runner; this repository cannot issue GO.
