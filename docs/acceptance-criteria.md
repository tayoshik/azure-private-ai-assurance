# Acceptance Criteria and Release Gates

The primary distinction is between *documented*, *synthetically tested*, *observed*, and *independently accepted* controls. No synthetic result constitutes a successful Azure acceptance test.

## Execution classes

1. DESIGN_REVIEW — signed architecture and requirements reviews.
2. OFFLINE_DETECTOR — local synthetic fixtures and unit tests.
3. SOURCE_REVIEW_REQUIRED — actual Terraform/application/CI source mapped to a commit.
4. CI_STATIC_OR_EVIDENCE — controlled static analysis or read-only output review.
5. LIVE_READONLY_CANDIDATE — authorized Azure state inventory without mutation.
6. LIVE_NONPROD_APPROVAL — controlled nonproduction dynamic tests requiring explicit approval.

## Required evidence for each test ID

Record the immutable test ID, applicable target, approved baseline, environment and scope, commit SHA, execution command, timestamp, operator, raw sanitized output, evidence SHA-256, independent reviewer, and disposition PASS / FAIL / NOT_READY / REVIEW_REQUIRED. Unavailable evidence MUST produce NOT_READY, not PASS.

## Release criteria

Critical/P0 findings closed; private ingress and data-plane network isolation measured; TLS/WAF/managed-identity/RBAC/DNS/logging verified with live evidence; drift and remote state approved; recovery objectives tested; accountable owners approve release.

**Current decision: NO-GO.** All 1,716 test IDs are NOT_READY for live acceptance.
