# P1 WAF, SBOM, TLS, route-drift source-to-evidence review (fourth slice)

**Date:** 2026-11-19. **Base:** draft PR #14, no merge to main. **Scope:** source-grounded offline mismatch detection ONLY.

## Ten selected canonical P1 IDs

| ID | Original published command's gap | Additional local requirement |
|---|---|---|
| AZ-T50-13 | \`jq '.bomFormat or .spdxVersion'\` tests presence, not content-to-image binding | Read the real local SBOM bytes, compare an approved SHA-256, parse CycloneDX/SPDX, verify artifact digest and component count |
| AZ-T50-21 | \`denied: true\` is self-asserted | Bind untrusted image, policy, request and deny-rule reference, deny outcome and isolated-test flag |
| AZ-T51-13 | \`sha256sum benign-junit.xml\` prints hash but does not verify allowed traffic | Compare exact approved digest of JUnit file; parse expected case, no failures/skips, correlate claimed WAF Allowed and 2xx/approved redirects |
| AZ-T51-15 | \`sha256sum sqli-junit.xml\` does not prove rule enforcement | Parse JUnit and correlate claimed SQLi test to WAF Blocked, 403, approved request and rule |
| AZ-T51-17 | \`sha256sum xss-junit.xml\` does not prove XSS enforcement | Same as above for approved isolated XSS test |
| AZ-T53-17 | \`result: Pass\` plus fallback may refer to another certificate | Bind Gateway/secret/approved change, old/new version, actual rollback target and no private key disclosure claim |
| AZ-T54-19 | \`backend_503_count: 0\` can hide an empty test and missing alert | Require >=20 explicitly counted approved requests, no unexpected 503, backend health and correlated delivered incident-alert claim |
| AZ-T55-11 | \`san_verified: true\` can conceal the wrong hostname or disabled TLS validation | Require actual SAN list to include approved backend host, approved certificate digest, hostname/chain checks and no TLS bypass |
| AZ-T56-09 | \`blocked: true\` may describe an unapproved test or mere timeout | Check approved unauthorized-test CIDR, target PE, isolated request, explicit blocked outcome and deny-flow correlation |
| AZ-T56-21 | \`unapproved_changes: 0\` can be true even without drift injection | Require simulated route change, alert acknowledgment, rollback run ID and same exact pre/post route-set digest |

The source catalogue's published commands remain unchanged. New helper \`scripts/review_p1_waf_supplychain.py\` never runs them and does not call Azure, Terraform, Playwright, WAF, network or an authenticated approval service.

### Technical guardrails

- A matching local JSON observation and local baseline is **not independent provenance**. All observations, claimed approvals and \`true\` values remain untrusted. CLI **always exits 2**.
- \`safe_json_sbom\` opens only a small (<=1 MiB) local non-symlink file, hashes its exact bytes and parses standard CycloneDX/SPDX structures before comparing the image checksum recorded for the BOM's artifact. This does not validate a signed SBOM or an OCI registry identity.
- \`safe_xml_junit\` opens only a small (<=1 MiB) local non-symlink file, hashes its exact bytes, refuses DTD/entity declarations, parses JUnit suites, verifies declared test counts, rejects failures/errors/skips and confirms the expected case name. **JUnit passing cannot prove the associated WAF event happened**; the claimed WAF event and rule correlation also require externally authenticated telemetry.
- Reject wrong source case/resource/runner identifiers, changed SHA, stale observation, incomplete approval reference, missing XML, mismatched rule, public/incorrect network test values and unexpected outcomes.
- A synthetic test may reference a local path; do not upload real XML logs or protected test traffic to public CI.
- \`NOT_READY\`: missing/invalid/unparseable inputs. \`DIFFERENCE_REVIEW_REQUIRED\`: mismatched typed input. \`REVIEW_REQUIRED\`: local fields agree, but identity/signature/real runner and runtime semantics remain **unverified**.
- No result is a PASS, independent security signoff or GO.

## Review progress / no change to security acceptance

P1 source static queue is **127 cases**. Prior PR #12–14 added optional local comparators for 30 distinct cases; this PR adds 10 further distinct P1 source cases for **40/127 local comparator coverage**. The **87 remaining P1 source cases** have not received these additional per-case local comparators. **All 127** still await independent security review. P0 5 and P2 28 are likewise unchanged.

Source references: 986 tracked, 717 with no direct script path, 13 Playwright missing, 0 literal input missing across 1,716 canonical IDs. **Independently accepted Azure live: 0/1,716. Release: NO_GO.** PRs #2 onward are unmerged drafts.

### Offline reproduction

~~~bash
python3 -m unittest discover -s tests -p 'test_p1_waf_supplychain.py' -v
python3 -m unittest discover -s tests -p 'test_p1_source_evidence.py' -v
python3 scripts/triage_static_criteria.py --summary
python3 scripts/audit_catalogue_dependencies.py
python3 scripts/release_gate.py  # expected exit 2
~~~

All CI examples use synthetic in-memory data and temporary JUnit/SBOM files. Never copy live evidence to a public GitHub workflow or treat a test XML's "success" attribute as signed WAF proof.
