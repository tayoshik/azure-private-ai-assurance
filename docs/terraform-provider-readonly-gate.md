# P4 — Terraform 1.9.8 / AzureRM 4.66.0 readonly provider validation

**2026-11-22. Azure subscription unavailable; credentials are deliberately excluded.**

## Verified starting point

- Root modules: `infra/bootstrap` and `infra/environments/dev`.
- Both `versions.tf` files require `hashicorp/azurerm = 4.66.0` and Terraform CLI `>= 1.9.0, < 2.0.0`.
- Both roots already have checked-in, byte-identical `.terraform.lock.hcl` files with `h1:` and `zh:` checksums.
- An earlier hosted GitHub Actions provider-schema run succeeded, but the historical workflow called `terraform fmt -recursive infra` before initializing/validating providers. This silently altered the transient checkout rather than validating **exactly** the reviewed source HCL.
- Historical `terraform init` did not specify readonly lockfile enforcement. Validating a generated or changed lock without an explicit check does not prove the reviewed pinned lock was honored.

## Implemented change

1. `scripts/verify_terraform_lock_consistency.py`: **no Terraform CLI**. Read both roots, fail on a missing lock or version file, wrong source, wrong provider version or CLI range, missing/malformed/duplicate `h1`/`zh` checksums, a second provider, or byte differences across the two approved roots. Report SHA-256 per lock. This is **structural input verification only**, not an online registry signature check.
2. `tests/test_terraform_lock_consistency.py`: 16 synthetic positive/mutation tests with isolated temporary directories; no Azure connectivity.
3. `.github/workflows/terraform-provider-schema-real.yml`: run the source/lock audit and its tests; **do not run mutating `terraform fmt`**; run `terraform fmt -check -diff -recursive infra`, `terraform init -backend=false -lockfile=readonly -input=false -no-color` separately in both roots, then `terraform validate -no-color`. Compare original and final locked file SHA-256, and require `git diff --exit-code -- infra`.
4. Keep CLI pinned to Terraform **1.9.8**, use actual provider **AzureRM 4.66.0**, `permissions: contents: read`, and upload sanitized version, validation, init and lockfile-hash artifacts. Provider download from the official registry **does require outbound registry access** on GitHub-hosted CI; it does not access Azure resources.

## Intended CI results (not acceptance)

- `source-preflight`: original source pins and both lockfiles satisfy our structural rules; mutation regressions pass.
- `format-check`: original checkout source already complies with `terraform fmt`.
- `provider-schema`: official Terraform binary initializes both pinned provider roots without configuring a remote backend, verifies pinned lockfile checksums with `-lockfile=readonly`, and validates the full HCL/module graph against actual provider schemas. No `terraform plan` or `terraform apply` is executed.
- Any changed source, provider constraint, absent/mismatched lock, invalid checksum, runtime provider-init problem or validation problem **fails CI**, not silently repaired.
- This provider job is path-filtered and must **not** be added as a globally required Ruleset check without first adjusting its trigger conditions. The always-on ruleset gates remain `offline-main-gate` and `offline-catalogue`.

## Reproduction without Azure login

Requires locally installed Terraform 1.9.8 and network access **only to Terraform provider registries**. Python preflight requires neither Terraform nor network.

```bash
set -Eeuo pipefail
python3 scripts/terraform_provider_preflight.py
python3 scripts/verify_terraform_lock_consistency.py
python3 -m unittest discover -s tests -p 'test_terraform_provider_preflight.py' -v
python3 -m unittest discover -s tests -p 'test_terraform_lock_consistency.py' -v

terraform fmt -check -diff -recursive infra
sha256sum infra/bootstrap/.terraform.lock.hcl infra/environments/dev/.terraform.lock.hcl > /tmp/tf-lock-before.txt
terraform -chdir=infra/bootstrap init -backend=false -lockfile=readonly -input=false -no-color
terraform -chdir=infra/bootstrap validate -no-color
terraform -chdir=infra/environments/dev init -backend=false -lockfile=readonly -input=false -no-color
terraform -chdir=infra/environments/dev validate -no-color
sha256sum infra/bootstrap/.terraform.lock.hcl infra/environments/dev/.terraform.lock.hcl > /tmp/tf-lock-after.txt
diff -u /tmp/tf-lock-before.txt /tmp/tf-lock-after.txt
git diff --exit-code -- infra
```

**Reference:** [Terraform `init` official documentation](https://developer.hashicorp.com/terraform/cli/commands/init) documents `-backend=false` and `-lockfile=readonly`; [Terraform `validate` official documentation](https://developer.hashicorp.com/terraform/cli/commands/validate) describes initialized-provider validation. Do not confuse it with plan-time validation of real subscriptions and access policies.

## Bounded conclusion

A passing **offline** provider workflow establishes pinned **source/HCL/provider-schema validity**, not Azure configuration correctness at deployment time, network isolation, financial approval, production security acceptance or an independent release signature. **Azure live passes 0 / 1,716 NOT_READY / release NO_GO** stay unchanged.

**Future approved change:** if bootstrap and DEV legitimately require different provider versions/dependency locks, update this exact two-root policy through versioned review; do **not** weaken checksum controls silently.
