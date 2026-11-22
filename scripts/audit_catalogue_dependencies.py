#!/usr/bin/env python3
"""Read-only, fail-closed dependency inventory for all 1,716 canonical test IDs.

The literal command reference audit is NOT a test executor. An existing file
does not prove that a control works, and a command without a local script may
be a valid approved Azure/CLI/manual procedure. No live PASS is issued here.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    "specs/english_tests_001_440.json",
    "specs/phase3_264_en.json",
    "specs/phase4_286_en.json",
    "specs/phase5_286_en.json",
    "specs/phase6_220_en.json",
    "specs/phase7_220_en.json",
)
SCRIPT_REF = re.compile(r"(?<![\w/.-])(?:scripts|tests)/[\w./-]+\.(?:py|sh|ts|js|mjs|ps1)\b")
INPUT_REF = re.compile(r"(?<![\w/.-])(?:specs|schemas|fixtures|policy)/[\w./-]+\.(?:json|ya?ml|csv|txt)\b")
CASE_ID = re.compile(r"^AZ-T(\d{2})-(\d{2})$")
EXPECTED_IDS = {f"AZ-T{s:02d}-{i:02d}" for s in range(1, 79) for i in range(1, 23)}


def literal_refs(command: str) -> tuple[list[str], list[str]]:
    """Extract local paths only, never execute or expand shell variables."""
    if not isinstance(command, str):
        raise ValueError("command must be a string")
    return sorted(set(SCRIPT_REF.findall(command))), sorted(set(INPUT_REF.findall(command)))


def path_exists(root: Path, relative: str) -> bool:
    """Refuse to follow any reference outside the checked-out repository."""
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        return False
    resolved_root = root.resolve()
    target = (resolved_root / relative).resolve()
    return target.is_relative_to(resolved_root) and target.is_file()


def audit(root: Path = ROOT, include_cases: bool = False) -> dict:
    root = Path(root)
    errors: list[str] = []
    rows: dict[str, dict] = {}
    status_counts = Counter()
    missing_scripts: dict[str, list[str]] = defaultdict(list)
    missing_inputs: dict[str, list[str]] = defaultdict(list)
    source_counts: dict[str, int] = {}

    for rel in SOURCES:
        try:
            document = json.loads((root / rel).read_text(encoding="utf-8"))
            items = document["cases"] if "cases" in document else document["tests"]
            if not isinstance(items, list):
                raise ValueError("tests/cases must be a list")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"{rel}: cannot read canonical catalogue: {exc}")
            continue
        source_counts[rel] = len(items)
        for item in items:
            if not isinstance(item, dict):
                errors.append(f"{rel}: non-object catalogue item")
                continue
            case_id = item.get("id")
            match = CASE_ID.fullmatch(case_id) if isinstance(case_id, str) else None
            if not match or case_id not in EXPECTED_IDS:
                errors.append(f"{rel}: invalid test ID {case_id!r}")
                continue
            if case_id in rows:
                errors.append(f"{rel}: duplicate test ID {case_id}")
                continue
            if item.get("step") != int(match.group(1)):
                errors.append(f"{case_id}: step does not match ID")
            command = item.get("command", "")
            if not isinstance(command, str) or not command.strip():
                errors.append(f"{case_id}: missing command")
                command = ""
            if item.get("azure_live_pass") is not False:
                errors.append(f"{case_id}: live acceptance is not explicitly false")
            scripts, inputs = literal_refs(command)
            absent_scripts = [p for p in scripts if not path_exists(root, p)]
            absent_inputs = [p for p in inputs if not path_exists(root, p)]
            status = (
                "MISSING_SCRIPT_REFERENCE" if absent_scripts else
                "TRACKED_SCRIPT_REFERENCE" if scripts else
                "NO_DIRECT_SCRIPT_REFERENCE"
            )
            status_counts[status] += 1
            if absent_inputs:
                status_counts["MISSING_INPUT_CASES"] += 1
            for p in absent_scripts:
                missing_scripts[p].append(case_id)
            for p in absent_inputs:
                missing_inputs[p].append(case_id)
            rows[case_id] = {
                "source": rel,
                "literal_script_state": status,
                "script_refs": scripts,
                "input_refs": inputs,
                "missing_scripts": absent_scripts,
                "missing_inputs": absent_inputs,
                # Provenance is a catalogue assertion, not an independently audited PASS.
                "azure_acceptance": "NOT_READY",
            }

    missing_ids = sorted(EXPECTED_IDS - rows.keys())
    if missing_ids:
        errors.append(f"missing canonical test IDs: {missing_ids[:12]} (total {len(missing_ids)})")
    if len(rows) != 1716:
        errors.append(f"expected 1,716 unique IDs, found {len(rows)}")

    unresolved_ids = sorted(
        k for k, r in rows.items() if r["missing_scripts"] or r["missing_inputs"]
    )
    summary = {
        "status": "INVALID_CATALOGUE" if errors else "AUDIT_ONLY_NOT_ACCEPTANCE",
        "canonical_test_ids": len(rows),
        "expected_test_ids": 1716,
        "catalogue_counts": source_counts,
        "literal_script_reference": {
            k: status_counts[k] for k in (
                "MISSING_SCRIPT_REFERENCE", "NO_DIRECT_SCRIPT_REFERENCE",
                "TRACKED_SCRIPT_REFERENCE",
            )
        },
        "cases_with_missing_input": status_counts["MISSING_INPUT_CASES"],
        "cases_with_unresolved_literal_dependencies": len(unresolved_ids),
        "missing_script_paths": {k: len(v) for k, v in sorted(missing_scripts.items())},
        "missing_input_paths": {k: len(v) for k, v in sorted(missing_inputs.items())},
        "azure_live_passes_verified": 0,
        "release_decision": "NO_GO",
        "errors": errors,
        "limitations": [
            "A tracked script does not prove that it implements the test semantics.",
            "A command without a script reference may be an Azure CLI/manual procedure.",
            "Literal paths miss dynamically constructed or variable-expanded references.",
            "This audit does not run the 1,716 commands or access any Azure environment.",
            "Missing files must be genuinely implemented and verified, never stubbed to claim PASS.",
        ],
    }
    if include_cases:
        summary["cases"] = {k: rows[k] for k in sorted(rows)}
        summary["unresolved_ids"] = unresolved_ids
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--cases", action="store_true", help="include per-ID inventory")
    parser.add_argument("--out", type=Path, help="write sanitized JSON inventory")
    parser.add_argument("--strict", action="store_true", help="return 2 for any unresolved local dependency")
    args = parser.parse_args(argv)
    result = audit(args.root, include_cases=args.cases)
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(json.dumps(
        {k: v for k, v in result.items() if k not in ("cases", "unresolved_ids")},
        ensure_ascii=False, indent=2, sort_keys=True,
    ))
    if result["errors"]:
        return 2
    if args.strict and result["cases_with_unresolved_literal_dependencies"]:
        return 2
    # Audit-only command may succeed despite known unresolved dependencies.
    # The separate release gate is unconditionally NO_GO for that situation.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
