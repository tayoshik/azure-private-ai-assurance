# Phase 4 Source Review and Command Correction Register

Source archive: `Azure_閉域AI基盤_試験設計_第4段階_20261110.zip`. SHA-256 of source specification: `b221babf4a1b7a17763723d06229e868b943748cbbf6c1b0726e8f07465fcf36`.

- Tests: 286; 143 positive/source-observation, 143 synthetic-negative; live passes: 0.
- Corrections made and preserved: 41. All changes listed below are proposals, not evidence of Azure CLI execution.
- `terraform plan -refresh-only` requires an approved runner and may access/lock remote state; never run as an unapproved offline check.
- Stage 45 JSON existence checks were not effective PNA/IP/RBAC/diagnostics assertions; a new conservative plan guard checks known risky changes while leaving final acceptance for human review.
- Source `test -s` and simple `jq -e` checks remain preflight only; file existence or a single boolean is not evidence authenticity.

## Exact edits

### AZ-T34-13

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
jq -e ".ai.data_residency.approved == true" "$AI_BASELINE"
```
After:
```bash
jq -e '.ai.data_residency.approved == true' "$AI_BASELINE"
```


### AZ-T34-15

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
jq -e ".ai.model_update.approval_id | type == "string"" "$AI_BASELINE"
```
After:
```bash
jq -e '.ai.model_update.approval_id | type == "string"' "$AI_BASELINE"
```


### AZ-T34-19

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
jq -e ".ai.smoke.approved_inputs | length > 0" "$AI_BASELINE"
```
After:
```bash
jq -e '.ai.smoke.approved_inputs | length > 0' "$AI_BASELINE"
```


### AZ-T35-11

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s docs/search-index-schema.json && jq -e ".name and .fields" docs/search-index-schema.json
```
After:
```bash
test -s docs/search-index-schema.json && jq -e '.name and .fields' docs/search-index-schema.json
```


### AZ-T35-13

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/search/query-smoke.json && jq -e ".status == "Pass" and .resource_id" evidence/search/query-smoke.json
```
After:
```bash
test -s evidence/search/query-smoke.json && jq -e '.status == "Pass" and .resource_id' evidence/search/query-smoke.json
```


### AZ-T35-15

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s docs/search-indexer-spec.json && jq -e ".name" docs/search-indexer-spec.json
```
After:
```bash
test -s docs/search-indexer-spec.json && jq -e '.name' docs/search-indexer-spec.json
```


### AZ-T37-19

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
jq -e ".encryption.cmk_decision.approved == true" "$SECURITY_BASELINE"
```
After:
```bash
jq -e '.encryption.cmk_decision.approved == true' "$SECURITY_BASELINE"
```


### AZ-T39-19

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/deploy/scm-private-path.json && jq -e ".approved == true" evidence/deploy/scm-private-path.json
```
After:
```bash
test -s evidence/deploy/scm-private-path.json && jq -e '.approved == true' evidence/deploy/scm-private-path.json
```


### AZ-T40-11

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/deploy/artifact-provenance.json && jq -e ".digest and .commit" evidence/deploy/artifact-provenance.json
```
After:
```bash
test -s evidence/deploy/artifact-provenance.json && jq -e '.digest and .commit' evidence/deploy/artifact-provenance.json
```


### AZ-T40-13

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/deploy/zip-deploy-result.json && jq -e ".resource_id and .result" evidence/deploy/zip-deploy-result.json
```
After:
```bash
test -s evidence/deploy/zip-deploy-result.json && jq -e '.resource_id and .result' evidence/deploy/zip-deploy-result.json
```


### AZ-T40-21

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/deploy/change-audit.json && jq -e ".approval and .commit" evidence/deploy/change-audit.json
```
After:
```bash
test -s evidence/deploy/change-audit.json && jq -e '.approval and .commit' evidence/deploy/change-audit.json
```


### AZ-T41-01

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
jq -e ".search.shared_private_link.required | type == "boolean"" "$AI_BASELINE"
```
After:
```bash
jq -e '.search.shared_private_link.required | type == "boolean"' "$AI_BASELINE"
```


### AZ-T41-03

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s docs/search-datasources.json && jq -e ".datasources" docs/search-datasources.json
```
After:
```bash
test -s docs/search-datasources.json && jq -e '.datasources' docs/search-datasources.json
```


### AZ-T41-05

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s docs/search-indexer-identity.json && jq -e ".principal_id" docs/search-indexer-identity.json
```
After:
```bash
test -s docs/search-indexer-identity.json && jq -e '.principal_id' docs/search-indexer-identity.json
```


### AZ-T41-09

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/search/indexer-dns.json && jq -e ".resolver and .private_addresses" evidence/search/indexer-dns.json
```
After:
```bash
test -s evidence/search/indexer-dns.json && jq -e '.resolver and .private_addresses' evidence/search/indexer-dns.json
```


### AZ-T41-11

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/search/indexer-connectivity.json && jq -e ".approved_route == true" evidence/search/indexer-connectivity.json
```
After:
```bash
test -s evidence/search/indexer-connectivity.json && jq -e '.approved_route == true' evidence/search/indexer-connectivity.json
```


### AZ-T41-13

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/search/indexer-execution.json && jq -e ".status == "success"" evidence/search/indexer-execution.json
```
After:
```bash
test -s evidence/search/indexer-execution.json && jq -e '.status == "success"' evidence/search/indexer-execution.json
```


### AZ-T41-17

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/search/indexer-denied.json && jq -e ".status == "denied"" evidence/search/indexer-denied.json
```
After:
```bash
test -s evidence/search/indexer-denied.json && jq -e '.status == "denied"' evidence/search/indexer-denied.json
```


### AZ-T41-21

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/search/shared-pe-review.json && jq -e ".decision and .reviewer" evidence/search/shared-pe-review.json
```
After:
```bash
test -s evidence/search/shared-pe-review.json && jq -e '.decision and .reviewer' evidence/search/shared-pe-review.json
```


### AZ-T42-15

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/identity/token-health.json && jq -e ".token_obtained == true" evidence/identity/token-health.json
```
After:
```bash
test -s evidence/identity/token-health.json && jq -e '.token_obtained == true' evidence/identity/token-health.json
```


### AZ-T42-17

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/identity/sanitization.json && jq -e ".raw_token_logged == false" evidence/identity/sanitization.json
```
After:
```bash
test -s evidence/identity/sanitization.json && jq -e '.raw_token_logged == false' evidence/identity/sanitization.json
```


### AZ-T42-19

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/identity/propagation.json && jq -e ".observed_at_utc" evidence/identity/propagation.json
```
After:
```bash
test -s evidence/identity/propagation.json && jq -e '.observed_at_utc' evidence/identity/propagation.json
```


### AZ-T42-21

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/identity/denied-principal.json && jq -e ".denied == true" evidence/identity/denied-principal.json
```
After:
```bash
test -s evidence/identity/denied-principal.json && jq -e '.denied == true' evidence/identity/denied-principal.json
```


### AZ-T43-13

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/cosmos/rbac-propagation.json && jq -e ".observed_at_utc" evidence/cosmos/rbac-propagation.json
```
After:
```bash
test -s evidence/cosmos/rbac-propagation.json && jq -e '.observed_at_utc' evidence/cosmos/rbac-propagation.json
```


### AZ-T43-15

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/cosmos/sdk-positive.json && jq -e ".auth == "managed_identity" and .result == "Pass"" evidence/cosmos/sdk-positive.json
```
After:
```bash
test -s evidence/cosmos/sdk-positive.json && jq -e '.auth == "managed_identity" and .result == "Pass"' evidence/cosmos/sdk-positive.json
```


### AZ-T43-17

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/cosmos/sdk-denied.json && jq -e ".result == "Denied"" evidence/cosmos/sdk-denied.json
```
After:
```bash
test -s evidence/cosmos/sdk-denied.json && jq -e '.result == "Denied"' evidence/cosmos/sdk-denied.json
```


### AZ-T43-21

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/cosmos/sql-role-audit.json && jq -e ".reviewer and .scope" evidence/cosmos/sql-role-audit.json
```
After:
```bash
test -s evidence/cosmos/sql-role-audit.json && jq -e '.reviewer and .scope' evidence/cosmos/sql-role-audit.json
```


### AZ-T44-15

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/plan/approved.tfplan.json && jq -e ".planned_values" evidence/plan/approved.tfplan.json
```
After:
```bash
test -s evidence/plan/approved.tfplan.json && jq -e '.planned_values' evidence/plan/approved.tfplan.json
```


### AZ-T44-17

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/ci/phase4-exitcodes.json && jq -e ".jobs" evidence/ci/phase4-exitcodes.json
```
After:
```bash
test -s evidence/ci/phase4-exitcodes.json && jq -e '.jobs' evidence/ci/phase4-exitcodes.json
```


### AZ-T44-21

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/approval/phase4-review.json && jq -e ".reviewers | length >= 2" evidence/approval/phase4-review.json
```
After:
```bash
test -s evidence/approval/phase4-review.json && jq -e '.reviewers | length >= 2' evidence/approval/phase4-review.json
```


### AZ-T45-09

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
jq -e ".resource_changes" "$PLAN_JSON_EVIDENCE"
```
After:
```bash
jq -e '.resource_changes' "$PLAN_JSON_EVIDENCE"
```


### AZ-T45-09

Reason: Existence of resource_changes does not prove policy compliance; scoped conservative checker yields REVIEW_REQUIRED/FAIL/NOT_READY.

Before:
```bash
jq -e ".resource_changes" "$PLAN_JSON_EVIDENCE"
```
After:
```bash
python3 scripts/plan_policy_guard.py --rule public_ip --plan "$PLAN_JSON_EVIDENCE" --scope "$APPROVED_SCOPE_JSON"
```


### AZ-T45-11

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
jq -e ".resource_changes" "$PLAN_JSON_EVIDENCE"
```
After:
```bash
jq -e '.resource_changes' "$PLAN_JSON_EVIDENCE"
```


### AZ-T45-11

Reason: Existence of resource_changes does not prove policy compliance; scoped conservative checker yields REVIEW_REQUIRED/FAIL/NOT_READY.

Before:
```bash
jq -e ".resource_changes" "$PLAN_JSON_EVIDENCE"
```
After:
```bash
python3 scripts/plan_policy_guard.py --rule public_access --plan "$PLAN_JSON_EVIDENCE" --scope "$APPROVED_SCOPE_JSON"
```


### AZ-T45-13

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
jq -e ".resource_changes" "$PLAN_JSON_EVIDENCE"
```
After:
```bash
jq -e '.resource_changes' "$PLAN_JSON_EVIDENCE"
```


### AZ-T45-13

Reason: Existence of resource_changes does not prove policy compliance; scoped conservative checker yields REVIEW_REQUIRED/FAIL/NOT_READY.

Before:
```bash
jq -e ".resource_changes" "$PLAN_JSON_EVIDENCE"
```
After:
```bash
python3 scripts/plan_policy_guard.py --rule rbac --plan "$PLAN_JSON_EVIDENCE" --scope "$APPROVED_SCOPE_JSON"
```


### AZ-T45-15

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
jq -e ".resource_changes" "$PLAN_JSON_EVIDENCE"
```
After:
```bash
jq -e '.resource_changes' "$PLAN_JSON_EVIDENCE"
```


### AZ-T45-15

Reason: Existence of resource_changes does not prove policy compliance; scoped conservative checker yields REVIEW_REQUIRED/FAIL/NOT_READY.

Before:
```bash
jq -e ".resource_changes" "$PLAN_JSON_EVIDENCE"
```
After:
```bash
python3 scripts/plan_policy_guard.py --rule diagnostics --plan "$PLAN_JSON_EVIDENCE" --scope "$APPROVED_SCOPE_JSON"
```


### AZ-T45-17

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/cost/phase4-estimate.json && jq -e ".approved == true" evidence/cost/phase4-estimate.json
```
After:
```bash
test -s evidence/cost/phase4-estimate.json && jq -e '.approved == true' evidence/cost/phase4-estimate.json
```


### AZ-T45-19

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/approval/two-person-review.json && jq -e ".reviewers | unique | length >= 2" evidence/approval/two-person-review.json
```
After:
```bash
test -s evidence/approval/two-person-review.json && jq -e '.reviewers | unique | length >= 2' evidence/approval/two-person-review.json
```


### AZ-T45-21

Reason: Corrected jq filter quoting; original result could misparse JSON string literals.

Before:
```bash
test -s evidence/approval/apply-evidence.json && jq -e ".plan_sha256 and .commit_sha and .executor" evidence/approval/apply-evidence.json
```
After:
```bash
test -s evidence/approval/apply-evidence.json && jq -e '.plan_sha256 and .commit_sha and .executor' evidence/approval/apply-evidence.json
```
