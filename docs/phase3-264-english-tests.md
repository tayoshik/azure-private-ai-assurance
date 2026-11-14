# Phase 3 — English Detailed Tests: Azure Networking, Private DNS, Monitoring
> **Design-stage documentation only.** Steps 21–32; 264 stable test IDs (132 positive read-only or controlled observations, 132 offline synthetic deviation tests). Azure live PASS: **0**. All live acceptance: `NOT_READY`.

Source: verified Phase 3 Japanese 264-case runbook and original 78-step construction baseline, published here as an English publication edition. Original per-case ID and command intent are preserved. The more extensive machine-readable offline bundle is retained separately for regression testing.

## Execution and evidence rules

- Never use interactive `az login` from the restricted WSL workstation. Azure queries run only on explicitly approved scoped CI runners.
- Commands using `dig` or `curl` require the authorized internal test runner and actual private routing. Never disable TLS verification.
- Some legacy `terraform plan -refresh-only` commands can lock state or modify local state/cache. Require explicit change approval and isolated CI.
- An exit code 0, JSON list, HTTP 403 or DNS response alone **never** proves network isolation, least privilege or Azure acceptance.
- For each case attach approved baseline revision, exact asset ID/scope, collected UTC timestamp, sanitized output SHA-256 and independent reviewer decision. Missing prerequisite means `NOT_READY`.
- Even-numbered cases use synthetic offline fixture detectors, not network attacks or proof of Azure blocking.

## Offline working instructions

```bash
# Run only after extracting the matching Turn 04 source bundle with its scripts/specs:
python3 scripts/verify_phase3_english.py
python3 scripts/phase3_guard.py --selftest ALL --spec specs/phase3_264.json
python3 -m unittest discover -s tests -v
```

## Step 21 — Network address plan and IPAM

**Common approved acceptance rule:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity.

## Step 22 — Azure Policy security baseline

**Common approved acceptance rule:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence.

## Step 23 — Resource groups and virtual networks

**Common approved acceptance rule:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence.

## Step 24 — Private Application Gateway subnet

**Common approved acceptance rule:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning.

## Step 25 — App Service outbound integration subnet

**Common approved acceptance rule:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution.

## Step 26 — Private Endpoint subnet isolation

**Common approved acceptance rule:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence.

## Step 27 — Azure DNS Private Resolver

**Common approved acceptance rule:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification.

## Step 28 — Application Gateway NSG and health

**Common approved acceptance rule:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health.

## Step 29 — Outbound routing and service dependencies

**Common approved acceptance rule:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry.

## Step 30 — Private DNS zones and records

**Common approved acceptance rule:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP.

## Step 31 — Azure Monitor private connectivity

**Common approved acceptance rule:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient.

## Step 32 — Centralized logging and alerting

**Common approved acceptance rule:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery.

### AZ-T21-01 — VNet CIDR (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed vnet cidr against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet show -g "$RG" -n "$VNET" --query "addressSpace.addressPrefixes" -o json
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: VNet CIDR.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-02 — VNet CIDR (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic vnet cidr deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-03 — On-premises CIDRs (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed on-premises cidrs against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".networks.onprem.cidrs | length > 0" "$IPAM_JSON"
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: On-premises CIDRs.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-04 — On-premises CIDRs (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic on-premises cidrs deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-05 — Hub CIDRs (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed hub cidrs against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".networks.hub.cidrs | length > 0" "$IPAM_JSON"
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: Hub CIDRs.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-06 — Hub CIDRs (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic hub cidrs deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-07 — VPN P2S/S2S CIDRs (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed vpn p2s/s2s cidrs against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".networks.vpn.cidrs | length > 0" "$IPAM_JSON"
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: VPN P2S/S2S CIDRs.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-08 — VPN P2S/S2S CIDRs (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic vpn p2s/s2s cidrs deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-09 — Disaster-recovery CIDRs (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed disaster-recovery cidrs against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".networks.dr.cidrs | length > 0" "$IPAM_JSON"
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: Disaster-recovery CIDRs.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-10 — Disaster-recovery CIDRs (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic disaster-recovery cidrs deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-11 — Subnet capacity plan (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed subnet capacity plan against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".subnets | length > 0" "$IPAM_JSON"
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: Subnet capacity plan.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-12 — Subnet capacity plan (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic subnet capacity plan deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-13 — Reserved IP ranges (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed reserved ip ranges against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e '.reserved | type == "array"' "$IPAM_JSON"
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: Reserved IP ranges.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-14 — Reserved IP ranges (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic reserved ip ranges deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-15 — CIDR overlap detector (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed cidr overlap detector against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --cidr-check "$IPAM_JSON"
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: CIDR overlap detector.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-16 — CIDR overlap detector (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic cidr overlap detector deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-17 — Expansion headroom (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed expansion headroom against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".capacity.approved == true" "$IPAM_JSON"
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: Expansion headroom.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-18 — Expansion headroom (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic expansion headroom deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-19 — IPAM approval (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed ipam approval against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".approvals.ipam.approver and .approvals.ipam.date" "$IPAM_JSON"
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: IPAM approval.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-20 — IPAM approval (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic ipam approval deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-21 — CIDR change history (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed cidr change history against the approved design and Step 21 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
git log -1 --format="%H %aI" -- docs/network-ipam.json
```

**Expected:** Compare signed IPAM CIDRs, subnet sizing, reservations and overlaps; ensure actual address plan matches approved connectivity and capacity. Specific focus: CIDR change history.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T21-22 — CIDR change history (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T21-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic cidr change history deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-01 — Public-IP deny policy (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed public-ip deny policy against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az policy assignment list --scope "$POLICY_SCOPE" -o json
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Public-IP deny policy.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-02 — Public-IP deny policy (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic public-ip deny policy deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-03 — Public-network-access deny policy (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed public-network-access deny policy against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az policy assignment list --scope "$POLICY_SCOPE" -o json
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Public-network-access deny policy.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-04 — Public-network-access deny policy (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic public-network-access deny policy deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-05 — Minimum TLS version policy (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed minimum tls version policy against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az policy assignment list --scope "$POLICY_SCOPE" -o json
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Minimum TLS version policy.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-06 — Minimum TLS version policy (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic minimum tls version policy deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-07 — Basic authentication deny policy (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed basic authentication deny policy against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az policy assignment list --scope "$POLICY_SCOPE" -o json
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Basic authentication deny policy.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-08 — Basic authentication deny policy (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic basic authentication deny policy deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-09 — Required resource tags (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed required resource tags against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az policy assignment list --scope "$POLICY_SCOPE" -o json
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Required resource tags.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-10 — Required resource tags (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic required resource tags deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-11 — Mandatory diagnostics policy (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed mandatory diagnostics policy against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az policy assignment list --scope "$POLICY_SCOPE" -o json
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Mandatory diagnostics policy.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-12 — Mandatory diagnostics policy (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic mandatory diagnostics policy deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-13 — Approved exemptions (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed approved exemptions against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az policy exemption list --scope "$POLICY_SCOPE" -o json
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Approved exemptions.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-14 — Approved exemptions (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic approved exemptions deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-15 — Assignment scope (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed assignment scope against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az policy assignment list --scope "$POLICY_SCOPE" --query "[].{id:id,scope:scope}" -o json
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Assignment scope.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-16 — Assignment scope (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic assignment scope deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-17 — Exemption expiry (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed exemption expiry against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az policy exemption list --scope "$POLICY_SCOPE" --query "[].{name:name,expiresOn:expiresOn}" -o json
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Exemption expiry.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-18 — Exemption expiry (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic exemption expiry deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-19 — Audit-to-Deny transition (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed audit-to-deny transition against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".policy_transition.approved == true" "$POLICY_BASELINE"
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Audit-to-Deny transition.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-20 — Audit-to-Deny transition (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic audit-to-deny transition deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-21 — Policy compliance evidence (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed policy compliance evidence against the approved design and Step 22 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az policy state summarize --subscription "$SUBSCRIPTION_ID" -o json
```

**Expected:** Confirm policy assignments, effective deny effects, scope and notScopes, time-limited exemptions, and evaluated asset coverage, not merely policy existence. Specific focus: Policy compliance evidence.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T22-22 — Policy compliance evidence (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T22-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic policy compliance evidence deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-01 — Resource group naming (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed resource group naming against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az group show -n "$RG" --query "{id:id,name:name}" -o json
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: Resource group naming.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-02 — Resource group naming (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic resource group naming deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-03 — VNet address space (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed vnet address space against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet show -g "$RG" -n "$VNET" --query "{cidrs:addressSpace.addressPrefixes}" -o json
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: VNet address space.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-04 — VNet address space (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic vnet address space deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-05 — Required resource tags (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed required resource tags against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet show -g "$RG" -n "$VNET" --query tags -o json
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: Required resource tags.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-06 — Required resource tags (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic required resource tags deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-07 — Resource group delete lock (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed resource group delete lock against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az lock list -g "$RG" -o json
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: Resource group delete lock.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-08 — Resource group delete lock (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic resource group delete lock deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-09 — Subnets match topology (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed subnets match topology against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet list -g "$RG" --vnet-name "$VNET" --query "[].{name:name,prefix:addressPrefix,prefixes:addressPrefixes}" -o json
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: Subnets match topology.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-10 — Subnets match topology (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic subnets match topology deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-11 — Azure location (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed azure location against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az group show -n "$RG" --query location -o tsv
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: Azure location.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-12 — Azure location (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic azure location deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-13 — Environment tag (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed environment tag against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az group show -n "$RG" --query "tags.Environment" -o tsv
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: Environment tag.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-14 — Environment tag (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic environment tag deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-15 — Owner tag (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed owner tag against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az group show -n "$RG" --query "tags.Owner" -o tsv
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: Owner tag.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-16 — Owner tag (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic owner tag deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-17 — VNet resource ID (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed vnet resource id against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet show -g "$RG" -n "$VNET" --query id -o tsv
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: VNet resource ID.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-18 — VNet resource ID (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic vnet resource id deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-19 — Terraform drift (positive observation)

**Execution environment:** Approval-gated isolated CI (state-lock aware)

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed terraform drift against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: Terraform drift.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-20 — Terraform drift (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic terraform drift deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-21 — Single IaC ownership (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed single iac ownership against the approved design and Step 23 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
git ls-files "infra/**/*.tf" "infra/*.tf"
```

**Expected:** Match RG/VNet resource IDs, tags, region, resource locks, IaC ownership and independently approved drift evidence. Specific focus: Single IaC ownership.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T23-22 — Single IaC ownership (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T23-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic single iac ownership deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-01 — Gateway-exclusive subnet (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed gateway-exclusive subnet against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_AGW" -o json
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: Gateway-exclusive subnet.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-02 — Gateway-exclusive subnet (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic gateway-exclusive subnet deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-03 — Gateway subnet capacity (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed gateway subnet capacity against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_AGW" --query "addressPrefix" -o tsv
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: Gateway subnet capacity.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-04 — Gateway subnet capacity (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic gateway subnet capacity deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-05 — Application Gateway delegation (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed application gateway delegation against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_AGW" --query delegations -o json
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: Application Gateway delegation.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-06 — Application Gateway delegation (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic application gateway delegation deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-07 — Non-Gateway IP configurations (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed non-gateway ip configurations against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_AGW" --query ipConfigurations -o json
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: Non-Gateway IP configurations.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-08 — Non-Gateway IP configurations (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic non-gateway ip configurations deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-09 — Gateway scale headroom (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed gateway scale headroom against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".gateway.approved_capacity > 0" "$NETWORK_BASELINE"
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: Gateway scale headroom.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-10 — Gateway scale headroom (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic gateway scale headroom deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-11 — Gateway NSG association (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed gateway nsg association against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_AGW" --query "networkSecurityGroup.id" -o tsv
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: Gateway NSG association.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-12 — Gateway NSG association (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic gateway nsg association deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-13 — Gateway UDR association (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed gateway udr association against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_AGW" --query "routeTable.id" -o tsv
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: Gateway UDR association.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-14 — Gateway UDR association (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic gateway udr association deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-15 — VNet/subnet identity (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed vnet/subnet identity against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_AGW" --query id -o tsv
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: VNet/subnet identity.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-16 — VNet/subnet identity (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic vnet/subnet identity deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-17 — Regional alignment (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed regional alignment against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".gateway.region == .vnet.region" "$NETWORK_BASELINE"
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: Regional alignment.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-18 — Regional alignment (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic regional alignment deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-19 — Gateway subnet drift (positive observation)

**Execution environment:** Approval-gated isolated CI (state-lock aware)

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed gateway subnet drift against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: Gateway subnet drift.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-20 — Gateway subnet drift (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic gateway subnet drift deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-21 — Gateway provisioning status (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed gateway provisioning status against the approved design and Step 24 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network application-gateway show -g "$RG" -n "$APPGW" --query provisioningState -o tsv
```

**Expected:** Confirm gateway-only subnet, correct delegation, available IP capacity, NSG/UDR compatibility, and healthy provisioning. Specific focus: Gateway provisioning status.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T24-22 — Gateway provisioning status (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T24-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic gateway provisioning status deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-01 — Dedicated VNet integration subnet (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed dedicated vnet integration subnet against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_APP" --query id -o tsv
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: Dedicated VNet integration subnet.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-02 — Dedicated VNet integration subnet (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic dedicated vnet integration subnet deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-03 — Microsoft.Web/serverFarms delegation (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed microsoft.web/serverfarms delegation against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_APP" --query delegations -o json
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: Microsoft.Web/serverFarms delegation.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-04 — Microsoft.Web/serverFarms delegation (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic microsoft.web/serverfarms delegation deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-05 — Outbound/inbound subnet separation (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed outbound/inbound subnet separation against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_PE" --query id -o tsv
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: Outbound/inbound subnet separation.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-06 — Outbound/inbound subnet separation (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic outbound/inbound subnet separation deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-07 — Integration subnet address headroom (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed integration subnet address headroom against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_APP" --query addressPrefix -o tsv
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: Integration subnet address headroom.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-08 — Integration subnet address headroom (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic integration subnet address headroom deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-09 — Egress NSG association (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed egress nsg association against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_APP" --query "networkSecurityGroup.id" -o tsv
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: Egress NSG association.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-10 — Egress NSG association (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic egress nsg association deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-11 — Egress route table (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed egress route table against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_APP" --query "routeTable.id" -o tsv
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: Egress route table.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-12 — Egress route table (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic egress route table deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-13 — Route All configuration (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed route all configuration against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az webapp show -g "$RG" -n "$WEB_APP" --query "siteConfig.vnetRouteAllEnabled" -o tsv
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: Route All configuration.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-14 — Route All configuration (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic route all configuration deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-15 — Outbound DNS resolution (positive observation)

**Execution environment:** Authorized internal network runner

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed outbound dns resolution against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
dig +short "$DNS_TEST_FQDN"
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: Outbound DNS resolution.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-16 — Outbound DNS resolution (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic outbound dns resolution deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-17 — Least-privilege egress destinations (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed least-privilege egress destinations against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_APP" -o json
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: Least-privilege egress destinations.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-18 — Least-privilege egress destinations (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic least-privilege egress destinations deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-19 — Web App integration subnet ID (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed web app integration subnet id against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az webapp show -g "$RG" -n "$WEB_APP" --query "virtualNetworkSubnetId" -o tsv
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: Web App integration subnet ID.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-20 — Web App integration subnet ID (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic web app integration subnet id deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-21 — VNet integration drift (positive observation)

**Execution environment:** Approval-gated isolated CI (state-lock aware)

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed vnet integration drift against the approved design and Step 25 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
```

**Expected:** Confirm separate outbound integration subnet, Microsoft.Web/serverFarms delegation, headroom, intended NSG/UDR and private egress resolution. Specific focus: VNet integration drift.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T25-22 — VNet integration drift (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T25-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic vnet integration drift deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-01 — Private Endpoint subnet zoning (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed private endpoint subnet zoning against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet list -g "$RG" --vnet-name "$VNET" -o json
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: Private Endpoint subnet zoning.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-02 — Private Endpoint subnet zoning (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic private endpoint subnet zoning deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-03 — NSG association on PE subnet (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed nsg association on pe subnet against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_PE" --query "networkSecurityGroup.id" -o tsv
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: NSG association on PE subnet.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-04 — NSG association on PE subnet (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic nsg association on pe subnet deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-05 — Private Endpoint network policies (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed private endpoint network policies against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_PE" --query "privateEndpointNetworkPolicies" -o tsv
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: Private Endpoint network policies.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-06 — Private Endpoint network policies (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic private endpoint network policies deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-07 — UDR association on PE subnet (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed udr association on pe subnet against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_PE" --query "routeTable.id" -o tsv
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: UDR association on PE subnet.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-08 — UDR association on PE subnet (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic udr association on pe subnet deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-09 — Private IP assignment (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed private ip assignment against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-endpoint list -g "$RG" --query "[].{name:name,ips:customDnsConfigs}" -o json
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: Private IP assignment.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-10 — Private IP assignment (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic private ip assignment deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-11 — Authorized PE source addresses (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed authorized pe source addresses against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_PE" -o json
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: Authorized PE source addresses.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-12 — Authorized PE source addresses (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic authorized pe source addresses deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-13 — Unauthorized PE sources denied (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed unauthorized pe sources denied against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_PE" -o json
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: Unauthorized PE sources denied.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-14 — Unauthorized PE sources denied (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic unauthorized pe sources denied deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-15 — Minimum TCP 443 allow rules (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed minimum tcp 443 allow rules against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_PE" -o json
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: Minimum TCP 443 allow rules.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-16 — Minimum TCP 443 allow rules (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic minimum tcp 443 allow rules deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-17 — Application Security Group membership (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed application security group membership against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-endpoint list -g "$RG" --query "[].{id:id,asg:applicationSecurityGroups}" -o json
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: Application Security Group membership.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-18 — Application Security Group membership (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic application security group membership deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-19 — PE-path flow-log evidence (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed pe-path flow-log evidence against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network watcher flow-log list -g "$WATCHER_RG" -o json
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: PE-path flow-log evidence.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-20 — PE-path flow-log evidence (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic pe-path flow-log evidence deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-21 — Isolated negative-test boundary (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed isolated negative-test boundary against the approved design and Step 26 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".change_rules.isolated_test == true" "$NETWORK_BASELINE"
```

**Expected:** Validate PE trust-zone segmentation, effective NSG/UDR policies, private IP allocation and authorized versus unauthorized traffic; require runtime evidence. Specific focus: Isolated negative-test boundary.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T26-22 — Isolated negative-test boundary (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T26-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic isolated negative-test boundary deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-01 — Resolver inbound delegation (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed resolver inbound delegation against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet list -g "$RG" --vnet-name "$VNET" -o json
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: Resolver inbound delegation.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-02 — Resolver inbound delegation (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic resolver inbound delegation deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-03 — Resolver outbound delegation (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed resolver outbound delegation against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet list -g "$RG" --vnet-name "$VNET" -o json
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: Resolver outbound delegation.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-04 — Resolver outbound delegation (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic resolver outbound delegation deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-05 — Inbound/outbound subnet separation (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed inbound/outbound subnet separation against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".resolver.inbound_subnet != .resolver.outbound_subnet" "$NETWORK_BASELINE"
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: Inbound/outbound subnet separation.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-06 — Inbound/outbound subnet separation (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic inbound/outbound subnet separation deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-07 — On-prem conditional forwarders (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed on-prem conditional forwarders against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".resolver.conditional_forwarders | length > 0" "$DNS_BASELINE"
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: On-prem conditional forwarders.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-08 — On-prem conditional forwarders (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic on-prem conditional forwarders deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-09 — Required Private DNS zones (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed required private dns zones against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-dns zone list -g "$DNS_RG" --query "[].name" -o json
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: Required Private DNS zones.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-10 — Required Private DNS zones (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic required private dns zones deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-11 — DNS-to-VNet links (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed dns-to-vnet links against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-dns link vnet list -g "$DNS_RG" --zone-name "$APP_PRIVATE_ZONE" -o json
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: DNS-to-VNet links.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-12 — DNS-to-VNet links (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic dns-to-vnet links deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-13 — UDP 53 resolution (positive observation)

**Execution environment:** Authorized internal network runner

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed udp 53 resolution against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
dig +time=2 +tries=1 +short @"$DNS_RESOLVER_IP" "$DNS_TEST_FQDN" A
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: UDP 53 resolution.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-14 — UDP 53 resolution (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic udp 53 resolution deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-15 — TCP 53 resolution (positive observation)

**Execution environment:** Authorized internal network runner

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed tcp 53 resolution against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
dig +tcp +time=2 +tries=1 +short @"$DNS_RESOLVER_IP" "$DNS_TEST_FQDN" A
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: TCP 53 resolution.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-16 — TCP 53 resolution (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic tcp 53 resolution deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-17 — Resolver routing (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed resolver routing against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_RESOLVER_IN" -o json
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: Resolver routing.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-18 — Resolver routing (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic resolver routing deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-19 — DNS error classification (positive observation)

**Execution environment:** Authorized internal network runner

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed dns error classification against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
dig +time=2 +tries=1 @"$DNS_RESOLVER_IP" "$DNS_TEST_FQDN" A
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: DNS error classification.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-20 — DNS error classification (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic dns error classification deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-21 — Private A record evidence (positive observation)

**Execution environment:** Authorized internal network runner

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed private a record evidence against the approved design and Step 27 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
dig +short "$DNS_TEST_FQDN" A
```

**Expected:** Verify resolver subnet delegation and isolation, conditional-forwarder coverage, matching private A responses over UDP and TCP, and failure classification. Specific focus: Private A record evidence.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T27-22 — Private A record evidence (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T27-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic private a record evidence deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-01 — Client-to-Gateway TCP 443 (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed client-to-gateway tcp 443 against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_AGW" -o json
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: Client-to-Gateway TCP 443.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-02 — Client-to-Gateway TCP 443 (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic client-to-gateway tcp 443 deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-03 — Permitted client CIDRs (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed permitted client cidrs against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_AGW" -o json
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: Permitted client CIDRs.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-04 — Permitted client CIDRs (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic permitted client cidrs deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-05 — AzureLoadBalancer allowance (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed azureloadbalancer allowance against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_AGW" -o json
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: AzureLoadBalancer allowance.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-06 — AzureLoadBalancer allowance (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic azureloadbalancer allowance deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-07 — GatewayManager requirements in isolation mode (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed gatewaymanager requirements in isolation mode against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".gateway.network_isolation == true" "$NETWORK_BASELINE"
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: GatewayManager requirements in isolation mode.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-08 — GatewayManager requirements in isolation mode (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic gatewaymanager requirements in isolation mode deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-09 — Required control-plane egress (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed required control-plane egress against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_AGW" -o json
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: Required control-plane egress.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-10 — Required control-plane egress (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic required control-plane egress deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-11 — Allow/Deny precedence (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed allow/deny precedence against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_AGW" -o json
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: Allow/Deny precedence.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-12 — Allow/Deny precedence (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic allow/deny precedence deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-13 — NSG priority uniqueness (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed nsg priority uniqueness against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_AGW" --query "[].{name:name,priority:priority}" -o json
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: NSG priority uniqueness.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-14 — NSG priority uniqueness (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic nsg priority uniqueness deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-15 — Gateway operational health (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed gateway operational health against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network application-gateway show -g "$RG" -n "$APPGW" --query "{provisioningState:provisioningState,operationalState:operationalState}" -o json
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: Gateway operational health.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-16 — Gateway operational health (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic gateway operational health deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-17 — Backend probe health (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed backend probe health against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network application-gateway show-backend-health -g "$RG" -n "$APPGW" -o json
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: Backend probe health.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-18 — Backend probe health (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic backend probe health deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-19 — Production NSG change restriction (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed production nsg change restriction against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".change_rules.no_production_nsg_mutations == true" "$NETWORK_BASELINE"
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: Production NSG change restriction.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-20 — Production NSG change restriction (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic production nsg change restriction deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-21 — Approved NSG change log (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed approved nsg change log against the approved design and Step 28 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor activity-log list --resource-group "$RG" --max-events 30 -o json
```

**Expected:** Validate effective gateway NSG allow/deny ordering, constrained corporate sources, control-plane exceptions, operational state and backend health. Specific focus: Approved NSG change log.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T28-22 — Approved NSG change log (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T28-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic approved nsg change log deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-01 — Entra ID outbound dependencies (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed entra id outbound dependencies against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".dependencies.entra | length > 0" "$NETWORK_BASELINE"
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: Entra ID outbound dependencies.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-02 — Entra ID outbound dependencies (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic entra id outbound dependencies deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-03 — Azure Monitor outbound dependencies (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed azure monitor outbound dependencies against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".dependencies.monitor | length > 0" "$NETWORK_BASELINE"
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: Azure Monitor outbound dependencies.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-04 — Azure Monitor outbound dependencies (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic azure monitor outbound dependencies deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-05 — Internal DNS egress (positive observation)

**Execution environment:** Authorized internal network runner

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed internal dns egress against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
dig +short "$DNS_TEST_FQDN" A
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: Internal DNS egress.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-06 — Internal DNS egress (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic internal dns egress deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-07 — Certificate revocation (CRL/OCSP) (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed certificate revocation (crl/ocsp) against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".dependencies.certificate_validation | length > 0" "$NETWORK_BASELINE"
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: Certificate revocation (CRL/OCSP).

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-08 — Certificate revocation (CRL/OCSP) (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic certificate revocation (crl/ocsp) deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-09 — PaaS Private Endpoint TCP 443 (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed paas private endpoint tcp 443 against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_APP" -o json
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: PaaS Private Endpoint TCP 443.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-10 — PaaS Private Endpoint TCP 443 (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic paas private endpoint tcp 443 deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-11 — UDR next hop (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed udr next hop against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network route-table route list -g "$RG" --route-table-name "$ROUTE_TABLE" -o json
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: UDR next hop.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-12 — UDR next hop (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic udr next hop deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-13 — Firewall/NVA routing (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed firewall/nva routing against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network route-table show -g "$RG" -n "$ROUTE_TABLE" -o json
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: Firewall/NVA routing.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-14 — Firewall/NVA routing (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic firewall/nva routing deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-15 — Unapproved internet egress blocked (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed unapproved internet egress blocked against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG_APP" -o json
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: Unapproved internet egress blocked.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-16 — Unapproved internet egress blocked (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic unapproved internet egress blocked deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-17 — Dependency ownership/approval (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed dependency ownership/approval against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".dependencies.approved == true" "$NETWORK_BASELINE"
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: Dependency ownership/approval.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-18 — Dependency ownership/approval (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic dependency ownership/approval deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-19 — Private application health (positive observation)

**Execution environment:** Authorized internal network runner

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed private application health against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
curl --noproxy "*" --max-time 10 -sS -o /dev/null -w '%{http_code}\n' "https://${APP_PRIVATE_FQDN}/healthz"
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: Private application health.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-20 — Private application health (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic private application health deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-21 — Denied-egress telemetry (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed denied-egress telemetry against the approved design and Step 29 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor activity-log list -g "$RG" --max-events 30 -o json
```

**Expected:** Verify Entra/monitor/certificate-validation dependency paths, Private Endpoint 443, controlled internet egress and actual deny telemetry. Specific focus: Denied-egress telemetry.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T29-22 — Denied-egress telemetry (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T29-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic denied-egress telemetry deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-01 — App Service Private DNS zone (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed app service private dns zone against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-dns zone show -g "$DNS_RG" -n privatelink.azurewebsites.net -o json
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: App Service Private DNS zone.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-02 — App Service Private DNS zone (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic app service private dns zone deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-03 — Azure OpenAI Private DNS zone (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed azure openai private dns zone against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-dns zone show -g "$DNS_RG" -n privatelink.openai.azure.com -o json
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: Azure OpenAI Private DNS zone.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-04 — Azure OpenAI Private DNS zone (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic azure openai private dns zone deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-05 — Azure AI Search Private DNS zone (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed azure ai search private dns zone against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-dns zone show -g "$DNS_RG" -n privatelink.search.windows.net -o json
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: Azure AI Search Private DNS zone.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-06 — Azure AI Search Private DNS zone (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic azure ai search private dns zone deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-07 — Cosmos DB Private DNS zone (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed cosmos db private dns zone against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-dns zone show -g "$DNS_RG" -n privatelink.documents.azure.com -o json
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: Cosmos DB Private DNS zone.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-08 — Cosmos DB Private DNS zone (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic cosmos db private dns zone deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-09 — Key Vault Private DNS zone (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed key vault private dns zone against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-dns zone show -g "$DNS_RG" -n privatelink.vaultcore.azure.net -o json
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: Key Vault Private DNS zone.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-10 — Key Vault Private DNS zone (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic key vault private dns zone deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-11 — PE DNS zone groups (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed pe dns zone groups against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-endpoint dns-zone-group list -g "$RG" --endpoint-name "$PE_APP" -o json
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: PE DNS zone groups.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-12 — PE DNS zone groups (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic pe dns zone groups deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-13 — Private DNS VNet links (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed private dns vnet links against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-dns link vnet list -g "$DNS_RG" --zone-name privatelink.azurewebsites.net -o json
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: Private DNS VNet links.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-14 — Private DNS VNet links (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic private dns vnet links deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-15 — DNS Resolver forwarding (positive observation)

**Execution environment:** Authorized internal network runner

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed dns resolver forwarding against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
dig +time=2 +tries=1 +short @"$DNS_RESOLVER_IP" "$DNS_TEST_FQDN" A
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: DNS Resolver forwarding.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-16 — DNS Resolver forwarding (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic dns resolver forwarding deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-17 — Duplicate Private DNS prevention (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed duplicate private dns prevention against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".private_dns.centralized == true" "$DNS_BASELINE"
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: Duplicate Private DNS prevention.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-18 — Duplicate Private DNS prevention (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic duplicate private dns prevention deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-19 — Ordinary FQDN CNAME chain (positive observation)

**Execution environment:** Authorized internal network runner

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed ordinary fqdn cname chain against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
dig +short "$APP_PRIVATE_FQDN" CNAME
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: Ordinary FQDN CNAME chain.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-20 — Ordinary FQDN CNAME chain (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic ordinary fqdn cname chain deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-21 — Resolved private A record (positive observation)

**Execution environment:** Authorized internal network runner

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed resolved private a record against the approved design and Step 30 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
dig +short "$APP_PRIVATE_FQDN" A
```

**Expected:** Confirm official private DNS zone, group and VNet link configurations; ordinary FQDNs must resolve through intended resolver to signed PE private IP. Specific focus: Resolved private A record.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T30-22 — Resolved private A record (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T30-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic resolved private a record deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-01 — AMPLS applicability decision (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed ampls applicability decision against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e '.monitor.ampls.required | type == "boolean"' "$MONITOR_BASELINE"
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: AMPLS applicability decision.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-02 — AMPLS applicability decision (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic ampls applicability decision deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-03 — AMPLS resource existence (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed ampls resource existence against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az resource show --ids "$AMPLS_RESOURCE_ID" -o json
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: AMPLS resource existence.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-04 — AMPLS resource existence (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic ampls resource existence deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-05 — Log Analytics workspace availability (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed log analytics workspace availability against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor log-analytics workspace show -g "$MONITOR_RG" -n "$WORKSPACE" -o json
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: Log Analytics workspace availability.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-06 — Log Analytics workspace availability (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic log analytics workspace availability deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-07 — Application Insights target (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed application insights target against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az resource show --ids "$APPINSIGHTS_RESOURCE_ID" -o json
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: Application Insights target.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-08 — Application Insights target (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic application insights target deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-09 — AMPLS Private Endpoint approval (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed ampls private endpoint approval against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-endpoint show -g "$RG" -n "$PE_AMPLS" -o json
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: AMPLS Private Endpoint approval.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-10 — AMPLS Private Endpoint approval (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic ampls private endpoint approval deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-11 — AMPLS private DNS zones (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed ampls private dns zones against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az network private-endpoint dns-zone-group list -g "$RG" --endpoint-name "$PE_AMPLS" -o json
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: AMPLS private DNS zones.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-12 — AMPLS private DNS zones (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic ampls private dns zones deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-13 — Log ingestion test approval (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed log ingestion test approval against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".monitor.ingestion_test.approved == true" "$MONITOR_BASELINE"
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: Log ingestion test approval.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-14 — Log ingestion test approval (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic log ingestion test approval deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-15 — Log query test approval (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed log query test approval against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".monitor.query_test.approved == true" "$MONITOR_BASELINE"
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: Log query test approval.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-16 — Log query test approval (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic log query test approval deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-17 — Least-privilege query identity (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed least-privilege query identity against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az role assignment list --scope "$WORKSPACE_RESOURCE_ID" -o json
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: Least-privilege query identity.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-18 — Least-privilege query identity (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic least-privilege query identity deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-19 — Approved monitoring public exceptions (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed approved monitoring public exceptions against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e '.monitor.public_access_exceptions | type == "array"' "$MONITOR_BASELINE"
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: Approved monitoring public exceptions.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-20 — Approved monitoring public exceptions (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic approved monitoring public exceptions deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-21 — Missing-monitoring alert (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed missing-monitoring alert against the approved design and Step 31 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor metrics alert list -g "$MONITOR_RG" -o json
```

**Expected:** Validate AMPLS applicability, PE/DNS/RBAC and correlated monitoring ingestion/query; merely creating an alert is insufficient. Specific focus: Missing-monitoring alert.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T31-22 — Missing-monitoring alert (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T31-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic missing-monitoring alert deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-01 — Log Analytics workspace baseline (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed log analytics workspace baseline against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor log-analytics workspace show -g "$MONITOR_RG" -n "$WORKSPACE" -o json
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: Log Analytics workspace baseline.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-02 — Log Analytics workspace baseline (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-02 --spec specs/phase3_264.json
```

**Expected:** Synthetic log analytics workspace baseline deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-03 — Application Insights workspace link (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed application insights workspace link against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az resource show --ids "$APPINSIGHTS_RESOURCE_ID" -o json
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: Application Insights workspace link.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-04 — Application Insights workspace link (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-04 --spec specs/phase3_264.json
```

**Expected:** Synthetic application insights workspace link deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-05 — Application Gateway access logs (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed application gateway access logs against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor diagnostic-settings list --resource "$APPGW_RESOURCE_ID" -o json
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: Application Gateway access logs.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-06 — Application Gateway access logs (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-06 --spec specs/phase3_264.json
```

**Expected:** Synthetic application gateway access logs deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-07 — WAF firewall logs (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed waf firewall logs against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor diagnostic-settings list --resource "$APPGW_RESOURCE_ID" -o json
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: WAF firewall logs.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-08 — WAF firewall logs (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-08 --spec specs/phase3_264.json
```

**Expected:** Synthetic waf firewall logs deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-09 — App Service diagnostic logs (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed app service diagnostic logs against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor diagnostic-settings list --resource "$WEBAPP_RESOURCE_ID" -o json
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: App Service diagnostic logs.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-10 — App Service diagnostic logs (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-10 --spec specs/phase3_264.json
```

**Expected:** Synthetic app service diagnostic logs deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-11 — Azure OpenAI diagnostic logs (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed azure openai diagnostic logs against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor diagnostic-settings list --resource "$OPENAI_RESOURCE_ID" -o json
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: Azure OpenAI diagnostic logs.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-12 — Azure OpenAI diagnostic logs (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-12 --spec specs/phase3_264.json
```

**Expected:** Synthetic azure openai diagnostic logs deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-13 — Cosmos DB diagnostics (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed cosmos db diagnostics against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor diagnostic-settings list --resource "$COSMOS_RESOURCE_ID" -o json
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: Cosmos DB diagnostics.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-14 — Cosmos DB diagnostics (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-14 --spec specs/phase3_264.json
```

**Expected:** Synthetic cosmos db diagnostics deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-15 — VNet Flow Logs (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed vnet flow logs against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az resource show --ids "$VNET_FLOWLOG_RESOURCE_ID" -o json
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: VNet Flow Logs.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-16 — VNet Flow Logs (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-16 --spec specs/phase3_264.json
```

**Expected:** Synthetic vnet flow logs deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-17 — Log retention policy (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed log retention policy against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor log-analytics workspace show -g "$MONITOR_RG" -n "$WORKSPACE" --query retentionInDays -o tsv
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: Log retention policy.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-18 — Log retention policy (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-18 --spec specs/phase3_264.json
```

**Expected:** Synthetic log retention policy deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-19 — Monitoring cost signoff (positive observation)

**Execution environment:** Local signed baseline / CI review

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed monitoring cost signoff against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
jq -e ".monitor.cost.approved == true" "$MONITOR_BASELINE"
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: Monitoring cost signoff.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-20 — Monitoring cost signoff (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-20 --spec specs/phase3_264.json
```

**Expected:** Synthetic monitoring cost signoff deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-21 — Alert thresholds and action groups (positive observation)

**Execution environment:** Approved CI, scoped Azure read-only permission

**Preconditions:** Named approved target, subscription/asset identifiers, source revision, baseline, reviewer and scoped runner.

**Detailed procedure:**
1. Identify the control and exact approved resource ID, scope, source revision and expected setting.
2. Confirm runner authorization, correct subscription, expected private network, required variables, and tool version.
3. Collect read-only output using the command below; never interpolate unapproved resource names.
4. Independently compare the observed alert thresholds and action groups against the approved design and Step 32 acceptance rule; a command exit alone is not PASS.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
az monitor metrics alert list -g "$MONITOR_RG" -o json
```

**Expected:** Confirm diagnostic settings, actual log arrival, retention, VNet Flow Logs, action groups and controlled alert delivery. Specific focus: Alert thresholds and action groups.

**Evidence:** Approved baseline and asset ID; sanitized raw output; UTC; SHA-256; independent reviewer.

**Troubleshooting / false-green control:** Check actual resource existence, effective routes/assignments, Private DNS links and telemetry as applicable; inspect whether this command merely lists configuration.

**Azure live acceptance:** `NOT_READY` (not executed).

### AZ-T32-22 — Alert thresholds and action groups (offline synthetic deviation)

**Execution environment:** Offline Python / synthetic fixtures only

**Preconditions:** Offline source fixture and Python 3; no Azure authentication.

**Detailed procedure:**
1. Find the paired odd-numbered positive case and its checked-in synthetic control.
2. Select good, deliberately incorrect and missing synthetic observations. Do not change live cloud resources.
3. Execute only the local detector invocation below; compare the returned good/incorrect/missing classifications.
4. Expected: good fixture is accepted; incorrect fixture returns FAIL; missing evidence returns NOT_READY.
5. Preserve evidence SHA-256, UTC, immutable source version, reviewer and any exception approval.
6. If scope, approval, source, baseline or evidence is missing, classify NOT_READY; if verified observation contradicts the baseline, classify FAIL.

**Command (for the stated environment only):**
```bash
python3 scripts/phase3_guard.py --selftest AZ-T32-22 --spec specs/phase3_264.json
```

**Expected:** Synthetic alert thresholds and action groups deviation is classified FAIL, absent input NOT_READY; Azure blocking is **not** established.

**Evidence:** Rule and fixture hashes, self-test log, ID and synthetic-only marker.

**Troubleshooting / false-green control:** Never convert simulated PASS to Azure PASS; check rule fixture and the missing-data path.

**Azure live acceptance:** `NOT_READY` (not executed).
