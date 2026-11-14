#!/usr/bin/env python3
"""REST03: fail-closed Azure ARM configuration assessor, default offline only.

The result OBSERVED_PENDING_REVIEW is deliberately *not* an Azure acceptance PASS.
No Azure connection is performed on import, --selftest, or --fixture.
No write API is available. The assessment never emits raw ARM properties or tokens.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from azure_rest_reader import AzureReadOnlyClient, NotReadyError

PROFILES = {
    "web_app": "microsoft.web/sites",
    "azure_openai": "microsoft.cognitiveservices/accounts",
    "ai_search": "microsoft.search/searchservices",
    "cosmos_nosql": "microsoft.documentdb/databaseaccounts",
    "key_vault": "microsoft.keyvault/vaults",
    "private_endpoint": "microsoft.network/privateendpoints",
    "application_gateway": "microsoft.network/applicationgateways",
}

# A missing field means NOT_READY. False/equivalent-looking values are not
# interpreted as secure. These checks are only a subset of full assurance.
SCALAR_CHECKS = {
    "web_app": (("properties.publicNetworkAccess", "Disabled"),
                ("properties.httpsOnly", True)),
    "azure_openai": (("kind", "OpenAI"),
                     ("properties.publicNetworkAccess", "Disabled"),
                     ("properties.disableLocalAuth", True)),
    "ai_search": (("properties.publicNetworkAccess", "Disabled"),
                  ("properties.disableLocalAuth", True)),
    "cosmos_nosql": (("properties.publicNetworkAccess", "Disabled"),
                     ("properties.disableLocalAuth", True)),
    "key_vault": (("properties.publicNetworkAccess", "Disabled"),
                  ("properties.enableRbacAuthorization", True),
                  ("properties.enablePurgeProtection", True)),
}
MISSING = object()
ID_RE = re.compile(
    r"^/subscriptions/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    r"/resourceGroups/[^/?#]+/providers/(?P<namespace>[a-zA-Z0-9.]+)/"
    r"(?P<type>[a-zA-Z0-9]+)/[^/?#]+$", re.I)
VERSION_RE = re.compile(r"^20\d\d-\d\d-\d\d(?:-preview)?$")


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
             separators=(",", ":")).encode("utf-8")).hexdigest()


def property_at(value: dict, path: str) -> Any:
    cursor = value
    for field in path.split("."):
        if not isinstance(cursor, dict) or field not in cursor:
            return MISSING
        cursor = cursor[field]
    return cursor


def equivalent(actual: Any, expected: Any) -> bool:
    # Python True == 1, so keep booleans strict. ARM enums are case-insensitive.
    if isinstance(expected, bool):
        return type(actual) is bool and actual is expected
    if isinstance(expected, str):
        return isinstance(actual, str) and actual.casefold() == expected.casefold()
    return type(actual) is type(expected) and actual == expected


def validate_targets(targets: list) -> list[dict]:
    if not isinstance(targets, list) or not targets or len(targets) > 100:
        raise ValueError("1..100 explicit targets required")
    normalized = []
    seen = set()
    for target in targets:
        if not isinstance(target, dict):
            raise ValueError("target must be a dictionary")
        rid, profile, version = target.get("resource_id"), target.get("profile"), target.get("api_version")
        match = ID_RE.fullmatch(rid) if isinstance(rid, str) else None
        if (match is None or not isinstance(profile, str) or profile not in PROFILES
                or not isinstance(version, str) or not VERSION_RE.fullmatch(version)):
            raise ValueError("target requires approved resource_id, profile and pinned api_version")
        if rid.lower() in seen:
            raise ValueError("duplicate resource ID")
        seen.add(rid.lower())
        # Validate ARM type segment from the approved resource ID.
        expected = PROFILES[profile]
        if (match.group("namespace") + "/" + match.group("type")).casefold() != expected:
            raise ValueError("resource ID does not match profile")
        groups = target.get("expected_group_ids")
        if profile == "private_endpoint":
            if not isinstance(groups, list) or len(groups) != 1 or not isinstance(groups[0], str) or not groups[0].strip():
                raise ValueError("private endpoint requires one approved group ID")
        elif groups is not None:
            raise ValueError("expected_group_ids only supported for private_endpoint")
        normalized.append(dict(target))
    return normalized


def assess_observation(target: dict, observed: dict, *, synthetic: bool = False) -> dict:
    """Evaluate bounded policy controls; never emits raw observed properties."""
    baseline = validate_targets([target])[0]
    rid, profile = baseline["resource_id"], baseline["profile"]
    issues = []
    missing = []
    evidence = observed.get("evidence_sha256") if isinstance(observed, dict) else None
    base = {"resource_id_sha256": digest(rid.lower()), "profile": profile,
            "baseline_sha256": digest(baseline),
            "evidence_sha256": evidence if isinstance(evidence, str) and re.fullmatch(r"[0-9a-f]{64}", evidence) else None,
            "azure_live_acceptance": "NOT_READY"}
    if not isinstance(observed, dict) or observed.get("state") != "OBSERVED_NOT_ACCEPTED":
        return {**base, "status": "NOT_READY", "issues": ["no complete REST02 observation"]}
    data = observed.get("observation")
    if not isinstance(data, dict) or str(observed.get("resource_id", "")).lower() != rid.lower():
        return {**base, "status": "NOT_READY", "issues": ["observation or resource scope mismatch"]}
    if base["evidence_sha256"] is None or base["evidence_sha256"] != digest(data):
        return {**base, "status": "NOT_READY", "issues": ["missing or inconsistent observation digest"]}
    if not isinstance(data.get("id"), str) or data["id"].lower() != rid.lower():
        return {**base, "status": "NOT_READY", "issues": ["resource ID mismatched"]}
    actual_type = data.get("type")
    if not isinstance(actual_type, str):
        missing.append("type")
    elif actual_type.casefold() != PROFILES[profile]:
        issues.append("unexpected resource type")

    for path, expected in SCALAR_CHECKS.get(profile, ()):
        actual = property_at(data, path)
        if actual is MISSING or actual is None:
            missing.append(path)
        elif not equivalent(actual, expected):
            issues.append(path + " violated")

    if profile == "private_endpoint":
        props = data.get("properties", {})
        links = props.get("privateLinkServiceConnections") if isinstance(props, dict) else None
        manual = props.get("manualPrivateLinkServiceConnections") if isinstance(props, dict) else None
        connections = []
        if isinstance(links, list):
            connections.extend(links)
        if isinstance(manual, list):
            connections.extend(manual)
        if not connections:
            missing.append("privateLinkServiceConnections")
        for c in connections:
            cp = c.get("properties", {}) if isinstance(c, dict) else {}
            state = property_at(cp, "privateLinkServiceConnectionState.status")
            groups = cp.get("groupIds") if isinstance(cp, dict) else None
            if state is MISSING or groups is None:
                missing.append("connection status/groupIds")
            else:
                if not equivalent(state, "Approved"):
                    issues.append("Private Endpoint connection not Approved")
                if not isinstance(groups, list) or baseline["expected_group_ids"][0].casefold() not in [str(x).casefold() for x in groups]:
                    issues.append("Private Endpoint group mismatch")
        # NIC IP and DNS are separately checked by REST04/private runner; no claim here.

    if profile == "application_gateway":
        frontends = property_at(data, "properties.frontendIPConfigurations")
        if not isinstance(frontends, list) or not frontends:
            missing.append("frontendIPConfigurations")
        else:
            for f in frontends:
                fp = f.get("properties", {}) if isinstance(f, dict) else {}
                if fp.get("publicIPAddress"):
                    issues.append("Gateway public frontend present")
                if not isinstance(fp.get("privateIPAddress"), str) or not fp["privateIPAddress"].strip():
                    missing.append("Gateway privateIPAddress")
                if not equivalent(fp.get("privateIPAllocationMethod"), "Static"):
                    missing.append("Gateway static private frontend") if fp.get("privateIPAllocationMethod") is None else issues.append("Gateway frontend allocation not static")
        waf = property_at(data, "properties.firewallPolicy.id")
        if waf is MISSING or not isinstance(waf, str) or not waf.strip():
            missing.append("firewallPolicy.id")
    if issues:
        status = "FAIL_POLICY_OBSERVED" if not synthetic else "FAIL_OFFLINE_POLICY_FIXTURE"
    elif missing:
        status = "NOT_READY"
    else:
        status = "PASS_OFFLINE_FIXTURE_ONLY" if synthetic else "OBSERVED_PENDING_INDEPENDENT_REVIEW"
    return {**base, "status": status, "issues": sorted(set(issues)), "missing": sorted(set(missing)),
            "checked_scalar_controls": len(SCALAR_CHECKS.get(profile, ()))}


def assess_inventory(observation: dict, targets: list[dict]) -> dict:
    targets = validate_targets(targets)
    if not isinstance(observation, dict) or observation.get("state") != "OBSERVED_NOT_ACCEPTED" or observation.get("complete_pages") is not True:
        return {"status": "NOT_READY", "reason": "incomplete Resource Graph observation"}
    rows = observation.get("rows")
    if not isinstance(rows, list):
        return {"status": "NOT_READY", "reason": "invalid Resource Graph rows"}
    if observation.get("evidence_sha256") != digest(rows):
        return {"status": "NOT_READY", "reason": "missing or inconsistent inventory digest"}
    observed = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            return {"status": "NOT_READY", "reason": "invalid Resource Graph resource ID"}
        ident = row["id"].lower()
        if ident in observed:
            return {"status": "NOT_READY", "reason": "duplicate Resource Graph resource ID"}
        observed[ident] = row
    for target in targets:
        row = observed.get(target["resource_id"].lower())
        if not row:
            return {"status": "NOT_READY", "reason": "approved target absent in queried inventory"}
        if str(row.get("type", "")).casefold() != PROFILES[target["profile"]]:
            return {"status": "FAIL_POLICY_OBSERVED", "reason": "inventory resource type mismatch"}
    return {"status": "OBSERVED_PENDING_INDEPENDENT_REVIEW", "target_count": len(targets),
            "inventory_evidence_sha256": observation.get("evidence_sha256"),
            "azure_live_acceptance": "NOT_READY"}


def audit_client(client: AzureReadOnlyClient, targets: list[dict]) -> dict:
    """Read-only resource audit for approved CI, used with mocked client offline.

    Live callers must provision a bounded, scoped client with read_enabled=True
    and OIDC credentials independently. This function never performs a write.
    """
    targets = validate_targets(targets)
    try:
        inventory = client.resource_graph_inventory([PROFILES[t["profile"]] for t in targets])
        inventory_result = assess_inventory(inventory, targets)
        if inventory_result["status"] != "OBSERVED_PENDING_INDEPENDENT_REVIEW":
            return {"status": "NOT_READY", "inventory": inventory_result,
                    "azure_live_acceptance": "NOT_READY", "results": []}
        results = []
        for target in targets:
            obs = client.get_resource(target["resource_id"], target["api_version"])
            results.append(assess_observation(target, obs))
    except (NotReadyError, ValueError) as exc:
        # Avoid leaking private resource strings/error bodies to stdout.
        return {"status": "NOT_READY", "reason_class": type(exc).__name__,
                "azure_live_acceptance": "NOT_READY", "results": []}
    if any(r["status"] == "FAIL_POLICY_OBSERVED" for r in results):
        status = "FAIL_POLICY_OBSERVED"
    elif any(r["status"] == "NOT_READY" for r in results):
        status = "NOT_READY"
    else:
        status = "OBSERVED_PENDING_INDEPENDENT_REVIEW"
    return {"status": status, "inventory": inventory_result, "results": results,
            "azure_live_acceptance": "NOT_READY", "azure_live_passes": 0}


def run_selftest() -> dict:
    rid = "/subscriptions/01234567-89ab-4def-8123-0123456789ab/resourceGroups/rg-synthetic/providers/Microsoft.Web/sites/web-synthetic"
    target = {"resource_id": rid, "profile": "web_app", "api_version": "2024-04-01"}
    good = {"id": rid, "type": "Microsoft.Web/sites",
            "properties": {"publicNetworkAccess": "Disabled", "httpsOnly": True}}
    def obs(d):
        return {"state": "OBSERVED_NOT_ACCEPTED", "resource_id": rid,
                "observation": d, "evidence_sha256": digest(d)}
    x = assess_observation(target, obs(good), synthetic=True)
    bad = json.loads(json.dumps(good));bad["properties"]["publicNetworkAccess"] = "Enabled"
    y = assess_observation(target, obs(bad), synthetic=True)
    missing = json.loads(json.dumps(good));missing["properties"].pop("httpsOnly")
    z = assess_observation(target, obs(missing), synthetic=True)
    if [x["status"], y["status"], z["status"]] != ["PASS_OFFLINE_FIXTURE_ONLY", "FAIL_OFFLINE_POLICY_FIXTURE", "NOT_READY"]:
        raise AssertionError("synthetic expected states mismatched")
    return {"status": "PASS_OFFLINE_FIXTURES_ONLY", "good": x["status"],
            "bad": y["status"], "missing": z["status"],
            "azure_live_passes": 0, "release_decision": "NO_GO"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true", help="fully synthetic, no Azure reads")
    group.add_argument("--fixture", type=Path, help="local JSON with targets and REST02-style observations")
    args = parser.parse_args()
    if args.selftest:
        result = run_selftest()
    else:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        targets = validate_targets(fixture["targets"])
        observations = fixture["observations"]
        if not isinstance(observations, list) or len(observations) != len(targets):
            raise ValueError("one observation per target required")
        result = {"status": "PASS_OFFLINE_FIXTURES_ONLY", "azure_live_passes": 0,
                  "results": [assess_observation(t, o, synthetic=True) for t, o in zip(targets, observations)]}
        if any(x["status"] == "FAIL_OFFLINE_POLICY_FIXTURE" for x in result["results"]):
            result["status"] = "FAIL_OFFLINE_POLICY_FIXTURE"
        elif any(x["status"] == "NOT_READY" for x in result["results"]):
            result["status"] = "NOT_READY"
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "PASS_OFFLINE_FIXTURES_ONLY" else 1


if __name__ == "__main__":
    sys.exit(main())
