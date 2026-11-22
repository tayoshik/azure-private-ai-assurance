#!/usr/bin/env python3
"""Source-only detailed review queue for exactly 149 shell-risk P0 local cases.

No command is executed or rendered in the report. No shell safety is certified.
This is reviewer task planning for immutable 1,716 Azure assurance test IDs.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import shlex

from build_execution_route_1716 import ROOT, digest_case
from triage_local_464 import (
    PRIORITY_SHELL, TriageError, inspect_command, make_queue,
    REMOTE_TOOLS, INDIRECT_TOOLS,
)

SCHEMA = "azure-local-p0-149-review/v1"
DYNAMIC = "A_DYNAMIC_OR_INDIRECT_EXECUTION_REVIEW"
CHAIN = "B_CHAIN_AND_EXIT_STATUS_REVIEW"
PIPE = "C_PIPELINE_AND_DATA_FLOW_REVIEW"
REDIRECT = "D_REDIRECTION_AND_OUTPUT_CUSTODY_REVIEW"
UNKNOWN = "E_UNPARSEABLE_OR_OTHER_SHELL_REVIEW"
CLASSES = (DYNAMIC, CHAIN, PIPE, REDIRECT, UNKNOWN)
SHELL_CHAIN = frozenset({";", ";;", "&&", "||", "&"})
SHELL_PIPE = frozenset({"|", "|&"})
SHELL_REDIRECT = frozenset({"<", ">", "<<", ">>", "<>", ">&", "<&", ">|", "<<<", "<<-"})
SHELL_META = frozenset(";&|<>")
RISK_TERMS = frozenset({
    "rm", "rmdir", "mv", "cp", "dd", "tee", "chmod", "chown", "truncate",
    "touch", "sed", "awk", "perl", "python", "python3", "terraform",
    "git", "npm", "node", "kubectl", "az", "curl", "wget", "ssh",
    "sudo", "bash", "sh", "npx", "eval", "exec", "xargs",
})
SOURCES = (
    "specs/english_tests_001_440.json", "specs/phase3_264_en.json",
    "specs/phase4_286_en.json", "specs/phase5_286_en.json",
    "specs/phase6_220_en.json", "specs/phase7_220_en.json",
)
NEXT_REVIEW = {
    DYNAMIC: (
        "REVIEW_COMPLETE_EXPANSIONS_AND_INDIRECT_TARGETS",
        "APPROVE_NO_EXECUTION_OR_EXTERNAL_NETWORK_SIDE_EFFECTS",
        "PIN_DEPENDENCIES_AND_IDENTITIES_BEFORE_ANY_RUN",
    ),
    CHAIN: (
        "REVIEW_ALL_SHELL_SEGMENTS_AND_BRANCH_EXIT_CODES",
        "REVIEW_SIDE_EFFECTS_AND_APPROVED_EVIDENCE_INPUTS",
        "APPROVE_EACH_SEGMENT_BEFORE_ANY_RUN",
    ),
    PIPE: (
        "REVIEW_EACH_PIPELINE_PROCESS_AND_DATA_SENSITIVITY",
        "REVIEW_PIPEFAIL_AND_FULL_EXIT_STATUS_ASSERTION",
        "APPROVE_OUTPUT_DESTINATIONS_BEFORE_ANY_RUN",
    ),
    REDIRECT: (
        "REVIEW_FILE_DESCRIPTOR_AND_TARGET_PATH_SAFETY",
        "BLOCK_PUBLIC_OUTPUT_AND_UNAPPROVED_OVERWRITES",
        "REVIEW_ERROR_SUPPRESSION_BEFORE_ANY_RUN",
    ),
    UNKNOWN: (
        "DO_NOT_RUN_UNPARSEABLE_OR_UNCLASSIFIED_SHELL",
        "REQUIRE_APPROVED_MANUAL_PARSE_AND_COMMAND_OWNER",
        "RECHECK_CANONICAL_SOURCE_FINGERPRINT",
    ),
}


def _tokens(command: str) -> tuple[list[str], bool]:
    """Conservative lexical scan, NOT an executable Bash grammar."""
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|<>")
        lexer.whitespace_split = True
        lexer.commenters = ""
        return list(lexer), False
    except ValueError:
        return [], True


def classify(command: str, parent_reasons: list[str]) -> tuple[str, list[str]]:
    """Exclusive priority class plus overlapping redacted, reviewer-facing flags."""
    if not isinstance(command, str) or not command.strip() or not isinstance(parent_reasons, list):
        raise TriageError("invalid canonical shell triage record")
    tokens, parse_error = _tokens(command)
    flags: set[str] = set()
    if parse_error:
        flags.add("LEXER_COULD_NOT_PARSE")
    operators = [t for t in tokens if t and set(t) <= SHELL_META]
    if any(x in SHELL_CHAIN for x in operators):
        flags.add("CHAIN_OR_CONDITIONAL_EXIT_STATUS")
    if any(x in SHELL_PIPE for x in operators):
        flags.add("PIPELINE_DATAFLOW")
    if any(x in SHELL_REDIRECT for x in operators):
        flags.add("REDIRECTION_OR_DESCRIPTOR")
    if any(x not in SHELL_CHAIN | SHELL_PIPE | SHELL_REDIRECT for x in operators):
        flags.add("UNRECOGNIZED_SHELL_OPERATOR")
    if "$(" in command or "\x60" in command or "\n" in command:
        flags.add("COMMAND_SUBSTITUTION_OR_MULTILINE")
    if any(x in REMOTE_TOOLS for x in tokens[1:]):
        flags.add("NESTED_REMOTE_TOOL_NEEDS_REVIEW")
    if tokens and tokens[0] in INDIRECT_TOOLS or any(x in INDIRECT_TOOLS for x in tokens[1:]):
        flags.add("INDIRECT_SHELL_TOOL_NEEDS_REVIEW")
    if any(x in RISK_TERMS for x in tokens[1:]):
        flags.add("NESTED_TOOL_OR_SIDE_EFFECT_NEEDS_REVIEW")
    if "DYNAMIC_PYTHON_INVOCATION_REVIEW" in parent_reasons:
        flags.add("DYNAMIC_PYTHON_OR_MODULE")
    if "SHELL_LEXING_UNCERTAIN" in parent_reasons or "FIRST_COMMAND_FAMILY_MISMATCH" in parent_reasons:
        flags.add("PARENT_LEXICAL_UNCERTAINTY")
    if (flags & {"LEXER_COULD_NOT_PARSE", "UNRECOGNIZED_SHELL_OPERATOR",
                 "PARENT_LEXICAL_UNCERTAINTY"}):
        classification = UNKNOWN
    elif flags & {"COMMAND_SUBSTITUTION_OR_MULTILINE", "NESTED_REMOTE_TOOL_NEEDS_REVIEW",
                  "INDIRECT_SHELL_TOOL_NEEDS_REVIEW", "DYNAMIC_PYTHON_OR_MODULE"}:
        classification = DYNAMIC
    elif "CHAIN_OR_CONDITIONAL_EXIT_STATUS" in flags:
        classification = CHAIN
    elif "PIPELINE_DATAFLOW" in flags:
        classification = PIPE
    elif "REDIRECTION_OR_DESCRIPTOR" in flags:
        classification = REDIRECT
    else:
        # Source code changed or a lexical heuristic missed something.
        # Never infer safe just because one parser found no operator.
        classification = UNKNOWN
        flags.add("P0_WITHOUT_RECOGNIZED_DETAILED_INDICATOR")
    return classification, sorted(flags)


def build_review(root: Path = ROOT, *, include_cases: bool = True) -> dict:
    parent = make_queue(root, include_cases=True)
    if parent["status"] != "REVIEW_PRIORITIES_ONLY":
        raise TriageError("upstream 464-case inventory invalid")
    p0 = {
        key: row for key, row in parent["cases"].items()
        if row["review_priority"] == PRIORITY_SHELL
    }
    if len(p0) != 149:
        raise TriageError("historical 149-case P0 partition changed")
    original: dict[str, dict] = {}
    for path in SOURCES:
        try:
            document = json.loads((Path(root) / path).read_text(encoding="utf-8"))
            source = document["cases"] if "cases" in document else document["tests"]
        except (OSError, ValueError, TypeError, KeyError) as exc:
            raise TriageError("frozen catalogue unavailable") from exc
        for row in source:
            ident = row["id"]
            if ident in original:
                raise TriageError("duplicate frozen catalogue case")
            original[ident] = row

    rows = {}
    counts = Counter()
    flags_count = Counter()
    phases = defaultdict(Counter)
    for ident, meta in sorted(p0.items()):
        rec = original.get(ident)
        if not rec or meta["contract_sha256"] != digest_case(rec):
            raise TriageError("P0 source provenance mismatch")
        # Reuse original 464-way classification, do not allow promotion.
        reclass, reasons = inspect_command(rec["command"], meta["command_family"], [])
        if reclass != PRIORITY_SHELL:
            raise TriageError("P0 case no longer marked as shell review")
        if sorted(x for x in meta["review_reason_codes"] if x != "MISSING_LITERAL_INPUT_PATH") != reasons:
            raise TriageError("parent risk flag mismatch")
        bucket, flags = classify(rec["command"], reasons)
        counts[bucket] += 1
        phases[rec["step"] // 10 if False else meta["canonical_source"]][bucket] += 1
        flags_count.update(flags)
        rows[ident] = {
            "source": meta["canonical_source"],
            "contract_sha256": meta["contract_sha256"],
            "command_family": meta["command_family"],
            "detailed_review_class": bucket,
            "risk_flag_codes": flags,
            "review_checklist": list(NEXT_REVIEW[bucket]),
            "source_dependencies_or_approved_inputs_verified": False,
            "actual_command_authorized": False,
            "command_executed": False,
            "semantic_expected_result_verified": False,
            "reviewer1_signed": False,
            "reviewer2_signed": False,
            "azure_live_acceptance": "NOT_READY",
        }
    if len(rows) != 149 or sum(counts.values()) != 149 or set(rows) != set(p0):
        raise TriageError("P0 review queue is incomplete")
    return {
        "schema": SCHEMA,
        "status": "SHELL_SOURCE_TRIAGE_ONLY",
        "original_frozen_case_count": 1716,
        "local_source_only_count": 464,
        "shell_p0_count": 149,
        "review_class_counts": {k: counts[k] for k in CLASSES},
        "phase_review_counts": {
            k: {cls: v[cls] for cls in CLASSES}
            for k, v in sorted(phases.items())
        },
        "risk_flag_counts": dict(sorted(flags_count.items())),
        "commands_executed": 0,
        "case_reviews_approved": 0,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "assurance_limitations": [
            "Shell lexing is not a Bash interpreter; categories are only review planning",
            "No commands, Azure resources, network endpoints or real evidence were evaluated",
            "No bucket grants execution permissions or proves a case acceptance",
            "Per-ID SHA-256 fingerprints bind to frozen command/expected source; not independent signatures",
        ],
        **({"cases": rows} if include_cases else {}),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--summary-only", action="store_true")
    parser.add_argument("--strict", action="store_true",
                        help="always deny acceptance, exit code 2")
    args = parser.parse_args(argv)
    try:
        result = build_review(args.root, include_cases=not args.summary_only)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(result, ensure_ascii=False,
                                            sort_keys=True, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "SOURCE_REVIEW_BLOCKED",
                          "error_type": type(exc).__name__,
                          "azure_live_passes": 0,
                          "release_decision": "NO_GO"}))
        return 1
    print(json.dumps({k: v for k, v in result.items() if k != "cases"},
                     ensure_ascii=False, sort_keys=True, indent=2))
    return 2 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
