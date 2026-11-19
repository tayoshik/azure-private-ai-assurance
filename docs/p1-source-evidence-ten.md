# P1 source-evidence correlation — third ten-case slice (review-only)

**Date:** 2026-11-19; **parent:** draft PR #13; **new draft:** PR #14.
**Trust boundary:** all observation and allegedly approved baseline data are untrusted local JSON. No authenticated Azure operation, DNS, browser or Terraform run is executed. A local match returns **REVIEW_REQUIRED, process exit 2**, never security PASS.

## Ten source-grounded P1 cases

| Original ID | Published source weakness | New offline comparator |
| --- | --- | --- |
| AZ-T35-13 | A query smoke report may claim Pass without principal, correct index or expected test data | Bind index, principal, runner, exact synthetic query/result IDs, managed identity, HTTP 200 and claimed private route |
| AZ-T40-13 | Deployment JSON with nonempty resource/result is not evidence of private runner, SCM PE or approved artifact | Bind source 40-hex commit, artifact SHA-256, approved SCM PE, runner, TLS/route and deployment identity |
| AZ-T41-11 | \`approved_route: true\` can refer to wrong datasource | Compare indexer, datasource, principal, hostname and approved private destination IP |
| AZ-T42-17 | \`raw_token_logged: false\` may cover no actual logs | Require three separate synthetic scan groups, nonzero scanned artifacts and positive controls, zero unmasked token findings |
| AZ-T43-17 | A \`Denied\` string may refer to wrong principal/container/operation | Bind negative-test principal, container, operation, request ID, 403 and audit correlation |
| AZ-T48-21 | \`secret_redaction: true\` may not cover prompts or personal data | Require prompt/credentials/personal_data control records with synthetic markers, positive-control detections and zero unmasked markers |
| AZ-T49-15 | \`status: Pass\` may hide wrong endpoints/public route | Require **all three** OpenAI/Search/Cosmos resource IDs, approved PE IPs, TLS, port 443 and claimed private routes |
| AZ-T50-19 | ACR pull \`runner_private: true\` may not match approved runner or image digest | Match runner CIDR, ACR PE, immutable source commit, exact artifact hash, claimed private route and no raw credential logging |
| AZ-T56-19 | \`collection_enabled: true\` does not demonstrate a correlated request | Require two or more distinct flow IDs with same synthetic request, approved private destination set, allowed source ranges and port 443 |
| AZ-T58-07 | \`approved_commit_sha == commit_sha\` can be self-asserted while plan used another commit | Compare original, approved and plan source commits, exact plan digest, scope, change ticket, reviewer distinct from release executor |

All case-specific helpers must require an input envelope including original case ID, resource ID, runner ID, immutable source SHA-256 and recent timestamp, with claimed baseline matching those fields and an approval-record digest reference. **These fields and a \`true\` flag are not verified provenance.** They are used solely for local discrepancy detection and cannot replace a signed independent review or actual runner trace.

### Local status contract

- Missing, malformed, stale, incomplete data: \`NOT_READY\`.
- Different resources/IP/digests/test results, denied condition absent: \`DIFFERENCE_REVIEW_REQUIRED\`.
- All *untrusted* expected fields match: \`REVIEW_REQUIRED\`.
- Any CLI invocation: **exit code 2**, **0 Azure live acceptance**, **release NO_GO**.

**Limits:** the synthetic scanner/positive-control fields, observed TLS, private-route and authorization status remain self-asserted. No actual logs are scanned and no real cryptographic signature is verified by this code. A real sound policy must require authenticated scoped records, independent validation of signers and approved identity, and an end-to-end negative/positive test in authorized execution environment. The file and metadata fields are not evidence of these operations.

### Review progress and independent acceptance

- Static source-priority queue: **160 candidates = P0 5 / P1 127 / P2 28**. None of the original catalogue IDs or published commands is changed by this PR.
- Optional offline P1 comparator coverage: **30 distinct original P1 cases** (PR #12 ten + PR #13 ten + PR #14 ten). **97 P1 cases** remain without these comparators; all 127 still require independent security review.
- Missing Playwright references: **13**, tracked script references: **986**, no direct local script reference: **717**, missing literal local inputs: **0**.
- Entire canonical catalogue **1,716 cases**; Azure live accepted **0/1,716**; release **NO_GO**.
- Stacked PRs #2 through #14 should remain unmerged drafts pending independent review.

### Reproduce without Azure access

~~~bash
python3 -m unittest discover -s tests -p 'test_p1_source_evidence.py' -v
python3 -m unittest discover -s tests -p 'test_p1_network_monitor.py' -v
python3 -m unittest discover -s tests -p 'test_p1_evidence_correlation.py' -v
python3 scripts/triage_static_criteria.py --summary
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py

# With private, owner-provided observation/approval JSON, always exit 2:
python3 scripts/review_p1_source_evidence.py \
  --case-id AZ-T42-17 \
  --observation /restricted/token-redaction-evidence.json \
  --approved /restricted/signed-approval-reference.json

python3 scripts/release_gate.py  # expected exit 2
~~~

Do not commit raw logs, tokens, customer data, Terraform plans or protected configuration to this public repository. Code and CI use nonproduction, in-memory synthetic inputs only.
