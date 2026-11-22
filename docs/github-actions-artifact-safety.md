# P7.4 — Offline CI artifacts: pre-upload staging, secret detection and 14-day retention

**Date:** 2026-11-22 · **Scope:** GitHub Actions source-only artifacts · **Azure acceptance:** 0/1,716 · **Release:** NO_GO.

## Verified source baseline

- Main at the start of this task contained **35** workflow YAMLs and **37** job IDs; **16** workflows uploaded Actions artifacts.
- All 16 uploaders already requested a `retention-days: 14` value, but many uploaded the entire mutable `artifacts/` directory and did not run a shared content review immediately before upload.
- An early failure could still reach an `if: always()` upload step, with no assertion that only intended, safely reviewable files were present.
- **Never assume historic artifacts are free from secrets:** these changes protect new runs only and do not retroactively inspect, redact or delete previously uploaded archives.

## Implemented fail-closed policy

`specs/github-actions-artifact-policy.json` is the reviewed, versioned inventory of exactly **16 producer workflows / 71 permitted relative file names**. All are offline JSON, text or logs; Terraform plan/state, tokens, Key Vault material, customer records, environment snapshots and real Azure operational evidence are not on the list.

`scripts/verify_offline_ci_artifacts.py` is a **stdlib-only, offline pre-upload scanner**. For the current workflow name it:

1. Loads the policy and rejects metadata drift, duplicate/unsorted paths, additional file types, absolute/traversal paths and unknown workflow IDs.
2. Walks `artifacts/`, denying **any unexpected file**, symlink, nonregular file, path exceeding the 8 MiB per-file or 16 MiB total limits, and invalid UTF-8.
3. Detects **high-confidence credential signatures** such as PEM private key headers, GitHub/AWS access keys, Authorization Basic/Bearer headers, JWTs, Azure Storage AccountKey/SAS signatures and sufficiently long credential-field values.
4. Only after **all** source files pass, copies their *reviewed exact bytes* to a freshly created sibling `artifacts-reviewed/` directory. It records the SHA-256 and byte count of each approved source but never prints file contents or credential values.
5. Returns nonzero on any safety failure; the staging folder is not created on an invalid input. The subsequent upload step only reads `artifacts-reviewed/` **when the scanner outcome is success**, and otherwise skips upload. This also works for `if: always()` diagnostics after upstream test failures.

All 16 producers set `id: artifact_safety`, run the scanner with `if: always()`, pin the official `actions/upload-artifact` commit, use `if: always() && steps.artifact_safety.outcome == 'success'`, set `if-no-files-found: ignore`, and retain a **14-day** expiration. If no artifact directory exists, nothing is staged or uploaded. The scanner and policy manifest are present in the producers' PR/main path filters, so future changes to either receive the producers' real CI checks before merge.

`scripts/audit_github_actions_quality.py` now audits all 35 YAMLs to ensure there are no uploaders outside the 16-file policy, each uploader is a single guarded step, the staging path is fixed, the allowlist scan runs even after failures, and retention remains exactly 14 days. A failure makes the offline `workflow-source-policy` CI fail. This **does not** make the optional path-filtered workflow a globally required Ruleset status context.

## Remaining limitations / security boundary

This is preventive protection, **not a complete DLP, antivirus, OCR or secret-scanning engine**, and not proof that any arbitrary confidential passage is absent. High-entropy secrets may appear in other formats. The user/reviewer must keep actual cloud logs, TLS keys, deployment plans, private-state files, configuration secrets and customer information outside these public artifacts. GitHub job logs are **not** intercepted or redacted by this tool. The stage is only a byte snapshot produced on the same runner; untrusted code running concurrently with the same runner permissions is outside the scanner's security guarantee.

A source scan, SHA-256 of local files, green mock CI and artifact retention policy are all **insufficient** to make Azure acceptance PASS. Only independent approved real Azure testing can change the immutable 1,716-case acceptance status or release decision. Neither `terraform plan`, `apply` nor `az login` is run by the scanner.

## Reproduction (credential-free)

```bash
set -Eeuo pipefail
python3 -m unittest discover -s tests -p 'test_offline_ci_artifacts.py' -v
python3 -m unittest discover -s tests -p 'test_github_actions_quality.py' -v
python3 scripts/audit_github_actions_quality.py --summary-only

# Only run this for an approved producer with offline JSON/TXT/log outputs.
# The script is intentionally stricter than simply archiving all output files:
python3 scripts/verify_offline_ci_artifacts.py \
  --workflow terraform-provider-schema-real.yml \
  --root artifacts \
  --stage artifacts-reviewed
```

Do **not** archive `artifacts/` directly. The reviewed snapshot is the only approved upload source. If the scanner blocks an artifact, fix the generating code or obtain a reviewed policy exception through PR; never turn its step into `continue-on-error`, use `if: always()` as the uploader condition alone, or silently enlarge file limits.

## Follow-up decision

The root of P7.4 is closed only after all 16 artifact producers and both mandatory GitHub Ruleset checks pass on PR and main. **Historical artifact exposure assessment**, centrally managed retention outside Actions (if mandated), and production Azure evidence storage remain separate tasks requiring their own scope, authorized environment and approvals.
