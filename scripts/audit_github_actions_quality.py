#!/usr/bin/env python3
"""Read-only GitHub Actions workflow context / trigger / Ruleset guard audit.

Source-only. Does not call GitHub API, execute workflows, or perform Azure tests.
A valid workflow audit is NOT evidence of application or live Azure acceptance.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ".github/workflows"
EXPECTED_MIN_WORKFLOWS = 35
EXPECTED_MIN_JOBS = 37
CHECKOUT = "actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd"
REQUIRED_GATES = {
    "offline-main-gate": {
        "workflow": "offline-validation.yml",
        "commands": ("python3 scripts/validate_package.py",
                     "python3 -m unittest discover -s tests -v"),
    },
    "offline-catalogue": {
        "workflow": "publication-integrity.yml",
        "commands": ("python3 scripts/verify_publication.py",
                     "python3 -m unittest discover -s tests -p 'test_publication*.py' -v"),
    },
}
SCOPED_JOBS = {
    "terraform-stage3-identity-vault-static.yml": "stage3-identity-vault-contracts",
    "terraform-stage5-webapp-static.yml": "stage5-webapp-contracts",
    "terraform-stage6-gateway-static.yml": "stage6-gateway-contracts",
    "azure-monitor-private-link-offline.yml": "monitor-private-link-offline",
}
MANUAL_ONLY = {"terraform-stage4-provider-validate.yml"}


def events_of(source: str) -> dict[str, list[str]]:
    """Parse only top-level YAML event lines, not general-purpose YAML."""
    lines = source.splitlines()
    try:
        start = lines.index("on:")
    except ValueError:
        return {}
    result: dict[str, list[str]] = {}
    current = None
    for line in lines[start + 1:]:
        if line and not line[0].isspace() and not line.startswith("#"):
            break
        if line.startswith("  ") and not line.startswith("    "):
            matched = re.fullmatch(r"  ([a-z_]+):(?:\s*.*)?", line)
            if matched:
                current = matched[1]
                result[current] = []
                continue
        if current:
            result[current].append(line)
    return result


def event_paths(lines: list[str]) -> list[str]:
    paths = []
    in_paths = False
    for line in lines:
        if line.strip() == "paths:" and line.startswith("    "):
            in_paths = True
        elif in_paths:
            m = re.fullmatch(r"\s{6}- ['\"]([^'\"]+)['\"]", line)
            if m:
                paths.append(m[1])
            elif line.strip() and not line.startswith("      "):
                in_paths = False
    return paths


def job_ids(source: str) -> list[str]:
    body = source.split("\njobs:\n", 1)
    if len(body) != 2:
        return []
    return re.findall(r"(?m)^  ([a-zA-Z][a-zA-Z0-9_-]*):\s*$", body[1])


def inspect(root: Path = ROOT, *, include_workflows: bool = True) -> dict:
    root = Path(root)
    errors: list[str] = []
    warnings: list[str] = []
    files = sorted((root / WORKFLOWS).glob("*.yml"))
    if len(files) < EXPECTED_MIN_WORKFLOWS:
        errors.append("workflow inventory unexpectedly shrank below reviewed baseline")
    workflows = {}
    job_owners: dict[str, list[str]] = defaultdict(list)
    unpinned_action_files = []
    unscoped_push_files = []
    for path in files:
        name = path.name
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(name + ": unreadable workflow")
            continue
        gates = events_of(source)
        jobs = job_ids(source)
        if not gates:
            errors.append(name + ": no YAML event triggers")
        if not jobs:
            errors.append(name + ": no job IDs")
        if not re.search(r"(?m)^permissions:\s*\n  contents: read\s*$", source):
            errors.append(name + ": missing explicit top-level contents: read permission")
        if any(e in gates for e in ("pull_request_target", "workflow_run")):
            errors.append(name + ": privileged trigger not allowed in offline workflows")
        if re.search(r"(?m)^\s+contents:\s*write\s*$", source):
            errors.append(name + ": write content permission not approved")
        action_refs = re.findall(r"(?m)^\s+- uses:\s+([^\s#]+)", source)
        if any(re.search(r"@v\d+(?:\.\d+)*$", x) for x in action_refs):
            unpinned_action_files.append(name)
        if "push" in gates and "branches: [main]" not in "\n".join(gates["push"]):
            unscoped_push_files.append(name)
        for job in jobs:
            job_owners[job].append(name)
        workflows[name] = {
            "jobs": jobs,
            "events": sorted(gates),
            "path_filtered_pull_request": bool(event_paths(gates.get("pull_request", []))),
            "path_filtered_push": bool(event_paths(gates.get("push", []))),
            "artifacts_uploaded": "actions/upload-artifact@" in source,
        }
        if name in MANUAL_ONLY and set(gates) != {"workflow_dispatch"}:
            errors.append(name + ": manual provider validation must stay dispatch-only")
        if name in SCOPED_JOBS:
            expected_job = SCOPED_JOBS[name]
            if jobs != [expected_job]:
                errors.append(name + ": unique scoped status check name changed")
            if "pull_request" not in gates or "push" not in gates:
                errors.append(name + ": both PR and main push events required")
            if "branches: [main]" not in "\n".join(gates.get("push", [])):
                errors.append(name + ": feature push must not duplicate PR check")
            push_paths = event_paths(gates.get("push", []))
            pr_paths = event_paths(gates.get("pull_request", []))
            if not push_paths or push_paths != pr_paths:
                errors.append(name + ": PR path filter must match main push path filter")
            if WORKFLOWS + "/" + name not in pr_paths:
                errors.append(name + ": workflow must trigger on its own changes")
    for job, owners in sorted(job_owners.items()):
        if len(owners) > 1:
            errors.append(f"duplicate status context {job}: {', '.join(owners)}")
    for job, rule in REQUIRED_GATES.items():
        name = rule["workflow"]
        path = root / WORKFLOWS / name
        if name not in workflows:
            errors.append(f"required Ruleset workflow missing: {name}")
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"required Ruleset workflow unreadable: {name}")
            continue
        ev = events_of(source)
        if workflows[name]["jobs"] != [job]:
            errors.append(f"{job}: required Ruleset check job ID changed")
        if "pull_request" not in ev or "push" not in ev:
            errors.append(f"{job}: must run on PR and main push")
        if event_paths(ev.get("push", [])) or event_paths(ev.get("pull_request", [])):
            errors.append(f"{job}: required check must not be path filtered")
        if "branches: [main]" not in "\n".join(ev.get("push", [])):
            errors.append(f"{job}: push must cover main")
        if "if:" in "\n".join(source.split("\njobs:\n", 1)[-1].splitlines()[:4]):
            errors.append(f"{job}: required job must not be conditional")
        if CHECKOUT not in source or not re.search(
                r"(?m)^\s+persist-credentials:\s+false\s*$", source):
            errors.append(f"{job}: credential-free full-SHA checkout required")
        if re.search(r"(?m)^\s+continue-on-error:\s+true\s*$", source):
            errors.append(f"{job}: cannot ignore failures")
        for command in rule["commands"]:
            if command not in source:
                errors.append(f"{job}: required offline command missing")
    total_jobs = sum(len(owners) for owners in job_owners.values())
    if total_jobs < EXPECTED_MIN_JOBS:
        errors.append("job count unexpectedly shrank below reviewed baseline")
    if unpinned_action_files:
        warnings.append(
            "Other workflows still have version-tag action references; follow-up full-SHA pin review needed")
    if unscoped_push_files:
        warnings.append(
            "Other workflows still push on feature branches as well as PRs; follow-up trigger normalization needed")
    return {
        "schema": "github-offline-ci-quality-audit/v1",
        "status": "INVALID_WORKFLOW_POLICY" if errors else "SOURCE_WORKFLOW_POLICY_VERIFIED_ONLY",
        "execution_class": "OFFLINE_STATIC_WORKFLOW_INSPECTION",
        "workflow_count": len(files),
        "unique_job_contexts": len(job_owners),
        "total_job_definitions": total_jobs,
        "required_ruleset_status_contexts": list(REQUIRED_GATES),
        "duplicate_status_contexts": sorted(
            {j for j, owners in job_owners.items() if len(owners) > 1}),
        "remaining_unpinned_action_workflows": sorted(unpinned_action_files),
        "remaining_unscoped_push_workflows": sorted(unscoped_push_files),
        "scope_approved": False,
        "source_workflows_executed": 0,
        "azure_live_passes_verified": 0,
        "release_decision": "NO_GO",
        "errors": errors,
        "advisories": warnings,
        "limitations": [
            "Static regex/top-level event audit, not a full YAML AST or GitHub runner",
            "Remote Ruleset settings must be checked separately through GitHub API",
            "Green static/source CI cannot certify Azure environments or release",
            "Path-filtered optional job checks must not be globally required",
        ],
        **({"workflows": workflows} if include_workflows else {}),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--summary-only", action="store_true")
    parser.add_argument("--strict", action="store_true",
                        help="deny Azure acceptance (expected exit 2)")
    args = parser.parse_args(argv)
    result = inspect(args.root, include_workflows=not args.summary_only)
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 1 if result["errors"] else (2 if args.strict else 0)


if __name__ == "__main__":
    raise SystemExit(main())
