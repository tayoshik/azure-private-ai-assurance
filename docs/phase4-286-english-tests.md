# Phase 4 — 286 Detailed English Test Procedures (Steps 33–45)

**Status:** Design and offline-detector validation only; **Azure live passes: 0; live acceptance: NOT_READY**. This document translates the original Stage 4 design. A syntactically valid command is *not* a proven Azure configuration. No Azure resources have been changed or queried for this publication.

## Test semantics and execution safety

- The 13 steps contain 11 distinct controls each; each control has one positive configuration/evidence check and one **synthetic-only** deviation-detector check, totalling **286 tests = 143 + 143**.
- `PASS` for a live case requires a real approved resource, signed baseline, correct environment and execution scope, observed output/time, intact evidence hash and independent approval. No such PASS is recorded here.
- `NOT_READY`: missing real implementation, credentials/approved runner, immutable baseline, service feature, version-pinned tool syntax, or reliable evidence.
- `FAIL`: independently verifiable observations contradict the signed requirement; no assumption that HTTP 403 or mere document existence proves success.
- `SKIPPED`: only for a conditionally *not adopted* feature where a signed applicability determination exists; do not skip an unimplemented requirement.
- The fixed Windows/WSL terminal does **not** run `az login`. Azure CLI examples belong in organization-approved OIDC CI; private DNS/HTTPS probes require an authorized VNet-connected runner. Plan, refresh-only plan, terraform test and apply are never executed in this publication; those operations need separate approval.
- `jq -e` tests that only check file fields or truthy values are *evidence preflight*, not authorization or security acceptance. Protect plan JSON, runtime logs, internal addresses, resource IDs, tokens and prompts from public repositories.
- Source quoted filters that would misparse `jq` are corrected transparently in JSON `command_edits`. Four Stage 45 resource-change placeholders are replaced by a conservative **offline** plan guard. Its output `REVIEW_REQUIRED` is not `PASS`.
- Conditional features such as ACR or Search Shared Private Link require an explicit adoption/waiver decision.

## Workstation and runner preparation (do not authenticate to Azure here)

```bash
set -Eeuo pipefail
python3 --version
python3 scripts/verify_phase4_english.py
python3 scripts/phase4_guard.py --selftest ALL --spec specs/phase4_286_source.json
python3 -m unittest discover -s tests -v
# Run these only inside an authorized pipeline with recorded approvals:
# az account show --output json
# az resource show --ids "$APPROVED_RESOURCE_ID" --output json
```

## Step-by-step source-mapped test catalogue


## Step 33 — Azure OpenAI account governance (22 tests)

**Source action:** Provision the approved Azure OpenAI account and keep public data-plane access disabled.
**Source provenance:** Runbook v1, Step 33. Preserve exact source IDs `AZ-T33-01` through `AZ-T33-22`.


### AZ-T33-01 — Azure OpenAI account type (POSITIVE)

- **Purpose / criterion:** Account kind is OpenAI and the exact resource ID matches the approved inventory
- **Deviation to detect:** An unrelated Cognitive Services kind is selected
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-01 (Step 33: Azure OpenAI account governance), control: Azure OpenAI account type.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Account kind is OpenAI and the exact resource ID matches the approved inventory** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account show -g "$RG" -n "$OPENAI_NAME" --query "{id:id,kind:kind}" -o json
```

- **Expected:** Account kind is OpenAI and the exact resource ID matches the approved inventory
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-02 — Azure OpenAI account type (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** An unrelated Cognitive Services kind is selected
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-02 and positive control AZ-T33-01: Azure OpenAI account type.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate an unrelated cognitive services kind is selected => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-03 — Custom subdomain (POSITIVE)

- **Purpose / criterion:** A non-empty custom subdomain matches the approved resource baseline
- **Deviation to detect:** The custom subdomain is missing or unapproved
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-03 (Step 33: Azure OpenAI account governance), control: Custom subdomain.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **A non-empty custom subdomain matches the approved resource baseline** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account show -g "$RG" -n "$OPENAI_NAME" --query "properties.customSubDomainName" -o tsv
```

- **Expected:** A non-empty custom subdomain matches the approved resource baseline
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-04 — Custom subdomain (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The custom subdomain is missing or unapproved
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-04 and positive control AZ-T33-03: Custom subdomain.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the custom subdomain is missing or unapproved => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-05 — Deployment region (POSITIVE)

- **Purpose / criterion:** The region meets approved model-availability and data-processing requirements
- **Deviation to detect:** An unapproved region is used
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-05 (Step 33: Azure OpenAI account governance), control: Deployment region.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The region meets approved model-availability and data-processing requirements** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account show -g "$RG" -n "$OPENAI_NAME" --query location -o tsv
```

- **Expected:** The region meets approved model-availability and data-processing requirements
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-06 — Deployment region (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** An unapproved region is used
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-06 and positive control AZ-T33-05: Deployment region.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate an unapproved region is used => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-07 — Account SKU (POSITIVE)

- **Purpose / criterion:** The provisioned SKU equals the approved design
- **Deviation to detect:** An unauthorized or unsuitable SKU is used
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-07 (Step 33: Azure OpenAI account governance), control: Account SKU.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The provisioned SKU equals the approved design** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account show -g "$RG" -n "$OPENAI_NAME" --query sku.name -o tsv
```

- **Expected:** The provisioned SKU equals the approved design
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-08 — Account SKU (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** An unauthorized or unsuitable SKU is used
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-08 and positive control AZ-T33-07: Account SKU.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate an unauthorized or unsuitable sku is used => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-09 — Public network access (POSITIVE)

- **Purpose / criterion:** The account publicNetworkAccess property is Disabled
- **Deviation to detect:** Public data-plane access is enabled
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-09 (Step 33: Azure OpenAI account governance), control: Public network access.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The account publicNetworkAccess property is Disabled** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account show -g "$RG" -n "$OPENAI_NAME" --query properties.publicNetworkAccess -o tsv
```

- **Expected:** The account publicNetworkAccess property is Disabled
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-10 — Public network access (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Public data-plane access is enabled
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-10 and positive control AZ-T33-09: Public network access.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate public data-plane access is enabled => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-11 — Local key authentication (POSITIVE)

- **Purpose / criterion:** disableLocalAuth is true when the signed security policy prohibits key authentication
- **Deviation to detect:** API-key authentication remains enabled without an exception
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-11 (Step 33: Azure OpenAI account governance), control: Local key authentication.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **disableLocalAuth is true when the signed security policy prohibits key authentication** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account show -g "$RG" -n "$OPENAI_NAME" --query properties.disableLocalAuth -o tsv
```

- **Expected:** disableLocalAuth is true when the signed security policy prohibits key authentication
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-12 — Local key authentication (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** API-key authentication remains enabled without an exception
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-12 and positive control AZ-T33-11: Local key authentication.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate api-key authentication remains enabled without an exception => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-13 — Network ACL (POSITIVE)

- **Purpose / criterion:** Network ACLs and any exceptions satisfy the signed least-privilege policy
- **Deviation to detect:** Broad unapproved network allowances are present
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-13 (Step 33: Azure OpenAI account governance), control: Network ACL.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Network ACLs and any exceptions satisfy the signed least-privilege policy** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account network-rule list -g "$RG" -n "$OPENAI_NAME" -o json
```

- **Expected:** Network ACLs and any exceptions satisfy the signed least-privilege policy
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-14 — Network ACL (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Broad unapproved network allowances are present
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-14 and positive control AZ-T33-13: Network ACL.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate broad unapproved network allowances are present => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-15 — Provisioning status (POSITIVE)

- **Purpose / criterion:** The account provisioning state is Succeeded
- **Deviation to detect:** Provisioning has failed or is incomplete
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-15 (Step 33: Azure OpenAI account governance), control: Provisioning status.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The account provisioning state is Succeeded** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account show -g "$RG" -n "$OPENAI_NAME" --query properties.provisioningState -o tsv
```

- **Expected:** The account provisioning state is Succeeded
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-16 — Provisioning status (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Provisioning has failed or is incomplete
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-16 and positive control AZ-T33-15: Provisioning status.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate provisioning has failed or is incomplete => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-17 — Private Endpoint dependency (POSITIVE)

- **Purpose / criterion:** A correctly linked, approved OpenAI Private Endpoint is verified with Step 38
- **Deviation to detect:** The required Private Endpoint is absent or not approved
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-17 (Step 33: Azure OpenAI account governance), control: Private Endpoint dependency.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **A correctly linked, approved OpenAI Private Endpoint is verified with Step 38** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint-connection list -g "$RG" -n "$OPENAI_NAME" --type Microsoft.CognitiveServices/accounts -o json
```

- **Expected:** A correctly linked, approved OpenAI Private Endpoint is verified with Step 38
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-18 — Private Endpoint dependency (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The required Private Endpoint is absent or not approved
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-18 and positive control AZ-T33-17: Private Endpoint dependency.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the required private endpoint is absent or not approved => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-19 — Diagnostic settings (POSITIVE)

- **Purpose / criterion:** Approved log categories, destination, and retention settings are enabled
- **Deviation to detect:** OpenAI audit diagnostics are missing
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-19 (Step 33: Azure OpenAI account governance), control: Diagnostic settings.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Approved log categories, destination, and retention settings are enabled** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az monitor diagnostic-settings list --resource "$OPENAI_ID" -o json
```

- **Expected:** Approved log categories, destination, and retention settings are enabled
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-20 — Diagnostic settings (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** OpenAI audit diagnostics are missing
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-20 and positive control AZ-T33-19: Diagnostic settings.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate openai audit diagnostics are missing => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-21 — Configuration drift (POSITIVE)

- **Purpose / criterion:** A scoped, approved plan and review show no unexplained drift
- **Deviation to detect:** A live configuration diverges from IaC
- **Execution class / priority:** `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T33-21 (Step 33: Azure OpenAI account governance), control: Configuration drift.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **A scoped, approved plan and review show no unexplained drift** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
```

- **Expected:** A scoped, approved plan and review show no unexplained drift
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T33-22 — Configuration drift (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A live configuration diverges from IaC
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T33-22 and positive control AZ-T33-21: Configuration drift.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a live configuration diverges from iac => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T33-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 34 — Model deployment and lifecycle (22 tests)

**Source action:** Deploy explicitly approved models/versions with quota, filter, regional and rollback controls.
**Source provenance:** Runbook v1, Step 34. Preserve exact source IDs `AZ-T34-01` through `AZ-T34-22`.


### AZ-T34-01 — Approved model deployment (POSITIVE)

- **Purpose / criterion:** Every required model deployment belongs to the signed model inventory
- **Deviation to detect:** An unintended model is deployed
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-01 (Step 34: Model deployment and lifecycle), control: Approved model deployment.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Every required model deployment belongs to the signed model inventory** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account deployment list -g "$RG" -n "$OPENAI_NAME" --query "[].{name:name,model:properties.model.name}" -o json
```

- **Expected:** Every required model deployment belongs to the signed model inventory
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-02 — Approved model deployment (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** An unintended model is deployed
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-02 and positive control AZ-T34-01: Approved model deployment.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate an unintended model is deployed => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-03 — Model version pinning (POSITIVE)

- **Purpose / criterion:** The deployed model version equals the approved version
- **Deviation to detect:** The model version changes without review
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-03 (Step 34: Model deployment and lifecycle), control: Model version pinning.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The deployed model version equals the approved version** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account deployment list -g "$RG" -n "$OPENAI_NAME" --query "[].{name:name,version:properties.model.version}" -o json
```

- **Expected:** The deployed model version equals the approved version
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-04 — Model version pinning (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The model version changes without review
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-04 and positive control AZ-T34-03: Model version pinning.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the model version changes without review => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-05 — Deployment type (POSITIVE)

- **Purpose / criterion:** Deployment SKU/type meets approved geography and data-processing constraints
- **Deviation to detect:** Deployment type violates processing boundary
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-05 (Step 34: Model deployment and lifecycle), control: Deployment type.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Deployment SKU/type meets approved geography and data-processing constraints** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account deployment list -g "$RG" -n "$OPENAI_NAME" --query "[].{name:name,sku:sku}" -o json
```

- **Expected:** Deployment SKU/type meets approved geography and data-processing constraints
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-06 — Deployment type (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Deployment type violates processing boundary
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-06 and positive control AZ-T34-05: Deployment type.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate deployment type violates processing boundary => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-07 — Capacity (POSITIVE)

- **Purpose / criterion:** Deployment capacity is within the approved limit and meets the workload minimum
- **Deviation to detect:** Capacity is insufficient or exceeds approval
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-07 (Step 34: Model deployment and lifecycle), control: Capacity.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Deployment capacity is within the approved limit and meets the workload minimum** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account deployment list -g "$RG" -n "$OPENAI_NAME" --query "[].{name:name,capacity:sku.capacity}" -o json
```

- **Expected:** Deployment capacity is within the approved limit and meets the workload minimum
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-08 — Capacity (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Capacity is insufficient or exceeds approval
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-08 and positive control AZ-T34-07: Capacity.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate capacity is insufficient or exceeds approval => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-09 — Regional quota (POSITIVE)

- **Purpose / criterion:** Usage plus planned growth remains inside the approved quota in the selected region
- **Deviation to detect:** Quota is exhausted or unverified
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-09 (Step 34: Model deployment and lifecycle), control: Regional quota.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Usage plus planned growth remains inside the approved quota in the selected region** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices usage list -g "$RG" -n "$OPENAI_NAME" -o json
```

- **Expected:** Usage plus planned growth remains inside the approved quota in the selected region
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-10 — Regional quota (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Quota is exhausted or unverified
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-10 and positive control AZ-T34-09: Regional quota.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate quota is exhausted or unverified => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-11 — Content safety configuration (POSITIVE)

- **Purpose / criterion:** The deployed content-filter policy matches the approved safety baseline
- **Deviation to detect:** Required content filtering is disabled
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-11 (Step 34: Model deployment and lifecycle), control: Content safety configuration.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The deployed content-filter policy matches the approved safety baseline** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cognitiveservices account deployment list -g "$RG" -n "$OPENAI_NAME" -o json
```

- **Expected:** The deployed content-filter policy matches the approved safety baseline
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-12 — Content safety configuration (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Required content filtering is disabled
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-12 and positive control AZ-T34-11: Content safety configuration.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate required content filtering is disabled => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-13 — Data-processing geography (POSITIVE)

- **Purpose / criterion:** Processing geography for the selected deployment type is approved
- **Deviation to detect:** Requests may be processed in an unapproved geography
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-13 (Step 34: Model deployment and lifecycle), control: Data-processing geography.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Processing geography for the selected deployment type is approved** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
jq -e '.ai.data_residency.approved == true' "$AI_BASELINE"
```

- **Expected:** Processing geography for the selected deployment type is approved
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-14 — Data-processing geography (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Requests may be processed in an unapproved geography
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-14 and positive control AZ-T34-13: Data-processing geography.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate requests may be processed in an unapproved geography => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-15 — Model update governance (POSITIVE)

- **Purpose / criterion:** Version changes and retirement require approval, testing and rollback planning
- **Deviation to detect:** Automatic updates lack governance
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-15 (Step 34: Model deployment and lifecycle), control: Model update governance.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Version changes and retirement require approval, testing and rollback planning** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
jq -e '.ai.model_update.approval_id | type == "string"' "$AI_BASELINE"
```

- **Expected:** Version changes and retirement require approval, testing and rollback planning
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-16 — Model update governance (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Automatic updates lack governance
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-16 and positive control AZ-T34-15: Model update governance.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate automatic updates lack governance => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-17 — Model rollback (POSITIVE)

- **Purpose / criterion:** The runbook identifies a compatible previous deployment, triggers and recovery steps
- **Deviation to detect:** There is no feasible rollback
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-17 (Step 34: Model deployment and lifecycle), control: Model rollback.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The runbook identifies a compatible previous deployment, triggers and recovery steps** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/ai-model-rollback.md && sha256sum docs/ai-model-rollback.md
```

- **Expected:** The runbook identifies a compatible previous deployment, triggers and recovery steps
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-18 — Model rollback (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** There is no feasible rollback
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-18 and positive control AZ-T34-17: Model rollback.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate there is no feasible rollback => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-19 — Non-sensitive smoke requests (POSITIVE)

- **Purpose / criterion:** Smoke input uses approved synthetic data and excludes sensitive content
- **Deviation to detect:** Test inputs contain personal or confidential data
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-19 (Step 34: Model deployment and lifecycle), control: Non-sensitive smoke requests.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Smoke input uses approved synthetic data and excludes sensitive content** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
jq -e '.ai.smoke.approved_inputs | length > 0' "$AI_BASELINE"
```

- **Expected:** Smoke input uses approved synthetic data and excludes sensitive content
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-20 — Non-sensitive smoke requests (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Test inputs contain personal or confidential data
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-20 and positive control AZ-T34-19: Non-sensitive smoke requests.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate test inputs contain personal or confidential data => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-21 — Deployment audit (POSITIVE)

- **Purpose / criterion:** Model changes and errors have configured, accessible diagnostic evidence
- **Deviation to detect:** Model changes cannot be audited
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T34-21 (Step 34: Model deployment and lifecycle), control: Deployment audit.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Model changes and errors have configured, accessible diagnostic evidence** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az monitor diagnostic-settings list --resource "$OPENAI_ID" -o json
```

- **Expected:** Model changes and errors have configured, accessible diagnostic evidence
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T34-22 — Deployment audit (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Model changes cannot be audited
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T34-22 and positive control AZ-T34-21: Deployment audit.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate model changes cannot be audited => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T34-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 35 — Azure AI Search security (22 tests)

**Source action:** Configure Azure AI Search with private connectivity, RBAC and reproducible index schema.
**Source provenance:** Runbook v1, Step 35. Preserve exact source IDs `AZ-T35-01` through `AZ-T35-22`.


### AZ-T35-01 — Search service SKU (POSITIVE)

- **Purpose / criterion:** The service SKU supports the approved Private Endpoint design
- **Deviation to detect:** The selected SKU does not support required features
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-01 (Step 35: Azure AI Search security), control: Search service SKU.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The service SKU supports the approved Private Endpoint design** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az search service show -g "$RG" -n "$SEARCH_NAME" --query sku.name -o tsv
```

- **Expected:** The service SKU supports the approved Private Endpoint design
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-02 — Search service SKU (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The selected SKU does not support required features
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-02 and positive control AZ-T35-01: Search service SKU.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the selected sku does not support required features => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-03 — Private Endpoint feature support (POSITIVE)

- **Purpose / criterion:** SKU, region and PE features are verified against the signed design
- **Deviation to detect:** PE support is assumed but unverified
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-03 (Step 35: Azure AI Search security), control: Private Endpoint feature support.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **SKU, region and PE features are verified against the signed design** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az search service show -g "$RG" -n "$SEARCH_NAME" --query "{sku:sku,provisioningState:provisioningState}" -o json
```

- **Expected:** SKU, region and PE features are verified against the signed design
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-04 — Private Endpoint feature support (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** PE support is assumed but unverified
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-04 and positive control AZ-T35-03: Private Endpoint feature support.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate pe support is assumed but unverified => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-05 — Public network access (POSITIVE)

- **Purpose / criterion:** Search publicNetworkAccess equals Disabled
- **Deviation to detect:** Public search data-plane access remains enabled
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-05 (Step 35: Azure AI Search security), control: Public network access.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Search publicNetworkAccess equals Disabled** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az search service show -g "$RG" -n "$SEARCH_NAME" --query publicNetworkAccess -o tsv
```

- **Expected:** Search publicNetworkAccess equals Disabled
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-06 — Public network access (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Public search data-plane access remains enabled
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-06 and positive control AZ-T35-05: Public network access.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate public search data-plane access remains enabled => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-07 — Local authentication (POSITIVE)

- **Purpose / criterion:** Search local/key authentication is disabled when required by policy
- **Deviation to detect:** Unapproved API-key authentication is enabled
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-07 (Step 35: Azure AI Search security), control: Local authentication.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Search local/key authentication is disabled when required by policy** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az search service show -g "$RG" -n "$SEARCH_NAME" --query disableLocalAuth -o tsv
```

- **Expected:** Search local/key authentication is disabled when required by policy
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-08 — Local authentication (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unapproved API-key authentication is enabled
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-08 and positive control AZ-T35-07: Local authentication.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unapproved api-key authentication is enabled => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-09 — Search data-plane RBAC (POSITIVE)

- **Purpose / criterion:** Data-plane roles are constrained to the needed indices and operations
- **Deviation to detect:** Excessive Search RBAC is granted
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-09 (Step 35: Azure AI Search security), control: Search data-plane RBAC.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Data-plane roles are constrained to the needed indices and operations** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az role assignment list --scope "$SEARCH_ID" --all -o json
```

- **Expected:** Data-plane roles are constrained to the needed indices and operations
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-10 — Search data-plane RBAC (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Excessive Search RBAC is granted
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-10 and positive control AZ-T35-09: Search data-plane RBAC.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate excessive search rbac is granted => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-11 — Index schema management (POSITIVE)

- **Purpose / criterion:** Required indices and fields are defined in versioned source and reviewed
- **Deviation to detect:** The index schema is missing or ad hoc
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-11 (Step 35: Azure AI Search security), control: Index schema management.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Required indices and fields are defined in versioned source and reviewed** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/search-index-schema.json && jq -e '.name and .fields' docs/search-index-schema.json
```

- **Expected:** Required indices and fields are defined in versioned source and reviewed
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-12 — Index schema management (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The index schema is missing or ad hoc
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-12 and positive control AZ-T35-11: Index schema management.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the index schema is missing or ad hoc => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-13 — Authorized query smoke (POSITIVE)

- **Purpose / criterion:** An approved internal runner records a successful identity-authenticated query
- **Deviation to detect:** The query-success claim has no authenticated evidence
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-13 (Step 35: Azure AI Search security), control: Authorized query smoke.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **An approved internal runner records a successful identity-authenticated query** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/search/query-smoke.json && jq -e '.status == "Pass" and .resource_id' evidence/search/query-smoke.json
```

- **Expected:** An approved internal runner records a successful identity-authenticated query
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-14 — Authorized query smoke (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The query-success claim has no authenticated evidence
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-14 and positive control AZ-T35-13: Authorized query smoke.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the query-success claim has no authenticated evidence => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-15 — Indexer adoption (POSITIVE)

- **Purpose / criterion:** Required indexers are governed and versioned, or explicitly recorded as not adopted
- **Deviation to detect:** Indexer requirements are unresolved
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-15 (Step 35: Azure AI Search security), control: Indexer adoption.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Required indexers are governed and versioned, or explicitly recorded as not adopted** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/search-indexer-spec.json && jq -e '.name' docs/search-indexer-spec.json
```

- **Expected:** Required indexers are governed and versioned, or explicitly recorded as not adopted
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-16 — Indexer adoption (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Indexer requirements are unresolved
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-16 and positive control AZ-T35-15: Indexer adoption.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate indexer requirements are unresolved => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-17 — Diagnostic settings (POSITIVE)

- **Purpose / criterion:** Search diagnostic logs have the approved destination and categories
- **Deviation to detect:** Search logging is stopped
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-17 (Step 35: Azure AI Search security), control: Diagnostic settings.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Search diagnostic logs have the approved destination and categories** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az monitor diagnostic-settings list --resource "$SEARCH_ID" -o json
```

- **Expected:** Search diagnostic logs have the approved destination and categories
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-18 — Diagnostic settings (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Search logging is stopped
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-18 and positive control AZ-T35-17: Diagnostic settings.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate search logging is stopped => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-19 — Capacity planning (POSITIVE)

- **Purpose / criterion:** Replica/partition counts and utilization meet the signed demand baseline
- **Deviation to detect:** Capacity is inadequate or unreviewed
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-19 (Step 35: Azure AI Search security), control: Capacity planning.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Replica/partition counts and utilization meet the signed demand baseline** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az search service show -g "$RG" -n "$SEARCH_NAME" -o json
```

- **Expected:** Replica/partition counts and utilization meet the signed demand baseline
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-20 — Capacity planning (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Capacity is inadequate or unreviewed
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-20 and positive control AZ-T35-19: Capacity planning.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate capacity is inadequate or unreviewed => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-21 — Terraform drift (POSITIVE)

- **Purpose / criterion:** A reviewed Search plan reveals no unapproved changes
- **Deviation to detect:** Manual configuration drift is present
- **Execution class / priority:** `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T35-21 (Step 35: Azure AI Search security), control: Terraform drift.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **A reviewed Search plan reveals no unapproved changes** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
terraform -chdir=infra plan -refresh-only -detailed-exitcode -no-color
```

- **Expected:** A reviewed Search plan reveals no unapproved changes
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T35-22 — Terraform drift (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Manual configuration drift is present
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T35-22 and positive control AZ-T35-21: Terraform drift.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate manual configuration drift is present => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T35-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 36 — Cosmos DB for NoSQL (22 tests)

**Source action:** Configure Cosmos DB for NoSQL with private access, appropriate backup and identity.
**Source provenance:** Runbook v1, Step 36. Preserve exact source IDs `AZ-T36-01` through `AZ-T36-22`.


### AZ-T36-01 — Cosmos DB NoSQL account (POSITIVE)

- **Purpose / criterion:** Account API/kind matches the approved Cosmos DB for NoSQL design
- **Deviation to detect:** A different Cosmos DB API is configured
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-01 (Step 36: Cosmos DB for NoSQL), control: Cosmos DB NoSQL account.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Account API/kind matches the approved Cosmos DB for NoSQL design** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb show -g "$RG" -n "$COSMOS_NAME" --query kind -o tsv
```

- **Expected:** Account API/kind matches the approved Cosmos DB for NoSQL design
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-02 — Cosmos DB NoSQL account (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A different Cosmos DB API is configured
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-02 and positive control AZ-T36-01: Cosmos DB NoSQL account.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a different cosmos db api is configured => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-03 — Public network access (POSITIVE)

- **Purpose / criterion:** Cosmos DB publicNetworkAccess equals Disabled
- **Deviation to detect:** Public Cosmos DB access is allowed
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-03 (Step 36: Cosmos DB for NoSQL), control: Public network access.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Cosmos DB publicNetworkAccess equals Disabled** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb show -g "$RG" -n "$COSMOS_NAME" --query publicNetworkAccess -o tsv
```

- **Expected:** Cosmos DB publicNetworkAccess equals Disabled
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-04 — Public network access (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Public Cosmos DB access is allowed
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-04 and positive control AZ-T36-03: Public network access.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate public cosmos db access is allowed => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-05 — Account local authentication (POSITIVE)

- **Purpose / criterion:** The verified API/provider property disables unauthorized local/key authentication
- **Deviation to detect:** Account-key authentication remains enabled
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-05 (Step 36: Cosmos DB for NoSQL), control: Account local authentication.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The verified API/provider property disables unauthorized local/key authentication** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb show -g "$RG" -n "$COSMOS_NAME" --query disableLocalAuth -o tsv
```

- **Expected:** The verified API/provider property disables unauthorized local/key authentication
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-06 — Account local authentication (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Account-key authentication remains enabled
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-06 and positive control AZ-T36-05: Account local authentication.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate account-key authentication remains enabled => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-07 — Backup configuration (POSITIVE)

- **Purpose / criterion:** Backup mode and retention satisfy approved RPO and recovery policy
- **Deviation to detect:** Backup configuration is absent or insufficient
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-07 (Step 36: Cosmos DB for NoSQL), control: Backup configuration.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Backup mode and retention satisfy approved RPO and recovery policy** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb show -g "$RG" -n "$COSMOS_NAME" --query backupPolicy -o json
```

- **Expected:** Backup mode and retention satisfy approved RPO and recovery policy
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-08 — Backup configuration (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Backup configuration is absent or insufficient
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-08 and positive control AZ-T36-07: Backup configuration.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate backup configuration is absent or insufficient => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-09 — Consistency model (POSITIVE)

- **Purpose / criterion:** The account consistency policy matches application consistency requirements
- **Deviation to detect:** A conflicting consistency level is configured
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-09 (Step 36: Cosmos DB for NoSQL), control: Consistency model.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The account consistency policy matches application consistency requirements** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb show -g "$RG" -n "$COSMOS_NAME" --query consistencyPolicy -o json
```

- **Expected:** The account consistency policy matches application consistency requirements
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-10 — Consistency model (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A conflicting consistency level is configured
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-10 and positive control AZ-T36-09: Consistency model.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a conflicting consistency level is configured => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-11 — Zone resilience (POSITIVE)

- **Purpose / criterion:** Availability zone and failover settings follow the approved resilience design
- **Deviation to detect:** The agreed resilience policy is not met
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-11 (Step 36: Cosmos DB for NoSQL), control: Zone resilience.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Availability zone and failover settings follow the approved resilience design** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb show -g "$RG" -n "$COSMOS_NAME" --query locations -o json
```

- **Expected:** Availability zone and failover settings follow the approved resilience design
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-12 — Zone resilience (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The agreed resilience policy is not met
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-12 and positive control AZ-T36-11: Zone resilience.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the agreed resilience policy is not met => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-13 — SQL data-plane RBAC (POSITIVE)

- **Purpose / criterion:** Dedicated Cosmos SQL data roles are assigned and verified separately from ARM RBAC
- **Deviation to detect:** ARM-only RBAC is mistakenly treated as Cosmos data access
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-13 (Step 36: Cosmos DB for NoSQL), control: SQL data-plane RBAC.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Dedicated Cosmos SQL data roles are assigned and verified separately from ARM RBAC** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb sql role assignment list -g "$RG" -a "$COSMOS_NAME" -o json
```

- **Expected:** Dedicated Cosmos SQL data roles are assigned and verified separately from ARM RBAC
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-14 — SQL data-plane RBAC (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** ARM-only RBAC is mistakenly treated as Cosmos data access
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-14 and positive control AZ-T36-13: SQL data-plane RBAC.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate arm-only rbac is mistakenly treated as cosmos data access => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-15 — Database scope (POSITIVE)

- **Purpose / criterion:** Database permissions and inventory match documented least privilege
- **Deviation to detect:** Data access is over-broad
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-15 (Step 36: Cosmos DB for NoSQL), control: Database scope.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Database permissions and inventory match documented least privilege** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb sql database list -g "$RG" -a "$COSMOS_NAME" -o json
```

- **Expected:** Database permissions and inventory match documented least privilege
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-16 — Database scope (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Data access is over-broad
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-16 and positive control AZ-T36-15: Database scope.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate data access is over-broad => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-17 — Request diagnostics (POSITIVE)

- **Purpose / criterion:** Request latency, errors and diagnostic routing are captured as designed
- **Deviation to detect:** Required Cosmos telemetry is absent
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-17 (Step 36: Cosmos DB for NoSQL), control: Request diagnostics.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Request latency, errors and diagnostic routing are captured as designed** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az monitor diagnostic-settings list --resource "$COSMOS_ID" -o json
```

- **Expected:** Request latency, errors and diagnostic routing are captured as designed
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-18 — Request diagnostics (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Required Cosmos telemetry is absent
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-18 and positive control AZ-T36-17: Request diagnostics.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate required cosmos telemetry is absent => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-19 — Encryption policy (POSITIVE)

- **Purpose / criterion:** Service-managed keys or CMK match the signed encryption requirement
- **Deviation to detect:** Mandatory customer-managed encryption is missing
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-19 (Step 36: Cosmos DB for NoSQL), control: Encryption policy.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Service-managed keys or CMK match the signed encryption requirement** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb show -g "$RG" -n "$COSMOS_NAME" --query "{keyVaultKeyUri:keyVaultKeyUri,properties:properties}" -o json
```

- **Expected:** Service-managed keys or CMK match the signed encryption requirement
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-20 — Encryption policy (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Mandatory customer-managed encryption is missing
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-20 and positive control AZ-T36-19: Encryption policy.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate mandatory customer-managed encryption is missing => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-21 — Recovery exercise (POSITIVE)

- **Purpose / criterion:** Restoration and failover drills are approved and measurable against RTO/RPO
- **Deviation to detect:** No recovery-test plan exists
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T36-21 (Step 36: Cosmos DB for NoSQL), control: Recovery exercise.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Restoration and failover drills are approved and measurable against RTO/RPO** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/cosmos-dr-test-plan.md && sha256sum docs/cosmos-dr-test-plan.md
```

- **Expected:** Restoration and failover drills are approved and measurable against RTO/RPO
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T36-22 — Recovery exercise (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** No recovery-test plan exists
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T36-22 and positive control AZ-T36-21: Recovery exercise.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate no recovery-test plan exists => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T36-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 37 — Key Vault and certificate custody (22 tests)

**Source action:** Configure Key Vault, Private Endpoint, secret-reader RBAC and certificate rotation.
**Source provenance:** Runbook v1, Step 37. Preserve exact source IDs `AZ-T37-01` through `AZ-T37-22`.


### AZ-T37-01 — Key Vault public access (POSITIVE)

- **Purpose / criterion:** Key Vault publicNetworkAccess equals Disabled
- **Deviation to detect:** The Vault data-plane is publicly enabled
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-01 (Step 37: Key Vault and certificate custody), control: Key Vault public access.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Key Vault publicNetworkAccess equals Disabled** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az keyvault show -g "$RG" -n "$VAULT_NAME" --query properties.publicNetworkAccess -o tsv
```

- **Expected:** Key Vault publicNetworkAccess equals Disabled
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-02 — Key Vault public access (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The Vault data-plane is publicly enabled
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-02 and positive control AZ-T37-01: Key Vault public access.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the vault data-plane is publicly enabled => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-03 — Key Vault Private Endpoint (POSITIVE)

- **Purpose / criterion:** Vault PE exists and targets the correct Vault and subnet
- **Deviation to detect:** Vault private endpoint is missing
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-03 (Step 37: Key Vault and certificate custody), control: Key Vault Private Endpoint.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Vault PE exists and targets the correct Vault and subnet** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint show -g "$RG" -n "$PE_VAULT" -o json
```

- **Expected:** Vault PE exists and targets the correct Vault and subnet
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-04 — Key Vault Private Endpoint (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Vault private endpoint is missing
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-04 and positive control AZ-T37-03: Key Vault Private Endpoint.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate vault private endpoint is missing => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-05 — Vault private DNS (POSITIVE)

- **Purpose / criterion:** The Vault public hostname resolves to the approved PE IP on an internal runner
- **Deviation to detect:** The hostname resolves to a public address
- **Execution class / priority:** `APPROVED_INTERNAL_RUNNER` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-05 (Step 37: Key Vault and certificate custody), control: Vault private DNS.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_INTERNAL_RUNNER` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The Vault public hostname resolves to the approved PE IP on an internal runner** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
dig +short "${VAULT_NAME}.vault.azure.net" A
```

- **Expected:** The Vault public hostname resolves to the approved PE IP on an internal runner
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-06 — Vault private DNS (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The hostname resolves to a public address
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-06 and positive control AZ-T37-05: Vault private DNS.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the hostname resolves to a public address => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-07 — Key Vault RBAC authorization (POSITIVE)

- **Purpose / criterion:** The signed design uses Azure RBAC authorization for the Vault
- **Deviation to detect:** An unapproved access-policy authorization mode is configured
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-07 (Step 37: Key Vault and certificate custody), control: Key Vault RBAC authorization.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The signed design uses Azure RBAC authorization for the Vault** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az keyvault show -g "$RG" -n "$VAULT_NAME" --query properties.enableRbacAuthorization -o tsv
```

- **Expected:** The signed design uses Azure RBAC authorization for the Vault
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-08 — Key Vault RBAC authorization (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** An unapproved access-policy authorization mode is configured
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-08 and positive control AZ-T37-07: Key Vault RBAC authorization.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate an unapproved access-policy authorization mode is configured => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-09 — Secret-reader least privilege (POSITIVE)

- **Purpose / criterion:** Application/Gateway identities have only required scoped secret-read permissions
- **Deviation to detect:** Unnecessary Secrets Officer or administrator rights are granted
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-09 (Step 37: Key Vault and certificate custody), control: Secret-reader least privilege.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Application/Gateway identities have only required scoped secret-read permissions** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az role assignment list --scope "$VAULT_ID" --all -o json
```

- **Expected:** Application/Gateway identities have only required scoped secret-read permissions
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-10 — Secret-reader least privilege (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unnecessary Secrets Officer or administrator rights are granted
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-10 and positive control AZ-T37-09: Secret-reader least privilege.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unnecessary secrets officer or administrator rights are granted => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-11 — TLS certificate expiry (POSITIVE)

- **Purpose / criterion:** Remaining certificate lifetime exceeds the approved renewal threshold
- **Deviation to detect:** Certificate is expired or nearing expiry without action
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-11 (Step 37: Key Vault and certificate custody), control: TLS certificate expiry.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Remaining certificate lifetime exceeds the approved renewal threshold** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az keyvault certificate show --vault-name "$VAULT_NAME" --name "$GW_CERT_NAME" --query attributes.expires -o tsv
```

- **Expected:** Remaining certificate lifetime exceeds the approved renewal threshold
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-12 — TLS certificate expiry (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Certificate is expired or nearing expiry without action
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-12 and positive control AZ-T37-11: TLS certificate expiry.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate certificate is expired or nearing expiry without action => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-13 — Certificate chain and hostname (POSITIVE)

- **Purpose / criterion:** Trusted issuer, hostname and intermediate chain are independently validated
- **Deviation to detect:** TLS trust chain is invalid or incomplete
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-13 (Step 37: Key Vault and certificate custody), control: Certificate chain and hostname.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Trusted issuer, hostname and intermediate chain are independently validated** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/tls/certificate-chain.txt && sha256sum evidence/tls/certificate-chain.txt
```

- **Expected:** Trusted issuer, hostname and intermediate chain are independently validated
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-14 — Certificate chain and hostname (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** TLS trust chain is invalid or incomplete
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-14 and positive control AZ-T37-13: Certificate chain and hostname.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate tls trust chain is invalid or incomplete => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-15 — Versionless certificate secret URI (POSITIVE)

- **Purpose / criterion:** App Gateway references the intended versionless Key Vault secret ID
- **Deviation to detect:** A pinned secret version prevents normal renewal
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-15 (Step 37: Key Vault and certificate custody), control: Versionless certificate secret URI.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **App Gateway references the intended versionless Key Vault secret ID** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/keyvault-cert-reference.md && grep -n "versionless" docs/keyvault-cert-reference.md
```

- **Expected:** App Gateway references the intended versionless Key Vault secret ID
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-16 — Versionless certificate secret URI (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A pinned secret version prevents normal renewal
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-16 and positive control AZ-T37-15: Versionless certificate secret URI.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a pinned secret version prevents normal renewal => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-17 — Rotation ownership (POSITIVE)

- **Purpose / criterion:** Keys and certificates have signed rotation intervals and accountable owners
- **Deviation to detect:** Rotation responsibility or expiration is unknown
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-17 (Step 37: Key Vault and certificate custody), control: Rotation ownership.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Keys and certificates have signed rotation intervals and accountable owners** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az keyvault key list --vault-name "$VAULT_NAME" --query "[].{name:name,enabled:attributes.enabled}" -o json
```

- **Expected:** Keys and certificates have signed rotation intervals and accountable owners
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-18 — Rotation ownership (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Rotation responsibility or expiration is unknown
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-18 and positive control AZ-T37-17: Rotation ownership.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate rotation responsibility or expiration is unknown => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-19 — CMK decision (POSITIVE)

- **Purpose / criterion:** The CMK need, cost and recovery impact are documented and approved
- **Deviation to detect:** Required CMK analysis is absent
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-19 (Step 37: Key Vault and certificate custody), control: CMK decision.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The CMK need, cost and recovery impact are documented and approved** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
jq -e '.encryption.cmk_decision.approved == true' "$SECURITY_BASELINE"
```

- **Expected:** The CMK need, cost and recovery impact are documented and approved
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-20 — CMK decision (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Required CMK analysis is absent
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-20 and positive control AZ-T37-19: CMK decision.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate required cmk analysis is absent => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-21 — Vault audit (POSITIVE)

- **Purpose / criterion:** Vault secret/key accesses are logged in the approved monitoring workspace
- **Deviation to detect:** Security-relevant Vault operations are not audited
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T37-21 (Step 37: Key Vault and certificate custody), control: Vault audit.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Vault secret/key accesses are logged in the approved monitoring workspace** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az monitor diagnostic-settings list --resource "$VAULT_ID" -o json
```

- **Expected:** Vault secret/key accesses are logged in the approved monitoring workspace
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T37-22 — Vault audit (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Security-relevant Vault operations are not audited
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T37-22 and positive control AZ-T37-21: Vault audit.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate security-relevant vault operations are not audited => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T37-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 38 — Data service private endpoints (22 tests)

**Source action:** Connect each AI/data endpoint to the correct Private Link subresource and zone group.
**Source provenance:** Runbook v1, Step 38. Preserve exact source IDs `AZ-T38-01` through `AZ-T38-22`.


### AZ-T38-01 — OpenAI PE group ID (POSITIVE)

- **Purpose / criterion:** OpenAI PE uses groupId account and the intended resource ID
- **Deviation to detect:** OpenAI Private Link subresource is incorrect
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-01 (Step 38: Data service private endpoints), control: OpenAI PE group ID.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **OpenAI PE uses groupId account and the intended resource ID** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint show -g "$RG" -n "$PE_OPENAI" --query privateLinkServiceConnections -o json
```

- **Expected:** OpenAI PE uses groupId account and the intended resource ID
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-02 — OpenAI PE group ID (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** OpenAI Private Link subresource is incorrect
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-02 and positive control AZ-T38-01: OpenAI PE group ID.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate openai private link subresource is incorrect => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-03 — Search PE group ID (POSITIVE)

- **Purpose / criterion:** Search PE uses groupId searchService and the intended resource ID
- **Deviation to detect:** Search PE targets the wrong subresource
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-03 (Step 38: Data service private endpoints), control: Search PE group ID.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Search PE uses groupId searchService and the intended resource ID** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint show -g "$RG" -n "$PE_SEARCH" --query privateLinkServiceConnections -o json
```

- **Expected:** Search PE uses groupId searchService and the intended resource ID
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-04 — Search PE group ID (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Search PE targets the wrong subresource
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-04 and positive control AZ-T38-03: Search PE group ID.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate search pe targets the wrong subresource => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-05 — Cosmos NoSQL PE group ID (POSITIVE)

- **Purpose / criterion:** Cosmos PE uses groupId Sql for the intended NoSQL account
- **Deviation to detect:** Cosmos PE group ID is incorrect
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-05 (Step 38: Data service private endpoints), control: Cosmos NoSQL PE group ID.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Cosmos PE uses groupId Sql for the intended NoSQL account** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint show -g "$RG" -n "$PE_COSMOS" --query privateLinkServiceConnections -o json
```

- **Expected:** Cosmos PE uses groupId Sql for the intended NoSQL account
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-06 — Cosmos NoSQL PE group ID (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Cosmos PE group ID is incorrect
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-06 and positive control AZ-T38-05: Cosmos NoSQL PE group ID.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate cosmos pe group id is incorrect => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-07 — Key Vault PE group ID (POSITIVE)

- **Purpose / criterion:** Vault PE uses groupId vault for the approved Vault
- **Deviation to detect:** Key Vault PE group ID is incorrect
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-07 (Step 38: Data service private endpoints), control: Key Vault PE group ID.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Vault PE uses groupId vault for the approved Vault** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint show -g "$RG" -n "$PE_VAULT" --query privateLinkServiceConnections -o json
```

- **Expected:** Vault PE uses groupId vault for the approved Vault
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-08 — Key Vault PE group ID (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Key Vault PE group ID is incorrect
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-08 and positive control AZ-T38-07: Key Vault PE group ID.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate key vault pe group id is incorrect => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-09 — Connection approval (POSITIVE)

- **Purpose / criterion:** Every required PE connection has Approved state
- **Deviation to detect:** A PE connection is Pending or Rejected
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-09 (Step 38: Data service private endpoints), control: Connection approval.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Every required PE connection has Approved state** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint list -g "$RG" --query "[].{name:name,state:privateLinkServiceConnections[0].privateLinkServiceConnectionState.status}" -o json
```

- **Expected:** Every required PE connection has Approved state
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-10 — Connection approval (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A PE connection is Pending or Rejected
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-10 and positive control AZ-T38-09: Connection approval.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a pe connection is pending or rejected => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-11 — Private DNS zone groups (POSITIVE)

- **Purpose / criterion:** Required PE zone groups reference the correct signed private DNS zones
- **Deviation to detect:** Zone group is absent or wrong
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-11 (Step 38: Data service private endpoints), control: Private DNS zone groups.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Required PE zone groups reference the correct signed private DNS zones** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint dns-zone-group list -g "$RG" --endpoint-name "$PE_OPENAI" -o json
```

- **Expected:** Required PE zone groups reference the correct signed private DNS zones
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-12 — Private DNS zone groups (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Zone group is absent or wrong
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-12 and positive control AZ-T38-11: Private DNS zone groups.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate zone group is absent or wrong => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-13 — Private NIC addresses (POSITIVE)

- **Purpose / criterion:** Each PE NIC address is inside the approved subnet and matches the inventory
- **Deviation to detect:** A PE IP is outside approved ranges
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-13 (Step 38: Data service private endpoints), control: Private NIC addresses.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Each PE NIC address is inside the approved subnet and matches the inventory** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint list -g "$RG" --query "[].{name:name,ip:customDnsConfigs}" -o json
```

- **Expected:** Each PE NIC address is inside the approved subnet and matches the inventory
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-14 — Private NIC addresses (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A PE IP is outside approved ranges
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-14 and positive control AZ-T38-13: Private NIC addresses.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a pe ip is outside approved ranges => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-15 — PE subnet assignment (POSITIVE)

- **Purpose / criterion:** Each PE belongs to its approved isolated network zone
- **Deviation to detect:** A PE is placed in the wrong subnet
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-15 (Step 38: Data service private endpoints), control: PE subnet assignment.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Each PE belongs to its approved isolated network zone** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint show -g "$RG" -n "$PE_OPENAI" --query subnet.id -o tsv
```

- **Expected:** Each PE belongs to its approved isolated network zone
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-16 — PE subnet assignment (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A PE is placed in the wrong subnet
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-16 and positive control AZ-T38-15: PE subnet assignment.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a pe is placed in the wrong subnet => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-17 — PE network policy (POSITIVE)

- **Purpose / criterion:** NSG attachment and Private Endpoint network policies are effective as designed
- **Deviation to detect:** PE traffic policy is absent or ineffective
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-17 (Step 38: Data service private endpoints), control: PE network policy.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **NSG attachment and Private Endpoint network policies are effective as designed** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_PE" --query "{nsg:networkSecurityGroup.id,policies:privateEndpointNetworkPolicies}" -o json
```

- **Expected:** NSG attachment and Private Endpoint network policies are effective as designed
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-18 — PE network policy (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** PE traffic policy is absent or ineffective
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-18 and positive control AZ-T38-17: PE network policy.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate pe traffic policy is absent or ineffective => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-19 — OpenAI private DNS response (POSITIVE)

- **Purpose / criterion:** The normal OpenAI hostname resolves to the approved PE IP internally
- **Deviation to detect:** PE A record is absent or incorrect
- **Execution class / priority:** `APPROVED_INTERNAL_RUNNER` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-19 (Step 38: Data service private endpoints), control: OpenAI private DNS response.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_INTERNAL_RUNNER` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The normal OpenAI hostname resolves to the approved PE IP internally** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
dig +short "${OPENAI_NAME}.openai.azure.com" A
```

- **Expected:** The normal OpenAI hostname resolves to the approved PE IP internally
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-20 — OpenAI private DNS response (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** PE A record is absent or incorrect
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-20 and positive control AZ-T38-19: OpenAI private DNS response.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate pe a record is absent or incorrect => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-21 — PE change provenance (POSITIVE)

- **Purpose / criterion:** PE resource ID, creation record and approval status are captured and reviewed
- **Deviation to detect:** PE changes lack an audit trail
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T38-21 (Step 38: Data service private endpoints), control: PE change provenance.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **PE resource ID, creation record and approval status are captured and reviewed** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint list -g "$RG" -o json
```

- **Expected:** PE resource ID, creation record and approval status are captured and reviewed
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T38-22 — PE change provenance (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** PE changes lack an audit trail
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T38-22 and positive control AZ-T38-21: PE change provenance.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate pe changes lack an audit trail => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T38-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 39 — App Service private ingress (22 tests)

**Source action:** Configure inbound App Service Private Endpoint, SCM DNS and private deployment routing.
**Source provenance:** Runbook v1, Step 39. Preserve exact source IDs `AZ-T39-01` through `AZ-T39-22`.


### AZ-T39-01 — Web App PE group ID (POSITIVE)

- **Purpose / criterion:** App Service PE uses the sites subresource and correct Web App
- **Deviation to detect:** Web App PE does not target sites
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-01 (Step 39: App Service private ingress), control: Web App PE group ID.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **App Service PE uses the sites subresource and correct Web App** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint show -g "$RG" -n "$PE_APP" --query privateLinkServiceConnections -o json
```

- **Expected:** App Service PE uses the sites subresource and correct Web App
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-02 — Web App PE group ID (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Web App PE does not target sites
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-02 and positive control AZ-T39-01: Web App PE group ID.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate web app pe does not target sites => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-03 — App private DNS zone group (POSITIVE)

- **Purpose / criterion:** The PE is associated with privatelink.azurewebsites.net as designed
- **Deviation to detect:** Web App private zone group is absent
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-03 (Step 39: App Service private ingress), control: App private DNS zone group.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The PE is associated with privatelink.azurewebsites.net as designed** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint dns-zone-group list -g "$RG" --endpoint-name "$PE_APP" -o json
```

- **Expected:** The PE is associated with privatelink.azurewebsites.net as designed
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-04 — App private DNS zone group (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Web App private zone group is absent
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-04 and positive control AZ-T39-03: App private DNS zone group.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate web app private zone group is absent => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-05 — SCM A record (POSITIVE)

- **Purpose / criterion:** The normal SCM FQDN resolves to the expected private address from internal DNS
- **Deviation to detect:** SCM A record is missing
- **Execution class / priority:** `APPROVED_INTERNAL_RUNNER` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-05 (Step 39: App Service private ingress), control: SCM A record.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_INTERNAL_RUNNER` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The normal SCM FQDN resolves to the expected private address from internal DNS** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
dig +short "${WEBAPP_NAME}.scm.azurewebsites.net" A
```

- **Expected:** The normal SCM FQDN resolves to the expected private address from internal DNS
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-06 — SCM A record (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** SCM A record is missing
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-06 and positive control AZ-T39-05: SCM A record.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate scm a record is missing => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-07 — App Service application A record (POSITIVE)

- **Purpose / criterion:** The standard application hostname resolves to the expected private address
- **Deviation to detect:** The hostname unexpectedly resolves publicly
- **Execution class / priority:** `APPROVED_INTERNAL_RUNNER` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-07 (Step 39: App Service private ingress), control: App Service application A record.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_INTERNAL_RUNNER` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The standard application hostname resolves to the expected private address** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
dig +short "${WEBAPP_NAME}.azurewebsites.net" A
```

- **Expected:** The standard application hostname resolves to the expected private address
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-08 — App Service application A record (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The hostname unexpectedly resolves publicly
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-08 and positive control AZ-T39-07: App Service application A record.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the hostname unexpectedly resolves publicly => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-09 — Private SCM HTTPS (POSITIVE)

- **Purpose / criterion:** Authorized runner reaches SCM over TLS with valid certificate; authorization is separately evaluated
- **Deviation to detect:** TLS verification fails or TCP 443 cannot connect
- **Execution class / priority:** `APPROVED_INTERNAL_RUNNER` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-09 (Step 39: App Service private ingress), control: Private SCM HTTPS.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_INTERNAL_RUNNER` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Authorized runner reaches SCM over TLS with valid certificate; authorization is separately evaluated** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
curl --noproxy "*" --connect-timeout 5 --max-time 15 -sS -o /dev/null -w "%{http_code} %{remote_ip}\n" "https://${WEBAPP_NAME}.scm.azurewebsites.net/"
```

- **Expected:** Authorized runner reaches SCM over TLS with valid certificate; authorization is separately evaluated
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-10 — Private SCM HTTPS (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** TLS verification fails or TCP 443 cannot connect
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-10 and positive control AZ-T39-09: Private SCM HTTPS.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate tls verification fails or tcp 443 cannot connect => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-11 — Separate ingress/egress subnets (POSITIVE)

- **Purpose / criterion:** App Service inbound PE subnet is distinct from outbound VNet Integration subnet
- **Deviation to detect:** Incoming PE and outbound integration share a prohibited subnet
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-11 (Step 39: App Service private ingress), control: Separate ingress/egress subnets.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **App Service inbound PE subnet is distinct from outbound VNet Integration subnet** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint show -g "$RG" -n "$PE_APP" --query subnet.id -o tsv
```

- **Expected:** App Service inbound PE subnet is distinct from outbound VNet Integration subnet
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-12 — Separate ingress/egress subnets (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Incoming PE and outbound integration share a prohibited subnet
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-12 and positive control AZ-T39-11: Separate ingress/egress subnets.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate incoming pe and outbound integration share a prohibited subnet => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-13 — Private Endpoint NSG (POSITIVE)

- **Purpose / criterion:** The PE subnet policies restrict sources to the approved set
- **Deviation to detect:** Unapproved network sources are allowed
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-13 (Step 39: App Service private ingress), control: Private Endpoint NSG.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The PE subnet policies restrict sources to the approved set** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network vnet subnet show -g "$RG" --vnet-name "$VNET" -n "$SNET_PE" --query "{nsg:networkSecurityGroup.id,policies:privateEndpointNetworkPolicies}" -o json
```

- **Expected:** The PE subnet policies restrict sources to the approved set
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-14 — Private Endpoint NSG (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unapproved network sources are allowed
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-14 and positive control AZ-T39-13: Private Endpoint NSG.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unapproved network sources are allowed => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-15 — App Service public ingress (POSITIVE)

- **Purpose / criterion:** App Service publicNetworkAccess is Disabled
- **Deviation to detect:** Public application ingress is enabled
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-15 (Step 39: App Service private ingress), control: App Service public ingress.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **App Service publicNetworkAccess is Disabled** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az webapp show -g "$RG" -n "$WEBAPP_NAME" --query publicNetworkAccess -o tsv
```

- **Expected:** App Service publicNetworkAccess is Disabled
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-16 — App Service public ingress (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Public application ingress is enabled
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-16 and positive control AZ-T39-15: App Service public ingress.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate public application ingress is enabled => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-17 — Internal health TLS (POSITIVE)

- **Purpose / criterion:** Internal runner validates HTTPS certificate and receives the approved health response
- **Deviation to detect:** Internal TLS/443 health probe fails
- **Execution class / priority:** `APPROVED_INTERNAL_RUNNER` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-17 (Step 39: App Service private ingress), control: Internal health TLS.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_INTERNAL_RUNNER` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Internal runner validates HTTPS certificate and receives the approved health response** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
curl --noproxy "*" --connect-timeout 5 --max-time 15 -sS -o /dev/null -w "%{http_code} %{remote_ip}\n" "https://${WEBAPP_NAME}.azurewebsites.net/healthz"
```

- **Expected:** Internal runner validates HTTPS certificate and receives the approved health response
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-18 — Internal health TLS (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Internal TLS/443 health probe fails
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-18 and positive control AZ-T39-17: Internal health TLS.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate internal tls/443 health probe fails => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-19 — Private deployment path (POSITIVE)

- **Purpose / criterion:** The approved runner deploys through the private SCM path
- **Deviation to detect:** Deployment depends on public SCM access
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-19 (Step 39: App Service private ingress), control: Private deployment path.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The approved runner deploys through the private SCM path** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/deploy/scm-private-path.json && jq -e '.approved == true' evidence/deploy/scm-private-path.json
```

- **Expected:** The approved runner deploys through the private SCM path
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-20 — Private deployment path (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Deployment depends on public SCM access
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-20 and positive control AZ-T39-19: Private deployment path.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate deployment depends on public scm access => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-21 — Web App PE approval (POSITIVE)

- **Purpose / criterion:** The App PE is Approved and linked to the exact Web App resource ID
- **Deviation to detect:** Web App PE is unapproved or mislinked
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T39-21 (Step 39: App Service private ingress), control: Web App PE approval.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The App PE is Approved and linked to the exact Web App resource ID** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint show -g "$RG" -n "$PE_APP" -o json
```

- **Expected:** The App PE is Approved and linked to the exact Web App resource ID
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T39-22 — Web App PE approval (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Web App PE is unapproved or mislinked
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T39-22 and positive control AZ-T39-21: Web App PE approval.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate web app pe is unapproved or mislinked => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T39-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 40 — Private CI and deployment pathway (22 tests)

**Source action:** Establish approved private self-hosted CI/runner and artifact provenance.
**Source provenance:** Runbook v1, Step 40. Preserve exact source IDs `AZ-T40-01` through `AZ-T40-22`.


### AZ-T40-01 — Self-hosted runner placement (POSITIVE)

- **Purpose / criterion:** The runner is attached only to the approved private subnet
- **Deviation to detect:** A public NIC exposes the runner
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-01 (Step 40: Private CI and deployment pathway), control: Self-hosted runner placement.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The runner is attached only to the approved private subnet** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az vm show -g "$RG" -n "$RUNNER_VM" --query "{id:id,networkProfile:networkProfile}" -o json
```

- **Expected:** The runner is attached only to the approved private subnet
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-02 — Self-hosted runner placement (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A public NIC exposes the runner
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-02 and positive control AZ-T40-01: Self-hosted runner placement.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a public nic exposes the runner => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-03 — Private SCM port 443 (POSITIVE)

- **Purpose / criterion:** The authorized runner reaches private SCM with validated TLS, separate from authorization
- **Deviation to detect:** SCM private HTTPS is unreachable
- **Execution class / priority:** `APPROVED_INTERNAL_RUNNER` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-03 (Step 40: Private CI and deployment pathway), control: Private SCM port 443.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_INTERNAL_RUNNER` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The authorized runner reaches private SCM with validated TLS, separate from authorization** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
curl --noproxy "*" --connect-timeout 5 --max-time 15 -sS -o /dev/null -w "%{http_code}\n" "https://${WEBAPP_NAME}.scm.azurewebsites.net/"
```

- **Expected:** The authorized runner reaches private SCM with validated TLS, separate from authorization
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-04 — Private SCM port 443 (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** SCM private HTTPS is unreachable
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-04 and positive control AZ-T40-03: Private SCM port 443.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate scm private https is unreachable => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-05 — ACR Private Endpoint (POSITIVE)

- **Purpose / criterion:** ACR PE is approved if container registry use is adopted
- **Deviation to detect:** Container registry uses only public access despite requiring private access
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-05 (Step 40: Private CI and deployment pathway), control: ACR Private Endpoint.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **ACR PE is approved if container registry use is adopted** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az network private-endpoint show -g "$RG" -n "$PE_ACR" -o json
```

- **Expected:** ACR PE is approved if container registry use is adopted
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-06 — ACR Private Endpoint (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Container registry uses only public access despite requiring private access
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-06 and positive control AZ-T40-05: ACR Private Endpoint.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate container registry uses only public access despite requiring private access => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-07 — Private ACR DNS (POSITIVE)

- **Purpose / criterion:** The approved runner resolves the normal ACR hostname to a private address
- **Deviation to detect:** Registry DNS unexpectedly resolves publicly
- **Execution class / priority:** `APPROVED_INTERNAL_RUNNER` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-07 (Step 40: Private CI and deployment pathway), control: Private ACR DNS.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_INTERNAL_RUNNER` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The approved runner resolves the normal ACR hostname to a private address** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
dig +short "${ACR_NAME}.azurecr.io" A
```

- **Expected:** The approved runner resolves the normal ACR hostname to a private address
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-08 — Private ACR DNS (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Registry DNS unexpectedly resolves publicly
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-08 and positive control AZ-T40-07: Private ACR DNS.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate registry dns unexpectedly resolves publicly => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-09 — Federated CI identity (POSITIVE)

- **Purpose / criterion:** Runner OIDC subject and audience are constrained to approved deployment workflows
- **Deviation to detect:** Long-lived client secrets are used without approval
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-09 (Step 40: Private CI and deployment pathway), control: Federated CI identity.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Runner OIDC subject and audience are constrained to approved deployment workflows** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/runner-oidc.md && sha256sum docs/runner-oidc.md
```

- **Expected:** Runner OIDC subject and audience are constrained to approved deployment workflows
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-10 — Federated CI identity (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Long-lived client secrets are used without approval
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-10 and positive control AZ-T40-09: Federated CI identity.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate long-lived client secrets are used without approval => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-11 — Artifact integrity (POSITIVE)

- **Purpose / criterion:** Artifact digest and source commit SHA match release approval
- **Deviation to detect:** Artifact provenance or integrity is unknown
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-11 (Step 40: Private CI and deployment pathway), control: Artifact integrity.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Artifact digest and source commit SHA match release approval** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/deploy/artifact-provenance.json && jq -e '.digest and .commit' evidence/deploy/artifact-provenance.json
```

- **Expected:** Artifact digest and source commit SHA match release approval
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-12 — Artifact integrity (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Artifact provenance or integrity is unknown
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-12 and positive control AZ-T40-11: Artifact integrity.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate artifact provenance or integrity is unknown => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-13 — Approved ZIP deployment (POSITIVE)

- **Purpose / criterion:** A documented successful ZIP deployment uses the approved private runner
- **Deviation to detect:** Deployment occurs through an unauthorized route
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-13 (Step 40: Private CI and deployment pathway), control: Approved ZIP deployment.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **A documented successful ZIP deployment uses the approved private runner** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/deploy/zip-deploy-result.json && jq -e '.resource_id and .result' evidence/deploy/zip-deploy-result.json
```

- **Expected:** A documented successful ZIP deployment uses the approved private runner
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-14 — Approved ZIP deployment (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Deployment occurs through an unauthorized route
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-14 and positive control AZ-T40-13: Approved ZIP deployment.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate deployment occurs through an unauthorized route => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-15 — CI log sanitization (POSITIVE)

- **Purpose / criterion:** Pipeline logs contain no tokens, keys, credentials or sensitive prompts
- **Deviation to detect:** Secrets or message content leak into logs
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-15 (Step 40: Private CI and deployment pathway), control: CI log sanitization.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Pipeline logs contain no tokens, keys, credentials or sensitive prompts** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/deploy/ci-log-redaction.txt && sha256sum evidence/deploy/ci-log-redaction.txt
```

- **Expected:** Pipeline logs contain no tokens, keys, credentials or sensitive prompts
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-16 — CI log sanitization (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Secrets or message content leak into logs
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-16 and positive control AZ-T40-15: CI log sanitization.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate secrets or message content leak into logs => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-17 — Reproducible build (POSITIVE)

- **Purpose / criterion:** Dependencies are version-locked and the build result is reproducible
- **Deviation to detect:** Dependency versions drift between runs
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-17 (Step 40: Private CI and deployment pathway), control: Reproducible build.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Dependencies are version-locked and the build result is reproducible** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s app/package-lock.json && sha256sum app/package-lock.json
```

- **Expected:** Dependencies are version-locked and the build result is reproducible
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-18 — Reproducible build (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Dependency versions drift between runs
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-18 and positive control AZ-T40-17: Reproducible build.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate dependency versions drift between runs => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-19 — Rollback plan (POSITIVE)

- **Purpose / criterion:** Failed application deployments have a reviewed rollback path
- **Deviation to detect:** No deployment rollback is defined
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-19 (Step 40: Private CI and deployment pathway), control: Rollback plan.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Failed application deployments have a reviewed rollback path** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/deploy-rollback.md && sha256sum docs/deploy-rollback.md
```

- **Expected:** Failed application deployments have a reviewed rollback path
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-20 — Rollback plan (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** No deployment rollback is defined
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-20 and positive control AZ-T40-19: Rollback plan.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate no deployment rollback is defined => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-21 — Deployment audit linkage (POSITIVE)

- **Purpose / criterion:** Commit, actor, approval, timestamp and change record match
- **Deviation to detect:** The deployment event has incomplete provenance
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T40-21 (Step 40: Private CI and deployment pathway), control: Deployment audit linkage.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Commit, actor, approval, timestamp and change record match** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/deploy/change-audit.json && jq -e '.approval and .commit' evidence/deploy/change-audit.json
```

- **Expected:** Commit, actor, approval, timestamp and change record match
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T40-22 — Deployment audit linkage (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The deployment event has incomplete provenance
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T40-22 and positive control AZ-T40-21: Deployment audit linkage.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the deployment event has incomplete provenance => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T40-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 41 — Search Shared Private Link (conditional) (22 tests)

**Source action:** Decide whether Shared Private Link is needed for Search indexers; implement only if adopted.
**Source provenance:** Runbook v1, Step 41. Preserve exact source IDs `AZ-T41-01` through `AZ-T41-22`.


### AZ-T41-01 — Shared Private Link decision (POSITIVE)

- **Purpose / criterion:** The design records whether Search indexers require Shared Private Link
- **Deviation to detect:** Adoption is undecided
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-01 (Step 41: Search Shared Private Link (conditional)), control: Shared Private Link decision.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The design records whether Search indexers require Shared Private Link** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
jq -e '.search.shared_private_link.required | type == "boolean"' "$AI_BASELINE"
```

- **Expected:** The design records whether Search indexers require Shared Private Link
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-02 — Shared Private Link decision (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Adoption is undecided
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-02 and positive control AZ-T41-01: Shared Private Link decision.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate adoption is undecided => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-03 — Data-source inventory (POSITIVE)

- **Purpose / criterion:** All permitted private indexer datasource types are inventoried
- **Deviation to detect:** An unapproved data source is configured
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-03 (Step 41: Search Shared Private Link (conditional)), control: Data-source inventory.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **All permitted private indexer datasource types are inventoried** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/search-datasources.json && jq -e '.datasources' docs/search-datasources.json
```

- **Expected:** All permitted private indexer datasource types are inventoried
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-04 — Data-source inventory (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** An unapproved data source is configured
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-04 and positive control AZ-T41-03: Data-source inventory.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate an unapproved data source is configured => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-05 — Indexer managed identity (POSITIVE)

- **Purpose / criterion:** Indexer identity is approved and constrained to required data access
- **Deviation to detect:** Indexer has no approved identity
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-05 (Step 41: Search Shared Private Link (conditional)), control: Indexer managed identity.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Indexer identity is approved and constrained to required data access** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/search-indexer-identity.json && jq -e '.principal_id' docs/search-indexer-identity.json
```

- **Expected:** Indexer identity is approved and constrained to required data access
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-06 — Indexer managed identity (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Indexer has no approved identity
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-06 and positive control AZ-T41-05: Indexer managed identity.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate indexer has no approved identity => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-07 — Shared link connection approval (POSITIVE)

- **Purpose / criterion:** When adopted, Shared Private Link connection is approved
- **Deviation to detect:** Shared Private Link is awaiting approval
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-07 (Step 41: Search Shared Private Link (conditional)), control: Shared link connection approval.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **When adopted, Shared Private Link connection is approved** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az resource list -g "$RG" --resource-type "Microsoft.Search/searchServices/sharedPrivateLinkResources" -o json
```

- **Expected:** When adopted, Shared Private Link connection is approved
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-08 — Shared link connection approval (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Shared Private Link is awaiting approval
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-08 and positive control AZ-T41-07: Shared link connection approval.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate shared private link is awaiting approval => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-09 — Indexer connection DNS assumptions (POSITIVE)

- **Purpose / criterion:** Indexer private connection setup is checked against actual service requirements
- **Deviation to detect:** Unsupported DNS assumptions are used
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-09 (Step 41: Search Shared Private Link (conditional)), control: Indexer connection DNS assumptions.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Indexer private connection setup is checked against actual service requirements** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/search/indexer-dns.json && jq -e '.resolver and .private_addresses' evidence/search/indexer-dns.json
```

- **Expected:** Indexer private connection setup is checked against actual service requirements
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-10 — Indexer connection DNS assumptions (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unsupported DNS assumptions are used
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-10 and positive control AZ-T41-09: Indexer connection DNS assumptions.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unsupported dns assumptions are used => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-11 — Private indexer route (POSITIVE)

- **Purpose / criterion:** Indexing traffic to private sources follows the approved private connection
- **Deviation to detect:** Indexer falls back to a public path
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-11 (Step 41: Search Shared Private Link (conditional)), control: Private indexer route.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Indexing traffic to private sources follows the approved private connection** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/search/indexer-connectivity.json && jq -e '.approved_route == true' evidence/search/indexer-connectivity.json
```

- **Expected:** Indexing traffic to private sources follows the approved private connection
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-12 — Private indexer route (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Indexer falls back to a public path
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-12 and positive control AZ-T41-11: Private indexer route.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate indexer falls back to a public path => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-13 — Controlled indexer execution (POSITIVE)

- **Purpose / criterion:** A synthetic test indexing job completes under an approved runtime
- **Deviation to detect:** Indexer test execution fails
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-13 (Step 41: Search Shared Private Link (conditional)), control: Controlled indexer execution.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **A synthetic test indexing job completes under an approved runtime** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/search/indexer-execution.json && jq -e '.status == "success"' evidence/search/indexer-execution.json
```

- **Expected:** A synthetic test indexing job completes under an approved runtime
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-14 — Controlled indexer execution (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Indexer test execution fails
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-14 and positive control AZ-T41-13: Controlled indexer execution.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate indexer test execution fails => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-15 — Indexer data-reader rights (POSITIVE)

- **Purpose / criterion:** Indexer permissions use minimal data-reader access to approved source
- **Deviation to detect:** Broad excessive permissions are granted
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-15 (Step 41: Search Shared Private Link (conditional)), control: Indexer data-reader rights.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Indexer permissions use minimal data-reader access to approved source** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az role assignment list --assignee "$INDEXER_PRINCIPAL_ID" --all -o json
```

- **Expected:** Indexer permissions use minimal data-reader access to approved source
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-16 — Indexer data-reader rights (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Broad excessive permissions are granted
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-16 and positive control AZ-T41-15: Indexer data-reader rights.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate broad excessive permissions are granted => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-17 — Unauthorized-source denial (POSITIVE)

- **Purpose / criterion:** Controlled isolated test proves unapproved data cannot be fetched
- **Deviation to detect:** Indexer reads unauthorized data
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-17 (Step 41: Search Shared Private Link (conditional)), control: Unauthorized-source denial.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Controlled isolated test proves unapproved data cannot be fetched** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/search/indexer-denied.json && jq -e '.status == "denied"' evidence/search/indexer-denied.json
```

- **Expected:** Controlled isolated test proves unapproved data cannot be fetched
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-18 — Unauthorized-source denial (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Indexer reads unauthorized data
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-18 and positive control AZ-T41-17: Unauthorized-source denial.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate indexer reads unauthorized data => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-19 — Indexer recovery (POSITIVE)

- **Purpose / criterion:** Indexer retry and reconstruction ordering are documented and reviewed
- **Deviation to detect:** Search reconstruction cannot be performed
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-19 (Step 41: Search Shared Private Link (conditional)), control: Indexer recovery.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Indexer retry and reconstruction ordering are documented and reviewed** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/search-indexer-recovery.md && sha256sum docs/search-indexer-recovery.md
```

- **Expected:** Indexer retry and reconstruction ordering are documented and reviewed
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-20 — Indexer recovery (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Search reconstruction cannot be performed
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-20 and positive control AZ-T41-19: Indexer recovery.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate search reconstruction cannot be performed => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-21 — Shared link evidence (POSITIVE)

- **Purpose / criterion:** Adoption decision, connection and approval records are retained
- **Deviation to detect:** Configuration lacks supporting approval evidence
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T41-21 (Step 41: Search Shared Private Link (conditional)), control: Shared link evidence.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Adoption decision, connection and approval records are retained** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/search/shared-pe-review.json && jq -e '.decision and .reviewer' evidence/search/shared-pe-review.json
```

- **Expected:** Adoption decision, connection and approval records are retained
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T41-22 — Shared link evidence (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Configuration lacks supporting approval evidence
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T41-22 and positive control AZ-T41-21: Shared link evidence.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate configuration lacks supporting approval evidence => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T41-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 42 — Application managed identity (22 tests)

**Source action:** Use Managed Identity and scoped roles for application data-plane access.
**Source provenance:** Runbook v1, Step 42. Preserve exact source IDs `AZ-T42-01` through `AZ-T42-22`.


### AZ-T42-01 — Application managed identity type (POSITIVE)

- **Purpose / criterion:** App managed-identity type and resource ID agree with approved design
- **Deviation to detect:** Configured identity does not match the app
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-01 (Step 42: Application managed identity), control: Application managed identity type.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **App managed-identity type and resource ID agree with approved design** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az identity show -g "$RG" -n "$APP_IDENTITY" --query "{id:id,principalId:principalId,clientId:clientId}" -o json
```

- **Expected:** App managed-identity type and resource ID agree with approved design
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-02 — Application managed identity type (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Configured identity does not match the app
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-02 and positive control AZ-T42-01: Application managed identity type.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate configured identity does not match the app => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-03 — Managed identity principal ID (POSITIVE)

- **Purpose / criterion:** The Principal ID matches the target of each applicable RBAC assignment
- **Deviation to detect:** Role assignment targets a different principal
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-03 (Step 42: Application managed identity), control: Managed identity principal ID.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The Principal ID matches the target of each applicable RBAC assignment** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az identity show -g "$RG" -n "$APP_IDENTITY" --query principalId -o tsv
```

- **Expected:** The Principal ID matches the target of each applicable RBAC assignment
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-04 — Managed identity principal ID (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Role assignment targets a different principal
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-04 and positive control AZ-T42-03: Managed identity principal ID.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate role assignment targets a different principal => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-05 — Azure OpenAI data-plane role (POSITIVE)

- **Purpose / criterion:** Azure OpenAI role grants only the intended inference operations and scope
- **Deviation to detect:** Overly broad OpenAI roles are granted
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-05 (Step 42: Application managed identity), control: Azure OpenAI data-plane role.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Azure OpenAI role grants only the intended inference operations and scope** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az role assignment list --assignee "$APP_PRINCIPAL_ID" --scope "$OPENAI_ID" --all -o json
```

- **Expected:** Azure OpenAI role grants only the intended inference operations and scope
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-06 — Azure OpenAI data-plane role (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Overly broad OpenAI roles are granted
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-06 and positive control AZ-T42-05: Azure OpenAI data-plane role.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate overly broad openai roles are granted => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-07 — Search data-plane role (POSITIVE)

- **Purpose / criterion:** Search Index Data Reader or equivalent is limited to approved actions
- **Deviation to detect:** Search Contributor is assigned without justification
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-07 (Step 42: Application managed identity), control: Search data-plane role.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Search Index Data Reader or equivalent is limited to approved actions** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az role assignment list --assignee "$APP_PRINCIPAL_ID" --scope "$SEARCH_ID" --all -o json
```

- **Expected:** Search Index Data Reader or equivalent is limited to approved actions
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-08 — Search data-plane role (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Search Contributor is assigned without justification
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-08 and positive control AZ-T42-07: Search data-plane role.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate search contributor is assigned without justification => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-09 — Key Vault identity role (POSITIVE)

- **Purpose / criterion:** App Vault permissions cover only required secret operations
- **Deviation to detect:** Vault administrator rights are assigned unnecessarily
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-09 (Step 42: Application managed identity), control: Key Vault identity role.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **App Vault permissions cover only required secret operations** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az role assignment list --assignee "$APP_PRINCIPAL_ID" --scope "$VAULT_ID" --all -o json
```

- **Expected:** App Vault permissions cover only required secret operations
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-10 — Key Vault identity role (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Vault administrator rights are assigned unnecessarily
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-10 and positive control AZ-T42-09: Key Vault identity role.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate vault administrator rights are assigned unnecessarily => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-11 — Role assignment scope (POSITIVE)

- **Purpose / criterion:** Roles use the smallest authorized resource scope
- **Deviation to detect:** Subscription-level Owner/Contributor is granted
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-11 (Step 42: Application managed identity), control: Role assignment scope.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Roles use the smallest authorized resource scope** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az role assignment list --assignee "$APP_PRINCIPAL_ID" --all -o json
```

- **Expected:** Roles use the smallest authorized resource scope
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-12 — Role assignment scope (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Subscription-level Owner/Contributor is granted
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-12 and positive control AZ-T42-11: Role assignment scope.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate subscription-level owner/contributor is granted => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-13 — Secretless application SDK (POSITIVE)

- **Purpose / criterion:** The application uses a managed-identity credential, not embedded API keys
- **Deviation to detect:** API-key credentials remain in app configuration
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-13 (Step 42: Application managed identity), control: Secretless application SDK.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The application uses a managed-identity credential, not embedded API keys** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/app-auth-config.md && grep -n "DefaultAzureCredential\|ManagedIdentityCredential" docs/app-auth-config.md
```

- **Expected:** The application uses a managed-identity credential, not embedded API keys
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-14 — Secretless application SDK (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** API-key credentials remain in app configuration
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-14 and positive control AZ-T42-13: Secretless application SDK.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate api-key credentials remain in app configuration => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-15 — Managed identity token health (POSITIVE)

- **Purpose / criterion:** Approved internal execution reports successful token acquisition without recording token bytes
- **Deviation to detect:** Managed identity token acquisition fails
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-15 (Step 42: Application managed identity), control: Managed identity token health.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Approved internal execution reports successful token acquisition without recording token bytes** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/identity/token-health.json && jq -e '.token_obtained == true' evidence/identity/token-health.json
```

- **Expected:** Approved internal execution reports successful token acquisition without recording token bytes
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-16 — Managed identity token health (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Managed identity token acquisition fails
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-16 and positive control AZ-T42-15: Managed identity token health.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate managed identity token acquisition fails => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-17 — Token disclosure prevention (POSITIVE)

- **Purpose / criterion:** Authentication tokens are not printed or persisted in logs
- **Deviation to detect:** Raw tokens leak to output
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-17 (Step 42: Application managed identity), control: Token disclosure prevention.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Authentication tokens are not printed or persisted in logs** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/identity/sanitization.json && jq -e '.raw_token_logged == false' evidence/identity/sanitization.json
```

- **Expected:** Authentication tokens are not printed or persisted in logs
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-18 — Token disclosure prevention (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Raw tokens leak to output
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-18 and positive control AZ-T42-17: Token disclosure prevention.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate raw tokens leak to output => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-19 — RBAC propagation handling (POSITIVE)

- **Purpose / criterion:** A test verifies role propagation before judging an access failure
- **Deviation to detect:** Propagation delay is misdiagnosed as permanent denial
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-19 (Step 42: Application managed identity), control: RBAC propagation handling.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **A test verifies role propagation before judging an access failure** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/identity/propagation.json && jq -e '.observed_at_utc' evidence/identity/propagation.json
```

- **Expected:** A test verifies role propagation before judging an access failure
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-20 — RBAC propagation handling (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Propagation delay is misdiagnosed as permanent denial
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-20 and positive control AZ-T42-19: RBAC propagation handling.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate propagation delay is misdiagnosed as permanent denial => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-21 — Unauthorized principal denial (POSITIVE)

- **Purpose / criterion:** Isolated unauthorized identity cannot reach protected operations
- **Deviation to detect:** Unexpected identities gain access
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T42-21 (Step 42: Application managed identity), control: Unauthorized principal denial.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Isolated unauthorized identity cannot reach protected operations** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/identity/denied-principal.json && jq -e '.denied == true' evidence/identity/denied-principal.json
```

- **Expected:** Isolated unauthorized identity cannot reach protected operations
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T42-22 — Unauthorized principal denial (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unexpected identities gain access
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T42-22 and positive control AZ-T42-21: Unauthorized principal denial.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unexpected identities gain access => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T42-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 43 — Cosmos SQL data-plane RBAC (22 tests)

**Source action:** Apply native Cosmos SQL data-plane roles independently of ARM control-plane RBAC.
**Source provenance:** Runbook v1, Step 43. Preserve exact source IDs `AZ-T43-01` through `AZ-T43-22`.


### AZ-T43-01 — Cosmos SQL role assignment (POSITIVE)

- **Purpose / criterion:** Native Cosmos SQL role assignments exist for required data operations
- **Deviation to detect:** No Cosmos SQL roles are assigned
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-01 (Step 43: Cosmos SQL data-plane RBAC), control: Cosmos SQL role assignment.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Native Cosmos SQL role assignments exist for required data operations** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb sql role assignment list -g "$RG" -a "$COSMOS_NAME" -o json
```

- **Expected:** Native Cosmos SQL role assignments exist for required data operations
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-02 — Cosmos SQL role assignment (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** No Cosmos SQL roles are assigned
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-02 and positive control AZ-T43-01: Cosmos SQL role assignment.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate no cosmos sql roles are assigned => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-03 — Reader data actions (POSITIVE)

- **Purpose / criterion:** Reader permissions include only intended read operations
- **Deviation to detect:** A reader is unnecessarily granted write rights
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-03 (Step 43: Cosmos SQL data-plane RBAC), control: Reader data actions.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Reader permissions include only intended read operations** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb sql role definition list -g "$RG" -a "$COSMOS_NAME" -o json
```

- **Expected:** Reader permissions include only intended read operations
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-04 — Reader data actions (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A reader is unnecessarily granted write rights
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-04 and positive control AZ-T43-03: Reader data actions.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a reader is unnecessarily granted write rights => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-05 — Contributor data actions (POSITIVE)

- **Purpose / criterion:** Contributor access is justified and limited to required operations
- **Deviation to detect:** Unnecessary writes are authorized
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-05 (Step 43: Cosmos SQL data-plane RBAC), control: Contributor data actions.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Contributor access is justified and limited to required operations** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb sql role definition list -g "$RG" -a "$COSMOS_NAME" -o json
```

- **Expected:** Contributor access is justified and limited to required operations
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-06 — Contributor data actions (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unnecessary writes are authorized
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-06 and positive control AZ-T43-05: Contributor data actions.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unnecessary writes are authorized => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-07 — Database role scope (POSITIVE)

- **Purpose / criterion:** Data-plane assignment is confined to intended databases
- **Deviation to detect:** Unbounded root-account data scope is accepted
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-07 (Step 43: Cosmos SQL data-plane RBAC), control: Database role scope.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Data-plane assignment is confined to intended databases** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb sql role assignment list -g "$RG" -a "$COSMOS_NAME" --query "[].scope" -o json
```

- **Expected:** Data-plane assignment is confined to intended databases
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-08 — Database role scope (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unbounded root-account data scope is accepted
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-08 and positive control AZ-T43-07: Database role scope.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unbounded root-account data scope is accepted => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-09 — Container role scope (POSITIVE)

- **Purpose / criterion:** Permissions apply to only the required containers
- **Deviation to detect:** An identity can read unrelated containers
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-09 (Step 43: Cosmos SQL data-plane RBAC), control: Container role scope.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Permissions apply to only the required containers** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb sql role assignment list -g "$RG" -a "$COSMOS_NAME" --query "[].scope" -o json
```

- **Expected:** Permissions apply to only the required containers
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-10 — Container role scope (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** An identity can read unrelated containers
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-10 and positive control AZ-T43-09: Container role scope.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate an identity can read unrelated containers => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-11 — Cosmos role principal (POSITIVE)

- **Purpose / criterion:** Cosmos role assignment targets the approved app identity principal
- **Deviation to detect:** Role is assigned to an unexpected principal
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-11 (Step 43: Cosmos SQL data-plane RBAC), control: Cosmos role principal.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Cosmos role assignment targets the approved app identity principal** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az cosmosdb sql role assignment list -g "$RG" -a "$COSMOS_NAME" --query "[].principalId" -o json
```

- **Expected:** Cosmos role assignment targets the approved app identity principal
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-12 — Cosmos role principal (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Role is assigned to an unexpected principal
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-12 and positive control AZ-T43-11: Cosmos role principal.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate role is assigned to an unexpected principal => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-13 — Role propagation (POSITIVE)

- **Purpose / criterion:** SDK access is retested after data-plane role propagation
- **Deviation to detect:** Propagation delay is treated as definitive failure
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-13 (Step 43: Cosmos SQL data-plane RBAC), control: Role propagation.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **SDK access is retested after data-plane role propagation** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/cosmos/rbac-propagation.json && jq -e '.observed_at_utc' evidence/cosmos/rbac-propagation.json
```

- **Expected:** SDK access is retested after data-plane role propagation
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-14 — Role propagation (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Propagation delay is treated as definitive failure
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-14 and positive control AZ-T43-13: Role propagation.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate propagation delay is treated as definitive failure => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-15 — Passwordless SDK read (POSITIVE)

- **Purpose / criterion:** Cosmos SDK succeeds using managed identity without account keys
- **Deviation to detect:** Successful test actually depends on keys
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-15 (Step 43: Cosmos SQL data-plane RBAC), control: Passwordless SDK read.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Cosmos SDK succeeds using managed identity without account keys** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/cosmos/sdk-positive.json && jq -e '.auth == "managed_identity" and .result == "Pass"' evidence/cosmos/sdk-positive.json
```

- **Expected:** Cosmos SDK succeeds using managed identity without account keys
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-16 — Passwordless SDK read (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Successful test actually depends on keys
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-16 and positive control AZ-T43-15: Passwordless SDK read.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate successful test actually depends on keys => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-17 — Unauthorized access denial (POSITIVE)

- **Purpose / criterion:** Controlled access to an unapproved container/principal is denied
- **Deviation to detect:** Unauthorized Cosmos reads succeed
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-17 (Step 43: Cosmos SQL data-plane RBAC), control: Unauthorized access denial.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Controlled access to an unapproved container/principal is denied** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/cosmos/sdk-denied.json && jq -e '.result == "Denied"' evidence/cosmos/sdk-denied.json
```

- **Expected:** Controlled access to an unapproved container/principal is denied
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-18 — Unauthorized access denial (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unauthorized Cosmos reads succeed
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-18 and positive control AZ-T43-17: Unauthorized access denial.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unauthorized cosmos reads succeed => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-19 — ARM vs Cosmos data RBAC (POSITIVE)

- **Purpose / criterion:** ARM Contributor does not by itself prove Cosmos SQL data authorization
- **Deviation to detect:** ARM control-plane roles are mistaken for data permissions
- **Execution class / priority:** `APPROVED_OIDC_CI_READ_ONLY` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-19 (Step 43: Cosmos SQL data-plane RBAC), control: ARM vs Cosmos data RBAC.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_OIDC_CI_READ_ONLY` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **ARM Contributor does not by itself prove Cosmos SQL data authorization** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
az role assignment list --assignee "$APP_PRINCIPAL_ID" --all -o json
```

- **Expected:** ARM Contributor does not by itself prove Cosmos SQL data authorization
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-20 — ARM vs Cosmos data RBAC (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** ARM control-plane roles are mistaken for data permissions
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-20 and positive control AZ-T43-19: ARM vs Cosmos data RBAC.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate arm control-plane roles are mistaken for data permissions => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-21 — Cosmos SQL RBAC audit (POSITIVE)

- **Purpose / criterion:** Native Cosmos role change rationale, scope and reviewer are recorded
- **Deviation to detect:** Data-role grants have no review trail
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T43-21 (Step 43: Cosmos SQL data-plane RBAC), control: Cosmos SQL RBAC audit.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Native Cosmos role change rationale, scope and reviewer are recorded** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/cosmos/sql-role-audit.json && jq -e '.reviewer and .scope' evidence/cosmos/sql-role-audit.json
```

- **Expected:** Native Cosmos role change rationale, scope and reviewer are recorded
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T43-22 — Cosmos SQL RBAC audit (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Data-role grants have no review trail
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T43-22 and positive control AZ-T43-21: Cosmos SQL RBAC audit.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate data-role grants have no review trail => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T43-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 44 — Provider schema and IaC validation (22 tests)

**Source action:** Verify installed AzureRM schema, source lint, policy gates and private evidence handling.
**Source provenance:** Runbook v1, Step 44. Preserve exact source IDs `AZ-T44-01` through `AZ-T44-22`.


### AZ-T44-01 — Pinned provider schema (POSITIVE)

- **Purpose / criterion:** Installed AzureRM schema matches the approved lockfile and resource attributes
- **Deviation to detect:** IaC assumes unverified provider attributes
- **Execution class / priority:** `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-01 (Step 44: Provider schema and IaC validation), control: Pinned provider schema.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Installed AzureRM schema matches the approved lockfile and resource attributes** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
terraform -chdir=infra providers schema -json > /dev/null
```

- **Expected:** Installed AzureRM schema matches the approved lockfile and resource attributes
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-02 — Pinned provider schema (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** IaC assumes unverified provider attributes
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-02 and positive control AZ-T44-01: Pinned provider schema.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate iac assumes unverified provider attributes => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-03 — Provider lockfile integrity (POSITIVE)

- **Purpose / criterion:** Provider versions and hashes match approved .terraform.lock.hcl
- **Deviation to detect:** Provider version changes without approval
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-03 (Step 44: Provider schema and IaC validation), control: Provider lockfile integrity.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Provider versions and hashes match approved .terraform.lock.hcl** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s infra/.terraform.lock.hcl && sha256sum infra/.terraform.lock.hcl
```

- **Expected:** Provider versions and hashes match approved .terraform.lock.hcl
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-04 — Provider lockfile integrity (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Provider version changes without approval
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-04 and positive control AZ-T44-03: Provider lockfile integrity.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate provider version changes without approval => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-05 — Terraform formatting (POSITIVE)

- **Purpose / criterion:** terraform fmt check completes successfully on the approved source revision
- **Deviation to detect:** Terraform configuration has format errors
- **Execution class / priority:** `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-05 (Step 44: Provider schema and IaC validation), control: Terraform formatting.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **terraform fmt check completes successfully on the approved source revision** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
terraform fmt -check -recursive -no-color infra
```

- **Expected:** terraform fmt check completes successfully on the approved source revision
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-06 — Terraform formatting (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Terraform configuration has format errors
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-06 and positive control AZ-T44-05: Terraform formatting.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate terraform configuration has format errors => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-07 — Terraform schema validation (POSITIVE)

- **Purpose / criterion:** terraform validate succeeds after approved initialization
- **Deviation to detect:** Unsupported resource attributes remain
- **Execution class / priority:** `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-07 (Step 44: Provider schema and IaC validation), control: Terraform schema validation.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **terraform validate succeeds after approved initialization** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
terraform -chdir=infra validate -no-color
```

- **Expected:** terraform validate succeeds after approved initialization
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-08 — Terraform schema validation (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unsupported resource attributes remain
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-08 and positive control AZ-T44-07: Terraform schema validation.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unsupported resource attributes remain => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-09 — Terraform test isolation (POSITIVE)

- **Purpose / criterion:** terraform test files are reviewed for plan/mock mode and unintended apply risk
- **Deviation to detect:** Unreviewed tests can apply real changes
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-09 (Step 44: Provider schema and IaC validation), control: Terraform test isolation.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **terraform test files are reviewed for plan/mock mode and unintended apply risk** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
find infra/tests -name "*.tftest.hcl" -print
```

- **Expected:** terraform test files are reviewed for plan/mock mode and unintended apply risk
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-10 — Terraform test isolation (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unreviewed tests can apply real changes
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-10 and positive control AZ-T44-09: Terraform test isolation.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unreviewed tests can apply real changes => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-11 — TFLint (POSITIVE)

- **Purpose / criterion:** tflint exits successfully without approved blocker exceptions
- **Deviation to detect:** Lint violations are ignored
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-11 (Step 44: Provider schema and IaC validation), control: TFLint.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **tflint exits successfully without approved blocker exceptions** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
tflint --chdir infra --no-color
```

- **Expected:** tflint exits successfully without approved blocker exceptions
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-12 — TFLint (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Lint violations are ignored
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-12 and positive control AZ-T44-11: TFLint.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate lint violations are ignored => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-13 — Checkov static analysis (POSITIVE)

- **Purpose / criterion:** Checkov finds no unapproved critical public access or RBAC findings
- **Deviation to detect:** Critical policy violations remain
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-13 (Step 44: Provider schema and IaC validation), control: Checkov static analysis.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Checkov finds no unapproved critical public access or RBAC findings** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
checkov -d infra --quiet
```

- **Expected:** Checkov finds no unapproved critical public access or RBAC findings
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-14 — Checkov static analysis (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Critical policy violations remain
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-14 and positive control AZ-T44-13: Checkov static analysis.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate critical policy violations remain => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-15 — OPA/Conftest plan analysis (POSITIVE)

- **Purpose / criterion:** Approved sanitized plan JSON is evaluated by complete policy rules
- **Deviation to detect:** A plan is accepted without policy inspection
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-15 (Step 44: Provider schema and IaC validation), control: OPA/Conftest plan analysis.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Approved sanitized plan JSON is evaluated by complete policy rules** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/plan/approved.tfplan.json && jq -e '.planned_values' evidence/plan/approved.tfplan.json
```

- **Expected:** Approved sanitized plan JSON is evaluated by complete policy rules
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-16 — OPA/Conftest plan analysis (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A plan is accepted without policy inspection
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-16 and positive control AZ-T44-15: OPA/Conftest plan analysis.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a plan is accepted without policy inspection => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-17 — All CI exit codes (POSITIVE)

- **Purpose / criterion:** fmt, validate, test, lint and policy exit codes and artifacts are retained
- **Deviation to detect:** Failed CI tasks are marked successful
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-17 (Step 44: Provider schema and IaC validation), control: All CI exit codes.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **fmt, validate, test, lint and policy exit codes and artifacts are retained** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/ci/phase4-exitcodes.json && jq -e '.jobs' evidence/ci/phase4-exitcodes.json
```

- **Expected:** fmt, validate, test, lint and policy exit codes and artifacts are retained
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-18 — All CI exit codes (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Failed CI tasks are marked successful
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-18 and positive control AZ-T44-17: All CI exit codes.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate failed ci tasks are marked successful => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-19 — Sensitive artifact handling (POSITIVE)

- **Purpose / criterion:** Plan JSON, logs and state remain access-controlled and suitably redacted
- **Deviation to detect:** Sensitive data is published in CI artifacts
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-19 (Step 44: Provider schema and IaC validation), control: Sensitive artifact handling.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Plan JSON, logs and state remain access-controlled and suitably redacted** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s docs/scan-redaction.md && sha256sum docs/scan-redaction.md
```

- **Expected:** Plan JSON, logs and state remain access-controlled and suitably redacted
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-20 — Sensitive artifact handling (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Sensitive data is published in CI artifacts
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-20 and positive control AZ-T44-19: Sensitive artifact handling.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate sensitive data is published in ci artifacts => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-21 — Independent change review (POSITIVE)

- **Purpose / criterion:** Source and policy exceptions receive two-person independent review
- **Deviation to detect:** A single author self-approves
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T44-21 (Step 44: Provider schema and IaC validation), control: Independent change review.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Source and policy exceptions receive two-person independent review** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/approval/phase4-review.json && jq -e '.reviewers | length >= 2' evidence/approval/phase4-review.json
```

- **Expected:** Source and policy exceptions receive two-person independent review
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T44-22 — Independent change review (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** A single author self-approves
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T44-22 and positive control AZ-T44-21: Independent change review.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate a single author self-approves => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T44-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## Step 45 — Saved Terraform plan approval (22 tests)

**Source action:** Review saved Terraform plan hash, source commit, network/RBAC changes and independent approval.
**Source provenance:** Runbook v1, Step 45. Preserve exact source IDs `AZ-T45-01` through `AZ-T45-22`.


### AZ-T45-01 — Saved plan existence (POSITIVE)

- **Purpose / criterion:** The exact saved Terraform plan is produced and protected for review
- **Deviation to detect:** The referenced plan artifact is missing
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-01 (Step 45: Saved Terraform plan approval), control: Saved plan existence.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **The exact saved Terraform plan is produced and protected for review** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s "$APPROVED_PLAN" && sha256sum "$APPROVED_PLAN"
```

- **Expected:** The exact saved Terraform plan is produced and protected for review
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-02 — Saved plan existence (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The referenced plan artifact is missing
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-02 and positive control AZ-T45-01: Saved plan existence.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the referenced plan artifact is missing => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-02 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-03 — Saved plan integrity (POSITIVE)

- **Purpose / criterion:** Plan SHA-256 equals the hash approved by change reviewers
- **Deviation to detect:** Another plan is substituted after approval
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-03 (Step 45: Saved Terraform plan approval), control: Saved plan integrity.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Plan SHA-256 equals the hash approved by change reviewers** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
sha256sum "$APPROVED_PLAN"
```

- **Expected:** Plan SHA-256 equals the hash approved by change reviewers
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-04 — Saved plan integrity (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Another plan is substituted after approval
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-04 and positive control AZ-T45-03: Saved plan integrity.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate another plan is substituted after approval => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-04 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-05 — Source commit integrity (POSITIVE)

- **Purpose / criterion:** Source commit SHA matches the approved plan generation revision
- **Deviation to detect:** The approved plan refers to a different revision
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-05 (Step 45: Saved Terraform plan approval), control: Source commit integrity.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Source commit SHA matches the approved plan generation revision** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
git rev-parse HEAD
```

- **Expected:** Source commit SHA matches the approved plan generation revision
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-06 — Source commit integrity (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** The approved plan refers to a different revision
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-06 and positive control AZ-T45-05: Source commit integrity.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate the approved plan refers to a different revision => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-06 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-07 — Planned action review (POSITIVE)

- **Purpose / criterion:** Creates, updates, deletes and replacements equal the approved change ticket
- **Deviation to detect:** Unexpected destroy/replace appears
- **Execution class / priority:** `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-07 (Step 45: Saved Terraform plan approval), control: Planned action review.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `APPROVED_CI_PLAN_OR_SCHEMA_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Creates, updates, deletes and replacements equal the approved change ticket** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
terraform -chdir=infra show -json "$APPROVED_PLAN" > "$PLAN_JSON_EVIDENCE"
```

- **Expected:** Creates, updates, deletes and replacements equal the approved change ticket
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-08 — Planned action review (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Unexpected destroy/replace appears
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-08 and positive control AZ-T45-07: Planned action review.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate unexpected destroy/replace appears => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-08 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-09 — Unauthorized public IP changes (POSITIVE)

- **Purpose / criterion:** No new or modified public IP exposes the private data-plane
- **Deviation to detect:** An unapproved public IP is provisioned
- **Execution class / priority:** `OFFLINE_APPROVED_PLAN_REVIEW` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-09 (Step 45: Saved Terraform plan approval), control: Unauthorized public IP changes.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `OFFLINE_APPROVED_PLAN_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **No new or modified public IP exposes the private data-plane** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/plan_policy_guard.py --rule public_ip --plan "$PLAN_JSON_EVIDENCE" --scope "$APPROVED_SCOPE_JSON"
```

- **Expected:** No new or modified public IP exposes the private data-plane
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-10 — Unauthorized public IP changes (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** An unapproved public IP is provisioned
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-10 and positive control AZ-T45-09: Unauthorized public IP changes.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate an unapproved public ip is provisioned => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-10 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-11 — PaaS public access changes (POSITIVE)

- **Purpose / criterion:** No selected PaaS resource is changed to enable public data-plane access
- **Deviation to detect:** Public network access is enabled
- **Execution class / priority:** `OFFLINE_APPROVED_PLAN_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-11 (Step 45: Saved Terraform plan approval), control: PaaS public access changes.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `OFFLINE_APPROVED_PLAN_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **No selected PaaS resource is changed to enable public data-plane access** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/plan_policy_guard.py --rule public_access --plan "$PLAN_JSON_EVIDENCE" --scope "$APPROVED_SCOPE_JSON"
```

- **Expected:** No selected PaaS resource is changed to enable public data-plane access
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-12 — PaaS public access changes (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Public network access is enabled
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-12 and positive control AZ-T45-11: PaaS public access changes.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate public network access is enabled => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-12 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-13 — Excessive RBAC changes (POSITIVE)

- **Purpose / criterion:** No newly introduced broad roles violate least-privilege policy
- **Deviation to detect:** Broad Owner or Contributor roles appear
- **Execution class / priority:** `OFFLINE_APPROVED_PLAN_REVIEW` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-13 (Step 45: Saved Terraform plan approval), control: Excessive RBAC changes.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `OFFLINE_APPROVED_PLAN_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **No newly introduced broad roles violate least-privilege policy** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/plan_policy_guard.py --rule rbac --plan "$PLAN_JSON_EVIDENCE" --scope "$APPROVED_SCOPE_JSON"
```

- **Expected:** No newly introduced broad roles violate least-privilege policy
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-14 — Excessive RBAC changes (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Broad Owner or Contributor roles appear
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-14 and positive control AZ-T45-13: Excessive RBAC changes.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate broad owner or contributor roles appear => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-14 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-15 — Diagnostic retention (POSITIVE)

- **Purpose / criterion:** Planned changes do not disable or delete required diagnostic settings
- **Deviation to detect:** Required logging is removed
- **Execution class / priority:** `OFFLINE_APPROVED_PLAN_REVIEW` / P1
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-15 (Step 45: Saved Terraform plan approval), control: Diagnostic retention.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `OFFLINE_APPROVED_PLAN_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Planned changes do not disable or delete required diagnostic settings** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/plan_policy_guard.py --rule diagnostics --plan "$PLAN_JSON_EVIDENCE" --scope "$APPROVED_SCOPE_JSON"
```

- **Expected:** Planned changes do not disable or delete required diagnostic settings
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-16 — Diagnostic retention (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Required logging is removed
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P1
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-16 and positive control AZ-T45-15: Diagnostic retention.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate required logging is removed => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-16 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-17 — Approved cost envelope (POSITIVE)

- **Purpose / criterion:** Estimated AI/Search/Cosmos cost remains within signed budget
- **Deviation to detect:** Cost estimate is missing or unapproved
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P0
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-17 (Step 45: Saved Terraform plan approval), control: Approved cost envelope.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **Estimated AI/Search/Cosmos cost remains within signed budget** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/cost/phase4-estimate.json && jq -e '.approved == true' evidence/cost/phase4-estimate.json
```

- **Expected:** Estimated AI/Search/Cosmos cost remains within signed budget
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-18 — Approved cost envelope (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Cost estimate is missing or unapproved
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P0
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-18 and positive control AZ-T45-17: Approved cost envelope.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate cost estimate is missing or unapproved => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-18 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-19 — Two independent approvals (POSITIVE)

- **Purpose / criterion:** At least two distinct reviewers independent of the execution author approved the exact plan
- **Deviation to detect:** Duplicate/self approvals are accepted
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-19 (Step 45: Saved Terraform plan approval), control: Two independent approvals.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **At least two distinct reviewers independent of the execution author approved the exact plan** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/approval/two-person-review.json && jq -e '.reviewers | unique | length >= 2' evidence/approval/two-person-review.json
```

- **Expected:** At least two distinct reviewers independent of the execution author approved the exact plan
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-20 — Two independent approvals (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** Duplicate/self approvals are accepted
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-20 and positive control AZ-T45-19: Two independent approvals.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate duplicate/self approvals are accepted => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-20 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-21 — Apply evidence provenance (POSITIVE)

- **Purpose / criterion:** If deployment occurs, the execution log is bound to the approved plan and source hash
- **Deviation to detect:** An unapproved plan is applied
- **Execution class / priority:** `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` / P2
- **Prerequisites:** Approved deployment baseline, exact resource or file identity, and immutable source revision; Collector / workspace permissions explicitly scoped to the selected resource; no fixed-terminal az login; Approval for any credentialed CI collection or state-affecting Terraform plan; independent reviewer and UTC evidence path
- **Procedure:**
  1. Confirm source test AZ-T45-21 (Step 45: Saved Terraform plan approval), control: Apply evidence provenance.
  2. Obtain the signed baseline and record the exact asset ID, approved value, expected network zone and source revision.
  3. In `LOCAL_SOURCE_OR_EVIDENCE_REVIEW` only, prepare the required variables and review the command for the pinned CLI/provider/API versions.
  4. Execute or have the approved CI operator execute the command below and retain stdout, stderr, exit code, scope and UTC timestamp.
  5. Evaluate **If deployment occurs, the execution log is bound to the approved plan and source hash** against signed configuration, not merely the command exit code or JSON field existence.
  6. Record sanitized evidence digest, independent reviewer decision, and any approved exception; otherwise mark NOT_READY.
- **Command (proposed; not executed against Azure):**

```bash
test -s evidence/approval/apply-evidence.json && jq -e '.plan_sha256 and .commit_sha and .executor' evidence/approval/apply-evidence.json
```

- **Expected:** If deployment occurs, the execution log is bound to the approved plan and source hash
- **Evidence:** Approved baseline ID, resource ID, pinned tool/source version, scoped observed JSON / DNS / TLS output, UTC, SHA-256 and two-person approval; raw sensitive values stay in protected storage.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


### AZ-T45-22 — Apply evidence provenance (SYNTHETIC_DEVIATION)

- **Purpose / criterion:** Synthetic detector distinguishes allowed / disallowed / missing cases; this is NOT an Azure acceptance test.
- **Deviation to detect:** An unapproved plan is applied
- **Execution class / priority:** `OFFLINE_SYNTHETIC_DETECTOR` / P2
- **Prerequisites:** Python 3 standard library installed; checked-in source specification is available; No Azure credentials; immutable synthetic fixtures and signed rule hash
- **Procedure:**
  1. Locate source test AZ-T45-22 and positive control AZ-T45-21: Apply evidence provenance.
  2. Verify the archived source rule and fixture IDs, then run the offline command below.
  3. Confirm good input => PASS, deliberate an unapproved plan is applied => FAIL, and missing observation => NOT_READY.
  4. Record UTC execution time, source/spec SHA-256, full return code, and synthetic verdict; never promote this to Azure PASS.
- **Command (proposed; not executed against Azure):**

```bash
python3 scripts/phase4_guard.py --selftest AZ-T45-22 --spec specs/phase4_286.json
```

- **Expected:** Good fixture PASS; deliberate deviation FAIL; missing fixture NOT_READY.
- **Evidence:** Synthetic fixture hash, guard version/commit, selftest stdout/exit code and UTC timestamp; separately labeled from Azure evidence.
- **On failure:** NOT_READY if baseline, scope, tool compatibility or required evidence is missing. FAIL only when trusted reviewed evidence contradicts approved policy. Do not apply or modify production.
- **Current live status:** `NOT_READY`; **Azure live passes:** 0.


## End-of-phase acceptance gate

A completed procedure record is not a passed test. Independent acceptance requires real Terraform/application source, approved architecture/baselines, exact Azure resource inventory, read-only CI identity and evidence collection, an independent reviewer, and controlled testing of identity and private network paths. The entire Phase 4 remains **NOT_READY** until these inputs and checks exist.