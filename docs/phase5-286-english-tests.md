# Phase 5 — English Detailed Test Procedures (Steps 46–58, 286 Cases)

**Status:** Design-only, Azure live passes **0**. This document preserves the original IDs, not evidence of deployment.
**Source:** previously archived Phase5 286-case specification; SHA-256: `e1a24b145ec7bdd66f3cbe123644e9f060354c7d1aa8d93c193214122d346de3`.

Every step has 11 paired controls (configuration/evidence review plus synthetic negative detector).
Azure queries below are **examples for a separately authorized CI runner**, not commands to execute from the restricted user workstation.
Never run Terraform `apply`, mutation/intrusion/load tests or `az login` as part of this offline documentation package.
An offline detector result must never count as an Azure control PASS. Source code, approved baseline, target Azure resources and independent acceptance evidence are currently unavailable.

## Mandatory environment variables and guardrails

- `$RG`, `$PLAN_NAME`, `$WEBAPP_NAME`, `$APPGW_NAME`, `$WAF_POLICY_NAME` and other names are **nonsecret placeholders** supplied by the approved execution configuration.
- `$APP_BASELINE` and other evidence paths must point to signed, restricted-access inventories; absence is NOT_READY.
- A `jq` truthy/field check or shell `test -s` cannot by itself establish security compliance.
- Private DNS/address results must be matched to the exact PE NIC and approved subnet, not merely any RFC1918 address.
- Some queries and attribute names depend on the actual CLI/API/Terraform version; verify before formal adoption.

## Detailed test cases

## Step 46: App Service Plan selection and capacity

Test ID range: `AZ-T46-01` to `AZ-T46-22`.

### AZ-T46-01 — Linux service plan (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az appservice plan show -g "$RG" -n "$PLAN_NAME" --query "{kind:kind,reserved:reserved,sku:sku.name}" -o json
```

**Expected result:** The target plan is Linux-compatible and matches the approved plan ID and SKU; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** The plan is a Windows-only plan or does not match inventory

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az appservice plan show -g "$RG" -n "$PLAN_NAME" --query "{kind:kind,reserved:reserved,sku:sku.name}" -o json
4. Check the actual observation against the signed criterion: The target plan is Linux-compatible and matches the approved plan ID and SKU.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-02 — Linux service plan (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** The plan is a Windows-only plan or does not match inventory

**Procedure:**

1. Use paired positive control AZ-T46-01 (Linux service plan).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-03 — Premium service plan tier (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az appservice plan show -g "$RG" -n "$PLAN_NAME" --query sku.name -o tsv
```

**Expected result:** The selected plan tier meets approved production availability requirements; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** The service tier is below the approved minimum

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az appservice plan show -g "$RG" -n "$PLAN_NAME" --query sku.name -o tsv
4. Check the actual observation against the signed criterion: The selected plan tier meets approved production availability requirements.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-04 — Premium service plan tier (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** The service tier is below the approved minimum

**Procedure:**

1. Use paired positive control AZ-T46-03 (Premium service plan tier).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-05 — Worker instance count (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az appservice plan show -g "$RG" -n "$PLAN_NAME" --query sku.capacity -o tsv
```

**Expected result:** Worker count is at or above the signed HA baseline; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Worker count is below the required minimum

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az appservice plan show -g "$RG" -n "$PLAN_NAME" --query sku.capacity -o tsv
4. Check the actual observation against the signed criterion: Worker count is at or above the signed HA baseline.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-06 — Worker instance count (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Worker count is below the required minimum

**Procedure:**

1. Use paired positive control AZ-T46-05 (Worker instance count).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-07 — Availability-zone redundancy (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az appservice plan show -g "$RG" -n "$PLAN_NAME" --query zoneRedundant -o tsv
```

**Expected result:** Zone redundancy configuration matches a region-supported, approved design; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** The requested zone redundancy is absent or unsupported

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az appservice plan show -g "$RG" -n "$PLAN_NAME" --query zoneRedundant -o tsv
4. Check the actual observation against the signed criterion: Zone redundancy configuration matches a region-supported, approved design.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-08 — Availability-zone redundancy (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** The requested zone redundancy is absent or unsupported

**Procedure:**

1. Use paired positive control AZ-T46-07 (Availability-zone redundancy).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-09 — Autoscale policy bounds (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az monitor autoscale list -g "$RG" -o json
```

**Expected result:** Autoscale rules, capacity ceiling and floor match approved limits; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Autoscale is disabled or outside approved limits

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az monitor autoscale list -g "$RG" -o json
4. Check the actual observation against the signed criterion: Autoscale rules, capacity ceiling and floor match approved limits.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-10 — Autoscale policy bounds (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Autoscale is disabled or outside approved limits

**Procedure:**

1. Use paired positive control AZ-T46-09 (Autoscale policy bounds).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-11 — SLA and resilience requirements (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/appservice/sla-requirements.json && jq -e '.rto and .rpo and .availability_target' docs/appservice/sla-requirements.json
```

**Expected result:** Signed SLA, RTO, and RPO requirements are traceable to the chosen plan; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** A documented SLA or recovery objective is missing

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/appservice/sla-requirements.json && jq -e '.rto and .rpo and .availability_target' docs/appservice/sla-requirements.json
4. Check the actual observation against the signed criterion: Signed SLA, RTO, and RPO requirements are traceable to the chosen plan.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-12 — SLA and resilience requirements (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** A documented SLA or recovery objective is missing

**Procedure:**

1. Use paired positive control AZ-T46-11 (SLA and resilience requirements).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-13 — CPU and worker quota (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az appservice plan show -g "$RG" -n "$PLAN_NAME" --query "{sku:sku,numberOfWorkers:numberOfWorkers}" -o json
```

**Expected result:** Available CPU/worker capacity meets reviewed workload requirements; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Worker capacity cannot meet the workload

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az appservice plan show -g "$RG" -n "$PLAN_NAME" --query "{sku:sku,numberOfWorkers:numberOfWorkers}" -o json
4. Check the actual observation against the signed criterion: Available CPU/worker capacity meets reviewed workload requirements.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-14 — CPU and worker quota (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Worker capacity cannot meet the workload

**Procedure:**

1. Use paired positive control AZ-T46-13 (CPU and worker quota).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-15 — Memory capacity baseline (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az appservice plan show -g "$RG" -n "$PLAN_NAME" --query "{sku:sku,maximumNumberOfWorkers:maximumNumberOfWorkers}" -o json
```

**Expected result:** Approved per-worker memory demand fits the selected SKU; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** The selected SKU is undersized

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az appservice plan show -g "$RG" -n "$PLAN_NAME" --query "{sku:sku,maximumNumberOfWorkers:maximumNumberOfWorkers}" -o json
4. Check the actual observation against the signed criterion: Approved per-worker memory demand fits the selected SKU.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-16 — Memory capacity baseline (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** The selected SKU is undersized

**Procedure:**

1. Use paired positive control AZ-T46-15 (Memory capacity baseline).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-17 — Reviewed cost estimate (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/cost/appservice-plan.json && jq -e '.approved == true and .currency' evidence/cost/appservice-plan.json
```

**Expected result:** A dated cost estimate and change approval cover the selected plan; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Forecast cost exceeds the approved budget or lacks approval

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/cost/appservice-plan.json && jq -e '.approved == true and .currency' evidence/cost/appservice-plan.json
4. Check the actual observation against the signed criterion: A dated cost estimate and change approval cover the selected plan.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-18 — Reviewed cost estimate (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Forecast cost exceeds the approved budget or lacks approval

**Procedure:**

1. Use paired positive control AZ-T46-17 (Reviewed cost estimate).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-19 — Controlled scale-out evidence (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/load/scale-out.json && jq -e '.result == "Pass" and .p95_ms and .concurrency' evidence/load/scale-out.json
```

**Expected result:** A sanctioned load exercise demonstrates the agreed scale-out SLO; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Scaling evidence is missing or thresholds are breached

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/load/scale-out.json && jq -e '.result == "Pass" and .p95_ms and .concurrency' evidence/load/scale-out.json
4. Check the actual observation against the signed criterion: A sanctioned load exercise demonstrates the agreed scale-out SLO.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-20 — Controlled scale-out evidence (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Scaling evidence is missing or thresholds are breached

**Procedure:**

1. Use paired positive control AZ-T46-19 (Controlled scale-out evidence).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-21 — HA design signoff (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/appservice/ha-approval.json && jq -e '.reviewer and .approved == true' docs/appservice/ha-approval.json
```

**Expected result:** An independent reviewer accepted the precise HA design revision; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** The approval or owner does not exist

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 46.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/appservice/ha-approval.json && jq -e '.reviewer and .approved == true' docs/appservice/ha-approval.json
4. Check the actual observation against the signed criterion: An independent reviewer accepted the precise HA design revision.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T46-22 — HA design signoff (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T46-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** The approval or owner does not exist

**Procedure:**

1. Use paired positive control AZ-T46-21 (HA design signoff).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T46-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 47: Linux Web App security configuration

Test ID range: `AZ-T47-01` to `AZ-T47-22`.

### AZ-T47-01 — HTTPS-only application ingress (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp show -g "$RG" -n "$WEBAPP_NAME" --query httpsOnly -o tsv
```

**Expected result:** The scoped Web App property httpsOnly is true; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** HTTP application ingress remains enabled

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp show -g "$RG" -n "$WEBAPP_NAME" --query httpsOnly -o tsv
4. Check the actual observation against the signed criterion: The scoped Web App property httpsOnly is true.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-02 — HTTPS-only application ingress (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** HTTP application ingress remains enabled

**Procedure:**

1. Use paired positive control AZ-T47-01 (HTTPS-only application ingress).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-03 — Public network access disabled (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp show -g "$RG" -n "$WEBAPP_NAME" --query publicNetworkAccess -o tsv
```

**Expected result:** The Web App public data-plane access is disabled; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Public network access is Enabled

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp show -g "$RG" -n "$WEBAPP_NAME" --query publicNetworkAccess -o tsv
4. Check the actual observation against the signed criterion: The Web App public data-plane access is disabled.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-04 — Public network access disabled (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Public network access is Enabled

**Procedure:**

1. Use paired positive control AZ-T47-03 (Public network access disabled).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-05 — Minimum TLS version (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query minTlsVersion -o tsv
```

**Expected result:** TLS minimum satisfies the signed organization requirement; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** An obsolete or unapproved TLS minimum is configured

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query minTlsVersion -o tsv
4. Check the actual observation against the signed criterion: TLS minimum satisfies the signed organization requirement.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-06 — Minimum TLS version (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** An obsolete or unapproved TLS minimum is configured

**Procedure:**

1. Use paired positive control AZ-T47-05 (Minimum TLS version).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-07 — FTP and FTPS disabled (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query ftpsState -o tsv
```

**Expected result:** FTPS state follows the approved complete-disable requirement; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** FTP/FTPS remains permitted without a waiver

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query ftpsState -o tsv
4. Check the actual observation against the signed criterion: FTPS state follows the approved complete-disable requirement.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-08 — FTP and FTPS disabled (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** FTP/FTPS remains permitted without a waiver

**Procedure:**

1. Use paired positive control AZ-T47-07 (FTP and FTPS disabled).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-09 — Basic publishing credentials disabled (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az resource show --ids "$WEBAPP_ID" --api-version "$WEB_API_VERSION" --query "properties.siteConfig" -o json
```

**Expected result:** Both relevant basic publishing credential policies are disabled; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** FTP or SCM basic authentication remains enabled

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az resource show --ids "$WEBAPP_ID" --api-version "$WEB_API_VERSION" --query "properties.siteConfig" -o json
4. Check the actual observation against the signed criterion: Both relevant basic publishing credential policies are disabled.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-10 — Basic publishing credentials disabled (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** FTP or SCM basic authentication remains enabled

**Procedure:**

1. Use paired positive control AZ-T47-09 (Basic publishing credentials disabled).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-11 — Assigned managed identity (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp identity show -g "$RG" -n "$WEBAPP_NAME" -o json
```

**Expected result:** Managed identity type, principal ID and RBAC mapping match source inventory; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** An unexpected identity is attached

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp identity show -g "$RG" -n "$WEBAPP_NAME" -o json
4. Check the actual observation against the signed criterion: Managed identity type, principal ID and RBAC mapping match source inventory.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-12 — Assigned managed identity (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** An unexpected identity is attached

**Procedure:**

1. Use paired positive control AZ-T47-11 (Assigned managed identity).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-13 — Health check configuration (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query healthCheckPath -o tsv
```

**Expected result:** The app health check path and response behavior match the agreed probe; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Health check path is absent or nonfunctional

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query healthCheckPath -o tsv
4. Check the actual observation against the signed criterion: The app health check path and response behavior match the agreed probe.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-14 — Health check configuration (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Health check path is absent or nonfunctional

**Procedure:**

1. Use paired positive control AZ-T47-13 (Health check configuration).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-15 — Always On decision (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query alwaysOn -o tsv
```

**Expected result:** The approved availability plan explicitly accepts or rejects Always On; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** The setting is unreviewed or inconsistent

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query alwaysOn -o tsv
4. Check the actual observation against the signed criterion: The approved availability plan explicitly accepts or rejects Always On.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-16 — Always On decision (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** The setting is unreviewed or inconsistent

**Procedure:**

1. Use paired positive control AZ-T47-15 (Always On decision).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-17 — Remote debugging disabled (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query remoteDebuggingEnabled -o tsv
```

**Expected result:** Remote debugging is disabled in the production baseline; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Remote debugging is enabled

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query remoteDebuggingEnabled -o tsv
4. Check the actual observation against the signed criterion: Remote debugging is disabled in the production baseline.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-18 — Remote debugging disabled (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Remote debugging is enabled

**Procedure:**

1. Use paired positive control AZ-T47-17 (Remote debugging disabled).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-19 — Deployment slot boundary (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp deployment slot list -g "$RG" -n "$WEBAPP_NAME" -o json
```

**Expected result:** Each adopted deployment slot follows its own approved network and RBAC boundary; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** A slot exposes an unintended public entry point

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp deployment slot list -g "$RG" -n "$WEBAPP_NAME" -o json
4. Check the actual observation against the signed criterion: Each adopted deployment slot follows its own approved network and RBAC boundary.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-20 — Deployment slot boundary (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** A slot exposes an unintended public entry point

**Procedure:**

1. Use paired positive control AZ-T47-19 (Deployment slot boundary).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-21 — Post-deployment drift check (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved isolated read-only CI with explicit state access (never run on restricted WSL)

**Command:**

```bash
terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
```

**Expected result:** A scoped, approved, read-only drift assessment returns exit code 0; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Unreviewed infrastructure drift is present

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 47.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
4. Check the actual observation against the signed criterion: A scoped, approved, read-only drift assessment returns exit code 0.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory. A refresh-only plan may contact cloud services, read state and change lock state; it is not executed here.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T47-22 — Post-deployment drift check (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T47-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Unreviewed infrastructure drift is present

**Procedure:**

1. Use paired positive control AZ-T47-21 (Post-deployment drift check).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T47-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 48: Canonical service FQDN and private name resolution

Test ID range: `AZ-T48-01` to `AZ-T48-22`.

### AZ-T48-01 — Canonical OpenAI hostname (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
jq -r ".endpoints.openai" "$APP_BASELINE"
```

**Expected result:** Azure OpenAI uses the intended canonical service hostname rather than a raw Private Link target; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** The application targets an incorrect or privately aliased name directly

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: jq -r ".endpoints.openai" "$APP_BASELINE"
4. Check the actual observation against the signed criterion: Azure OpenAI uses the intended canonical service hostname rather than a raw Private Link target.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-02 — Canonical OpenAI hostname (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** The application targets an incorrect or privately aliased name directly

**Procedure:**

1. Use paired positive control AZ-T48-01 (Canonical OpenAI hostname).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-03 — Canonical Search hostname (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
jq -r ".endpoints.search" "$APP_BASELINE"
```

**Expected result:** Search connects using the approved *.search.windows.net service hostname; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** The configured Search host is wrong

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: jq -r ".endpoints.search" "$APP_BASELINE"
4. Check the actual observation against the signed criterion: Search connects using the approved *.search.windows.net service hostname.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-04 — Canonical Search hostname (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** The configured Search host is wrong

**Procedure:**

1. Use paired positive control AZ-T48-03 (Canonical Search hostname).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-05 — Canonical Cosmos hostname (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
jq -r ".endpoints.cosmos" "$APP_BASELINE"
```

**Expected result:** Cosmos connects using the approved *.documents.azure.com service hostname; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** The Cosmos hostname is unapproved

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: jq -r ".endpoints.cosmos" "$APP_BASELINE"
4. Check the actual observation against the signed criterion: Cosmos connects using the approved *.documents.azure.com service hostname.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-06 — Canonical Cosmos hostname (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** The Cosmos hostname is unapproved

**Procedure:**

1. Use paired positive control AZ-T48-05 (Canonical Cosmos hostname).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-07 — Private DNS resolution chain (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved VNet-connected internal test runner; never public workstation

**Command:**

```bash
dig +short "$OPENAI_FQDN" A && dig +short "$SEARCH_FQDN" A && dig +short "$COSMOS_FQDN" A
```

**Expected result:** From an approved internal runner all canonical names resolve to approved PE IPs; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** A hostname resolves publicly or to an unexpected private IP

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: dig +short "$OPENAI_FQDN" A && dig +short "$SEARCH_FQDN" A && dig +short "$COSMOS_FQDN" A
4. Check the actual observation against the signed criterion: From an approved internal runner all canonical names resolve to approved PE IPs.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-08 — Private DNS resolution chain (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** A hostname resolves publicly or to an unexpected private IP

**Procedure:**

1. Use paired positive control AZ-T48-07 (Private DNS resolution chain).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-09 — TLS SNI and certificate verification (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved VNet-connected internal test runner; never public workstation

**Command:**

```bash
openssl s_client -connect "${OPENAI_FQDN}:443" -servername "$OPENAI_FQDN" -verify_return_error </dev/null
```

**Expected result:** TLS handshake succeeds with the canonical hostname and certificate verification; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** SNI/hostname verification fails

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: openssl s_client -connect "${OPENAI_FQDN}:443" -servername "$OPENAI_FQDN" -verify_return_error </dev/null
4. Check the actual observation against the signed criterion: TLS handshake succeeds with the canonical hostname and certificate verification.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-10 — TLS SNI and certificate verification (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** SNI/hostname verification fails

**Procedure:**

1. Use paired positive control AZ-T48-09 (TLS SNI and certificate verification).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-11 — HTTPS URI scheme (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
jq -e '.endpoints | to_entries | all(.value | startswith("https://"))' "$APP_BASELINE"
```

**Expected result:** Configured service endpoint URIs are valid HTTPS URLs; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** A service URL uses HTTP or an invalid URI

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: jq -e '.endpoints | to_entries | all(.value | startswith("https://"))' "$APP_BASELINE"
4. Check the actual observation against the signed criterion: Configured service endpoint URIs are valid HTTPS URLs.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-12 — HTTPS URI scheme (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** A service URL uses HTTP or an invalid URI

**Procedure:**

1. Use paired positive control AZ-T48-11 (HTTPS URI scheme).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-13 — Configuration provenance (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
jq -e '.configuration.source and .configuration.version' "$APP_BASELINE"
```

**Expected result:** Application endpoint settings are pinned to an approved revision; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Configuration origin or revision is untracked

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: jq -e '.configuration.source and .configuration.version' "$APP_BASELINE"
4. Check the actual observation against the signed criterion: Application endpoint settings are pinned to an approved revision.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-14 — Configuration provenance (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Configuration origin or revision is untracked

**Procedure:**

1. Use paired positive control AZ-T48-13 (Configuration provenance).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-15 — No plaintext API keys (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/security/appsettings-scan.json && jq -e '.raw_api_keys_found == 0 and .plaintext_passwords_found == 0' evidence/security/appsettings-scan.json
```

**Expected result:** Confidential credentials are not present in app settings or logs; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Plaintext API keys remain in application configuration

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/security/appsettings-scan.json && jq -e '.raw_api_keys_found == 0 and .plaintext_passwords_found == 0' evidence/security/appsettings-scan.json
4. Check the actual observation against the signed criterion: Confidential credentials are not present in app settings or logs.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-16 — No plaintext API keys (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Plaintext API keys remain in application configuration

**Procedure:**

1. Use paired positive control AZ-T48-15 (No plaintext API keys).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-17 — DNS failure diagnosis (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/dependency-dns.json && jq -e '.status == "Pass" and .runner_vnet' evidence/network/dependency-dns.json
```

**Expected result:** NXDOMAIN, timeouts, and incorrect A records are distinguished in evidence; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** DNS failure is misclassified as private network enforcement

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/dependency-dns.json && jq -e '.status == "Pass" and .runner_vnet' evidence/network/dependency-dns.json
4. Check the actual observation against the signed criterion: NXDOMAIN, timeouts, and incorrect A records are distinguished in evidence.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-18 — DNS failure diagnosis (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** DNS failure is misclassified as private network enforcement

**Procedure:**

1. Use paired positive control AZ-T48-17 (DNS failure diagnosis).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-19 — Authenticated service dependency smoke (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/app/dependency-smoke.json && jq -e '.openai == "Pass" and .search == "Pass" and .cosmos == "Pass"' evidence/app/dependency-smoke.json
```

**Expected result:** Private internal app-to-service calls succeed with approved identity; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** The dependency is inaccessible or authenticated incorrectly

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/app/dependency-smoke.json && jq -e '.openai == "Pass" and .search == "Pass" and .cosmos == "Pass"' evidence/app/dependency-smoke.json
4. Check the actual observation against the signed criterion: Private internal app-to-service calls succeed with approved identity.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-20 — Authenticated service dependency smoke (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** The dependency is inaccessible or authenticated incorrectly

**Procedure:**

1. Use paired positive control AZ-T48-19 (Authenticated service dependency smoke).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-21 — Sensitive payload redaction (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/logging/payload-redaction.json && jq -e '.secret_redaction == true and .personal_data_redaction == true' evidence/logging/payload-redaction.json
```

**Expected result:** Evidence shows prompt, credential and personal-data masking is effective; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Sensitive values leak into diagnostic telemetry

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 48.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/logging/payload-redaction.json && jq -e '.secret_redaction == true and .personal_data_redaction == true' evidence/logging/payload-redaction.json
4. Check the actual observation against the signed criterion: Evidence shows prompt, credential and personal-data masking is effective.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T48-22 — Sensitive payload redaction (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T48-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Sensitive values leak into diagnostic telemetry

**Procedure:**

1. Use paired positive control AZ-T48-21 (Sensitive payload redaction).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T48-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 49: App Service outbound VNet integration

Test ID range: `AZ-T49-01` to `AZ-T49-22`.

### AZ-T49-01 — Approved integration subnet (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp show -g "$RG" -n "$WEBAPP_NAME" --query virtualNetworkSubnetId -o tsv
```

**Expected result:** App Service outbound integration subnet ID matches signed network inventory; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** App Service is integrated with an unexpected subnet

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp show -g "$RG" -n "$WEBAPP_NAME" --query virtualNetworkSubnetId -o tsv
4. Check the actual observation against the signed criterion: App Service outbound integration subnet ID matches signed network inventory.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-02 — Approved integration subnet (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** App Service is integrated with an unexpected subnet

**Procedure:**

1. Use paired positive control AZ-T49-01 (Approved integration subnet).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-03 — Single Terraform ownership method (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -d infra && ! rg -q "azurerm_app_service_virtual_network_swift_connection" infra
```

**Expected result:** An approved single Terraform resource/property controls outbound VNet integration; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** A conflicting swift-connection resource manages the same integration

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -d infra && ! rg -q "azurerm_app_service_virtual_network_swift_connection" infra
4. Check the actual observation against the signed criterion: An approved single Terraform resource/property controls outbound VNet integration.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-04 — Single Terraform ownership method (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** A conflicting swift-connection resource manages the same integration

**Procedure:**

1. Use paired positive control AZ-T49-03 (Single Terraform ownership method).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-05 — Delegated integration subnet (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET_NAME" -n "$APP_SUBNET_NAME" --query delegations -o json
```

**Expected result:** The integration subnet delegates to Microsoft.Web/serverFarms; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Required delegation is missing

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network vnet subnet show -g "$RG" --vnet-name "$VNET_NAME" -n "$APP_SUBNET_NAME" --query delegations -o json
4. Check the actual observation against the signed criterion: The integration subnet delegates to Microsoft.Web/serverFarms.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-06 — Delegated integration subnet (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Required delegation is missing

**Procedure:**

1. Use paired positive control AZ-T49-05 (Delegated integration subnet).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-07 — Route All governance (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query vnetRouteAllEnabled -o tsv
```

**Expected result:** Outbound Route All behavior matches signed routing and DNS design; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Outbound traffic bypasses the approved route

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query vnetRouteAllEnabled -o tsv
4. Check the actual observation against the signed criterion: Outbound Route All behavior matches signed routing and DNS design.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-08 — Route All governance (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Outbound traffic bypasses the approved route

**Procedure:**

1. Use paired positive control AZ-T49-07 (Route All governance).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-09 — App Service DNS resolver path (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/dns/appservice-resolver.json && jq -e '.resolver and .result == "Pass"' evidence/dns/appservice-resolver.json
```

**Expected result:** Internal app DNS observations match approved resolver forwarding design; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Resolver uses an unintended name server

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/dns/appservice-resolver.json && jq -e '.resolver and .result == "Pass"' evidence/dns/appservice-resolver.json
4. Check the actual observation against the signed criterion: Internal app DNS observations match approved resolver forwarding design.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-10 — App Service DNS resolver path (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Resolver uses an unintended name server

**Procedure:**

1. Use paired positive control AZ-T49-09 (App Service DNS resolver path).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-11 — Egress NSG enforcement (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network nsg rule list -g "$RG" --nsg-name "$APP_NSG_NAME" -o json
```

**Expected result:** Egress allow/deny rules agree with least-privilege approved sources and destinations; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Broad egress allowances exist

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network nsg rule list -g "$RG" --nsg-name "$APP_NSG_NAME" -o json
4. Check the actual observation against the signed criterion: Egress allow/deny rules agree with least-privilege approved sources and destinations.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-12 — Egress NSG enforcement (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Broad egress allowances exist

**Procedure:**

1. Use paired positive control AZ-T49-11 (Egress NSG enforcement).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-13 — Firewall and UDR routes (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network route-table route list -g "$RG" --route-table-name "$APP_ROUTE_TABLE" -o json
```

**Expected result:** Routing tables use approved next hops for protected dependency networks; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Traffic bypasses the inspected egress route

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network route-table route list -g "$RG" --route-table-name "$APP_ROUTE_TABLE" -o json
4. Check the actual observation against the signed criterion: Routing tables use approved next hops for protected dependency networks.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-14 — Firewall and UDR routes (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Traffic bypasses the inspected egress route

**Procedure:**

1. Use paired positive control AZ-T49-13 (Firewall and UDR routes).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-15 — Internal PE connectivity (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/app-to-private-endpoints.json && jq -e '.status == "Pass"' evidence/network/app-to-private-endpoints.json
```

**Expected result:** Approved App Service test traffic reaches required PEs on expected ports; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** A required private service cannot be reached

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/app-to-private-endpoints.json && jq -e '.status == "Pass"' evidence/network/app-to-private-endpoints.json
4. Check the actual observation against the signed criterion: Approved App Service test traffic reaches required PEs on expected ports.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-16 — Internal PE connectivity (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** A required private service cannot be reached

**Procedure:**

1. Use paired positive control AZ-T49-15 (Internal PE connectivity).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-17 — Deny unapproved public egress (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/public-egress.json && jq -e '.unapproved_public_egress == 0' evidence/network/public-egress.json
```

**Expected result:** An approved isolated test demonstrates blocking of unapproved public destinations; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Unauthorized public egress succeeds

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/public-egress.json && jq -e '.unapproved_public_egress == 0' evidence/network/public-egress.json
4. Check the actual observation against the signed criterion: An approved isolated test demonstrates blocking of unapproved public destinations.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-18 — Deny unapproved public egress (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Unauthorized public egress succeeds

**Procedure:**

1. Use paired positive control AZ-T49-17 (Deny unapproved public egress).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-19 — Integration subnet drift (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved isolated read-only CI with explicit state access (never run on restricted WSL)

**Command:**

```bash
terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
```

**Expected result:** An approved scoped plan does not reveal unexplained network configuration changes; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** A route or subnet setting has drifted

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
4. Check the actual observation against the signed criterion: An approved scoped plan does not reveal unexplained network configuration changes.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory. A refresh-only plan may contact cloud services, read state and change lock state; it is not executed here.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-20 — Integration subnet drift (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** A route or subnet setting has drifted

**Procedure:**

1. Use paired positive control AZ-T49-19 (Integration subnet drift).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-21 — Failover and restoration runbook (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/network/appservice-failover.md && sha256sum docs/network/appservice-failover.md
```

**Expected result:** Network failover/rollback procedures have tested ownership and bounded scope; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Failover behavior and recovery steps are undefined

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 49.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/network/appservice-failover.md && sha256sum docs/network/appservice-failover.md
4. Check the actual observation against the signed criterion: Network failover/rollback procedures have tested ownership and bounded scope.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T49-22 — Failover and restoration runbook (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T49-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Failover behavior and recovery steps are undefined

**Procedure:**

1. Use paired positive control AZ-T49-21 (Failover and restoration runbook).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T49-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 50: Azure Container Registry adoption (conditional)

Test ID range: `AZ-T50-01` to `AZ-T50-22`.

### AZ-T50-01 — Containerization decision (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
jq -e '.containerization.decision and .containerization.approved_by' "$APP_BASELINE"
```

**Expected result:** The signed ADR states whether this system uses OCI container images; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Container use is ambiguous or unsigned

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: jq -e '.containerization.decision and .containerization.approved_by' "$APP_BASELINE"
4. Check the actual observation against the signed criterion: The signed ADR states whether this system uses OCI container images.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-02 — Containerization decision (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Container use is ambiguous or unsigned

**Procedure:**

1. Use paired positive control AZ-T50-01 (Containerization decision).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-03 — ACR private-compatible tier (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az acr show -g "$RG" -n "$ACR_NAME" --query sku.name -o tsv
```

**Expected result:** When ACR is adopted, its SKU supports the approved PE architecture; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** ACR SKU lacks required private access

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az acr show -g "$RG" -n "$ACR_NAME" --query sku.name -o tsv
4. Check the actual observation against the signed criterion: When ACR is adopted, its SKU supports the approved PE architecture.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-04 — ACR private-compatible tier (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** ACR SKU lacks required private access

**Procedure:**

1. Use paired positive control AZ-T50-03 (ACR private-compatible tier).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-05 — ACR Private Endpoint connection (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network private-endpoint show -g "$RG" -n "$PE_ACR_NAME" -o json
```

**Expected result:** Adopted ACR has an approved PE scoped to the registry; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Container registry PE is missing

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network private-endpoint show -g "$RG" -n "$PE_ACR_NAME" -o json
4. Check the actual observation against the signed criterion: Adopted ACR has an approved PE scoped to the registry.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-06 — ACR Private Endpoint connection (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Container registry PE is missing

**Procedure:**

1. Use paired positive control AZ-T50-05 (ACR Private Endpoint connection).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-07 — ACR private DNS (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved VNet-connected internal test runner; never public workstation

**Command:**

```bash
dig +short "${ACR_NAME}.azurecr.io" A
```

**Expected result:** Internal runner resolves registry and applicable data endpoints privately; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Registry resolves to public endpoints

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: dig +short "${ACR_NAME}.azurecr.io" A
4. Check the actual observation against the signed criterion: Internal runner resolves registry and applicable data endpoints privately.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-08 — ACR private DNS (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Registry resolves to public endpoints

**Procedure:**

1. Use paired positive control AZ-T50-07 (ACR private DNS).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-09 — AcrPull least privilege (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az role assignment list --assignee "$WEBAPP_PRINCIPAL_ID" --scope "$ACR_ID" -o json
```

**Expected result:** The Web App identity has only required registry pull permissions; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Excessive registry write/admin permission is granted

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az role assignment list --assignee "$WEBAPP_PRINCIPAL_ID" --scope "$ACR_ID" -o json
4. Check the actual observation against the signed criterion: The Web App identity has only required registry pull permissions.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-10 — AcrPull least privilege (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Excessive registry write/admin permission is granted

**Procedure:**

1. Use paired positive control AZ-T50-09 (AcrPull least privilege).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-11 — Immutable image digest (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
jq -e '.containerization.image_digest | startswith("sha256:")' "$APP_BASELINE"
```

**Expected result:** Deployed image reference is pinned to an approved sha256 digest; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Mutable image tag controls deployment without digest pinning

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: jq -e '.containerization.image_digest | startswith("sha256:")' "$APP_BASELINE"
4. Check the actual observation against the signed criterion: Deployed image reference is pinned to an approved sha256 digest.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-12 — Immutable image digest (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Mutable image tag controls deployment without digest pinning

**Procedure:**

1. Use paired positive control AZ-T50-11 (Immutable image digest).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-13 — Software bill of materials (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/supplychain/sbom.json && jq -e '.bomFormat or .spdxVersion' evidence/supplychain/sbom.json
```

**Expected result:** SBOM is generated and retained for the exact deployed artifact; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** SBOM is missing or unrelated to the image

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/supplychain/sbom.json && jq -e '.bomFormat or .spdxVersion' evidence/supplychain/sbom.json
4. Check the actual observation against the signed criterion: SBOM is generated and retained for the exact deployed artifact.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-14 — Software bill of materials (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** SBOM is missing or unrelated to the image

**Procedure:**

1. Use paired positive control AZ-T50-13 (Software bill of materials).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-15 — Signed container image (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/supplychain/signature-review.json && jq -e '.verified == true and .digest' evidence/supplychain/signature-review.json
```

**Expected result:** Image signature verification binds to the expected digest and trusted identity; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Signature is missing, invalid or unrelated to artifact

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/supplychain/signature-review.json && jq -e '.verified == true and .digest' evidence/supplychain/signature-review.json
4. Check the actual observation against the signed criterion: Image signature verification binds to the expected digest and trusted identity.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-16 — Signed container image (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Signature is missing, invalid or unrelated to artifact

**Procedure:**

1. Use paired positive control AZ-T50-15 (Signed container image).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-17 — Vulnerability assessment (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/supplychain/vulnerability-scan.json && jq -e '.critical == 0 and .high_waivers_approved == true' evidence/supplychain/vulnerability-scan.json
```

**Expected result:** Critical findings are absent or formally adjudicated by security review; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Unapproved critical vulnerabilities remain

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/supplychain/vulnerability-scan.json && jq -e '.critical == 0 and .high_waivers_approved == true' evidence/supplychain/vulnerability-scan.json
4. Check the actual observation against the signed criterion: Critical findings are absent or formally adjudicated by security review.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-18 — Vulnerability assessment (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Unapproved critical vulnerabilities remain

**Procedure:**

1. Use paired positive control AZ-T50-17 (Vulnerability assessment).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-19 — Private runner image retrieval (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/deployment/acr-pull.json && jq -e '.runner_private == true and .status == "Pass"' evidence/deployment/acr-pull.json
```

**Expected result:** Approved private runner can retrieve the image through the intended private route; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Image pull depends on unauthorized public access

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/deployment/acr-pull.json && jq -e '.runner_private == true and .status == "Pass"' evidence/deployment/acr-pull.json
4. Check the actual observation against the signed criterion: Approved private runner can retrieve the image through the intended private route.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-20 — Private runner image retrieval (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Image pull depends on unauthorized public access

**Procedure:**

1. Use paired positive control AZ-T50-19 (Private runner image retrieval).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-21 — Reject unauthorized image (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/supplychain/untrusted-image.json && jq -e '.denied == true' evidence/supplychain/untrusted-image.json
```

**Expected result:** Isolated policy test refuses a nonapproved image; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Untrusted images are deployable

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 50.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/supplychain/untrusted-image.json && jq -e '.denied == true' evidence/supplychain/untrusted-image.json
4. Check the actual observation against the signed criterion: Isolated policy test refuses a nonapproved image.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T50-22 — Reject unauthorized image (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T50-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Untrusted images are deployable

**Procedure:**

1. Use paired positive control AZ-T50-21 (Reject unauthorized image).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T50-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 51: WAF policy and controlled transition to Prevention

Test ID range: `AZ-T51-01` to `AZ-T51-22`.

### AZ-T51-01 — Detection baseline and tuning (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query policySettings.mode -o tsv
```

**Expected result:** WAF Detection-phase review includes benign control traffic and authorized Prevention transition; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Prevention is enabled before tuning and signoff

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query policySettings.mode -o tsv
4. Check the actual observation against the signed criterion: WAF Detection-phase review includes benign control traffic and authorized Prevention transition.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-02 — Detection baseline and tuning (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Prevention is enabled before tuning and signoff

**Procedure:**

1. Use paired positive control AZ-T51-01 (Detection baseline and tuning).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-03 — Managed rule set version (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query managedRules.managedRuleSets -o json
```

**Expected result:** The effective managed rule set is the approved DRS 2.2 or reviewed successor; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Unsupported rule set or unapproved version is active

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query managedRules.managedRuleSets -o json
4. Check the actual observation against the signed criterion: The effective managed rule set is the approved DRS 2.2 or reviewed successor.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-04 — Managed rule set version (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Unsupported rule set or unapproved version is active

**Procedure:**

1. Use paired positive control AZ-T51-03 (Managed rule set version).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-05 — Prevention enforcement status (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query policySettings.mode -o tsv
```

**Expected result:** Production acceptance requires approved effective Prevention mode; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** WAF stays in Detection after release authorization

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query policySettings.mode -o tsv
4. Check the actual observation against the signed criterion: Production acceptance requires approved effective Prevention mode.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-06 — Prevention enforcement status (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** WAF stays in Detection after release authorization

**Procedure:**

1. Use paired positive control AZ-T51-05 (Prevention enforcement status).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-07 — Approved rule identifiers (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/waf/approved-rule-ids.json && jq -e '.version and .approved_rules' docs/waf/approved-rule-ids.json
```

**Expected result:** Tested rule IDs and effective rule-set revision match the signed inventory; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Different rule IDs were evaluated than those deployed

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/waf/approved-rule-ids.json && jq -e '.version and .approved_rules' docs/waf/approved-rule-ids.json
4. Check the actual observation against the signed criterion: Tested rule IDs and effective rule-set revision match the signed inventory.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-08 — Approved rule identifiers (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Different rule IDs were evaluated than those deployed

**Procedure:**

1. Use paired positive control AZ-T51-07 (Approved rule identifiers).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-09 — Narrow WAF exclusions (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query managedRules.exclusions -o json
```

**Expected result:** Field-level exclusions are documented, minimal, and reviewer-approved; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Blanket exclusions undermine protections

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query managedRules.exclusions -o json
4. Check the actual observation against the signed criterion: Field-level exclusions are documented, minimal, and reviewer-approved.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-10 — Narrow WAF exclusions (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Blanket exclusions undermine protections

**Procedure:**

1. Use paired positive control AZ-T51-09 (Narrow WAF exclusions).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-11 — Controlled custom WAF rules (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query customRules -o json
```

**Expected result:** Custom rules have explicit business reason, priority, owner, and expiry; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Unreviewed custom rule widens public acceptance

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query customRules -o json
4. Check the actual observation against the signed criterion: Custom rules have explicit business reason, priority, owner, and expiry.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-12 — Controlled custom WAF rules (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Unreviewed custom rule widens public acceptance

**Procedure:**

1. Use paired positive control AZ-T51-11 (Controlled custom WAF rules).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-13 — Benign request control (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/waf/benign-junit.xml && sha256sum evidence/waf/benign-junit.xml
```

**Expected result:** Approved nonproduction tests show representative allowed traffic is not blocked; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** WAF blocks an approved benign control flow

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/waf/benign-junit.xml && sha256sum evidence/waf/benign-junit.xml
4. Check the actual observation against the signed criterion: Approved nonproduction tests show representative allowed traffic is not blocked.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-14 — Benign request control (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** WAF blocks an approved benign control flow

**Procedure:**

1. Use paired positive control AZ-T51-13 (Benign request control).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-15 — SQLi detector correlation (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/waf/sqli-junit.xml && sha256sum evidence/waf/sqli-junit.xml
```

**Expected result:** Harmless authorized simulation maps to the intended WAF rule and deny outcome; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** SQLi simulation is not detected or blocked as required

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/waf/sqli-junit.xml && sha256sum evidence/waf/sqli-junit.xml
4. Check the actual observation against the signed criterion: Harmless authorized simulation maps to the intended WAF rule and deny outcome.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-16 — SQLi detector correlation (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** SQLi simulation is not detected or blocked as required

**Procedure:**

1. Use paired positive control AZ-T51-15 (SQLi detector correlation).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-17 — XSS detector correlation (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/waf/xss-junit.xml && sha256sum evidence/waf/xss-junit.xml
```

**Expected result:** Harmless authorized simulation maps to the intended WAF rule and deny outcome; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** XSS simulation is not detected or blocked as required

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/waf/xss-junit.xml && sha256sum evidence/waf/xss-junit.xml
4. Check the actual observation against the signed criterion: Harmless authorized simulation maps to the intended WAF rule and deny outcome.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-18 — XSS detector correlation (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** XSS simulation is not detected or blocked as required

**Procedure:**

1. Use paired positive control AZ-T51-17 (XSS detector correlation).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-19 — WAF request-to-log correlation (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/waf/firewall-correlation.json && jq -e '.transaction_id and .rule_id and .action' evidence/waf/firewall-correlation.json
```

**Expected result:** Each expected denial has matching WAF event, transaction ID and action; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** HTTP 403 occurs without the expected WAF log evidence

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/waf/firewall-correlation.json && jq -e '.transaction_id and .rule_id and .action' evidence/waf/firewall-correlation.json
4. Check the actual observation against the signed criterion: Each expected denial has matching WAF event, transaction ID and action.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-20 — WAF request-to-log correlation (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** HTTP 403 occurs without the expected WAF log evidence

**Procedure:**

1. Use paired positive control AZ-T51-19 (WAF request-to-log correlation).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-21 — WAF policy version history (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/waf/release-history.json && jq -e '.changes and .reviewer' docs/waf/release-history.json
```

**Expected result:** Exceptions and policy revisions are signed, traceable, and reversible; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** WAF policy changes lack independent review

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 51.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/waf/release-history.json && jq -e '.changes and .reviewer' docs/waf/release-history.json
4. Check the actual observation against the signed criterion: Exceptions and policy revisions are signed, traceable, and reversible.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T51-22 — WAF policy version history (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T51-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** WAF policy changes lack independent review

**Procedure:**

1. Use paired positive control AZ-T51-21 (WAF policy version history).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T51-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 52: Private-only Application Gateway

Test ID range: `AZ-T52-01` to `AZ-T52-22`.

### AZ-T52-01 — Private frontend IP (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query "frontendIPConfigurations[].privateIPAddress" -o json
```

**Expected result:** Application Gateway frontend uses an approved private subnet address; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Frontend IP is public or outside signed ranges

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query "frontendIPConfigurations[].privateIPAddress" -o json
4. Check the actual observation against the signed criterion: Application Gateway frontend uses an approved private subnet address.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-02 — Private frontend IP (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Frontend IP is public or outside signed ranges

**Procedure:**

1. Use paired positive control AZ-T52-01 (Private frontend IP).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-03 — No public frontend references (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query frontendIPConfigurations -o json
```

**Expected result:** No frontend IP configuration references a public IP ID; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Public frontend IP remains configured

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query frontendIPConfigurations -o json
4. Check the actual observation against the signed criterion: No frontend IP configuration references a public IP ID.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-04 — No public frontend references (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Public frontend IP remains configured

**Procedure:**

1. Use paired positive control AZ-T52-03 (No public frontend references).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-05 — Delegated gateway subnet (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET_NAME" -n "$AGW_SUBNET_NAME" --query delegations -o json
```

**Expected result:** Isolated Application Gateway subnet has required delegation for selected private deployment; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Delegation is missing or subnet is shared

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network vnet subnet show -g "$RG" --vnet-name "$VNET_NAME" -n "$AGW_SUBNET_NAME" --query delegations -o json
4. Check the actual observation against the signed criterion: Isolated Application Gateway subnet has required delegation for selected private deployment.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-06 — Delegated gateway subnet (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Delegation is missing or subnet is shared

**Procedure:**

1. Use paired positive control AZ-T52-05 (Delegated gateway subnet).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-07 — Network isolation feature state (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az feature show --namespace Microsoft.Network --name EnableApplicationGatewayNetworkIsolation --query properties.state -o tsv
```

**Expected result:** Required subscription feature is registered where demanded by the selected supported deployment mode; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Private deployment prerequisite is not registered

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az feature show --namespace Microsoft.Network --name EnableApplicationGatewayNetworkIsolation --query properties.state -o tsv
4. Check the actual observation against the signed criterion: Required subscription feature is registered where demanded by the selected supported deployment mode.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-08 — Network isolation feature state (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Private deployment prerequisite is not registered

**Procedure:**

1. Use paired positive control AZ-T52-07 (Network isolation feature state).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-09 — Same-region backend PE (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/network/same-region-pe.json && jq -e '.appgw_region == .app_pe_region' docs/network/same-region-pe.json
```

**Expected result:** Gateway and App Service PE topology complies with signed regional/peering limitations; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Gateway relies on unsupported cross-region private backend

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/network/same-region-pe.json && jq -e '.appgw_region == .app_pe_region' docs/network/same-region-pe.json
4. Check the actual observation against the signed criterion: Gateway and App Service PE topology complies with signed regional/peering limitations.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-10 — Same-region backend PE (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Gateway relies on unsupported cross-region private backend

**Procedure:**

1. Use paired positive control AZ-T52-09 (Same-region backend PE).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-11 — No conflicting AppGW Private Link (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query privateLinkConfigurations -o json
```

**Expected result:** Private-only gateway does not use an unsupported simultaneous Private Link configuration; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Forbidden Private Link configuration is present

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query privateLinkConfigurations -o json
4. Check the actual observation against the signed criterion: Private-only gateway does not use an unsupported simultaneous Private Link configuration.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-12 — No conflicting AppGW Private Link (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Forbidden Private Link configuration is present

**Procedure:**

1. Use paired positive control AZ-T52-11 (No conflicting AppGW Private Link).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-13 — Private HTTPS listener (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway http-listener list -g "$RG" --gateway-name "$APPGW_NAME" -o json
```

**Expected result:** HTTPS listener is bound to approved private frontend and certificate; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Listener exposes an unapproved route

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway http-listener list -g "$RG" --gateway-name "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: HTTPS listener is bound to approved private frontend and certificate.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-14 — Private HTTPS listener (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Listener exposes an unapproved route

**Procedure:**

1. Use paired positive control AZ-T52-13 (Private HTTPS listener).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-15 — Gateway autoscaling policy (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query autoscaleConfiguration -o json
```

**Expected result:** Autoscale capacity constraints match signed operational baseline; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Autoscale can exceed budget or violates HA floor

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query autoscaleConfiguration -o json
4. Check the actual observation against the signed criterion: Autoscale capacity constraints match signed operational baseline.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-16 — Gateway autoscaling policy (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Autoscale can exceed budget or violates HA floor

**Procedure:**

1. Use paired positive control AZ-T52-15 (Gateway autoscaling policy).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-17 — Backend pool health (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway show-backend-health -g "$RG" -n "$APPGW_NAME" -o json
```

**Expected result:** App Service backend reports Healthy through approved private path; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Gateway backend is Unhealthy

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway show-backend-health -g "$RG" -n "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: App Service backend reports Healthy through approved private path.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-18 — Backend pool health (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Gateway backend is Unhealthy

**Procedure:**

1. Use paired positive control AZ-T52-17 (Backend pool health).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-19 — Zero unauthorized public IP (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network public-ip list -g "$RG" --query "[?contains(name, 'appgw')]" -o json
```

**Expected result:** All related public IP resources and references are absent or explicitly approved outside this private data-plane; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** An unapproved public IP is attached

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network public-ip list -g "$RG" --query "[?contains(name, 'appgw')]" -o json
4. Check the actual observation against the signed criterion: All related public IP resources and references are absent or explicitly approved outside this private data-plane.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-20 — Zero unauthorized public IP (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** An unapproved public IP is attached

**Procedure:**

1. Use paired positive control AZ-T52-19 (Zero unauthorized public IP).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-21 — Approved gateway drift (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved isolated read-only CI with explicit state access (never run on restricted WSL)

**Command:**

```bash
terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
```

**Expected result:** Saved-plan comparison shows no unreviewed gateway infrastructure changes; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Gateway configuration differs from signed design

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 52.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
4. Check the actual observation against the signed criterion: Saved-plan comparison shows no unreviewed gateway infrastructure changes.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory. A refresh-only plan may contact cloud services, read state and change lock state; it is not executed here.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T52-22 — Approved gateway drift (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T52-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Gateway configuration differs from signed design

**Procedure:**

1. Use paired positive control AZ-T52-21 (Approved gateway drift).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T52-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 53: TLS certificates and Key Vault custody

Test ID range: `AZ-T53-01` to `AZ-T53-22`.

### AZ-T53-01 — Versionless certificate secret ID (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/tls/secret-reference.json && jq -e '.versionless == true and .secret_uri' docs/tls/secret-reference.json
```

**Expected result:** Application Gateway references the approved versionless Key Vault secret ID; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Version-pinned URI prevents certificate rotation

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/tls/secret-reference.json && jq -e '.versionless == true and .secret_uri' docs/tls/secret-reference.json
4. Check the actual observation against the signed criterion: Application Gateway references the approved versionless Key Vault secret ID.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-02 — Versionless certificate secret ID (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Version-pinned URI prevents certificate rotation

**Procedure:**

1. Use paired positive control AZ-T53-01 (Versionless certificate secret ID).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-03 — Gateway user-assigned identity (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az identity show -g "$RG" -n "$APPGW_IDENTITY_NAME" --query principalId -o tsv
```

**Expected result:** Gateway UAMI principal matches approved inventory and Vault role target; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Wrong or missing managed identity

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az identity show -g "$RG" -n "$APPGW_IDENTITY_NAME" --query principalId -o tsv
4. Check the actual observation against the signed criterion: Gateway UAMI principal matches approved inventory and Vault role target.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-04 — Gateway user-assigned identity (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Wrong or missing managed identity

**Procedure:**

1. Use paired positive control AZ-T53-03 (Gateway user-assigned identity).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-05 — Least-privilege Vault secret read (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az role assignment list --assignee "$APPGW_PRINCIPAL_ID" --scope "$VAULT_ID" -o json
```

**Expected result:** Gateway identity has approved secret read scope without Vault administrator privileges; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Excessive Key Vault permissions are granted

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az role assignment list --assignee "$APPGW_PRINCIPAL_ID" --scope "$VAULT_ID" -o json
4. Check the actual observation against the signed criterion: Gateway identity has approved secret read scope without Vault administrator privileges.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-06 — Least-privilege Vault secret read (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Excessive Key Vault permissions are granted

**Procedure:**

1. Use paired positive control AZ-T53-05 (Least-privilege Vault secret read).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-07 — Certificate expiry threshold (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az keyvault certificate show --vault-name "$VAULT_NAME" --name "$GW_CERT_NAME" --query attributes.expires -o tsv
```

**Expected result:** Certificate validity exceeds the signed alert/renewal lead time; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Certificate is expired or renewal lead time breached

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az keyvault certificate show --vault-name "$VAULT_NAME" --name "$GW_CERT_NAME" --query attributes.expires -o tsv
4. Check the actual observation against the signed criterion: Certificate validity exceeds the signed alert/renewal lead time.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-08 — Certificate expiry threshold (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Certificate is expired or renewal lead time breached

**Procedure:**

1. Use paired positive control AZ-T53-07 (Certificate expiry threshold).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-09 — Certificate SAN coverage (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/tls/certificate-san.json && jq -e '.approved_hostnames and .san_verified == true' evidence/tls/certificate-san.json
```

**Expected result:** Subject alternative names cover the approved private hostname; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Gateway hostname not present in certificate SAN

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/tls/certificate-san.json && jq -e '.approved_hostnames and .san_verified == true' evidence/tls/certificate-san.json
4. Check the actual observation against the signed criterion: Subject alternative names cover the approved private hostname.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-10 — Certificate SAN coverage (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Gateway hostname not present in certificate SAN

**Procedure:**

1. Use paired positive control AZ-T53-09 (Certificate SAN coverage).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-11 — Trusted TLS certificate chain (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved VNet-connected internal test runner; never public workstation

**Command:**

```bash
openssl s_client -connect "${APPGW_FQDN}:443" -servername "$APPGW_FQDN" -verify_return_error </dev/null
```

**Expected result:** Approved internal client verifies full TLS chain and hostname using SNI; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Certificate chain verification fails

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: openssl s_client -connect "${APPGW_FQDN}:443" -servername "$APPGW_FQDN" -verify_return_error </dev/null
4. Check the actual observation against the signed criterion: Approved internal client verifies full TLS chain and hostname using SNI.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-12 — Trusted TLS certificate chain (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Certificate chain verification fails

**Procedure:**

1. Use paired positive control AZ-T53-11 (Trusted TLS certificate chain).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-13 — Certificate rotation governance (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/tls/cert-rotation.json && jq -e '.rotation_lead_days and .owner' docs/tls/cert-rotation.json
```

**Expected result:** Rotation trigger, owner and fallback steps are approved and documented; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** No owner or renewal procedure exists

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/tls/cert-rotation.json && jq -e '.rotation_lead_days and .owner' docs/tls/cert-rotation.json
4. Check the actual observation against the signed criterion: Rotation trigger, owner and fallback steps are approved and documented.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-14 — Certificate rotation governance (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** No owner or renewal procedure exists

**Procedure:**

1. Use paired positive control AZ-T53-13 (Certificate rotation governance).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-15 — Gateway-to-Vault private path (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network private-endpoint show -g "$RG" -n "$PE_VAULT_NAME" -o json
```

**Expected result:** Key Vault PE/DNS and Gateway token+secret access route are independently verified; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Private Vault path fails

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network private-endpoint show -g "$RG" -n "$PE_VAULT_NAME" -o json
4. Check the actual observation against the signed criterion: Key Vault PE/DNS and Gateway token+secret access route are independently verified.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-16 — Gateway-to-Vault private path (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Private Vault path fails

**Procedure:**

1. Use paired positive control AZ-T53-15 (Gateway-to-Vault private path).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-17 — Authorized certificate rotation drill (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/tls/rotation-drill.json && jq -e '.result == "Pass" and .fallback' evidence/tls/rotation-drill.json
```

**Expected result:** Isolated nonproduction drill verifies renew and rollback without key disclosure; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Rotation breaks TLS or cannot be rolled back

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/tls/rotation-drill.json && jq -e '.result == "Pass" and .fallback' evidence/tls/rotation-drill.json
4. Check the actual observation against the signed criterion: Isolated nonproduction drill verifies renew and rollback without key disclosure.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-18 — Authorized certificate rotation drill (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Rotation breaks TLS or cannot be rolled back

**Procedure:**

1. Use paired positive control AZ-T53-17 (Authorized certificate rotation drill).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-19 — Expiry alert delivery (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/tls/expiry-alert.json && jq -e '.lead_days and .action_group' docs/tls/expiry-alert.json
```

**Expected result:** Certificate expiry notification reaches the agreed action group; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Certificate alert is missing

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/tls/expiry-alert.json && jq -e '.lead_days and .action_group' docs/tls/expiry-alert.json
4. Check the actual observation against the signed criterion: Certificate expiry notification reaches the agreed action group.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-20 — Expiry alert delivery (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Certificate alert is missing

**Procedure:**

1. Use paired positive control AZ-T53-19 (Expiry alert delivery).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-21 — Nonsecret certificate audit (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/tls/cert-management-audit.json && jq -e '.reviewer and .resource_id and .collected_at_utc' evidence/tls/cert-management-audit.json
```

**Expected result:** Evidence contains resource, expiry, reviewer and timestamp without private keys; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Certificate records are incomplete or sensitive

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 53.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/tls/cert-management-audit.json && jq -e '.reviewer and .resource_id and .collected_at_utc' evidence/tls/cert-management-audit.json
4. Check the actual observation against the signed criterion: Evidence contains resource, expiry, reviewer and timestamp without private keys.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T53-22 — Nonsecret certificate audit (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T53-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Certificate records are incomplete or sensitive

**Procedure:**

1. Use paired positive control AZ-T53-21 (Nonsecret certificate audit).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T53-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 54: HTTPS listeners, routing rules, and backend probes

Test ID range: `AZ-T54-01` to `AZ-T54-22`.

### AZ-T54-01 — Private HTTPS 443 listener (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway http-listener list -g "$RG" --gateway-name "$APPGW_NAME" -o json
```

**Expected result:** Approved HTTPS listener uses private frontend on 443; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Listener is missing or uses a public endpoint

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway http-listener list -g "$RG" --gateway-name "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: Approved HTTPS listener uses private frontend on 443.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-02 — Private HTTPS 443 listener (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Listener is missing or uses a public endpoint

**Procedure:**

1. Use paired positive control AZ-T54-01 (Private HTTPS 443 listener).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-03 — HTTP port 80 handling (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway http-listener list -g "$RG" --gateway-name "$APPGW_NAME" --query "[?protocol=='Http']" -o json
```

**Expected result:** Unencrypted HTTP is disabled or, when explicitly approved, redirects only to HTTPS; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Port 80 serves protected content unencrypted

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway http-listener list -g "$RG" --gateway-name "$APPGW_NAME" --query "[?protocol=='Http']" -o json
4. Check the actual observation against the signed criterion: Unencrypted HTTP is disabled or, when explicitly approved, redirects only to HTTPS.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-04 — HTTP port 80 handling (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Port 80 serves protected content unencrypted

**Procedure:**

1. Use paired positive control AZ-T54-03 (HTTP port 80 handling).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-05 — HTTPS backend connection (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway http-settings list -g "$RG" --gateway-name "$APPGW_NAME" -o json
```

**Expected result:** Backend settings use TLS and approved port 443; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Backend is plain HTTP or wrong port

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway http-settings list -g "$RG" --gateway-name "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: Backend settings use TLS and approved port 443.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-06 — HTTPS backend connection (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Backend is plain HTTP or wrong port

**Procedure:**

1. Use paired positive control AZ-T54-05 (HTTPS backend connection).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-07 — Named health probe (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway probe list -g "$RG" --gateway-name "$APPGW_NAME" -o json
```

**Expected result:** Probe path/host targets the app-approved health resource; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Probe uses wrong hostname or endpoint

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway probe list -g "$RG" --gateway-name "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: Probe path/host targets the app-approved health resource.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-08 — Named health probe (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Probe uses wrong hostname or endpoint

**Procedure:**

1. Use paired positive control AZ-T54-07 (Named health probe).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-09 — Unique route priorities (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway rule list -g "$RG" --gateway-name "$APPGW_NAME" -o json
```

**Expected result:** Request routing priorities are distinct and meet approved routing order; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Conflicting priorities alter routes

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway rule list -g "$RG" --gateway-name "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: Request routing priorities are distinct and meet approved routing order.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-10 — Unique route priorities (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Conflicting priorities alter routes

**Procedure:**

1. Use paired positive control AZ-T54-09 (Unique route priorities).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-11 — Host header allowlist (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway http-listener list -g "$RG" --gateway-name "$APPGW_NAME" --query "[].hostNames" -o json
```

**Expected result:** Listener host configuration is restricted to approved DNS names; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Wildcard/unknown host is accepted outside approved plan

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway http-listener list -g "$RG" --gateway-name "$APPGW_NAME" --query "[].hostNames" -o json
4. Check the actual observation against the signed criterion: Listener host configuration is restricted to approved DNS names.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-12 — Host header allowlist (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Wildcard/unknown host is accepted outside approved plan

**Procedure:**

1. Use paired positive control AZ-T54-11 (Host header allowlist).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-13 — Safe rewrite rules (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway rewrite-rule set list -g "$RG" --gateway-name "$APPGW_NAME" -o json
```

**Expected result:** Rewrites preserve Host/SNI boundaries and required security headers; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Rewrite breaks host security or strips safeguards

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway rewrite-rule set list -g "$RG" --gateway-name "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: Rewrites preserve Host/SNI boundaries and required security headers.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-14 — Safe rewrite rules (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Rewrite breaks host security or strips safeguards

**Procedure:**

1. Use paired positive control AZ-T54-13 (Safe rewrite rules).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-15 — Healthy backend observations (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway show-backend-health -g "$RG" -n "$APPGW_NAME" -o json
```

**Expected result:** Backend health and corresponding app response/log evidence agree; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Health shows failure or is unsupported by app evidence

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway show-backend-health -g "$RG" -n "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: Backend health and corresponding app response/log evidence agree.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-16 — Healthy backend observations (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Health shows failure or is unsupported by app evidence

**Procedure:**

1. Use paired positive control AZ-T54-15 (Healthy backend observations).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-17 — Approved TLS policy (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query sslPolicy -o json
```

**Expected result:** Application Gateway SSL policy equals approved baseline; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Weak or unreviewed TLS policy is active

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query sslPolicy -o json
4. Check the actual observation against the signed criterion: Application Gateway SSL policy equals approved baseline.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-18 — Approved TLS policy (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Weak or unreviewed TLS policy is active

**Procedure:**

1. Use paired positive control AZ-T54-17 (Approved TLS policy).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-19 — 5xx alert handling (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/gateway/503-analysis.json && jq -e '.backend_503_count == 0' evidence/gateway/503-analysis.json
```

**Expected result:** Approved normal traffic has no unexplained 503 and incident alerts are proven; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** HTTP 503 occurs without detection/triage

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/gateway/503-analysis.json && jq -e '.backend_503_count == 0' evidence/gateway/503-analysis.json
4. Check the actual observation against the signed criterion: Approved normal traffic has no unexplained 503 and incident alerts are proven.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-20 — 5xx alert handling (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** HTTP 503 occurs without detection/triage

**Procedure:**

1. Use paired positive control AZ-T54-19 (5xx alert handling).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-21 — Routing map approval (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/gateway/routing-approval.json && jq -e '.reviewer and .rule_ids' docs/gateway/routing-approval.json
```

**Expected result:** Frontend, listener, routing rule and backend association are versioned and signed; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Network routing differs from reviewed topology

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 54.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/gateway/routing-approval.json && jq -e '.reviewer and .rule_ids' docs/gateway/routing-approval.json
4. Check the actual observation against the signed criterion: Frontend, listener, routing rule and backend association are versioned and signed.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T54-22 — Routing map approval (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T54-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Network routing differs from reviewed topology

**Procedure:**

1. Use paired positive control AZ-T54-21 (Routing map approval).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T54-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 55: Backend hostname, SNI, and private reachability

Test ID range: `AZ-T55-01` to `AZ-T55-22`.

### AZ-T55-01 — Canonical backend FQDN (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway address-pool list -g "$RG" --gateway-name "$APPGW_NAME" -o json
```

**Expected result:** Gateway backend pool contains App Service canonical FQDN; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Backend uses a wrong alias/IP or a public-only endpoint

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway address-pool list -g "$RG" --gateway-name "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: Gateway backend pool contains App Service canonical FQDN.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-02 — Canonical backend FQDN (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Backend uses a wrong alias/IP or a public-only endpoint

**Procedure:**

1. Use paired positive control AZ-T55-01 (Canonical backend FQDN).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-03 — Backend private DNS (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved VNet-connected internal test runner; never public workstation

**Command:**

```bash
dig +short "$WEBAPP_FQDN" A
```

**Expected result:** Gateway DNS path resolves App Service hostname to approved PE IP; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Backend DNS resolves to unintended public A record

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: dig +short "$WEBAPP_FQDN" A
4. Check the actual observation against the signed criterion: Gateway DNS path resolves App Service hostname to approved PE IP.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-04 — Backend private DNS (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Backend DNS resolves to unintended public A record

**Procedure:**

1. Use paired positive control AZ-T55-03 (Backend private DNS).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-05 — Backend Host header alignment (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway http-settings list -g "$RG" --gateway-name "$APPGW_NAME" -o json
```

**Expected result:** Host override matches App Service routing/certificate expectation; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Backend Host header mismatch causes 502/503

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway http-settings list -g "$RG" --gateway-name "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: Host override matches App Service routing/certificate expectation.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-06 — Backend Host header alignment (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Backend Host header mismatch causes 502/503

**Procedure:**

1. Use paired positive control AZ-T55-05 (Backend Host header alignment).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-07 — TLS SNI correctness (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved VNet-connected internal test runner; never public workstation

**Command:**

```bash
openssl s_client -connect "${WEBAPP_FQDN}:443" -servername "$WEBAPP_FQDN" -verify_return_error </dev/null
```

**Expected result:** Private backend TLS handshake validates canonical server name; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** SNI differs from certificate hostname

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: openssl s_client -connect "${WEBAPP_FQDN}:443" -servername "$WEBAPP_FQDN" -verify_return_error </dev/null
4. Check the actual observation against the signed criterion: Private backend TLS handshake validates canonical server name.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Output must be compared with a signed baseline and approved test-scope inventory.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-08 — TLS SNI correctness (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** SNI differs from certificate hostname

**Procedure:**

1. Use paired positive control AZ-T55-07 (TLS SNI correctness).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-09 — Health probe hostname (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway probe list -g "$RG" --gateway-name "$APPGW_NAME" -o json
```

**Expected result:** Probe Host header matches validated app hostname and probe settings; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Probe hostname differs from expected backend

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway probe list -g "$RG" --gateway-name "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: Probe Host header matches validated app hostname and probe settings.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-10 — Health probe hostname (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Probe hostname differs from expected backend

**Procedure:**

1. Use paired positive control AZ-T55-09 (Health probe hostname).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-11 — Backend certificate SAN (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/tls/app-backend-san.json && jq -e '.san_verified == true' evidence/tls/app-backend-san.json
```

**Expected result:** Backend hostname is covered by certificate SAN and verified; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Backend TLS certificate does not match hostname

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/tls/app-backend-san.json && jq -e '.san_verified == true' evidence/tls/app-backend-san.json
4. Check the actual observation against the signed criterion: Backend hostname is covered by certificate SAN and verified.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-12 — Backend certificate SAN (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Backend TLS certificate does not match hostname

**Procedure:**

1. Use paired positive control AZ-T55-11 (Backend certificate SAN).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-13 — Observed App Service PE IP (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network private-endpoint show -g "$RG" -n "$PE_APP_NAME" --query customDnsConfigs -o json
```

**Expected result:** Private Endpoint NIC address matches approved backend resolution target; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Backend DNS resolves to an unrelated IP

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network private-endpoint show -g "$RG" -n "$PE_APP_NAME" --query customDnsConfigs -o json
4. Check the actual observation against the signed criterion: Private Endpoint NIC address matches approved backend resolution target.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-14 — Observed App Service PE IP (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Backend DNS resolves to an unrelated IP

**Procedure:**

1. Use paired positive control AZ-T55-13 (Observed App Service PE IP).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-15 — Gateway-to-backend port 443 (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/gateway-to-webapp.json && jq -e '.port == 443 and .status == "Pass"' evidence/network/gateway-to-webapp.json
```

**Expected result:** Actual private traffic reaches PE over TLS 443; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Backend is unreachable or uses unapproved port

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/gateway-to-webapp.json && jq -e '.port == 443 and .status == "Pass"' evidence/network/gateway-to-webapp.json
4. Check the actual observation against the signed criterion: Actual private traffic reaches PE over TLS 443.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-16 — Gateway-to-backend port 443 (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Backend is unreachable or uses unapproved port

**Procedure:**

1. Use paired positive control AZ-T55-15 (Gateway-to-backend port 443).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-17 — Backend healthy + app log agreement (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network application-gateway show-backend-health -g "$RG" -n "$APPGW_NAME" -o json
```

**Expected result:** Gateway probe success agrees with application /healthz behavior; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Gateway health and backend response disagree

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network application-gateway show-backend-health -g "$RG" -n "$APPGW_NAME" -o json
4. Check the actual observation against the signed criterion: Gateway probe success agrees with application /healthz behavior.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-18 — Backend healthy + app log agreement (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Gateway health and backend response disagree

**Procedure:**

1. Use paired positive control AZ-T55-17 (Backend healthy + app log agreement).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-19 — App default hostname public denial (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az webapp show -g "$RG" -n "$WEBAPP_NAME" --query publicNetworkAccess -o tsv
```

**Expected result:** App Service default data-plane endpoint has public network access disabled; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Default app hostname is exposed publicly

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az webapp show -g "$RG" -n "$WEBAPP_NAME" --query publicNetworkAccess -o tsv
4. Check the actual observation against the signed criterion: App Service default data-plane endpoint has public network access disabled.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-20 — App default hostname public denial (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Default app hostname is exposed publicly

**Procedure:**

1. Use paired positive control AZ-T55-19 (App default hostname public denial).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-21 — Gateway-to-App request trace (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/backend-trace.json && jq -e '.request_id and .appgw_access and .app_service' evidence/network/backend-trace.json
```

**Expected result:** Synthetic request ID joins Gateway access and backend application logs; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** End-to-end request cannot be traced

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 55.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/backend-trace.json && jq -e '.request_id and .appgw_access and .app_service' evidence/network/backend-trace.json
4. Check the actual observation against the signed criterion: Synthetic request ID joins Gateway access and backend application logs.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T55-22 — Gateway-to-App request trace (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T55-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** End-to-end request cannot be traced

**Procedure:**

1. Use paired positive control AZ-T55-21 (Gateway-to-App request trace).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T55-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 56: Private Endpoint traffic boundaries and least privilege

Test ID range: `AZ-T56-01` to `AZ-T56-22`.

### AZ-T56-01 — Gateway to App PE (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/agw-to-app-pe.json && jq -e '.result == "Pass" and .port == 443' evidence/network/agw-to-app-pe.json
```

**Expected result:** Gateway reaches App Service PE on HTTPS 443 via approved path; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Gateway-to-App PE route is blocked/unapproved

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/agw-to-app-pe.json && jq -e '.result == "Pass" and .port == 443' evidence/network/agw-to-app-pe.json
4. Check the actual observation against the signed criterion: Gateway reaches App Service PE on HTTPS 443 via approved path.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-02 — Gateway to App PE (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Gateway-to-App PE route is blocked/unapproved

**Procedure:**

1. Use paired positive control AZ-T56-01 (Gateway to App PE).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-03 — App to OpenAI PE (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/app-to-openai-pe.json && jq -e '.result == "Pass" and .port == 443' evidence/network/app-to-openai-pe.json
```

**Expected result:** Authenticated App Service test reaches OpenAI PE over approved route; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** AI dependency cannot be reached privately

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/app-to-openai-pe.json && jq -e '.result == "Pass" and .port == 443' evidence/network/app-to-openai-pe.json
4. Check the actual observation against the signed criterion: Authenticated App Service test reaches OpenAI PE over approved route.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-04 — App to OpenAI PE (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** AI dependency cannot be reached privately

**Procedure:**

1. Use paired positive control AZ-T56-03 (App to OpenAI PE).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-05 — App to Search PE (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/app-to-search-pe.json && jq -e '.result == "Pass" and .port == 443' evidence/network/app-to-search-pe.json
```

**Expected result:** Authenticated App Service test reaches Search PE over approved route; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Search dependency cannot be reached privately

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/app-to-search-pe.json && jq -e '.result == "Pass" and .port == 443' evidence/network/app-to-search-pe.json
4. Check the actual observation against the signed criterion: Authenticated App Service test reaches Search PE over approved route.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-06 — App to Search PE (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Search dependency cannot be reached privately

**Procedure:**

1. Use paired positive control AZ-T56-05 (App to Search PE).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-07 — App to Cosmos PE (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/app-to-cosmos-pe.json && jq -e '.result == "Pass" and .port == 443' evidence/network/app-to-cosmos-pe.json
```

**Expected result:** Authenticated App Service test reaches Cosmos PE over approved route; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Cosmos dependency cannot be reached privately

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/app-to-cosmos-pe.json && jq -e '.result == "Pass" and .port == 443' evidence/network/app-to-cosmos-pe.json
4. Check the actual observation against the signed criterion: Authenticated App Service test reaches Cosmos PE over approved route.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-08 — App to Cosmos PE (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Cosmos dependency cannot be reached privately

**Procedure:**

1. Use paired positive control AZ-T56-07 (App to Cosmos PE).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-09 — Unauthorized subnet denial (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/unauthorized-subnet.json && jq -e '.blocked == true and .test_segment' evidence/network/unauthorized-subnet.json
```

**Expected result:** Isolated unauthorized subnet cannot reach restricted PE operations; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Unauthorized subnet reaches PE

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/unauthorized-subnet.json && jq -e '.blocked == true and .test_segment' evidence/network/unauthorized-subnet.json
4. Check the actual observation against the signed criterion: Isolated unauthorized subnet cannot reach restricted PE operations.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-10 — Unauthorized subnet denial (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Unauthorized subnet reaches PE

**Procedure:**

1. Use paired positive control AZ-T56-09 (Unauthorized subnet denial).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-11 — NSG rule precedence (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network nsg rule list -g "$RG" --nsg-name "$PE_NSG_NAME" -o json
```

**Expected result:** Effective NSG priorities enforce signed allow/deny policy; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Shadowing or broad NSG permit bypasses boundary

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network nsg rule list -g "$RG" --nsg-name "$PE_NSG_NAME" -o json
4. Check the actual observation against the signed criterion: Effective NSG priorities enforce signed allow/deny policy.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-12 — NSG rule precedence (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Shadowing or broad NSG permit bypasses boundary

**Procedure:**

1. Use paired positive control AZ-T56-11 (NSG rule precedence).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-13 — ASG and PE associations (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network private-endpoint show -g "$RG" -n "$PE_APP_NAME" --query applicationSecurityGroups -o json
```

**Expected result:** ASG associations and PE network policy semantics match signed configuration; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Unapproved ASG or PE subnet policy is deployed

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network private-endpoint show -g "$RG" -n "$PE_APP_NAME" --query applicationSecurityGroups -o json
4. Check the actual observation against the signed criterion: ASG associations and PE network policy semantics match signed configuration.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-14 — ASG and PE associations (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Unapproved ASG or PE subnet policy is deployed

**Procedure:**

1. Use paired positive control AZ-T56-13 (ASG and PE associations).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-15 — Private Endpoint route table (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az network route-table route list -g "$RG" --route-table-name "$PE_ROUTE_TABLE" -o json
```

**Expected result:** PE subnet UDR/next hop matches reviewed network policy; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** UDR sends protected traffic to wrong hop

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az network route-table route list -g "$RG" --route-table-name "$PE_ROUTE_TABLE" -o json
4. Check the actual observation against the signed criterion: PE subnet UDR/next hop matches reviewed network policy.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-16 — Private Endpoint route table (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** UDR sends protected traffic to wrong hop

**Procedure:**

1. Use paired positive control AZ-T56-15 (Private Endpoint route table).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-17 — Application identity authorization (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az role assignment list --assignee "$WEBAPP_PRINCIPAL_ID" --all -o json
```

**Expected result:** Network-only access does not substitute for narrow Managed Identity RBAC; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Service accepts calls from unauthorized identity

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az role assignment list --assignee "$WEBAPP_PRINCIPAL_ID" --all -o json
4. Check the actual observation against the signed criterion: Network-only access does not substitute for narrow Managed Identity RBAC.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-18 — Application identity authorization (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Service accepts calls from unauthorized identity

**Procedure:**

1. Use paired positive control AZ-T56-17 (Application identity authorization).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-19 — VNet Flow Logs correlation (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/flow-logs.json && jq -e '.collection_enabled == true and .correlation_id' evidence/network/flow-logs.json
```

**Expected result:** Traffic logs correlate synthetic request ID, private source and destination; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Private-path claim lacks associated flow evidence

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/flow-logs.json && jq -e '.collection_enabled == true and .correlation_id' evidence/network/flow-logs.json
4. Check the actual observation against the signed criterion: Traffic logs correlate synthetic request ID, private source and destination.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-20 — VNet Flow Logs correlation (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Private-path claim lacks associated flow evidence

**Procedure:**

1. Use paired positive control AZ-T56-19 (VNet Flow Logs correlation).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-21 — Route change detection (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/network/route-diff.json && jq -e '.unapproved_changes == 0' evidence/network/route-diff.json
```

**Expected result:** Unauthorized route modifications trigger drift or change-control alert; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Route changes occur without review

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 56.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/network/route-diff.json && jq -e '.unapproved_changes == 0' evidence/network/route-diff.json
4. Check the actual observation against the signed criterion: Unauthorized route modifications trigger drift or change-control alert.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T56-22 — Route change detection (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T56-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Route changes occur without review

**Procedure:**

1. Use paired positive control AZ-T56-21 (Route change detection).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T56-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 57: Diagnostic logging, monitoring, and alert verification

Test ID range: `AZ-T57-01` to `AZ-T57-22`.

### AZ-T57-01 — Gateway access diagnostics (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az monitor diagnostic-settings list --resource "$APPGW_ID" -o json
```

**Expected result:** Application Gateway access logs are routed to the approved workspace; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Gateway access logs are missing

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az monitor diagnostic-settings list --resource "$APPGW_ID" -o json
4. Check the actual observation against the signed criterion: Application Gateway access logs are routed to the approved workspace.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-02 — Gateway access diagnostics (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Gateway access logs are missing

**Procedure:**

1. Use paired positive control AZ-T57-01 (Gateway access diagnostics).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-03 — WAF Firewall diagnostics (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az monitor diagnostic-settings list --resource "$APPGW_ID" -o json
```

**Expected result:** Application Gateway WAF firewall events reach the approved diagnostic destination; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** WAF events are not collected

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az monitor diagnostic-settings list --resource "$APPGW_ID" -o json
4. Check the actual observation against the signed criterion: Application Gateway WAF firewall events reach the approved diagnostic destination.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-04 — WAF Firewall diagnostics (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** WAF events are not collected

**Procedure:**

1. Use paired positive control AZ-T57-03 (WAF Firewall diagnostics).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-05 — App Service diagnostics (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az monitor diagnostic-settings list --resource "$WEBAPP_ID" -o json
```

**Expected result:** Web App HTTP and platform diagnostics are enabled as required; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Application diagnostic flow is missing

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az monitor diagnostic-settings list --resource "$WEBAPP_ID" -o json
4. Check the actual observation against the signed criterion: Web App HTTP and platform diagnostics are enabled as required.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-06 — App Service diagnostics (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Application diagnostic flow is missing

**Procedure:**

1. Use paired positive control AZ-T57-05 (App Service diagnostics).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-07 — Azure OpenAI diagnostics (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az monitor diagnostic-settings list --resource "$OPENAI_ID" -o json
```

**Expected result:** Model/account usage events required by policy are collected; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** OpenAI diagnostic settings are incomplete

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az monitor diagnostic-settings list --resource "$OPENAI_ID" -o json
4. Check the actual observation against the signed criterion: Model/account usage events required by policy are collected.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-08 — Azure OpenAI diagnostics (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** OpenAI diagnostic settings are incomplete

**Procedure:**

1. Use paired positive control AZ-T57-07 (Azure OpenAI diagnostics).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-09 — Azure AI Search diagnostics (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az monitor diagnostic-settings list --resource "$SEARCH_ID" -o json
```

**Expected result:** Search diagnostics target the approved workspace and categories; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Search logging is absent

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az monitor diagnostic-settings list --resource "$SEARCH_ID" -o json
4. Check the actual observation against the signed criterion: Search diagnostics target the approved workspace and categories.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-10 — Azure AI Search diagnostics (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Search logging is absent

**Procedure:**

1. Use paired positive control AZ-T57-09 (Azure AI Search diagnostics).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-11 — Cosmos DB diagnostics (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az monitor diagnostic-settings list --resource "$COSMOS_ID" -o json
```

**Expected result:** Cosmos request/system diagnostics are configured per baseline; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Cosmos telemetry is missing

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az monitor diagnostic-settings list --resource "$COSMOS_ID" -o json
4. Check the actual observation against the signed criterion: Cosmos request/system diagnostics are configured per baseline.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-12 — Cosmos DB diagnostics (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Cosmos telemetry is missing

**Procedure:**

1. Use paired positive control AZ-T57-11 (Cosmos DB diagnostics).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-13 — Key Vault auditing (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az monitor diagnostic-settings list --resource "$VAULT_ID" -o json
```

**Expected result:** Vault secret/key access events are recorded and accessible; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Key Vault audit events are absent

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az monitor diagnostic-settings list --resource "$VAULT_ID" -o json
4. Check the actual observation against the signed criterion: Vault secret/key access events are recorded and accessible.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-14 — Key Vault auditing (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Key Vault audit events are absent

**Procedure:**

1. Use paired positive control AZ-T57-13 (Key Vault auditing).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-15 — Metric alert rules (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
az monitor metrics alert list -g "$RG" -o json
```

**Expected result:** Expected metric alerts and destinations exist and are enabled; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Critical metrics have no alert

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: az monitor metrics alert list -g "$RG" -o json
4. Check the actual observation against the signed criterion: Expected metric alerts and destinations exist and are enabled.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. Read-only Azure query requires resource ID, target-scope and signed-baseline comparison; a successfully executed command is not PASS.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-16 — Metric alert rules (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Critical metrics have no alert

**Procedure:**

1. Use paired positive control AZ-T57-15 (Metric alert rules).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-17 — Measured ingestion latency (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/monitoring/log-ingest-lag.json && jq -e '.p95_minutes <= .approved_p95_minutes' evidence/monitoring/log-ingest-lag.json
```

**Expected result:** Log arrival p95 is below an approved timestamped threshold; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Diagnostic ingestion exceeds agreed latency

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/monitoring/log-ingest-lag.json && jq -e '.p95_minutes <= .approved_p95_minutes' evidence/monitoring/log-ingest-lag.json
4. Check the actual observation against the signed criterion: Log arrival p95 is below an approved timestamped threshold.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-18 — Measured ingestion latency (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Diagnostic ingestion exceeds agreed latency

**Procedure:**

1. Use paired positive control AZ-T57-17 (Measured ingestion latency).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-19 — Retention and residency approval (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/monitoring/retention-approval.json && jq -e '.retention_days and .approved_by' docs/monitoring/retention-approval.json
```

**Expected result:** Retention duration and region follow signed regulatory requirements; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Log retention is absent or below required period

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/monitoring/retention-approval.json && jq -e '.retention_days and .approved_by' docs/monitoring/retention-approval.json
4. Check the actual observation against the signed criterion: Retention duration and region follow signed regulatory requirements.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-20 — Retention and residency approval (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Log retention is absent or below required period

**Procedure:**

1. Use paired positive control AZ-T57-19 (Retention and residency approval).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-21 — Alert notification smoke (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/monitoring/alert-delivery.json && jq -e '.result == "Pass" and .recipient' evidence/monitoring/alert-delivery.json
```

**Expected result:** Synthetic authorized alert is delivered to a verified receiver; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Alert never reaches on-call destination

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 57.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/monitoring/alert-delivery.json && jq -e '.result == "Pass" and .recipient' evidence/monitoring/alert-delivery.json
4. Check the actual observation against the signed criterion: Synthetic authorized alert is delivered to a verified receiver.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T57-22 — Alert notification smoke (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T57-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Alert never reaches on-call destination

**Procedure:**

1. Use paired positive control AZ-T57-21 (Alert notification smoke).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T57-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

## Step 58: Approved infrastructure change and deployment evidence

Test ID range: `AZ-T58-01` to `AZ-T58-22`.

### AZ-T58-01 — Federated CI identity (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/ci/oidc-claims-sanitized.json && jq -e '.federated == true and .issuer and .audience' evidence/ci/oidc-claims-sanitized.json
```

**Expected result:** CI runner uses OIDC/federation without long-lived credential; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** CI authentication depends on static client secrets

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/ci/oidc-claims-sanitized.json && jq -e '.federated == true and .issuer and .audience' evidence/ci/oidc-claims-sanitized.json
4. Check the actual observation against the signed criterion: CI runner uses OIDC/federation without long-lived credential.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-02 — Federated CI identity (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-02 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** CI authentication depends on static client secrets

**Procedure:**

1. Use paired positive control AZ-T58-01 (Federated CI identity).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-02 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-03 — Immutable approved saved plan (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/ci/saved-plan.json && jq -e '.plan_path and .approved == true' evidence/ci/saved-plan.json
```

**Expected result:** Terraform saved-plan artifact and reviewer approval bind to an immutable hash; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Plan path or approval is missing

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/ci/saved-plan.json && jq -e '.plan_path and .approved == true' evidence/ci/saved-plan.json
4. Check the actual observation against the signed criterion: Terraform saved-plan artifact and reviewer approval bind to an immutable hash.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-04 — Immutable approved saved plan (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-04 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Plan path or approval is missing

**Procedure:**

1. Use paired positive control AZ-T58-03 (Immutable approved saved plan).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-04 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-05 — Saved plan SHA-256 (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
sha256sum evidence/ci/approved.tfplan
```

**Expected result:** Executed plan bytes match exactly those approved by independent reviewers; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Applied plan hash differs from approved hash

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: sha256sum evidence/ci/approved.tfplan
4. Check the actual observation against the signed criterion: Executed plan bytes match exactly those approved by independent reviewers.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-06 — Saved plan SHA-256 (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-06 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Applied plan hash differs from approved hash

**Procedure:**

1. Use paired positive control AZ-T58-05 (Saved plan SHA-256).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-06 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-07 — Pinned source commit (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/ci/commit-approval.json && jq -e '.commit_sha and .approved_commit_sha == .commit_sha' evidence/ci/commit-approval.json
```

**Expected result:** Plan generation and approved execution reference the same source commit; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Source revision differs at apply time

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/ci/commit-approval.json && jq -e '.commit_sha and .approved_commit_sha == .commit_sha' evidence/ci/commit-approval.json
4. Check the actual observation against the signed criterion: Plan generation and approved execution reference the same source commit.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-08 — Pinned source commit (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-08 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Source revision differs at apply time

**Procedure:**

1. Use paired positive control AZ-T58-07 (Pinned source commit).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-08 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-09 — Two independent reviewers (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/ci/two-reviewers.json && jq -e '.reviewers | unique | length >= 2' evidence/ci/two-reviewers.json
```

**Expected result:** At least two distinct non-author reviewers approve exact plan hash; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Duplicate/self approval bypasses governance

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/ci/two-reviewers.json && jq -e '.reviewers | unique | length >= 2' evidence/ci/two-reviewers.json
4. Check the actual observation against the signed criterion: At least two distinct non-author reviewers approve exact plan hash.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-10 — Two independent reviewers (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-10 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Duplicate/self approval bypasses governance

**Procedure:**

1. Use paired positive control AZ-T58-09 (Two independent reviewers).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-10 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-11 — Approved apply execution evidence (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/ci/apply-result.json && jq -e '.exit_code == 0 and .run_id' evidence/ci/apply-result.json
```

**Expected result:** A separate authorized runner generated a success result and run ID; no apply is performed by this project; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Apply result is absent or untrusted

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/ci/apply-result.json && jq -e '.exit_code == 0 and .run_id' evidence/ci/apply-result.json
4. Check the actual observation against the signed criterion: A separate authorized runner generated a success result and run ID; no apply is performed by this project.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-12 — Approved apply execution evidence (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-12 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Apply result is absent or untrusted

**Procedure:**

1. Use paired positive control AZ-T58-11 (Approved apply execution evidence).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-12 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-13 — State-lock conflict protection (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/ci/state-lock.json && jq -e '.lock_behavior_tested == true and .result == "Pass"' evidence/ci/state-lock.json
```

**Expected result:** Approved isolated test confirms conflicting state operations cannot corrupt remote state; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Concurrent plan/apply bypasses locking

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/ci/state-lock.json && jq -e '.lock_behavior_tested == true and .result == "Pass"' evidence/ci/state-lock.json
4. Check the actual observation against the signed criterion: Approved isolated test confirms conflicting state operations cannot corrupt remote state.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-14 — State-lock conflict protection (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-14 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Concurrent plan/apply bypasses locking

**Procedure:**

1. Use paired positive control AZ-T58-13 (State-lock conflict protection).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-14 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-15 — CI log secret redaction (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/ci/log-redaction.json && jq -e '.tokens_leaked == 0 and .secrets_leaked == 0' evidence/ci/log-redaction.json
```

**Expected result:** CI logs and artifacts do not expose tokens, plans, or key material; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Raw credentials or sensitive plan contents are published

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/ci/log-redaction.json && jq -e '.tokens_leaked == 0 and .secrets_leaked == 0' evidence/ci/log-redaction.json
4. Check the actual observation against the signed criterion: CI logs and artifacts do not expose tokens, plans, or key material.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-16 — CI log secret redaction (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-16 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Raw credentials or sensitive plan contents are published

**Procedure:**

1. Use paired positive control AZ-T58-15 (CI log secret redaction).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-16 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-17 — Traceable change ticket (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/ci/change-record.json && jq -e '.change_id and .approver and .resource_ids' evidence/ci/change-record.json
```

**Expected result:** Change record binds reviewer, run ID, resource IDs and exact artifact hashes; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** No approved change record exists

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/ci/change-record.json && jq -e '.change_id and .approver and .resource_ids' evidence/ci/change-record.json
4. Check the actual observation against the signed criterion: Change record binds reviewer, run ID, resource IDs and exact artifact hashes.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-18 — Traceable change ticket (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-18 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** No approved change record exists

**Procedure:**

1. Use paired positive control AZ-T58-17 (Traceable change ticket).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-18 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-19 — Post-deployment zero drift (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s evidence/ci/post-apply-drift.json && jq -e '.exit_code == 0 and .state_consistent == true' evidence/ci/post-apply-drift.json
```

**Expected result:** Approved refresh-only drift check shows zero unreviewed changes; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** Drift persists after the approved change

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s evidence/ci/post-apply-drift.json && jq -e '.exit_code == 0 and .state_consistent == true' evidence/ci/post-apply-drift.json
4. Check the actual observation against the signed criterion: Approved refresh-only drift check shows zero unreviewed changes.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-20 — Post-deployment zero drift (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-20 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** Drift persists after the approved change

**Procedure:**

1. Use paired positive control AZ-T58-19 (Post-deployment zero drift).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-20 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-21 — Rollback and recovery procedure (REAL_CONFIGURATION_OR_EVIDENCE_REVIEW)

**Objective:** Assess the approved implementation against one explicit control.

**Preconditions:** An approved actual target, stable resource ID, signed baseline, CI runner access and proper reviewers are mandatory.

**Approved execution context:** Approved read-only Azure CI / protected evidence review, as applicable

**Command:**

```bash
test -s docs/ci/rollback-plan.md && sha256sum docs/ci/rollback-plan.md
```

**Expected result:** Reviewed rollback triggers, owner, version and recovery drill evidence exist; verified independent review required; otherwise NOT_READY/FAIL.

**Deviation case:** No feasible rollback or approved fallback path exists

**Procedure:**

1. Identify and authorize the exact target resource and signed baseline for Step 58.
2. Verify subscription, PIM/runner role, approved network path, tool versions, and that this command is permitted for the assigned environment.
3. Collect a scoped observation without mutating production: test -s docs/ci/rollback-plan.md && sha256sum docs/ci/rollback-plan.md
4. Check the actual observation against the signed criterion: Reviewed rollback triggers, owner, version and recovery drill evidence exist.
5. Preserve raw evidence in restricted storage and log UTC time, tool version, resource ID, source revision, and reviewer.
6. If any baseline, resource or evidence is missing => NOT_READY; verified violation => FAIL; all met => REVIEW_REQUIRED pending independent sign-off. File existence or a valid hash alone does not prove the control; inspect exact properties and signed acceptance criteria.

**Evidence:** Record the exact approved Azure resource ID, subscription, baseline version, UTC collection time, command/program version, exit status, raw restricted evidence digest, and two independent review references. Remove tokens, private keys, state files and sensitive payloads from any public artifact.

**Troubleshooting:** Check correct subscription, resource, Azure CLI/API version, DNS route, RBAC, baseline and log correlation. Do not treat 403, DNS error or empty output as success.

**Live acceptance:** `NOT_READY` (no Azure evidence).

### AZ-T58-22 — Rollback and recovery procedure (SYNTHETIC_DEVIATION)

**Objective:** Prove the offline validator flags a synthetic deviation; do not make a live acceptance claim.

**Preconditions:** Pinned synthetic spec and Python 3; no Azure credentials.

**Approved execution context:** Local WSL / isolated offline runner (no Azure authentication)

**Command:**

```bash
python3 scripts/phase5_guard.py --selftest AZ-T58-22 --spec specs/phase5_286_en.json
```

**Expected result:** Synthetic adverse observation => Fail; absent observation => NotReady. No inference about real Azure isolation.

**Deviation case:** No feasible rollback or approved fallback path exists

**Procedure:**

1. Use paired positive control AZ-T58-21 (Rollback and recovery procedure).
2. In an isolated offline workspace, check the synthetic specification SHA-256 and evaluation rule.
3. Run: python3 scripts/phase5_guard.py --selftest AZ-T58-22 --spec specs/phase5_286_en.json
4. Verify the intentionally nonconforming fixture is classified Fail and that missing observation is NotReady.
5. Archive the synthetic output and checker hash; leave Azure live acceptance NotReady.

**Evidence:** Evidence is a synthetic fixture log, guard/version digest, and repeatable expected Fail/NotReady results; never live pass.

**Troubleshooting:** Check fixture/guard schema and input typing; classify absent fixture as NOT_READY.

**Live acceptance:** `NOT_READY` (no Azure evidence).

