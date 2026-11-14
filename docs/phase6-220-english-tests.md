# Phase 6: Post-Deployment Assurance — 220 English Tests

**Source:** 2026-11-10 frozen Phase 6 test specification; SHA-256 `ef5b39269486b293b019ef0cf8b2c9efe4b16b3ddf8b2ec7dba285a60ffd845e`.
**Assurance state:** documentation and offline detector validation only; Azure live passes = **0**; all live acceptance cases = **NOT_READY**.
**Security boundaries:** No `az login` from fixed WSL, no `terraform apply`, no unapproved WAF simulation, load test, network probe or identity mutation. Environment-specific versions and scopes remain unverified.
**Important:** 110 configuration/evidence reviews + 110 synthetic deviation detections; synthetics do not establish any live control.

## Runbook and acceptance workflow
1. Pin the signed design revision, non-production inventory, exact resource IDs, permission scopes and approved test window.
2. Choose the test executor by the **Execution class** below; do not run an Azure query from the fixed workstation.
3. Record command, UTC timestamp, exit code, sanitized raw output SHA-256, actor, pipeline job, commit, asset IDs and reviewer.
4. Compare observed values with approved baseline and an independent observation where required.
5. Report `FAIL` for a verified violation; `NOT_READY` for missing source, approval, resource, log, trusted evidence or incomplete evaluation.
6. Release only after independent approval; this offline catalogue never grants Azure `PASS`.

## Step 59 — Preflight Configuration Audit

**Coverage:** `AZ-T59-01` through `AZ-T59-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T59-01` — Public IP inventory (configuration/evidence review)

**Objective:** Verify the approved public ip inventory requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The complete scoped inventory matches signed exceptions; the private-only gateway has no public frontend IP.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network public-ip list -g "$RG" --query "[].{id:id,name:name,ip:ipAddress}" -o json
```

**Expected outcome:** The complete scoped inventory matches signed exceptions; the private-only gateway has no public frontend IP. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T59-02` — Public IP inventory (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-02 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T59-03` — PaaS public access inventory (configuration/evidence review)

**Objective:** Verify the approved paas public access inventory requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Every in-scope App Service has public network access disabled.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az graph query --subscriptions "$SUBSCRIPTION_ID" -q "Resources | where type =~ 'microsoft.web/sites' | project id, publicNetworkAccess = properties.publicNetworkAccess" -o json
```

**Expected outcome:** Every in-scope App Service has public network access disabled. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T59-04` — PaaS public access inventory (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-04 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T59-05` — Excess RBAC assignments (configuration/evidence review)

**Objective:** Verify the approved excess rbac assignments requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Unapproved Owner or Contributor assignments are absent at every reviewed scope.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az role assignment list --scope "$SCOPE_ID" --all -o json
```

**Expected outcome:** Unapproved Owner or Contributor assignments are absent at every reviewed scope. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T59-06` — Excess RBAC assignments (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-06 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T59-07` — Diagnostic settings (configuration/evidence review)

**Objective:** Verify the approved diagnostic settings requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Gateway log categories and destinations match the approved monitoring baseline.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az monitor diagnostic-settings list --resource "$APPGW_ID" -o json
```

**Expected outcome:** Gateway log categories and destinations match the approved monitoring baseline. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T59-08` — Diagnostic settings (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-08 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T59-09` — Policy compliance (configuration/evidence review)

**Objective:** Verify the approved policy compliance requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Deny and audit policy assignments have no unresolved in-scope noncompliance without approved exceptions.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az policy state list --resource "$RG_ID" -o json
```

**Expected outcome:** Deny and audit policy assignments have no unresolved in-scope noncompliance without approved exceptions. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T59-10` — Policy compliance (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-10 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T59-11` — Resource Graph scope (configuration/evidence review)

**Objective:** Verify the approved resource graph scope requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Subscription IDs, query timestamp, and returned assets reconcile with the approved inventory.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az graph query -q "Resources | project id,type,location,tags" -o json
```

**Expected outcome:** Subscription IDs, query timestamp, and returned assets reconcile with the approved inventory. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T59-12` — Resource Graph scope (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-12 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T59-13` — Required governance tags (configuration/evidence review)

**Objective:** Verify the approved required governance tags requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: All required Owner, Environment, and DataClassification tags are present and valid.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az group show -n "$RG" --query tags -o json
```

**Expected outcome:** All required Owner, Environment, and DataClassification tags are present and valid. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T59-14` — Required governance tags (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-14 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T59-15` — Minimum TLS policy (configuration/evidence review)

**Objective:** Verify the approved minimum tls policy requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The effective App Service minimum TLS version meets the approved threshold.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az webapp config show -g "$RG" -n "$WEBAPP_NAME" --query minTlsVersion -o tsv
```

**Expected outcome:** The effective App Service minimum TLS version meets the approved threshold. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T59-16` — Minimum TLS policy (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-16 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T59-17` — Local authentication (configuration/evidence review)

**Objective:** Verify the approved local authentication requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Azure OpenAI local key authentication is disabled when required by the approved baseline.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az cognitiveservices account show -g "$RG" -n "$OPENAI_NAME" --query properties.disableLocalAuth -o tsv
```

**Expected outcome:** Azure OpenAI local key authentication is disabled when required by the approved baseline. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T59-18` — Local authentication (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-18 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T59-19` — Exception expiry (configuration/evidence review)

**Objective:** Verify the approved exception expiry requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Every exception has a ticket, expiry, accountable owner, and recorded approval.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".exceptions | all(.ticket and .expires_at and .owner and .approved == true)" docs/security/approved-exceptions.json
```

**Expected outcome:** Every exception has a ticket, expiry, accountable owner, and recorded approval. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T59-20` — Exception expiry (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-20 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T59-21` — Audit provenance (configuration/evidence review)

**Objective:** Verify the approved audit provenance requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 59, test AZ-T59-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Audit inventory includes resource scope, UTC collection time, and SHA-256 evidence integrity.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
test -s evidence/phase6/config-audit-manifest.json && sha256sum evidence/phase6/config-audit-manifest.json
```

**Expected outcome:** Audit inventory includes resource scope, UTC collection time, and SHA-256 evidence integrity. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T59-22` — Audit provenance (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T59-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T59-22 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 60 — Private Endpoint Configuration Audit

**Coverage:** `AZ-T60-01` through `AZ-T60-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T60-01` — Private endpoint approval (configuration/evidence review)

**Objective:** Verify the approved private endpoint approval requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Every required private endpoint connection is in Approved state.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network private-endpoint show -g "$RG" -n "$PE_NAME" --query "privateLinkServiceConnections[].privateLinkServiceConnectionState.status" -o json
```

**Expected outcome:** Every required private endpoint connection is in Approved state. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T60-02` — Private endpoint approval (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-02 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T60-03` — Subresource mapping (configuration/evidence review)

**Objective:** Verify the approved subresource mapping requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Each endpoint's group ID matches the approved service-specific subresource.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network private-endpoint show -g "$RG" -n "$PE_NAME" --query "privateLinkServiceConnections[].groupIds" -o json
```

**Expected outcome:** Each endpoint's group ID matches the approved service-specific subresource. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T60-04` — Subresource mapping (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-04 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T60-05` — Endpoint NIC linkage (configuration/evidence review)

**Objective:** Verify the approved endpoint nic linkage requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Each private endpoint references the expected network interface.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network nic show --ids "$PE_NIC_ID" --query "{id:id,ipConfigs:ipConfigurations}" -o json
```

**Expected outcome:** Each private endpoint references the expected network interface. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T60-06` — Endpoint NIC linkage (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-06 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T60-07` — Endpoint private IP (configuration/evidence review)

**Objective:** Verify the approved endpoint private ip requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Each endpoint NIC address matches the signed IPAM allocation.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network nic show --ids "$PE_NIC_ID" --query "ipConfigurations[].privateIPAddress" -o json
```

**Expected outcome:** Each endpoint NIC address matches the signed IPAM allocation. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T60-08` — Endpoint private IP (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-08 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T60-09` — DNS zone group (configuration/evidence review)

**Objective:** Verify the approved dns zone group requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Each private endpoint has the correct service-specific private DNS zone group.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network private-endpoint dns-zone-group list -g "$RG" --endpoint-name "$PE_NAME" -o json
```

**Expected outcome:** Each private endpoint has the correct service-specific private DNS zone group. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T60-10` — DNS zone group (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-10 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T60-11` — Endpoint VNet mapping (configuration/evidence review)

**Objective:** Verify the approved endpoint vnet mapping requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Virtual network and subnet resource IDs equal the approved topology.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network private-endpoint show -g "$RG" -n "$PE_NAME" --query subnet.id -o tsv
```

**Expected outcome:** Virtual network and subnet resource IDs equal the approved topology. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T60-12` — Endpoint VNet mapping (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-12 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T60-13` — Endpoint subnet policy (configuration/evidence review)

**Objective:** Verify the approved endpoint subnet policy requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Network policies and attached NSG/UDR match the approved subnet design.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network vnet subnet show --ids "$PE_SUBNET_ID" --query "{id:id,privateEndpointNetworkPolicies:privateEndpointNetworkPolicies}" -o json
```

**Expected outcome:** Network policies and attached NSG/UDR match the approved subnet design. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T60-14` — Endpoint subnet policy (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-14 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T60-15` — Endpoint DNS linkage (configuration/evidence review)

**Objective:** Verify the approved endpoint dns linkage requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Every private endpoint DNS record resolves to its registered NIC private IP.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network private-dns record-set a list -g "$DNS_RG" -z "$PE_ZONE" -o json
```

**Expected outcome:** Every private endpoint DNS record resolves to its registered NIC private IP. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T60-16` — Endpoint DNS linkage (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-16 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T60-17` — Duplicate IP detection (configuration/evidence review)

**Objective:** Verify the approved duplicate ip detection requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: No unintended duplicate private IP mappings exist in the endpoint inventory.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e "[.[].private_ip] | length == (unique | length)" evidence/phase6/approved-pe-map.json
```

**Expected outcome:** No unintended duplicate private IP mappings exist in the endpoint inventory. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T60-18` — Duplicate IP detection (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-18 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T60-19` — Unknown private endpoints (configuration/evidence review)

**Objective:** Verify the approved unknown private endpoints requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Every discovered endpoint is accounted for in the approved inventory.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network private-endpoint list -g "$RG" -o json
```

**Expected outcome:** Every discovered endpoint is accounted for in the approved inventory. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T60-20` — Unknown private endpoints (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-20 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T60-21` — Endpoint configuration drift (configuration/evidence review)

**Objective:** Verify the approved endpoint configuration drift requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 60, test AZ-T60-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: A read-only detailed-exitcode plan indicates no unauthorized private endpoint drift.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
```

**Expected outcome:** A read-only detailed-exitcode plan indicates no unauthorized private endpoint drift. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Pinned Terraform/provider versions and approved remote state; no apply or destroy

### `AZ-T60-22` — Endpoint configuration drift (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T60-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T60-22 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 61 — Internal Private DNS Resolution

**Coverage:** `AZ-T61-01` through `AZ-T61-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T61-01` — App Service production hostname (configuration/evidence review)

**Objective:** Verify the approved app service production hostname requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Normal App Service hostname resolves from an internal runner to its approved private endpoint IP.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
dig +short "$APP_FQDN" A
```

**Expected outcome:** Normal App Service hostname resolves from an internal runner to its approved private endpoint IP. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T61-02` — App Service production hostname (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-02 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T61-03` — SCM/Kudu hostname (configuration/evidence review)

**Objective:** Verify the approved scm/kudu hostname requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Internal resolution for the SCM hostname matches the approved private endpoint address.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
dig +short "$SCM_FQDN" A
```

**Expected outcome:** Internal resolution for the SCM hostname matches the approved private endpoint address. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T61-04` — SCM/Kudu hostname (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-04 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T61-05` — Azure OpenAI hostname (configuration/evidence review)

**Objective:** Verify the approved azure openai hostname requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Normal OpenAI service hostname resolves to its approved private endpoint IP.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
dig +short "$OPENAI_FQDN" A
```

**Expected outcome:** Normal OpenAI service hostname resolves to its approved private endpoint IP. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T61-06` — Azure OpenAI hostname (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-06 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T61-07` — Azure AI Search hostname (configuration/evidence review)

**Objective:** Verify the approved azure ai search hostname requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Normal Search hostname resolves to its approved private endpoint IP.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
dig +short "$SEARCH_FQDN" A
```

**Expected outcome:** Normal Search hostname resolves to its approved private endpoint IP. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T61-08` — Azure AI Search hostname (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-08 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T61-09` — Cosmos DB hostname (configuration/evidence review)

**Objective:** Verify the approved cosmos db hostname requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Normal Cosmos DB hostname resolves to its approved private endpoint IP.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
dig +short "$COSMOS_FQDN" A
```

**Expected outcome:** Normal Cosmos DB hostname resolves to its approved private endpoint IP. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T61-10` — Cosmos DB hostname (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-10 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T61-11` — Key Vault hostname (configuration/evidence review)

**Objective:** Verify the approved key vault hostname requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Normal Key Vault hostname resolves to its approved private endpoint IP.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
dig +short "$VAULT_FQDN" A
```

**Expected outcome:** Normal Key Vault hostname resolves to its approved private endpoint IP. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T61-12` — Key Vault hostname (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-12 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T61-13` — Resolved-IP reconciliation (configuration/evidence review)

**Objective:** Verify the approved resolved-ip reconciliation requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Every returned address matches the authoritative private endpoint NIC inventory.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".results | all(.private_ip_verified == true and .resource_id)" evidence/phase6/dns-resolution.json
```

**Expected outcome:** Every returned address matches the authoritative private endpoint NIC inventory. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T61-14` — Resolved-IP reconciliation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-14 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T61-15` — Private-link CNAME chain (configuration/evidence review)

**Objective:** Verify the approved private-link cname chain requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Each service's CNAME chain follows the documented service-specific private-link convention.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
dig "$OPENAI_FQDN" CNAME +noall +answer
```

**Expected outcome:** Each service's CNAME chain follows the documented service-specific private-link convention. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T61-16` — Private-link CNAME chain (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-16 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T61-17` — Split-horizon DNS (configuration/evidence review)

**Objective:** Verify the approved split-horizon dns requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Internal and outside DNS observations match the documented split-horizon policy.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".internal and .external and .approved_split_horizon == true" evidence/phase6/split-horizon-review.json
```

**Expected outcome:** Internal and outside DNS observations match the documented split-horizon policy. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T61-18` — Split-horizon DNS (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-18 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T61-19` — Unexpected public resolution (configuration/evidence review)

**Objective:** Verify the approved unexpected public resolution requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: No in-scope internal query ends at an unapproved public A record.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".unexpected_public_a_records == 0" evidence/phase6/dns-exposure-audit.json
```

**Expected outcome:** No in-scope internal query ends at an unapproved public A record. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T61-20` — Unexpected public resolution (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-20 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T61-21` — DNS recovery readiness (configuration/evidence review)

**Objective:** Verify the approved dns recovery readiness requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 61, test AZ-T61-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: DNS forwarding, TTL, recovery ownership, and recovery procedure are approved.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
test -s docs/dns/rollback.md && sha256sum docs/dns/rollback.md
```

**Expected outcome:** DNS forwarding, TTL, recovery ownership, and recovery procedure are approved. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T61-22` — DNS recovery readiness (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T61-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T61-22 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 62 — External Exposure Verification

**Coverage:** `AZ-T62-01` through `AZ-T62-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T62-01` — Gateway public frontend (configuration/evidence review)

**Objective:** Verify the approved gateway public frontend requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The gateway has no configured public frontend IP reference.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query "frontendIPConfigurations[].publicIPAddress.id" -o json
```

**Expected outcome:** The gateway has no configured public frontend IP reference. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T62-02` — Gateway public frontend (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-02 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T62-03` — App Service public access (configuration/evidence review)

**Objective:** Verify the approved app service public access requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: All in-scope App Service public network access settings are Disabled.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az webapp show -g "$RG" -n "$WEBAPP_NAME" --query publicNetworkAccess -o tsv
```

**Expected outcome:** All in-scope App Service public network access settings are Disabled. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T62-04` — App Service public access (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-04 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T62-05` — Azure OpenAI public access (configuration/evidence review)

**Objective:** Verify the approved azure openai public access requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: All in-scope Azure OpenAI public network access settings are Disabled.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az cognitiveservices account show -g "$RG" -n "$OPENAI_NAME" --query properties.publicNetworkAccess -o tsv
```

**Expected outcome:** All in-scope Azure OpenAI public network access settings are Disabled. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T62-06` — Azure OpenAI public access (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-06 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T62-07` — Azure AI Search public access (configuration/evidence review)

**Objective:** Verify the approved azure ai search public access requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: All in-scope Azure AI Search public network access settings are Disabled.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az search service show -g "$RG" -n "$SEARCH_NAME" --query publicNetworkAccess -o tsv
```

**Expected outcome:** All in-scope Azure AI Search public network access settings are Disabled. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T62-08` — Azure AI Search public access (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-08 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T62-09` — Cosmos DB public access (configuration/evidence review)

**Objective:** Verify the approved cosmos db public access requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: All in-scope Cosmos DB public network access settings are Disabled.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az cosmosdb show -g "$RG" -n "$COSMOS_NAME" --query publicNetworkAccess -o tsv
```

**Expected outcome:** All in-scope Cosmos DB public network access settings are Disabled. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T62-10` — Cosmos DB public access (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-10 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T62-11` — Key Vault public access (configuration/evidence review)

**Objective:** Verify the approved key vault public access requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: All in-scope Key Vault public network access settings are Disabled.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az keyvault show -n "$VAULT_NAME" --query properties.publicNetworkAccess -o tsv
```

**Expected outcome:** All in-scope Key Vault public network access settings are Disabled. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T62-12` — Key Vault public access (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-12 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T62-13` — External DNS observation (configuration/evidence review)

**Objective:** Verify the approved external dns observation requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Off-network DNS evidence shows no unapproved public application endpoint.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
dig +short "$APPGW_FQDN" A
```

**Expected outcome:** Off-network DNS evidence shows no unapproved public application endpoint. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T62-14` — External DNS observation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-14 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T62-15` — Off-network HTTPS observation (configuration/evidence review)

**Objective:** Verify the approved off-network https observation requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Outside clients cannot use the protected application entry point, corroborated by actual resource configuration.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
curl --connect-timeout 5 --max-time 15 --output /dev/null --write-out "%{http_code}
" "https://$APPGW_FQDN/healthz"
```

**Expected outcome:** Outside clients cannot use the protected application entry point, corroborated by actual resource configuration. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T62-16` — Off-network HTTPS observation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-16 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T62-17` — Not-deployed false-green prevention (configuration/evidence review)

**Objective:** Verify the approved not-deployed false-green prevention requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Confirm the asset exists before evaluating a negative test; absent assets are NOT_READY.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query id -o tsv
```

**Expected outcome:** Confirm the asset exists before evaluating a negative test; absent assets are NOT_READY. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T62-18` — Not-deployed false-green prevention (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-18 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T62-19` — Configuration plus external observations (configuration/evidence review)

**Objective:** Verify the approved configuration plus external observations requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Network configuration and independently collected external observations jointly support the conclusion.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".control_plane_confirmed == true and .external_probe_observed == true and .unauthorized_public_path_count == 0" evidence/phase6/exposure-audit.json
```

**Expected outcome:** Network configuration and independently collected external observations jointly support the conclusion. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T62-20` — Configuration plus external observations (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-20 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T62-21` — Exposure review record (configuration/evidence review)

**Objective:** Verify the approved exposure review record requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 62, test AZ-T62-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Signed report names test scope, UTC time, network vantage point, and reviewer.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
test -s evidence/phase6/exposure-audit.json && sha256sum evidence/phase6/exposure-audit.json
```

**Expected outcome:** Signed report names test scope, UTC time, network vantage point, and reviewer. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T62-22` — Exposure review record (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T62-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T62-22 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 63 — Denial and Failure Classification

**Coverage:** `AZ-T63-01` through `AZ-T63-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T63-01` — Unprovisioned DNS classification (configuration/evidence review)

**Objective:** Verify the approved unprovisioned dns classification requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: An unprovisioned hostname or NXDOMAIN outcome is NOT_READY, never PASS.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_result_classifier.py --input evidence/phase6/classification/nxdomain.json --expected NotReady
```

**Expected outcome:** An unprovisioned hostname or NXDOMAIN outcome is NOT_READY, never PASS. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T63-02` — Unprovisioned DNS classification (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-02 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T63-03` — Unexpected public DNS classification (configuration/evidence review)

**Objective:** Verify the approved unexpected public dns classification requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: A DNS response to an unapproved public IP is FAIL.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_result_classifier.py --input evidence/phase6/classification/public-ip.json --expected Fail
```

**Expected outcome:** A DNS response to an unapproved public IP is FAIL. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T63-04` — Unexpected public DNS classification (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-04 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T63-05` — HTTP 403 classification (configuration/evidence review)

**Objective:** Verify the approved http 403 classification requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: HTTP 403 alone does not prove a private-only application: NOT_READY without other evidence.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_result_classifier.py --input evidence/phase6/classification/403.json --expected NotReady
```

**Expected outcome:** HTTP 403 alone does not prove a private-only application: NOT_READY without other evidence. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T63-06` — HTTP 403 classification (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-06 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T63-07` — Timeout classification (configuration/evidence review)

**Objective:** Verify the approved timeout classification requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: A connection timeout alone is NOT_READY until its cause and target configuration are known.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_result_classifier.py --input evidence/phase6/classification/timeout.json --expected NotReady
```

**Expected outcome:** A connection timeout alone is NOT_READY until its cause and target configuration are known. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T63-08` — Timeout classification (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-08 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T63-09` — Internal TLS failure classification (configuration/evidence review)

**Objective:** Verify the approved internal tls failure classification requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Invalid certificates in internal permitted connections are FAIL.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_result_classifier.py --input evidence/phase6/classification/tls-error.json --expected Fail
```

**Expected outcome:** Invalid certificates in internal permitted connections are FAIL. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T63-10` — Internal TLS failure classification (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-10 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T63-11` — Unauthorized external HTTP 200 (configuration/evidence review)

**Objective:** Verify the approved unauthorized external http 200 requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Unexpected externally accessible HTTP 200 is FAIL.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_result_classifier.py --input evidence/phase6/classification/200.json --expected Fail
```

**Expected outcome:** Unexpected externally accessible HTTP 200 is FAIL. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T63-12` — Unauthorized external HTTP 200 (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-12 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T63-13` — Refused connection classification (configuration/evidence review)

**Objective:** Verify the approved refused connection classification requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: An isolated refusal is NOT_READY without corroborated configuration and reachability.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_result_classifier.py --input evidence/phase6/classification/refused.json --expected NotReady
```

**Expected outcome:** An isolated refusal is NOT_READY without corroborated configuration and reachability. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T63-14` — Refused connection classification (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-14 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T63-15` — Missing-evidence classification (configuration/evidence review)

**Objective:** Verify the approved missing-evidence classification requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Missing required evidence results in NOT_READY.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_result_classifier.py --input evidence/phase6/classification/missing-evidence.json --expected NotReady
```

**Expected outcome:** Missing required evidence results in NOT_READY. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T63-16` — Missing-evidence classification (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-16 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T63-17` — Undeployed baseline classification (configuration/evidence review)

**Objective:** Verify the approved undeployed baseline classification requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: A resource that does not yet exist remains NOT_READY.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_result_classifier.py --input evidence/phase6/classification/not-provisioned.json --expected NotReady
```

**Expected outcome:** A resource that does not yet exist remains NOT_READY. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T63-18` — Undeployed baseline classification (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-18 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T63-19` — Corroborated blocked-path verdict (configuration/evidence review)

**Objective:** Verify the approved corroborated blocked-path verdict requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Only a configured asset plus matching external and configuration evidence may be eligible for approval.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_result_classifier.py --input evidence/phase6/classification/correlated.json --expected Pass
```

**Expected outcome:** Only a configured asset plus matching external and configuration evidence may be eligible for approval. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T63-20` — Corroborated blocked-path verdict (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-20 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T63-21` — Versioned classification rubric (configuration/evidence review)

**Objective:** Verify the approved versioned classification rubric requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 63, test AZ-T63-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The denial-state classification rubric has an approved immutable revision.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".schema_version and .approved_by and .classification_table_sha256" docs/qa/network-denial-classification.json
```

**Expected outcome:** The denial-state classification rubric has an approved immutable revision. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T63-22` — Versioned classification rubric (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T63-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T63-22 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 64 — Internal Playwright End-to-End Tests

**Coverage:** `AZ-T64-01` through `AZ-T64-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T64-01` — Private gateway HTTPS (configuration/evidence review)

**Objective:** Verify the approved private gateway https requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Internal runner receives the expected HTTPS application response through the private gateway.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
npx playwright test tests/phase6/phase6.spec.ts --project=internal --grep "AZ-T64-01"
```

**Expected outcome:** Internal runner receives the expected HTTPS application response through the private gateway. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T64-02` — Private gateway HTTPS (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-02 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T64-03` — TLS certificate validation (configuration/evidence review)

**Objective:** Verify the approved tls certificate validation requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The approved hostname, chain, expiry and TLS validation all pass without insecure bypasses.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
npx playwright test tests/phase6/phase6.spec.ts --project=internal --grep "AZ-T64-03"
```

**Expected outcome:** The approved hostname, chain, expiry and TLS validation all pass without insecure bypasses. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T64-04` — TLS certificate validation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-04 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T64-05` — User sign-in integration (configuration/evidence review)

**Objective:** Verify the approved user sign-in integration requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Approved application authentication and an authorized sign-in scenario work on the real source-integrated application.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
npx playwright test tests/phase6/phase6.spec.ts --project=internal --grep "AZ-T64-05"
```

**Expected outcome:** Approved application authentication and an authorized sign-in scenario work on the real source-integrated application. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T64-06` — User sign-in integration (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-06 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T64-07` — Application health endpoint (configuration/evidence review)

**Objective:** Verify the approved application health endpoint requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The internal /healthz endpoint gives the approved HTTP status under the intended authentication policy.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
npx playwright test tests/phase6/phase6.spec.ts --project=internal --grep "AZ-T64-07"
```

**Expected outcome:** The internal /healthz endpoint gives the approved HTTP status under the intended authentication policy. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T64-08` — Application health endpoint (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-08 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T64-09` — Primary application page (configuration/evidence review)

**Objective:** Verify the approved primary application page requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The main page renders and mandatory DOM elements are visible.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
npx playwright test tests/phase6/phase6.spec.ts --project=internal --grep "AZ-T64-09"
```

**Expected outcome:** The main page renders and mandatory DOM elements are visible. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T64-10` — Primary application page (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-10 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T64-11` — Search feature test (configuration/evidence review)

**Objective:** Verify the approved search feature test requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Search UI returns expected synthetic test-data results.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
npx playwright test tests/phase6/phase6.spec.ts --project=internal --grep "AZ-T64-11"
```

**Expected outcome:** Search UI returns expected synthetic test-data results. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T64-12` — Search feature test (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-12 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T64-13` — Chat feature test (configuration/evidence review)

**Objective:** Verify the approved chat feature test requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Chat UI processes safe test input with approved sanitization and no sensitive logging.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
npx playwright test tests/phase6/phase6.spec.ts --project=internal --grep "AZ-T64-13"
```

**Expected outcome:** Chat UI processes safe test input with approved sanitization and no sensitive logging. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T64-14` — Chat feature test (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-14 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T64-15` — Session expiration handling (configuration/evidence review)

**Objective:** Verify the approved session expiration handling requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: After expiration or revocation, unauthorized session reuse is rejected and authentication is required.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
npx playwright test tests/phase6/phase6.spec.ts --project=internal --grep "AZ-T64-15"
```

**Expected outcome:** After expiration or revocation, unauthorized session reuse is rejected and authentication is required. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T64-16` — Session expiration handling (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-16 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T64-17` — Safe error responses (configuration/evidence review)

**Objective:** Verify the approved safe error responses requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Error paths disclose no tokens, credentials, prompts, stack traces or protected data.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
npx playwright test tests/phase6/phase6.spec.ts --project=internal --grep "AZ-T64-17"
```

**Expected outcome:** Error paths disclose no tokens, credentials, prompts, stack traces or protected data. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T64-18` — Safe error responses (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-18 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T64-19` — Playwright trace retention (configuration/evidence review)

**Objective:** Verify the approved playwright trace retention requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: JUnit, test trace, runner, and environment identifiers are stored with verified provenance.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
test -s evidence/phase6/playwright/junit.xml && sha256sum evidence/phase6/playwright/junit.xml
```

**Expected outcome:** JUnit, test trace, runner, and environment identifiers are stored with verified provenance. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T64-20` — Playwright trace retention (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-20 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T64-21` — Gateway backend health (configuration/evidence review)

**Objective:** Verify the approved gateway backend health requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 64, test AZ-T64-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The intended private backend is Healthy with corroborating gateway configuration.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network application-gateway show-backend-health -g "$RG" -n "$APPGW_NAME" -o json
```

**Expected outcome:** The intended private backend is Healthy with corroborating gateway configuration. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T64-22` — Gateway backend health (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T64-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T64-22 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 65 — Private AI Dependency Connectivity

**Coverage:** `AZ-T65-01` through `AZ-T65-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T65-01` — Managed-identity token for OpenAI (configuration/evidence review)

**Objective:** Verify the approved managed-identity token for openai requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The application uses a managed-identity access token for OpenAI with appropriate audience and scope.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".openai.managed_identity == true and .openai.token_acquired == true" evidence/phase6/app-dependencies.json
```

**Expected outcome:** The application uses a managed-identity access token for OpenAI with appropriate audience and scope. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T65-02` — Managed-identity token for OpenAI (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-02 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T65-03` — Managed-identity token for Search (configuration/evidence review)

**Objective:** Verify the approved managed-identity token for search requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The application authenticates to Search using managed identity.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".search.managed_identity == true and .search.token_acquired == true" evidence/phase6/app-dependencies.json
```

**Expected outcome:** The application authenticates to Search using managed identity. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T65-04` — Managed-identity token for Search (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-04 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T65-05` — Managed-identity token for Cosmos DB (configuration/evidence review)

**Objective:** Verify the approved managed-identity token for cosmos db requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The application authenticates to Cosmos data plane using managed identity.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".cosmos.managed_identity == true and .cosmos.token_acquired == true" evidence/phase6/app-dependencies.json
```

**Expected outcome:** The application authenticates to Cosmos data plane using managed identity. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T65-06` — Managed-identity token for Cosmos DB (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-06 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T65-07` — Live OpenAI call (configuration/evidence review)

**Objective:** Verify the approved live openai call requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: A sanitized request reaches the approved deployment with the expected successful response.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".openai.http_code == 200 and .openai.deployment_id" evidence/phase6/app-dependencies.json
```

**Expected outcome:** A sanitized request reaches the approved deployment with the expected successful response. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T65-08` — Live OpenAI call (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-08 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T65-09` — Search smoke query (configuration/evidence review)

**Objective:** Verify the approved search smoke query requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: A minimal search on synthetic indexed data returns the expected result.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".search.query_ok == true and .search.index_name" evidence/phase6/app-dependencies.json
```

**Expected outcome:** A minimal search on synthetic indexed data returns the expected result. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T65-10` — Search smoke query (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-10 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T65-11` — Cosmos NoSQL read (configuration/evidence review)

**Objective:** Verify the approved cosmos nosql read requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: An authorized benign Cosmos SQL API read succeeds with the expected synthetic record.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".cosmos.read_ok == true and .cosmos.container_id" evidence/phase6/app-dependencies.json
```

**Expected outcome:** An authorized benign Cosmos SQL API read succeeds with the expected synthetic record. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T65-12` — Cosmos NoSQL read (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-12 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T65-13` — Private DNS and endpoint route (configuration/evidence review)

**Objective:** Verify the approved private dns and endpoint route requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: DNS resolution and the actual network path to each service correspond to its approved private endpoint.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".network.private_dns_verified == true and .network.pe_nic_ip_verified == true" evidence/phase6/app-dependencies.json
```

**Expected outcome:** DNS resolution and the actual network path to each service correspond to its approved private endpoint. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T65-14` — Private DNS and endpoint route (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-14 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T65-15` — Sanitized prompt fixture (configuration/evidence review)

**Objective:** Verify the approved sanitized prompt fixture requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Only synthetic, approved, non-personal input is used for the smoke test.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".payload.synthetic == true and .payload.contains_personal_data == false" evidence/phase6/app-dependencies.json
```

**Expected outcome:** Only synthetic, approved, non-personal input is used for the smoke test. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T65-16` — Sanitized prompt fixture (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-16 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T65-17` — Secret-free application logging (configuration/evidence review)

**Objective:** Verify the approved secret-free application logging requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Stored logs contain no access tokens or full protected prompt contents.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".logging.token_logged == false and .logging.prompt_logged == false" evidence/phase6/app-dependencies.json
```

**Expected outcome:** Stored logs contain no access tokens or full protected prompt contents. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T65-18` — Secret-free application logging (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-18 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T65-19` — Dependency timeout behavior (configuration/evidence review)

**Objective:** Verify the approved dependency timeout behavior requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Dependency calls use bounded retries and an approved timeout/failure behavior.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".timeouts.handled == true and .timeouts.retry_bounded == true" evidence/phase6/app-dependencies.json
```

**Expected outcome:** Dependency calls use bounded retries and an approved timeout/failure behavior. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T65-20` — Dependency timeout behavior (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-20 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T65-21` — Cross-service evidence correlation (configuration/evidence review)

**Objective:** Verify the approved cross-service evidence correlation requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 65, test AZ-T65-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Application response, correlation ID, resource ID, UTC timestamp and service-side evidence reconcile.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
test -s evidence/phase6/app-dependencies.json && sha256sum evidence/phase6/app-dependencies.json
```

**Expected outcome:** Application response, correlation ID, resource ID, UTC timestamp and service-side evidence reconcile. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T65-22` — Cross-service evidence correlation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T65-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T65-22 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 66 — Managed Identity and Least-Privilege RBAC

**Coverage:** `AZ-T66-01` through `AZ-T66-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T66-01` — Authorized application principal (configuration/evidence review)

**Objective:** Verify the approved authorized application principal requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The application managed-identity principal ID matches the authorized inventory.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az webapp identity show -g "$RG" -n "$WEBAPP_NAME" -o json
```

**Expected outcome:** The application managed-identity principal ID matches the authorized inventory. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T66-02` — Authorized application principal (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-02 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T66-03` — Least-privilege OpenAI assignment (configuration/evidence review)

**Objective:** Verify the approved least-privilege openai assignment requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The required OpenAI data-plane role is assigned at the smallest approved scope.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az role assignment list --assignee "$APP_PRINCIPAL_ID" --scope "$OPENAI_ID" -o json
```

**Expected outcome:** The required OpenAI data-plane role is assigned at the smallest approved scope. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T66-04` — Least-privilege OpenAI assignment (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-04 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T66-05` — Least-privilege Search assignment (configuration/evidence review)

**Objective:** Verify the approved least-privilege search assignment requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Required Search data-plane read role is assigned at the smallest approved scope.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az role assignment list --assignee "$APP_PRINCIPAL_ID" --scope "$SEARCH_ID" -o json
```

**Expected outcome:** Required Search data-plane read role is assigned at the smallest approved scope. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T66-06` — Least-privilege Search assignment (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-06 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T66-07` — Cosmos SQL data-plane assignment (configuration/evidence review)

**Objective:** Verify the approved cosmos sql data-plane assignment requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Cosmos SQL role definition, principal and assignment scope match approved requirements.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az cosmosdb sql role assignment list -g "$RG" -a "$COSMOS_NAME" -o json
```

**Expected outcome:** Cosmos SQL role definition, principal and assignment scope match approved requirements. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T66-08` — Cosmos SQL data-plane assignment (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-08 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T66-09` — Unauthorized OpenAI identity (configuration/evidence review)

**Objective:** Verify the approved unauthorized openai identity requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: An isolated, unprivileged test identity is denied the unauthorized OpenAI operation.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".unapproved_identity.openai_http_status == 403 and .isolation == true" evidence/phase6/rbac-deny.json
```

**Expected outcome:** An isolated, unprivileged test identity is denied the unauthorized OpenAI operation. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T66-10` — Unauthorized OpenAI identity (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-10 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T66-11` — Unauthorized Search identity (configuration/evidence review)

**Objective:** Verify the approved unauthorized search identity requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: An isolated, unprivileged test identity is denied the unauthorized Search operation.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".unapproved_identity.search_http_status == 403 and .isolation == true" evidence/phase6/rbac-deny.json
```

**Expected outcome:** An isolated, unprivileged test identity is denied the unauthorized Search operation. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T66-12` — Unauthorized Search identity (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-12 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T66-13` — Unauthorized Cosmos identity (configuration/evidence review)

**Objective:** Verify the approved unauthorized cosmos identity requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: An isolated, unprivileged test identity is denied unauthorized Cosmos SQL access.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".unapproved_identity.cosmos_http_status == 403 and .isolation == true" evidence/phase6/rbac-deny.json
```

**Expected outcome:** An isolated, unprivileged test identity is denied unauthorized Cosmos SQL access. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T66-14` — Unauthorized Cosmos identity (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-14 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T66-15` — Role assignment scope (configuration/evidence review)

**Objective:** Verify the approved role assignment scope requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: All effective assignments are independently reviewed for least privilege.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".role_scope_minimized == true and .reviewed_by" evidence/phase6/rbac-scope.json
```

**Expected outcome:** All effective assignments are independently reviewed for least privilege. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T66-16` — Role assignment scope (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-16 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T66-17` — Test principal isolation (configuration/evidence review)

**Objective:** Verify the approved test principal isolation requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Negative identity tests use only an explicitly authorized isolated non-production principal.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".test_environment_isolated == true and .synthetic_id == true" evidence/phase6/rbac-deny.json
```

**Expected outcome:** Negative identity tests use only an explicitly authorized isolated non-production principal. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T66-18` — Test principal isolation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-18 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T66-19` — No production role changes (configuration/evidence review)

**Objective:** Verify the approved no production role changes requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The identity test does not modify any production role assignments.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".production_role_changes == 0" evidence/phase6/rbac-deny.json
```

**Expected outcome:** The identity test does not modify any production role assignments. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T66-20` — No production role changes (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-20 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T66-21` — Paired authorization evidence (configuration/evidence review)

**Objective:** Verify the approved paired authorization evidence requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 66, test AZ-T66-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Both allowed and denied cases retain corresponding HTTP/audit logs and correlation IDs.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
test -s evidence/phase6/rbac-deny.json && sha256sum evidence/phase6/rbac-deny.json
```

**Expected outcome:** Both allowed and denied cases retain corresponding HTTP/audit logs and correlation IDs. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T66-22` — Paired authorization evidence (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T66-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T66-22 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 67 — Gateway Diagnostics and Network Troubleshooting

**Coverage:** `AZ-T67-01` through `AZ-T67-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T67-01` — Private gateway diagnostic limitations (configuration/evidence review)

**Objective:** Verify the approved private gateway diagnostic limitations requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The test plan does not depend on unsupported private gateway Network Watcher diagnostics.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".private_gateway_network_watcher_limitation_acknowledged == true" evidence/phase6/network-troubleshooting.json
```

**Expected outcome:** The test plan does not depend on unsupported private gateway Network Watcher diagnostics. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T67-02` — Private gateway diagnostic limitations (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-02 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T67-03` — Runner NIC IP flow (configuration/evidence review)

**Objective:** Verify the approved runner nic ip flow requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: IP flow verification on a supported runner NIC aligns with approved connectivity.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network watcher test-ip-flow -g "$RG" --vm "$RUNNER_VM_NAME" --direction Outbound --protocol TCP --local "${RUNNER_PRIVATE_IP}:50000" --remote "${APPGW_PRIVATE_IP}:443" -o json
```

**Expected outcome:** IP flow verification on a supported runner NIC aligns with approved connectivity. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T67-04` — Runner NIC IP flow (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-04 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T67-05` — Runner NIC next hop (configuration/evidence review)

**Objective:** Verify the approved runner nic next hop requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Next Hop results for the runner NIC match approved routing.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network watcher show-next-hop -g "$RG" --vm "$RUNNER_VM_NAME" --source-ip "$RUNNER_PRIVATE_IP" --dest-ip "$APPGW_PRIVATE_IP" -o json
```

**Expected outcome:** Next Hop results for the runner NIC match approved routing. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T67-06` — Runner NIC next hop (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-06 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T67-07` — Gateway backend health (configuration/evidence review)

**Objective:** Verify the approved gateway backend health requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The gateway backend is healthy and targets the intended App Service private endpoint.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network application-gateway show-backend-health -g "$RG" -n "$APPGW_NAME" -o json
```

**Expected outcome:** The gateway backend is healthy and targets the intended App Service private endpoint. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T67-08` — Gateway backend health (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-08 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T67-09` — Probe settings (configuration/evidence review)

**Objective:** Verify the approved probe settings requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Probe path, host, protocol and backend target match the approved design.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query "probes" -o json
```

**Expected outcome:** Probe path, host, protocol and backend target match the approved design. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T67-10` — Probe settings (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-10 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T67-11` — Effective NSG rules (configuration/evidence review)

**Objective:** Verify the approved effective nsg rules requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Runner effective NSG rules are captured and meet the approved least-privilege matrix.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$RUNNER_NSG" -o json
```

**Expected outcome:** Runner effective NSG rules are captured and meet the approved least-privilege matrix. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T67-12` — Effective NSG rules (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-12 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T67-13` — VNet Flow Logs (configuration/evidence review)

**Objective:** Verify the approved vnet flow logs requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Approved VNet Flow Logs are present and queryable, without dependency on deprecated NSG Flow Logs.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".vnet_flow_logs.enabled == true and .vnet_flow_logs.records_seen == true" evidence/phase6/network-troubleshooting.json
```

**Expected outcome:** Approved VNet Flow Logs are present and queryable, without dependency on deprecated NSG Flow Logs. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T67-14` — VNet Flow Logs (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-14 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T67-15` — Private endpoint approval (configuration/evidence review)

**Objective:** Verify the approved private endpoint approval requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Required private endpoint connections are Approved.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network private-endpoint show -g "$RG" -n "$PE_NAME" --query "privateLinkServiceConnections[].privateLinkServiceConnectionState.status" -o json
```

**Expected outcome:** Required private endpoint connections are Approved. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T67-16` — Private endpoint approval (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-16 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T67-17` — Cross-layer network diagnosis (configuration/evidence review)

**Objective:** Verify the approved cross-layer network diagnosis requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: DNS, endpoint NIC, NSG, routing and gateway backend evidence are correlated.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".dns_checked == true and .pe_ip_matched == true" evidence/phase6/network-troubleshooting.json
```

**Expected outcome:** DNS, endpoint NIC, NSG, routing and gateway backend evidence are correlated. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T67-18` — Cross-layer network diagnosis (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-18 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T67-19` — Gateway firewall logs (configuration/evidence review)

**Objective:** Verify the approved gateway firewall logs requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Firewall log contains the expected rule and correlation identifier.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".waf_firewall_log.checked == true and .waf_firewall_log.workspace" evidence/phase6/network-troubleshooting.json
```

**Expected outcome:** Firewall log contains the expected rule and correlation identifier. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T67-20` — Gateway firewall logs (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-20 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T67-21` — Troubleshooting evidence (configuration/evidence review)

**Objective:** Verify the approved troubleshooting evidence requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 67, test AZ-T67-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Investigation record includes UTC timestamps, owner, observations and approved remedial actions.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
test -s evidence/phase6/network-troubleshooting.json && sha256sum evidence/phase6/network-troubleshooting.json
```

**Expected outcome:** Investigation record includes UTC timestamps, owner, observations and approved remedial actions. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T67-22` — Troubleshooting evidence (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T67-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T67-22 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 68 — Remote State and Disaster Recovery

**Coverage:** `AZ-T68-01` through `AZ-T68-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T68-01` — Remote Terraform state (configuration/evidence review)

**Objective:** Verify the approved remote terraform state requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Terraform state is stored in the approved remote Blob backend, not local files.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az storage blob show --account-name "$TFSTATE_ACCOUNT" -c "$TFSTATE_CONTAINER" -n "$TFSTATE_KEY" --auth-mode login --query "{name:name,etag:properties.etag}" -o json
```

**Expected outcome:** Terraform state is stored in the approved remote Blob backend, not local files. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T68-02` — Remote Terraform state (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-02 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T68-03` — Remote state locking (configuration/evidence review)

**Objective:** Verify the approved remote state locking requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Lease acquisition and release adhere to the approved exclusive-locking process.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az storage blob show --account-name "$TFSTATE_ACCOUNT" -c "$TFSTATE_CONTAINER" -n "$TFSTATE_KEY" --auth-mode login --query "properties.lease" -o json
```

**Expected outcome:** Lease acquisition and release adhere to the approved exclusive-locking process. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T68-04` — Remote state locking (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-04 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T68-05` — State Blob versioning (configuration/evidence review)

**Objective:** Verify the approved state blob versioning requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Backend storage Blob versioning is enabled.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az storage account blob-service-properties show --account-name "$TFSTATE_ACCOUNT" --resource-group "$STATE_RG" --query isVersioningEnabled -o tsv
```

**Expected outcome:** Backend storage Blob versioning is enabled. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T68-06` — State Blob versioning (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-06 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T68-07` — State soft-delete policy (configuration/evidence review)

**Objective:** Verify the approved state soft-delete policy requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Blob soft-delete retention matches the approved recovery threshold.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az storage account blob-service-properties show --account-name "$TFSTATE_ACCOUNT" --resource-group "$STATE_RG" --query deleteRetentionPolicy -o json
```

**Expected outcome:** Blob soft-delete retention matches the approved recovery threshold. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T68-08` — State soft-delete policy (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-08 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T68-09` — Least-privilege state RBAC (configuration/evidence review)

**Objective:** Verify the approved least-privilege state rbac requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: State access rights are limited to named, authorized automation identities.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az role assignment list --scope "$TFSTATE_ACCOUNT_ID" -o json
```

**Expected outcome:** State access rights are limited to named, authorized automation identities. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T68-10` — Least-privilege state RBAC (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-10 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T68-11` — Drift detailed exit code (configuration/evidence review)

**Objective:** Verify the approved drift detailed exit code requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Read-only Terraform plan exit code 0 means no drift, 2 means differences, and 1 means failure.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
terraform -chdir=infra plan -detailed-exitcode -no-color
```

**Expected outcome:** Read-only Terraform plan exit code 0 means no drift, 2 means differences, and 1 means failure. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Pinned Terraform/provider versions and approved remote state; no apply or destroy

### `AZ-T68-12` — Drift detailed exit code (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-12 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T68-13` — Recovery time objective (configuration/evidence review)

**Objective:** Verify the approved recovery time objective requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Measured non-production recovery time is within the signed RTO.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".rto_minutes <= .approved_rto_minutes and .recovery_tested == true" evidence/phase6/dr-exercise.json
```

**Expected outcome:** Measured non-production recovery time is within the signed RTO. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T68-14` — Recovery time objective (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-14 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T68-15` — Recovery point objective (configuration/evidence review)

**Objective:** Verify the approved recovery point objective requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Measured recovery data loss is within the signed RPO.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".rpo_minutes <= .approved_rpo_minutes and .recovery_tested == true" evidence/phase6/dr-exercise.json
```

**Expected outcome:** Measured recovery data loss is within the signed RPO. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T68-16` — Recovery point objective (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-16 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T68-17` — Search index rebuild (configuration/evidence review)

**Objective:** Verify the approved search index rebuild requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Azure AI Search index can be rebuilt from protected authoritative source data.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".search_rebuild.source_data_available == true and .search_rebuild.reindexed == true" evidence/phase6/dr-exercise.json
```

**Expected outcome:** Azure AI Search index can be rebuilt from protected authoritative source data. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T68-18` — Search index rebuild (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-18 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T68-19` — Cosmos isolated restore (configuration/evidence review)

**Objective:** Verify the approved cosmos isolated restore requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Cosmos recovery to an isolated destination preserves required data integrity.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e ".cosmos_restore.restored_to_isolated_target == true and .cosmos_restore.data_validation == true" evidence/phase6/dr-exercise.json
```

**Expected outcome:** Cosmos recovery to an isolated destination preserves required data integrity. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T68-20` — Cosmos isolated restore (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-20 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T68-21` — Disaster recovery exercise record (configuration/evidence review)

**Objective:** Verify the approved disaster recovery exercise record requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 68, test AZ-T68-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Recovery timeline, independent reviewer, input set and outcome are traceable.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
test -s evidence/phase6/dr-exercise.json && sha256sum evidence/phase6/dr-exercise.json
```

**Expected outcome:** Recovery timeline, independent reviewer, input set and outcome are traceable. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T68-22` — Disaster recovery exercise record (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T68-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase6_guard.py --selftest AZ-T68-22 --spec specs/phase6_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

