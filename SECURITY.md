# Security Policy

## Scope

This repository contains documentation, offline checks, and illustrative architecture. It is **not** an endorsed hardened deployment template and should not be deployed directly without an organization-specific security review.

## Sensitive data

Do not submit secrets, private keys, identity tokens, actual tenant/subscription identifiers, internal hostnames, unredacted logs, customer records, or production Terraform state. When disclosing a vulnerability, use an approved private reporting channel rather than a public issue. No public security-response address has been designated in this draft.

## Safe testing

Azure reads require an explicitly approved scope and read-only role. WAF, denial, load, NSG mutation and disaster-recovery experiments require a designated non-production environment and separate authorization. This repository's Stage 1 verification does not connect to Azure.