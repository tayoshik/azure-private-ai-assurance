# Contributing

This repository is an English documentation and offline verification workstream. Proposed changes should reference a tracked document or original test ID, describe whether the change is editorial or substantive, and include evidence for changed expected results.

- Preserve existing `AZ-T##-##` identifiers (78 steps x 22 cases).
- Do not mark a test `PASS` without approved source, scope, actual evidence and review.
- Keep synthetic fixtures separately labeled and out of operational evidence.
- Do not introduce secrets, customer identities, real environment IDs or unapproved network targets.
- Use pull requests and independent review for test, security and IaC changes.
- Re-run `python3 scripts/validate_package.py` and offline unit tests before review.