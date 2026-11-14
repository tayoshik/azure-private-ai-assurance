# Terraform Stage 3 — I01/I02/I03 identities / private Key Vault

**Source implemented / offline only; `terraform validate`, `plan`, `apply` and real Azure acceptance NOT_EXECUTED.**

Baseline: Stage 1 bootstrap + Stage 2 network/NSGs, plus two user-assigned identities, one PNA-disabled RBAC Key Vault and a PE/zone group. No secret values or certificates in Terraform state. Role grants and the Key Vault/PE approval gates default false.

See `docs/terraform-stage3-i01-i03-operator.md` for fully worked offline commands, authorized CI read-only observation examples, evidence and troubleshooting.

```bash
python3 scripts/check_terraform_stage1.py
python3 scripts/check_terraform_n04.py
python3 scripts/check_terraform_i01_i03.py
python3 -m unittest discover -s tests -p 'test_terraform*.py' -v
```

Provisional azurerm=4.66.0 must be confirmed in provider mirror and by `terraform validate` on an approved runner. All 1,716 real acceptance tests are NOT_READY. Release remains NO-GO.
