"""AZ-T29 scoped egress, Private Runner and identity observations."""
from __future__ import annotations

import argparse
import base64
from datetime import date
import ipaddress
import json
import logging
from http.client import HTTPException
import os
from pathlib import Path
import re
from uuid import UUID

from azure_gateway_step28 import egress, parse_nsg
from azure_monitor_private_audit import PrivateHTTPSConnection, resource_id
from azure_private_dns_step30 import InputIssue, Mismatch, check_addresses, dig_query, name, read_file, reports, require
from azure_private_endpoint_step26 import NET_API, NETWORK, assoc, expect, observed, private_networks, review_flow, route_policy, subnet_prefixes, usable
from azure_rest_reader import ARM_HOST, ARM_SCOPE, AzureReadOnlyClient, NotReadyError, RestFailure
from rest04_private_dns_audit import private_ip


AUTHORITY = "https://login.microsoftonline.com"
GITHUB_ISSUER = "https://token.actions.githubusercontent.com"
EXCHANGE_AUDIENCE = "api://AzureADTokenExchange"
CATEGORIES = {1: "entra", 3: "monitor", 7: "certificate_validation", 17: "all"}
KINDS = {1: "entra_dependency_review", 3: "monitor_dependency_review", 5: "private_dns",
         7: "certificate_dependency_review", 9: "nsg_configuration", 11: "effective_next_hop_extract",
         13: "route_and_firewall_configuration", 15: "denied_egress_flow_extract",
         17: "ownership_review", 19: "private_https", 21: "denial_telemetry_extract"}


def ready(condition, reason):
    expect(condition, reason, NotReadyError)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def authority_check(cloud, tenant_id, issuer):
    require(cloud == "AzurePublic", "only AzurePublic is supported; other cloud endpoints need a reviewed profile")
    tenant = str(UUID(tenant_id))
    require(issuer == f"{AUTHORITY}/{tenant}/v2.0", "authority or tenant differs from approved AzurePublic profile")
    return tenant


def identity_contract(config):
    tenant = config["tenant_id"]
    auth = config["identity"]
    require(set(auth) == {"app", "managed", "github"}, "separate app, managed identity and GitHub contracts required")
    app, mi, gh = (auth[key] for key in ("app", "managed", "github"))
    authority_check(config["cloud"], tenant, app["issuer"])
    require(text(app["audience"]) and "*" not in app["audience"] and text(app["design_ref"]),
            "exact approved application audience and design reference required")
    require(mi.get("platform") == "app_service" and text(mi["audience"]) and "*" not in mi["audience"],
            "managed identity needs an approved App Service resource audience")
    UUID(mi["client_id"])
    UUID(gh["client_id"])
    require(gh["issuer"] == GITHUB_ISSUER and gh["exchange_audience"] == EXCHANGE_AUDIENCE
            and gh["resource_scope"] == ARM_SCOPE,
            "GitHub issuer, exchange audience or ARM resource scope is not the approved public-cloud value")
    subject_prefix = "repo:tayoshik/azure-private-ai-assurance:"
    require(isinstance(gh["subject"], str) and gh["subject"].startswith(
                (subject_prefix + "ref:refs/heads/", subject_prefix + "environment:"))
            and bool(gh["subject"].rsplit(":", 1)[-1])
            and "*" not in gh["subject"] and all(ch.isprintable() and not ch.isspace() for ch in gh["subject"]),
            "exact approved GitHub ref/environment subject required")
    return auth


def dependency_key(row):
    return (row["category"], row["actor"], name(row["host"]), row["port"], row["control"])


def validate(config):
    require(config.get("schema") == "azure-entra-egress/az-t29/v1", "unknown Entra egress schema")
    require(config.get("environment") == "nonproduction" and config.get("topology") in ("hub", "dev")
            and config.get("approved_private_runner") is True, "approved nonproduction topology and Private Runner required")
    require(text(config.get("approval_ref")) and text(config.get("scope_ref")), "approved dependency scope required")
    config["tenant_id"] = authority_check(config["cloud"], config["tenant_id"], config["entra_issuer"])
    identity_contract(config)
    dependencies = config["dependencies"]
    require(isinstance(dependencies, list) and 1 <= len(dependencies) <= 80, "explicit bounded dependencies required")
    seen = set()
    for row in dependencies:
        key = dependency_key(row)
        category, actor, _, port, control = key
        require(category in ("entra", "monitor", "certificate_validation")
                and actor in ("app_browser", "app_service", "github_runner", "private_runner", "gateway")
                and type(port) is int and (port == 443 or category == "certificate_validation" and port == 80)
                and control in ("firewall", "proxy", "private_dns_firewall"),
                "unknown dependency category/control or unapproved port")
        require(all(text(row[field]) for field in ("purpose", "owner", "approval_ref")), "dependency ownership fields required")
        expires = date.fromisoformat(row["expires"])
        require(expires >= date.today(), "approved dependency expired")
        require(key not in seen, "duplicate dependency declaration")
        seen.add(key)
    require({(category, actor) for category, actor, host, port, _ in seen
             if host == "login.microsoftonline.com" and port == 443}
            >= {("entra", "app_browser"), ("entra", "github_runner")},
            "separately approved browser and GitHub Entra authority dependencies required")
    require({row["category"] for row in dependencies} == {"entra", "monitor", "certificate_validation"},
            "Entra, Monitor and certificate-validation dependency inventories required")
    return config


def review_policy(config, document, category="all"):
    ready(document.get("complete") is True and document.get("scope_ref") == config["scope_ref"]
          and text(document.get("collection_ref")), "complete reviewed effective Firewall/Proxy export required")
    ready(document.get("no_bypass_reviewed") is True and document.get("dns_view_reviewed") is True,
          "effective Firewall/Proxy path, DNS and bypass risk need independent review")
    # The export is normalized from source policy. NSG/UDR shape is not an FQDN control.
    expected = {dependency_key(row) for row in config["dependencies"]
                if category == "all" or row["category"] == category}
    rules = document.get("allows")
    ready(isinstance(rules, list), "FQDN allowance inventory unavailable")
    relevant = [row for row in rules if category == "all" or row["category"] == category]
    try:
        keys = {dependency_key(row) for row in relevant}
    except (InputIssue, ValueError) as exc:
        raise Mismatch("Firewall/Proxy export contains wildcard or unsupported hostname") from exc
    expect(keys == expected and len(keys) == len(relevant), "Firewall/Proxy allow inventory missing or exceeds scope")
    ready(document.get("default_unapproved_deny") is True,
          "unapproved egress policy not evidenced in the effective-rule export")


def private_input(config):
    data = config["private_target"]
    host = name(data["host"])
    chain = data["chain"]
    require(isinstance(chain, list) and 1 <= len(chain) <= 9 and all(name(item) for item in chain)
            and chain[0] == host and len(chain) == len(set(chain)), "explicit private DNS alias path required")
    require(private_ip(data["resolver_ip"]), "approved private resolver IP required")
    networks = private_networks(data["cidrs"])
    addresses = data["ips"]
    require(isinstance(addresses, list) and 1 <= len(addresses) <= 8 and len(set(addresses)) == len(addresses)
            and all(private_ip(ip) and any(ipaddress.IPv4Address(ip) in net for net in networks) for ip in addresses),
            "exact approved private addresses and subnet ranges required")
    return data


def dns_observe(config, query=dig_query):
    data = private_input(config)
    check_addresses(query(data["resolver_ip"], data["host"], "A"), data["chain"], data["ips"])
    return data


def health_observe(config, query=dig_query, connection=PrivateHTTPSConnection):
    data = private_input(config)
    path = data["health_path"]
    require(isinstance(path, str) and path.startswith("/") and "//" not in path and "?" not in path and "#" not in path
            and "%" not in path and ".." not in path.split("/") and all(32 < ord(ch) < 127 for ch in path),
            "approved literal private health path required")
    require(type(data["health_status"]) is int and 200 <= data["health_status"] <= 299,
            "approved successful HTTP result required")
    dns_observe(config, query)
    for ip in data["ips"]:
        with_connection = connection(data["host"], ip)
        try:
            with_connection.request("GET", path, headers={"Accept": "application/json"})
            expect(with_connection.getresponse().status == data["health_status"], "private HTTPS status differs from approval")
        finally:
            with_connection.close()


def arm_input(config):
    baseline = config["network"]
    subscriptions = [str(UUID(item)) for item in config["subscriptions"]]
    require(bool(subscriptions), "approved ARM subscription required")
    for field, kind in (("subnet_id", "virtualNetworks/subnets"), ("nsg_id", "networkSecurityGroups"),
                        ("route_table_id", "routeTables")):
        if baseline[field] is not None or field != "route_table_id":
            require(baseline[field].startswith("/subscriptions/"), "canonical ARM resource ID required")
            resource_id(baseline[field], NETWORK + kind, subscriptions)
    source = private_networks(baseline["cidrs"])
    require(isinstance(baseline["egress"], list) and 1 <= len(baseline["egress"]) <= 32,
            "approved complete subnet egress legs required")
    for leg in baseline["egress"]:
        require(leg["protocol"] in ("tcp", "udp") and type(leg["port"]) is int and 1 <= leg["port"] <= 65535
                and isinstance(leg["destinations"], list) and bool(leg["destinations"]),
                "approved bounded egress legs require protocol, port and destinations")
        private_networks(leg["destinations"])
    pe = private_networks(baseline["paas_pe_cidrs"])
    require(set(pe) <= {net for leg in baseline["egress"] if (leg["protocol"], leg["port"]) == ("tcp", 443)
                        for net in private_networks(leg["destinations"])},
            "approved PaaS ranges must be covered by explicit TCP 443 egress legs")
    require(isinstance(baseline["expected_routes"], list) and (baseline["route_table_id"] or not baseline["expected_routes"]),
            "explicit route inventory required")
    return baseline, source


def read_arm(config, client):
    baseline, source = arm_input(config)

    def get(key):
        rid = baseline[key]
        return client.get_resource(rid, NET_API)["observation"] if rid is not None else None

    def scoped_subnet():
        subnet = usable(get("subnet_id"))
        expect(subnet_prefixes(subnet) == set(source), "subnet IPAM differs from approval")
        return subnet

    def nsg():
        assoc(scoped_subnet(), baseline["nsg_id"], "networkSecurityGroup")
        egress(parse_nsg(get("nsg_id"))["Outbound"], baseline)

    def route():
        route_policy(scoped_subnet(), get("route_table_id"), baseline)

    report = pending("separate approved evidence or Private Runner observation required")
    for key, check, note in ((9, nsg, "configured NSG CIDRs and precedence only; peer PE policy and reachability unobserved"),
                             (13, route, "attached route table and next hops only; actual Firewall/Proxy path unobserved")):
        state, reason = observed(check)
        report[key] = ("CONFIG_OBSERVED_NOT_ACCEPTED", note) if state == "OBSERVED_NOT_ACCEPTED" else (state, reason)
    return report


def review_next_hop(config, document):
    expected = config["effective_next_hop"]
    ready(document.get("scope_ref") == config["scope_ref"] and document.get("complete") is True
          and text(document.get("collection_ref")), "reviewed effective next-hop extract required")
    for field in ("source_ip", "destination_ip", "hop_ip"):
        require(private_ip(expected[field]), "approved private next-hop tuple required")
    expect(all(document.get(field) == expected[field] for field in ("source_ip", "destination_ip", "hop_ip", "hop_type")),
           "effective next-hop tuple differs from approved NVA/firewall route")


def review_denied(config, document):
    plan = config["deny_evidence"]
    ready(document.get("scope_ref") == config["scope_ref"] and document.get("complete") is True
          and document.get("source_type") in ("vnet_flow", "firewall_flow"), "only scoped Firewall or VNet Flow evidence qualifies")
    destination = ipaddress.IPv4Address(plan["destination_ip"])
    require(plan.get("direction") == "deny" and private_ip(plan["source_ip"]) and destination.is_global
            and plan.get("isolated_scope_approved") is True and text(plan.get("approval_ref")),
            "approved isolated public-egress denial tuple required")
    ready(text(document.get("collection_ref")), "approved flow collection reference required")
    review_flow(document, plan)


def review_auth(config, document):
    auth = identity_contract(config)
    actor = document.get("flow")
    ready(actor in auth and document.get("scope_ref") == config["scope_ref"] and text(document.get("collector_ref")),
          "approved identity observation extract required")
    expected = auth[actor]
    expect(document.get("tenant_id") == config["tenant_id"] and document.get("cloud") == config["cloud"],
           "identity evidence tenant or cloud differs from approval")
    target_audience = expected["audience"] if actor != "github" else ARM_HOST
    expect(document.get("target_audience") == target_audience, "target token audience differs from approval")
    if actor == "github":
        expect(all(document.get(key) == expected[key] for key in ("issuer", "subject", "exchange_audience")),
               "federated issuer, subject or exchange audience differs from approval")
    elif actor == "app":
        expect(document.get("issuer") == expected["issuer"], "application issuer differs from approval")
    else:
        expect(document.get("client_id") == expected["client_id"], "managed identity differs from approval")
    states = {}
    for key in ("transport", "token_acquisition", "target_authorization"):
        outcome = document.get(key)
        states[key] = ("EXTRACT_OBSERVED_NOT_ACCEPTED" if outcome == "observed" else
                       "NOT_READY" if outcome in ("unavailable", "not_run", "denied", None) else "FAIL")
    if states["transport"] != "EXTRACT_OBSERVED_NOT_ACCEPTED":
        states["token_acquisition"] = states["target_authorization"] = "NOT_READY"
    if states["token_acquisition"] != "EXTRACT_OBSERVED_NOT_ACCEPTED":
        states["target_authorization"] = "NOT_READY"
    return states


def discover(config, connection=None):
    if connection is None:
        from http.client import HTTPSConnection
        connection = HTTPSConnection
    conn = connection("login.microsoftonline.com", timeout=8)
    tenant = config["tenant_id"]
    try:
        conn.request("GET", f"/{tenant}/v2.0/.well-known/openid-configuration", headers={"Accept": "application/json"})
        rsp = conn.getresponse()
        ready(rsp.status == 200, "tenant discovery HTTPS unavailable")
        raw = rsp.read(32769)
        ready(len(raw) <= 32768, "tenant discovery projection too large")
        metadata = json.loads(raw)
        expect(metadata.get("issuer") == config["entra_issuer"]
               and metadata.get("token_endpoint") == f"{AUTHORITY}/{tenant}/oauth2/v2.0/token",
               "discovery metadata issuer/token endpoint mismatches approved tenant")
    finally:
        conn.close()


def auth_probe_input(config):
    setup = config["github_auth_probe"]
    require(setup.get("explicit_auth_approved") is True and text(setup.get("auth_approval_ref"))
            and setup.get("direct_https_approved") is True,
            "explicit approval for scoped GitHub OIDC, read target and direct HTTPS required")
    subscriptions = [str(UUID(value)) for value in config["subscriptions"]]
    require(setup["arm_read_id"].startswith("/subscriptions/"), "canonical ARM read ID required")
    resource_id(setup["arm_read_id"], "Microsoft.Web/sites", subscriptions)
    return setup, subscriptions


def checked_assertion(path, expected):
    with path.open("rb") as stream:
        raw = stream.read(32769).strip()
    ready(len(raw) <= 32768, "workload assertion projection too large")
    parts = raw.split(b".")
    ready(len(parts) == 3 and all(re.fullmatch(rb"[A-Za-z0-9_-]+", part) for part in parts),
          "workload assertion is not a compact signed token")
    payload = parts[1]
    claims = json.loads(base64.urlsafe_b64decode(payload + b"=" * (-len(payload) % 4)))
    ready(isinstance(claims, dict) and claims.get("iss") == expected["issuer"]
          and claims.get("sub") == expected["subject"]
          and claims.get("aud") in (expected["exchange_audience"], [expected["exchange_audience"]]),
          "assertion issuer, subject or exchange audience differs from approval")
    # Prefilter untrusted metadata only. Entra validates the assertion.
    return raw.decode("ascii")


def oidc_credential(config):
    identity = config["identity"]["github"]
    client_id = str(UUID(identity["client_id"]))
    tenant = config["tenant_id"]
    ready(os.environ.get("AZURE_TENANT_ID", "").lower() == tenant
          and os.environ.get("AZURE_CLIENT_ID", "").lower() == client_id
          and os.environ.get("AZURE_AUTHORITY_HOST", AUTHORITY).rstrip("/") == AUTHORITY,
          "OIDC client, tenant or authority environment differs from approval")
    token_path = os.environ.get("AZURE_FEDERATED_TOKEN_FILE", "")
    ready(bool(token_path) and Path(token_path).is_file(), "approved GitHub workload token file unavailable")
    assertion = checked_assertion(Path(token_path), identity)
    try:
        from azure.identity import ClientAssertionCredential
    except ImportError as exc:
        raise NotReadyError("approved azure-identity dependency unavailable") from exc
    return ClientAssertionCredential(tenant, client_id, lambda: assertion, authority=AUTHORITY, logging_enable=False)


def client_for(config):
    arm_input(config)
    identity = oidc_credential(config)
    return AzureReadOnlyClient(config["subscriptions"], lambda: identity.get_token(ARM_SCOPE).token, read_enabled=True)


def auth_probe(config, *, transport=discover, credential=oidc_credential, client_factory=AzureReadOnlyClient):
    setup, subscriptions = auth_probe_input(config)
    state = {"transport": "NOT_READY", "token_acquisition": "NOT_READY", "target_authorization": "NOT_READY"}
    phases = (
        ("transport", lambda: transport(config)),
        ("token_acquisition", lambda: mint()),
        ("target_authorization", lambda: authorize()),
    )
    token = None

    def mint():
        nonlocal token
        try:
            identity = credential(config)
            try:
                token = identity.get_token(ARM_SCOPE).token
            finally:
                identity.close()
        except Exception as exc:
            # SDK or identity responses can contain sensitive details. Never serialize them.
            raise NotReadyError("approved workload token exchange unavailable") from exc
        ready(text(token), "approved workload token unavailable")

    def authorize():
        client_factory(subscriptions, lambda: token, read_enabled=True).get_resource(setup["arm_read_id"], "2024-11-01")

    for key, action in phases:
        try:
            status, _ = observed(action)
        except HTTPException:
            status = "NOT_READY"
        state[key] = status
        if status != "OBSERVED_NOT_ACCEPTED":
            break
    return state


def pending(reason):
    return {i: ("NOT_READY", reason) for i in range(1, 23)}


def result_for_states(states, *, source):
    codes = set(states.values())
    state = "FAIL" if "FAIL" in codes else "NOT_READY" if "NOT_READY" in codes else "OBSERVED_NOT_ACCEPTED"
    return state, source + ": " + ", ".join(f"{key}={value}" for key, value in states.items())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    options = ("check-config", "live-arm", "live-dns", "live-health", "live-auth",
               "review-policy", "review-hop", "review-denied", "review-auth")
    for option in options:
        modes.add_argument("--" + option, action="store_true")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    os.umask(0o077)
    mode = next((option for option in options if getattr(args, option.replace("-", "_"))), "not-run")
    result = pending("explicit mode and approved configuration required")
    if mode in ("live-arm", "live-auth"):
        # Suppress third-party SDK diagnostic messages; only bounded statuses leave this tool.
        sdk_log = logging.getLogger("azure")
        sdk_log.addHandler(logging.NullHandler())
        sdk_log.propagate = False
    selected = {"live-dns": 5, "live-health": 19, "live-auth": 1, "review-hop": 11,
                "review-denied": 15, "review-auth": 1}.get(mode)
    code = 2
    try:
        require(mode != "not-run" and args.config is not None, "explicit mode and approved configuration required")
        config = validate(read_file(args.config))
        if mode == "check-config":
            if "private_target" in config:
                private_input(config)
            if "network" in config:
                arm_input(config)
            if "github_auth_probe" in config:
                auth_probe_input(config)
            result = pending("approved input shape checked offline; Azure checks unexecuted")
            code = 0
        elif mode == "live-arm":
            result = read_arm(config, client_for(config))
            codes = [result[i][0] for i in (9, 13)]
            code = 1 if "FAIL" in codes else 2 if "NOT_READY" in codes else 0
        elif mode in ("live-dns", "live-health"):
            action = dns_observe if mode == "live-dns" else health_observe
            result[selected] = observed(lambda: action(config))
            code = {"FAIL": 1, "NOT_READY": 2}.get(result[selected][0], 0)
        elif mode == "live-auth":
            result[1] = result_for_states(auth_probe(config), source="scoped workload observation")
            code = {"FAIL": 1, "NOT_READY": 2}.get(result[1][0], 0)
        else:
            require(args.evidence is not None, "approved evidence extract required")
            doc = read_file(args.evidence)
            if mode == "review-policy":
                for key, category in CATEGORIES.items():
                    state, reason = observed(lambda: review_policy(config, doc, category))
                    result[key] = (("NOT_READY", "scoped policy content matches; owner approval and provenance remain required")
                                   if state == "OBSERVED_NOT_ACCEPTED" else (state, reason))
                code = 1 if any(result[key][0] == "FAIL" for key in CATEGORIES) else 2
            elif mode == "review-auth":
                result[1] = result_for_states(review_auth(config, doc), source="identity extract")
                code = {"FAIL": 1, "NOT_READY": 2}.get(result[1][0], 0)
            elif mode == "review-hop":
                review_next_hop(config, doc)
                result[11] = ("EXTRACT_MATCHED_NOT_ACCEPTED", "effective hop content matches; collection provenance unconfirmed")
                code = 0
            else:
                review_denied(config, doc)
                result[15] = ("EXTRACT_MATCHED_NOT_ACCEPTED", "approved denial tuple and decision match; authenticity unconfirmed")
                result[21] = ("EXTRACT_MATCHED_NOT_ACCEPTED", "scoped firewall or flow telemetry content matches; authenticity unconfirmed")
                code = 0
    except Mismatch as exc:
        result[selected or 1] = ("FAIL", str(exc))
        if mode == "review-denied":
            result[21] = result[15]
        code = 1
    except (InputIssue, NotReadyError) as exc:
        if selected:
            result[selected] = ("NOT_READY", str(exc))
        else:
            result = pending(str(exc))
        if mode == "review-denied":
            result[21] = result[15]
    except (ValueError, TypeError, KeyError, AttributeError, IndexError, OSError, RestFailure, HTTPException):
        reason = "approved inputs or complete observations unavailable"
        if selected:
            result[selected] = ("NOT_READY", reason)
        else:
            result = pending(reason)
        if mode == "review-denied":
            result[21] = result[15]
    reports(result, mode, args.out, step=29, kinds=KINDS)
    print(f"AZ-T29 mode={mode} Azure acceptance=0 exit={code}; JSON and JUnit written")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
