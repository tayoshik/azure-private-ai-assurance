# Issue #30 — Historical GitHub Actions artifact review (restricted, local-only)

Prepared 2026-11-22. This procedure is not proof of historical artifact confidentiality. PR #29's reviewed upload snapshots protect future runs only. Prior artifacts might remain accessible under their historical permissions and cannot be reclassified as safe from source inspection alone.

## Verified baseline (metadata only)

Previous review sampled one pre-PR-#29 successful run for each of the 16 artifact-producing workflows. All 16 representative runs retained one artifact, and these 16 ZIPs totaled 206,884 compressed bytes, with expiry metadata showing 2026-12-06 UTC. Earlier workflow YAMLs had 13 broad uploads from artifacts/ and three narrower directory uploads. All 16 requested 14-day retention.

This was a sample, NOT a complete inventory or content review. Real ZIP contents, historical job logs, actual access/download history, global retention configuration, and anonymous/public accessibility remain unverified. Exposure status: UNKNOWN. Azure-live PASS remains 0/1,716; release NO_GO.

## Authorization and private workspace

Only an authorized operator may inspect actual artifacts. Use an approved WSL/Linux workstation and encrypted, restricted storage, never the public Git checkout, CI workspace, synced folder, issue comment, or cloud evidence store. Do not paste raw log data, ZIP contents, secret values, or complete private reports into GitHub.

For metadata-only enumeration, after approving the workstation and verifying an already authenticated GitHub CLI with read permission, the following is a WSL example:

    set -Eeuo pipefail
    umask 077
    PRIVATE="$HOME/.local/share/private-actions-history-review"
    mkdir -p "$PRIVATE/incoming" "$PRIVATE/reports"
    chmod 700 "$PRIVATE" "$PRIVATE/incoming" "$PRIVATE/reports"
    command -v gh >/dev/null
    gh api --paginate "repos/tayoshik/azure-private-ai-assurance/actions/artifacts?per_page=100" \
      --jq '.artifacts[] | {id, name, size_in_bytes, created_at, expires_at, expired, workflow_run}' \
      > "$PRIVATE/reports/all-artifacts.ndjson"
    chmod 600 "$PRIVATE/reports/all-artifacts.ndjson"

This GitHub API query collects the available repository artifact metadata across pages; it does not download ZIP payloads. Match each artifact's workflow_run ID to its workflow path and historical date against the 16 named producer workflows in specs/github-actions-artifact-policy.json. Include failed and cancelled runs that used if: always() uploads. Keep expired or deleted records as NOT_INSPECTED if unavailable. Names alone do not prove producer identity.

## Actual archive inspection — only after explicit security authorization

Select a reviewed artifact ID and approved workstation before downloading. The example below avoids extracting ZIP contents. It does not authenticate to Azure or modify GitHub artifacts.

    set -Eeuo pipefail
    umask 077
    ID="REPLACE_WITH_APPROVED_NUMERIC_ARTIFACT_ID"
    case "$ID" in ''|*[!0-9]*) echo 'Invalid artifact ID' >&2; exit 2;; esac
    PRIVATE="$HOME/.local/share/private-actions-history-review"
    gh api "repos/tayoshik/azure-private-ai-assurance/actions/artifacts/$ID/zip" \
      > "$PRIVATE/incoming/$ID.zip"
    chmod 600 "$PRIVATE/incoming/$ID.zip"
    python3 scripts/triage_historical_actions_archives.py \
      --archive-dir "$PRIVATE/incoming" \
      --report "$PRIVATE/reports/triage-$(date -u +%Y%m%dT%H%M%SZ).json"

Run the Python tool from a trusted checkout, not inside a downloaded archive. It needs no cloud credentials, Python third-party dependencies, or Azure CLI. The parser does not extract or execute members, makes no network requests, bounds ZIP size and decompression ratio, and flags known credential patterns, sensitive file extensions, duplicate/path-traversal/symlink entries and nested archives. It writes to a newly named 0600 report in a pre-existing private 0700 directory outside the repository. The console shows redacted indicator counts only. All archives remain MANUAL_REVIEW_REQUIRED even when the heuristic detects no secrets.

Run the synthetic-only tests with:

    python3 -m unittest discover -s tests -p 'test_historical_actions_archives.py' -v

## Mandatory human review and closure gate

1. A second authorized reviewer confirms the complete retained artifact inventory, producer/run mapping, expiry/deletion coverage, access configuration and log exposure. ZIP metadata/filenames alone are insufficient.
2. Inspect all flagged items and unrecognized content in an approved restricted environment. Signature scanning is NOT complete DLP and cannot rule out PII, embedded base64/encoded keys, unusual formats, historical job log leaks, or secrets in nested archives.
3. Record a restricted per-artifact decision with owner authorization, artifact/run ID, evidence digest, reviewer, UTC timestamp, assessed exposure, response actions and unresolved uncertainty. Put only redacted findings in the public issue.
4. If exposure is plausible, follow incident response and owner-approved containment and key rotation. Preserve legally required evidence; do not automatically delete historical artifacts.
5. Close Issue #30 only after full-scope content and access assessment and the separate Azure-live private evidence storage decision. Do not treat this tool, mock/CI PASS, or the metadata sample as proof of safety.

Never run az login, Terraform plan/apply, Azure mutations, or live acceptance commands as part of this historical ZIP review.


## Full available metadata reconciliation (run before any ZIP download)

The previous 16-artifact sample is not a complete retained inventory. Use two independently paginated GitHub REST collections in your **approved, access-restricted WSL ext4 filesystem**, using a GitHub CLI session that the owner has already authorized. Do not create or paste GitHub tokens into scripts. Ensure the CLI is authenticated and repository read access is authorized. The following commands are one paste; they do not download artifact bytes:

```bash
set -Eeuo pipefail
umask 077
cd "$HOME/azure-private-ai-assurance"  # trusted, up-to-date checkout
ROOT="$HOME/.local/share/private-actions-history-review"
mkdir -p "$ROOT" "$ROOT/reports"
chmod 700 "$ROOT" "$ROOT/reports"
command -v gh >/dev/null
gh auth status >/dev/null
gh api --paginate "repos/tayoshik/azure-private-ai-assurance/actions/artifacts?per_page=100" \
  --jq '.artifacts[] | {id, size_in_bytes, created_at, expires_at, expired, workflow_run} | @json' \
  > "$ROOT/artifacts.ndjson"
gh api --paginate "repos/tayoshik/azure-private-ai-assurance/actions/runs?per_page=100" \
  --jq '.workflow_runs[] | {id, path, head_sha, created_at, status, conclusion} | @json' \
  > "$ROOT/runs.ndjson"
chmod 600 "$ROOT/artifacts.ndjson" "$ROOT/runs.ndjson"
python3 scripts/reconcile_historical_actions_inventory.py \
  --artifacts "$ROOT/artifacts.ndjson" --runs "$ROOT/runs.ndjson" \
  --report "$ROOT/reports/metadata-$(date -u +%Y%m%dT%H%M%SZ).json"
```

The `@json` serialization produces one compact object per line for the strict NDJSON reader. The tool joins artifact workflow_run IDs to workflow run paths, compares each path to the **16 reviewed producer workflow file names**, and flags missing mappings or pre-guard source candidates. Classification after the 2026-11-22T12:24:44Z guard merge is **not a safe verdict**: a feature branch or rerun can use older workflow source. The private JSON contains artifact/run IDs for authorized follow-up; the console prints aggregate redacted counts only. The script will not overwrite existing results and requires private input files and a pre-existing private output directory.

**Evidence limits:** Listing accessible repository artifacts through the REST API does not recover permanently deleted or expired artifacts and cannot prove a complete historical inventory. An API result may also change while paginating. Re-run and reconcile counts in an approved review window. Confirm repository/account retention and historical artifact access independently. Never upload raw NDJSON or full per-artifact reports to a public PR or Issue.

```bash
python3 -m unittest discover -s tests -p 'test_historical_actions_metadata.py' -v
```

**Manual gate remains:** the reviewer must inspect actual historical ZIPs, job logs and exposure in approved restricted storage; metadata-only reconciliation cannot close Issue #30.
