# Azure Monitor Private Link implementation and verification

Substantive change for construction Step 31. The source audit baseline is main at ed2168fe492261e373f563829c9268b7ac727681. Its local checkout and R10-R1 evidence were retained.

## Sanitized baseline findings

Six canonical catalogues define 1,716 unique test IDs. The previous audit matched literal command references to first-party files under scripts/ and tests/ with Python, shell, JS/TS or PowerShell extensions and checked paths against tracked files at the baseline commit.

- **999 IDs reference an absent script or test file.** Examples include the phase guard scripts and Playwright config/specs.
- **717 IDs have no direct script/test path of the scanned form.** This includes inline system commands, CLI and jq expressions; it is a different category from a missing referenced file.
- **607 IDs also reference a missing literal input file** under specs/, schemas/, fixtures/ or policy/. That count overlaps the categories above.
- The check does not resolve variable-expanded/indirect references, execute catalogue commands, or prove that live target/fixture binding exists. The counts remain a baseline. The new [Step 31 mapping](azure-monitor-step31-mapping.md) explicitly associates checks without changing the 1,716 IDs or claiming that all other missing references are resolved.

## Local verification

| Check | Observed result |
|---|---|
| Package validator and Python offline suite | PASS, 344 tests including 18 new Monitor tests. |
| Formatting of the changed HCL, monitoring module and mock fixture | PASS using Terraform 1.9.8. |
| Both root `init -backend=false -input=false -lockfile=readonly` and `validate` | PASS using Terraform 1.9.8 and AzureRM 4.66.0. Initial registry installation reported HashiCorp-signed provider. Existing deprecation warnings remain for bootstrap storage resource_manager_id and Application Gateway enable_http2. |
| Mocked Terraform Monitor configuration | PASS, 6 of 6. Disabled, dev and Hub configurations plus rejection of non-isolated DNS, incomplete Hub imports and too-small PE subnet. |
| Live entry point without opt-in | Expected NOT_READY and exit 2; tests assert no live calls. |
| Azure acceptance | **0/1,716**, independent signatures **0**, release **NO_GO**. |

R10-R1 already established original-directory R9 integrity on its fixed source. No R10-R1 rerun was needed. The newly changed source has separate Terraform/Python checks above. The 22 Step 31 rows are mapped. Six have a guarded runtime observation path, five have separate manual or runtime work, and eleven have offline checks.

## Remaining work

- Choose the approved target topology and DNS owner and provide reviewed subnet/endpoint and OIDC inputs. Live Monitor DNS/TLS/REST, log arrival and query remain NOT_RUN. Any separate agent/DCE ingestion, App Insights binding, effective RBAC, public exception completeness and operational alert delivery still need evidence.
- Azure real plan/apply, Private Runner hosted CI, provider/platform readiness for the target environment, and independent review remain outstanding. This change adds a local workflow candidate only.
- REST23 ZIP supply remains NOT_READY; full REST11 858-case CI is NOT_RUN. Existing `validate_catalogue.py` dependency and broader Terraform/REST/Playwright coverage gaps remain.
