#!/usr/bin/env python3
"""Observe the approved Azure Monitor Private Link path. Never changes Azure."""
import argparse
from datetime import date
import http.client
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import ssl
import time
from uuid import UUID

from azure_rest_reader import ARM_SCOPE, AzureReadOnlyClient, NotReadyError, RestFailure


ZONES = frozenset({
    "privatelink.monitor.azure.com", "privatelink.oms.opinsights.azure.com",
    "privatelink.ods.opinsights.azure.com", "privatelink.agentsvc.azure-automation.net",
    "privatelink.blob.core.windows.net",
})
QUERY_HOST = "api.loganalytics.azure.com"
QUERY_SCOPE = "https://api.loganalytics.io/.default"
NET_API = "2024-05-01"
MONITOR_API = "2021-07-01-preview"
AZURE_PRIVATE_IPV4 = tuple(map(ipaddress.ip_network, ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")))


def require(condition, reason):
    if not condition:
        raise NotReadyError(reason)


def resource_id(value, provider_type, subscriptions):
    provider, *types = provider_type.lower().split("/")
    parts = value.lower().split("/")
    require(
        len(parts) == 7 + 2 * len(types)
        and parts[:2] == ["", "subscriptions"]
        and parts[2] in subscriptions
        and parts[3] == "resourcegroups"
        and parts[5:7] == ["providers", provider]
        and parts[7::2] == types
        and all(re.fullmatch(r"[a-z0-9_-][a-z0-9_.()-]*", n) for n in [parts[4], *parts[8::2]]),
        "resource ID is invalid or outside approved subscriptions",
    )
    return value


def private_ips(values):
    require(isinstance(values, list) and bool(values), "approved endpoint IPs are missing")
    addresses = set(map(ipaddress.ip_address, values))
    require(all(any(address in net for net in AZURE_PRIVATE_IPV4) for address in addresses),
            "endpoint IPs must be RFC1918 IPv4")
    return {str(address) for address in addresses}


def read_config(config):
    require(config.get("approved_private_runner") is True and config.get("environment") == "nonproduction",
            "approved nonproduction Private Runner declaration required")
    require(config.get("mode") in ("dev", "hub"), "approved AMPLS topology is missing")
    for key in ("topology_approval_ref", "query_approval_ref", "log_source_approval_ref"):
        require(isinstance(config.get(key), str) and bool(config[key].strip()), f"{key} required")
    for key in ("tenant_id", "client_id", "workspace_guid", "transaction_guid"):
        config[key] = str(UUID(config[key]))
    require(isinstance(config["subscriptions"], list) and bool(config["subscriptions"]),
            "approved subscriptions required")
    subscriptions = [str(UUID(v)) for v in config["subscriptions"]]
    config["subscriptions"] = subscriptions
    checks = {
        "scope_id": "Microsoft.Insights/privateLinkScopes",
        "workspace_id": "Microsoft.OperationalInsights/workspaces",
        "association_id": "Microsoft.Insights/privateLinkScopes/scopedResources",
        "endpoint_id": "Microsoft.Network/privateEndpoints",
        "zone_group_id": "Microsoft.Network/privateEndpoints/privateDnsZoneGroups",
        "gateway_id": "Microsoft.Network/applicationGateways",
    }
    for field, resource_type in checks.items():
        resource_id(config[field], resource_type, subscriptions)
    require(config["association_id"].lower().startswith(config["scope_id"].lower() + "/scopedresources/")
            and config["zone_group_id"].lower().startswith(config["endpoint_id"].lower() + "/privatednszonegroups/"),
            "association or zone group does not belong to the approved parent")
    require(set(config["zone_ids"]) == ZONES, "five approved Monitor DNS zones are required")
    for name, zone in config["zone_ids"].items():
        resource_id(zone, "Microsoft.Network/privateDnsZones", subscriptions)
        require(zone.lower().rsplit("/", 1)[1] == name, "DNS zone ID does not match its zone name")
    config["endpoint_ips"] = private_ips(config["endpoint_ips"])
    hours = config.get("lookback_hours", 1)
    require(type(hours) is int and 1 <= hours <= 24, "lookback_hours must be 1..24")
    config["lookback_hours"] = hours
    return config


def properties(client, resource, api):
    return client.get_resource(resource, api)["observation"]["properties"]


def matched_endpoint(endpoint, scope_id):
    connections = endpoint.get("privateLinkServiceConnections", []) + endpoint.get("manualPrivateLinkServiceConnections", [])
    matches = [c["properties"] for c in connections
               if c["properties"]["privateLinkServiceId"].lower() == scope_id.lower()
               and set(c["properties"].get("groupIds", [])) == {"azuremonitor"}]
    require(len(matches) == 1, "expected one PE connection to the approved AMPLS/azuremonitor target")
    require(matches[0].get("privateLinkServiceConnectionState", {}).get("status") == "Approved",
            "Monitor Private Endpoint approval is pending or unavailable")
    return matches[0]


def audit_arm(client, cfg, observed):
    scope = properties(client, cfg["scope_id"], MONITOR_API)
    modes = scope.get("accessModeSettings", {})
    require(all(modes.get(key) == "PrivateOnly" for key in ("queryAccessMode", "ingestionAccessMode"))
            and not modes.get("exclusions"),
            "AMPLS must use PrivateOnly without unreviewed endpoint overrides")
    observed["AZ-T31-03"] = "OBSERVED_NOT_ACCEPTED"

    workspace = properties(client, cfg["workspace_id"], "2023-09-01")
    require(str(workspace.get("customerId", "")).lower() == cfg["workspace_guid"]
            and all(workspace.get(key) == "Disabled"
                    for key in ("publicNetworkAccessForIngestion", "publicNetworkAccessForQuery")),
            "workspace GUID or public network flags differ from baseline")
    association = properties(client, cfg["association_id"], MONITOR_API)
    require(association.get("linkedResourceId", "").lower() == cfg["workspace_id"].lower(),
            "AMPLS association points at the wrong workspace")

    matched_endpoint(properties(client, cfg["endpoint_id"], NET_API), cfg["scope_id"])
    observed["AZ-T31-09"] = "OBSERVED_NOT_ACCEPTED"
    group = properties(client, cfg["zone_group_id"], NET_API)
    zones = [item["properties"]["privateDnsZoneId"].lower() for item in group.get("privateDnsZoneConfigs", [])]
    require(len(zones) == len(ZONES) and set(zones) == {v.lower() for v in cfg["zone_ids"].values()},
            "endpoint DNS zone group differs from the approved five zones")
    observed["AZ-T31-11"] = "OBSERVED_NOT_ACCEPTED"


def resolve_private(host, approved, resolver=socket.getaddrinfo):
    addresses = {entry[4][0] for entry in resolver(host, 443, type=socket.SOCK_STREAM)}
    require(addresses and addresses <= approved,
            "Monitor DNS returned no address or an address outside the approved endpoint IPs")
    return sorted(addresses)


class PrivateHTTPSConnection(http.client.HTTPSConnection):
    """Connect to the already checked IP while retaining canonical host TLS validation."""
    def __init__(self, host, address):
        super().__init__(host, timeout=8, context=ssl.create_default_context())
        self.address = address

    def connect(self):
        with socket.create_connection((self.address, 443), timeout=self.timeout) as raw:
            self.sock = self._context.wrap_socket(raw.dup(), server_hostname=self.host)


def check_transport(addresses):
    for host, ips in addresses.items():
        for address in ips:
            connection = PrivateHTTPSConnection(host, address)
            try:
                connection.connect()
            finally:
                connection.close()


def read_log_count(connection, cfg, token):
    # UUID and validated ARM resource ID only; no externally supplied KQL.
    transaction = UUID(cfg["transaction_guid"]).hex
    query = (f"AGWAccessLogs | where tolower(_ResourceId) == '{cfg['gateway_id'].lower()}' "
             f"| where replace_string(tolower(tostring(TransactionId)), '-', '') == '{transaction}' "
             "| count")
    body = json.dumps({"query": query, "timespan": f"PT{cfg['lookback_hours']}H"})
    connection.request("POST", f"/v1/workspaces/{cfg['workspace_guid']}/query", body, {
        "Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8",
    })
    response = connection.getresponse()
    require(response.status == 200, f"bounded Log Analytics query HTTP status {response.status}")
    raw = response.read(65_537)
    require(len(raw) <= 65_536, "Log Analytics response exceeded limit")
    data = json.loads(raw)
    require("error" not in data and len(data.get("tables", [])) == 1, "log query result incomplete or partial")
    rows = data["tables"][0]["rows"]
    require(len(rows) == 1 and len(rows[0]) == 1 and type(rows[0][0]) is int and rows[0][0] >= 0,
            "invalid aggregate Log Analytics result")
    return rows[0][0]


def await_log(cfg, address, token, attempts=6, sleeper=time.sleep):
    for attempt in range(attempts):
        connection = PrivateHTTPSConnection(QUERY_HOST, address)
        try:
            if read_log_count(connection, cfg, token) > 0:
                return
        finally:
            connection.close()
        if attempt + 1 < attempts:
            sleeper(10)
    raise NotReadyError("approved Gateway log did not arrive in the query window")


def credential_for(cfg):
    require(os.environ.get("AZURE_TENANT_ID", "").lower() == cfg["tenant_id"]
            and os.environ.get("AZURE_CLIENT_ID", "").lower() == cfg["client_id"]
            and Path(os.environ.get("AZURE_FEDERATED_TOKEN_FILE", "")).is_file(),
            "approved OIDC identity or token file is unavailable")
    try:
        from azure.identity import WorkloadIdentityCredential
    except ImportError as exc:
        raise NotReadyError("approved azure-identity dependency is unavailable") from exc
    return WorkloadIdentityCredential()


def run_live(cfg, observed):
    credential = credential_for(cfg)
    arm = AzureReadOnlyClient(cfg["subscriptions"], lambda: credential.get_token(ARM_SCOPE).token, read_enabled=True)
    audit_arm(arm, cfg, observed)
    hosts = (QUERY_HOST, f"{cfg['workspace_guid']}.ods.opinsights.azure.com",
             f"{cfg['workspace_guid']}.oms.opinsights.azure.com")
    addresses = {host: resolve_private(host, cfg["endpoint_ips"]) for host in hosts}
    check_transport(addresses)
    try:
        token = credential.get_token(QUERY_SCOPE).token
    except Exception as exc:
        raise NotReadyError("Log Analytics OIDC token unavailable") from exc
    await_log(cfg, addresses[QUERY_HOST][0], token)
    observed.update({f"AZ-T31-{i:02}": "OBSERVED_NOT_ACCEPTED" for i in (5, 13, 15)})


def review_supporting_controls(document):
    """Compare supplied evidence to a baseline, with no runtime acceptance claim."""
    checks = {f"AZ-T31-{i:02}": "NOT_READY" for i in (8, 18, 20, 22)}
    as_of = date.fromisoformat(document["as_of"])
    workspace = str(document["workspace_id"]).lower()
    for number, field, predicate in (
        (8, "app_insights", lambda obj: bool(workspace) and obj["workspace_id"].lower() == workspace),
        (18, "query_role", lambda obj: bool(workspace)
         and obj["scope_id"].lower() == workspace
         and UUID(obj["principal_id"]) == UUID(obj["approved_principal_id"])
         and UUID(obj["role_guid"]) == UUID(obj["approved_role_guid"])),
        (20, "public_exceptions", lambda entries: isinstance(entries, list) and all(
            all(isinstance(entry[k], str) and bool(entry[k].strip()) for k in ("purpose", "owner", "scope"))
            and date.fromisoformat(entry["expires"]) > as_of for entry in entries
        )),
        (22, "absence_alert", lambda obj: bool(workspace) and obj["workspace_id"].lower() == workspace
         and obj["enabled"] is True and obj["checks_absence"] is True
         and bool(obj["approved_action_group_id"])
         and obj["action_group_id"].lower() == obj["approved_action_group_id"].lower()),
    ):
        if field in document:
            try:
                state = "MATCHED_OFFLINE" if predicate(document[field]) else "MISMATCH_OFFLINE"
            except (KeyError, TypeError, ValueError, AttributeError):
                state = "NOT_READY"
            checks[f"AZ-T31-{number:02}"] = state
    return checks


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--live", action="store_true")
    modes.add_argument("--review-file", type=Path, help="compare supporting control evidence offline")
    parser.add_argument("--config", type=Path)
    args = parser.parse_args(argv)
    checks = {f"AZ-T31-{i:02}": "NOT_READY" for i in range(1, 22, 2)}
    report = {"status": "NOT_READY", "checks": checks, "azure_live_passes": 0, "release_decision": "NO_GO"}
    try:
        if args.review_file is not None:
            with args.review_file.open("rb") as stream:
                raw = stream.read(65_537)
            require(len(raw) <= 65_536, "offline supporting evidence exceeds size limit")
            checks = review_supporting_controls(json.loads(raw))
            report.update(checks=checks)
            if all(value == "MATCHED_OFFLINE" for value in checks.values()):
                report.update(status="MATCHED_OFFLINE")
            else:
                report.update(reason="supporting evidence is missing or differs from its baseline")
        else:
            require(args.live and args.config is not None, "explicit --live and approved --config required")
            with args.config.open("rb") as stream:
                raw = stream.read(65_537)
            require(len(raw) <= 65_536, "approved config exceeds size limit")
            run_live(read_config(json.loads(raw)), checks)
            report.update(status="OBSERVED_NOT_ACCEPTED",
                          remaining="Decision review, App Insights, effective RBAC, exceptions and alert delivery require separate evidence.")
    except NotReadyError as exc:
        report["reason"] = str(exc)
    except (OSError, RestFailure, http.client.HTTPException):
        report["reason"] = "approved file, DNS/TLS connection or Azure response unavailable"
    except (ValueError, KeyError, TypeError, AttributeError, IndexError):
        report["reason"] = "approved config or Azure response is incomplete or invalid"
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] in ("OBSERVED_NOT_ACCEPTED", "MATCHED_OFFLINE") else 2


if __name__ == "__main__":
    raise SystemExit(main())
