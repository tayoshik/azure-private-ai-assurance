#!/usr/bin/env python3
"""Phase 7 offline Terraform-plan triage, NEVER an Azure/plan acceptance decision.

Original Phase7 plan guard was unsafe: it returned "Pass" for incomplete plans and
exit zero for self-reported --expect. This implementation only accepts source
fixtures for synthetic smoke tests; all --plan invocations exit 2.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANS = ROOT / "fixtures"
DATA_PLANE = {
    "azurerm_linux_web_app", "azurerm_windows_web_app", "azurerm_cognitive_account",
    "azurerm_search_service", "azurerm_cosmosdb_account", "azurerm_key_vault",
}
BROAD_SOURCE = {"*", "any", "internet", "0.0.0.0/0", "::/0"}
SENSITIVE_PORTS = {"*", "80", "443", "22", "3389"}


def inspect(plan):
    """Return (nonauthoritative status, reasons) based on *local* JSON only."""
    if not isinstance(plan, dict):
        return "NOT_READY", ["plan must be a JSON object"]
    changes = plan.get("resource_changes")
    if not isinstance(plan.get("planned_values"), dict) or not isinstance(changes, list):
        return "NOT_READY", ["planned_values/resource_changes missing or wrong type"]
    if not changes:
        return "NOT_READY", ["empty or unverified plan"]
    findings = []
    incomplete = []
    for n, change in enumerate(changes):
        if not isinstance(change, dict) or not isinstance(change.get("type"), str):
            incomplete.append(f"change {n}: invalid resource row")
            continue
        kind = change["type"]
        details = change.get("change")
        if not isinstance(details, dict):
            incomplete.append(f"change {n}: missing change object")
            continue
        actions = details.get("actions")
        after = details.get("after")
        if (not isinstance(actions, list) or not actions
                or any(a not in ("create", "read", "update", "delete", "no-op") for a in actions)):
            incomplete.append(f"change {n}: unknown/invalid actions")
            continue
        if "delete" in actions and "create" not in actions:
            incomplete.append(f"change {n}: deletion needs separate policy")
            continue
        if not isinstance(after, dict):
            incomplete.append(f"change {n}: after state missing or unresolved")
            continue
        unknown = details.get("after_unknown")
        if isinstance(unknown, dict) and any(unknown.get(k) for k in (
                "public_network_access_enabled", "access", "direction",
                "source_address_prefix", "source_address_prefixes",
                "destination_port_range", "destination_port_ranges")):
            incomplete.append(f"change {n}: relevant value unknown")
            continue
        if kind in DATA_PLANE:
            if after.get("public_network_access_enabled") is True:
                findings.append(f"change {n}: {kind} public network access enabled")
            elif after.get("public_network_access_enabled") is not False:
                incomplete.append(f"change {n}: PNA not explicitly false")
        elif kind == "azurerm_network_security_rule":
            if "access" not in after or "direction" not in after:
                incomplete.append(f"change {n}: NSG access/direction unknown")
                continue
            if after["access"] == "Allow" and after["direction"] == "Inbound":
                sources = after.get("source_address_prefixes") or [after.get("source_address_prefix")]
                ports = after.get("destination_port_ranges") or [after.get("destination_port_range")]
                if (not isinstance(sources, list) or not isinstance(ports, list)
                        or any(not isinstance(x, str) for x in sources + ports)):
                    incomplete.append(f"change {n}: NSG source/port unknown")
                elif any(x.strip().lower() in BROAD_SOURCE for x in sources) and any(
                        p.strip().lower() in SENSITIVE_PORTS for p in ports):
                    findings.append(f"change {n}: broad inbound NSG allow")
                else:
                    incomplete.append(f"change {n}: no proof of acceptable NSG scope")
            else:
                incomplete.append(f"change {n}: NSG scope requires independent review")
        else:
            incomplete.append(f"change {n}: unreviewed resource type {kind}")
    if findings:
        return "DIFFERENCE_REVIEW_REQUIRED", findings + incomplete
    if incomplete:
        return "NOT_READY", incomplete
    return "REVIEW_REQUIRED", ["matched selected offline predicates only; independent plan review required"]


def synthetic_tests():
    expected = (
        ("plan_app_pna_true.json", "DIFFERENCE_REVIEW_REQUIRED"),
        ("plan_nsg_any.json", "DIFFERENCE_REVIEW_REQUIRED"),
        ("plan_safe.json", "REVIEW_REQUIRED"),
    )
    results = []
    for name, wanted in expected:
        try:
            data = json.loads((PLANS / name).read_text(encoding="utf-8"))
            actual, _ = inspect(data)
        except (OSError, ValueError, TypeError):
            actual = "NOT_READY"
        results.append({"fixture": name, "classification": actual, "expected": wanted,
                        "synthetic": True, "success": actual == wanted})
    invalid, _ = inspect({})
    ok = all(x["success"] for x in results) and invalid == "NOT_READY"
    return {"execution_class": "OFFLINE_SYNTHETIC_ONLY",
            "result": "SELFTEST_PASS" if ok else "SELFTEST_FAIL",
            "synthetic_cases": len(results), "selftest_pass": sum(x["success"] for x in results),
            "cases": results, "malformed_plan": invalid, "azure_live_passes": 0,
            "release_decision": "NO_GO"}, (0 if ok else 1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true")
    group.add_argument("--plan", type=Path)
    ap.add_argument("--expect", choices=["Pass", "Fail", "NotReady"])
    args = ap.parse_args(argv)
    if args.selftest:
        output, status = synthetic_tests()
    else:
        try:
            source = json.loads(args.plan.read_text(encoding="utf-8"))
            label, reasons = inspect(source)
        except (OSError, ValueError, TypeError):
            label, reasons = "NOT_READY", ["missing, unreadable or malformed plan"]
        output = {"classification": label, "findings": reasons,
                  "review_only": True, "expected_argument_ignored_for_acceptance": args.expect,
                  "azure_live_passes": 0, "release_decision": "NO_GO"}
        status = 2  # no unsigned local plan can produce an acceptance exit-zero
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
