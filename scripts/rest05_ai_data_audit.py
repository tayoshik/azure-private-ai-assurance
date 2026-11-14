#!/usr/bin/env python3
"""REST05: fail-closed Azure OpenAI / AI Search / Cosmos DB ARM assessor.

Offline CLI only: --selftest, --fixture. No live Azure operation is exposed
as a CLI switch. A separately approved OIDC CI integration can call audit_client
with REST02's read-only AzureReadOnlyClient. No data-plane operations, inference,
account keys, mutations, or log disclosure are included. Every live observation
remains pending independent review and private data-plane verification.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

from azure_rest_reader import AzureReadOnlyClient, NotReadyError
from rest03_resource_audit import digest

SCHEMA = "azure-private-ai-assurance/rest05-manifest/v1"
SID_RE = re.compile(r"^/subscriptions/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/", re.I)
ACCOUNT_TYPES = {
    "azure_openai": "microsoft.cognitiveservices/accounts",
    "ai_search": "microsoft.search/searchservices",
    "cosmos_nosql": "microsoft.documentdb/databaseaccounts",
}
API_VERSION = {
    "azure_openai": "2024-10-01",
    "ai_search": "2025-05-01",
    "cosmos_nosql": "2025-10-15",
}
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,62}$")
REGION = re.compile(r"^[a-z0-9]{3,40}$")
RID = re.compile(
    r"^/subscriptions/[0-9a-f-]{36}/resourceGroups/[A-Za-z0-9_.()-]+/providers/"
    r"[A-Za-z0-9.]+/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", re.I)
ALLOWED_PROFILES = frozenset(ACCOUNT_TYPES)
ROLES = {"azure_openai": ("account", "deployment"),
         "ai_search": ("service",),
         "cosmos_nosql": ("account", "database", "container")}
MISSING = object()


def value_at(obj: Any, path: str):
    for part in path.split("."):
        if not isinstance(obj, dict) or part not in obj:
            return MISSING
        obj = obj[part]
    return obj


def eq(actual: Any, expected: Any) -> bool:
    if type(expected) is bool:
        return type(actual) is bool and actual is expected
    if isinstance(expected, str):
        return isinstance(actual, str) and actual.casefold() == expected.casefold()
    return type(actual) is type(expected) and actual == expected


def child_resource_id(target: dict, role: str) -> str:
    base = target["resource_id"]
    expected = target["expected"]
    profile = target["profile"]
    if profile == "azure_openai" and role == "deployment":
        return base + "/deployments/" + expected["deployment_name"]
    if profile == "cosmos_nosql" and role in ("database", "container"):
        db = base + "/sqlDatabases/" + expected["database_name"]
        return db if role == "database" else db + "/containers/" + expected["container_name"]
    if role in ("account", "service"):
        return base
    raise ValueError("unknown REST05 role")


def _expect_string(obj: dict, key: str, pattern=NAME):
    s = obj.get(key)
    if not isinstance(s, str) or not pattern.fullmatch(s):
        raise ValueError("invalid approved field: " + key)
    return s


def validate_target(t: dict) -> dict:
    """Allowlisted, explicit scope. No default tenant, region, names, SKUs or IDs."""
    if not isinstance(t, dict) or set(t) != {"profile", "resource_id", "api_version", "expected"}:
        raise ValueError("REST05 target has unexpected or missing fields")
    profile, rid, version, exp = t["profile"], t["resource_id"], t["api_version"], t["expected"]
    if profile not in ALLOWED_PROFILES or version != API_VERSION[profile]:
        raise ValueError("unreviewed REST05 resource profile/API version")
    if not isinstance(rid, str) or not RID.fullmatch(rid) or not SID_RE.match(rid):
        raise ValueError("invalid scoped ARM resource ID")
    kind = rid.split("/providers/", 1)[1].split("/")
    if (kind[0]+"/"+kind[1]).casefold() != ACCOUNT_TYPES[profile]:
        raise ValueError("ARM ID type/profile mismatch")
    if not isinstance(exp, dict):
        raise ValueError("expected baseline must be an object")
    _expect_string(exp, "location", REGION)
    if profile == "azure_openai":
        fields = {"location", "custom_subdomain", "deployment_name", "model_format", "model_name",
                  "model_version", "sku_name", "sku_capacity"}
        if set(exp) != fields:
            raise ValueError("OpenAI expected baseline incomplete or ambiguous")
        for k in ("custom_subdomain", "deployment_name", "model_format", "model_name", "model_version", "sku_name"):
            _expect_string(exp, k)
        if exp["model_format"].casefold() != "openai":
            raise ValueError("OpenAI deployment format must be pinned")
        if type(exp["sku_capacity"]) is not int or exp["sku_capacity"] < 1:
            raise ValueError("OpenAI positive approved capacity required")
    if profile == "ai_search":
        if set(exp) != {"location", "sku_name", "replica_count", "partition_count"}:
            raise ValueError("Search expected baseline incomplete")
        _expect_string(exp, "sku_name")
        if exp["sku_name"].casefold() == "free":
            raise ValueError("Search Free SKU is not an approved private baseline")
        for k in ("replica_count", "partition_count"):
            if type(exp[k]) is not int or not (1 <= exp[k] <= 100):
                raise ValueError("Search approved capacity required")
    if profile == "cosmos_nosql":
        if set(exp) != {"location", "database_name", "container_name", "partition_key_paths", "backup_type",
                         "consistency_level", "backup_tier"}:
            raise ValueError("Cosmos expected baseline incomplete")
        for k in ("database_name", "container_name", "consistency_level"):
            _expect_string(exp, k)
        if not isinstance(exp["backup_type"], str) or exp["backup_type"].casefold() != "continuous":
            raise ValueError("Cosmos continuous backup required")
        if exp["backup_tier"] not in ("Continuous7Days", "Continuous30Days"):
            raise ValueError("Cosmos approved continuous backup retention tier required")
        keys = exp["partition_key_paths"]
        if not isinstance(keys, list) or not (1 <= len(keys) <= 3) or len(set(keys)) != len(keys):
            raise ValueError("Cosmos partition key paths must be explicit")
        if any(not isinstance(s, str) or not re.fullmatch(r"/(?:[A-Za-z_][A-Za-z0-9_]*)", s) for s in keys):
            raise ValueError("Cosmos partition key must be a supported JSON top-level path")
    return t


def validate_manifest(doc: dict) -> list[dict]:
    if not isinstance(doc, dict) or set(doc) != {"schema", "targets"} or doc["schema"] != SCHEMA:
        raise ValueError("unknown REST05 manifest schema")
    targets = doc["targets"]
    if not isinstance(targets, list) or not (1 <= len(targets) <= 3):
        raise ValueError("REST05 requires explicit targets, up to three service accounts")
    seen = set()
    for t in targets:
        validate_target(t)
        if t["profile"] in seen:
            raise ValueError("REST05 one approved target per profile")
        seen.add(t["profile"])
    return targets


def _verify_observations(t: dict, observations: dict) -> dict | None:
    expected_roles = ROLES[t["profile"]]
    if not isinstance(observations, dict) or set(observations) != set(expected_roles):
        return None
    data = {}
    for role in expected_roles:
        wrapper = observations.get(role)
        rid = child_resource_id(t, role)
        if not isinstance(wrapper, dict) or wrapper.get("state") != "OBSERVED_NOT_ACCEPTED":
            return None
        observed = wrapper.get("observation")
        if not isinstance(observed, dict) or not eq(wrapper.get("resource_id"), rid) or not eq(observed.get("id"), rid):
            return None
        if not isinstance(wrapper.get("evidence_sha256"), str) or wrapper["evidence_sha256"] != digest(observed):
            return None
        data[role] = observed
    return data


def assess_target(t: dict, observations: dict, *, synthetic: bool=False) -> dict:
    """Compare ARM observations against an approved baseline; never emit raw data."""
    validate_target(t)
    base = {"profile":t["profile"], "target_sha256":digest(t),
            "azure_live_acceptance":"NOT_READY", "azure_live_passes":0,
            "private_data_plane_proven":False}
    data = _verify_observations(t, observations)
    if data is None:
        return {**base,"status":"NOT_READY","missing":["complete bounded REST02 observations"]}
    issues, missing = [], []
    exp = t["expected"]
    def check(role, path, expected, rule):
        actual = value_at(data[role], path)
        if actual is MISSING or actual is None:
            missing.append(rule)
        elif not eq(actual, expected):
            issues.append(rule)
    def check_exact_type(role, expected_type):
        check(role, "type", expected_type, role+".type")
    def check_account(role):
        check(role, "location", exp["location"], role+".location")
        check(role, "properties.publicNetworkAccess", "Disabled", role+".publicNetworkAccess")
        check(role, "properties.disableLocalAuth", True, role+".disableLocalAuth")
    profile = t["profile"]
    if profile == "azure_openai":
        check_exact_type("account", "Microsoft.CognitiveServices/accounts")
        check_account("account")
        check("account", "kind", "OpenAI", "account.kind")
        check("account", "properties.customSubDomainName", exp["custom_subdomain"], "account.customSubDomainName")
        check_exact_type("deployment", "Microsoft.CognitiveServices/accounts/deployments")
        for path, expected in (("properties.model.format", exp["model_format"]),
                               ("properties.model.name", exp["model_name"]),
                               ("properties.model.version", exp["model_version"]),
                               ("properties.versionUpgradeOption", "NoAutoUpgrade"),
                               ("sku.name", exp["sku_name"]),
                               ("sku.capacity", exp["sku_capacity"])):
            check("deployment", path, expected, "deployment."+path)
    elif profile == "ai_search":
        check_exact_type("service", "Microsoft.Search/searchServices")
        check_account("service")
        check("service", "properties.networkRuleSet.bypass", "None", "service.networkRuleSet.bypass")
        check("service", "sku.name", exp["sku_name"], "service.sku")
        for k in ("replica_count", "partition_count"):
            actual = value_at(data["service"], "properties."+ ("replicaCount" if k=="replica_count" else "partitionCount"))
            if actual is MISSING or actual is None:
                missing.append("service."+k)
            elif type(actual) is not int or actual < exp[k]:
                issues.append("service."+k)
    else:
        check_exact_type("account", "Microsoft.DocumentDB/databaseAccounts")
        check_account("account")
        check("account", "properties.networkAclBypass", "None", "account.networkAclBypass")
        check("account", "properties.backupPolicy.type", "Continuous", "account.backupPolicy.type")
        check("account", "properties.backupPolicy.continuousModeProperties.tier", exp["backup_tier"],
              "account.backupPolicy.tier")
        check("account", "kind", "GlobalDocumentDB", "account.kind")
        check("account", "properties.consistencyPolicy.defaultConsistencyLevel",
              exp["consistency_level"], "account.consistency")
        # Cosmos data/database paths remain unchanged; only metadata is read.
        check("database", "properties.resource.id", exp["database_name"], "database.resource.id")
        check("container", "properties.resource.id", exp["container_name"], "container.resource.id")
        partitions = value_at(data["container"], "properties.resource.partitionKey.paths")
        if partitions is MISSING or partitions is None:
            missing.append("container.partitionKey.paths")
        elif not isinstance(partitions, list) or partitions != exp["partition_key_paths"]:
            issues.append("container.partitionKey.paths")
    if issues:
        status = "FAIL_OFFLINE_POLICY_FIXTURE" if synthetic else "FAIL_POLICY_OBSERVED"
    elif missing:
        status = "NOT_READY"
    else:
        status = "PASS_OFFLINE_FIXTURE_ONLY" if synthetic else "OBSERVED_PENDING_PRIVATE_DATA_PLANE_AND_REVIEW"
    return {**base, "status":status, "issues":sorted(set(issues)), "missing":sorted(set(missing)),
            "evidence_sha256": digest({role:observations[role]["evidence_sha256"] for role in ROLES[profile]})}


def assess_manifest(manifest: dict, evidence: dict, *, synthetic=False) -> dict:
    targets = validate_manifest(manifest)
    if not isinstance(evidence,dict) or set(evidence) != {t["profile"] for t in targets}:
        return {"status":"NOT_READY","issues":["missing or extra evidence roles"],
                "azure_live_passes":0,"release_decision":"NO_GO"}
    results = [assess_target(t, evidence[t["profile"]], synthetic=synthetic) for t in targets]
    statuses = [x["status"] for x in results]
    if any(s.startswith("FAIL") for s in statuses):
        status="FAIL_OFFLINE_POLICY_FIXTURE" if synthetic else "FAIL_POLICY_OBSERVED"
    elif "NOT_READY" in statuses:
        status="NOT_READY"
    else:
        status="PASS_OFFLINE_FIXTURES_ONLY" if synthetic else "OBSERVED_PENDING_PRIVATE_DATA_PLANE_AND_REVIEW"
    return {"status":status,"profiles":results,"target_count":len(results),
            "azure_live_passes":0,"release_decision":"NO_GO", "private_data_plane_proven":False}


def audit_client(client: AzureReadOnlyClient, manifest: dict) -> dict:
    """Optional *separately approved* ARM-only CI integration. Never public CI."""
    targets=validate_manifest(manifest)
    subs={SID_RE.match(t["resource_id"]).group(1).lower() for t in targets}
    if len(subs) != 1 or not subs.issubset(set(client.subscriptions)) or not client.read_enabled:
        raise NotReadyError("REST05 requires approved scoped read-enabled REST02 client")
    evidence={}
    for t in targets:
        roles={}
        try:
            for role in ROLES[t["profile"]]:
                roles[role]=client.get_resource(child_resource_id(t,role),t["api_version"])
        except (NotReadyError, ValueError) as exc:
            # No potentially sensitive message from cloud response is released.
            evidence[t["profile"]]=None
            continue
        evidence[t["profile"]]=roles
    return assess_manifest(manifest,evidence)


def synthetic_inputs():
    sid="01234567-89ab-4def-8123-0123456789ab"
    root=f"/subscriptions/{sid}/resourceGroups/rg-synthetic/providers/"
    m={"schema":SCHEMA,"targets":[
        {"profile":"azure_openai","resource_id":root+"Microsoft.CognitiveServices/accounts/openai-synthetic",
         "api_version":API_VERSION["azure_openai"],"expected":{
             "location":"japaneast","custom_subdomain":"openai-synthetic", "deployment_name":"test-deploy",
             "model_format":"OpenAI", "model_name":"synthetic-model", "model_version":"test-v1",
             "sku_name":"Standard", "sku_capacity":1}},
        {"profile":"ai_search","resource_id":root+"Microsoft.Search/searchServices/search-synthetic",
         "api_version":API_VERSION["ai_search"],"expected":{
             "location":"japaneast", "sku_name":"standard", "replica_count":1, "partition_count":1}},
        {"profile":"cosmos_nosql","resource_id":root+"Microsoft.DocumentDB/databaseAccounts/cosmos-synthetic",
         "api_version":API_VERSION["cosmos_nosql"],"expected":{
             "location":"japaneast", "database_name":"synthetic-db", "container_name":"synthetic-records",
             "partition_key_paths":["/tenantId"],"backup_type":"Continuous","backup_tier":"Continuous7Days","consistency_level":"Session"}}
    ]}
    ev={}
    for t in m["targets"]:
        p=t["profile"]; x=t["expected"]; obs={}
        for role in ROLES[p]:
            rid=child_resource_id(t,role)
            d={"id":rid}
            if role in ("account","service"):
                d.update({"type":ACCOUNT_TYPES[p],"location":x["location"],"properties":{
                    "publicNetworkAccess":"Disabled", "disableLocalAuth":True}})
            if p=="azure_openai":
                if role=="account":
                    d["kind"]="OpenAI";d["properties"]["customSubDomainName"]=x["custom_subdomain"]
                else:
                    d.update({"type":"Microsoft.CognitiveServices/accounts/deployments", "sku":{
                        "name":x["sku_name"],"capacity":x["sku_capacity"]},"properties":{
                        "model":{"format":x["model_format"],"name":x["model_name"],
                                 "version":x["model_version"]},"versionUpgradeOption":"NoAutoUpgrade"}})
            elif p=="ai_search":
                d["properties"].update({"networkRuleSet":{"bypass":"None"},
                    "replicaCount":x["replica_count"],"partitionCount":x["partition_count"]})
                d["sku"]={"name":x["sku_name"]}
            elif p=="cosmos_nosql":
                if role=="account":
                    d["kind"]="GlobalDocumentDB"
                    d["properties"].update({"networkAclBypass":"None", "backupPolicy":{
                        "type":"Continuous", "continuousModeProperties":{"tier":x["backup_tier"]}}, "consistencyPolicy":{"defaultConsistencyLevel":x["consistency_level"]}})
                elif role=="database":
                    d.update({"type":"Microsoft.DocumentDB/databaseAccounts/sqlDatabases", "properties":{
                        "resource":{"id":x["database_name"]}}})
                else:
                    d.update({"type":"Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers", "properties":{
                        "resource":{"id":x["container_name"],"partitionKey":{"paths":x["partition_key_paths"]}}}})
            obs[role]={"state":"OBSERVED_NOT_ACCEPTED","resource_id":rid,
                       "observation":d,"evidence_sha256":digest(d)}
        ev[p]=obs
    return m,ev


def selftest():
    m,e=synthetic_inputs()
    good=assess_manifest(m,e,synthetic=True)
    if good["status"]!="PASS_OFFLINE_FIXTURES_ONLY":
        raise AssertionError("expected safe synthetic fixture")
    bad=copy.deepcopy(e)
    bad["azure_openai"]["account"]["observation"]["properties"]["publicNetworkAccess"]="Enabled"
    d=bad["azure_openai"]["account"]
    d["evidence_sha256"]=digest(d["observation"])
    unsafe=assess_manifest(m,bad,synthetic=True)
    if unsafe["status"]!="FAIL_OFFLINE_POLICY_FIXTURE":
        raise AssertionError("unsafe public access was not detected")
    missing=copy.deepcopy(e);missing["cosmos_nosql"].pop("container")
    incomplete=assess_manifest(m,missing,synthetic=True)
    if incomplete["status"]!="NOT_READY":
        raise AssertionError("missing evidence was not marked NOT_READY")
    return {"status":"PASS_OFFLINE_FIXTURES_ONLY", "good":good["status"],
            "unsafe":unsafe["status"],"missing":incomplete["status"],
            "profiles":len(m["targets"]),"azure_live_passes":0,"release_decision":"NO_GO"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest",action="store_true")
    modes.add_argument("--fixture",type=Path)
    args=parser.parse_args()
    if args.selftest:
        result=selftest()
    else:
        doc=json.loads(args.fixture.read_text(encoding="utf-8"))
        if set(doc)!={"manifest","evidence","synthetic"} or doc["synthetic"] is not True:
            raise ValueError("CLI accepts explicitly synthetic fixtures only")
        result=assess_manifest(doc["manifest"],doc["evidence"],synthetic=True)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 0 if result["status"].startswith("PASS_OFFLINE") else 2


if __name__=="__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, json.JSONDecodeError, AssertionError) as exc:
        print(json.dumps({"status":"NOT_READY","reason":type(exc).__name__,
                          "azure_live_passes":0,"release_decision":"NO_GO"}),file=sys.stderr)
        sys.exit(2)
