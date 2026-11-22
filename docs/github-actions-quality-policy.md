# P7 — GitHub Actions cross-workflow quality and status-check governance

**Date:** 2026-11-22. **Scope:** GitHub Actions source/workflow controls only; no Azure authentication, live environment, Terraform plan/apply or customer data.

## Verified baseline and original weaknesses

The repository contained **34** workflows and **36** job definitions on the original main snapshot. GitHub Ruleset `main-protected-offline` (ID `27836039`) is **active** and requires precisely `offline-main-gate` and `offline-catalogue` from GitHub Actions; neither workflow was path-filtered. Those check contexts must retain their exact names.

Two optional status names were **ambiguous across separate workflows**:
- `offline-contracts` was used by Terraform Stage 3 **and** Stage 6.
- `offline` was used by Terraform Stage 5 **and** Azure Monitor private-link.

Different jobs reporting the same context on a single SHA can confuse a reviewer or required-check enforcement. Source files also mixed mutable version-tag checkout references and two optional workflows were unnecessarily triggered on both feature-branch push and PR events.

## Changes in this PR

| Topic | Before | After |
| --- | --- | --- |
| `offline-main-gate` | `actions/checkout@v4`, credentials retention not explicit, default long timeout | Full SHA pinned `checkout`, `persist-credentials: false`, 20-min max. **Job name and commands unchanged** |
| `offline-catalogue` | `actions/checkout@v4`, credentials retention not explicit | Full SHA pinned `checkout`, `persist-credentials: false`. **Job name and commands unchanged** |
| Terraform Stage 3 | `offline-contracts` | `stage3-identity-vault-contracts` |
| Terraform Stage 6 | `offline-contracts` | `stage6-gateway-contracts` |
| Terraform Stage 5 | `offline` | `stage5-webapp-contracts` |
| Azure Monitor private-link | `offline` | `monitor-private-link-offline` |
| Four scoped workflows | Feature pushes could repeat PR checks, and several PR path filters did not match push coverage | `push` limited to main, corresponding `pull_request` coverage aligned; Monitor PR coverage added |
| Future workflow edits | No cross-file check-name uniqueness enforcement | `workflow-source-policy` verifies 35 workflow definitions and 37 globally unique job contexts |

The four scoped workflows use exact, symmetric path filters to ensure a PR is tested before merge and its final main commit can be tested after merge. This is *not* applied indiscriminately to unrelated workflows; the audit reports those remaining with feature-branch push triggers.

## New cross-workflow assurance contract

`scripts/audit_github_actions_quality.py` scans source YAML **without executing it**. It refuses:
- Missing/duplicated job context names; missing workflow inventory; privileged `pull_request_target`/`workflow_run` events; missing read-only `contents: read` or write-level content permissions.
- Renamed, gated, path-filtered or absent required `offline-main-gate` and `offline-catalogue`, altered mandatory package/catalogue commands, ignored command errors, mutable checkout tags or retained checkout credentials.
- Missing PR coverage, unbounded feature push, inconsistent push/PR path filters or absent self-trigger in the four scoped workflows.
- Silent removal of dispatch-only `terraform-stage4-provider-validate.yml` gate's manual-only status.

These checks target the **source structure**, not a full YAML schema, remote GitHub branch/ruleset API, runner behavior, or Azure acceptance. External branch protection must continue to be inspected independently through the GitHub Settings API. Paths used by optional workflows must **not** be made globally required in the current Ruleset, because many optional jobs correctly skip unrelated PRs.

`tests/test_github_actions_quality.py` implements **19** positive/negative and mutation cases. The new `.github/workflows/github-actions-quality.yml` uploads a JSON-only source-policy audit for 14 days, with no credentials and no Azure observations.

## Reproducible commands (no Azure)

```bash
set -Eeuo pipefail
python3 scripts/audit_github_actions_quality.py --out /tmp/github-actions-source-policy.json
python3 -m unittest discover -s tests -p 'test_github_actions_quality.py' -v
python3 -m unittest discover -s tests -v

# This expected NO_GO mode deliberately refuses release:
rc=0
python3 scripts/audit_github_actions_quality.py --summary-only --strict > /tmp/workflow-strict.json || rc=$?
test "$rc" -eq 2
```

GitHub-side verification of the actual source checks:
- `Settings` → `Rulesets` → `main-protected-offline` still lists `offline-main-gate` and `offline-catalogue` as required.
- GitHub Actions PR checks and main post-merge checks must pass before closing P7 source work.
- If an eligible PR lacks a required job, it is a blocker. Never paper over it with a success stub or skip.

## Remaining nonblocking quality backlog

- Some other workflows still use mutable checkout/action tags. The audit **reports their filenames** under `remaining_unpinned_action_workflows`; review provider/action compatibility before pinning them all, rather than changing versions blindly.
- Some unrelated path-scoped workflows still run on both feature push and PR. The audit reports them in `remaining_unscoped_push_workflows`; each should be migrated to PR + main push only **after** verifying complete PR coverage and any intentional feature-push-only use.
- Artifact policies differ in older workflows; future hardening should specify evidence class, retention, and confidential-data exclusion before unifying archives.
- No Actions test produces independent deployment, network isolation, permission, health or release acceptance evidence. **1,716 canonical tests remain NOT_READY, Azure live accepted 0, release NO_GO**.

**Exit criterion for this bounded P7 slice:** Required contexts remain stable and credential-free, the four duplicate optional contexts are unique, 35/37 workflow inventory is verified, 19 regressions and all required PR/main CI checks pass. Source-only quality improvement must not be misreported as live Azure security validation.
