#!/usr/bin/env python3
"""Rank the 160 flagged static-check procedures without executing test commands.

A deterministic review queue. It does NOT verify an approved baseline,
prove application behavior, establish identity/signer provenance, or certify Azure.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

if __package__:
    from .audit_semantic_readiness import ROOT, STATIC_PRESENCE, review
    from .audit_catalogue_dependencies import SOURCES
else:
    from audit_semantic_readiness import ROOT, STATIC_PRESENCE, review
    from audit_catalogue_dependencies import SOURCES

# Five source-grounded semantic traps to be triaged ahead of existence-only checks.
FIRST_FIVE = (
    "AZ-T20-13",  # grep ignoreHTTPSErrors would also accept an insecure 'true'
    "AZ-T45-03",  # sha256sum displays a plan digest without comparing approved value
    "AZ-T45-19",  # jq unique reviewers not independent of author / executor
    "AZ-T40-11",  # jq truthy digest+commit not correlated to a signed release
    "AZ-T45-21",  # jq truthy plan/commit/executor is not an approved apply record
)
PRIORITY_EXPLANATIONS = {
    FIRST_FIVE[0]: (
        "TLS_BYPASS_STRING_SEARCH",
        "Static grep can find ignoreHTTPSErrors: true and still exit zero.",
        "Inspect actual Playwright configuration and require TLS validation; real browser/TLS evidence remains blocked.",
    ),
    FIRST_FIVE[1]: (
        "PLAN_HASH_NOT_COMPARED",
        "sha256sum output alone does not compare the exact plan with an independently approved digest.",
        "Hash the actual approved plan bytes and compare a separately controlled authorized digest; verify signers externally.",
    ),
    FIRST_FIVE[2]: (
        "REVIEWER_INDEPENDENCE_UNVERIFIED",
        "Two distinct reviewer entries may include the change author or deploy executor.",
        "Verify distinct reviewer identities, roles and separation from author/executor; verify authorization externally.",
    ),
    FIRST_FIVE[3]: (
        "ARTIFACT_SOURCE_UNBOUND",
        "A JSON document with nonempty digest and commit does not bind to approved release source/artifact.",
        "Type-check and compare exact artifact digest and source commit against the separately controlled approval.",
    ),
    FIRST_FIVE[4]: (
        "DEPLOY_EVIDENCE_UNBOUND",
        "Nonempty plan SHA, source commit and executor may differ from approved release details.",
        "Compare immutable plan/source/executor references with change approval and independent execution records.",
    ),
}
CATEGORIES = (
    ("evidence", re.compile(r"\bevidence/[A-Za-z0-9_./-]+"), 75,
     "Evidence-file presence/self-asserted status needs independent origin, time, scope and expected result"),
    ("hash_output", re.compile(r"\bsha256sum\b"), 66,
     "Hash output alone needs exact approved digest comparison, source identity and custody"),
    ("jq_status", re.compile(r"\bjq\s+-e\b"), 62,
     "Local JSON predicate alone lacks provenance, approved baseline and independent attestation"),
    ("grep_text", re.compile(r"\b(?:grep|rg)\b"), 51,
     "Text occurrence does not establish effective runtime configuration or safe absence"),
    ("file_presence", re.compile(r"\b(?:test\s+-(?:s|f|d)|find|ls)\b"), 42,
     "Filesystem existence/listing alone does not validate policy behavior or approved content"),
)


def _criterion(row):
    for field in ("approved_acceptance_criterion_en", "expected",
                  "acceptance_criterion_en", "acceptance_criterion", "criteria"):
        value = row.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "SOURCE_CRITERION_NEEDS_REVIEW"


def classify(case):
    """Advisory static risk, not PASS/FAIL or a claim of vulnerability."""
    ident, cmd = case["id"], case["command"]
    if ident in PRIORITY_EXPLANATIONS:
        code, reason, action = PRIORITY_EXPLANATIONS[ident]
        return "P0", code, reason, action, 100 - FIRST_FIVE.index(ident)

    hits = [(key, score, description) for key, rx, score, description in CATEGORIES if rx.search(cmd)]
    if not hits:
        return ("P2", "OTHER_STATIC_PRESENCE", "Command only proves limited local state",
                "Review against its full approved criterion and observed source", 20)

    key, score, reason = max(hits, key=lambda x: x[1])
    if "private" in case.get("command", "").lower() or any(
        word in ident for word in ()
    ):
        # No uncontrolled leap from a string match to P0 vulnerability.
        score = min(score + 2, 89)
    return (
        "P1" if score >= 60 else "P2",
        key.upper(),
        reason,
        "Require typed criteria, source/artifact digest, approved baseline and independently reviewed observation.",
        score,
    )


def triage(root: Path = ROOT, include_rows: bool = True):
    root = Path(root)
    audit = review(root, include_cases=False)
    errors = list(audit["errors"])
    source_rows = {}
    for rel in SOURCES:
        try:
            doc = json.loads((root / rel).read_text(encoding="utf-8"))
            cases = doc["cases"] if "cases" in doc else doc["tests"]
        except (OSError, KeyError, TypeError, ValueError) as err:
            errors.append(f"{rel}: unreadable source: {err}")
            continue
        for item in cases:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            ident = item["id"]
            if ident in source_rows:
                errors.append(f"duplicate ID {ident}")
            source_rows[ident] = (rel, item)

    flagged = audit["flag_case_ids"].get("ARTIFACT_PRESENCE_NEEDS_CONTENT_AND_BASELINE_REVIEW", [])
    priorities = []
    for ident in flagged:
        if ident not in source_rows:
            errors.append(f"flagged source absent: {ident}")
            continue
        rel, item = source_rows[ident]
        cmd = item.get("command", "")
        if (int(ident[-2:]) % 2 != 1 or not isinstance(cmd, str)
                or not STATIC_PRESENCE.search(cmd)):
            errors.append(f"unexpected non-static flagged row: {ident}")
            continue
        priority, code, reason, action, score = classify(item)
        priorities.append({
            "id": ident,
            "phase": audit.get("by_phase", {}) and next(
                p for p, counts in audit["by_phase"].items()
                if int(ident[4:6]) in (
                    {"P1": range(1,11), "P2":range(11,21), "P3":range(21,33),
                     "P4":range(33,46), "P5":range(46,59), "P6":range(59,69),
                     "P7":range(69,79)}[p]
                )
            ),
            "catalogue": rel,
            "priority": priority,
            "review_score": score,
            "semantic_risk": code,
            "published_command": cmd,
            "published_acceptance_criterion": _criterion(item),
            "specific_review_reason": reason,
            "requested_action": action,
            "control_provenance": "PUBLISHED_SOURCE_UNMODIFIED",
            "criterion_verified": False,
            "independent_approval_verified": False,
            "azure_acceptance": "NOT_READY",
        })
    priorities.sort(key=lambda x: (-x["review_score"], x["id"]))
    if len(priorities) != 160:
        errors.append(f"expected 160 source-grounded static flagged IDs, got {len(priorities)}")
    if priorities[:5] and {row["id"] for row in priorities[:5]} != set(FIRST_FIVE):
        errors.append("the five fixed critical semantic traps were not ranked first")
    if not set(FIRST_FIVE).issubset(set(flagged)):
        errors.append("expected five critical semantic traps not all in original 160 flags")

    counts = {prio: sum(x["priority"] == prio for x in priorities) for prio in ("P0","P1","P2")}
    output = {
        "schema": "azure-static-criteria-priority-review/v1",
        "execution_class": "READ_ONLY_SOURCE_TRIAGE",
        "catalogue_test_ids": audit["catalogue_cases_reviewed"],
        "static_review_candidates": len(priorities),
        "priority_counts": counts,
        "first_five_critical_ids": list(FIRST_FIVE),
        "errors": errors,
        "live_azure_acceptances": 0,
        "release_decision": "NO_GO",
        "limitations": [
            "Risk scores are review-order heuristics, not exploitability, factual failure or compliance severity",
            "Published commands and criteria are unchanged; no Azure or Terraform commands were run",
            "Existing data and even perfectly matching hash/identity fields require signed independent verification",
            "The five focused semantic checks can flag differences, but never create approved Azure PASS",
        ],
    }
    if include_rows:
        output["cases"] = priorities
    return output


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path)
    p.add_argument("--summary", action="store_true", help="omit full 160-row review queue")
    p.add_argument("--strict", action="store_true", help="return 2 while acceptance remains unapproved")
    args = p.parse_args(argv)
    report = triage(args.root, include_rows=not args.summary)
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 2 if report["errors"] or args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
