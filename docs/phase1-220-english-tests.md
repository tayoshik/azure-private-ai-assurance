# Phase 1 / Steps 01–10 (220 cases): Detailed English Security Test Procedures

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

## Step 01: Private boundary definition

**Traceability:** AZ-T01-01 through AZ-T01-22 (22 IDs, 11 controls).

### AZ-T01-01 — Business data-plane boundary — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-01
```

**Expected and acceptance criteria:** The design field `network.data_plane.private_only` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-02 — Business data-plane boundary — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-02
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network.data_plane.private_only` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-03 — Azure management-plane exceptions — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-03
```

**Expected and acceptance criteria:** The design field `network.management_plane.dependencies_documented` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-04 — Azure management-plane exceptions — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-04
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network.management_plane.dependencies_documented` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-05 — Identity dependency flows — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-05
```

**Expected and acceptance criteria:** The design field `network.identity_plane.dependencies_documented` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-06 — Identity dependency flows — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-06
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network.identity_plane.dependencies_documented` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-07 — Monitoring data flows — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-07
```

**Expected and acceptance criteria:** The design field `network.monitoring_plane.allowed_flows_documented` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-08 — Monitoring data flows — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-08
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network.monitoring_plane.allowed_flows_documented` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-09 — Package supply-chain access — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-09
```

**Expected and acceptance criteria:** The design field `network.supply_chain.approved_sources_documented` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-10 — Package supply-chain access — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-10
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network.supply_chain.approved_sources_documented` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-11 — Corporate user ingress — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-11
```

**Expected and acceptance criteria:** The design field `network.user_access.method` must satisfy the approved predicate (enum). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-12 — Corporate user ingress — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-12
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network.user_access.method` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-13 — No public WAF frontend — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-13
```

**Expected and acceptance criteria:** The design field `application_gateway.frontend_visibility` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-14 — No public WAF frontend — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-14
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `application_gateway.frontend_visibility` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-15 — No direct public application ingress — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-15
```

**Expected and acceptance criteria:** The design field `app_service.public_network_access_enabled` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-16 — No direct public application ingress — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-16
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `app_service.public_network_access_enabled` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-17 — Private endpoints between services — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-17
```

**Expected and acceptance criteria:** The design field `ai_services.private_endpoint_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-18 — Private endpoints between services — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-18
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_services.private_endpoint_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-19 — Exception approval expiry — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-19
```

**Expected and acceptance criteria:** The design field `exceptions.expiry_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-20 — Exception approval expiry — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-20
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `exceptions.expiry_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-21 — ADR-001 approver — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T01-21
```

**Expected and acceptance criteria:** The design field `governance.adr001_dual_approval_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T01-22 — ADR-001 approver — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T01-22
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `governance.adr001_dual_approval_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

## Step 02: Corporate connectivity

**Traceability:** AZ-T02-01 through AZ-T02-22 (22 IDs, 11 controls).

### AZ-T02-01 — Approved ExpressRoute or VPN type — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-01
```

**Expected and acceptance criteria:** The design field `connectivity.selected_type` must satisfy the approved predicate (enum). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-02 — Approved ExpressRoute or VPN type — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-02
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `connectivity.selected_type` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-03 — Corporate client CIDR — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-03
```

**Expected and acceptance criteria:** The design field `connectivity.client_cidrs` must satisfy the approved predicate (list_nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-04 — Corporate client CIDR — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-04
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `connectivity.client_cidrs` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-05 — Hub/spoke routing — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-05
```

**Expected and acceptance criteria:** The design field `connectivity.hub_spoke_plan` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-06 — Hub/spoke routing — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-06
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `connectivity.hub_spoke_plan` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-07 — VPN transit points — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-07
```

**Expected and acceptance criteria:** The design field `connectivity.vpn_hops` must satisfy the approved predicate (list_nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-08 — VPN transit points — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-08
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `connectivity.vpn_hops` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-09 — On-premises DNS forwarding — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-09
```

**Expected and acceptance criteria:** The design field `dns.onprem_forwarder_defined` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-10 — On-premises DNS forwarding — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-10
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `dns.onprem_forwarder_defined` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-11 — Conditional Access policy — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-11
```

**Expected and acceptance criteria:** The design field `identity.conditional_access_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-12 — Conditional Access policy — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-12
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `identity.conditional_access_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-13 — User connection authentication — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-13
```

**Expected and acceptance criteria:** The design field `connectivity.user_auth_method` must satisfy the approved predicate (enum). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-14 — User connection authentication — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-14
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `connectivity.user_auth_method` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-15 — Route advertisement and UDRs — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-15
```

**Expected and acceptance criteria:** The design field `routing.route_advertisements_reviewed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-16 — Route advertisement and UDRs — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-16
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `routing.route_advertisements_reviewed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-17 — Failover connection path — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-17
```

**Expected and acceptance criteria:** The design field `connectivity.failover_plan` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-18 — Failover connection path — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-18
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `connectivity.failover_plan` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-19 — Connectivity ownership — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-19
```

**Expected and acceptance criteria:** The design field `connectivity.raci` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-20 — Connectivity ownership — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-20
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `connectivity.raci` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-21 — Approved topology — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T02-21
```

**Expected and acceptance criteria:** The design field `connectivity.topology_approved` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T02-22 — Approved topology — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T02-22
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `connectivity.topology_approved` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

## Step 03: Security and regulatory controls

**Traceability:** AZ-T03-01 through AZ-T03-22 (22 IDs, 11 controls).

### AZ-T03-01 — Data classification — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-01
```

**Expected and acceptance criteria:** The design field `governance.data_classification` must satisfy the approved predicate (enum). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-02 — Data classification — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-02
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `governance.data_classification` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-03 — Storage and processing region — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-03
```

**Expected and acceptance criteria:** The design field `governance.allowed_regions` must satisfy the approved predicate (list_nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-04 — Storage and processing region — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-04
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `governance.allowed_regions` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-05 — Recovery time objective — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-05
```

**Expected and acceptance criteria:** The design field `continuity.rto_minutes` must satisfy the approved predicate (positive). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-06 — Recovery time objective — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-06
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `continuity.rto_minutes` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-07 — Recovery point objective — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-07
```

**Expected and acceptance criteria:** The design field `continuity.rpo_minutes` must satisfy the approved predicate (positive). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-08 — Recovery point objective — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-08
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `continuity.rpo_minutes` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-09 — Backup accountability — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-09
```

**Expected and acceptance criteria:** The design field `continuity.backup_owner` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-10 — Backup accountability — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-10
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `continuity.backup_owner` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-11 — Audit log retention — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-11
```

**Expected and acceptance criteria:** The design field `logging.retention_days` must satisfy the approved predicate (positive). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-12 — Audit log retention — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-12
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `logging.retention_days` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-13 — Key management owner — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-13
```

**Expected and acceptance criteria:** The design field `keys.management_owner` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-14 — Key management owner — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-14
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `keys.management_owner` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-15 — PIM elevation policy — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-15
```

**Expected and acceptance criteria:** The design field `identity.pim_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-16 — PIM elevation policy — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-16
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `identity.pim_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-17 — Change approval workflow — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-17
```

**Expected and acceptance criteria:** The design field `change_control.approval_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-18 — Change approval workflow — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-18
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `change_control.approval_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-19 — Regulatory control mapping — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-19
```

**Expected and acceptance criteria:** The design field `governance.compliance_mapping_reviewed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-20 — Regulatory control mapping — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-20
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `governance.compliance_mapping_reviewed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-21 — Owner of unresolved decisions — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T03-21
```

**Expected and acceptance criteria:** The design field `governance.open_items_have_owners` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T03-22 — Owner of unresolved decisions — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T03-22
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `governance.open_items_have_owners` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

## Step 04: Service availability and quota

**Traceability:** AZ-T04-01 through AZ-T04-22 (22 IDs, 11 controls).

### AZ-T04-01 — Azure OpenAI regional availability — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-01
```

**Expected and acceptance criteria:** The design field `availability.openai_region_confirmed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-02 — Azure OpenAI regional availability — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-02
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.openai_region_confirmed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-03 — Azure OpenAI model version — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-03
```

**Expected and acceptance criteria:** The design field `availability.openai_model_version_confirmed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-04 — Azure OpenAI model version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-04
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.openai_model_version_confirmed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-05 — Model deployment quota — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-05
```

**Expected and acceptance criteria:** The design field `availability.openai_quota_confirmed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-06 — Model deployment quota — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-06
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.openai_quota_confirmed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-07 — AI Search SKU — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-07
```

**Expected and acceptance criteria:** The design field `availability.search_sku_selected` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-08 — AI Search SKU — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-08
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.search_sku_selected` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-09 — AI Search private endpoint availability — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-09
```

**Expected and acceptance criteria:** The design field `availability.search_private_endpoint_confirmed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-10 — AI Search private endpoint availability — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-10
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.search_private_endpoint_confirmed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-11 — Cosmos DB NoSQL availability — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-11
```

**Expected and acceptance criteria:** The design field `availability.cosmos_nosql_supported` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-12 — Cosmos DB NoSQL availability — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-12
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.cosmos_nosql_supported` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-13 — Application Gateway WAF_v2 availability — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-13
```

**Expected and acceptance criteria:** The design field `availability.application_gateway_wafv2_supported` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-14 — Application Gateway WAF_v2 availability — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-14
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.application_gateway_wafv2_supported` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-15 — Key Vault Private Link support — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-15
```

**Expected and acceptance criteria:** The design field `availability.key_vault_private_link_supported` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-16 — Key Vault Private Link support — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-16
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.key_vault_private_link_supported` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-17 — Log Analytics location — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-17
```

**Expected and acceptance criteria:** The design field `availability.log_analytics_region_confirmed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-18 — Log Analytics location — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-18
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.log_analytics_region_confirmed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-19 — Alternate region implications — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-19
```

**Expected and acceptance criteria:** The design field `availability.alternative_region_impact_recorded` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-20 — Alternate region implications — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-20
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.alternative_region_impact_recorded` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-21 — Capacity and cost approval — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T04-21
```

**Expected and acceptance criteria:** The design field `availability.capacity_cost_approved` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T04-22 — Capacity and cost approval — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T04-22
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `availability.capacity_cost_approved` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

## Step 05: AI data handling

**Traceability:** AZ-T05-01 through AZ-T05-22 (22 IDs, 11 controls).

### AZ-T05-01 — No secret prompts in logs — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-01
```

**Expected and acceptance criteria:** The design field `ai_data.prompt_secret_logging_prohibited` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-02 — No secret prompts in logs — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-02
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.prompt_secret_logging_prohibited` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-03 — Inference output logging policy — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-03
```

**Expected and acceptance criteria:** The design field `ai_data.response_logging_policy_approved` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-04 — Inference output logging policy — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-04
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.response_logging_policy_approved` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-05 — Azure OpenAI processing geography — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-05
```

**Expected and acceptance criteria:** The design field `ai_data.processing_region_confirmed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-06 — Azure OpenAI processing geography — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-06
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.processing_region_confirmed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-07 — Abuse monitoring policy — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-07
```

**Expected and acceptance criteria:** The design field `ai_data.abuse_monitoring_policy_reviewed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-08 — Abuse monitoring policy — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-08
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.abuse_monitoring_policy_reviewed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-09 — Pinned model version — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-09
```

**Expected and acceptance criteria:** The design field `ai_data.model_version_pinning_policy` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-10 — Pinned model version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-10
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.model_version_pinning_policy` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-11 — Data retention period — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-11
```

**Expected and acceptance criteria:** The design field `ai_data.retention_days` must satisfy the approved predicate (positive). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-12 — Data retention period — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-12
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.retention_days` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-13 — Audit access roles — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-13
```

**Expected and acceptance criteria:** The design field `ai_data.audit_access_least_privilege` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-14 — Audit access roles — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-14
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.audit_access_least_privilege` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-15 — Data subject handling — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-15
```

**Expected and acceptance criteria:** The design field `ai_data.data_subject_handling_documented` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-16 — Data subject handling — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-16
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.data_subject_handling_documented` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-17 — Anonymized test datasets — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-17
```

**Expected and acceptance criteria:** The design field `ai_data.test_data_anonymization_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-18 — Anonymized test datasets — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-18
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.test_data_anonymization_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-19 — Incident audit trail — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-19
```

**Expected and acceptance criteria:** The design field `ai_data.incident_audit_trail_defined` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-20 — Incident audit trail — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-20
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.incident_audit_trail_defined` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-21 — Legal and application signoff — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T05-21
```

**Expected and acceptance criteria:** The design field `ai_data.legal_app_dual_approval` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T05-22 — Legal and application signoff — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T05-22
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `ai_data.legal_app_dual_approval` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

## Step 06: Developer workstation prerequisites

**Traceability:** AZ-T06-01 through AZ-T06-22 (22 IDs, 11 controls).

### AZ-T06-01 — WSL2 enablement — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-01
```

**Expected and acceptance criteria:** The design field `local_environment.wsl2_enabled` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-02 — WSL2 enablement — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-02
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.wsl2_enabled` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-03 — Ubuntu release — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-03
```

**Expected and acceptance criteria:** The design field `local_environment.ubuntu_release` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-04 — Ubuntu release — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-04
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.ubuntu_release` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-05 — Git version — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-05
```

**Expected and acceptance criteria:** The design field `local_environment.git_version` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-06 — Git version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-06
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.git_version` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-07 — Terraform CLI version — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-07
```

**Expected and acceptance criteria:** The design field `local_environment.terraform_version` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-08 — Terraform CLI version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-08
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.terraform_version` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-09 — jq availability — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-09
```

**Expected and acceptance criteria:** The design field `local_environment.jq_available` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-10 — jq availability — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-10
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.jq_available` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-11 — dig and nslookup availability — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-11
```

**Expected and acceptance criteria:** The design field `local_environment.dns_tools_available` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-12 — dig and nslookup availability — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-12
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.dns_tools_available` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-13 — Node.js version — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-13
```

**Expected and acceptance criteria:** The design field `local_environment.node_version` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-14 — Node.js version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-14
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.node_version` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-15 — npm version — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-15
```

**Expected and acceptance criteria:** The design field `local_environment.npm_version` must satisfy the approved predicate (nonempty). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-16 — npm version — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-16
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.npm_version` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-17 — Approved package sources — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-17
```

**Expected and acceptance criteria:** The design field `local_environment.package_sources_approved` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-18 — Approved package sources — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-18
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.package_sources_approved` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-19 — No local secret files — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-19
```

**Expected and acceptance criteria:** The design field `local_environment.secret_files_excluded` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-20 — No local secret files — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-20
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.secret_files_excluded` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-21 — Workstation identity record — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T06-21
```

**Expected and acceptance criteria:** The design field `local_environment.endpoint_identified` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T06-22 — Workstation identity record — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T06-22
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `local_environment.endpoint_identified` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

## Step 07: Identity and administrative access path

**Traceability:** AZ-T07-01 through AZ-T07-22 (22 IDs, 11 controls).

### AZ-T07-01 — Azure Portal access path — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-01
```

**Expected and acceptance criteria:** The design field `auth_strategy.portal_via_zscaler` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-02 — Azure Portal access path — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-02
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.portal_via_zscaler` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-03 — Zscaler enforcement — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-03
```

**Expected and acceptance criteria:** The design field `auth_strategy.zscaler_controls_documented` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-04 — Zscaler enforcement — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-04
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.zscaler_controls_documented` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-05 — Fixed endpoint restrictions — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-05
```

**Expected and acceptance criteria:** The design field `auth_strategy.fixed_endpoint_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-06 — Fixed endpoint restrictions — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-06
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.fixed_endpoint_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-07 — CI OIDC setup — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-07
```

**Expected and acceptance criteria:** The design field `auth_strategy.ci_oidc_enabled` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-08 — CI OIDC setup — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-08
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.ci_oidc_enabled` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-09 — Federated credential scope — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-09
```

**Expected and acceptance criteria:** The design field `auth_strategy.federated_subject_approved` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-10 — Federated credential scope — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-10
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.federated_subject_approved` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-11 — CI principal ID — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-11
```

**Expected and acceptance criteria:** The design field `auth_strategy.ci_principal_id_recorded` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-12 — CI principal ID — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-12
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.ci_principal_id_recorded` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-13 — Least-privilege RBAC — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-13
```

**Expected and acceptance criteria:** The design field `auth_strategy.rbac_minimal_scope_reviewed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-14 — Least-privilege RBAC — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-14
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.rbac_minimal_scope_reviewed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-15 — PIM elevation workflow — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-15
```

**Expected and acceptance criteria:** The design field `auth_strategy.pim_procedure_approved` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-16 — PIM elevation workflow — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-16
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.pim_procedure_approved` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-17 — No long-lived secrets — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-17
```

**Expected and acceptance criteria:** The design field `auth_strategy.no_long_lived_secret` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-18 — No long-lived secrets — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-18
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.no_long_lived_secret` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-19 — CI audit trail — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-19
```

**Expected and acceptance criteria:** The design field `auth_strategy.ci_evidence_retained` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-20 — CI audit trail — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-20
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.ci_evidence_retained` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-21 — Break-glass accountability — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T07-21
```

**Expected and acceptance criteria:** The design field `auth_strategy.breakglass_raci_defined` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T07-22 — Break-glass accountability — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T07-22
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `auth_strategy.breakglass_raci_defined` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

## Step 08: Private Application Gateway feature registration

**Traceability:** AZ-T08-01 through AZ-T08-22 (22 IDs, 11 controls).

### AZ-T08-01 — Target subscription — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-01
```

**Expected and acceptance criteria:** The design field `network_isolation.subscription_confirmed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-02 — Target subscription — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-02
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.subscription_confirmed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-03 — Preview feature name — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-03
```

**Expected and acceptance criteria:** The design field `network_isolation.feature_name_confirmed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-04 — Preview feature name — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-04
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.feature_name_confirmed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-05 — Preview feature Registered status — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-05
```

**Expected and acceptance criteria:** The design field `network_isolation.feature_registered` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-06 — Preview feature Registered status — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-06
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.feature_registered` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-07 — Regional restrictions — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-07
```

**Expected and acceptance criteria:** The design field `network_isolation.region_eligibility_confirmed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-08 — Regional restrictions — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-08
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.region_eligibility_confirmed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-09 — Preview adoption approval — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-09
```

**Expected and acceptance criteria:** The design field `network_isolation.preview_adoption_approved` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-10 — Preview adoption approval — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-10
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.preview_adoption_approved` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-11 — Feature registrar identity — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-11
```

**Expected and acceptance criteria:** The design field `network_isolation.registration_operator_approved` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-12 — Feature registrar identity — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-12
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.registration_operator_approved` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-13 — Subnet delegation compatibility — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-13
```

**Expected and acceptance criteria:** The design field `network_isolation.delegation_compatibility_checked` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-14 — Subnet delegation compatibility — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-14
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.delegation_compatibility_checked` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-15 — GatewayManager rule compatibility — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-15
```

**Expected and acceptance criteria:** The design field `network_isolation.gateway_manager_rules_reviewed` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-16 — GatewayManager rule compatibility — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-16
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.gateway_manager_rules_reviewed` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-17 — Feature constraints recorded — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-17
```

**Expected and acceptance criteria:** The design field `network_isolation.feature_limitations_documented` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-18 — Feature constraints recorded — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-18
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.feature_limitations_documented` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-19 — Feature change history — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-19
```

**Expected and acceptance criteria:** The design field `network_isolation.change_history_recorded` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-20 — Feature change history — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-20
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.change_history_recorded` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-21 — Registration evidence — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T08-21
```

**Expected and acceptance criteria:** The design field `network_isolation.registration_evidence_present` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T08-22 — Registration evidence — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T08-22
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `network_isolation.registration_evidence_present` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

## Step 09: Git repository layout

**Traceability:** AZ-T09-01 through AZ-T09-22 (22 IDs, 11 controls).

### AZ-T09-01 — Repository initialization — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-01
```

**Expected and acceptance criteria:** The design field `repo.initialized` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-02 — Repository initialization — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-02
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.initialized` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-03 — bootstrap directory — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-03
```

**Expected and acceptance criteria:** The design field `repo.bootstrap_present` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-04 — bootstrap directory — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-04
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.bootstrap_present` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-05 — infra/modules directory — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-05
```

**Expected and acceptance criteria:** The design field `repo.modules_present` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-06 — infra/modules directory — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-06
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.modules_present` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-07 — infra/environments directory — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-07
```

**Expected and acceptance criteria:** The design field `repo.environments_present` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-08 — infra/environments directory — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-08
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.environments_present` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-09 — policy/tests directory — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-09
```

**Expected and acceptance criteria:** The design field `repo.policy_tests_present` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-10 — policy/tests directory — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-10
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.policy_tests_present` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-11 — tests/external directory — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-11
```

**Expected and acceptance criteria:** The design field `repo.external_tests_present` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-12 — tests/external directory — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-12
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.external_tests_present` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-13 — tests/internal directory — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-13
```

**Expected and acceptance criteria:** The design field `repo.internal_tests_present` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-14 — tests/internal directory — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-14
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.internal_tests_present` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-15 — scripts directory — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-15
```

**Expected and acceptance criteria:** The design field `repo.scripts_present` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-16 — scripts directory — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-16
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.scripts_present` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-17 — docs directory — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-17
```

**Expected and acceptance criteria:** The design field `repo.docs_present` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-18 — docs directory — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-18
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.docs_present` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-19 — Protected branch — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-19
```

**Expected and acceptance criteria:** The design field `repo.protected_branch_enabled` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-20 — Protected branch — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-20
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.protected_branch_enabled` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-21 — Two-reviewer rule — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T09-21
```

**Expected and acceptance criteria:** The design field `repo.two_reviewers_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T09-22 — Two-reviewer rule — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T09-22
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo.two_reviewers_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

## Step 10: Secret exclusion and commit hygiene

**Traceability:** AZ-T10-01 through AZ-T10-22 (22 IDs, 11 controls).

### AZ-T10-01 — Exclude Terraform state — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-01
```

**Expected and acceptance criteria:** The design field `repo_ignore.tfstate` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-02 — Exclude Terraform state — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-02
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.tfstate` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-03 — Exclude Terraform plan files — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-03
```

**Expected and acceptance criteria:** The design field `repo_ignore.tfplan` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-04 — Exclude Terraform plan files — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-04
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.tfplan` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-05 — Exclude .env files — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-05
```

**Expected and acceptance criteria:** The design field `repo_ignore.dotenv` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-06 — Exclude .env files — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-06
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.dotenv` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-07 — Exclude PEM keys — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-07
```

**Expected and acceptance criteria:** The design field `repo_ignore.pem` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-08 — Exclude PEM keys — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-08
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.pem` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-09 — Exclude PFX files — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-09
```

**Expected and acceptance criteria:** The design field `repo_ignore.pfx` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-10 — Exclude PFX files — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-10
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.pfx` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-11 — Exclude private key files — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-11
```

**Expected and acceptance criteria:** The design field `repo_ignore.key` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-12 — Exclude private key files — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-12
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.key` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-13 — Exclude node_modules — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-13
```

**Expected and acceptance criteria:** The design field `repo_ignore.node_modules` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-14 — Exclude node_modules — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-14
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.node_modules` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-15 — Exclude Playwright traces — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-15
```

**Expected and acceptance criteria:** The design field `repo_ignore.playwright_trace` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-16 — Exclude Playwright traces — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-16
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.playwright_trace` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-17 — Secret scanning — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-17
```

**Expected and acceptance criteria:** The design field `repo_ignore.secret_scanning_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-18 — Secret scanning — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-18
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.secret_scanning_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-19 — Git history contamination — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-19
```

**Expected and acceptance criteria:** The design field `repo_ignore.history_scanned` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-20 — Git history contamination — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-20
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.history_scanned` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-21 — Redacted audit evidence — Positive Review

**Execution:** `DESIGN_REVIEW`; **current acceptance:** `NOT_READY`.

**Preconditions:** Organization-approved baseline JSON, non-synthetic; design schema adopted and reviewed

**Procedure:**
1. Confirm approved source revision, scope, asset existence, baseline and operator.
2. Run the read-only command only in its designated authorized environment; WSL cannot be used for Azure login.
3. Compare the observed property or field to the expected predicate and check supporting independent evidence.
4. Assign NOT_READY/FAIL/REVIEW_REQUIRED; live PASS requires authorized execution and independent acceptance.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --baseline "$APPROVED_BASELINE_JSON" --test-id AZ-T10-21
```

**Expected and acceptance criteria:** The design field `repo_ignore.audit_redaction_required` must satisfy the approved predicate (eq). A matching local document returns REVIEW_REQUIRED, never Azure PASS.

**Required evidence:** Capture sanitized raw output, source SHA-256, UTC collection time, runner identity, scoped asset ID, expected criterion, and reviewer decision. Evidence and authorization must be independently reviewed.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema

### AZ-T10-22 — Redacted audit evidence — Offline Deviation Detection

**Execution:** `OFFLINE_DETECTOR`; **current acceptance:** `NOT_READY`.

**Preconditions:** This package only; synthetic fixture generated in memory

**Procedure:**
1. Work only with a synthetic copy of the input or a mock plan.
2. Run the case-specific detector self-test without calling Azure.
3. Confirm prohibited values yield FAIL, absent values yield NOT_READY and synthetic test results never count as Azure PASS.
4. Preserve sanitized fixture hashes and regression log.

**Command (review before any non-offline execution):**
```bash
python3 scripts/phase1_policy_check.py --rules specs/phase1_policies_110.json --selftest --test-id AZ-T10-22
```

**Expected and acceptance criteria:** Synthetic good/bad/missing fixtures for `repo_ignore.audit_redaction_required` must classify PASS/FAIL/NOT_READY respectively. These are detector-only results.

**Required evidence:** Offline JSON fixture results, exact control ID, policy SHA-256 and synthetic marker; no live acceptance credit.

**Failure / NotReady handling:** If prerequisites or evidence are missing, record NOT_READY; if an approved observation contradicts the control, record FAIL. Investigate ownership, source version, scope and policy without changing production.

**Source lineage:** Phase 9 corrected Phase 1 JSON and 110-control policy schema
