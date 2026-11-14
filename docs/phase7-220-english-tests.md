# Phase 7: Operations, Security and Release Assurance — 220 English Tests

**Source:** 2026-11-10 frozen Phase 7 test specification; SHA-256 `27aac2b85153f1ff6c4dc253bcd27960f9454d562d1440e9d99d3a985f8dbb94`.
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

## Step 69 — Approved WAF Simulation

**Coverage:** `AZ-T69-01` through `AZ-T69-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T69-01` — Approved non-production WAF target (configuration/evidence review)

**Objective:** Verify the approved approved non-production waf target requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The targeted gateway is a recorded, approved non-production resource.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network application-gateway show -g "$RG" -n "$APPGW_NAME" --query "{id:id,frontendIPConfigurations:frontendIPConfigurations}" -o json
```

**Expected outcome:** The targeted gateway is a recorded, approved non-production resource. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T69-02` — Approved non-production WAF target (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-02 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T69-03` — Authorized WAF test change (configuration/evidence review)

**Objective:** Verify the approved authorized waf test change requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Test ticket authorizes the exact environment, requests and test window.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.ticket and .scope.approved == true and .scope.environment == "nonprod" and .scope.owner' docs/qa/waf-test-approval.json
```

**Expected outcome:** Test ticket authorizes the exact environment, requests and test window. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T69-04` — Authorized WAF test change (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-04 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T69-05` — Approved SQLi simulation (configuration/evidence review)

**Objective:** Verify the approved approved sqli simulation requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: A harmless authorized SQLi simulation is correlated with its WAF event and response.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
curl --silent --show-error --get "${WAF_TEST_URL:?}" --data-urlencode "q=${APPROVED_SQLI_VECTOR:?}" -H "X-Test-ID: ${TEST_ID:?}" -o evidence/phase7/waf_sqli_response.json -w "%{http_code}\n"
```

**Expected outcome:** A harmless authorized SQLi simulation is correlated with its WAF event and response. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T69-06` — Approved SQLi simulation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-06 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T69-07` — Approved XSS simulation (configuration/evidence review)

**Objective:** Verify the approved approved xss simulation requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: A harmless authorized XSS simulation is correlated with its WAF event and response.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
curl --silent --show-error --get "${WAF_TEST_URL:?}" --data-urlencode "q=${APPROVED_XSS_VECTOR:?}" -H "X-Test-ID: ${TEST_ID:?}" -o evidence/phase7/waf_xss_response.json -w "%{http_code}\n"
```

**Expected outcome:** A harmless authorized XSS simulation is correlated with its WAF event and response. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T69-08` — Approved XSS simulation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-08 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T69-09` — Benign control input (configuration/evidence review)

**Objective:** Verify the approved benign control input requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved private-network CI runner or VNet test VM, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Ordinary approved requests pass without false-positive WAF blocking.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
curl --silent --show-error --get "${WAF_TEST_URL:?}" --data-urlencode "q=${APPROVED_BENIGN_VECTOR:?}" -H "X-Test-ID: ${TEST_ID:?}" -o evidence/phase7/waf_benign_response.json -w "%{http_code}\n"
```

**Expected outcome:** Ordinary approved requests pass without false-positive WAF blocking. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required

### `AZ-T69-10` — Benign control input (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-10 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T69-11` — Query-field scope (configuration/evidence review)

**Objective:** Verify the approved query-field scope requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Query field test input and request count match the approved test matrix.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.query_vector_approved == true and .request_count <= .max_requests' docs/qa/waf-test-matrix.json
```

**Expected outcome:** Query field test input and request count match the approved test matrix. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T69-12` — Query-field scope (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-12 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T69-13` — Body-field scope (configuration/evidence review)

**Objective:** Verify the approved body-field scope requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Body test input and request count match the approved test matrix.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.body_vector_approved == true and .request_count <= .max_requests' docs/qa/waf-test-matrix.json
```

**Expected outcome:** Body test input and request count match the approved test matrix. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T69-14` — Body-field scope (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-14 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T69-15` — Header-field scope (configuration/evidence review)

**Objective:** Verify the approved header-field scope requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Header test input and request count match the approved test matrix.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.header_vector_approved == true and .request_count <= .max_requests' docs/qa/waf-test-matrix.json
```

**Expected outcome:** Header test input and request count match the approved test matrix. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T69-16` — Header-field scope (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-16 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T69-17` — Managed rule identity (configuration/evidence review)

**Objective:** Verify the approved managed rule identity requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: WAF rule IDs and managed rule-set version match the signed baseline.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query "{policySettings:policySettings,managedRules:managedRules}" -o json
```

**Expected outcome:** WAF rule IDs and managed rule-set version match the signed baseline. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T69-18` — Managed rule identity (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-18 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T69-19` — Unique test correlation ID (configuration/evidence review)

**Objective:** Verify the approved unique test correlation id requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Every request has a unique test identifier correlated with server-side evidence.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e --arg id "$TEST_ID" '.test_id == $id and .sample_hash and .utc and .approved_by' evidence/phase7/waf-test-observation.json
```

**Expected outcome:** Every request has a unique test identifier correlated with server-side evidence. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T69-20` — Unique test correlation ID (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-20 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T69-21` — Safe execution audit (configuration/evidence review)

**Objective:** Verify the approved safe execution audit requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 69, test AZ-T69-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: The test execution log contains no credentials, tokens or protected test payloads.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.completed == true and .contains_sensitive_payload == false and .test_id and .collector_job' evidence/phase7/waf-test-observation.json
```

**Expected outcome:** The test execution log contains no credentials, tokens or protected test payloads. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T69-22` — Safe execution audit (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T69-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T69-22 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 70 — WAF Blocking Evidence Review

**Coverage:** `AZ-T70-01` through `AZ-T70-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T70-01` — Blocked HTTP response (configuration/evidence review)

**Objective:** Verify the approved blocked http response requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Authorized simulated attack yields expected HTTP 403 and matching WAF Blocked action.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.response.status == 403 and .waf.action == "Blocked" and .waf.test_id == .test_id' evidence/phase7/waf-correlation.json
```

**Expected outcome:** Authorized simulated attack yields expected HTTP 403 and matching WAF Blocked action. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T70-02` — Blocked HTTP response (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-02 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T70-03` — WAF blocked event (configuration/evidence review)

**Objective:** Verify the approved waf blocked event requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Corresponding Rule ID and Blocked action are present in the firewall log.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.waf.action == "Blocked" and .waf.rule_id and .waf.policy_id' evidence/phase7/waf-correlation.json
```

**Expected outcome:** Corresponding Rule ID and Blocked action are present in the firewall log. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T70-04` — WAF blocked event (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-04 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T70-05` — Matched versus Blocked (configuration/evidence review)

**Objective:** Verify the approved matched versus blocked requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Matched detection-only events are not counted as Blocked traffic.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.matched_events >= 1 and .blocked_events >= 1 and .action_semantics_verified == true' evidence/phase7/waf-correlation.json
```

**Expected outcome:** Matched detection-only events are not counted as Blocked traffic. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T70-06` — Matched versus Blocked (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-06 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T70-07` — Anomaly-score policy (configuration/evidence review)

**Objective:** Verify the approved anomaly-score policy requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Aggregated anomaly score and enforcement follow approved managed rule policy.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.anomaly_score.checked == true and .anomaly_score.result == "meets_policy"' evidence/phase7/waf-correlation.json
```

**Expected outcome:** Aggregated anomaly score and enforcement follow approved managed rule policy. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T70-08` — Anomaly-score policy (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-08 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T70-09` — Rule-set version (configuration/evidence review)

**Objective:** Verify the approved rule-set version requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Effective WAF DRS version matches approved change records.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network application-gateway waf-policy show -g "$RG" -n "$WAF_POLICY_NAME" --query "managedRules.managedRuleSets[].{type:ruleSetType,version:ruleSetVersion}" -o json
```

**Expected outcome:** Effective WAF DRS version matches approved change records. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T70-10` — Rule-set version (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-10 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T70-11` — Narrow rule exclusions (configuration/evidence review)

**Objective:** Verify the approved narrow rule exclusions requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: WAF exceptions are scoped to necessary paths and input fields only.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.exclusions_reviewed == true and .excessive_exclusion_count == 0' evidence/phase7/waf-correlation.json
```

**Expected outcome:** WAF exceptions are scoped to necessary paths and input fields only. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T70-12` — Narrow rule exclusions (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-12 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T70-13` — Benign request success (configuration/evidence review)

**Objective:** Verify the approved benign request success requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Normal control input is not blocked and returns the expected approved status.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.benign.status == 200 and .benign.blocked == false' evidence/phase7/waf-correlation.json
```

**Expected outcome:** Normal control input is not blocked and returns the expected approved status. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T70-14` — Benign request success (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-14 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T70-15` — WAF transaction correlation (configuration/evidence review)

**Objective:** Verify the approved waf transaction correlation requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Gateway access and firewall entries share the expected correlation/transaction identifier.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.test_id and .request_id and .waf.transaction_id and .timestamp_utc' evidence/phase7/waf-correlation.json
```

**Expected outcome:** Gateway access and firewall entries share the expected correlation/transaction identifier. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T70-16` — WAF transaction correlation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-16 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T70-17` — No backend delivery for blocked request (configuration/evidence review)

**Objective:** Verify the approved no backend delivery for blocked request requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Blocked requests do not reach the backend, confirmed by backend-side logs.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.blocked.backend_access_count == 0 and .blocked.join_complete == true' evidence/phase7/waf-correlation.json
```

**Expected outcome:** Blocked requests do not reach the backend, confirmed by backend-side logs. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T70-18` — No backend delivery for blocked request (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-18 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T70-19` — Log collection retry bound (configuration/evidence review)

**Objective:** Verify the approved log collection retry bound requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Delayed event capture is retried within bounded approved timing limits.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.log_retry.completed == true and .log_retry.within_approved_window == true' evidence/phase7/waf-correlation.json
```

**Expected outcome:** Delayed event capture is retried within bounded approved timing limits. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T70-20` — Log collection retry bound (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-20 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T70-21` — Independent blocking verdict (configuration/evidence review)

**Objective:** Verify the approved independent blocking verdict requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 70, test AZ-T70-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Final WAF verdict includes independent review, timestamp and rule version.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.decision == "Pass" and .reviewed_by[0] and .reviewed_by[1] and .rule_set_revision' evidence/phase7/waf-correlation.json
```

**Expected outcome:** Final WAF verdict includes independent review, timestamp and rule version. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T70-22` — Independent blocking verdict (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T70-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T70-22 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 71 — Log Analytics Correlation

**Coverage:** `AZ-T71-01` through `AZ-T71-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T71-01` — Unique request test ID (configuration/evidence review)

**Objective:** Verify the approved unique request test id requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Each request ID is unique and visible in the expected telemetry.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.test_id and .test_id_unique == true' evidence/phase7/log-correlation.json
```

**Expected outcome:** Each request ID is unique and visible in the expected telemetry. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T71-02` — Unique request test ID (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-02 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T71-03` — Gateway access telemetry (configuration/evidence review)

**Objective:** Verify the approved gateway access telemetry requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: App Gateway access logs are delivered to the approved workspace.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az monitor diagnostic-settings list --resource "$APPGW_ID" -o json
```

**Expected outcome:** App Gateway access logs are delivered to the approved workspace. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T71-04` — Gateway access telemetry (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-04 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T71-05` — Firewall telemetry (configuration/evidence review)

**Objective:** Verify the approved firewall telemetry requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: WAF firewall logs are delivered and contain the expected action.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az monitor log-analytics query -w "$WORKSPACE_ID" --analytics-query "AGWFirewallLogs | where TimeGenerated > ago(1h) | summarize count() by Action" -o json
```

**Expected outcome:** WAF firewall logs are delivered and contain the expected action. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T71-06` — Firewall telemetry (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-06 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T71-07` — Application request telemetry (configuration/evidence review)

**Objective:** Verify the approved application request telemetry requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: App Service logs allow correlation of permitted requests.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az monitor log-analytics query -w "$WORKSPACE_ID" --analytics-query "AppServiceHTTPLogs | where TimeGenerated > ago(1h) | summarize count() by _ResourceId" -o json
```

**Expected outcome:** App Service logs allow correlation of permitted requests. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T71-08` — Application request telemetry (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-08 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T71-09` — Blocked event telemetry (configuration/evidence review)

**Objective:** Verify the approved blocked event telemetry requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Actual blocked action appears for the sanctioned test input.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.waf.blocked_count > 0 and .waf.action == "Blocked"' evidence/phase7/log-correlation.json
```

**Expected outcome:** Actual blocked action appears for the sanctioned test input. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T71-10` — Blocked event telemetry (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-10 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T71-11` — WAF rule metadata (configuration/evidence review)

**Objective:** Verify the approved waf rule metadata requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Correct rule ID and rule-set version are retained.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.waf.rule_id and .waf.rule_set_version' evidence/phase7/log-correlation.json
```

**Expected outcome:** Correct rule ID and rule-set version are retained. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T71-12` — WAF rule metadata (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-12 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T71-13` — Log latency objective (configuration/evidence review)

**Objective:** Verify the approved log latency objective requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Ingestion latency meets the approved monitoring SLO.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.ingestion_delay_seconds <= .approved_max_ingestion_delay_seconds' evidence/phase7/log-correlation.json
```

**Expected outcome:** Ingestion latency meets the approved monitoring SLO. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T71-14` — Log latency objective (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-14 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T71-15` — Saved KQL evidence (configuration/evidence review)

**Objective:** Verify the approved saved kql evidence requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Executed KQL, UTC timestamp, and workspace ID are retained.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.query_saved == true and .query_hash and .workspace_id' evidence/phase7/log-correlation.json
```

**Expected outcome:** Executed KQL, UTC timestamp, and workspace ID are retained. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T71-16` — Saved KQL evidence (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-16 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T71-17` — Cross-table correlation (configuration/evidence review)

**Objective:** Verify the approved cross-table correlation requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Request ID and transaction ID join the intended records without ambiguity.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.test_id and .waf.transaction_id and .gateway.request_id and .join_validated == true' evidence/phase7/log-correlation.json
```

**Expected outcome:** Request ID and transaction ID join the intended records without ambiguity. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T71-18` — Cross-table correlation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-18 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T71-19` — Blocked-request isolation (configuration/evidence review)

**Objective:** Verify the approved blocked-request isolation requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Backend lacks blocked requests while permitted requests appear, with bounded log delay accounted for.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.blocked.backend_access_count == 0 and .allowed.backend_access_count >= 1 and .backend_join_complete == true' evidence/phase7/log-correlation.json
```

**Expected outcome:** Backend lacks blocked requests while permitted requests appear, with bounded log delay accounted for. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T71-20` — Blocked-request isolation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-20 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T71-21` — Tamper-evident log retention (configuration/evidence review)

**Objective:** Verify the approved tamper-evident log retention requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 71, test AZ-T71-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Evidence has SHA-256 digest and retention controls.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.saved == true and .sha256 and .retention_policy_ref and .contains_secrets == false' evidence/phase7/log-correlation.json
```

**Expected outcome:** Evidence has SHA-256 digest and retention controls. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T71-22` — Tamper-evident log retention (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T71-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T71-22 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 72 — Network Lateral Movement Isolation

**Coverage:** `AZ-T72-01` through `AZ-T72-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T72-01` — Authorized subnet reachability (configuration/evidence review)

**Objective:** Verify the approved authorized subnet reachability requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Authorized subnet can establish permitted connection to private endpoint.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.authorized_subnet.private_endpoint_reachable == true' evidence/phase7/lateral-movement.json
```

**Expected outcome:** Authorized subnet can establish permitted connection to private endpoint. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T72-02` — Authorized subnet reachability (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-02 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T72-03` — Unauthorized subnet rejection (configuration/evidence review)

**Objective:** Verify the approved unauthorized subnet rejection requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Explicitly isolated unauthorized subnet is refused without changes to production policies.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.unauthorized_subnet.private_endpoint_reachable == false and .unauthorized_subnet.tested == true' evidence/phase7/lateral-movement.json
```

**Expected outcome:** Explicitly isolated unauthorized subnet is refused without changes to production policies. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T72-04` — Unauthorized subnet rejection (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-04 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T72-05` — Authorized App Service ingress (configuration/evidence review)

**Objective:** Verify the approved authorized app service ingress requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Authorized client successfully reaches the App Service private endpoint over HTTPS.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.app_pe.allow_source_matched == true and .app_pe.https_ok == true' evidence/phase7/lateral-movement.json
```

**Expected outcome:** Authorized client successfully reaches the App Service private endpoint over HTTPS. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T72-06` — Authorized App Service ingress (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-06 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T72-07` — Authorized OpenAI ingress (configuration/evidence review)

**Objective:** Verify the approved authorized openai ingress requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Application reaches approved OpenAI private endpoint over HTTPS.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.openai_pe.authorized_https_ok == true and .openai_pe.private_ip_checked == true' evidence/phase7/lateral-movement.json
```

**Expected outcome:** Application reaches approved OpenAI private endpoint over HTTPS. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T72-08` — Authorized OpenAI ingress (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-08 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T72-09` — Authorized Search ingress (configuration/evidence review)

**Objective:** Verify the approved authorized search ingress requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Application reaches approved Search private endpoint over HTTPS.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.search_pe.authorized_https_ok == true and .search_pe.private_ip_checked == true' evidence/phase7/lateral-movement.json
```

**Expected outcome:** Application reaches approved Search private endpoint over HTTPS. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T72-10` — Authorized Search ingress (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-10 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T72-11` — Authorized Cosmos ingress (configuration/evidence review)

**Objective:** Verify the approved authorized cosmos ingress requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Application reaches approved Cosmos DB private endpoint over HTTPS.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.cosmos_pe.authorized_https_ok == true and .cosmos_pe.private_ip_checked == true' evidence/phase7/lateral-movement.json
```

**Expected outcome:** Application reaches approved Cosmos DB private endpoint over HTTPS. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T72-12` — Authorized Cosmos ingress (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-12 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T72-13` — NSG enforcement (configuration/evidence review)

**Objective:** Verify the approved nsg enforcement requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: NSG priority and endpoint network policies enforce approved allowed and denied paths.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$PE_NSG_NAME" -o json
```

**Expected outcome:** NSG priority and endpoint network policies enforce approved allowed and denied paths. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T72-14` — NSG enforcement (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-14 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T72-15` — Route table enforcement (configuration/evidence review)

**Objective:** Verify the approved route table enforcement requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Effective route table uses the approved firewall or next hop.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network route-table route list -g "$RG" --route-table-name "$ROUTE_TABLE_NAME" -o json
```

**Expected outcome:** Effective route table uses the approved firewall or next hop. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T72-16` — Route table enforcement (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-16 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T72-17` — Authorized identity operation (configuration/evidence review)

**Objective:** Verify the approved authorized identity operation requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Approved managed identity succeeds with the required data-plane role.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.rbac.allowed_identity_succeeded == true and .rbac.role_scope_checked == true' evidence/phase7/lateral-movement.json
```

**Expected outcome:** Approved managed identity succeeds with the required data-plane role. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T72-18` — Authorized identity operation (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-18 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T72-19` — Unauthorized identity denial (configuration/evidence review)

**Objective:** Verify the approved unauthorized identity denial requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Isolated identity is denied data-plane operation without production role modifications.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.rbac.unauthorized_identity_denied == true and .rbac.no_production_role_revoked == true' evidence/phase7/lateral-movement.json
```

**Expected outcome:** Isolated identity is denied data-plane operation without production role modifications. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T72-20` — Unauthorized identity denial (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-20 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T72-21` — Network and identity combined record (configuration/evidence review)

**Objective:** Verify the approved network and identity combined record requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 72, test AZ-T72-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Networking and RBAC evidence both match the approved security boundary.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.network_control_checked == true and .identity_control_checked == true and .evidence_correlation == true' evidence/phase7/lateral-movement.json
```

**Expected outcome:** Networking and RBAC evidence both match the approved security boundary. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T72-22` — Network and identity combined record (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T72-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T72-22 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 73 — Non-Production Performance and Availability

**Coverage:** `AZ-T73-01` through `AZ-T73-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T73-01` — Approved load generator (configuration/evidence review)

**Objective:** Verify the approved approved load generator requirement against actual, attributable evidence.
**Execution class:** `CONTROLLED_NONPROD_TEST_REQUIRES_APPROVAL`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: k6 or approved Azure Load Testing runs only against a sanctioned non-production target.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.k6.execution_approved == true and .k6.target == "nonproduction" and .k6.script_sha256' evidence/phase7/performance.json
```

**Expected outcome:** k6 or approved Azure Load Testing runs only against a sanctioned non-production target. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Network or application test; approved non-production target, request budget and change ticket required; JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-02` — Approved load generator (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-02 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T73-03` — Functional versus load tooling (configuration/evidence review)

**Objective:** Verify the approved functional versus load tooling requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Playwright results are not represented as load or throughput validation.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.playwright_not_used_as_load_test == true and .k6_or_loadtesting_used == true' evidence/phase7/performance.json
```

**Expected outcome:** Playwright results are not represented as load or throughput validation. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-04` — Functional versus load tooling (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-04 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T73-05` — Measured request throughput (configuration/evidence review)

**Objective:** Verify the approved measured request throughput requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Measured RPS meets the approved minimum load requirement.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.throughput.observed_rps >= .throughput.approved_min_rps' evidence/phase7/performance.json
```

**Expected outcome:** Measured RPS meets the approved minimum load requirement. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-06` — Measured request throughput (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-06 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T73-07` — Measured p95 latency (configuration/evidence review)

**Objective:** Verify the approved measured p95 latency requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Observed p95 latency remains within signed maximum threshold.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.latency.p95_ms <= .latency.approved_max_p95_ms' evidence/phase7/performance.json
```

**Expected outcome:** Observed p95 latency remains within signed maximum threshold. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-08` — Measured p95 latency (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-08 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T73-09` — Measured error percentage (configuration/evidence review)

**Objective:** Verify the approved measured error percentage requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Errors remain within signed maximum acceptable rate.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.errors.observed_rate <= .errors.approved_max_rate' evidence/phase7/performance.json
```

**Expected outcome:** Errors remain within signed maximum acceptable rate. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-10` — Measured error percentage (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-10 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T73-11` — Autoscale behavior (configuration/evidence review)

**Objective:** Verify the approved autoscale behavior requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Observed autoscale triggers and capacity match approved thresholds.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.autoscale.trigger_tested == true and .autoscale.instance_count_sufficient == true' evidence/phase7/performance.json
```

**Expected outcome:** Observed autoscale triggers and capacity match approved thresholds. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-12` — Autoscale behavior (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-12 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T73-13` — Availability objective (configuration/evidence review)

**Objective:** Verify the approved availability objective requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Demonstrated availability satisfies the defined and measured SLO.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.ha.availability_slo_met == true and .ha.zone_design_reviewed == true' evidence/phase7/performance.json
```

**Expected outcome:** Demonstrated availability satisfies the defined and measured SLO. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-14` — Availability objective (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-14 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T73-15` — Retry safety (configuration/evidence review)

**Objective:** Verify the approved retry safety requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Retries honor idempotency and bounded backoff design.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.retry.safe == true and .retry.idempotency_checked == true' evidence/phase7/performance.json
```

**Expected outcome:** Retries honor idempotency and bounded backoff design. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-16` — Retry safety (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-16 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T73-17` — Isolated failover exercise (configuration/evidence review)

**Objective:** Verify the approved isolated failover exercise requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Approved isolated failover exercise recovers service within stated constraints.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.failover.isolated_test_done == true and .failover.recovered == true' evidence/phase7/performance.json
```

**Expected outcome:** Approved isolated failover exercise recovers service within stated constraints. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-18` — Isolated failover exercise (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-18 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T73-19` — SLO provenance (configuration/evidence review)

**Objective:** Verify the approved slo provenance requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: SLO thresholds, sampling period, methodology and sign-off are retained.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.slo.approved == true and .slo.metrics_evidenced == true' evidence/phase7/performance.json
```

**Expected outcome:** SLO thresholds, sampling period, methodology and sign-off are retained. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-20` — SLO provenance (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-20 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T73-21` — Signed load test report (configuration/evidence review)

**Objective:** Verify the approved signed load test report requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 73, test AZ-T73-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Raw measurements and signed summary are preserved without customer data.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.report.signed == true and .report.original_results_sha256 and .report.target_verified == true' evidence/phase7/performance.json
```

**Expected outcome:** Raw measurements and signed summary are preserved without customer data. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T73-22` — Signed load test report (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T73-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T73-22 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 74 — Infrastructure Policy Mutation Detection

**Coverage:** `AZ-T74-01` through `AZ-T74-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T74-01` — Public access mutation rejection (configuration/evidence review)

**Objective:** Verify the approved public access mutation rejection requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: A synthetic plan turning on unapproved PNA is rejected before apply.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_plan_policy.py --plan fixtures/plan_app_pna_true.json --expect Fail
```

**Expected outcome:** A synthetic plan turning on unapproved PNA is rejected before apply. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T74-02` — Public access mutation rejection (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-02 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T74-03` — Overly permissive NSG rejection (configuration/evidence review)

**Objective:** Verify the approved overly permissive nsg rejection requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: A synthetic plan opening broad inbound access is rejected before apply.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_plan_policy.py --plan fixtures/plan_nsg_any.json --expect Fail
```

**Expected outcome:** A synthetic plan opening broad inbound access is rejected before apply. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T74-04` — Overly permissive NSG rejection (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-04 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T74-05` — Excessive RBAC rejection (configuration/evidence review)

**Objective:** Verify the approved excessive rbac rejection requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Policy rejects simulated excessive identity role assignments.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.cases.rbac_overprivileged.deny == true' evidence/phase7/policy-mutations.json
```

**Expected outcome:** Policy rejects simulated excessive identity role assignments. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T74-06` — Excessive RBAC rejection (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-06 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T74-07` — Insecure HTTP listener rejection (configuration/evidence review)

**Objective:** Verify the approved insecure http listener rejection requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Policy rejects simulated unauthorized HTTP listeners.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.cases.http_listener.deny == true' evidence/phase7/policy-mutations.json
```

**Expected outcome:** Policy rejects simulated unauthorized HTTP listeners. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T74-08` — Insecure HTTP listener rejection (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-08 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T74-09` — Missing diagnostics rejection (configuration/evidence review)

**Objective:** Verify the approved missing diagnostics rejection requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Policy rejects synthetic plan with mandatory logging disabled.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.cases.missing_logs.deny == true' evidence/phase7/policy-mutations.json
```

**Expected outcome:** Policy rejects synthetic plan with mandatory logging disabled. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T74-10` — Missing diagnostics rejection (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-10 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T74-11` — Weak TLS rejection (configuration/evidence review)

**Objective:** Verify the approved weak tls rejection requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Policy rejects simulated weak TLS settings.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.cases.weak_tls.deny == true' evidence/phase7/policy-mutations.json
```

**Expected outcome:** Policy rejects simulated weak TLS settings. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T74-12` — Weak TLS rejection (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-12 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T74-13` — Policy self-test correctness (configuration/evidence review)

**Objective:** Verify the approved policy self-test correctness requirement against actual, attributable evidence.
**Execution class:** `OFFLINE_POLICY_SELFTEST`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Each policy rule has passing safe and failing unsafe synthetic fixtures.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_plan_policy.py --selftest
```

**Expected outcome:** Each policy rule has passing safe and failing unsafe synthetic fixtures. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Review command compatibility and evidence provenance for the actual environment

### `AZ-T74-14` — Policy self-test correctness (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-14 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T74-15` — Plan-only boundary (configuration/evidence review)

**Objective:** Verify the approved plan-only boundary requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Mutation tests inspect plans or fixtures and never invoke apply.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.plan_only == true and .apply_executed == false' evidence/phase7/policy-mutations.json
```

**Expected outcome:** Mutation tests inspect plans or fixtures and never invoke apply. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T74-16` — Plan-only boundary (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-16 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T74-17` — No production changes (configuration/evidence review)

**Objective:** Verify the approved no production changes requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Evidence confirms the rehearsal made no production changes.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.apply_executed == false and .production_resource_changed == false' evidence/phase7/policy-mutations.json
```

**Expected outcome:** Evidence confirms the rehearsal made no production changes. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T74-18` — No production changes (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-18 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T74-19` — Isolated mutation workspace (configuration/evidence review)

**Objective:** Verify the approved isolated mutation workspace requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Policy mutation runs in a temporary isolated environment only.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.workspace == "isolated" and .resource_isolated == true' evidence/phase7/policy-mutations.json
```

**Expected outcome:** Policy mutation runs in a temporary isolated environment only. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T74-20` — Isolated mutation workspace (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-20 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T74-21` — Fail-closed CI enforcement (configuration/evidence review)

**Objective:** Verify the approved fail-closed ci enforcement requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 74, test AZ-T74-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Failed policy verdict prevents any downstream apply gate.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.failure_stops_pipeline == true and .mutation_detected == true' evidence/phase7/policy-mutations.json
```

**Expected outcome:** Failed policy verdict prevents any downstream apply gate. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T74-22` — Fail-closed CI enforcement (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T74-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T74-22 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 75 — Continuous Exposure and Drift Audit

**Coverage:** `AZ-T75-01` through `AZ-T75-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T75-01` — Daily public IP inventory (configuration/evidence review)

**Objective:** Verify the approved daily public ip inventory requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Daily audit finds no public IPs outside signed exception scope.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az network public-ip list --query "[].{id:id,ip:ipAddress}" -o json
```

**Expected outcome:** Daily audit finds no public IPs outside signed exception scope. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T75-02` — Daily public IP inventory (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-02 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T75-03` — Daily PaaS public access audit (configuration/evidence review)

**Objective:** Verify the approved daily paas public access audit requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Daily inventory confirms no unapproved PaaS public access.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az graph query -q "Resources | where isnotempty(properties.publicNetworkAccess) | project id, type, pna=tostring(properties.publicNetworkAccess)" -o json
```

**Expected outcome:** Daily inventory confirms no unapproved PaaS public access. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T75-04` — Daily PaaS public access audit (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-04 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T75-05` — Daily API key audit (configuration/evidence review)

**Objective:** Verify the approved daily api key audit requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Required OpenAI accounts have local API-key authentication disabled.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az cognitiveservices account show -g "$RG" -n "$OPENAI_NAME" --query "properties.disableLocalAuth" -o tsv
```

**Expected outcome:** Required OpenAI accounts have local API-key authentication disabled. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T75-06` — Daily API key audit (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-06 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T75-07` — Weekly diagnostics inventory (configuration/evidence review)

**Objective:** Verify the approved weekly diagnostics inventory requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Diagnostic settings match approved destinations and mandatory categories.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az monitor diagnostic-settings list --resource "$APPGW_ID" -o json
```

**Expected outcome:** Diagnostic settings match approved destinations and mandatory categories. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T75-08` — Weekly diagnostics inventory (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-08 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T75-09` — Weekly state drift review (configuration/evidence review)

**Objective:** Verify the approved weekly state drift review requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Read-only plan indicates no unauthorized Terraform drift.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
terraform -chdir=infra plan -detailed-exitcode -no-color -input=false
```

**Expected outcome:** Read-only plan indicates no unauthorized Terraform drift. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Pinned Terraform/provider versions and approved remote state; no apply or destroy

### `AZ-T75-10` — Weekly state drift review (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-10 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T75-11` — Weekly critical vulnerability review (configuration/evidence review)

**Objective:** Verify the approved weekly critical vulnerability review requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Open critical findings meet the signed security threshold.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.scan_completed == true and .unaccepted_critical_count == 0' evidence/phase7/vulnerability-audit.json
```

**Expected outcome:** Open critical findings meet the signed security threshold. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T75-12` — Weekly critical vulnerability review (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-12 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T75-13` — Weekly RBAC inventory (configuration/evidence review)

**Objective:** Verify the approved weekly rbac inventory requirement against actual, attributable evidence.
**Execution class:** `AZURE_READONLY_CONFIG_REQUIRES_IDENTITY`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Approved CI runner using federated identity with read-only scoped access, execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Effective assignments reconcile with approved principal and role inventory.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
az role assignment list --scope "$APP_SCOPE_ID" --all -o json
```

**Expected outcome:** Effective assignments reconcile with approved principal and role inventory. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Authenticate only on approved CI using workload identity; never run az login on fixed WSL

### `AZ-T75-14` — Weekly RBAC inventory (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-14 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T75-15` — Certificate renewal horizon (configuration/evidence review)

**Objective:** Verify the approved certificate renewal horizon requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Certificate expiry is beyond the configured rotation notice threshold.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.certificates | all(.days_to_expire > .approved_min_days_to_expire)' evidence/phase7/certificates.json
```

**Expected outcome:** Certificate expiry is beyond the configured rotation notice threshold. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T75-16` — Certificate renewal horizon (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-16 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T75-17` — Approved exception expiration (configuration/evidence review)

**Objective:** Verify the approved approved exception expiration requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Every security exception has current ticket, expiry and approval.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.exceptions | all(.approved == true and .expires_at and .ticket and .owner)' docs/security/approved-exceptions.json
```

**Expected outcome:** Every security exception has current ticket, expiry and approval. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T75-18` — Approved exception expiration (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-18 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T75-19` — Remediation issue trace (configuration/evidence review)

**Objective:** Verify the approved remediation issue trace requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Detected findings have owned remediation tickets and deadlines.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.tickets | all(.owner and .severity and .due_date and .triage_status)' evidence/phase7/remediation.json
```

**Expected outcome:** Detected findings have owned remediation tickets and deadlines. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T75-20` — Remediation issue trace (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-20 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T75-21` — Signed monitoring digest (configuration/evidence review)

**Objective:** Verify the approved signed monitoring digest requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 75, test AZ-T75-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Weekly report includes scoped asset list, UTC window and reviewer signature.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.signed == true and .assets_scanned > 0 and .collector_job and .week_start' evidence/phase7/weekly-audit.json
```

**Expected outcome:** Weekly report includes scoped asset list, UTC window and reviewer signature. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T75-22` — Signed monitoring digest (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T75-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T75-22 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 76 — CI/CD Enforcement Gates

**Coverage:** `AZ-T76-01` through `AZ-T76-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T76-01` — Terraform formatting gate (configuration/evidence review)

**Objective:** Verify the approved terraform formatting gate requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Formatting gate runs and must pass on the source branch.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.gates.fmt == "Pass"' evidence/phase7/pipeline.json
```

**Expected outcome:** Formatting gate runs and must pass on the source branch. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-02` — Terraform formatting gate (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-02 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T76-03` — Terraform validation gate (configuration/evidence review)

**Objective:** Verify the approved terraform validation gate requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Terraform validate succeeds against pinned provider schema.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.gates.validate == "Pass"' evidence/phase7/pipeline.json
```

**Expected outcome:** Terraform validate succeeds against pinned provider schema. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-04` — Terraform validation gate (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-04 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T76-05` — Terraform test gate (configuration/evidence review)

**Objective:** Verify the approved terraform test gate requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Terraform unit tests pass in isolated plan-only mode.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.gates.test == "Pass"' evidence/phase7/pipeline.json
```

**Expected outcome:** Terraform unit tests pass in isolated plan-only mode. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-06` — Terraform test gate (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-06 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T76-07` — Dependency and security scan gate (configuration/evidence review)

**Objective:** Verify the approved dependency and security scan gate requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Approved scanner passes with accepted and documented exceptions.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.gates.security_scan == "Pass"' evidence/phase7/pipeline.json
```

**Expected outcome:** Approved scanner passes with accepted and documented exceptions. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-08` — Dependency and security scan gate (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-08 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T76-09` — Infrastructure policy gate (configuration/evidence review)

**Objective:** Verify the approved infrastructure policy gate requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Policy-as-code gate passes for the exact reviewed saved plan.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.gates.policy == "Pass"' evidence/phase7/pipeline.json
```

**Expected outcome:** Policy-as-code gate passes for the exact reviewed saved plan. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-10` — Infrastructure policy gate (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-10 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T76-11` — Plan identity lock (configuration/evidence review)

**Objective:** Verify the approved plan identity lock requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Saved plan digest and source commit SHA match the approved artifact.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.gates.plan == "Pass" and .plan.hash and .plan.commit_sha' evidence/phase7/pipeline.json
```

**Expected outcome:** Saved plan digest and source commit SHA match the approved artifact. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-12` — Plan identity lock (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-12 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T76-13` — Two independent approvals (configuration/evidence review)

**Objective:** Verify the approved two independent approvals requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Two distinct reviewers approve the exact immutable plan artifact.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.approvals.two_distinct_reviewers == true and .approvals.approved_plan_hash == .plan.hash' evidence/phase7/pipeline.json
```

**Expected outcome:** Two distinct reviewers approve the exact immutable plan artifact. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-14` — Two independent approvals (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-14 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T76-15` — Post-approval apply gate (configuration/evidence review)

**Objective:** Verify the approved post-approval apply gate requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Apply is permissible only after all gates and approvals; this document performs no apply.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.apply.performed_only_after_approval == true and .apply.plan_hash == .plan.hash' evidence/phase7/pipeline.json
```

**Expected outcome:** Apply is permissible only after all gates and approvals; this document performs no apply. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-16` — Post-approval apply gate (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-16 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T76-17` — External exposure gate (configuration/evidence review)

**Objective:** Verify the approved external exposure gate requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: External validation and configuration evidence jointly confirm closed public ingress.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.gates.external == "Pass" and .gates.external_baseline_verified == true' evidence/phase7/pipeline.json
```

**Expected outcome:** External validation and configuration evidence jointly confirm closed public ingress. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-18` — External exposure gate (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-18 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T76-19` — Internal connectivity gate (configuration/evidence review)

**Objective:** Verify the approved internal connectivity gate requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Approved VNet runner validates internal DNS and application dependencies.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.gates.internal == "Pass" and .gates.internal_runner_private == true' evidence/phase7/pipeline.json
```

**Expected outcome:** Approved VNet runner validates internal DNS and application dependencies. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-20` — Internal connectivity gate (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-20 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T76-21` — Log and evidence gate (configuration/evidence review)

**Objective:** Verify the approved log and evidence gate requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 76, test AZ-T76-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Required logs reconcile and a failed gate blocks downstream promotion.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.gates.log == "Pass" and .gates.fail_closed == true and .gates.logs_redacted == true' evidence/phase7/pipeline.json
```

**Expected outcome:** Required logs reconcile and a failed gate blocks downstream promotion. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T76-22` — Log and evidence gate (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T76-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T76-22 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 77 — Release Artifact Freeze and Handover

**Coverage:** `AZ-T77-01` through `AZ-T77-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T77-01` — Approved architecture diagrams (configuration/evidence review)

**Objective:** Verify the approved approved architecture diagrams requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Handover topology and network zone diagrams are reviewed and signed.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.architecture.diagram_sha256 and .architecture.reviewed == true' evidence/phase7/release-package.json
```

**Expected outcome:** Handover topology and network zone diagrams are reviewed and signed. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-02` — Approved architecture diagrams (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-02 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T77-03` — Operations and rollback playbooks (configuration/evidence review)

**Objective:** Verify the approved operations and rollback playbooks requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Documented operation, incident and rollback procedures are ready.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.runbooks.operations_sha256 and .runbooks.rollback_sha256 and .runbooks.reviewed == true' evidence/phase7/release-package.json
```

**Expected outcome:** Documented operation, incident and rollback procedures are ready. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-04` — Operations and rollback playbooks (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-04 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T77-05` — Signed software bill of materials (configuration/evidence review)

**Objective:** Verify the approved signed software bill of materials requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Version-bound SBOM and signature cover the exact delivered components.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.sbom.signed == true and .sbom.sha256 and .sbom.scope_checked == true' evidence/phase7/release-package.json
```

**Expected outcome:** Version-bound SBOM and signature cover the exact delivered components. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-06` — Signed software bill of materials (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-06 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T77-07` — Versioned change history (configuration/evidence review)

**Objective:** Verify the approved versioned change history requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Git commit, Terraform plan digest, and approvals map to the same release.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.changes.commit_sha and .changes.approved_plan_hash and .changes.audit_trail' evidence/phase7/release-package.json
```

**Expected outcome:** Git commit, Terraform plan digest, and approvals map to the same release. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-08` — Versioned change history (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-08 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T77-09` — Key management inventory (configuration/evidence review)

**Objective:** Verify the approved key management inventory requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Key inventory and rotation policy are complete without exposed secret values.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.key_inventory.owner and .key_inventory.rotation_policy and .key_inventory.secrets_disclosed == false' evidence/phase7/release-package.json
```

**Expected outcome:** Key inventory and rotation policy are complete without exposed secret values. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-10` — Key management inventory (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-10 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T77-11` — Independent recovery exercise (configuration/evidence review)

**Objective:** Verify the approved independent recovery exercise requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Signed isolated recovery exercise evidence is available.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.recovery.exercise_recorded == true and .recovery.evidence_sha256' evidence/phase7/release-package.json
```

**Expected outcome:** Signed isolated recovery exercise evidence is available. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-12` — Independent recovery exercise (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-12 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T77-13` — Measured RTO and RPO compliance (configuration/evidence review)

**Objective:** Verify the approved measured rto and rpo compliance requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Measured recovery outcomes meet signed objectives.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.recovery.rto_met == true and .recovery.rpo_met == true' evidence/phase7/release-package.json
```

**Expected outcome:** Measured recovery outcomes meet signed objectives. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-14` — Measured RTO and RPO compliance (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-14 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T77-15` — All 1716 test evidence traceability (configuration/evidence review)

**Objective:** Verify the approved all 1716 test evidence traceability requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: All test IDs have evidence references and acceptance status without conflating synthetic with live results.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.tests.test_count == 1716 and .tests.executed_count <= 1716 and .tests.evidence_index_sha256' evidence/phase7/release-package.json
```

**Expected outcome:** All test IDs have evidence references and acceptance status without conflating synthetic with live results. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-16` — All 1716 test evidence traceability (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-16 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T77-17` — Signed release tag (configuration/evidence review)

**Objective:** Verify the approved signed release tag requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Release tag signature is independently verifiable.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.tag.signed == true and .tag.commit_sha and .tag.attestation_verified == true' evidence/phase7/release-package.json
```

**Expected outcome:** Release tag signature is independently verifiable. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-18` — Signed release tag (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-18 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T77-19` — Handover acknowledgment (configuration/evidence review)

**Objective:** Verify the approved handover acknowledgment requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Receiving operations owner signs the handover acceptance.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.handover.signed == true and .handover.receiver and .handover.date_utc' evidence/phase7/release-package.json
```

**Expected outcome:** Receiving operations owner signs the handover acceptance. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-20` — Handover acknowledgment (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-20 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T77-21` — Sensitive-data exclusion (configuration/evidence review)

**Objective:** Verify the approved sensitive-data exclusion requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 77, test AZ-T77-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Release artifacts contain no customer secrets, state files, or unapproved data.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.redaction.completed == true and .redaction.secret_findings == 0' evidence/phase7/release-package.json
```

**Expected outcome:** Release artifacts contain no customer secrets, state files, or unapproved data. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T77-22` — Sensitive-data exclusion (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T77-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T77-22 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

## Step 78 — Formal Go/No-Go Decision

**Coverage:** `AZ-T78-01` through `AZ-T78-22` (11 controls and 11 paired synthetic deviations).

### `AZ-T78-01` — Zero unauthorized public ingress (configuration/evidence review)

**Objective:** Verify the approved zero unauthorized public ingress requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-01, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: All public application entry paths are absent or explicitly approved and risk accepted.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.exposure.unapproved_public_paths == 0 and .exposure.asset_scope_complete == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** All public application entry paths are absent or explicitly approved and risk accepted. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-02` — Zero unauthorized public ingress (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-01 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-02 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T78-03` — PaaS public network access disabled (configuration/evidence review)

**Objective:** Verify the approved paas public network access disabled requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-03, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: All in-scope PaaS services have expected Disabled public network access.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.private_access.pna_disabled_all == true and .private_access.assets_found == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** All in-scope PaaS services have expected Disabled public network access. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-04` — PaaS public network access disabled (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-03 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-04 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T78-05` — Correct private DNS resolution (configuration/evidence review)

**Objective:** Verify the approved correct private dns resolution requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-05, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Private DNS resolves normal service hostnames to approved endpoint NIC addresses.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.dns.all_private_resolved == true and .dns.pe_nic_verified == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** Private DNS resolves normal service hostnames to approved endpoint NIC addresses. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-06` — Correct private DNS resolution (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-05 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-06 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T78-07` — Identity-based authentication (configuration/evidence review)

**Objective:** Verify the approved identity-based authentication requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-07, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Managed identity is used without embedded client secrets where required.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.identity.mi_auth_passed == true and .identity.production_secrets_absent == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** Managed identity is used without embedded client secrets where required. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-08` — Identity-based authentication (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-07 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-08 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T78-09` — Least-privilege authorization (configuration/evidence review)

**Objective:** Verify the approved least-privilege authorization requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-09, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Role assignments are minimal and negative-case denials have approved evidence.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.identity.rbac_minimum == true and .identity.denial_test_documented == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** Role assignments are minimal and negative-case denials have approved evidence. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-10` — Least-privilege authorization (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-09 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-10 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T78-11` — WAF prevention effectiveness (configuration/evidence review)

**Objective:** Verify the approved waf prevention effectiveness requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-11, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: WAF Prevention mode and blocked-log correlation are demonstrated.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.waf.mode == "Prevention" and .waf.block_correlation_verified == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** WAF Prevention mode and blocked-log correlation are demonstrated. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-12` — WAF prevention effectiveness (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-11 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-12 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T78-13` — Diagnostic log arrival (configuration/evidence review)

**Objective:** Verify the approved diagnostic log arrival requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-13, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Required diagnostics arrive at approved destinations within retention objectives.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.logging.ingestion_confirmed == true and .logging.retention_approved == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** Required diagnostics arrive at approved destinations within retention objectives. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-14` — Diagnostic log arrival (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-13 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-14 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T78-15` — Disaster recovery acceptance (configuration/evidence review)

**Objective:** Verify the approved disaster recovery acceptance requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-15, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Recovery tests meet signed RTO and RPO requirements.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.recovery.exercise_confirmed == true and .recovery.rto_rpo_met == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** Recovery tests meet signed RTO and RPO requirements. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-16` — Disaster recovery acceptance (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-15 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-16 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T78-17` — Remote state and zero unauthorized drift (configuration/evidence review)

**Objective:** Verify the approved remote state and zero unauthorized drift requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-17, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: State locking operates and approved detailed-exitcode plan reports zero unintended drift.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.terraform.drift_count == 0 and .terraform.state_lock_verified == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** State locking operates and approved detailed-exitcode plan reports zero unintended drift. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** Pinned Terraform/provider versions and approved remote state; no apply or destroy; JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-18` — Remote state and zero unauthorized drift (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-17 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-18 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T78-19` — No unresolved critical risks (configuration/evidence review)

**Objective:** Verify the approved no unresolved critical risks requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-19, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: No unresolved Critical findings remain without formally accepted blocking resolution.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.risk.unresolved_critical_count == 0 and .risk.exceptions_all_approved == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** No unresolved Critical findings remain without formally accepted blocking resolution. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-20` — No unresolved critical risks (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-19 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-20 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

### `AZ-T78-21` — Final signed release decision (configuration/evidence review)

**Objective:** Verify the approved final signed release decision requirement against actual, attributable evidence.
**Execution class:** `LOCAL_STATIC_OR_EVIDENCE_REVIEW`. **Required setup:** Actual inventory and asset IDs; signed baseline; environment and actor approval; requisite least-privilege access; supported CLI/provider; required logs and independently reviewable evidence.

**Procedure:**
- 1. Pin Step 78, test AZ-T78-21, signed baseline version, exact resource scope, and responsible reviewer.
- 2. Check that the target exists and collector role, network vantage point and change/QA approval are valid.
- 3. In Offline isolated WSL / unit test runner (no Azure authorization), execute the displayed command only when fully authorized; save raw output and exit status.
- 4. Evaluate: Complete proof package has two independent approvals before any GO decision.
- 5. Cross-check resource properties, target IDs, UTC, configuration, logs and evidence against independent approved baseline.
- 6. Mark FAIL only for an evidenced violation; missing source/resource/permission/signature/baseline/log is NOT_READY; two reviewers control final acceptance.

**Command (documented; not executed against Azure):**
```bash
jq -e '.decision == "Go" and .approvers.two_distinct == true and .approvers.signatures_verified == true and .evidence_complete == true' evidence/phase7/go-nogo.json
```

**Expected outcome:** Complete proof package has two independent approvals before any GO decision. Live outcome cannot be PASS without a complete, independently approved observation.

**Evidence:** Test ID; resource IDs; subscription/scope; approved baseline and ticket; CI/runner identity; UTC; exit code; raw output SHA-256; correlated logs when applicable; two independent reviewers; classification and sign-off.

**Troubleshooting:** If NOT_READY: restore missing approval, real resource, baseline, logs, execution permission, or implementation source. If FAIL: preserve raw evidence and open a remediation ticket. Never repair production while executing a read-only audit.

**Safety review:** JSON input must be trusted, complete, scoped, timestamped and signed; checking field presence alone is insufficient

### `AZ-T78-22` — Final signed release decision (synthetic deviation)

**Objective:** Prove the synthetic detector flags an unsafe fixture and missing observation; never count this as Azure acceptance.
**Execution class:** `SYNTHETIC_DETECTOR_SELFTEST`. **Required setup:** Frozen spec and synthetic fixtures available offline; no Azure environment or credentials.

**Procedure:**
- 1. Locate paired control AZ-T78-21 in English specification.
- 2. Review good and bad synthetic fixtures without changing any real Azure resource.
- 3. Run the specified offline detector self-test; confirm bad fixture is FAIL and missing evidence is NOT_READY.
- 4. Save output, fixture provenance and checker SHA-256 as synthetic QC evidence only.

**Command (documented; not executed against Azure):**
```bash
python3 scripts/phase7_guard.py --selftest AZ-T78-22 --spec specs/phase7_220_en.json
```

**Expected outcome:** Synthetic deviation => FAIL; missing observation => NOT_READY; detector test success does not certify any live system.

**Evidence:** Test ID; fixture digests; offline guard version; synthetic result; never label as live evidence.

**Troubleshooting:** If the bad fixture is not FAIL or missing is not NOT_READY, stop publishing positive assurances and inspect the rule/fixture mapping.

**Safety review:** offline synthetic only; no cloud operations

