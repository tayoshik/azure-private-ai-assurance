# Terraform Stage 5 — W01-W05 Source Checkpoint
Source modules created: Linux Service Plan, hardened Linux Web App, inline outbound VNet integration, separate inbound sites Private Endpoint, Private DNS zone group, and nonsecret AI endpoint app settings. Existing 43 HCL files retained; nine new files added. HCL compact multiattribute blocks inherited from Stage 4 normalized to multiline in the dev root.

**Local source ZIP:** 91/91 Python unit/mutation tests PASS, including 22 new W01–W05 checks. These are OFFLINE TEXT CONTRACTS only. Terraform fmt/init/validate/plan/apply NOT executed; Azure live PASS=0, release NO-GO. Python 3.11 is an illustrative runtime pending real app source review.

Read [Stage 5 detailed runbook](terraform-stage5-w01-w05-operator.md).
