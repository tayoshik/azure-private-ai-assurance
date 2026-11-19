#!/usr/bin/env python3
"""Phase 5 original-source offline detector. NEVER authorizes Azure acceptance."""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import ipaddress
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "specs/phase5_286.json"
TRANSLATION = ROOT / "specs/phase5_286_en.json"
SOURCE_SHA256 = "e1a24b145ec7bdd66f3cbe123644e9f060354c7d1aa8d93c193214122d346de3"
PHASE4_SHA256 = "b221babf4a1b7a17763723d06229e868b943748cbbf6c1b0726e8f07465fcf36"
EXPECTED = {f"AZ-T{s:02}-{n:02}" for s in range(46, 59) for n in range(1, 23)}
CONTROL_IDS = {f"AZ-T{s:02}-{n:02}" for s in range(46, 59) for n in range(1, 23, 2)}
CASE = re.compile(r"^AZ-T(\d{2})-(\d{2})$")
RULES = {"eq", "is_true", "is_false", "nonempty", "minimum", "maximum", "private_ip"}


def equal_typed(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, float) and (not math.isfinite(a) or not math.isfinite(b)):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(equal_typed(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(equal_typed(x, y) for x, y in zip(a, b))
    return a == b


def predicate(rule, args, value):
    if value is None or rule not in RULES or not isinstance(args, dict):
        return "NOT_READY"
    if rule == "eq":
        expect = args.get("expected")
        if expect is None:
            return "NOT_READY"
        return "MATCH" if equal_typed(value, expect) else "MISMATCH"
    if rule == "is_true":
        return "MATCH" if value is True else "MISMATCH"
    if rule == "is_false":
        return "MATCH" if value is False else "MISMATCH"
    if rule == "nonempty":
        return "MATCH" if type(value) in (str, list, dict) and bool(value) else "MISMATCH"
    if rule in ("minimum", "maximum"):
        expect = args.get("expected")
        if (type(value) not in (int, float) or type(expect) not in (int, float)
                or not math.isfinite(value) or not math.isfinite(expect)):
            return "NOT_READY"
        ok = value >= expect if rule == "minimum" else value <= expect
        return "MATCH" if ok else "MISMATCH"
    if rule == "private_ip":
        try:
            if not isinstance(value, str) or not isinstance(args.get("subnet"), str):
                return "NOT_READY"
            address = ipaddress.ip_address(value)
            subnet = ipaddress.ip_network(args["subnet"], strict=True)
            return "MATCH" if address.version == subnet.version and address.is_private and address in subnet else "MISMATCH"
        except (TypeError, ValueError):
            return "NOT_READY"
    return "NOT_READY"


def load_original(path=SOURCE):
    """Accept only a full source with the exact original digest, counts and IDs."""
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("Phase 5 source digest mismatch")
    doc = json.loads(raw)
    if (not isinstance(doc, dict) or doc.get("schema") != "azure-phase5-286/v1"
            or doc.get("prior_phase4_spec_sha256") != PHASE4_SHA256
            or doc.get("live_azure_tests_passed") != 0):
        raise ValueError("Phase 5 source provenance or claims invalid")
    controls, tests = doc.get("controls"), doc.get("tests")
    if not isinstance(controls, list) or not isinstance(tests, list) or len(controls) != 143 or len(tests) != 286:
        raise ValueError("143 controls and 286 cases required")
    if any(not isinstance(x, dict) for x in controls + tests):
        raise ValueError("invalid rule/case row")
    cr = {}
    for row in controls:
        cid = row.get("control_id")
        m = CASE.fullmatch(cid) if isinstance(cid, str) else None
        if (cid not in CONTROL_IDS or cid in cr or not m
                or row.get("step") != int(m[1]) or row.get("rule_type") not in RULES
                or not isinstance(row.get("rule_args"), dict)
                or "good_fixture" not in row or "bad_fixture" not in row):
            raise ValueError("invalid or duplicate control")
        cr[cid] = row
    if set(cr) != CONTROL_IDS:
        raise ValueError("incomplete source controls")
    cases = {}
    for row in tests:
        cid = row.get("id")
        m = CASE.fullmatch(cid) if isinstance(cid, str) else None
        if (cid not in EXPECTED or cid in cases or not m
                or str(row.get("step")) != str(int(m[1]))
                or row.get("status") != "未実行"
                or not isinstance(row.get("command"), str) or not row["command"].strip()
                or not row.get("expected") or not row.get("procedure") or not row.get("evidence")):
            raise ValueError("incomplete or unapproved source case")
        cases[cid] = row
    if set(cases) != EXPECTED:
        raise ValueError("incomplete Phase 5 test coverage")
    return cr, cases


def published_translation(path=TRANSLATION):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    if (not isinstance(doc, dict) or doc.get("provenance", {}).get("original_phase5_spec_sha256") != SOURCE_SHA256
            or doc.get("azure_live_passes") != 0
            or not isinstance(doc.get("tests"), list)
            or {x.get("id") for x in doc["tests"]} != EXPECTED
            or len(doc["tests"]) != 286):
        raise ValueError("English Phase 5 translation identity mismatch")
    return doc


def synthetic_check(controls, selector):
    if selector == "ALL":
        ids = sorted(EXPECTED)
    elif selector in EXPECTED:
        ids = [selector]
    else:
        return {"result": "NOT_READY", "reason": "unknown Phase 5 case", "azure_live_passes": 0}, 2
    errors = []
    for cid in ids:
        n = int(cid[-2:])
        original = f"{cid[:-2]}{n if n % 2 else n-1:02}"
        r = controls[original]
        observed = r["good_fixture"] if n % 2 else r["bad_fixture"]
        expected = "MATCH" if n % 2 else "MISMATCH"
        if predicate(r["rule_type"], r["rule_args"], observed) != expected:
            errors.append(cid + ": fixture predicate mismatch")
        if predicate(r["rule_type"], r["rule_args"], None) != "NOT_READY":
            errors.append(cid + ": missing evidence accepted")
    ok = not errors
    return {
        "result": "SELFTEST_PASS" if ok else "SELFTEST_FAIL",
        "execution_class": "OFFLINE_SYNTHETIC_ONLY",
        "case_labels_tested": len(ids),
        "synthetic_checks_succeeded": len(ids) - len(set(x.split(":")[0] for x in errors)),
        "errors": errors[:10],
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "limitations": "Synthetic fixture predicate match is NOT approved Azure live acceptance",
    }, 0 if ok else 1


def review_observation(controls, cid, path):
    if cid not in EXPECTED or int(cid[-2:]) % 2 == 0 or not path:
        return {"result": "NOT_READY", "reason": "unknown, synthetic-only or missing observation"}, 2
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {"result": "NOT_READY", "reason": "observation unreadable"}, 2
    if not isinstance(data, dict) or data.get("fixture") is not False or data.get("synthetic") is True:
        return {"result": "NOT_READY", "reason": "local fixture or unmarked evidence"}, 2
    for k in ("source", "resource_id", "collected_at_utc", "baseline_id", "reviewer"):
        if not isinstance(data.get(k), str) or not data[k].strip():
            return {"result": "NOT_READY", "reason": "provenance missing"}, 2
    if "synthetic" in data["source"].lower() or "synthetic" in data["baseline_id"].lower():
        return {"result": "NOT_READY", "reason": "synthetic content"}, 2
    try:
        ts = datetime.fromisoformat(data["collected_at_utc"].replace("Z", "+00:00"))
        if ts.tzinfo is None:
            raise ValueError("UTC offset missing")
    except ValueError:
        return {"result": "NOT_READY", "reason": "timestamp invalid"}, 2
    if "observation" not in data:
        return {"result": "NOT_READY", "reason": "value absent"}, 2
    r = controls[cid]
    outcome = predicate(r["rule_type"], r["rule_args"], data["observation"])
    status = {"MATCH":"REVIEW_REQUIRED","MISMATCH":"DIFFERENCE_REVIEW_REQUIRED","NOT_READY":"NOT_READY"}[outcome]
    return {"result": status, "predicate": outcome, "reason": "unsigned local evidence; external attestation required"}, 2


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    m = ap.add_mutually_exclusive_group(required=True)
    m.add_argument("--selftest", metavar="ALL_OR_TEST_ID")
    m.add_argument("--evaluate", metavar="TEST_ID")
    ap.add_argument("--spec", type=Path, default=SOURCE)
    ap.add_argument("--observation", type=Path)
    args = ap.parse_args(argv)
    try:
        selected = args.spec.resolve(strict=True)
        if selected == TRANSLATION.resolve(strict=True):
            published_translation(selected)
        elif selected != SOURCE.resolve(strict=True):
            raise ValueError("unknown spec path; original-source pin required")
        controls, _ = load_original(SOURCE)
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        print(json.dumps({"result":"NOT_READY","reason":"Phase 5 original/translation unavailable or untrusted",
                          "azure_live_passes":0,"release_decision":"NO_GO"}))
        return 2
    output, code = (synthetic_check(controls,args.selftest) if args.selftest
                    else review_observation(controls,args.evaluate,args.observation))
    output["azure_live_passes"] = 0
    output["release_decision"] = "NO_GO"
    print(json.dumps(output,ensure_ascii=False,sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
