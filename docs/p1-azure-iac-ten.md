# Azure IaC evidence comparison for ten P1 cases

The coverage denominator comes from the source-grounded triage queue (127 P1 cases). The original acceptance criteria come from `specs/phase4_286_en.json`, Git blob `b10e821492df155c48a1c411117512e15fe49113`. The command strings in that catalogue are preserved.

| ID | Compared evidence |
| --- | --- |
| AZ-T40-15 | Pipeline/run/policy and sanitized report digest. All approved artifacts must be covered for tokens, keys, credentials and sensitive prompts, with positive controls and zero unredacted findings. |
| AZ-T40-21 | Deployment, commit, actor, approval, change record, reviewer and timestamps. The approval must precede or coincide with deployment and the reviewer must differ from the actor. |
| AZ-T41-13 | Indexer, source, target, principal, runtime, run and synthetic fixture. The run must finish successfully with the expected document total and zero failed documents. |
| AZ-T41-17 | Indexer, unauthorized source, principal, isolated runtime, run and fixture. The operation must return an authorization denial (403) with zero documents fetched. |
| AZ-T41-21 | Shared connection, target, group, adoption decision, approval and independent reviewer. Adoption expects an approved connection. Declining expects an absent connection and a retained decision record. |
| AZ-T42-15 | Managed identity, tenant, audience, internal runtime and request. Evidence is limited to acquisition status and sanitized metadata. |
| AZ-T42-19 | Principal, role, assignment, scope and operation. The initial attempt, confirmed propagation and successful retest must occur in sequence within the approved window. |
| AZ-T43-13 | The propagation sequence plus Cosmos account/container, SDK use, native data-plane role and keyless access. |
| AZ-T43-21 | Native Cosmos role change with account, principal, assignment, operation, scope, rationale, change record and independent reviewer. |
| AZ-T44-15 | Approved sanitized Terraform JSON digest, policy revision and exact resource operation inventory. Each operation, including both legs of replacement, is evaluated by the repository's public-IP, public-access, RBAC and diagnostics rules. |

Run the CLI with sanitized, local JSON inputs.

```sh
python3 scripts/review_p1_azure_iac.py --case-id AZ-T41-13 \
  --observation observation.json --approved approved.json
```

The observation has `metadata` and `observation` objects. The baseline has `metadata` and `expected` objects. Both metadata objects carry the same `case_id`, `resource_id`, `runner_id` and `source_sha256`. Observation metadata carries `observed_at_utc`. Baseline metadata carries `observation_sha256` over the complete observation document and `approval_record_sha256` over the baseline with that digest field omitted. The plan's `plan_sha256` covers the embedded plan object. All these content digests use SHA-256 over sorted-key, compact JSON with ASCII escapes and no non-finite values. The synthetic input builders in `tests/test_p1_azure_iac.py` show the expected payloads for each case and how to calculate the digests.

Both input documents and all claimed approvals are unsigned. Someone able to modify both files can recompute their digests. Log scans, token handling, effective access and runtime identity still require independent provenance. The plan check covers the four implemented rules on the supplied resource changes. Unknown after-values and change sections such as output changes, drift, deferred changes or invoked actions require separate review. The offline check cannot establish the full external OPA/Conftest policy scope or the completeness of the supplied plan.

Missing or unsupported evidence yields `NOT_READY`. Discrepancies yield `DIFFERENCE_REVIEW_REQUIRED`. Matching inputs yield `REVIEW_REQUIRED`. The CLI returns 2 for all three results and keeps Azure acceptance at zero and the release at `NO_GO`.
