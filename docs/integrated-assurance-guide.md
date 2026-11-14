# Turn 08: Integrated Offline Assurance, Evidence Integrity, and CI Gates

**Status (2026-11-14): Design and offline tooling only. Azure live PASS: 0. Release: NO-GO.**

## 1. Objective and trustworthy boundaries

Create a reproducible, inspectable English test index for **78 steps / 1,716 IDs** and block false claims of deployment verification. Six source test catalogues are referenced by SHA-256. Of 1,716 cases, 858 are configuration/evidence reviews and **858 are synthetic deviation-detector checks**. They are not 1,716 independent Azure live validations. `AZ-T74-01` is specifically classified as `OFFLINE_POLICY_REVIEW` following the Turn 07 correction.

Implementation code, approved infrastructure configuration, and accepted live Azure observations were **not supplied**. All cases begin in `NOT_READY`. A `PASS` from the catalogue or fixture regression below is **offline test tooling PASS only**.

## 2. Repository layout

```text
specs/
  english_tests_001_440.json       # Turn03 source
  phase3_264_en.json              # Turn04 source, English-only derivative
  phase4_286_en.json              # Turn05 source, English-only derivative
  phase5_286_en.json              # Turn06 source
  phase6_220_en.json              # Turn07 source
  phase7_220_en.json              # Turn07 source
  catalogue_index_1716.json       # NEW: 6 file digests, 1,716 ID rows
schemas/evidence-record.schema.json
scripts/validate_catalogue.py
scripts/evidence_gate.py
scripts/release_gate.py
tests/test_turn08.py
.github/workflows/turn08-offline-integrity.yml
```

The `source_sha256` fields capture the retained original local source byte digests. The `sha256` fields pin the English catalogues **as published**. The index hashes must be updated *only through a reviewed, explicit regeneration* if any source content changes. Directly editing the index to make a modified source appear valid defeats its design; independent code review and branch protection must enforce the required workflow.

## 3. WSL2 commands — no Azure login

```bash
set -Eeuo pipefail
REPO="${HOME}/azure-private-ai-assurance"
# One-time checkout; use the existing clone when available
if [[ ! -d "$REPO/.git" ]]; then
  git clone https://github.com/tayoshik/azure-private-ai-assurance.git "$REPO"
fi
cd "$REPO"
git fetch --prune origin
git log -1 --format='%H %cI %s'
python3 --version
openssl version
python3 scripts/validate_catalogue.py --root .
python3 -m unittest discover -s tests -p 'test_turn08.py' -v
python3 scripts/release_gate.py --root .
```

**Expected:** catalogue command exits 0 with `PASS: 78 steps, 1,716...`; tests exit 0; release gate prints `NO_GO` and `live_passes: 0`. Do **not** treat `NO_GO` as a test failure: it is the **intended current release decision**. If the repository is offline, use an organization-approved, checksum-verified source archive rather than silently substituting stale files. `git fetch` requires network access; when restricted, omit it only with a documented pinned commit.

### Command checks

```bash
# Parse and compile the new Python tools; neither command accesses Azure
python3 -m py_compile scripts/validate_catalogue.py scripts/evidence_gate.py scripts/release_gate.py
# Verify all six referenced specs and index without modifying them
python3 scripts/validate_catalogue.py --root .
# List the failed checks without automatically fixing baseline data
python3 scripts/validate_catalogue.py --root . || echo 'NOT_READY: investigate version/hash/ID mismatch'
```

When a checker reports `NOT_READY`, examine the exact source path and `source SHA-256` against signed change records; never bypass it with `--force` or upload regenerated summaries without review.

## 4. Evidence envelope, approved scope, and cryptography

The evidence verifier operates on **real signed collection artifacts** in a protected evidence workspace, not on repository test fixtures. Use a trusted CI identity, a private key held in an approved signing service, an independently pinned public key, and an **out-of-band approved scope**. No keys or raw resource exports are committed to this public repository.

Required files in the authorized evidence root:
- `record.json`: typed metadata with canonical test ID, UTC time, subscription and resource IDs, collector and runner, non-production authorization ticket, raw observation and baseline hashes, and explicit `synthetic=false`.
- `record.sig`: detached **Ed25519** signature over the exact bytes of `record.json`, produced by the authorized signer.
- `observation.json`: sanitized actual data, whose SHA-256 matches the signed envelope.
- `baseline.json`: approved baseline, byte-identical to the version pinned by independent scope authority.

Outside that root, supply the approved `scope.json` (approved ID, ticket, runner and collector allowlists, required baseline digest), the organization's trusted public key and the public-key SHA-256 **from a separately controlled trust distribution channel**. `scope.json` is not itself authenticated by this tool; the organization **must** independently verify its authorization and integrity (e.g., protected artifact / signed configuration) before providing it. If this cannot be done, the result is `NOT_READY`, regardless of the local tool result.

```bash
# Run only on an authorized evidence-review runner. Do not paste real IDs/logs into chat.
set -Eeuo pipefail
: "${EVIDENCE_ROOT:?approved evidence store path required}"
: "${TRUSTED_PUBKEY:?organization public key required}"
: "${TRUSTED_PUBKEY_SHA256:?separately trusted 64-hex digest required}"
: "${APPROVED_SCOPE_JSON:?externally authorized scope file required}"
python3 scripts/evidence_gate.py \
  --record "$EVIDENCE_ROOT/record.json" \
  --signature "$EVIDENCE_ROOT/record.sig" \
  --observation "$EVIDENCE_ROOT/observation.json" \
  --baseline "$EVIDENCE_ROOT/baseline.json" \
  --scope "$APPROVED_SCOPE_JSON" \
  --trusted-pubkey "$TRUSTED_PUBKEY" \
  --pubkey-sha256 "$TRUSTED_PUBKEY_SHA256" \
  --evidence-root "$EVIDENCE_ROOT"
```

| Tool result | Meaning | Next action |
|---|---|---|
| `NOT_READY` (exit 2) | Missing, changed, expired, synthetic or out-of-scope evidence, bad signature/key, or unapproved context | Stop and obtain valid independent evidence; don't change expected values |
| `REVIEW_REQUIRED` (exit 0) | Detached signature, observation hash, baseline hash, source scope, and time have passed integrity checks | Apply **control-specific predicate**, cross-check actual deployment and independently review |
| Live `PASS` | **Not an output of this tool** | Authorized acceptance process outside this repository, with signed reviewer decision |

**Important limitations:** a detached signature authenticates only the key holder. It does not prove source honesty, network location, Azure identity, RBAC/MI policy, original observation completeness, or actual control success. The `source_environment` field is signed metadata, not a hardware-backed attestation. Distinct observation timestamps and independent infrastructure-side evidence are needed to substantiate live claims.

## 5. Release safety gate

```bash
python3 scripts/release_gate.py --root .
# Expected JSON: "decision": "NO_GO", "live_passes": 0
```

The local release gate **never issues GO**. A production decision additionally needs signed external evidence of full release-scope controls, no unresolved Critical/P0 blockers, approved exception handling, privileged review, approved rollback plan, DR test and change board decision. This is not a compliance certification.

## 6. CI/CD boundary

`turn08-offline-integrity.yml` runs `validate_catalogue.py`, the Python regression tests, and `release_gate.py` on GitHub-hosted runners **without Azure credentials**, with `contents: read`. It **does not** call `az login`, `terraform apply`, WAF probes, traffic generation, role mutation, or real infrastructure queries. An independently approved, privately networked runner and federated identity are required for live read-only collection.

Test data is explicitly synthetic: tests create temporary Ed25519 keys, which are discarded after each run, and use obvious fake tenant/subscription IDs. `27/27` unit tests succeeding is *not* evidence of 1,716 production controls succeeding.

## 7. Failure triage and operator actions

| Failure | Probable cause | Safe response |
|---|---|---|
| Source hash mismatch | Catalogue changed or transferred incorrectly | Compare signed release manifest, restore reviewed version, do not rehash automatically |
| ID duplication or missing ID | Dropped case, wrong phase input | Compare phase-specific source JSON and 78-step range |
| `NOT_READY` due to key pin | Untrusted replacement signer, incorrectly provisioned key | Escalate to trust owner; never replace trusted pin based on the suspect record |
| Bad signed envelope | Signature mismatch or unsigned edits | Recollect and re-sign on approved CI; preserve originals |
| Wrong scope / subscription | Wrong target or authorization ticket | Stop; obtain explicit approved scope |
| Evidence older than 7 days | Stale observations | Recollect after authorization; retain historical evidence separately |
| Expected `NO_GO` in pipeline | No accepted Azure evidence | Report truthful unresolved acceptance; don't disable release gate |

## 8. Next steps

Turn 09: cross-document quality audit, 1,716-case coverage and lineage report, GitHub Actions status verification. Turn 10: final English deliverable release manifest, commit checks, independent acceptance handoff. The user's participation is **not needed** for Turn 09/10 offline documentation and GitHub publication; **live validation** will require actual implementation source, an approved non-production Azure environment, and explicit execution authorization.
