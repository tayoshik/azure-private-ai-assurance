#!/usr/bin/env python3
"""Phase 4 (AZ-T33..45) offline guard; never authorizes Azure acceptance.

The frozen 286-case Japanese source is required for source-specific selftests.
An English translation alone is not a replacement for its 143 rule definitions.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "specs/phase4_286.json"
CASE_ID = re.compile(r"^AZ-T(\d{2})-(\d{2})$")
EXPECTED = {f"AZ-T{step:02}-{slot:02}" for step in range(33, 46) for slot in range(1, 23)}
RULES = {"eq", "is_true", "is_false", "nonempty", "minimum", "private_ip"}
RELEASE = "NO_GO"


def verdict(rule, arguments, value):
    """Strict, synthetic-only predicate result; never a production verdict."""
    if value is None:
        return "NOT_READY"
    if not isinstance(arguments, dict) or rule not in RULES:
        return "NOT_READY"
    if rule == "eq":
        expected = arguments.get("expected")
        if expected is None:
            return "NOT_READY"
        return "MATCH" if type(value) is type(expected) and value == expected else "MISMATCH"
    if rule == "is_true":
        return "MATCH" if value is True else "MISMATCH"
    if rule == "is_false":
        return "MATCH" if value is False else "MISMATCH"
    if rule == "nonempty":
        return "MATCH" if type(value) in (str, list, dict) and bool(value) else "MISMATCH"
    if rule == "minimum":
        expected = arguments.get("expected")
        if (type(value) not in (int, float) or type(expected) not in (int, float)
                or not math.isfinite(value) or not math.isfinite(expected)):
            return "NOT_READY"
        return "MATCH" if value >= expected else "MISMATCH"
    if rule == "private_ip":
        try:
            if not isinstance(value, str) or not isinstance(arguments.get("subnet"), str):
                return "NOT_READY"
            addr = ipaddress.ip_address(value)
            subnet = ipaddress.ip_network(arguments["subnet"], strict=True)
            if addr.version != subnet.version:
                return "MISMATCH"
            return "MATCH" if addr.is_private and addr in subnet else "MISMATCH"
        except (ValueError, TypeError):
            return "NOT_READY"
    return "NOT_READY"


def load_source(path=SOURCE):
    """Enforce full 286-case / 143-control identity before using any rule."""
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(doc, dict) or doc.get("schema") != "azure-phase4-286/v1":
        raise ValueError("source schema not approved")
    controls, tests = doc.get("controls"), doc.get("tests")
    if not isinstance(controls, list) or not isinstance(tests, list):
        raise ValueError("controls/tests arrays missing")
    if len(controls) != 143 or len(tests) != 286 or doc.get("live_azure_successes") != 0:
        raise ValueError("source counts or live-acceptance claims invalid")
    if any(not isinstance(x, dict) for x in controls + tests):
        raise ValueError("non-object source rows")
    by_control = {}
    for row in controls:
        ident = row.get("control_id")
        match = CASE_ID.fullmatch(ident) if isinstance(ident, str) else None
        if not match or int(match[2]) % 2 == 0 or ident in by_control:
            raise ValueError(f"invalid/duplicate control ID: {ident!r}")
        if row.get("step") != int(match[1]) or row.get("rule_type") not in RULES:
            raise ValueError(f"invalid control step/predicate: {ident}")
        if not isinstance(row.get("rule_args"), dict):
            raise ValueError(f"missing rule args: {ident}")
        by_control[ident] = row
    expected_controls = {f"AZ-T{s:02}-{i:02}" for s in range(33, 46)
                         for i in range(1, 23, 2)}
    if set(by_control) != expected_controls:
        raise ValueError("143 control identities incomplete")
    by_case = {}
    for row in tests:
        ident = row.get("id")
        match = CASE_ID.fullmatch(ident) if isinstance(ident, str) else None
        if not match or ident not in EXPECTED or ident in by_case:
            raise ValueError(f"invalid/duplicate case ID: {ident!r}")
        control_id = f"AZ-T{match[1]}-{int(match[2]) - (int(match[2]) % 2 == 0):02}"
        if (control_id not in by_control
            or str(row.get("step")) != str(int(match[1]))
            or row.get("status") != "未実行"
            or not isinstance(row.get("command"), str)
            or not row["command"].strip()
            or not row.get("expected") or not row.get("evidence")
            or not row.get("procedure")):
            raise ValueError(f"incomplete or unapproved row: {ident}")
        by_case[ident] = row
    if set(by_case) != EXPECTED:
        raise ValueError("286 canonical case IDs incomplete")
    return by_control, by_case


def selftest(controls, cases, requested):
    if requested == "ALL":
        ids = sorted(EXPECTED)
    elif requested in EXPECTED:
        ids = [requested]
    else:
        return {"result": "NOT_READY", "reason": "unknown test ID",
                "azure_live_passes": 0}, 2
    errors = []
    for ident in ids:
        match = CASE_ID.fullmatch(ident)
        slot = int(match[2])
        control_id = f"AZ-T{match[1]}-{slot - (slot % 2 == 0):02}"
        c = controls[control_id]
        value = c["good_fixture"] if slot % 2 else c["bad_fixture"]
        actual = verdict(c["rule_type"], c["rule_args"], value)
        expected = "MATCH" if slot % 2 else "MISMATCH"
        if actual != expected:
            errors.append(f"{ident}: expected {expected}, got {actual}")
        if verdict(c["rule_type"], c["rule_args"], None) != "NOT_READY":
            errors.append(f"{ident}: null fixture was not rejected")
    return ({
        "execution_class": "OFFLINE_SYNTHETIC_ONLY",
        "case_labels_tested": len(ids),
        "synthetic_checks_succeeded": len(ids) - len({x.split(":")[0] for x in errors}),
        "errors": errors[:20],
        "azure_live_passes": 0,
        "release_decision": RELEASE,
        "result": "SELFTEST_PASS" if not errors else "SELFTEST_FAIL",
        "limitations": "Synthetic fixtures are not deployed Azure controls or approved evidence",
    }, 0 if not errors else 1)


def review_observation(controls, case_id, evidence_path):
    if case_id not in EXPECTED or int(case_id[-2:]) % 2 == 0:
        return {"result": "NOT_READY", "reason": "unknown or synthetic-only ID"}, 2
    if not evidence_path:
        return {"result": "NOT_READY", "reason": "missing --observation"}, 2
    try:
        evidence = json.loads(Path(evidence_path).read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {"result": "NOT_READY", "reason": "observation unreadable"}, 2
    if not isinstance(evidence, dict):
        return {"result": "NOT_READY", "reason": "observation not a JSON object"}, 2
    keys = ("source", "resource_id", "collected_at_utc", "baseline_id", "reviewer")
    if any(not isinstance(evidence.get(k), str) or not evidence[k].strip() for k in keys):
        return {"result": "NOT_READY", "reason": "provenance incomplete"}, 2
    if (evidence.get("synthetic") is True or evidence.get("fixture") is True
        or "synthetic" in evidence["source"].lower()
        or "synthetic" in evidence["baseline_id"].lower()
        or evidence.get("observation") is None):
        return {"result": "NOT_READY", "reason": "synthetic or missing observation"}, 2
    match = CASE_ID.fullmatch(case_id)
    control_id = f"AZ-T{match[1]}-{int(match[2]):02}"
    rule = controls[control_id]
    result = verdict(rule["rule_type"], rule["rule_args"], evidence["observation"])
    state = {"MATCH": "REVIEW_REQUIRED", "MISMATCH": "DIFFERENCE_REVIEW_REQUIRED",
             "NOT_READY": "NOT_READY"}[result]
    return ({
        "result": state,
        "predicate": result,
        "reason": "unsigned local evidence; independent Azure observation and approval required",
    }, 2)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", metavar="TEST_ID_OR_ALL")
    modes.add_argument("--evaluate", metavar="TEST_ID")
    parser.add_argument("--spec", type=Path, default=SOURCE)
    parser.add_argument("--observation", type=Path)
    args = parser.parse_args(argv)
    try:
        controls, cases = load_source(args.spec)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"result": "NOT_READY",
                          "reason": "frozen Phase 4 source unavailable/invalid",
                          "azure_live_passes": 0, "release_decision": RELEASE}))
        return 2
    if args.selftest:
        output, status = selftest(controls, cases, args.selftest)
    else:
        output, status = review_observation(controls, args.evaluate, args.observation)
    output["azure_live_passes"] = 0
    output["release_decision"] = RELEASE
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
