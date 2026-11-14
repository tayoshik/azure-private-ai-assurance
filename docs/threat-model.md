# Threat Model — Private Azure AI Web Platform

**Turn 02 baseline (2026-11-14) · Scope: proposed, not deployed · Findings are design hypotheses, not verified vulnerabilities.**

## Security objectives and assumptions

Protect prompt/response data and client identifiers; prevent unauthorized external ingress; preserve confidentiality of secrets and state; enforce least-privilege data-plane access; ensure evidence integrity, recoverability and controlled changes. Trust must be explicitly assigned across corporate endpoints, approved private network, App Gateway, PaaS management/control plane, outbound application connectivity, CI/workload identities and evidence stores.

The threat model applies to a single-region web+AI design and does not claim to cover all financial/medical regulatory controls. A customer-managed private network does not eliminate Azure-managed service dependencies.

## Trust boundaries

1. **TB-01: Off-network → approved corporate path → private gateway**: identity, transport and public-exposure boundary.
2. **TB-02: Gateway → App Service inbound PE**: internal DNS, TLS/SNI, PE subnet/NSG and WAF bypass boundary.
3. **TB-03: App Service outbound VNet integration → AI/data services**: private route and data-plane RBAC boundary.
4. **TB-04: App/CI identities → Entra/ARM/Key Vault**: token lifetime, scope, privileged change boundary.
5. **TB-05: Developer/CI → remote state and repository**: secret exfiltration and supply-chain boundary.
6. **TB-06: Application/diagnostics → Log Analytics/evidence**: sensitive payload leakage, tampering and evidentiary provenance.
7. **TB-07: Backup/recovery facilities → resumed application**: restore integrity and recovery-time boundary.

## STRIDE-based threat register (proposed controls)

| ID | Category | Attack / failure hypothesis | Primary mitigations | Verification steps and evidence | Unresolved assumption |
|---|---|---|---|---|---|
| TM-01 | Spoofing | Compromised user connects via allowed corporate network | Entra/application auth, device access, explicit access policy | 2, 64, 66; successful/denied sign-in pair | Real auth method absent |
| TM-02 | Tampering | Unreviewed change opens public gateway / enables PNA | Azure Policy, plan review, protected branch, two-person approval | 22, 45, 52, 59, 74, 76; plan audit | No live policy assignment evidence |
| TM-03 | Repudiation | Change cannot be attributed to identity/commit | OIDC CI run, PIM, signed evidence, immutable change record | 15, 45, 58, 77; provenance trace | Approval chain not provided |
| TM-04 | Disclosure | App Service exposed via default endpoint | PNA disabled; inbound PE and test from unapproved source | 39, 47, 62; resource state plus observation | Target not deployed |
| TM-05 | Disclosure | PE DNS misroutes service calls to public endpoint | Canonical FQDN, linked zones, forwarding, NIC equality check | 27, 30, 48, 61; full resolution chain | DNS authorities not provided |
| TM-06 | Spoofing | Backend host mismatch or rogue TLS endpoint | Trusted backend TLS, expected SNI/Host, rotated cert | 53–55; TLS + health | Certificate/host not known |
| TM-07 | Disclosure | Unauthorized subnet bypasses WAF to PE | PE network policies, NSG/ASG, app identity/auth | 26, 56, 72; allowed/denied network paths | Effective NSG unverified |
| TM-08 | Elevation of privilege | Managed identity can read all Search/Cosmos data | Per-index/collection data roles and separation of identities | 42, 43, 65, 66; paired data operations | App principal absent |
| TM-09 | Tampering | Terraform state overwritten or lost | Entra/OIDC, protected Blob state, versioning, lease lock | 11–15, 68; audit/recovery rehearsal | Backend nonexistent/not supplied |
| TM-10 | Disclosure | Pipeline commits token, client secret or tfplan | Secret scanning, minimal CI logs, Git ignore and history scans | 10, 16, 76; redacted scan output | Public repository hygiene only partially proven |
| TM-11 | Denial of service | WAF rule tuning causes false positive for valid traffic | Detection tuning, narrow exclusions, positive control samples | 51, 69, 70; correlated WAF logs | No live WAF policy |
| TM-12 | Denial of service | Abusive prompts cause quota exhaustion or cost spike | Rate caps, model limits, monitoring, budget alerts | 4, 34, 57, 73; SLO/cost events | Model quota unknown |
| TM-13 | Disclosure | Prompts/responses/PII leak through diagnostics or traces | Data minimization, masking, retention and access scopes | 5, 32, 57, 71; redacted example | Data classification unsigned |
| TM-14 | Tampering | Fake evidence produces erroneous PASS | Hash/signature, approved source identity, baseline binding, independent reviewer | 17, 63, 75–78; evidence validator/approval | Live provenance unverified |
| TM-15 | Denial of service | Failed recovery or Search index cannot be rebuilt | Backup drills, preserved input data, reindex reproducibility | 68, 73, 77; restoration output | RTO/RPO not approved |
| TM-16 | Elevation of privilege | Runner with plan role silently performs apply | Split identities, explicit approval, workflow gates | 7, 16, 45, 58, 76; denied apply in non-authorized role | CI connection not supplied |
| TM-17 | Disclosure | Egress to arbitrary public endpoints bypasses governance | Scoped outbound rules, firewall, approved Entra/Monitor deps | 29, 56, 67; flow tests | Dependency allowlist not fixed |
| TM-18 | Repudiation | A 403 or timeout is presented as proof of closure | Require target existence, config, path and correlated telemetry | 17, 18, 62, 63, 70; multi-source evidence | Azure observations absent |

## Attack-path walk-throughs

**Path A — public ingress regression.** A new gateway frontend or PaaS public-network setting is introduced in a Terraform plan. Before apply, policy over plan JSON must reject the change. After approval, an independent control-plane inventory must corroborate the absence of public exposure. An external client timing out or receiving 403 cannot independently establish safety.

**Path B — bypassing the gateway.** A party on a peered VNet attempts direct access to App Service PE. NSG/network policy denies unapproved sources; application authorization also denies invalid tokens. App Service access restrictions are not a substitute for PE-level boundaries.

**Path C — stolen application identity.** A compromised workload token tries to query unrelated indexes/collections. The token's audience and narrowly scoped Search/Cosmos data roles limit the blast radius. Isolation claims require real approved/denied calls and audit evidence.

**Path D — poisoned audit evidence.** An attacker injects a synthetic `PASS` JSON or edits timestamps. The verifier refuses unapproved scope/identity, hashes and signatures or absent independent review. Repository-stored synthetic fixtures may demonstrate detector behavior but never confer Azure acceptance.

**Path E — leaked raw plan or logs via public GitHub.** CI writes `tfplan`, state, private resource IDs/tokens or prompt text to the repo. CI must prohibit these file classes, scan prior history, avoid unreviewed raw artifacts and rotate exposed credentials. This repository publishes only sanitized baseline instructions and checker source.

## Risk disposition and acceptance protocol

- Threat model **status:** DRAFT; no organization-signed likelihood/impact or residual risk score exists.
- For each threat: assign business owner, scenario, preventive control, detective control, test ID, evidence URI/digest, result, residual risk decision and review date. Never invent these fields.
- P0/critical unknowns require `NOT_READY` or `NO-GO`; a proposed mitigation does not close a finding. Negative tests that would modify production RBAC, NSG, WAF or user sessions must be executed only in approved disposable staging.
- Separately examine data residency, Prompt Injection / RAG data access, content filtering, misuse monitoring, retention, data exfiltration and privacy obligations after actual app/retrieval design becomes available. Those claims cannot be fully assessed from the infrastructure-only baseline.

## References

- [Detailed architecture](architecture-detailed.md)
- [78-step runbook](78-step-construction-runbook.md)
- [Acceptance criteria](acceptance-criteria.md)
- [Command recipes](command-recipes.md)