# Azure Private AI Assurance

> **Status:** Documentation and offline test-tooling baseline; **not** a deployed or Azure-validated production system. **Release decision: NO-GO** (missing implementation, approved environment, and live evidence).

Azure Private AI Assurance is an evidence-driven design and verification project for an Azure-hosted, private-data-plane AI web application. It aims to combine a private-only Application Gateway WAF_v2 frontend, App Service Private Endpoint, outbound VNet integration, Azure OpenAI, Azure AI Search, Azure Cosmos DB, Private DNS, managed identities, monitored access, and reviewable infrastructure-as-code.

The project originated in a 78-step Japanese-language construction runbook and an associated 1,716-ID verification catalogue. This repository is the **English publication workspace**, not a claim of successful deployment or compliance certification.

## Objectives

1. Define an auditable private data-plane architecture and its scope, including necessary identity, management, and monitoring dependencies.
2. Bring approved Terraform and application source into a reviewable, versioned Git workflow once actually supplied.
3. Map the **78 construction steps** to **1,716 test IDs** without silently changing identifiers.
4. Separate offline synthetic checks, source review, Azure read-only observations, controlled non-production tests, and acceptance decisions.
5. Retain integrity-protected, scope-bound evidence for independent review and a defensible Go/No-Go outcome.

## What has been demonstrated

| Measure | Verified record | Interpretation |
|---|---:|---|
| Construction steps documented | 78 | Runbook design, **not deployment** |
| Test IDs with draft procedures | 1,716 | Test design, **not live tests passed** |
| Positive / deviation-detection cases | 858 / 858 | The second group largely exercises synthetic detector fixtures |
| Stage 9 synthetic outcomes | 330 / 330 | 110 checks x good / bad / missing fixtures |
| Stage 10 offline unit tests | 18 / 18 | Evidence-gate tooling |
| Stage 11 offline unit tests | 21 / 21 | Source and asset inventory tooling |
| Azure live test passes | **0** | No accepted live evidence |
| Accepted live test cases | **0 / 1,716** | All `NOT_READY` |
| Officially closed critical P0 findings | **0** | Independent closure remains pending |

**Last source-report checkpoint:** 2026-11-13. Values come from saved source reports and are not refreshed against Azure or GitHub by this repository. See [Current status](docs/current-status.md) and [source provenance](docs/source-provenance.md).

## Intended architecture

```text
Corporate clients -- ExpressRoute / approved VPN --> Azure VNet
  --> Private-only Application Gateway WAF_v2 (HTTPS)
  --> App Service Private Endpoint --> App Service
                                      | VNet Integration (outbound)
                                      +--> Private Endpoint: Azure OpenAI
                                      +--> Private Endpoint: Azure AI Search
                                      +--> Private Endpoint: Cosmos DB

Private DNS / Managed Identity / Key Vault / Azure Monitor
Approved CI runner --> Federated identity --> Azure control plane / remote state
```

**Private does not mean zero public dependencies:** identity, control plane, certificate revocation, security feeds, and other explicitly authorized service endpoints may remain required. Threat modelling and sign-off must enumerate those connections.

## Repository layout

- `docs/` — English report, architecture baseline, acceptance criteria, 10-turn roadmap, publishing instructions and source provenance.
- `schemas/` — machine-readable project status and test-plan allocation metadata.
- `scripts/` — offline package checks (no Azure authentication and no mutations).
- `tests/` — offline self-tests.
- `.github/workflows/` — read-only CI validation; no Azure credentials.

## Local verification (no credentials required)

```bash
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
```

No `terraform apply`, Azure login, WAF traffic, load testing, or deployment occurs in this first milestone.

## Next steps

Follow the [10-turn roadmap](docs/ten-turn-roadmap.md). Translation of the 1,716 detailed test procedures, software implementation review, and subsequent GitHub publication milestones are future work. For provenance and safety, the original Japanese ZIP/XLSX inputs are **not** copied into this initial repository. Do not publish raw traces, customer data, subscription identifiers or secrets without a security review.

## Publication and reuse

Repository visibility: **public**, as explicitly selected by the owner on 2026-11-14. Publication requires a confirmed GitHub destination, write permission and review of the data classification. **No license is granted by default:** a license and its scope must be selected by the rights holder before open-source redistribution.

For permitted vulnerability disclosures, see [SECURITY.md](SECURITY.md). For publication instructions, see [GitHub publishing](docs/github-publishing.md).