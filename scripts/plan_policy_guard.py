#!/usr/bin/env python3
"""Strict, offline-only Terraform plan triage. REVIEW_REQUIRED is not approval."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

RULES = {"public_ip", "public_access", "rbac", "diagnostics"}
DATA_PLANE_TYPES = {
    "azurerm_cognitive_account", "azurerm_search_service",
    "azurerm_cosmosdb_account", "azurerm_linux_web_app",
    "azurerm_windows_web_app", "azurerm_key_vault",
}
BROAD_ROLES = {"owner", "contributor", "user access administrator"}


def decision(rule, plan, scope, plan_sha):
    """Return conservative (verdict, reason), without executing plan/apply."""
    if rule not in RULES:
        return "NOT_READY", "Unknown policy rule"
    if not isinstance(plan, dict) or not isinstance(scope, dict):
        return "NOT_READY", "Non-object plan or scope"
    if not isinstance(plan_sha, str) or len(plan_sha) != 64:
        return "NOT_READY", "Plan digest not verified"
    if not isinstance(scope.get("approval_id"), str) or not scope["approval_id"].strip():
        return "NOT_READY", "Approval ID missing"
    if scope.get("plan_sha256") != plan_sha:
        return "NOT_READY", "Plan bytes differ from approved digest"
    reviewers = scope.get("reviewers")
    if (not isinstance(reviewers, list) or len(reviewers) < 2
        or any(not isinstance(x, str) or not x.strip() for x in reviewers)
        or len(set(reviewers)) < 2):
        return "NOT_READY", "Two distinct reviewers required"
    addresses = scope.get("approved_addresses")
    if (not isinstance(addresses, list) or not addresses
        or any(not isinstance(x, str) or not x.strip() for x in addresses)
        or len(set(addresses)) != len(addresses)
        or not isinstance(scope.get("source_commit"), str)
        or not scope["source_commit"].strip()):
        return "NOT_READY", "Pinned source or approved address inventory missing"
    changes = plan.get("resource_changes")
    if not isinstance(changes, list):
        return "NOT_READY", "Terraform resource_changes not available"
    known_addresses = set(addresses)
    for item in changes:
        if not isinstance(item, dict) or not isinstance(item.get("change"), dict):
            return "NOT_READY", "Malformed resource change"
        if item.get("address") not in known_addresses:
            return "NOT_READY", "Out-of-scope resource address"
        operation = item["change"].get("actions")
        if not isinstance(operation, list) or not operation:
            return "NOT_READY", "Operation unknown"
        if any(x not in ("create", "read", "update", "delete", "no-op") for x in operation):
            return "NOT_READY", "Unexpected plan action"
        if "delete" in operation and "create" in operation:
            return "NOT_READY", "Replacement needs a separate control review"
        kind = item.get("type")
        after = item["change"].get("after")
        if rule == "public_ip" and kind == "azurerm_public_ip" and (
                "create" in operation or "update" in operation):
            return "FAIL", "Public IP creation/update is not approved by this rule"
        if rule == "public_access" and kind in DATA_PLANE_TYPES and (
                "create" in operation or "update" in operation):
            if not isinstance(after, dict):
                return "NOT_READY", "PaaS after state is not known"
            flag = after.get("public_network_access_enabled")
            alternate = after.get("public_network_access")
            if flag is True or (isinstance(alternate, str)
                                and alternate.lower() == "enabled"):
                return "FAIL", "Public data-plane enabled"
            if flag is not False and not (
                    isinstance(alternate, str) and alternate.lower() == "disabled"):
                return "NOT_READY", "No explicit public-network deny evidence"
        if rule == "rbac" and kind == "azurerm_role_assignment" and (
                "create" in operation or "update" in operation):
            if not isinstance(after, dict):
                return "NOT_READY", "RBAC after state unavailable"
            role = after.get("role_definition_name")
            if not isinstance(role, str) or not role.strip():
                return "NOT_READY", "Role definition name must be resolved"
            if role.strip().lower() in BROAD_ROLES:
                return "FAIL", "Broad role requires exceptional approval"
        if rule == "diagnostics" and kind == "azurerm_monitor_diagnostic_setting":
            if "delete" in operation:
                return "FAIL", "Diagnostic setting deletion"
            if "create" in operation or "update" in operation:
                if not isinstance(after, dict):
                    return "NOT_READY", "Diagnostic after state unknown"
                cats = after.get("enabled_log", after.get("log"))
                if cats is None:
                    return "NOT_READY", "Diagnostic categories missing"
                if not isinstance(cats, list) or not cats:
                    return "FAIL", "No diagnostic categories"
                if not all(isinstance(x, dict) for x in cats):
                    return "NOT_READY", "Invalid log-category representation"
                if "log" in after and not any(x.get("enabled") is True for x in cats):
                    return "FAIL", "All legacy diagnostic categories disabled"
    # Even with an apparently clean plan, there is no live resource/effective
    # access/scope proof, and no independent signature review in this script.
    return "REVIEW_REQUIRED", "No selected-rule violation; plan completeness unproven"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rule", required=True, choices=sorted(RULES))
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--scope", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        raw = args.plan.read_bytes()
        plan = json.loads(raw.decode("utf-8"))
        scope = json.loads(args.scope.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        print(json.dumps({"rule": args.rule, "result": "NOT_READY", "azure_live_pass": False}))
        return 2
    result, reason = decision(args.rule, plan, scope, hashlib.sha256(raw).hexdigest())
    print(json.dumps({"rule": args.rule, "result": result, "reason": reason,
                      "execution_class": "OFFLINE_UNTRUSTED_PLAN_TRIAGE",
                      "azure_live_pass": False, "release_decision": "NO_GO"}))
    return 1 if result == "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
