"""AZ-T28: scoped private WAF_v2 Application Gateway observations."""
from __future__ import annotations

import argparse
from datetime import datetime
import ipaddress
import os
from pathlib import Path
import re
import socket
from uuid import UUID

from azure_monitor_private_audit import resource_id
from azure_private_dns_step30 import InputIssue, Mismatch, read_file, reports, require
from azure_private_endpoint_step26 import (
    NET_API, NETWORK, assoc, array, client_for, expect, observed, private_networks,
    review_flow, route_policy, rule_values, subnet_prefixes, usable,
)
from azure_rest_reader import NotReadyError, RestFailure
from rest04_private_dns_audit import private_ip


KINDS = {1: "client_https_configuration_or_tcp", 3: "approved_client_cidrs",
         5: "load_balancer_precedence", 7: "platform_profile_review",
         9: "control_egress_and_udr_configuration", 11: "precedence_or_tcp_flow",
         13: "rule_order", 15: "gateway_arm_health", 17: "backend_evidence_review",
         19: "change_approval_review", 21: "activity_ticket_evidence_review"}
AZURE_LB_IPV4 = ipaddress.IPv4Network("168.63.129.16/32")
PROTOCOLS = {"*", "tcp", "udp", "icmp", "esp", "ah"}
DEFAULT = {"Inbound": {"allowvnetinbound": 65000, "allowazureloadbalancerinbound": 65001,
                       "denyallinbound": 65500},
           "Outbound": {"allowvnetoutbound": 65000, "allowinternetoutbound": 65001,
                        "denyalloutbound": 65500}}


def address(value):
    if value == "*":
        return value
    try:
        return ipaddress.IPv4Network(value)
    except ValueError:
        expect(isinstance(value, str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9.]{0,100}", value),
               "unsupported NSG address projection", NotReadyError)
        return value.lower()


def port(value):
    if value == "*":
        return 0, 65535
    pieces = str(value).split("-")
    expect(len(pieces) in (1, 2) and all(item.isdecimal() for item in pieces),
           "invalid NSG port projection", NotReadyError)
    low, high = int(pieces[0]), int(pieces[-1])
    expect(0 <= low <= high <= 65535, "invalid NSG port range", NotReadyError)
    return low, high


def validate(cfg):
    require(cfg.get("schema") == "azure-private-gateway/az-t28/v1", "unknown Gateway manifest schema")
    require(cfg.get("environment") == "nonproduction" and cfg.get("topology") in ("hub", "dev")
            and cfg.get("approved_private_runner") is True, "approved nonproduction Hub/dev scope and Private Runner required")
    for key in ("approval_ref", "network_isolation_review_ref", "egress_review_ref"):
        require(isinstance(cfg.get(key), str) and cfg[key].strip(), f"{key} required")
    require(cfg.get("profile") == "private_waf_v2_network_isolation",
            "only reviewed private WAF_v2 Network Isolation is supported")
    require(isinstance(cfg["subscriptions"], list) and 1 <= len(cfg["subscriptions"]) <= 5,
            "approved ARM subscriptions required")
    cfg["subscriptions"] = [str(UUID(value)) for value in cfg["subscriptions"]]
    for field, kind in (("gateway_id", "applicationGateways"), ("vnet_id", "virtualNetworks"),
                        ("subnet_id", "virtualNetworks/subnets"), ("nsg_id", "networkSecurityGroups"),
                        ("route_table_id", "routeTables")):
        if field != "route_table_id" or cfg[field] is not None:
            resource_id(cfg[field], NETWORK + kind, cfg["subscriptions"])
            require(cfg[field].startswith("/subscriptions/"), "canonical absolute ARM IDs required")
    require(cfg["subnet_id"].lower().startswith(cfg["vnet_id"].lower() + "/subnets/"),
            "Gateway subnet must belong to the approved VNet")
    nets = private_networks(cfg["cidrs"])
    clients = private_networks(cfg["client_cidrs"])
    denied = private_networks(cfg.get("deny_test_cidrs", []), allow_empty=True)
    require(not any(block.overlaps(c) for block in denied for c in clients),
            "approved deny CIDRs must be outside approved client ranges")
    require(all(not client.overlaps(net) for client in clients for net in nets),
            "Gateway and client CIDRs cannot overlap in this profile")
    require(private_ip(cfg["frontend_ip"]) and any(ipaddress.IPv4Address(cfg["frontend_ip"]) in n for n in nets),
            "approved private frontend must be in the Gateway subnet")
    require(isinstance(cfg["expected_routes"], list) and (cfg["route_table_id"] or not cfg["expected_routes"]),
            "explicit approved route baseline required")
    for row in cfg["expected_routes"]:
        ipaddress.IPv4Network(row["prefix"])
        require(row["next_hop_type"] in {"VirtualAppliance", "Internet", "VnetLocal", "VirtualNetworkGateway", "None"},
                "unsupported route next hop")
        require(private_ip(row.get("next_hop_ip")) if row["next_hop_type"] == "VirtualAppliance"
                else row.get("next_hop_ip") is None, "invalid route next hop input")
    require(set(cfg["approved_priorities"]) == set(DEFAULT), "approve custom priorities for both directions")
    for values in cfg["approved_priorities"].values():
        require(isinstance(values, list) and bool(values) and all(type(v) is int and 100 <= v <= 4096 for v in values)
                and values == sorted(set(values)), "priorities must be unique, ordered and between 100 and 4096")
    require(isinstance(cfg["egress"], list) and 1 <= len(cfg["egress"]) <= 32,
            "approved, bounded egress dependency list required")
    for leg in cfg["egress"]:
        port_value = leg["port"]
        require(leg["protocol"] in ("tcp", "udp") and type(port_value) is int and 1 <= port_value <= 65535,
                "egress dependency requires exact TCP/UDP port")
        require(isinstance(leg.get("purpose"), str) and leg["purpose"].strip(), "egress purpose required")
        require(isinstance(leg["destinations"], list) and 1 <= len(leg["destinations"]) <= 32,
                "explicit approved destination(s) required")
        for item in leg["destinations"]:
            dest = address(item)
            require(dest not in {"*", "internet", "virtualnetwork"} and
                    (not isinstance(dest, ipaddress.IPv4Network) or dest.prefixlen > 0),
                    "broad egress dependencies are unsupported")
    return cfg


def selector(rule, side):
    plain = rule_values(rule, side + "AddressPrefix", side + "AddressPrefixes")
    asgs = rule.get(side + "ApplicationSecurityGroups") or []
    expect(bool(plain) != bool(asgs), "missing or mixed address and ASG selectors", NotReadyError)
    # ASG membership is dynamic. Preserve its identity but never infer membership.
    return tuple(address(value) for value in plain) or tuple(("asg", item["id"].lower()) for item in asgs)


def addresses_overlap(a, b):
    if "*" in (a, b) or a == b:
        return True
    a = AZURE_LB_IPV4 if a == "azureloadbalancer" else a
    b = AZURE_LB_IPV4 if b == "azureloadbalancer" else b
    if isinstance(a, ipaddress.IPv4Network) and isinstance(b, ipaddress.IPv4Network):
        return a.overlaps(b)
    return None


def contains(outer, inner):
    return outer == "*" or outer == inner or (
        isinstance(outer, ipaddress.IPv4Network) and isinstance(inner, ipaddress.IPv4Network)
        and inner.subnet_of(outer)
    )


def overlap(left, right):
    values = [addresses_overlap(a, b) for a in left for b in right]
    return True if True in values else None if None in values else False


def parse_nsg(body):
    props = usable(body)
    result = {key: [] for key in DEFAULT}
    defaults = {key: {} for key in DEFAULT}
    for field in ("securityRules", "defaultSecurityRules"):
        for item in array(props, field):
            expect(not item.get("nextLink"), "incomplete rule projection", NotReadyError)
            rule = item["properties"]
            direction = rule.get("direction")
            proto = str(rule.get("protocol")).lower()
            priority = rule.get("priority")
            expect(direction in DEFAULT and proto in PROTOCOLS and rule.get("access") in ("Allow", "Deny")
                   and type(priority) is int and 100 <= priority <= 65535,
                   "unsupported or incomplete NSG rule", NotReadyError)
            item_ports = [rule_values(rule, side + "PortRange", side + "PortRanges")
                          for side in ("source", "destination")]
            expect(all(item_ports), "NSG port projection missing", NotReadyError)
            value = (priority, rule["access"], proto, selector(rule, "source"), selector(rule, "destination"),
                     tuple(map(port, item_ports[0])), tuple(map(port, item_ports[1])))
            if field == "defaultSecurityRules":
                name = item["name"].lower()
                expect(name not in defaults[direction], "duplicate default rule", NotReadyError)
                defaults[direction][name] = priority
            else:
                expect(priority <= 4096, "invalid custom priority")
            result[direction].append(value)
    expect(defaults == DEFAULT, "approved Azure default rule inventory unavailable", NotReadyError)
    for rules in result.values():
        expect(len({r[0] for r in rules}) == len(rules), "NSG priority collision in one direction")
        rules.sort(key=lambda r: r[0])
    return result


def match_dimension(choices, wanted):
    return any(contains(item, wanted) for item in choices)


def first_decision(rules, requested, expected):
    """Prove a whole request region or leave ambiguous precedence unresolved."""
    source, dest, proto, ports = requested
    for _, access, protocol, sources, destinations, src_ports, dest_ports in rules:
        if protocol != "*" and proto != "*" and protocol != proto:
            continue
        if not any(max(low, ports[0]) <= min(high, ports[1]) for low, high in dest_ports):
            continue
        src, dst = overlap(sources, (source,)), overlap(destinations, (dest,))
        if src is False or dst is False:
            continue
        if src is None or dst is None:
            raise NotReadyError("prior Service Tag or ASG overlap cannot be established")
        covers = (protocol in ("*", proto) and match_dimension(sources, source)
                  and match_dimension(destinations, dest)
                  and (0, 65535) in src_ports
                  and any(low <= ports[0] and high >= ports[1] for low, high in dest_ports))
        if not covers:
            if access != expected:
                raise Mismatch("higher priority opposite rule shadows part of the approved region")
            continue
        expect(access == expected, "higher priority rule changes the approved decision")
        return
    raise NotReadyError("cannot prove decision across the whole approved region")


def selector_subset(values, approved):
    return all(any(contains(allow, value) for allow in approved) for value in values)


def catchall(rules):
    expect(any(access == "Deny" and proto == "*" and sources == ("*",) and dest == ("*",)
               and src_ports == ((0, 65535),) and ports == ((0, 65535),) and priority <= 4096
               for priority, access, proto, sources, dest, src_ports, ports in rules),
           "explicit scoped fallback deny before Azure defaults required")


def inbound(rules, cfg):
    clients = private_networks(cfg["client_cidrs"])
    approved = set(clients)
    got = set()
    for priority, action, proto, sources, dest, _, ports in rules:
        if priority > 4096 or action != "Allow":
            continue
        if sources == ("azureloadbalancer",):
            expect(proto == "*" and dest == ("*",) and ports == ((0, 65535),),
                   "AzureLoadBalancer allowance differs from the private isolation profile")
            continue
        expect(all(isinstance(item, ipaddress.IPv4Network) for item in sources),
               "unreviewed inbound allow Service Tag, ASG or broad source", NotReadyError)
        expect(proto == "tcp" and ports == ((443, 443),) and set(sources) <= approved
               and (dest == ("*",) or selector_subset(dest, private_networks(cfg["cidrs"]))),
               "inbound allow differs in CIDR, port, protocol or destination")
        got.update(sources)
    expect(got == approved, "client allow CIDRs differ from the signed list")


def load_balancer(rules, cfg):
    for network in private_networks(cfg["cidrs"]):
        first_decision(rules, ("azureloadbalancer", network, "*", (0, 65535)), "Allow")


def egress(rules, cfg):
    catchall(rules)
    legs = [(item["protocol"], (item["port"], item["port"]),
             tuple(map(address, item["destinations"]))) for item in cfg["egress"]]
    for priority, action, protocol, sources, dest, _, ports in rules:
        if priority > 4096 or action != "Allow":
            continue
        expect(sources == ("*",) or selector_subset(sources, private_networks(cfg["cidrs"])),
               "outbound source exceeds approved Gateway subnet")
        expect(any(protocol == p and ports == (ports_allowed,) and selector_subset(dest, approved)
                   for p, ports_allowed, approved in legs),
               "outbound allow exceeds approved protocol, port or destination")
    for protocol, ports, destinations in legs:
        for network in private_networks(cfg["cidrs"]):
            for dest in destinations:
                first_decision(rules, (network, dest, protocol, ports), "Allow")


def get_body(client, rid):
    body = client.get_resource(rid, NET_API)["observation"]
    expect(isinstance(body, dict) and not body.get("nextLink"), "incomplete ARM resource result", NotReadyError)
    return body


def gateway_health(body):
    props = body.get("properties", {})
    expect(not props.get("nextLink") and props.get("sku", {}).get("tier") == "WAF_v2",
           "approved WAF_v2 health projection unavailable", NotReadyError)
    provision, state = props.get("provisioningState"), props.get("operationalState")
    expect(isinstance(provision, str) and isinstance(state, str),
           "Gateway provisioning or operational state unavailable", NotReadyError)
    expect((provision, state) == ("Succeeded", "Running"), "Gateway is not provisioned and running")


def boundary(gateway, subnet, cfg):
    props = usable(gateway)
    expect(props.get("sku", {}).get("name") == "WAF_v2" and props.get("sku", {}).get("tier") == "WAF_v2",
           "Gateway SKU profile unsupported", NotReadyError)
    expect(subnet_prefixes(subnet) == set(private_networks(cfg["cidrs"])), "Gateway subnet CIDRs differ from approval")
    assoc(subnet, cfg["nsg_id"], "networkSecurityGroup")
    delegations = [row["properties"]["serviceName"] for row in array(subnet, "delegations")]
    expect(delegations == ["Microsoft.Network/applicationGateways"],
           "Gateway subnet delegation differs from the supported private profile")
    expect(any(row.get("id", "").lower() == cfg["gateway_id"].lower()
               for row in array(subnet, "applicationGatewayIPConfigurations"))
           or any(row.get("id", "").lower().startswith(cfg["gateway_id"].lower() + "/gatewayipconfigurations/")
                  for row in subnet["applicationGatewayIPConfigurations"]),
           "Gateway subnet reverse association does not match")
    configurations = array(props, "gatewayIPConfigurations")
    frontend = array(props, "frontendIPConfigurations")
    expect(len(configurations) == len(frontend) == 1, "expected one scoped Gateway IP configuration and private frontend")
    expect(configurations[0]["properties"]["subnet"]["id"].lower() == cfg["subnet_id"].lower(),
           "Gateway is attached to a different subnet")
    actual = frontend[0]["properties"]
    expect(not actual.get("publicIPAddress") and actual.get("privateIPAllocationMethod") == "Static"
           and actual.get("privateIPAddress") == cfg["frontend_ip"]
           and actual.get("subnet", {}).get("id", "").lower() == cfg["subnet_id"].lower(),
           "Gateway frontend differs from the approved private frontend")
    ports = {p["id"].lower() for p in array(props, "frontendPorts") if p["properties"].get("port") == 443}
    listener = [row["properties"] for row in array(props, "httpListeners")]
    approved = {row["id"].lower() for row in frontend}
    expect(any(row.get("protocol") == "Https" and row["frontendPort"]["id"].lower() in ports
               and row["frontendIPConfiguration"]["id"].lower() in approved for row in listener),
           "no HTTPS 443 listener on the approved private frontend")


def policy_results(cfg, gateway, subnet_body, nsg, route):
    result = pending("separate approved evidence or runtime observation needed")
    result[15] = observed(lambda: gateway_health(gateway))
    config_result = observed(lambda: boundary(gateway, usable(subnet_body), cfg))
    if config_result[0] != "OBSERVED_NOT_ACCEPTED":
        for i in (1, 3, 5, 9, 11, 13):
            result[i] = config_result
        return result
    rules = {}
    inspection = observed(lambda: rules.update(parse_nsg(nsg)))
    if inspection[0] != "OBSERVED_NOT_ACCEPTED":
        for i in (1, 3, 5, 9, 11, 13):
            result[i] = inspection
        return result

    def client_paths():
        inbound(rules["Inbound"], cfg)
        catchall(rules["Inbound"])
        for source in private_networks(cfg["client_cidrs"]):
            first_decision(rules["Inbound"], (source, ipaddress.IPv4Network(cfg["frontend_ip"]),
                                            "tcp", (443, 443)), "Allow")

    def approved_order():
        for direction, actual in rules.items():
            expect([r[0] for r in actual if r[0] < 65000] == cfg["approved_priorities"][direction],
                   "custom priorities differ from approval")

    def outbound():
        route_policy(usable(subnet_body), route, cfg)
        egress(rules["Outbound"], cfg)

    def precedence():
        client_paths()
        load_balancer(rules["Inbound"], cfg)
        # Any preceding client permits are limited to the signed sources and
        # AzureLoadBalancer is the documented platform IPv4 identity.
        for source in private_networks(cfg.get("deny_test_cidrs", []), allow_empty=True):
            first_decision(rules["Inbound"], (source, ipaddress.IPv4Network(cfg["frontend_ip"]),
                                            "tcp", (443, 443)), "Deny")

    for i, check in {1: client_paths, 3: lambda: inbound(rules["Inbound"], cfg),
                     5: lambda: load_balancer(rules["Inbound"], cfg), 9: outbound,
                     11: precedence, 13: approved_order}.items():
        state, reason = observed(check)
        result[i] = (("CONFIG_OBSERVED_NOT_ACCEPTED",
                      "associated UDR/NSG configuration only; effective route and BGP unobserved" if i == 9
                      else "scoped Gateway subnet NSG configuration only") if state == "OBSERVED_NOT_ACCEPTED"
                     else (state, reason))
    if result[15][0] == "OBSERVED_NOT_ACCEPTED":
        result[15] = ("CONFIG_OBSERVED_NOT_ACCEPTED", "ARM state only; backend and TLS not observed")
    return result


def pending(reason):
    return {i: ("NOT_READY", reason) for i in range(1, 23)}


def observe_arm(cfg, client):
    def read(rid):
        try:
            return get_body(client, rid) if rid is not None else None
        except (NotReadyError, RestFailure):
            return {}
    return policy_results(cfg, *(read(cfg[key]) for key in ("gateway_id", "subnet_id", "nsg_id", "route_table_id")))


def probe_input(cfg):
    plan = cfg["probe"]
    require(plan.get("direction") in ("allow", "deny") and plan.get("vantage_approved") is True
            and isinstance(plan.get("approval_ref"), str) and plan["approval_ref"].strip(),
            "approval for one isolated probe and vantage required")
    require(private_ip(plan["source_ip"]) and plan["destination_ip"] == cfg["frontend_ip"],
            "probe tuple must use approved source and private frontend")
    address_value = ipaddress.IPv4Address(plan["source_ip"])
    require(address_value in private_networks([plan["runner_cidr"]])[0],
            "source IP differs from approved Runner CIDR")
    approved = any(address_value in net for net in private_networks(cfg["client_cidrs"]))
    if plan["direction"] == "deny":
        require(plan.get("isolated_deny_approved") is True and not approved
                and any(address_value in net for net in private_networks(cfg["deny_test_cidrs"])),
                "isolated deny vantage must be outside approved clients and inside approved test CIDRs")
    else:
        require(approved, "allow vantage must be within approved client CIDRs")
    return plan


def probe(cfg, client, connect=socket.create_connection):
    plan = probe_input(cfg)
    boundary(get_body(client, cfg["gateway_id"]), usable(get_body(client, cfg["subnet_id"])), cfg)
    try:
        with connect((cfg["frontend_ip"], 443), timeout=3, source_address=(plan["source_ip"], 0)) as conn:
            expect(conn.getsockname()[0] == plan["source_ip"] and conn.getpeername()[0] == cfg["frontend_ip"],
                   "socket tuple differs from approved vantage and Gateway frontend")
    except OSError:
        return "NOT_READY", "TCP did not connect; corroborating scoped flow or policy observation required"
    if plan["direction"] == "deny":
        return "FAIL", "approved isolated deny vantage unexpectedly connected"
    return "TCP_OBSERVED_NOT_ACCEPTED", "bound source connected; TLS, HTTPS and other paths remain unverified"


def review_policy(cfg, document):
    expect(document.get("topology_ref") == cfg["network_isolation_review_ref"]
           and document.get("sku") == "WAF_v2" and document.get("network_isolation") is True
           and document.get("gateway_manager_required") is False,
           "reviewed private platform design evidence missing or inconsistent", NotReadyError)
    if "change_controls" in document:
        control = document["change_controls"]
        expect(control.get("no_production_nsg_mutations") is True
               and control.get("nonproduction_boundary_approved") is True
               and isinstance(control.get("approval_ref"), str) and control["approval_ref"].strip(),
               "approved nonproduction and no-production-change safeguards are incomplete", NotReadyError)


def review_backend(cfg, document):
    target = cfg["backend"]
    for key in ("pool_id", "settings_id"):
        require(isinstance(target[key], str) and target[key].lower().startswith(cfg["gateway_id"].lower() + "/"),
                "approved backend configuration IDs must belong to the Gateway")
    expect(document.get("scope_complete") is True and document.get("gateway_id", "").lower() == cfg["gateway_id"].lower(),
           "backend extract scope unavailable", NotReadyError)
    expect(document.get("pool_id", "").lower() == target["pool_id"].lower()
           and document.get("settings_id", "").lower() == target["settings_id"].lower()
           and document.get("address") == target["address"] and document.get("health") == "Healthy"
           and document.get("configured_hostname") == target["hostname"]
           and document.get("configured_sni") == target["hostname"],
           "backend health identity, state or configured Host/SNI differ from approval")


def review_changes(cfg, document):
    expect(document.get("collection_complete") is True and isinstance(document.get("review_ref"), str)
           and document["review_ref"].strip(), "bounded change-log extract and review reference required", NotReadyError)
    expected = cfg["changes"]
    start, end = (datetime.fromisoformat(expected[k]) for k in ("start", "end"))
    expect(start.tzinfo is not None and end.tzinfo is not None and start < end,
           "explicit timezone-aware activity interval required", NotReadyError)
    expect(document.get("start") == expected["start"] and document.get("end") == expected["end"],
           "activity interval differs from approval")
    events = array(document, "events")
    approvals = array(expected, "tickets")
    def event_key(event):
        return tuple(event[key] for key in ("event_id", "actor_ref", "operation", "ticket_ref"))
    expect(bool(approvals) and all(row.get("resource_id", "").lower() == cfg["nsg_id"].lower()
               and row.get("status") == "Succeeded"
               and start <= datetime.fromisoformat(row["observed_at"]) < end for row in events),
           "activity extract is outside approved resource, status or time interval")
    observed_keys = {event_key(row) for row in events}
    approved_keys = {event_key(row) for row in approvals}
    expect(all(isinstance(item, str) and item.strip() for key in approved_keys for item in key)
           and len(observed_keys) == len(events) and len(approved_keys) == len(approvals)
           and observed_keys == approved_keys, "activity event, actor or ticket association differs from approval")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    for flag in ("live", "check-config", "probe", "review-flow", "review-backend", "review-changes", "review-policy"):
        modes.add_argument("--" + flag, action="store_true")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    os.umask(0o077)
    mode = "not_run"
    code = 2
    selected = None
    result = pending("explicit mode and approved config required")
    try:
        flags = ("live", "check_config", "probe", "review_flow", "review_backend", "review_changes", "review_policy")
        mode = next((flag for flag in flags if getattr(args, flag)), "not_run")
        require(mode != "not_run" and args.config is not None, "explicit mode and approved config required")
        cfg = validate(read_file(args.config))
        if args.live:
            result = observe_arm(cfg, client_for(cfg))
            states = [result[i][0] for i in (1, 3, 5, 9, 11, 13, 15)]
            code = 1 if "FAIL" in states else 2 if "NOT_READY" in states else 0
        elif args.check_config:
            if "probe" in cfg:
                probe_input(cfg)
            result = pending("input shape validated; observation not executed")
            code = 0
        elif args.probe:
            plan = probe_input(cfg)
            selected = 1 if plan["direction"] == "allow" else 11
            result[selected] = probe(cfg, client_for(cfg))
            code = {"FAIL": 1, "NOT_READY": 2}.get(result[selected][0], 0)
        else:
            selected = (11 if args.review_flow else 17 if args.review_backend else
                        21 if args.review_changes else 7)
            require(args.evidence is not None, "approved evidence extract required")
            document = read_file(args.evidence)
            if args.review_flow:
                review_flow(document, probe_input(cfg))
            elif args.review_backend:
                review_backend(cfg, document)
            elif args.review_changes:
                review_changes(cfg, document)
            else:
                review_policy(cfg, document)
                for case in (7, 19):
                    result[case] = ("NOT_READY", "owner approval, scope completeness and authenticity require human review")
                reports(result, mode, args.out, step=28, kinds=KINDS)
                return 2
            result[selected] = ("EXTRACT_MATCHED_NOT_ACCEPTED",
                                "approved fields match; collection provenance and remaining runtime checks require review")
            code = 0
    except Mismatch as exc:
        result[selected or 1] = ("FAIL", str(exc))
        code = 1
    except (InputIssue, NotReadyError) as exc:
        if selected is None:
            result = pending(str(exc))
        else:
            result[selected] = ("NOT_READY", str(exc))
    except (RestFailure, ValueError, KeyError, IndexError, TypeError, AttributeError, OSError):
        message = "approved input or complete observations unavailable"
        if selected is None:
            result = pending(message)
        else:
            result[selected] = ("NOT_READY", message)
    reports(result, mode, args.out, step=28, kinds=KINDS)
    print(f"AZ-T28 mode={mode} Azure acceptance=0 exit={code}; JSON and JUnit written")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
