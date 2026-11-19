# P1 evidence self-report: ten prioritized source-grounded offline comparisons

**Date:** 2026-11-19. **Branch:** audit/p1-evidence-correlation-20261119. **Parent:** draft PR #11.

## Summary

The PR #11 machine ranking identified **127 P1 static-check cases**, including **86** classified as evidence-file-reference cases. Many original published commands simply run \`jq -e\` on status fields or check for nonempty fields. The existence of a local document — even one claiming \`approved: true\`, \`result: Pass\`, or \`verified: true\` — cannot authenticate its source, prove the route taken by a request, validate the approval authority or establish the underlying security requirement.

This slice selects ten specific **published P1** IDs for control-specific **offline negative-path triage**, instead of globally rewriting the canonical catalogue or publishing synthetic "live evidence." The source IDs, published English command strings and criteria remain immutable in PR #11's 160-case queue.

| Case ID | Requirement | Defect in literal published command | New local cross-check |
| --- | --- | --- | --- |
| AZ-T19-03 | Internal runner private IP | A nonempty \`private_ip\` may be unrelated to the runner's approved CIDR | Parse IP and compare with approved runner network |
| AZ-T39-19 | App Service SCM private deployment | \`approved: true\` does not prove the runner's source, SCM PE destination or TLS | Match source/PE IPs, SCM hostname, TLS and execution result |
| AZ-T43-15 | Cosmos SDK with managed identity | \`auth: managed_identity\` and \`Pass\` can be self-asserted for another principal/container | Match approved principal and container; reject account-key use |
| AZ-T48-19 | OpenAI/Search/Cosmos connectivity | Three \`Pass\` fields can ignore wrong resources or public routes | Require all three named resource IDs, principal and private-route fields |
| AZ-T50-15 | OCI image signature | \`verified: true\` is not cryptographic verification or trusted signing provenance | Match artifact SHA-256 and trusted signer reference; flag unsigned claim |
| AZ-T50-17 | Critical/high vulnerabilities | \`critical: 0\` and \`high_waivers_approved: true\` omit scan identity and waiver-by-finding linkage | Match artifact digest, require zero critical and individually allowed high IDs |
| AZ-T51-19 | WAF enforcement | Nonempty \`action\` may be \`Matched\`, not \`Blocked\` | Match transaction/request/rule, require Blocked action and denial response |
| AZ-T53-09 | TLS certificate SAN | \`san_verified: true\` does not show approved hostname is in SAN or a trusted chain exists | Compare hostname with SAN, require chain and hostname validation assertions |
| AZ-T55-15 | Gateway to private WebApp PE | \`port: 443\` and \`Pass\` can describe a public endpoint or wrong Gateway | Compare source CIDRs, approved destination PE IP, resource ID and TLS field |
| AZ-T58-09 | Independent plan review | Two unique names may include the author, executor or approvals of different plans | Verify two distinct roles/identities, exclude author/executor and match exact plan digest |

### Input contract

\`scripts/review_p1_evidence_correlation.py\` reads *untrusted* local JSON only. Each observation has \`metadata\` with \`case_id\`, \`resource_id\`, \`runner_id\`, \`source_sha256\`, \`observed_at_utc\`, and an \`observation\` object. Each independently *claimed* approved baseline has \`metadata\` matching those source/scope keys plus an \`approval_record_sha256\`, and an \`expected\` object with case-specific fields.

A valid SHA-256 string is a typed reference, **not** a verified signature. The file does not confirm that observed or approved JSON was signed by any trusted authority; observed time and runner IDs are still **self-asserted**. The checker rejects stale (older than seven days) or future-dated (over five minutes) local observations, but its UTC/date check does not independently establish the clock or data collection time.

The checker prints only case ID, a controlled result/reason code, explicit unverified flags, \`azure_live_passes: 0\` and \`release_decision: NO_GO\`. It does not echo JSON, plan bytes, identity tokens or Azure resource identifiers. Local files are size-limited and are never uploaded as CI artifacts.

### Output state

| Outcome | Meaning | Exit code |
| --- | --- | ---: |
| \`NOT_READY\` | Missing, invalid, oversize, stale or unparseable data | 2 |
| \`DIFFERENCE_REVIEW_REQUIRED\` | Typed, scoped input values disagree or reveal a dangerous discrepancy | 2 |
| \`REVIEW_REQUIRED\` | Local values agree, but external provenance/signature and semantics were **not** established | 2 |

No outcome is Azure PASS, READY, GO, independently certified, or safe to deploy. A \`REVIEW_REQUIRED\` result cannot override the release gate and is not a self-contained authorization to run production or nonproduction tests.

### Safe reproduction (restricted synthetic/approved workspace)

~~~bash
python3 -m unittest discover -s tests -p 'test_p1_evidence_correlation.py' -v
python3 scripts/triage_static_criteria.py --summary
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py
python3 scripts/review_p1_evidence_correlation.py \
  --case-id AZ-T51-19 \
  --observation /restricted/evidence-waf.json \
  --baseline /restricted/approved-waf.json
# Exit code 2, even if all local values match.
python3 scripts/release_gate.py # expected exit 2, NO_GO
~~~

All workflow tests use **synthetic Python in-memory dictionaries**. Do not commit sample actual customer, authentication, IPAM, protected Terraform plan, private runner or production evidence to this public repo.

## Exact review backlog after this slice

- 10/127 P1 cases now have **control-specific offline mismatch/absence comparators**; 117 remaining P1 cases have not received comparators through this PR. No independent semantic signoff has been performed on the ten comparators.
- Five P0 source-trap helpers from PR #11 still require external review; 28 P2 cases also remain on the review queue.
- The existing 13 Playwright source references are still unresolved; no fake \`.ts\` file added.
- **1,716** catalogue IDs; 986 tracked direct script references, 717 cases with no direct script reference, 13 missing direct script references, **0** missing literal input references.
- Azure independently accepted live results remain **0/1,716**, release **NO_GO**.
- Draft PR #2→#12 review/merge backlog continues. Do not merge stacked drafts without independent code review.

The new predicates are *illustrative source-specific local triage*, not a substitute for deep security proofs. Actual acceptance will require separately authorized scoped collection from real resources, authentic signer/runner identity, verified trust roots, two independent reviewers and release authority.
