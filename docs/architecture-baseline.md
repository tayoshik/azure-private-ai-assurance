# Azure Private AI Architecture — Design Baseline

This is a **target design**, not evidence of an existing production deployment.

## Business data plane

```text
Corporate client -- ExpressRoute / approved VPN --> Azure VNet
  --> Private-only Application Gateway (WAF_v2, HTTPS)
  --> App Service Private Endpoint --> App Service
                                      | Outbound VNet Integration
                                      +--> PE: Azure OpenAI
                                      +--> PE: Azure AI Search
                                      +--> PE: Azure Cosmos DB
Private DNS / Managed Identity / Key Vault / Monitor / approved internal runner
```

App Service VNet integration enables outbound routing; it does not make inbound traffic private. Public network access for applicable PaaS data planes is intended to be disabled, with private endpoints and scoped authorization. DNS must resolve normal service hostnames to private addresses from permitted networks.

## Other planes and dependencies

A private application ingress path does not eliminate Microsoft Entra ID, ARM, certificate revocation, updates, monitoring or other necessary public dependencies. Document approved routing, network policies, access constraints, and audit evidence separately.

## Testable invariants

- No unapproved public ingress; private Application Gateway configuration must match the supported deployment mode and its networking requirements.
- App Service ingress PE and outbound integration are independent and verified.
- Correct Private DNS zones, records, VNet links and resolution from internal test runners.
- Managed identities and least-privilege data-plane roles allow authorized access and reject unauthorized access.
- TLS/SNI/backend health, WAF Detection-to-Prevention transition, and logging are validated with actual evidence.
- State backend, change approvals, recovery/rebuild, and drift checks are reproducible.

Provider attributes, service limits, deployment regions and product configurations must be checked at execution time. **No Azure resource has yet passed live acceptance.**
