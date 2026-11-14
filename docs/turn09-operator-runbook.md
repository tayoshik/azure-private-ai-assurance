# Turn 09 — Operator Commands and Troubleshooting

All commands below are **offline**, run from a local trusted WSL2 clone. They are examples to execute locally; they were not executed against Azure.

## 1. Confirm repository / pinned commit

```bash
set -Eeuo pipefail
REPO="$HOME/azure-private-ai-assurance"
if [[ ! -d "$REPO/.git" ]]; then
  git clone https://github.com/tayoshik/azure-private-ai-assurance.git "$REPO"
fi
cd "$REPO"
git rev-parse HEAD
git status --short
python3 --version
openssl version
```

A local clone is not proof of a particular published revision. Record the exact commit SHA, expected source-manifest SHA-256, and the release review.

## 2. Validate the 1,716-case mapping

```bash
python3 scripts/validate_catalogue.py --root .
python3 scripts/turn09_audit.py --root . --report /tmp/turn09_audit.json
python3 -m json.tool /tmp/turn09_audit.json > /dev/null
```

Verify the output has `test_cases: 1716`, `synthetic_detector_cases: 858`, `azure_live_passes: 0`, and `release_decision: NO_GO`. The auditor intentionally prints three project-test blockers rather than inventing passing E2E tests.

## 3. Run repeatable detector exercises

```bash
bash scripts/turn09_offline_regression.sh
python3 -m unittest discover -s tests -p 'test_turn08.py' -v
python3 -m unittest discover -s tests -p 'test_turn09.py' -v
```

**What is verified:** local fixture classification, catalogue consistency, hash tamper rejection, exclusion of synthetic controls from live credit, and explicit NO-GO. **What is not verified:** Private DNS and routing, TLS/backend correctness, Entra authentication, Azure resource properties, WAF behavior, Azure Monitor telemetry, or actual recovery.

## 4. Reconcile internal code dependencies

```bash
python3 scripts/turn09_audit.py --root . --strict-source
# Should return 2 until actual tests/package-lock.json, tests/playwright.config.ts,
# and tests/phase6/phase6.spec.ts are provided by the implementation owner.
```

Do not create a fake package-lock or mock tests to make this pass. The example `tests/phase6/playwright.config.ts.example` is instructional, **not executable E2E coverage**.

## 5. Source acquisition before non-production acceptance

Ask the implementation owner for the reviewed Git commit/PR, Terraform providers and lock file, approved region and resource IDs, private DNS/VNet reachability, app auth code, Playwright tests and lockfile, sanitized read-only observation outputs, independent baseline and trusted signer pin. Confirm security classification and that any provided material may be handled outside the enterprise environment. Keep raw protected material **out of public GitHub**.

## 6. Failure responses

| Symptom | Expected operator response |
|---|---|
| Catalogue SHA-256 mismatch | Stop, inspect source revision and manifest, do not rehash automatically |
| `NOT_READY`/missing project test file | Request approved actual project source, not synthetic replacement |
| Playwright login/session test unavailable | Keep `AZ-T64-05`, `AZ-T64-15` unaccepted |
| Bash syntax passes, cloud flag unknown | Validate against pinned tool version in approved CI after source review |
| Offline fixture PASS but no signed observation | Keep Azure live result `NOT_READY` |
| Signature mismatch / untrusted key | Isolate questionable artifact, re-obtain independent trust pin |
| CI starts requesting Azure credentials | Stop; offline workflow must not request them |
| Release gate prints `NO_GO` | Expected status while evidence is missing; never bypass |

## 7. Escalation trigger and required human input

No human operations are needed for this **Turn 09** English publication QA. For Turn 10, the final published commit and project handoff are prepared offline. To *start Azure implementation verification after Turn 10*, obtain non-production environment owner, source repository/commit, exact approved resource inventory, enterprise CI execution route, and explicit test authorization.