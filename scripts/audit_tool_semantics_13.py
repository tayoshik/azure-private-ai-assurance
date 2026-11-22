#!/usr/bin/env python3
"""Review thirteen local tool semantics from immutable original case definitions.

This is metadata-only. No canonical command, external tool, fixture, network,
provider, Azure resource or private input is executed, read or approved.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import shlex

from build_execution_route_1716 import ROOT, digest_case
from triage_local_464 import PRIORITY_TOOL, TriageError, inspect_command, make_queue

SCHEMA = "azure-local-p2-13-tool-semantics-review/v1"
INIT = "TERRAFORM_INIT_BACKEND_AND_PROVIDER_RISK"
PROVIDERS = "TERRAFORM_PROVIDERS_DISCOVERY"
FMT = "TERRAFORM_FMT_SOURCE_STYLE_ONLY"
VALIDATE = "TERRAFORM_VALIDATE_INITIALIZATION_REQUIRED"
TFLINT = "TFLINT_CONFIG_PLUGIN_AND_RULESET"
CHECKOV = "CHECKOV_POLICY_SEVERITY_AND_EXCEPTIONS"
NODE = "NODE_VERSION_PINNING"
PY_NEGATIVE = "PYTHON_SYNTHETIC_NEGATIVE_FIXTURE"
GROUPS = (INIT, PROVIDERS, FMT, VALIDATE, TFLINT, CHECKOV, NODE, PY_NEGATIVE)
EXPECTED = {
    "AZ-T14-13": PROVIDERS,
    "AZ-T15-17": INIT,
    "AZ-T16-01": FMT,
    "AZ-T16-03": VALIDATE,
    "AZ-T16-07": TFLINT,
    "AZ-T16-09": CHECKOV,
    "AZ-T20-03": NODE,
    "AZ-T44-05": FMT,
    "AZ-T44-07": VALIDATE,
    "AZ-T44-11": TFLINT,
    "AZ-T44-13": CHECKOV,
    "AZ-T74-01": PY_NEGATIVE,
    "AZ-T74-03": PY_NEGATIVE,
}
EXPECTED_COUNTS = {INIT: 1, PROVIDERS: 1, FMT: 2, VALIDATE: 2,
                   TFLINT: 2, CHECKOV: 2, NODE: 1, PY_NEGATIVE: 2}
SOURCES = (
    "specs/english_tests_001_440.json", "specs/phase3_264_en.json",
    "specs/phase4_286_en.json", "specs/phase5_286_en.json",
    "specs/phase6_220_en.json", "specs/phase7_220_en.json",
)
REVIEW_CHECKS = {
    INIT: (
        "REVIEW_BACKEND_CONFIGURATION_AND_PROVIDER_INSTALL_NETWORK_BEHAVIOR",
        "PROHIBIT_UNAUTHORIZED_BACKEND_ACCESS_OR_DOWNLOADS",
        "REQUIRE_APPROVED_ISOLATED_RUNNER_AND_PINNED_PROVIDER_LOCKFILE",
        "VERIFY_EXIT_STATUS_AND_BACKENDLESS_ALTERNATIVE_IF_ACCEPTED",
    ),
    PROVIDERS: (
        "VERIFY_SOURCE_REVISION_LOCKFILE_AND_PROVIDER_VERSION_CONSTRAINTS",
        "REVIEW_PROVIDER_DISCOVERY_SCOPE_NO_IMPLIED_AZURE_ACCEPTANCE",
        "CONFIRM_OUTPUT_AGAINST_SIGNED_COMPATIBILITY_BASELINE",
    ),
    FMT: (
        "VERIFY_SOURCE_REVISION_AND_FORMATTER_PINNED_VERSION",
        "DISTINGUISH_STYLE_ONLY_FROM_SECURITY_OR_LIVE_ACCEPTANCE",
        "REVIEW_NONMUTATING_CHECK_FLAG_AND_EXPECTED_ERROR_SEMANTICS",
    ),
    VALIDATE: (
        "REQUIRE_APPROVED_PREINITIALIZED_PROVIDER_AND_BACKEND_CONTEXT",
        "DO_NOT_INFER_PROVIDER_DOWNLOAD_OR_REMOTE_ACCESS_IS_AUTHORIZED",
        "DISTINGUISH_STATIC_HCL_VALIDITY_FROM_LIVE_AZURE_POLICY_STATE",
    ),
    TFLINT: (
        "REVIEW_PLUGIN_DOWNLOADS_VERSION_PINS_AND_RULESET_CONFIGURATION",
        "VERIFY_SEVERITY_EXCLUSIONS_AND_BASELINE_EXCEPTION_APPROVAL",
        "DISTINGUISH_LINT_EXIT_ZERO_FROM_COMPLETE_CONTROL_COVERAGE",
    ),
    CHECKOV: (
        "REVIEW_SCAN_SCOPE_POLICY_VERSION_SEVERITY_AND_SKIPPED_CHECKS",
        "REVIEW_NO_EXTERNAL_MODULE_DOWNLOAD_OR_UNAPPROVED_NETWORK_ACCESS",
        "VERIFY_APPROVED_FINDINGS_BASELINE_AND_EXCEPTION_OWNER",
    ),
    NODE: (
        "COMPARE_REPORTED_TOOL_VERSION_TO_SIGNED_VERSION_REQUIREMENT",
        "VERIFY_APPROVED_SOURCE_AND_TOOL_CHAIN_NOT_JUST_EXIT_ZERO",
        "NEVER_CREDIT_LOCAL_TOOL_VERSION_AS_LIVE_AZURE_ACCEPTANCE",
    ),
    PY_NEGATIVE: (
        "PIN_REPOSITORY_SOURCE_AND_SYNTHETIC_FIXTURE_SHA256",
        "REVIEW_EXPECT_FAIL_NEGATIVE_ASSERTION_AND_FALSE_POSITIVE_CONTROLS",
        "DO_NOT_COUNT_REJECTED_SYNTHETIC_PLAN_AS_REAL_AZURE_PLAN_REJECTION",
    ),
}
NETWORK_CONTEXT = frozenset({INIT, VALIDATE, TFLINT, CHECKOV})
SHELL_PUNCTUATION = frozenset(";&|<>")
ALLOWED_PY_FIXTURES = frozenset({
    "fixtures/plan_app_pna_true.json", "fixtures/plan_nsg_any.json",
})


def categorize(command: str) -> str:
    """Classify syntax of known commands, never invoke them or authorize execution."""
    if not isinstance(command, str) or not command.strip():
        raise TriageError("empty tool command")
    if "$" in command or "\x60" in command or "\n" in command:
        raise TriageError("unexpected expansion or multiline command")
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|<>")
        lexer.whitespace_split = True
        lexer.commenters = ""
        tokens = list(lexer)
    except ValueError as exc:
        raise TriageError("tool command lexical ambiguity") from exc
    if not tokens or any(t and set(t) <= SHELL_PUNCTUATION for t in tokens):
        raise TriageError("compound or redirected command cannot remain in P2")
    tool = tokens[0]
    if tool == "terraform":
        args = [t for t in tokens[1:] if not t.startswith("-chdir=")]
        if not args:
            raise TriageError("terraform operation absent")
        op = args[0]
        mapping = {"init": INIT, "providers": PROVIDERS, "fmt": FMT,
                   "validate": VALIDATE}
        if op not in mapping:
            raise TriageError("unexpected terraform operation")
        return mapping[op]
    if tool == "tflint":
        return TFLINT
    if tool == "checkov":
        return CHECKOV
    if tool == "node" and tokens == ["node", "--version"]:
        return NODE
    if tool == "python3":
        if (len(tokens) != 6 or tokens[1] != "scripts/phase7_plan_policy.py" or
                tokens[2] != "--plan" or tokens[3] not in ALLOWED_PY_FIXTURES or
                tokens[4:] != ["--expect", "Fail"]):
            raise TriageError("unknown python fixture semantics")
        return PY_NEGATIVE
    raise TriageError("unrecognized tool or unverified command contract")


def load_sources(root: Path) -> dict:
    cases = {}
    for rel in SOURCES:
        try:
            data = json.loads((root / rel).read_text(encoding="utf-8"))
            records = data["cases"] if "cases" in data else data["tests"]
            if not isinstance(records, list):
                raise TriageError("canonical records are not a list")
        except (OSError, KeyError, ValueError, TypeError) as exc:
            raise TriageError("canonical source unavailable") from exc
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("id"), str):
                raise TriageError("malformed frozen record")
            ident = record["id"]
            if ident in cases:
                raise TriageError("duplicate source ID")
            cases[ident] = record
    return cases


def build_review(root: Path = ROOT, *, include_cases: bool = True) -> dict:
    root = Path(root)
    upstream = make_queue(root, include_cases=True)
    if upstream["status"] != "REVIEW_PRIORITIES_ONLY" or upstream["local_candidate_cases"] != 464:
        raise TriageError("parent source-only inventory invalid")
    target = {i: v for i, v in upstream["cases"].items()
              if v["review_priority"] == PRIORITY_TOOL}
    if set(target) != set(EXPECTED):
        raise TriageError("the original thirteen tool IDs changed")
    cases = load_sources(root)
    details = {}
    counts = Counter()
    phase_counts = defaultdict(Counter)
    for ident, original in sorted(target.items()):
        source = cases.get(ident)
        if source is None or digest_case(source) != original["contract_sha256"]:
            raise TriageError("frozen tool case contract mismatch")
        if original["review_reason_codes"] != ["IMPLEMENTATION_OR_TOOL_SEMANTICS"]:
            raise TriageError("tool-only risk assumptions changed")
        group = categorize(source["command"])
        if group != EXPECTED[ident]:
            raise TriageError("tool operation changed from approved review mapping")
        # Validate route classification a second time; never infer execution readiness.
        priority, _ = inspect_command(source["command"], original["command_family"], [])
        if priority != PRIORITY_TOOL:
            raise TriageError("case no longer belongs to source-only tool review")
        counts[group] += 1
        phase_counts[original["canonical_source"]][group] += 1
        details[ident] = {
            "canonical_source": original["canonical_source"],
            "contract_sha256": original["contract_sha256"],
            "command_family": original["command_family"],
            "tool_semantics_group": group,
            "review_checks": list(REVIEW_CHECKS[group]),
            "possible_network_or_dependency_side_effects": group in NETWORK_CONTEXT,
            "owner_approved_execution_environment": False,
            "network_and_backend_approval_verified": False,
            "pinned_toolchain_and_source_verified": False,
            "assertion_semantics_verified": False,
            "approved_evidence_verified": False,
            "reviewer1_signed": False,
            "reviewer2_signed": False,
            "original_command_executed": False,
            "azure_live_acceptance": "NOT_READY",
        }
    if len(details) != 13 or dict(counts) != {k: v for k, v in EXPECTED_COUNTS.items()}:
        raise TriageError("tool semantics coverage or counts changed")
    return {
        "schema": SCHEMA,
        "status": "TOOL_SEMANTICS_REVIEW_ONLY",
        "original_frozen_case_count": 1716,
        "local_parent_cases": 464,
        "tool_review_cases": 13,
        "group_counts": {k: counts[k] for k in GROUPS},
        "source_group_counts": {p: {k: n[k] for k in GROUPS}
                                for p, n in sorted(phase_counts.items())},
        "original_commands_executed": 0,
        "approved_tool_environments_verified": 0,
        "approved_evidence_verified": 0,
        "independent_review_signatures": 0,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "limitations": [
            "Source and command syntax review does not execute or verify any original test",
            "Terraform init may download provider plugins or access configured remote backend",
            "Lint and static tooling can depend on extensions, plugins and configuration",
            "A synthetic negative fixture success is not independent live Azure evidence",
            "No checklist item grants execution permission or advances live acceptance",
        ],
        **({"cases": details} if include_cases else {}),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path)
    p.add_argument("--summary-only", action="store_true")
    p.add_argument("--strict", action="store_true",
                   help="always deny live acceptance with exit status 2")
    a = p.parse_args(argv)
    try:
        report = build_review(a.root, include_cases=not a.summary_only)
        if a.out:
            a.out.parent.mkdir(parents=True, exist_ok=True)
            a.out.write_text(json.dumps(report, sort_keys=True, indent=2,
                                        ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "TOOL_SEMANTICS_SOURCE_BLOCKED",
                          "error_type": type(exc).__name__,
                          "azure_live_passes": 0,
                          "release_decision": "NO_GO"}, sort_keys=True))
        return 1
    print(json.dumps({k: v for k, v in report.items() if k != "cases"},
                     ensure_ascii=False, indent=2, sort_keys=True))
    return 2 if a.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
