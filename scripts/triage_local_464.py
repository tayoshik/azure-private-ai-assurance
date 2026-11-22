#!/usr/bin/env python3
"""Source-only triage of 464 local-appearing canonical acceptance commands.

This script NEVER executes command text. All 464 remain UNEXECUTED/NOT_READY.
Priority labels identify what reviewers should assess first, not what is safe to run.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import shlex

from build_execution_route_1716 import ROOT, ROUTE_LOCAL, build, digest_case

SCHEMA = "azure-local-464-review-queue/v1"
PRIORITY_SHELL = "P0_SHELL_OR_INDIRECT_EXECUTION_REVIEW"
PRIORITY_INPUT = "P1_PRIVATE_INPUT_AND_CUSTODY_REVIEW"
PRIORITY_TOOL = "P2_SOURCE_TOOL_SEMANTICS_REVIEW"
PRIORITY_ASSERTION = "P3_LOCAL_ASSERTION_SEMANTICS_REVIEW"
PRIORITIES = (PRIORITY_SHELL, PRIORITY_INPUT, PRIORITY_TOOL, PRIORITY_ASSERTION)
OPERATORS = frozenset({";", ";;", "&&", "||", "&", "|", "|&", "<", ">", "<<", ">>", "<>", ">&", "<&"})
REMOTE_TOOLS = frozenset({"az", "curl", "dig", "getent", "openssl", "npx", "wget", "ssh", "scp", "nc", "netcat"})
INDIRECT_TOOLS = frozenset({"bash", "sh", "zsh", "eval", "exec", "xargs", "env", "sudo", "pwsh", "powershell"})
BUILD_OR_STATIC_TOOLS = frozenset({"python3", "python", "terraform", "tflint", "checkov", "node", "npm"})
LOCAL_ASSERT_TOOLS = frozenset({"jq", "test", "grep", "find", "git", "sha256sum"})
ENV_RE = re.compile(r"\$(?:\{[A-Za-z_][A-Za-z0-9_]*[^}]*\}|[A-Za-z_][A-Za-z0-9_]*)")
SENSITIVE_RE = re.compile(
    r"(?i)(?:\.tfstate\b|\.tfplan\b|\.tfvars\b|"
    r"approved[_/-]|baseline|evidence[/_-]|"
    r"credentials?|private[/_-]|secret|customer|token[/_-])"
)


class TriageError(ValueError):
    """Invalid source inventory; no command may be executed to resolve it."""


def inspect_command(command: str, first_family: str, missing_inputs: list[str]) -> tuple[str, list[str]]:
    """Lexical heuristics only: never validate shell safety or evaluate inputs."""
    if not isinstance(command, str) or not command.strip():
        raise TriageError("empty canonical command")
    if not isinstance(first_family, str) or not first_family:
        raise TriageError("missing command family")
    if not isinstance(missing_inputs, list):
        raise TriageError("missing-input audit must be a list")
    reasons: set[str] = set()
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|<>")
        lexer.whitespace_split = True
        lexer.commenters = ""
        tokens = list(lexer)
    except ValueError:
        tokens = []
        reasons.add("SHELL_LEXING_UNCERTAIN")
    if any(t and all(ch in ";&|<>" for ch in t) for t in tokens):
        reasons.add("SHELL_OPERATOR_OR_REDIRECTION")
    if "$(" in command or "\x60" in command or "\n" in command:
        reasons.add("SHELL_EXPANSION_OR_MULTILINE")
    if any(t in REMOTE_TOOLS or t in INDIRECT_TOOLS for t in tokens[1:]):
        reasons.add("NESTED_NETWORK_OR_INDIRECT_TOOL")
    if tokens and tokens[0] in INDIRECT_TOOLS:
        reasons.add("INDIRECT_TOP_LEVEL_COMMAND")
    if tokens and (tokens[0] in ("python3", "python") and
                   any(t in ("-c", "-m") for t in tokens[1:])):
        reasons.add("DYNAMIC_PYTHON_INVOCATION_REVIEW")
    if tokens and tokens[0] != first_family:
        reasons.add("FIRST_COMMAND_FAMILY_MISMATCH")
    if ENV_RE.search(command):
        reasons.add("ENVIRONMENT_INPUT_UNVERIFIED")
    if SENSITIVE_RE.search(command):
        reasons.add("POSSIBLE_RESTRICTED_OR_APPROVED_INPUT")
    if missing_inputs:
        reasons.add("MISSING_LITERAL_INPUT_PATH")
    if first_family in BUILD_OR_STATIC_TOOLS:
        reasons.add("IMPLEMENTATION_OR_TOOL_SEMANTICS")
    if first_family not in BUILD_OR_STATIC_TOOLS | LOCAL_ASSERT_TOOLS:
        reasons.add("UNRECOGNIZED_LOCAL_COMMAND_FAMILY")
    shell_reasons = {
        "SHELL_LEXING_UNCERTAIN", "SHELL_OPERATOR_OR_REDIRECTION",
        "SHELL_EXPANSION_OR_MULTILINE", "NESTED_NETWORK_OR_INDIRECT_TOOL",
        "INDIRECT_TOP_LEVEL_COMMAND", "DYNAMIC_PYTHON_INVOCATION_REVIEW",
        "FIRST_COMMAND_FAMILY_MISMATCH",
    }
    if reasons & shell_reasons:
        priority = PRIORITY_SHELL
    elif reasons & {"ENVIRONMENT_INPUT_UNVERIFIED", "POSSIBLE_RESTRICTED_OR_APPROVED_INPUT",
                     "MISSING_LITERAL_INPUT_PATH"}:
        priority = PRIORITY_INPUT
    elif reasons & {"IMPLEMENTATION_OR_TOOL_SEMANTICS", "UNRECOGNIZED_LOCAL_COMMAND_FAMILY"}:
        priority = PRIORITY_TOOL
    else:
        priority = PRIORITY_ASSERTION
    return priority, sorted(reasons)


def make_queue(root: Path = ROOT, *, include_cases: bool = True) -> dict:
    """Join current immutable source commands to the preexisting source-only route."""
    root = Path(root)
    parent = build(root, include_cases=True)
    if parent["status"] != "ROUTING_INVENTORY_ONLY" or parent["errors"]:
        raise TriageError("parent inventory is invalid")
    if parent["route_counts"].get(ROUTE_LOCAL) != 464:
        raise TriageError("expected 464 local candidates; source route drift")
    cases = {}
    for rel in (
        "specs/english_tests_001_440.json", "specs/phase3_264_en.json",
        "specs/phase4_286_en.json", "specs/phase5_286_en.json",
        "specs/phase6_220_en.json", "specs/phase7_220_en.json",
    ):
        try:
            payload = json.loads((root / rel).read_text(encoding="utf-8"))
            records = payload["cases"] if "cases" in payload else payload["tests"]
        except (KeyError, TypeError, ValueError, OSError) as exc:
            raise TriageError("frozen source could not be read: " + rel) from exc
        for rec in records:
            if rec["id"] in cases:
                raise TriageError("duplicate frozen case ID")
            cases[rec["id"]] = rec

    entries = {}
    phase_counts: dict[str, Counter] = defaultdict(Counter)
    reasons_total = Counter()
    priorities = Counter()
    for case_id, row in sorted(parent["cases"].items()):
        if row["route"] != ROUTE_LOCAL:
            continue
        case = cases.get(case_id)
        if not case or row["catalogue_contract_sha256"] != digest_case(case):
            raise TriageError("immutable source fingerprint mismatch")
        priority, reasons = inspect_command(
            case["command"], row["direct_command_family"], row["missing_input_paths"])
        priorities[priority] += 1
        phase_counts[row["phase"]][priority] += 1
        reasons_total.update(reasons)
        entries[case_id] = {
            "canonical_source": row["canonical_catalogue"],
            "contract_sha256": row["catalogue_contract_sha256"],
            "command_family": row["direct_command_family"],
            "review_priority": priority,
            "review_reason_codes": reasons,
            "source_reference_state": row["source_reference_state"],
            "declared_missing_literal_input_count": len(row["missing_input_paths"]),
            "command_executed": False,
            "approved_input_verified": False,
            "semantic_assertion_reviewed": False,
            "independent_reviewer_signed": False,
            "azure_live_acceptance": "NOT_READY",
        }
    if len(entries) != 464 or sum(priorities.values()) != 464:
        raise TriageError("local priority partition is incomplete")
    for row in entries.values():
        if row["command_executed"] or row["approved_input_verified"] or row["independent_reviewer_signed"]:
            raise TriageError("unapproved evidence promotion")
    return {
        "schema": SCHEMA,
        "status": "REVIEW_PRIORITIES_ONLY",
        "original_total_cases": 1716,
        "local_candidate_cases": len(entries),
        "source_only_priority_counts": {p: priorities[p] for p in PRIORITIES},
        "phase_priority_counts": {
            phase: {p: counts[p] for p in PRIORITIES}
            for phase, counts in sorted(phase_counts.items())
        },
        "reason_counts": dict(sorted(reasons_total.items())),
        "review_queue_has_executable_commands": False,
        "commands_executed": 0,
        "approved_inputs_verified": 0,
        "independent_approvals": 0,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "limitations": [
            "Static lexical risk triage is not a shell parser or an authorization to run commands",
            "All 464 local-appearing commands may depend on real, restricted evidence",
            "A low-priority assertion can still be unsafe, insufficient, or semantically wrong",
            "No canonical case, command, approved result or Azure resource was changed",
        ],
        **({"cases": entries} if include_cases else {}),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--summary-only", action="store_true")
    parser.add_argument("--strict", action="store_true",
                        help="always return 2 until every original test is accepted")
    args = parser.parse_args(argv)
    try:
        report = make_queue(args.root, include_cases=not args.summary_only)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2,
                                            sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "LOCAL_REVIEW_SOURCE_BLOCKED",
                          "error_class": type(exc).__name__,
                          "azure_live_passes": 0, "release_decision": "NO_GO"}))
        return 1
    summary = {k: v for k, v in report.items() if k != "cases"}
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 2 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
