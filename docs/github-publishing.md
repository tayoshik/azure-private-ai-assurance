# GitHub Publication Procedure — Public Repository

**Destination:** https://github.com/tayoshik/azure-private-ai-assurance

The owner explicitly chose **public visibility** on 2026-11-14. Public means all committed files and history are visible to anyone. A public repository does not imply an open-source license; none is granted in this baseline.

## Publication controls

1. Inspect every file for credentials, subscription and tenant IDs, customer data, internal hostnames, Terraform state, private keys, and raw logs.
2. Exclude original Japanese source archives, unreviewed asset inventories, screenshots, proof-of-access tokens, and material with unresolved publication rights.
3. Run `python3 scripts/validate_package.py` and `python3 -m unittest discover -s tests -v` prior to publication.
4. Publish only approved documentation and offline tooling; preserve frozen IDs and historical evidence boundaries.
5. Verify the GitHub visibility, committed paths, commit SHA and CI status after push. Branch protection and code review are recommended.

## Manual verification

```bash
git clone https://github.com/tayoshik/azure-private-ai-assurance.git
cd azure-private-ai-assurance
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
```

Never publish production Terraform plans, .tfstate, .env or cloud credentials. No Azure deployment is authorized by repository publication.
