#!/usr/bin/env python3
"""Phase 2 offline detector and review-only evidence triage.

This command has no Azure network calls. It NEVER issues Azure acceptance PASS
or authoritative FAIL from unsigned/unauthenticated local JSON.
"""
from __future__ import annotations
import argparse
from datetime import datetime
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {f"AZ-T{s:02d}-{n:02d}" for s in range(11, 21) for n in range(1, 23)}
SHA = re.compile(r"^[0-9a-f]{64}$")


def equal_typed(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(equal_typed(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(equal_typed(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and (not math.isfinite(a) or not math.isfinite(b)):
        return False
    return a == b


def compare(observed, approved):
    if observed is None or approved is None:
        return "NOT_READY"
    return "MATCH" if equal_typed(observed, approved) else "MISMATCH"


def load_spec(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    tests = data.get("tests")
    if not isinstance(tests, list) or len(tests) != 220:
        raise ValueError("Phase 2 source must contain exactly 220 tests")
    if any(not isinstance(x, dict) for x in tests):
        raise ValueError("non-object test case")
    ids = [x.get("id") for x in tests]
    if len(set(ids)) != 220 or set(ids) != EXPECTED:
        raise ValueError("Phase 2 canonical IDs incomplete or duplicated")
    for row in tests:
        if str(row.get("step")) != str(int(row["id"][4:6])):
            raise ValueError("step/test ID mismatch")
        if not isinstance(row.get("command"), str) or not row["command"].strip():
            raise ValueError("missing command")
        if row.get("azure_live_pass") is True:
            raise ValueError("unapproved live Azure PASS in source")
    return data


def selftest(test_id):
    observed = [
        compare({"flag": True, "items": [1, "ok"]}, {"flag": True, "items": [1, "ok"]}),
        compare({"flag": 1}, {"flag": True}),
        compare(None, {"flag": True}),
    ]
    return {"test_id": test_id, "synthetic": True, "outcomes": observed,
            "status": "SELFTEST_PASS" if observed == ["MATCH", "MISMATCH", "NOT_READY"] else "SELFTEST_FAIL",
            "azure_live_pass": False}


def triage(evidence):
    if not isinstance(evidence, dict) or evidence.get("fixture") is not False or evidence.get("synthetic") is True:
        return "NOT_READY", "synthetic, unmarked or missing input"
    for key in ("asset_id", "collector", "collected_at", "source_sha256", "baseline_sha256", "authorization_ticket"):
        if not isinstance(evidence.get(key), str) or not evidence[key].strip():
            return "NOT_READY", "required provenance field missing"
    if not SHA.fullmatch(evidence["source_sha256"]) or not SHA.fullmatch(evidence["baseline_sha256"]):
        return "NOT_READY", "malformed digest"
    try:
        stamp = datetime.fromisoformat(evidence["collected_at"].replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            return "NOT_READY", "timestamp timezone missing"
    except ValueError:
        return "NOT_READY", "invalid timestamp"
    if "observed" not in evidence or "approved" not in evidence:
        return "NOT_READY", "observed/approved data missing"
    outcome = compare(evidence["observed"], evidence["approved"])
    if outcome == "NOT_READY":
        return "NOT_READY", "observed/approved data missing"
    if outcome == "MATCH":
        return "REVIEW_REQUIRED", "value equality is not independent acceptance"
    return "DIFFERENCE_REVIEW_REQUIRED", "external verification needed before authoritative FAIL"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--selftest", metavar="ID_OR_ALL")
    mode.add_argument("--check", metavar="TEST_ID")
    p.add_argument("--spec", default=str(ROOT / "specs/phase2_220.json"))
    p.add_argument("--evidence")
    args = p.parse_args(argv)
    try:
        spec = load_spec(args.spec)
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps({"result": "NOT_READY", "reason": "Phase 2 canonical source missing or invalid",
                          "azure_live_passes": 0}))
        return 2
    if args.selftest:
        ids = (sorted(x for x in EXPECTED if int(x[-2:]) % 2 == 0) if args.selftest == "ALL" else [args.selftest])
        if any(x not in EXPECTED or int(x[-2:]) % 2 for x in ids):
            print(json.dumps({"result": "NOT_READY", "reason": "unknown or non-synthetic test ID",
                              "azure_live_passes": 0}))
            return 2
        result = [selftest(x) for x in ids]
        succeeded = all(x["status"] == "SELFTEST_PASS" for x in result)
        print(json.dumps({"execution_class": "OFFLINE_DETECTOR", "synthetic_cases": len(ids),
                          "selftest_pass": sum(x["status"] == "SELFTEST_PASS" for x in result),
                          "azure_live_passes": 0, "accepted_azure_cases": 0,
                          "result": "SELFTEST_PASS" if succeeded else "SELFTEST_FAIL"}, sort_keys=True))
        return 0 if succeeded else 1
    if args.check not in EXPECTED or int(args.check[-2:]) % 2 == 0:
        print(json.dumps({"result": "NOT_READY", "reason": "unknown or synthetic-only test ID",
                          "azure_live_passes": 0}))
        return 2
    try:
        if not args.evidence:
            raise ValueError("missing evidence path")
        evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        print(json.dumps({"result": "NOT_READY", "reason": "evidence missing or invalid",
                          "azure_live_passes": 0}))
        return 2
    result, reason = triage(evidence)
    print(json.dumps({"test_id": args.check, "result": result, "reason": reason,
                      "scope": "UNTRUSTED_LOCAL_VALUE_COMPARISON",
                      "azure_live_passes": 0, "accepted_azure_cases": 0}, sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
