# 160 static-presence procedures: source-grounded risk review (2026-11-19)

**Scope:** offline-only audit; no Azure observation, runtime/browser test, Terraform plan or apply. Stacked draft PR #11 on top of draft PR #10.

## Why these checks need review

PR #10 established that 160 **odd-numbered** test commands begin with file presence, grep, find, ls or sha256sum. That means their successful exit often establishes only that a file or text exists. A source-level criterion may require a stronger assertion. This PR does not change any of the frozen published command strings, original Japanese source JSON, catalogue ID mapping, or recorded Azure results.

\`scripts/triage_static_criteria.py\` generates an ordered, exact 160-case JSON review queue from the six canonical English catalogues. Each row records the unmodified published command and acceptance criterion, case-specific risk reason, remediation request, priority, and perpetual \`NOT_READY\` acceptance. Risk scores rank review effort and are **not vulnerability scores** or independent findings of a failed control.

## Five highest-priority, demonstrable semantic gaps

| ID | Original check | Specific gap | New optional review aid |
| --- | --- | --- | --- |
| AZ-T20-13 | grep for \`ignoreHTTPSErrors\` | Both \`ignoreHTTPSErrors: false\` and unsafe \`true\` can match; presence cannot prove TLS validation | Detect obvious unsafe TLS-bypass patterns; no source-based TLS approval |
| AZ-T45-03 | \`sha256sum "$APPROVED_PLAN"\` | Outputs a digest but does not compare to the approved plan digest | Hash the *actual local file bytes* and compare to a separately supplied claimed approved SHA-256 |
| AZ-T45-19 | \`jq '.reviewers \| unique \| length >= 2'\` | Two distinct entries may include the change author or execution operator; roles may not be independent | Require two distinct, separate-role reviewer identities excluded from author/executor |
| AZ-T40-11 | \`jq '.digest and .commit'\` | Nonempty fields do not bind a deployed artifact to the authorized source commit | Compare typed artifact SHA-256 and source commit with the separately supplied approval |
| AZ-T45-21 | \`jq '.plan_sha256 and .commit_sha and .executor'\` | Existence of metadata does not prove that the *approved* plan, source or executor was used | Require matching plan SHA-256, source commit, executor and change ticket |

These are **not corrected live tests**. The five-case helper \`scripts/review_high_risk_static.py\` accepts untrusted local observation/approval JSON, checks for obvious mismatches, and always exits **2**. Matching metadata yields **REVIEW_REQUIRED**, mismatches **DIFFERENCE_REVIEW_REQUIRED**, and missing inputs **NOT_READY**. A review-required state cannot become Azure PASS without verified signatures, asset scope and independent approval.

The TLS check is a conservative lexical scan for dangerous literals; absence of a match does **not** prove the actual TLS implementation is safe. A supplied hash/approval JSON is *self-asserted* until a separate approval authority validates the provenance. Do not treat equality as a signed attestation.

## Reproduction and safeguards

~~~bash
python3 scripts/triage_static_criteria.py --out /tmp/static-160-review.json
python3 -m unittest discover -s tests -p 'test_static_criteria_review.py' -v
python3 scripts/audit_semantic_readiness.py --summary
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py
# Strict review and release gate intentionally return 2:
python3 scripts/triage_static_criteria.py --strict --summary
python3 scripts/release_gate.py
~~~

Example only with protected temporary files (DO NOT commit any real plan or customer evidence):

~~~bash
python3 scripts/review_high_risk_static.py \
  --case-id AZ-T45-03 \
  --observation /restricted/observed-plan-file-reference.json \
  --approved /restricted/separately-approved-digest.json
# exit 2 even on matching hash; independently verify the approval record
~~~

The \`--observation\` JSON for AZ-T45-03 references a real local file via \`plan_path\`. The file's SHA-256 is computed read-only; plan contents are never output. The helper limits that file to 100 MiB. Do not place real plans in a public GitHub Actions run.

## Acceptance and next DAG steps

1. **SC-01** — Freeze the 160 original ID/command/criterion identities and prioritization. This PR adds machine output and unit regressions; formal independent signoff remains OPEN.
2. **SC-02** — Review the five semantic traps with owners; use local comparison only for negative-path triage. No criterion is accepted on self-supplied data.
3. **SC-03** — For remaining 155, review source-to-criterion equivalence, immutable source/approved baseline, scope, identity and false-positive possibilities. The ranked file routes work; it is not 155 independently finished reviews.
4. **SC-04** — When real app source and approved Playwright internal/external runner are supplied, replace the nine browser journey blockers with real, independently approved tests (existing PR #8/#9).
5. **SC-05** — Independently review stacked PR chain #2 → #11. Hold release NO_GO until real scoped evidence, validated signed approvals and release authority.

**Unchanged inventory:** 1,716 canonical IDs; 858 synthetic; 858 odd review/observation procedures; 13 missing Playwright code references; 986 tracked script references; 717 no direct local script reference; 0 missing literal input references; independently accepted Azure cases 0; release NO_GO.
