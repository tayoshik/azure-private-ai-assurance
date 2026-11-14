# Stage 8 — Terraform CLI / AzureRM Provider Schema Verification

**Status:** SOURCE AND OFFLINE CHECKS; Azure live PASS = **0**, release = **NO-GO**. This stage tests the source syntax and the pinned AzureRM Provider schema; it does **not** create resources or prove that the chosen Azure SKU/region is available.

## 0. Provenance and constraints

Source: existing public repository, baseline Q01/Q02 (137 synthetic tests), 61 `.tf` files, two Terraform roots. Do not redo earlier network, AI, IAM, or Gateway design; use the existing modules. No interactive `az login` from fixed WSL. Azure `plan`/`apply` are explicitly out of scope. Terraform `1.9.8` and AzureRM `4.66.0` are **provisional** exact pins, not an independent approval.

Terraform needs an installed provider plugin for `validate`. `terraform init -backend=false` avoids configuring the remote backend for offline source validation. Check the current official HashiCorp documentation before any change to those commands. Do not treat a text-only checker, `fmt`, `validate`, or a downloaded provider as proof of Azure deployment success.

## 1. Work products and prerequisites

- `.github/workflows/terraform-provider-schema-real.yml` — automatic push/PR/manual three-job workflow (source preflight, formatting, real provider schema).
- `scripts/terraform_provider_preflight.py` — read-only CLI/lockfile/dual-root prerequisite inspector.
- `tests/test_terraform_provider_preflight.py` — negative and baseline tests.
- **Required source inputs:** `infra/bootstrap/versions.tf`, `infra/environments/dev/versions.tf`, module source files. **Expected provider lockfiles:** `infra/bootstrap/.terraform.lock.hcl`, `infra/environments/dev/.terraform.lock.hcl`; both are currently **MISSING** until real provider initialization on trusted CI and independent review.

## 2. WSL2: one-paste preflight (no Azure login, no Terraform required)

```bash
cat <<'CATEOF' > /tmp/azure_tf_stage8_offline.sh
#!/usr/bin/env bash
set -Eeuo pipefail
REPO="$HOME/azure-private-ai-assurance"
OUT="$HOME/azure-private-ai-assurance-qa/stage8"
mkdir -p "$OUT"
test -d "$REPO/.git" || { echo "MISSING_REPO: $REPO" >&2; exit 1; }
cd "$REPO"
# Do not discard local edits; manual reconciliation needed if pull fails.
git pull --ff-only
git rev-parse HEAD | tee "$OUT/git-head.txt"
python3 scripts/terraform_provider_preflight.py | tee "$OUT/provider-preflight.json"
python3 scripts/terraform_q01_integrated.py | tee "$OUT/q01-integrated.json"
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v \
  2>&1 | tee "$OUT/terraform-tests.log"
sha256sum "$OUT"/* | tee "$OUT/SHA256SUMS.txt"
echo "SOURCE_CHECK_COMPLETE: provider/Azure verification is separate"
CATEOF
bash /tmp/azure_tf_stage8_offline.sh
```

**Expected:** `PASS_SOURCE_WITH_PROVIDER_GATES_NOT_READY`, `PASS_OFFLINE_CONTRACT_ONLY`, 145 Python tests, `Azure live PASS = 0`. Lockfile and local CLI blockers are not source failures; they stay explicit `NOT_READY`.

## 3. Approved CI: real Terraform CLI + provider validation

A push to this repository triggers `Terraform provider schema verification (no Azure credentials)` with separate jobs:

1. **source-preflight:** verifies two roots, source pins, and missing lockfile disclosure.
2. **format-check:** `terraform fmt -check -diff -recursive infra`. Failure means actual HCL formatting needs remediation; it is never silently waived.
3. **provider-schema:** pins Terraform `1.9.8`, reformats a disposable Actions checkout (no source commit), runs `terraform init -backend=false -input=false -no-color` and `terraform validate -no-color` for **both** roots. The job uploads logs, a format patch, and generated provider lockfile candidates. The generated lockfiles are **not approved or merged** by this workflow.

**CI commands** (in the approved clean checkout):

```bash
set -Eeuo pipefail
terraform version
terraform fmt -check -diff -recursive infra
terraform -chdir=infra/bootstrap init -backend=false -input=false -no-color
terraform -chdir=infra/bootstrap validate -no-color
terraform -chdir=infra/environments/dev init -backend=false -input=false -no-color
terraform -chdir=infra/environments/dev validate -no-color
```

The workflow runs its provider schema job independently of the format-check job to collect both results. Validation happens after formatting the **ephemeral checkout**; code in GitHub may still require formatting fixes.

## 4. Review generated dependency locks before committing

The official registry download and installer verify signed provider package checksums; verify the provider source (`registry.terraform.io/hashicorp/azurerm`), `4.66.0`, supported target OS/architecture, signer and hashes, then conduct **two independent reviews**. Never invent hashes. For multi-platform releases use `terraform providers lock -platform=linux_amd64 -platform=windows_amd64` with an approved registry or mirror and verify the signer. Commit reviewed lockfiles for both roots, but never commit `.terraform`, credentials, `.tfstate`, `.tfplan`, or raw production logs.

A missing lockfile is an explicit blocker for final G03 approval even if ephemeral CI `init` creates a candidate.

## 5. Failure classification, triage and fallback

| Failure | Likely cause | Corrective action and evidence |
|---|---|---|
| `fmt` fails | existing HCL spacing/indent | inspect `terraform-fmt.patch` artifact; make reviewed source-only formatting commit; rerun |
| `init` fails reaching provider Registry | offline runner/proxy/mirror/certificate | use approved provider mirror; do **not** disable TLS validation; record registry/mirror provenance |
| `validate` reports unsupported argument | provider/schema mismatch | inspect exact resource, file, attribute, AzureRM version; fix HCL; run baseline 145 tests and revalidate |
| `validate` reports undeclared input/output | module interface mismatch | fix module variables/outputs and root binding; add negative test |
| `validate` fails on uninitialized backend | failed `init` or wrong `-backend=false` usage | rerun init in the correct root; never configure production backend for local validation |
| Missing `.terraform.lock.hcl` | candidate not reviewed or not generated | keep G03 `NOT_READY`; generate signed candidate in CI, double review and commit |
| Azure tenant/region/models unknown | G07 not approved | defer all real `plan`/`apply`; continue source-only fixes |

## 6. Completion gates

**G03/Q01 provider validation can be recorded as passed only when:** both root `fmt` checks pass; both provider installs are authenticated and logged; both `validate` runs exit 0; lockfiles match exact pins, are reviewed and committed; SHA-256/commit/CI run IDs are recorded. This still does **not** authorize Q03 (`plan`). For Q03 additionally require G07 (subscription, region, CIDRs, identity, certificate, quota, approved runner), B05 (private backend reachable), independent scope approvals and evidence storage. **Current stage remains NO-GO**.

## 7. First real CI result and corrective change record (2026-11-14)

- Baseline commit `651791fc5946303cd02e8d744a493458ec86c961` → [CI run 43598887055](https://github.com/tayoshik/azure-private-ai-assurance/actions/runs/43598887055).
- `source-preflight`: PASS; 145/145 tests at first publish.
- `format-check`: FAIL; actual Terraform CLI found formatting changes in 19 HCL files. The provider-schema job uploaded a **39,039-byte official `terraform fmt` diff**; do not ignore this formatting failure.
- `provider-schema`: actual Terraform CLI `1.9.8` and HashiCorp-signed AzureRM `4.66.0` were installed successfully. `infra/bootstrap` init + validate **PASS**. `infra/environments/dev` init **PASS**, validate **FAIL** on `azurerm_cosmosdb_account.no_sql.local_authentication_enabled` (unsupported argument in 4.66.0).
- **Fix:** Replace Cosmos account `local_authentication_enabled = false` with `local_authentication_disabled = true`, update the A01-A06 source-contract checker and Q02 Plan guard to assert the opposite boolean polarity, and add two synthetic negative cases. **The Search Service attribute is different and must remain `local_authentication_enabled = false`.**
- Applied the actual CI `terraform fmt` patch to 19 files; manually reconciled three hunks with prior source comments/modified Cosmos setting. Refactored the mutation test helper to tolerate HCL spacing so formatting does not create false failures. On the corrected candidate **147/147** local Python tests PASS; local CLI is absent, so only a new GitHub Actions run can confirm real `fmt` and `validate`.
- Both roots generated **matching provisional lockfile candidates** from the provider registry in CI, SHA-256 `4c4d4bd4ac67e53c049edb3daeadf355847221daa1fdecea59522068dcf6cfc1`. Do not merge them as final approved locks until signed package, platform coverage, provider version and two independent reviews are complete.

**Close gate only after checking the corrected follow-up CI run.** No prior static PASS is evidence of a real Azure deployment. Azure Plan/Apply and 1,716 live tests remain NOT_READY; formal decision remains NO-GO.
