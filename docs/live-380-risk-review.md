# L1 — 380 Azure/private-runner live-route hazard preflight (source-only)

**2026-11-22. No Azure environment, credentials, private runner or approved live test target is available to this audit.** This reviewer queue is not an execution plan. It is separate from the **858 offline synthetic** candidates, **464 local-appearing approved-input review** candidates, **13 unapproved R41 browser-to-REST scope decisions**, and **1 odd self-test semantic exception**.

## Why the 380 source definitions need a second pass

`scripts/build_execution_route_1716.py` assigns exactly 380 of the 1,716 frozen canonical IDs to `AZURE_OR_PRIVATE_RUNNER_REQUIRED` on original direct-command prefixes. That is a useful environment hint, **not safe-to-run certification**. The new `scripts/review_live_380_preflight.py` cross-checks each source's exact ID/command/expected SHA-256 fingerprint with that routing inventory and emits a **redacted per-ID hazard and owner-evidence queue**. It never executes any original command.

| Review priority | Exact count | Control and next approval |
| --- | ---: | --- |
| P0 active WAF test traffic (`AZ-T69-05/07/09`) | 3 | Do not send SQLi/XSS/benign probe vectors without signed target, rate, payload, operator and time-window authorization, plus an independent security review |
| P0 Terraform `plan` state and lock | 11 | Require approved private backend, OIDC, provider pins, state access, refresh/locking, drift expectation, and encrypted plan custody; **not offline syntax-only** |
| P0 external recursive DNS resolver (`AZ-T18-05`) | 1 | Require an approved external test vantage, destination resolver and query disclosure review before contacting literal `@1.1.1.1` |
| P1 Azure CLI command/identity/scope review | 321 | Approve each `az` subcommand, quoted expression, resource/tenant scope and evidence predicate; some data/output may be sensitive and `--auth-mode login` is **not** permission to run interactive `az login` |
| P1 HTTP observation | 8 | Verify exact host, HTTP method, source, DNS/TLS and no-proxy behavior; HTTP status is not evidence of network isolation |
| P1 TLS peer observation | 3 | Verify real peer hostname/certificate chain/expiry and network vantage |
| P1 DNS resolution | 33 | Verify scoped resolver, CNAME/A chain and approved private endpoint NIC correlation; a DNS response is not proof of authorized connectivity |
| **Total** | **380** | **No original commands executed and zero approved live passes** |

By original command head, the 380 cases are **321 `az`**, **33 `dig`**, **11 `curl`**, **11 `terraform`**, **3 `openssl`**, **1 `getent`**. All **9 legacy Phase 6 `npx playwright` cases** are in the separate R41 proposal lane, not silently included in this queue.

The P0/P1 labels specify **review ordering, not tested safety or implementation coverage**. Other command classes can also contain unreviewed risks. Shell and variable expansion parsing is never used to authorize execution. All source commands are untrusted input data and must be separately reviewed before a protected, owner-approved run.

## Already completed versus outstanding

Completed source-only: deterministic 380 case membership, exact frozen fingerprints, review group count checks, hazard examples, negative mutations (unapproved WAF, Terraform apply, unscoped literal external DNS, HTTP method, missing quote), CI unit tests and expected strict exit 2.

**Still required from authorized owners**: G07 nonproduction scope; B05 private runner/backend; explicit federated identity and RBAC; versioned target IDs/approved DNS/route/PE NICs; WAF test ticket and short, bounded authorization window; negative expectations; encrypted evidence custody; signed independent review. Do not use a public GitHub Actions runner for these private/cloud tests. WSL on a fixed endpoint with no permitted `az login` remains unsuitable for live evidence collection.

In particular, `terraform plan -refresh-only` is not equivalent to an offline lint, `dig` may generate an external query, and a WAF probe changes operational traffic. No `az`, `terraform plan/apply`, `curl`, `dig`, `openssl` or `getent` frozen command should be started by source-review CI.

## Offline-only reproduction (reviewed local checkout)

```bash
set -Eeuo pipefail
umask 077
cd "$HOME/azure-private-ai-assurance"
OUT="$(mktemp -d "$HOME/live-preflight-380-XXXXXXXX")"
chmod 700 "$OUT"
python3 scripts/review_live_380_preflight.py --out "$OUT/live-380-review.json"
python3 -m unittest discover -s tests -p 'test_live_380_preflight.py' -v
rc=0
python3 scripts/review_live_380_preflight.py --summary-only --strict > "$OUT/strict.json" || rc=$?
test "$rc" -eq 2
```

The JSON file contains only metadata (case ID, existing source fingerprint, route family, category, evidence checklist and false approval fields): no original command bytes, tokens, IPs, private test payloads, state files or customer material. Do not copy real Azure evidence to a public issue, pull request or GitHub Actions artifact.

This L1 review does **not** change the six published canonical test files, test counts, missing Playwright references or owner decisions. **Azure accepted live PASS = 0/1,716; all 1,716 still NOT_READY; release NO_GO.** Historical GitHub Actions artifacts (Issue #30) remain a separate restricted reviewer task.
