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

- **Closed by P7.2:** the previously reported 13 workflows with mutable Action tags now use repository-reviewed full SHA references; `remaining_unpinned_action_workflows` is required to be **empty** by CI. The full list and GitHub tag-reference provenance are fixed in `specs/github-actions-approved-pins.json`.
- **Closed by P7.3:** all 34 automated workflows now have `push.branches: [main]` and retain `pull_request` coverage. The remaining manual-only provider workflow is intentionally `workflow_dispatch` only. The source audit now requires `remaining_unscoped_push_workflows=[]`.
- Artifact policies differ in older workflows; future hardening should specify evidence class, retention, and confidential-data exclusion before unifying archives.
- No Actions test produces independent deployment, network isolation, permission, health or release acceptance evidence. **1,716 canonical tests remain NOT_READY, Azure live accepted 0, release NO_GO**.

**Exit criterion for this bounded P7 slice:** Required contexts remain stable and credential-free, the four duplicate optional contexts are unique, 35/37 workflow inventory is verified, 19 regressions and all required PR/main CI checks pass. Source-only quality improvement must not be misreported as live Azure security validation.


## P7.2 — Approved full-SHA Action pins (2026-11-22)

Follow-up to Issue #26. The 13 outstanding workflow files have been updated, **without changing the underlying Terraform CLI version or the setup-terraform v3 major series**. Every `actions/checkout` step now includes `persist-credentials: false`. This includes three independent checkout steps in the provider-schema workflow.

| Action | Reviewed immutable commit | Upstream tag reference inspected |
| --- | --- | --- |
| `actions/checkout` | `93cb6efe18208431cddfb8368fd83d5badbf9bfd` | `v5.0.1` |
| `actions/setup-python` | `a26af69be951a213d495a4c3e4e4022e16d87065` | `v5` and `v5.6.0`, same commit |
| `actions/upload-artifact` | `ea165f8d65b6e75b540449e92b4886f43607fa02` | `v4.6.2` |
| `hashicorp/setup-terraform` (v3) | `b9cd54a3c349d3f38e8881555d616ced269862dd` | `v3` (major alias at inspection date) |
| `hashicorp/setup-terraform` (v4) | `dfe3c3f87815947d99a8997f908cb6525fc44e9e` | `v4.0.1`, already used elsewhere |

**Verification method:** queried each repository's official GitHub REST `git/ref/tags/<tag>` endpoint on 2026-11-22; the `object.type=commit` and `object.sha` values identify the exact version. A SHA is an immutable Git content reference and prevents future movement of a major tag from silently changing the runner's action. It is **not** a code signature, SBOM, vulnerability scan or proof that the publisher remains uncompromised.

The audit now uses a **fail-closed, reviewed SHA allowlist** plus the versioned JSON provenance manifest, rather than treating future tag references merely as advisory warnings. It rejects missing or altered pin manifests, unknown Action refs, mutable tags, and any checkout step that does not explicitly disable persisted credentials. Eight further adversarial unit tests were added, bringing the total workflow-policy regression tests to **27**. For any legitimate future Action upgrade, update the audited source, allowlist, manifest and tests together through a PR with all existing offline CI and relevant provider jobs green.

**Validation commands:**

```bash
python3 scripts/audit_github_actions_quality.py --summary-only
python3 -m unittest discover -s tests -p 'test_github_actions_quality.py' -v
python3 -m unittest discover -s tests -v
```

The Ruleset's only globally required contexts remain `offline-main-gate` and `offline-catalogue`. Paths and credentials for actual Azure deployment are unchanged. Issue #26 remains OPEN for the 27 other workflows with feature-branch push triggers and evidence-retention standardization. All 1,716 original Azure cases remain NOT_READY; accepted live Azure evidence **0**, release **NO_GO**.


## P7.3 — Eliminate redundant feature-branch pushes without narrowing PR coverage

**Date:** 2026-11-22. **Scope:** GitHub Actions event triggers, source policy and tests; no change to the required Ruleset contexts, Terraform code, canonical tests or Azure acceptance.

### Audited before/after

| Dimension | Before | After |
| --- | ---: | ---: |
| Automated workflows with an unrestricted feature-branch `push` | 27 | **0** |
| Automated workflows whose push is limited to `main` | 7 | **34** |
| Manual-only provider workflow | 1 | **1 (unchanged)** |
| All workflows / job contexts | 35 / 37 | **35 / 37** |
| Globally required Ruleset checks | `offline-main-gate`, `offline-catalogue` | **Unchanged** |
| Workflow source-policy regression tests | 27 | **35** |

Every previously unscoped `push` event received `branches: [main]`. The original `pull_request` event remains; existing path filters are retained or broadened. In particular:

- **9** workflows previously ran on **every PR**, even when their main-push event was path-filtered. Their PR events intentionally remain unfiltered. Narrowing those PRs would remove already-working validation coverage and is now rejected by the source-policy audit.
- `english-catalogue-validation.yml` and `terraform-stage4-ai-data-static.yml` had PR filters narrower than the corresponding push filters. Their PR filters were **expanded** to include the push paths and their own workflow YAML. This makes subsequent workflow edits reviewable by their respective checks.
- Other filtered workflows retain the existing symmetric push/PR path sets. A changed YAML file is included in both filters, so the workflow can test its own modifications before merging.
- `offline-main-gate` and `offline-catalogue` still run on **every PR** and every push to main. `terraform-stage4-provider-validate.yml` retains intentional manual-only operation; no live Azure access or `terraform apply` was enabled.

**Why this avoids duplication:** previously, committing to a feature branch could trigger its workflow's `push` *and* `pull_request` for the same code. Now that feature-branch push cannot fire the path-scoped duplicate; PR verification still fires and the merged main commit receives a single main-push run when its paths match. The number of jobs on a given PR can remain high because distinct controls intentionally validate overlapping source paths; this change only removes the redundant event type, not separate controls.

### Fail-closed policy

`scripts/audit_github_actions_quality.py` now rejects any non-`main` push filter, any automated push workflow without PR coverage, any filtered PR whose path set differs from its corresponding main-push filter, or a filtered workflow that cannot trigger on its own YAML. It also maintains an explicit list of the nine historically unfiltered PR workflows and refuses to narrow them without an independently reviewed policy change. Eight new mutation tests in `tests/test_github_actions_quality.py` exercise this contract.

```bash
python3 scripts/audit_github_actions_quality.py --summary-only
python3 -m unittest discover -s tests -p 'test_github_actions_quality.py' -v
python3 -m unittest discover -s tests -v
```

A passing source audit demonstrates a **configured event-routing policy**, not billing reduction, full GitHub Actions runtime semantics, independent security review, Azure connectivity or Azure acceptance. The remaining part of Issue #26 is **standardizing artifact retention, safe outputs and confidentiality**, not trigger normalization. Existing synthetic tests and **1,716 original acceptance records remain unchanged**, Azure live passes **0**, release **NO_GO**.
