# Maintainer Handoff — Azure Private AI Assurance

**Applies to:** the public `tayoshik/azure-private-ai-assurance` repository and the 2026-11-14 English catalogue baseline.

## Source-of-truth and scope

- `docs/78-step-construction-runbook.md`: sequence, ownership, approved environments, commands and failure triage.
- `specs/english_tests_001_440.json`, `specs/phase{3,4,5,6,7}_*_en.json`: six machine-readable English test catalogues covering 78 steps and 1,716 unique IDs. Maintain IDs and a change log; do not silently renumber.
- `docs/phase{1,2,3,4,5,6,7}-*-english-tests.md`: readable test procedures. A shell command's syntax alone is not a pass condition.
- `scripts/verify_publication.py`: offline publication completeness/uniqueness test; not a cloud acceptance checker.
- `docs/final-accomplishment-report.md`: outcome, known gaps and honest acceptance status.

## Reproduce publication checks on WSL2 (no Azure login)

```bash
set -Eeuo pipefail
git clone https://github.com/tayoshik/azure-private-ai-assurance.git
cd azure-private-ai-assurance
git rev-parse HEAD
python3 scripts/verify_publication.py
python3 -m unittest discover -s tests -p 'test_publication*.py' -v
# Optional: inspect current Git tree and possible secret-like files
git ls-files | sort
git grep -nE 'gh[pousr]_[A-Za-z0-9]{25,}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----' -- . || true
```

**Interpretation:** `git grep` is only a basic heuristic. Use an approved secrets scanner and manual disclosure review before granting public access. The helper does not create or authenticate to Azure.

## Handoff inputs required before testing actual Azure resources

1. Obtain the real source repository URL + commit SHA for Terraform, application, Playwright, dependency lock files, and configuration.
2. Obtain an approved non-production inventory: tenant/subscription, resource IDs, region, VNet/subnet/private endpoint/NICs, FQDNs and expected DNS/IP records. Store sensitive inventories outside this public repository.
3. Confirm approved test-runner VNet attachment, workload-identity federation, least-privilege RBAC, approved Terraform/provider version, and organization review gates. Do not use `az login` on the restricted WSL workstation.
4. Approve bounded network tests, safe WAF simulations, performance budget, data classification, log retention and rollback owners **before execution**.
5. Capture test ID, source SHA, asset ID, time, runner ID, command, exit status, expected/observed values, and immutable evidence hash. Verify signature using the organization's trusted key, not the demonstration key.
6. Conduct an independent acceptance review. Mark missing evidence `NOT_READY`, a verified violation `FAIL`, and only fully supported and reviewed controls `PASS`.
7. Authorize Terraform `apply` only in a separate human-approved, least-privilege runner workflow; never run it merely to make an offline validation pass.

## Safe troubleshooting decision table

| Condition | Treatment |
|---|---|
| Missing source, baseline, Azure asset or trusted signature | NOT_READY; no success claim |
| GitHub JSON absent or duplicate test ID | FAIL publication integrity; fix catalogue and rerun CI |
| Internal DNS resolves unexpectedly | Investigate Private DNS/VNet link/forwarding and compare with approved private IP; not automatic PASS |
| External connection rejected or 403 received | Check actual resource existence, public network settings, gateway/WAF logs, transaction ID and approved negative-test conditions |
| Terraform plan shows changes | Investigate drift or intentional approved changes; do not automatically apply |
| GitHub Action fails due to dependency or path | Fix build/test wiring; do not alter Azure release acceptance |

## Operator approval checkpoints

**No user action is required for the completed publication and offline integrity checks.** Azure live execution cannot begin until approved non-production environment, source access and explicit authorization are provided. Treat the first environment-onboarding turn as the earliest likely user-input checkpoint. The next turn, if requested, should focus on these inputs, not duplicate earlier public Azure product research.

## Publication and security

This is a **public** research/engineering documentation repository, not an organization-authorized production reference implementation. Never publish tenant IDs, customer data, production network details, secrets, raw state, CI tokens, or private certificates. Archive originals separately with verified SHA-256 and access controls.
