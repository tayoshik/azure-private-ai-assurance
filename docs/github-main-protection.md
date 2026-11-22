# P0 — Protect `main` and require offline CI

**Prepared:** 2026-11-22. **Repository:** `tayoshik/azure-private-ai-assurance` (public).
**Scope:** GitHub source control only. No Azure subscription, OIDC, Terraform `plan`/`apply`, live acceptance, or production authorization.

## Current evidence and limitation

- `main` at preparation: `387b9463ea910ebfe665c5be554f630284a81ddf`.
- GitHub branch metadata: `protected: false`.
- Repository rulesets API: empty list.
- The GitHub integration used to prepare this change **cannot write repository rulesets or branch protection**; an authorized repository administrator must activate the policy in GitHub Settings.
- On the pinned initial main, the existing offline validation job is named `check`, which is too generic to rely on as a long-term required-check context. This PR renames its job to `offline-main-gate` without changing its test commands.

## Change applied by this PR

The always-triggered `.github/workflows/offline-validation.yml` job becomes **`offline-main-gate`**. It still runs:
1. `python3 scripts/validate_package.py`
2. `python3 -m unittest discover -s tests -v`

The already-existing `.github/workflows/publication-integrity.yml` always runs on pull requests, with job **`offline-catalogue`**:
1. `python3 scripts/verify_publication.py`
2. `python3 -m unittest discover -s tests -p 'test_publication*.py' -v`

Both are credential-free and Azure-offline. Do **not** configure either job as required until the new names have run successfully on this PR / on the merged main, to avoid a permanently pending required check. Other workflows use path filters and should **not** be made globally required until their trigger configuration is changed.

## Administrator activation: repository ruleset

1. Open `tayoshik/azure-private-ai-assurance` → **Settings**. In the current GitHub UI, look under **Code, planning, and automation** for **Rulesets** → **Rulesets**; in the alternate/older sidebar, use **Code and automation** → **Rules** → **Rulesets**. Then click **New ruleset** → **New branch ruleset**. If the menu is hidden, open the repository Rulesets settings directly: `https://github.com/tayoshik/azure-private-ai-assurance/settings/rules`. GitHub documentation: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository .
2. Name `main-protected-offline`. Select **Active** enforcement and target **the exact `main` branch**.
3. Enable **Require a pull request before merging**, **Require status checks to pass before merging**, **Require conversation resolution before merging**, **Block force pushes**, and **Restrict deletions** (labels can vary slightly).
4. Add two exact required checks, preferably with source **GitHub Actions**:
   - `offline-main-gate`
   - `offline-catalogue`
5. Enable the requirement that the PR branch be up to date with main before merge if practical. Avoid a required check whose workflow is path-filtered or job name is duplicated.
6. **Approvals:** If an independent reviewer with write access is available, set at least **1 approving review** and dismiss stale approvals on code changes. Increase to **2** only once two independent reviewers are available. GitHub does not allow a PR author to approve their own PR; on a one-person repository an enforced one-review setting can block all merges. Until a reviewer is added, temporarily require PR + the two CI checks, and record independent review as **OPEN**, not accomplished.
7. Keep the bypass list empty for normal development. Any exceptional break-glass bypass must be separately documented and auditable. Do not enable force pushes/deletions for convenience.
8. Do not enable **Require linear history**: the existing history uses merge commits.
9. Save the ruleset. If an organization-level ruleset already applies, reconcile it rather than creating conflicting requirements.

## Verification and evidence

- On a new throwaway branch, open a documentation-only PR to `main`.
- Verify that an untested or failing PR is blocked, and that both `offline-main-gate` and `offline-catalogue` complete successfully before the Merge button becomes available.
- Verify a direct push to protected `main` is rejected. Do not attempt a force push or deletion against `main`; confirm the settings instead.
- Record ruleset name/ID, selected branch, enforcement, required checks/source, review threshold, bypass list, operator, time (UTC), and test PR link in a restricted review log. Keep secrets and personal access tokens out of Git.
- Verify GitHub API/ruleset UI reflects the expected active rule after activation. `protected` metadata alone is not sufficient to prove the full policy details.

**Completion criteria:** the administrator confirms an active ruleset applying to `main`, both exact checks are required and have passed in an example PR, PR-only merging is enforced, and deletion/force-push bypass cannot occur in normal operation.

**If blocked:** record `P0_BRANCH_PROTECTION_NOT_ACTIVE`, keep the source PR and offline CI, and continue with ranking #2 without claiming this issue CLOSED.

**Safety:** This change does not alter release gate `NO_GO` or the canonical 1,716 test IDs. All Azure live tests remain `NOT_READY`.
