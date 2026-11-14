# Terraform Q01–Q02 — Integrated Offline QA and Fail-Closed Plan Review

**Project:** Azure Private AI Assurance  
**Scope:** existing 61 `.tf` files (Bootstrap through GW01–GW05), six inherited contract checkers, and new Q01/Q02 regression controls.  
**Azure acceptance:** 0/1,716 live passes; **NO-GO**. No Terraform command has been executed against Azure by these scripts.

## 1. Execution boundaries

| Location | Allowed | Prohibited / requires separate approval |
|---|---|---|
| Corporate WSL2 workstation | Git checkout, Python offline source/fixture checks, optionally `terraform fmt -check` when installed | `az login`, cloud `plan`/`apply`, WAF testing |
| Pinned, approved isolated CI | Terraform fmt; provider initialization from **approved mirror** with `-backend=false`; `validate` after lockfile review | Unreviewed provider download, deployment, state mutation |
| Federated, authorized nonproduction CI | Remote state connectivity, approved saved plan, restricted plan JSON, Q02 review and two human approvals | Automatic `apply`, printing state/plan/credentials in public logs |

**Do not put `terraform.tfstate`, `.tfplan`, `terraform show -json` output, environment-scoped baselines, certificates, or credentials in this public repository.** A plan JSON often includes sensitive configuration and identifiers.

## 2. Q01: reproducible offline check (safe WSL one-paste)

```bash
set -Eeuo pipefail
REPO="$HOME/azure-private-ai-assurance"
if [[ ! -d "$REPO/.git" ]]; then
  git clone https://github.com/tayoshik/azure-private-ai-assurance.git "$REPO"
fi
cd "$REPO"
git pull --ff-only
python3 scripts/terraform_q01_integrated.py
python3 scripts/terraform_q02_plan_guard.py --selftest --scope dev
python3 scripts/terraform_q02_plan_guard.py --selftest --scope bootstrap
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v
```

- `Q01.status = PASS_OFFLINE_CONTRACT_ONLY` means all six predecessor checkers reported zero errors. It checks **source text contracts**, not the actual HCL language schema or Azure state.
- `Q02.status = PASS_OFFLINE_FIXTURES_ONLY` means synthetic good/unsafe/missing plans classify correctly. It is **not** evidence of a valid Azure deployment.
- Exit `0`: offline check succeeds; nonzero: investigate the cited check. Never override a failed gate to make CI green.
- These commands do not need the W01–W05 ZIP copied into WSL: the GitHub working tree contains the current source.

## 3. Q01: true Terraform fmt and provider validate (separate gate)

Run only with an **approved Terraform CLI**, provider version, checksum-verified package source and committed `.terraform.lock.hcl` in the permitted build environment:

```bash
set -Eeuo pipefail
cd "$HOME/azure-private-ai-assurance"
terraform version
terraform fmt -check -recursive infra
# Requires allowed provider mirror/cache, an audited .terraform.lock.hcl,
# and a runner allowed to acquire the pinned provider binary.
terraform -chdir=infra/environments/dev init -backend=false -input=false -lockfile=readonly
terraform -chdir=infra/environments/dev validate -no-color
```

`-backend=false` avoids remote state login but does **not** prevent provider downloads. `-lockfile=readonly` deliberately fails when the lockfile has not been generated and reviewed. The current publication does not include a verified lockfile and this gate is `NOT_READY`. Do not claim that the earlier Python tests constitute `terraform validate`.

## 4. Q02: read-only Terraform plan policy audit (approved nonprod CI only)

Preconditions: approved G07 inventory; B05 private state path; federated runner; approved Terraform and provider versions; signed expected resource inventory; exact reviewed source commit; permitted private data storage; two reviewers.

```bash
set -Eeuo pipefail
umask 077
: "${SECURE_EVIDENCE_DIR:?set restricted private evidence path}"
mkdir -p "$SECURE_EVIDENCE_DIR"
# The next two commands run ONLY in approved federated CI; never on WSL.
# terraform -chdir=infra/environments/dev plan -input=false -out="$SECURE_EVIDENCE_DIR/approved.tfplan"
# terraform -chdir=infra/environments/dev show -json "$SECURE_EVIDENCE_DIR/approved.tfplan" > "$SECURE_EVIDENCE_DIR/plan.json"
python3 scripts/terraform_q02_plan_guard.py \
  --scope dev --plan "$SECURE_EVIDENCE_DIR/plan.json"
```

This policy reads the **entire planned-values tree**, including nested modules, and checks supported network/auth/TLS properties. It rejects destructive changes to protected resource types, reports unknown security-sensitive fields as NOT_READY, and requires expected resource types for the specified `dev` or `bootstrap` scope. It does **not** authorize any `apply`.

**Plan guard exit codes:**

| Exit | Status | Meaning |
|---:|---|---|
| 0 | `REVIEW_REQUIRED` | No policy violation/unknown found, but independent approval and Azure evidence still required |
| 1 | `FAIL_POLICY` | One or more explicit unsafe configurations or protected deletions |
| 2 | `NOT_READY` | Incomplete plan, unknown values, source/approval not present, or missing required resource type |

A synthetic fixture is never accepted as a real plan. The selftests do not publish real plan JSON or Azure IDs.

## 5. Coverage matrix

| Control | Prior project steps | Targeted policy evidence |
|---|---|---|
| Entra/OIDC-backed state bootstrap | B01–B05, Step 11–15 | No self-referencing bootstrap backend; Storage HTTPS/TLS, PNA/key auth off; scope review |
| Private network topology | N01–N05, Step 21–30 | Prior N04 contracts plus planned PE subnet/service-group/DNS checks |
| OpenAI/Search/Cosmos | A01–A06, Step 33–45 | PNA off, local key auth off, secure endpoint and planned identity controls |
| Key Vault and identity | I01–I03, Step 37–43 | PNA off, purge protection and RBAC on |
| App Service | W01–W05, Step 46–50 | PNA off, TLS >=1.2, HTTPS on, FTP/basic auth off, distinct private inbound/egress designs |
| Application Gateway and WAF | GW01–GW05, Step 51–57 | WAF_v2 and private frontend only, Key Vault TLS reference, approved WAF mode |
| Logs and evidence | Step 57, 59–78 | Log Analytics public ingestion/query off; reviewer attestation remains separate |

## 6. Troubleshooting and false-green prevention

| Symptom | Likely cause | Resolution |
|---|---|---|
| `cd: ... No such file or directory` | Repository not cloned | Use the one-paste clone/checkout above; copying a ZIP is not equivalent to `git clone` |
| `terraform: command not found` | CLI not available | Keep fmt/validate NOT_READY; use approved installation/mirror, not an improvised provider download |
| `init -lockfile=readonly` fails | No approved lockfile or provider version mismatch | Obtain pinned provider from approved registry/mirror, generate lock in controlled review workflow, commit reviewed lockfile |
| Q01 reports missing checker | Git checkout stale or incomplete | `git pull --ff-only`; compare Git commit; do not edit test expectations to silence errors |
| Q02 says expected type missing | Partial/targeted plan or mismatched scope | Perform full approved scope plan or review authorized scope explicitly; no automatic PASS |
| Q02 says unresolved private endpoint ID/DNS | Newly computed Terraform values, plan phase incomplete | Obtain approved source dependency proof; independent reviewer decides if separate pre-apply acceptance is possible; never invent values |
| Q02 reports public access enabled | Misconfigured PNA/identity/private endpoint | Revert HCL; rerun Q01/Q02; require two-person review before any approval |
| WAF Prevention returns NOT_READY | No external signed mode-change approval | Keep Detection until approved WAF test evidence exists |
| Plan reports `REVIEW_REQUIRED` | Plan alone cannot prove runtime isolation | Reviewer checks exact resource inventory, DNS/PE NIC, change diff, logs and signed baseline |

## 7. Known gaps and next implementation nodes

- Q01 still lacks **real** Terraform CLI fmt/validate and approved provider schema; no approved `.terraform.lock.hcl` is present in the reviewed Stage 6 archive.
- Azure plan/PE DNS/identity/certificate evidence and actual application code are missing.
- AMPLS/private monitoring ingress (O02), actual Playwright E2E tests (V04) and authorized nonproduction runtime checks remain incomplete.
- The plan guard intentionally returns `NOT_READY` for unresolved planned attributes; do not weaken it to avoid a first-deployment blocker without an independent, auditable review path.
- Next turn: improve provider/lock readiness and close schema findings before any Q03 planned deployment. **User action is not needed for the present Q01/Q02 offline work.** Before a real plan, environment owner must supply approved nonprod inventory, CI federation/permissions, scoped network/DNS, service SKU/model choices and authorization.
