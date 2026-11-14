# Phase 3 — Source Preservation and Command Review

**Readiness:** design documentation only. All 264 cases are `NOT_READY` for Azure acceptance.

**Legacy source SHA-256:** `66d389a459bd0abc6ce930a1995e6d1328b087c3532849957f2bc458f7336c14`

## Source-level corrections
Four source commands were edited only to repair quoting/newline syntax; originals and corrected values are preserved in the spec:

### AZ-T21-13 — fixed jq quoting in source

Source:
```bash
jq -e ".reserved | type == "array"" "$IPAM_JSON"
```
Corrected:
```bash
jq -e '.reserved | type == "array"' "$IPAM_JSON"
```

### AZ-T29-19 — repaired linefeed in curl format string

Source:
```bash
curl --noproxy "*" --max-time 10 -sS -o /dev/null -w "%{http_code}
" "https://${APP_PRIVATE_FQDN}/healthz"
```
Corrected:
```bash
curl --noproxy "*" --max-time 10 -sS -o /dev/null -w '%{http_code}\n' "https://${APP_PRIVATE_FQDN}/healthz"
```

### AZ-T31-01 — fixed jq quoting in source

Source:
```bash
jq -e ".monitor.ampls.required | type == "boolean"" "$MONITOR_BASELINE"
```
Corrected:
```bash
jq -e '.monitor.ampls.required | type == "boolean"' "$MONITOR_BASELINE"
```

### AZ-T31-19 — fixed jq quoting in source

Source:
```bash
jq -e ".monitor.public_access_exceptions | type == "array"" "$MONITOR_BASELINE"
```
Corrected:
```bash
jq -e '.monitor.public_access_exceptions | type == "array"' "$MONITOR_BASELINE"
```

## Review gaps (no false green)

The command may successfully return data yet fail to establish the security property. See the individual `command_review_note` fields. Examples:
- `az policy assignment list` cannot alone prove Deny effect, compliance, correct scope, or absence of exemptions.
- `jq ... | length > 0` cannot prove CIDR non-overlap or complete inventory.
- `az monitor activity-log list` is not a substitute for VNet Flow Logs or firewall-deny evidence.
- `dig +short` returns a name/address but must be compared with the signed private endpoint NIC IP and resolver context.
- `terraform plan -refresh-only` can affect state locks or local caches and must be approved separately.
- Synthetic equality checks with words such as `approved` are illustrative and cannot establish production compliance.

## Traceability and non-claims
IDs `AZ-T21-01` to `AZ-T32-22` are maintained, exactly 22 per step.
No tenant/subscription/environment identifiers have been supplied. No Azure resource or network test was executed.
The specified regional service features and CLI commands must be verified against the pinned environment at execution time.
No legal/compliance certification is claimed.
