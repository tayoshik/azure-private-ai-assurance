#!/usr/bin/env python3
"""Five focused offline checks for semantic traps in published static commands.

Inputs are UNTRUSTED local observations and user-supplied approvals.
Never interpret self-asserted equality as signed approval, Azure PASS, or GO.
No Azure CLI, Node, Terraform or browser commands are executed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

CASE_IDS = {
    "AZ-T20-13": "TLS_BYPASS_STRING_SEARCH",
    "AZ-T45-03": "PLAN_HASH_NOT_COMPARED",
    "AZ-T45-19": "REVIEWER_INDEPENDENCE_UNVERIFIED",
    "AZ-T40-11": "ARTIFACT_SOURCE_UNBOUND",
    "AZ-T45-21": "DEPLOY_EVIDENCE_UNBOUND",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
INSECURE_TLS = (
    re.compile(r"\bignoreHTTPSErrors\s*:\s*true\b", re.I),
    re.compile(r"\brejectUnauthorized\s*:\s*false\b", re.I),
    re.compile(r"\bNODE_TLS_REJECT_UNAUTHORIZED\s*=\s*['\"]?0\b", re.I),
)
MAX_TEXT = 400_000
MAX_PLAN_BYTES = 100 * 1024 * 1024


def safe_str(value, pattern=None):
    return (type(value) is str and bool(value.strip()) and len(value) <= 512
            and (pattern is None or pattern.fullmatch(value) is not None))


def hash_file(path):
    """Compute bytes of a local provided plan; never execute or disclose it."""
    if not safe_str(path):
        return None
    try:
        item = Path(path)
        if not item.is_file() or item.stat().st_size > MAX_PLAN_BYTES:
            return None
        h = hashlib.sha256()
        with item.open("rb") as f:
            for buf in iter(lambda: f.read(1024 * 1024), b""):
                h.update(buf)
        return h.hexdigest()
    except (OSError, ValueError):
        return None


def predicate(case_id, observation, approved):
    """Return mismatch/indeterminate/match *candidate*; not acceptance."""
    if case_id not in CASE_IDS or not isinstance(observation, dict) or not isinstance(approved, dict):
        return "NOT_READY", "MISSING_OR_INVALID_INPUT"
    if case_id == "AZ-T20-13":
        source = observation.get("playwright_config_text")
        if type(source) is not str or not source.strip() or len(source) > MAX_TEXT:
            return "NOT_READY", "NO_REVIEWED_PLAYWRIGHT_CONFIGURATION"
        if not safe_str(approved.get("approved_tls_hostname")):
            return "NOT_READY", "NO_APPROVED_TLS_HOSTNAME"
        if any(p.search(source) for p in INSECURE_TLS):
            return "DIFFERENCE_REVIEW_REQUIRED", "INSECURE_TLS_BYPASS_PATTERN"
        return "REVIEW_REQUIRED", "TEXT_HAS_NO_OBVIOUS_BYPASS_BUT_TLS_UNVERIFIED"
    if case_id == "AZ-T45-03":
        expected = approved.get("plan_sha256")
        if not safe_str(expected, SHA256):
            return "NOT_READY", "MISSING_APPROVED_PLAN_SHA256"
        actual = hash_file(observation.get("plan_path"))
        if actual is None:
            return "NOT_READY", "MISSING_OR_OVERSIZED_PLAN_FILE"
        return ("REVIEW_REQUIRED", "PLAN_HASH_EQUALS_UNVERIFIED_APPROVAL") if actual == expected else (
            "DIFFERENCE_REVIEW_REQUIRED", "PLAN_HASH_DIFFERS_FROM_CLAIMED_APPROVAL")
    if case_id == "AZ-T45-19":
        author, executor = observation.get("change_author"), observation.get("executor")
        reviewers = observation.get("reviewers")
        permitted = approved.get("approved_reviewer_identities")
        if (not safe_str(author) or not safe_str(executor)
            or not isinstance(reviewers, list) or len(reviewers) < 2
            or not isinstance(permitted, list) or len(permitted) < 2
            or not all(safe_str(x) for x in permitted)):
            return "NOT_READY", "REVIEWER_INPUTS_INCOMPLETE"
        ids, roles = [], []
        for person in reviewers:
            if (not isinstance(person, dict) or
                not safe_str(person.get("identity_id")) or not safe_str(person.get("role"))):
                return "NOT_READY", "REVIEWER_INPUTS_INCOMPLETE"
            ids.append(person["identity_id"])
            roles.append(person["role"])
        if (len(set(ids)) < 2 or len(set(roles)) < 2 or
            author in ids or executor in ids or not set(ids).issubset(set(permitted))):
            return "DIFFERENCE_REVIEW_REQUIRED", "UNTRUSTED_OR_NONINDEPENDENT_REVIEWER"
        return "REVIEW_REQUIRED", "REVIEWER_METADATA_MATCHES_UNVERIFIED_APPROVAL"
    if case_id in ("AZ-T40-11", "AZ-T45-21"):
        fields = ("artifact_sha256", "source_commit_sha") if case_id == "AZ-T40-11" else (
            "plan_sha256", "source_commit_sha", "executor", "change_ticket"
        )
        for key in fields:
            pattern = SHA256 if key.endswith("sha256") else COMMIT if key.endswith("sha") else None
            if not safe_str(observation.get(key), pattern) or not safe_str(approved.get(key), pattern):
                return "NOT_READY", "ARTIFACT_APPROVAL_FIELDS_INCOMPLETE"
        if any(observation[k] != approved[k] for k in fields):
            return "DIFFERENCE_REVIEW_REQUIRED", "ARTIFACT_REFERENCE_MISMATCH"
        return "REVIEW_REQUIRED", "METADATA_MATCHES_UNVERIFIED_APPROVAL"
    return "NOT_READY", "UNKNOWN_CONTROL"


def review(case_id, observation, approved):
    status, reason = predicate(case_id, observation, approved)
    return {
        "case_id": case_id,
        "finding_code": CASE_IDS.get(case_id, "UNKNOWN_CONTROL"),
        "result": status,
        "reason_code": reason,
        "independent_signer_or_approval_verified": False,
        "source_to_runtime_equivalence_verified": False,
        "live_azure_passes": 0,
        "release_decision": "NO_GO",
        "limitation": "Local comparison of user-provided observations and approvals; requires independent authenticated evidence review",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--observation", type=Path, required=True)
    parser.add_argument("--approved", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        obs = json.loads(args.observation.read_text(encoding="utf-8"))
        appr = json.loads(args.approved.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, TypeError, ValueError):
        obs, appr = None, None
    print(json.dumps(review(args.case_id, obs, appr), sort_keys=True, ensure_ascii=False))
    return 2  # Never return success for unsigned local or synthetic observations.


if __name__ == "__main__":
    raise SystemExit(main())
