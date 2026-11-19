#!/usr/bin/env python3
"""Cross-catalogue assurance-readiness audit for all 1,716 published test IDs.

Read-only: parses canonical commands and audit status, executes NOTHING.
Source integrity, green CI and a present script are NEVER a live Azure PASS.
No string heuristic here may authorize deployment or release.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

if __package__:
    from .audit_catalogue_dependencies import ROOT, SOURCES, EXPECTED_IDS, audit
else:
    from audit_catalogue_dependencies import ROOT, SOURCES, EXPECTED_IDS, audit

SELFTEST = re.compile(r"(?<!\w)--selftest(?:\b|=)")
STATIC_PRESENCE = re.compile(
    r"^\s*(?:test\s+-(?:s|f|d)\b|grep\b|sha256sum\b|find\b|ls\b)"
)
BROWSER = {
    "AZ-T20-07", "AZ-T20-09", "AZ-T20-15", "AZ-T20-17",
    *(f"AZ-T64-{n:02}" for n in range(1, 18, 2)),
}
# Synthetic parity is defined by the frozen published catalogue design (odd:
# review/procedure, even: offline deviation).  An odd-numbered --selftest is
# a REVIEW FLAG, not necessarily an error in the canonical source.
PHASES = (
    (1, 10, "P1"), (11, 20, "P2"), (21, 32, "P3"),
    (33, 45, "P4"), (46, 58, "P5"), (59, 68, "P6"), (69, 78, "P7"),
)


def phase_for(case_id: str) -> str:
    step = int(case_id[4:6])
    return next(name for start, end, name in PHASES if start <= step <= end)


def review(root: Path = ROOT, include_cases: bool = False) -> dict:
    """Build evidence-conscious review inventory, not a test acceptance count."""
    root = Path(root)
    deps = audit(root, include_cases=True)
    errors = list(deps["errors"])
    rows: dict[str, dict] = {}
    counts = Counter()
    by_phase = defaultdict(Counter)
    classes = Counter()
    flags_by_name = defaultdict(list)

    for relative in SOURCES:
        try:
            source = json.loads((root / relative).read_text(encoding="utf-8"))
            cases = source["cases"] if "cases" in source else source["tests"]
            if not isinstance(cases, list):
                raise ValueError("cases/tests must be a list")
        except (OSError, KeyError, ValueError, TypeError) as exc:
            errors.append(f"{relative}: unavailable canonical source: {exc}")
            continue

        for case in cases:
            if not isinstance(case, dict) or not isinstance(case.get("id"), str):
                errors.append(f"{relative}: malformed case row")
                continue
            ident = case["id"]
            if ident in rows or ident not in EXPECTED_IDS:
                errors.append(f"{relative}: invalid/duplicate ID {ident}")
                continue
            cmd = case.get("command")
            if not isinstance(cmd, str) or not cmd.strip():
                errors.append(f"{ident}: blank or invalid command")
                continue
            dep = deps.get("cases", {}).get(ident)
            if dep is None:
                errors.append(f"{ident}: absent from dependency inventory")
                continue
            odd = int(ident[-2:]) % 2 == 1
            is_selftest = bool(SELFTEST.search(cmd))
            missing = bool(dep["missing_scripts"] or dep["missing_inputs"])

            # These categories are deliberately not PASS/FAIL decisions.
            if missing:
                status = "SOURCE_REFERENCE_MISSING"
            elif not odd:
                status = "OFFLINE_SYNTHETIC_ONLY"
            elif is_selftest:
                status = "ODD_SELFTEST_REQUIRES_SEMANTIC_REVIEW"
            else:
                status = "UNVERIFIED_NON_SYNTHETIC_PROCEDURE"
            flags = []
            if ident in BROWSER:
                flags.append("REAL_APP_AUTH_AND_RUNNER_REQUIRED")
            if odd and is_selftest:
                flags.append("ODD_ID_RUNS_SELFTEST_NOT_RUNTIME_EVIDENCE")
            if odd and STATIC_PRESENCE.search(cmd):
                flags.append("ARTIFACT_PRESENCE_NEEDS_CONTENT_AND_BASELINE_REVIEW")
            if not odd and not is_selftest:
                flags.append("EVEN_ID_NO_EXPLICIT_SELFTEST_OPTION")
            if dep["literal_script_state"] == "NO_DIRECT_SCRIPT_REFERENCE":
                flags.append("NO_LOCAL_SCRIPT_REF_CLI_OR_MANUAL_REVIEW")
            if missing:
                flags.append("UNRESOLVED_LITERAL_PATH")

            for flag in flags:
                flags_by_name[flag].append(ident)
            classes[str(case.get("execution_class", "UNSPECIFIED"))] += 1
            counts[status] += 1
            counts["ODD_PROCEDURES" if odd else "EVEN_SYNTHETIC_LABELS"] += 1
            by_phase[phase_for(ident)][status] += 1
            by_phase[phase_for(ident)]["cases"] += 1
            rows[ident] = {
                "catalogue": relative,
                "phase": phase_for(ident),
                "case_polarity": "ODD_REVIEW_OR_OBSERVATION" if odd else "EVEN_SYNTHETIC",
                "execution_class_claim": case.get("execution_class", "UNSPECIFIED"),
                "source_reference": dep["literal_script_state"],
                "missing_script_paths": dep["missing_scripts"],
                "missing_input_paths": dep["missing_inputs"],
                "assurance_readiness": status,
                "review_flags": flags,
                "accepted_live_evidence": False,
                "azure_acceptance": "NOT_READY",
            }

    missing_ids = EXPECTED_IDS - set(rows)
    if missing_ids:
        errors.append(f"case coverage incomplete: {len(missing_ids)} canonical IDs absent")
    if len(rows) != 1716:
        errors.append(f"expected 1716 reviewed IDs, got {len(rows)}")
    if counts["ODD_PROCEDURES"] != 858 or counts["EVEN_SYNTHETIC_LABELS"] != 858:
        errors.append("858 odd/even partition violated")
    if (sum(counts[k] for k in (
        "SOURCE_REFERENCE_MISSING", "OFFLINE_SYNTHETIC_ONLY",
        "ODD_SELFTEST_REQUIRES_SEMANTIC_REVIEW", "UNVERIFIED_NON_SYNTHETIC_PROCEDURE"
    )) != len(rows)):
        errors.append("case assurance classification not exhaustive")

    result = {
        "schema": "azure-assurance-semantic-readiness/v1",
        "execution_class": "OFFLINE_SOURCE_INSPECTION_ONLY",
        "catalogue_cases_reviewed": len(rows),
        "classification": dict(sorted(counts.items())),
        "by_phase": {p: dict(sorted(by_phase[p].items())) for _, _, p in PHASES},
        "published_execution_class_distribution": dict(sorted(classes.items())),
        "flag_counts": {k: len(v) for k, v in sorted(flags_by_name.items())},
        "flag_case_ids": {k: sorted(v) for k, v in sorted(flags_by_name.items())},
        "literal_dependency_snapshot": {
            **deps["literal_script_reference"],
            "MISSING_INPUT_CASES": deps["cases_with_missing_input"],
        },
        "errors": errors,
        "release_decision": "NO_GO",
        "independently_approved_azure_passes": 0,
        "interpretation": [
            "858 EVEN IDs label synthetic deviation checks; never Azure acceptance",
            "858 ODD IDs describe design, static review, approved observation or live procedures",
            "An ODD --selftest is flagged for semantics review, never counted as runtime proof",
            "A tracked script or shell command is not automatically a complete control-specific check",
            "An absence of local script references does not prove a case lacks an execution method",
            "Presence/grep/hash-only checks need content and approved baseline interpretation",
            "No Azure CLI, Terraform, browser, local test command or network request was executed",
            "No external evidence, issuer, runner or independent reviewer was verified",
        ],
    }
    if include_cases:
        result["cases"] = {k: rows[k] for k in sorted(rows)}
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--cases", action="store_true", help="include all 1716 review rows")
    ap.add_argument("--strict", action="store_true", help="exit 2 until independently accepted live evidence exists")
    args = ap.parse_args(argv)
    output = review(args.root, include_cases=args.cases)
    encoded = json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    if output["errors"] or args.strict:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
