# P1 follow-on: network, identity, WAF, and monitoring evidence correlation (ten cases)

**Date:** 2026-11-19. **Parent:** Draft PR #12 on branch \`audit/p1-evidence-correlation-20261119\`. This is a source-linked, offline, read-only review aid, not live acceptance. New source-specific helper and tests are separate from the original catalogue commands.

## Ten original P1 review cases

| Test ID | Original check's semantic weakness | Added *local* cross-field discrepancy review |
| --- | --- | --- |
| AZ-T18-19 | A nonempty external network observation can be unrelated to effective configuration | Match exact target and deny rule, approved external probe CIDR, disabled public access, denied outcome, correlation ID |
| AZ-T19-19 | \`auth_success\` is self-reported | Match managed principal, audience and scope, require explicit no-token-logging and correlated smoke result |
| AZ-T41-09 | Nonempty DNS resolver and private addresses aren't a verified PE set | Match resolver, target hostname, canonical private A-address set and query ID |
| AZ-T42-21 | \`denied: true\` alone doesn't establish a controlled RBAC denial | Match unauthorized principal, operation, 403 status and audit correlation |
| AZ-T48-17 | A \`Pass\` DNS label can hide NXDOMAIN, timeout or wrong A records | Require OpenAI/Search/Cosmos names and exact approved private addresses, fail on NXDOMAIN/public or wrong IP |
| AZ-T49-17 | \`unapproved_public_egress: 0\` can describe an empty or unperformed check | Require at least two explicitly enumerated public targets, scoped source and a distinct denied flow-log correlation per record |
| AZ-T51-21 | Existence of \`changes\` and \`reviewer\` does not establish authorized WAF policy revision | Compare policy, revision, ticket, reviewer, rule IDs, exception set, and separate rollback revision |
| AZ-T55-21 | Gateway and backend log fields may not refer to the same request or resources | Match request ID, Gateway/backend resource IDs, observation times and claimed private route |
| AZ-T57-17 | Self-reported \`p95_minutes <= approved_p95_minutes\` can be fabricated | Recompute nearest-rank p95 from at least 20 explicit timestamp pairs and compare approved threshold |
| AZ-T57-21 | \`result: Pass\` and \`recipient\` do not establish synthetic alert delivery | Correlate alert rule, approved receiver, synthetic event ID, delivery acknowledgment, channel and delivery delay |

Each record is treated as **untrusted**: status flags, resource IDs, scoped caller, timestamps, plan/hash values and signed approvals are not validated against Azure. This script never calls an Azure API. User input does not establish a signer, independently authenticated runner, certificate chain or network path. Evidence can lie, and two matching locally supplied JSON files are still not trustworthy acceptance evidence.

## New code and tests

- \`scripts/review_p1_network_monitor.py\`: ten source-specific typed comparators; shares the existing strict envelope from PR #12, requires original case and scoped resource/runner/source SHA, claimed approval digest and recent UTC time.
- \`tests/test_p1_network_monitor.py\`: 16 regression methods with multiple subcases across the ten controls, wrong resources/principals, public or wrong private addresses, revoked proof assumptions, unsigned WAF exceptions, lost correlation, p95 misreporting, late alerts and malformed inputs.
- \`.github/workflows/p1-network-monitor.yml\`: no cloud secrets, browser, actual DNS or network calls; source-grounded 160-rank and 1,716-ledger checks, explicit NO_GO enforcement.
- All original frozen commands, source-catalogue SHA-256s, ledger ID counts and dependencies are unchanged.

### Output contract

| Result | Meaning | CLI exit |
| --- | --- | ---: |
| \`NOT_READY\` | Missing/invalid/stale data | 2 |
| \`DIFFERENCE_REVIEW_REQUIRED\` | Source-specific local typed mismatch or dangerous value | 2 |
| \`REVIEW_REQUIRED\` | Untrusted local observation and claimed baseline match in the modeled fields | 2 |

Even an all-match state does not prove a route, TLS identity, WAF enforcement, approved release or live Azure acceptance. **Do not promote an offline review result to \`PASS\`.**

## Review backlog

P1 review ranking initially contained **127** cases. PR #12 added local comparators for ten; this PR adds another ten **distinct** P1 cases. Thus **20 of 127 have optional, source-linked offline comparators**, **107 remain without these new comparators**. The twenty do **not** have independent semantic sign-off. The original priority distribution remains P0 5 / P1 127 / P2 28; the review ranking counts are not altered by adding helper files.

Playwright is still missing four configuration + nine journey source references (13 total). Dependency audit remains 1,716 canonical, 986 tracked script references, 717 without a direct script reference, 13 missing, zero narrow literal missing inputs. Verified Azure live passes: 0/1,716. Release decision: NO_GO.

## Safe local reproduction

~~~bash
python3 -m unittest discover -s tests -p 'test_p1_network_monitor.py' -v
python3 -m unittest discover -s tests -p 'test_p1_evidence_correlation.py' -v
python3 scripts/triage_static_criteria.py --summary
python3 scripts/build_test_automation_ledger.py --check
python3 scripts/audit_catalogue_dependencies.py

# With owner-provided restricted JSON, returns exit 2 even on local match:
python3 scripts/review_p1_network_monitor.py \
  --case-id AZ-T57-17 \
  --observation /restricted/monitor-observation.json \
  --baseline /restricted/monitor-approved-baseline.json

python3 scripts/release_gate.py  # exit 2, NO_GO
~~~

No real IPAM, tenant IDs, protected logs or authentic signatures are included in this public repository. Stacked PRs #2 through #13 remain draft and should only merge after independent review and source-integrity checks.
