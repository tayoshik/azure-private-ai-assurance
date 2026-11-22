#!/usr/bin/env python3
"""Source-only review of 19 local grep/find/git/jq assertions (NOT accepted).

A reported match, file listing, git SHA or JSON approval flag is not actual
control acceptance. Original canonical commands and private evidence never run.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import shlex

from build_execution_route_1716 import ROOT, digest_case
from triage_local_464 import PRIORITY_ASSERTION, TriageError, inspect_command, make_queue
from audit_tool_semantics_13 import load_sources

SCHEMA = "azure-local-p3-19-assertion-semantics-review/v1"
GREP = "GREP_TEXT_MATCH_NOT_SEMANTIC_PROOF"
FIND = "FIND_LISTING_NOT_NONEMPTY_PROOF"
GIT = "GIT_SOURCE_METADATA_NOT_APPROVAL_PROOF"
JQ = "JQ_SELF_DECLARED_FLAGS_NOT_INDEPENDENT_APPROVAL"
GROUPS = (GREP, FIND, GIT, JQ)
EXPECTED = {
    "AZ-T14-03": GREP, "AZ-T14-05": GREP,
    "AZ-T14-07": GIT,
    "AZ-T15-01": GREP, "AZ-T15-03": GREP, "AZ-T15-11": GREP,
    "AZ-T16-05": FIND, "AZ-T16-11": FIND, "AZ-T16-15": FIND,
    "AZ-T20-11": GREP, "AZ-T20-13": GREP,
    "AZ-T21-21": GIT, "AZ-T23-21": GIT,
    "AZ-T44-09": FIND, "AZ-T45-05": GIT,
    "AZ-T69-03": JQ, "AZ-T69-11": JQ, "AZ-T69-13": JQ, "AZ-T69-15": JQ,
}
EXPECTED_COUNTS = {GREP: 7, FIND: 4, GIT: 4, JQ: 4}
CHECKS = {
    GREP: (
        "VERIFY_REGEX_SHELL_QUOTING_MATCHED_TARGET_AND_EXCLUDED_FILES",
        "PROVE_EFFECTIVE_CONFIG_SEMANTICS_NOT_JUST_ANY_TEXT_MATCH",
        "CONFIRM_SOURCE_VERSION_FALSE_POSITIVE_AND_NEGATIVE_CONTROLS",
    ),
    FIND: (
        "VERIFY_ROOT_PATH_AND_RECURSION_SCOPE_EXIST_IN_APPROVED_SOURCE",
        "PROVE_MATCH_COUNT_GREATER_THAN_ZERO_NOT_JUST_FIND_EXIT_ZERO",
        "REVIEW_FILES_FOR_REQUIRED_CONTENT_AND_EXPECTED_CONTROL_CONTRACT",
    ),
    GIT: (
        "VERIFY_REPOSITORY_REVISION_IS_APPROVED_AND_ATTESTED",
        "DISTINGUISH_TRACKED_FILE_OR_COMMIT_EXISTENCE_FROM_CONTROL_PROOF",
        "BIND_RELEVANT_SOURCE_AND_PLAN_HASH_TO_INDEPENDENT_REVIEWED_BASELINE",
    ),
    JQ: (
        "VERIFY_INPUT_DOCUMENT_CUSTODY_SCHEMA_SOURCE_AND_OWNER_APPROVAL",
        "DO_NOT_TRUST_SELF_DECLARED_APPROVED_TRUE_FIELDS_AS_SIGNATURES",
        "CORRELATE_ACTUAL_WAF_SCOPE_WINDOW_REQUEST_LIMITS_AND_TEST_AUTHORIZATION",
    ),
}
CASE_SPECIAL_CHECKS = {
    "AZ-T15-01": "CHECK_NESTED_QUOTE_REGEX_MATCHES_INTENDED_AZURERM_BACKEND_BLOCK",
    "AZ-T20-13": "VERIFY_TLS_IGNORE_HTTP_ERRORS_IS_DISABLED_NOT_JUST_PRESENT",
    "AZ-T20-11": "VERIFY_HTTP_EXPECTATIONS_ARE_EFFECTIVE_RUNTIME_ASSERTIONS",
    "AZ-T45-05": "MATCH_GIT_SHA_TO_SIGNED_PLAN_GENERATION_SOURCE_REVISION",
    "AZ-T69-03": "VERIFY_TICKET_AUTHORITY_EXACT_TARGET_OWNER_AND_TEST_WINDOW",
}
SHELL_META = frozenset(";&|<>")


def categorize(command: str) -> str:
    """Read syntax, not the filesystem or tool output; reject shell complexity."""
    if not isinstance(command, str) or not command.strip():
        raise TriageError("blank assertion command")
    if "$" in command or "\x60" in command or "\n" in command:
        raise TriageError("source shell expansion requires higher priority review")
    try:
        lex = shlex.shlex(command, posix=True, punctuation_chars=";&|<>")
        lex.whitespace_split = True
        lex.commenters = ""
        tokens = list(lex)
    except ValueError as exc:
        raise TriageError("assertion command cannot be lexed") from exc
    if not tokens or any(t and set(t) <= SHELL_META for t in tokens):
        raise TriageError("shell operator belongs to higher priority class")
    group = {"grep": GREP, "find": FIND, "git": GIT, "jq": JQ}.get(tokens[0])
    if group is None:
        raise TriageError("unexpected assertion command family")
    if group == JQ and "-e" not in tokens:
        raise TriageError("jq predicate must have explicit -e exit check")
    if group == GREP and not any(x == "-R" or x.startswith("-R") for x in tokens[1:]):
        raise TriageError("grep source scan recursion semantics changed")
    return group


def build_review(root: Path = ROOT, *, include_cases: bool = True) -> dict:
    root = Path(root)
    upstream = make_queue(root, include_cases=True)
    if upstream["status"] != "REVIEW_PRIORITIES_ONLY" or upstream["local_candidate_cases"] != 464:
        raise TriageError("incomplete inherited local classification")
    targets = {ident: row for ident, row in upstream["cases"].items()
               if row["review_priority"] == PRIORITY_ASSERTION}
    if set(targets) != set(EXPECTED):
        raise TriageError("nineteen fixed assertion ID membership changed")
    source = load_sources(root)
    out = {}
    counts = Counter()
    phases = defaultdict(Counter)
    for ident, row in sorted(targets.items()):
        rec = source.get(ident)
        if not rec or digest_case(rec) != row["contract_sha256"]:
            raise TriageError("frozen assertion fingerprint mismatch")
        priority, reasons = inspect_command(
            rec["command"], row["command_family"], [])
        if priority != PRIORITY_ASSERTION or reasons != [] or row["review_reason_codes"] != []:
            raise TriageError("case no longer belongs to simple lexical assertion group")
        category = categorize(rec["command"])
        if category != EXPECTED[ident]:
            raise TriageError("original source assertion group changed")
        counts[category] += 1
        phases[row["canonical_source"]][category] += 1
        out[ident] = {
            "canonical_source": row["canonical_source"],
            "contract_sha256": row["contract_sha256"],
            "command_family": row["command_family"],
            "semantic_review_class": category,
            "review_checklist": list(CHECKS[category]),
            "additional_case_specific_check": CASE_SPECIAL_CHECKS.get(ident),
            "source_control_contract_verified": False,
            "approved_source_revision_verified": False,
            "input_custody_and_signatures_verified": False,
            "effective_assertion_semantics_verified": False,
            "owner_authorized_command_execution": False,
            "original_command_executed": False,
            "reviewer1_signed": False,
            "reviewer2_signed": False,
            "azure_live_acceptance": "NOT_READY",
        }
    if len(out) != 19 or dict(counts) != EXPECTED_COUNTS:
        raise TriageError("P3 source assertion coverage changed")
    return {
        "schema": SCHEMA,
        "status": "ASSERTION_SEMANTICS_REVIEW_ONLY",
        "frozen_case_count": 1716,
        "local_case_count": 464,
        "simple_assertion_cases": 19,
        "review_class_counts": {key: counts[key] for key in GROUPS},
        "source_group_counts": {rel: {key: groups[key] for key in GROUPS}
                                for rel, groups in sorted(phases.items())},
        "original_commands_executed": 0,
        "independent_approval_signatures": 0,
        "approved_input_bytes_inspected": 0,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "limitations": [
            "Lexically simple commands are not execution-authorized or independently verified",
            "grep presence cannot prove enabled policy or absence of insecure alternatives",
            "find exit status may be zero with zero matching files",
            "git tracking or SHA alone does not prove approved source-to-plan lineage",
            "self-declared JSON approval flags are not reviewer signatures or WAF authorization",
            "No original command or actual input bytes were evaluated",
        ],
        **({"cases": out} if include_cases else {}),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path)
    p.add_argument("--summary-only", action="store_true")
    p.add_argument("--strict", action="store_true")
    a = p.parse_args(argv)
    try:
        report = build_review(a.root, include_cases=not a.summary_only)
        if a.out:
            a.out.parent.mkdir(parents=True, exist_ok=True)
            a.out.write_text(json.dumps(report, sort_keys=True, ensure_ascii=False,
                                        indent=2) + "\n", encoding="utf-8")
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(json.dumps({"status": "ASSERTION_SOURCE_REVIEW_BLOCKED",
                          "error_type": type(exc).__name__,
                          "azure_live_passes": 0, "release_decision": "NO_GO"}))
        return 1
    print(json.dumps({k: v for k, v in report.items() if k != "cases"},
                     ensure_ascii=False, indent=2, sort_keys=True))
    return 2 if a.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
