#!/usr/bin/env python3
"""Phase 3 frozen-source offline fixture checker and conservative IPAM review.

Never connects to Azure and NEVER issues Azure live PASS/FAIL or release approval.
Source fixtures demonstrate a *detector interface*, not real control compliance.
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "specs/phase3_264.json"
# Frozen original 2026-11-10 Phase 3 source archive, verified against
# the English publication's source_phase3_spec_sha256.
SPEC_SHA256 = "66d389a459bd0abc6ce930a1995e6d1328b087c3532849957f2bc458f7336c14"
EXPECTED = {f"AZ-T{step:02}-{n:02}" for step in range(21, 33) for n in range(1, 23)}
MATCH = "MATCH"
MISMATCH = "MISMATCH"
NOT_READY = "NOT_READY"


def equal_typed(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(equal_typed(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(equal_typed(x, y) for x, y in zip(a, b))
    if isinstance(a, float):
        return math.isfinite(a) and math.isfinite(b) and a == b
    return a == b


def evaluate(rule: str, cfg: dict, observed):
    """Pure predicate evaluator. Internal MATCH never means Azure PASS."""
    if observed is None:
        return NOT_READY
    try:
        if rule == "eq":
            return MATCH if equal_typed(observed, cfg["expected"]) else MISMATCH
        if rule == "nonempty":
            return MATCH if type(observed) in (str, list, dict) and len(observed) > 0 else MISMATCH
        if rule in ("minimum", "maximum"):
            limit = cfg["expected"]
            if type(observed) not in (int, float) or type(limit) not in (int, float):
                return MISMATCH
            if not (math.isfinite(observed) and math.isfinite(limit)):
                return MISMATCH
            good = observed >= limit if rule == "minimum" else observed <= limit
            return MATCH if good else MISMATCH
        if rule == "is_true":
            return MATCH if observed is True else MISMATCH
        if rule == "is_false":
            return MATCH if observed is False else MISMATCH
        if rule == "is_succeeded":
            return MATCH if observed == "Succeeded" else MISMATCH
        if rule == "private_ip":
            if not isinstance(observed, str):
                return MISMATCH
            address = ipaddress.ip_address(observed)
            subnet = ipaddress.ip_network(cfg["subnet"], strict=True)
            return MATCH if address.is_private and address in subnet else MISMATCH
        if rule == "no_overlap":
            if not isinstance(observed, list) or not observed:
                return MISMATCH
            nets = [ipaddress.ip_network(x, strict=True) for x in observed]
            return MATCH if all(not a.overlaps(b) for i, a in enumerate(nets)
                                for b in nets[i + 1:]) else MISMATCH
        # The original spec uses only the seven rules above. Unknown predicates
        # must never silently accept a new or unreviewed control type.
        return NOT_READY
    except (KeyError, ValueError, TypeError, OverflowError):
        return NOT_READY


def load_source(path: Path = DEFAULT_SPEC):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != SPEC_SHA256:
        raise ValueError("Phase 3 spec SHA-256 differs from frozen primary source")
    source = json.loads(raw)
    if not isinstance(source, dict) or source.get("schema") != "azure-phase3-264/v1":
        raise ValueError("unexpected Phase 3 source schema")
    if source.get("live_azure_successes") != 0:
        raise ValueError("unapproved real Azure acceptance")
    tests, controls = source.get("tests"), source.get("controls")
    if not isinstance(tests, list) or len(tests) != 264:
        raise ValueError("expected 264 original tests")
    if not isinstance(controls, list) or len(controls) != 132:
        raise ValueError("expected 132 controls")
    if any(not isinstance(t, dict) for t in tests) or any(
        not isinstance(c, dict) for c in controls
    ):
        raise ValueError("non-object test or control")
    ids = [t.get("id") for t in tests]
    if len(set(ids)) != 264 or set(ids) != EXPECTED:
        raise ValueError("canonical Phase 3 test IDs missing or duplicate")
    by_id = {x["id"]: x for x in tests}
    expected_control_ids = {f"AZ-T{s:02}-{n:02}" for s in range(21, 33)
                            for n in range(1, 23, 2)}
    control_ids = [x.get("control_id") for x in controls]
    if len(set(control_ids)) != 132 or set(control_ids) != expected_control_ids:
        raise ValueError("canonical Phase 3 control IDs incomplete")
    for t in tests:
        tid = t["id"]
        step = int(tid[4:6])
        number = int(tid[-2:])
        if (str(t.get("step")) != str(step)
            or t.get("polarity") != ("正系" if number % 2 else "逸脱検出")
            or t.get("offline_case") is not (number % 2 == 0)
            or not isinstance(t.get("command"), str) or not t["command"].strip()):
            raise ValueError(f"invalid canonical test metadata: {tid}")
    for c in controls:
        tid = c["control_id"]
        next_id = tid[:-2] + f"{int(tid[-2:]) + 1:02}"
        if (c.get("step") != int(tid[4:6])
            or by_id[tid].get("rule_type") != c.get("rule_type")
            or by_id[next_id].get("rule_type") != c.get("rule_type")
            or not isinstance(c.get("rule_args"), dict)):
            raise ValueError(f"control rule/partner mismatch: {tid}")
    return source


def offline_selftest(source: dict, case_id: str):
    tests = source["tests"] if case_id == "ALL" else [
        x for x in source["tests"] if x["id"] == case_id
    ]
    if not tests:
        raise ValueError(f"unknown test ID {case_id}")
    controls = {c["control_id"]: c for c in source["controls"]}
    failures = []
    for test in tests:
        tid = test["id"]
        number = int(tid[-2:])
        partner = tid[:-2] + f"{number - 1 if number % 2 == 0 else number:02}"
        control = controls[partner]
        is_synthetic_negative = number % 2 == 0
        observed = control["bad_fixture"] if is_synthetic_negative else control["good_fixture"]
        expected = MISMATCH if is_synthetic_negative else MATCH
        actual = evaluate(control["rule_type"], control["rule_args"], observed)
        absent = evaluate(control["rule_type"], control["rule_args"], None)
        if actual != expected or absent != NOT_READY:
            failures.append({"id": tid, "expected": expected,
                             "observed": actual, "missing": absent})
    return {
        "kind": "OFFLINE_FROZEN_FIXTURE_SMOKE_TEST",
        "checked_test_ids": len(tests),
        "detector_smoke_pass": len(tests) - len(failures),
        "detector_smoke_fail": len(failures),
        "fixture_source": "FROZEN_SYNTHETIC_NOT_AZURE",
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "warning": "Passing synthetic fixtures is not 264 independent control proofs.",
        "errors": failures[:10],
    }


def review_ipam(path: Path):
    """Read-only structural IPAM triage; never reports live security PASS."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as ex:
        return NOT_READY, [f"unreadable IPAM: {ex}"]
    if not isinstance(data, dict) or not isinstance(data.get("networks"), dict):
        return NOT_READY, ["IPAM networks must be an object"]
    names = ("vnet", "onprem", "hub", "vpn", "dr")
    if any(k not in data["networks"] for k in names):
        return NOT_READY, ["missing mandatory network categories"]
    roots = []
    try:
        for name in names:
            entry = data["networks"][name]
            if not isinstance(entry, dict) or not isinstance(entry.get("cidrs"), list):
                return NOT_READY, [f"invalid {name}.cidrs"]
            for cidr in entry["cidrs"]:
                roots.append((name, ipaddress.ip_network(cidr, strict=True)))
        if not data["networks"]["vnet"]["cidrs"]:
            return NOT_READY, ["VNet CIDR inventory empty"]
        subnets = data.get("subnets")
        if not isinstance(subnets, list) or not subnets:
            return NOT_READY, ["subnet inventory missing"]
        parsed = []
        for entry in subnets:
            if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) \
               or not entry["name"] or not isinstance(entry.get("cidr"), str):
                return NOT_READY, ["subnet must contain name and CIDR"]
            parsed.append((entry["name"], ipaddress.ip_network(entry["cidr"], strict=True)))
    except (ValueError, KeyError, TypeError) as ex:
        return NOT_READY, [f"malformed IPAM network: {ex}"]
    findings = []
    if len({n for n, _ in parsed}) != len(parsed):
        findings.append("duplicate subnet names")
    for i, (name, subnet) in enumerate(roots):
        for other, network in roots[i + 1:]:
            if subnet.overlaps(network):
                findings.append(f"cross-scope overlap: {name}:{subnet} vs {other}:{network}")
    for i, (name, subnet) in enumerate(parsed):
        if not any(subnet.subnet_of(net) for scope, net in roots if scope == "vnet"):
            findings.append(f"subnet outside VNet: {name}:{subnet}")
        for other, network in parsed[i + 1:]:
            if subnet.overlaps(network):
                findings.append(f"subnet overlap: {name}:{subnet} vs {other}:{network}")
    return (MISMATCH if findings else MATCH), findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    option = parser.add_mutually_exclusive_group(required=True)
    option.add_argument("--selftest", metavar="CASE_ID_OR_ALL")
    option.add_argument("--cidr-check", metavar="IPAM_JSON", type=Path)
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    args = parser.parse_args(argv)
    if args.cidr_check:
        internal, findings = review_ipam(args.cidr_check)
        result = (NOT_READY if internal == NOT_READY else
                  "REVIEW_REQUIRED" if internal == MATCH else
                  "DIFFERENCE_REVIEW_REQUIRED")
        print(json.dumps({"kind": "OFFLINE_IPAM_REVIEW", "result": result,
                          "findings": findings, "azure_live_passes": 0,
                          "release_decision": "NO_GO",
                          "note": "Unsigned IPAM source does not prove Azure state."},
                         ensure_ascii=False, sort_keys=True))
        return 2
    try:
        spec = load_source(args.spec)
        result = offline_selftest(spec, args.selftest)
    except (ValueError, TypeError, KeyError, OSError, UnicodeError) as ex:
        print(json.dumps({"kind": "OFFLINE_FROZEN_FIXTURE_SMOKE_TEST",
                          "result": NOT_READY, "reason": str(ex),
                          "azure_live_passes": 0, "release_decision": "NO_GO"},
                         ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if not result["detector_smoke_fail"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
