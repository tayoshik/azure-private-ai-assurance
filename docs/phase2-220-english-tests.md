# Phase 2 / Steps 11–20 (220 cases): Detailed English Security Test Procedures

**Status:** Design-only verification catalogue. 0 accepted live Azure passes. Every case remains NOT_READY.

The original case IDs, the corrected Phase 1 predicates, and Phase 2 source commands have been retained. Command snippets are *proposals* and must be reviewed for the deployed CLI version, source code, and environment. They were not run against Azure.

## Operating rules

- **WSL:** offline file, Terraform configuration and policy checks; do not use interactive `az login` on the restricted workstation.
- **Approved CI with OIDC:** Azure read-only inventory commands only after approved scope and authorization are established.
- **Isolated offline runner:** synthetic negative tests only. Never attack production, mutate live role assignments, or use missing resources as evidence of isolation.
- **Verdicts:** Missing source or approver -> NOT_READY. Verified deviation -> FAIL. Local predicate matched -> REVIEW_REQUIRED. Azure PASS requires independently approved live evidence; no cases have reached it.
- **Secrets:** never commit raw Terraform state/plan, authentication tokens, user data or internal asset identifiers to a public repository.

## Offline verification commands

```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --all
python3 scripts/phase2_policy_check.py --selftest ALL --spec specs/phase2_220.json
python3 scripts/verify_english_tests.py
```

**Important:** These three commands check *local synthetic data and catalogue consistency*. They cannot establish Azure resource configuration, security enforcement or approval.

## Step 11: Terraform state bootstrap separation

**Traceability:** AZ-T11-01 through AZ-T11-22 (22 IDs, 11 controls).

### AZ-T11-01 — Separate bootstrap state — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -d bootstrap && test -d infra && find bootstrap infra -maxdepth 3 -name "*.tf" -print
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Separate bootstrap state. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-02 — Separate bootstrap state — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-02 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Separate bootstrap state must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-03 — Management resource group — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az group show --name "$STATE_RG" --query "{id:id,location:location,tags:tags}" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Management resource group. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-04 — Management resource group — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-04 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Management resource group must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-05 — Storage account naming — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage account show --name "$STATE_SA" --resource-group "$STATE_RG" --query "{id:id,name:name,kind:kind}" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Storage account naming. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-06 — Storage account naming — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-06 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Storage account naming must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-07 — Blob container naming — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage container show --name "$STATE_CONTAINER" --account-name "$STATE_SA" --auth-mode login --query "{name:name,publicAccess:properties.publicAccess}" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Blob container naming. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-08 — Blob container naming — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-08 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Blob container naming must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-09 — Backend authorization — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az role assignment list --scope "$STATE_CONTAINER_RESOURCE_ID" --all -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Backend authorization. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-10 — Backend authorization — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-10 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Backend authorization must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-11 — Resource locks — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az lock list --resource-group "$STATE_RG" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Resource locks. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-12 — Resource locks — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-12 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Resource locks must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-13 — Diagnostics destination — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az monitor diagnostic-settings list --resource "$STATE_SA_RESOURCE_ID" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Diagnostics destination. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-14 — Diagnostics destination — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-14 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Diagnostics destination must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-15 — State deletion recovery — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/state-recovery.md && sha256sum docs/state-recovery.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: State deletion recovery. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-16 — State deletion recovery — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-16 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for State deletion recovery must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-17 — Bootstrap recovery ownership — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/ownership-matrix.md && sha256sum docs/ownership-matrix.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Bootstrap recovery ownership. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-18 — Bootstrap recovery ownership — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-18 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Bootstrap recovery ownership must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-19 — Provisioning order — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
find .github/workflows scripts -type f \( -name "*.yml" -o -name "*.yaml" -o -name "*.sh" \) -print 2>/dev/null
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Provisioning order. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-20 — Provisioning order — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-20 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Provisioning order must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-21 — Main state independence — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -f bootstrap/backend.tf && test -f infra/backend.tf && sha256sum bootstrap/backend.tf infra/backend.tf
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Main state independence. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T11-22 — Main state independence — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T11-22 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Main state independence must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

## Step 12: Remote-state Storage hardening

**Traceability:** AZ-T12-01 through AZ-T12-22 (22 IDs, 11 controls).

### AZ-T12-01 — Blob minimum TLS — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage account show -g "$STATE_RG" -n "$STATE_SA" --query minimumTlsVersion -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Blob minimum TLS. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-02 — Blob minimum TLS — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-02 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Blob minimum TLS must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-03 — Disable shared key authorization — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage account show -g "$STATE_RG" -n "$STATE_SA" --query allowSharedKeyAccess -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Disable shared key authorization. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-04 — Disable shared key authorization — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-04 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Disable shared key authorization must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-05 — Disable public storage access — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage account show -g "$STATE_RG" -n "$STATE_SA" --query publicNetworkAccess -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Disable public storage access. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-06 — Disable public storage access — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-06 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Disable public storage access must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-07 — Blob versioning — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage account blob-service-properties show -g "$STATE_RG" --account-name "$STATE_SA" --query isVersioningEnabled -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Blob versioning. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-08 — Blob versioning — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-08 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Blob versioning must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-09 — Soft delete retention — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage account blob-service-properties show -g "$STATE_RG" --account-name "$STATE_SA" --query "deleteRetentionPolicy" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Soft delete retention. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-10 — Soft delete retention — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-10 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Soft delete retention must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-11 — Least-privilege RBAC scope — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az role assignment list --scope "$STATE_SA_RESOURCE_ID" --all -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Least-privilege RBAC scope. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-12 — Least-privilege RBAC scope — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-12 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Least-privilege RBAC scope must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-13 — Container authorization scope — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az role assignment list --scope "$STATE_CONTAINER_RESOURCE_ID" --all -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Container authorization scope. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-14 — Container authorization scope — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-14 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Container authorization scope must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-15 — Storage diagnostic settings — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az monitor diagnostic-settings list --resource "$STATE_SA_RESOURCE_ID" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Storage diagnostic settings. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-16 — Storage diagnostic settings — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-16 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Storage diagnostic settings must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-17 — Deletion prevention locks — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az lock list --resource-group "$STATE_RG" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Deletion prevention locks. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-18 — Deletion prevention locks — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-18 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Deletion prevention locks must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-19 — State data classification — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/data-classification.md && sha256sum docs/data-classification.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: State data classification. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-20 — State data classification — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-20 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for State data classification must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-21 — Blob audit events — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az monitor diagnostic-settings list --resource "$STATE_SA_RESOURCE_ID" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Blob audit events. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T12-22 — Blob audit events — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T12-22 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Blob audit events must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

## Step 13: State private endpoint and DNS

**Traceability:** AZ-T13-01 through AZ-T13-22 (22 IDs, 11 controls).

### AZ-T13-01 — Blob private endpoint — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az network private-endpoint show -g "$NETWORK_RG" -n "$STATE_PE" --query "{id:id,networkInterfaces:networkInterfaces}" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Blob private endpoint. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-02 — Blob private endpoint — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-02 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Blob private endpoint must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-03 — Private DNS zone — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az network private-dns zone show -g "$DNS_RG" -n privatelink.blob.core.windows.net -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Private DNS zone. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-04 — Private DNS zone — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-04 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Private DNS zone must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-05 — Private endpoint approval — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az network private-endpoint show -g "$NETWORK_RG" -n "$STATE_PE" --query "privateLinkServiceConnections[].privateLinkServiceConnectionState.status" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Private endpoint approval. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-06 — Private endpoint approval — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-06 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Private endpoint approval must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-07 — Blob subresource group — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az network private-endpoint show -g "$NETWORK_RG" -n "$STATE_PE" --query "privateLinkServiceConnections[].groupIds" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Blob subresource group. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-08 — Blob subresource group — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-08 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Blob subresource group must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-09 — CI runner DNS resolution — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
dig +short "${STATE_SA}.blob.core.windows.net"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: CI runner DNS resolution. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-10 — CI runner DNS resolution — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-10 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for CI runner DNS resolution must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-11 — CI runner TLS 443 — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
curl --noproxy "*" --connect-timeout 5 -sS -o /dev/null -w "%{http_code} %{remote_ip}\n" "https://${STATE_SA}.blob.core.windows.net/"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: CI runner TLS 443. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-12 — CI runner TLS 443 — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-12 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for CI runner TLS 443 must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-13 — Storage public network disabled — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage account show -g "$STATE_RG" -n "$STATE_SA" --query publicNetworkAccess -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Storage public network disabled. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-14 — Storage public network disabled — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-14 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Storage public network disabled must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-15 — External access restriction — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage account show -g "$STATE_RG" -n "$STATE_SA" --query "{pna:publicNetworkAccess,network:networkRuleSet}" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: External access restriction. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-16 — External access restriction — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-16 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for External access restriction must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-17 — Private DNS zone groups — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az network private-endpoint dns-zone-group list -g "$NETWORK_RG" --endpoint-name "$STATE_PE" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Private DNS zone groups. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-18 — Private DNS zone groups — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-18 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Private DNS zone groups must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-19 — CI OIDC container access — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage container show --name "$STATE_CONTAINER" --account-name "$STATE_SA" --auth-mode login -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: CI OIDC container access. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-20 — CI OIDC container access — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-20 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for CI OIDC container access must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-21 — Recovery path for state PE — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/state-recovery.md && sha256sum docs/state-recovery.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Recovery path for state PE. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T13-22 — Recovery path for state PE — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T13-22 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Recovery path for state PE must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

## Step 14: Terraform toolchain pinning

**Traceability:** AZ-T14-01 through AZ-T14-22 (22 IDs, 11 controls).

### AZ-T14-01 — Pinned Terraform CLI version — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
terraform version -json | jq -r .terraform_version
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Pinned Terraform CLI version. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-02 — Pinned Terraform CLI version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-02 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Pinned Terraform CLI version must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-03 — Pinned AzureRM provider — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R --line-number "required_providers" infra --include="*.tf"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Pinned AzureRM provider. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-04 — Pinned AzureRM provider — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-04 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Pinned AzureRM provider must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-05 — Terraform required_version — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R --line-number "required_version" infra --include="*.tf"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Terraform required_version. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-06 — Terraform required_version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-06 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Terraform required_version must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-07 — Tracked dependency lockfile — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
git ls-files --error-unmatch infra/.terraform.lock.hcl
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Tracked dependency lockfile. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-08 — Tracked dependency lockfile — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-08 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Tracked dependency lockfile must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-09 — Provider checksums — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
sha256sum infra/.terraform.lock.hcl && grep -n "hashes" infra/.terraform.lock.hcl
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Provider checksums. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-10 — Provider checksums — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-10 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Provider checksums must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-11 — Pinned modules — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R --line-number "source[[:space:]]*=" infra/modules --include="*.tf" 2>/dev/null
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Pinned modules. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-12 — Pinned modules — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-12 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Pinned modules must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-13 — CLI and SKU compatibility — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
terraform providers -no-color
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: CLI and SKU compatibility. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-14 — CLI and SKU compatibility — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-14 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for CLI and SKU compatibility must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-15 — CI Terraform version — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
terraform version -json | jq -r .terraform_version
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: CI Terraform version. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-16 — CI Terraform version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-16 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for CI Terraform version must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-17 — WSL Terraform version — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
terraform version -json | jq -r .terraform_version
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: WSL Terraform version. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-18 — WSL Terraform version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-18 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for WSL Terraform version must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-19 — Provider schema export — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
terraform providers schema -json | jq -r ".provider_schemas | keys[]"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Provider schema export. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-20 — Provider schema export — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-20 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Provider schema export must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-21 — Version upgrade approval — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/version-approval.md && sha256sum docs/version-approval.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Version upgrade approval. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T14-22 — Version upgrade approval — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T14-22 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Version upgrade approval must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

## Step 15: Federated backend authentication

**Traceability:** AZ-T15-01 through AZ-T15-22 (22 IDs, 11 controls).

### AZ-T15-01 — AzureRM backend declaration — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R -n "backend[[:space:]]*"azurerm"" infra --include="*.tf"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: AzureRM backend declaration. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-02 — AzureRM backend declaration — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-02 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for AzureRM backend declaration must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-03 — Azure AD backend auth — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R -n "use_azuread_auth" infra --include="*.tf"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Azure AD backend auth. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-04 — Azure AD backend auth — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-04 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Azure AD backend auth must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-05 — OIDC backend auth — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R -n "use_oidc" infra .github --include="*.tf" --include="*.yml" 2>/dev/null
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: OIDC backend auth. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-06 — OIDC backend auth — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-06 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for OIDC backend auth must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-07 — CI federation setup — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/oidc-federation.md && sha256sum docs/oidc-federation.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: CI federation setup. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-08 — CI federation setup — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-08 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for CI federation setup must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-09 — State storage container and key — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s infra/backend.hcl && sed -E "s/(key|secret|token) ?=.*/[REDACTED]/I" infra/backend.hcl
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: State storage container and key. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-10 — State storage container and key — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-10 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for State storage container and key must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-11 — Per-environment state keys — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R -n "key[[:space:]]*=" infra --include="*.tf"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Per-environment state keys. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-12 — Per-environment state keys — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-12 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Per-environment state keys must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-13 — Blob Data Contributor scope — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az role assignment list --scope "$STATE_CONTAINER_RESOURCE_ID" --all -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Blob Data Contributor scope. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-14 — Blob Data Contributor scope — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-14 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Blob Data Contributor scope must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-15 — No shared key fallback — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az storage account show -g "$STATE_RG" -n "$STATE_SA" --query allowSharedKeyAccess -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: No shared key fallback. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-16 — No shared key fallback — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-16 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for No shared key fallback must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-17 — Terraform init output — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
terraform init -input=false -lockfile=readonly -no-color
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Terraform init output. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-18 — Terraform init output — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-18 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Terraform init output must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-19 — No local state files — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
find infra -maxdepth 2 -name terraform.tfstate -print
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: No local state files. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-20 — No local state files — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-20 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for No local state files must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-21 — Concurrent state lock — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/backend-locking.md && sha256sum docs/backend-locking.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Concurrent state lock. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T15-22 — Concurrent state lock — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T15-22 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Concurrent state lock must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

## Step 16: IaC static quality gates

**Traceability:** AZ-T16-01 through AZ-T16-22 (22 IDs, 11 controls).

### AZ-T16-01 — Terraform fmt — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
terraform fmt -check -recursive -no-color infra
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Terraform fmt. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-02 — Terraform fmt — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-02 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Terraform fmt must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-03 — Terraform validate — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
terraform -chdir=infra validate -no-color
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Terraform validate. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-04 — Terraform validate — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-04 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Terraform validate must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-05 — Terraform test — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
find infra/tests -name "*.tftest.hcl" -print
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Terraform test. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-06 — Terraform test — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-06 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Terraform test must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-07 — TFLint — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
tflint --chdir infra --no-color
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: TFLint. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-08 — TFLint — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-08 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for TFLint must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-09 — Checkov — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
checkov -d infra --quiet
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Checkov. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-10 — Checkov — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-10 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Checkov must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-11 — OPA and Conftest — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
find policy -type f -maxdepth 3 -print
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: OPA and Conftest. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-12 — OPA and Conftest — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-12 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for OPA and Conftest must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-13 — Terraform plan JSON — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/plan/approved.tfplan.json && jq -e ".format_version" evidence/plan/approved.tfplan.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Terraform plan JSON. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-14 — Terraform plan JSON — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-14 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Terraform plan JSON must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-15 — Policy unit tests — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
find policy/tests -type f -maxdepth 3 -print
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Policy unit tests. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-16 — Policy unit tests — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-16 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Policy unit tests must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-17 — Static-analysis exit codes — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/ci/static-scan-exitcodes.json && jq -e ".jobs" evidence/ci/static-scan-exitcodes.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Static-analysis exit codes. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-18 — Static-analysis exit codes — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-18 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Static-analysis exit codes must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-19 — Fail-fast CI gate — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/ci-gates.md && sha256sum docs/ci-gates.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Fail-fast CI gate. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-20 — Fail-fast CI gate — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-20 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Fail-fast CI gate must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-21 — Security scan report retention — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/ci/security-scan-report.json && sha256sum evidence/ci/security-scan-report.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Security scan report retention. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T16-22 — Security scan report retention — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T16-22 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Security scan report retention must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

## Step 17: Avoiding false-positive negative tests

**Traceability:** AZ-T17-01 through AZ-T17-22 (22 IDs, 11 controls).

### AZ-T17-01 — Actual target resource exists — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/inventory/resources.json && jq -e ".resources" evidence/inventory/resources.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Actual target resource exists. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-02 — Actual target resource exists — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-02 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Actual target resource exists must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-03 — Target resource ID confirmed — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/inventory/resources.json && jq -r ".resources[].id" evidence/inventory/resources.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Target resource ID confirmed. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-04 — Target resource ID confirmed — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-04 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Target resource ID confirmed must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-05 — Expected public DNS name — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/endpoint-inventory.md && sha256sum docs/endpoint-inventory.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Expected public DNS name. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-06 — Expected public DNS name — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-06 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Expected public DNS name must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-07 — Absent resources yield NotReady — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/test-verdicts.md && sha256sum docs/test-verdicts.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Absent resources yield NotReady. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-08 — Absent resources yield NotReady — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-08 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Absent resources yield NotReady must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-09 — DNS failure classification — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
dig +short "${INTERNAL_APP_FQDN}"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: DNS failure classification. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-10 — DNS failure classification — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-10 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for DNS failure classification must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-11 — Timeout classification — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/test-verdicts.md && grep -n "Timeout" docs/test-verdicts.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Timeout classification. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-12 — Timeout classification — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-12 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Timeout classification must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-13 — HTTP 403 classification — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/test-verdicts.md && grep -n "403" docs/test-verdicts.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: HTTP 403 classification. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-14 — HTTP 403 classification — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-14 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for HTTP 403 classification must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-15 — HTTP 200 false-green prevention — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/test-verdicts.md && grep -n "200" docs/test-verdicts.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: HTTP 200 false-green prevention. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-16 — HTTP 200 false-green prevention — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-16 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for HTTP 200 false-green prevention must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-17 — TLS certificate error classification — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/test-verdicts.md && grep -n "TLS" docs/test-verdicts.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: TLS certificate error classification. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-18 — TLS certificate error classification — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-18 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for TLS certificate error classification must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-19 — Correlated evidence — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/ci/negative-test-matrix.json && jq -e .cases evidence/ci/negative-test-matrix.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Correlated evidence. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-20 — Correlated evidence — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-20 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Correlated evidence must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-21 — Negative verdict specification approval — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/test-verdicts.md && sha256sum docs/test-verdicts.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Negative verdict specification approval. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T17-22 — Negative verdict specification approval — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T17-22 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Negative verdict specification approval must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

## Step 18: External exposure assurance

**Traceability:** AZ-T18-01 through AZ-T18-22 (22 IDs, 11 controls).

### AZ-T18-01 — Public IP inventory — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az network public-ip list --resource-group "$APP_RG" --query "[].{id:id,name:name,ip:ipAddress}" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Public IP inventory. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-02 — Public IP inventory — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-02 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Public IP inventory must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-03 — Public network access inventory — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az resource list -g "$APP_RG" --query "[].{type:type,name:name,id:id}" -o json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Public network access inventory. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-04 — Public network access inventory — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-04 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Public network access inventory must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-05 — External DNS resolution — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
dig +short "${INTERNAL_APP_FQDN}" @1.1.1.1
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: External DNS resolution. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-06 — External DNS resolution — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-06 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for External DNS resolution must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-07 — External TLS reachability — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
curl --noproxy "*" --connect-timeout 5 -sS -o /dev/null -w "%{http_code} %{remote_ip}\n" "https://${INTERNAL_APP_FQDN}/healthz"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: External TLS reachability. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-08 — External TLS reachability — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-08 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for External TLS reachability must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-09 — App Service public FQDN — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az webapp show -g "$APP_RG" -n "$APP_NAME" --query publicNetworkAccess -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: App Service public FQDN. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-10 — App Service public FQDN — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-10 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for App Service public FQDN must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-11 — OpenAI public access — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az cognitiveservices account show -g "$APP_RG" -n "$OPENAI_NAME" --query publicNetworkAccess -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: OpenAI public access. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-12 — OpenAI public access — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-12 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for OpenAI public access must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-13 — AI Search public access — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az search service show -g "$APP_RG" -n "$SEARCH_NAME" --query publicNetworkAccess -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: AI Search public access. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-14 — AI Search public access — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-14 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for AI Search public access must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-15 — Cosmos DB public access — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az cosmosdb show -g "$APP_RG" -n "$COSMOS_NAME" --query publicNetworkAccess -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Cosmos DB public access. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-16 — Cosmos DB public access — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-16 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Cosmos DB public access must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-17 — Key Vault public access — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
az keyvault show -g "$APP_RG" -n "$VAULT_NAME" --query properties.publicNetworkAccess -o tsv
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Key Vault public access. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-18 — Key Vault public access — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-18 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Key Vault public access must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-19 — Config-to-observation comparison — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/external/config-vs-network.json && jq -e .observations evidence/external/config-vs-network.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Config-to-observation comparison. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-20 — Config-to-observation comparison — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-20 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Config-to-observation comparison must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-21 — External evidence retention — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/external/summary.json && sha256sum evidence/external/summary.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: External evidence retention. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T18-22 — External evidence retention — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T18-22 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for External evidence retention must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

## Step 19: Internal connectivity and E2E readiness

**Traceability:** AZ-T19-01 through AZ-T19-22 (22 IDs, 11 controls).

### AZ-T19-01 — Internal runner exists — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/runner/identity.json && jq -e .runner_id evidence/runner/identity.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Internal runner exists. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-02 — Internal runner exists — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-02 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Internal runner exists must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-03 — Runner private IP — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/runner/network.json && jq -e .private_ip evidence/runner/network.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Runner private IP. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-04 — Runner private IP — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-04 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Runner private IP must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-05 — Internal DNS resolver — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
getent hosts "${INTERNAL_APP_FQDN}"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Internal DNS resolver. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-06 — Internal DNS resolver — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-06 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Internal DNS resolver must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-07 — Private application FQDN — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
dig +short "${INTERNAL_APP_FQDN}"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Private application FQDN. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-08 — Private application FQDN — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-08 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Private application FQDN must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-09 — Health endpoint — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
curl --noproxy "*" --connect-timeout 5 --max-time 15 -sS -o /dev/null -w "%{http_code}\n" "https://${INTERNAL_APP_FQDN}/healthz"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Health endpoint. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-10 — Health endpoint — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-10 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Health endpoint must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-11 — App Service private endpoint — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
dig +short "${APP_NAME}.azurewebsites.net"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: App Service private endpoint. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-12 — App Service private endpoint — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-12 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for App Service private endpoint must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-13 — OpenAI private DNS — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
dig +short "${OPENAI_NAME}.openai.azure.com"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: OpenAI private DNS. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-14 — OpenAI private DNS — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-14 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for OpenAI private DNS must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-15 — AI Search private DNS — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
dig +short "${SEARCH_NAME}.search.windows.net"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: AI Search private DNS. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-16 — AI Search private DNS — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-16 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for AI Search private DNS must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-17 — Cosmos DB private DNS — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
dig +short "${COSMOS_NAME}.documents.azure.com"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Cosmos DB private DNS. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-18 — Cosmos DB private DNS — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-18 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Cosmos DB private DNS must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-19 — Managed identity smoke check — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/runner/mi-health.json && jq -e .auth_success evidence/runner/mi-health.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Managed identity smoke check. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-20 — Managed identity smoke check — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-20 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Managed identity smoke check must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-21 — Internal evidence capture — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s evidence/runner/summary.json && sha256sum evidence/runner/summary.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Internal evidence capture. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T19-22 — Internal evidence capture — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T19-22 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Internal evidence capture must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

## Step 20: Playwright initialization

**Traceability:** AZ-T20-01 through AZ-T20-22 (22 IDs, 11 controls).

### AZ-T20-01 — Playwright pinned version — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s tests/package-lock.json && npm --prefix tests ls @playwright/test --depth=0
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Playwright pinned version. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-02 — Playwright pinned version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-02 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Playwright pinned version must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-03 — Node.js pinned version — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
node --version
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Node.js pinned version. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-04 — Node.js pinned version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-04 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Node.js pinned version must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-05 — npm lockfile — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s tests/package-lock.json && sha256sum tests/package-lock.json
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: npm lockfile. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-06 — npm lockfile — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-06 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for npm lockfile must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-07 — External Playwright project — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R -n "name:[[:space:]]*.*external" tests/playwright.config.ts
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: External Playwright project. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-08 — External Playwright project — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-08 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for External Playwright project must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-09 — Internal Playwright project — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R -n "name:[[:space:]]*.*internal" tests/playwright.config.ts
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Internal Playwright project. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-10 — Internal Playwright project — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-10 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Internal Playwright project must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-11 — HTTP response assertion — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R -n "expect(.*status" tests --include="*.ts"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: HTTP response assertion. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-12 — HTTP response assertion — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-12 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for HTTP response assertion must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-13 — TLS verification — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R -n "ignoreHTTPSErrors" tests --include="*.ts"
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: TLS verification. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-14 — TLS verification — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-14 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for TLS verification must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-15 — JUnit reporter — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R -n "junit" tests/playwright.config.ts
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: JUnit reporter. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-16 — JUnit reporter — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-16 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for JUnit reporter must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-17 — Trace report control — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
grep -R -n "trace" tests/playwright.config.ts
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Trace report control. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-18 — Trace report control — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-18 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Trace report control must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-19 — Screenshot data handling — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
test -s docs/test-data-handling.md && sha256sum docs/test-data-handling.md
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Screenshot data handling. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-20 — Screenshot data handling — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-20 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Screenshot data handling must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-21 — Reproducible npm ci — Positive Review

**Execution:** `READ_ONLY_EVIDENCE`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
cd tests && npm ci --ignore-scripts --offline && npx --no-install playwright test --list
```

**Expected and acceptance criteria:** Approved configuration or observed result must demonstrate: Reproducible npm ci. Check actual values against the review-approved control baseline and resource ID; command exit success alone is insufficient.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)

### AZ-T20-22 — Reproducible npm ci — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** An approved, scoped baseline and traceable asset or design identifier must exist; an offline fixture is never Azure evidence.

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase2_policy_check.py --selftest AZ-T20-22 --spec specs/phase2_220.json
```

**Expected and acceptance criteria:** An isolated synthetic deviation or missing observation for Reproducible npm ci must be rejected (FAIL or NOT_READY); no live resource is modified.

**Required evidence:** Synthetic self-test ID, policy/tool SHA-256, expected deviation and verdict. This is not a live block test.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 2 original 220-test JSON (command preserved, English interpretation added)
