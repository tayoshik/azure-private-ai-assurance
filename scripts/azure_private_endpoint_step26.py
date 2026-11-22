"""AZ-T26 scoped Private Endpoint zoning, policy and TCP evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import ipaddress
import os
from pathlib import Path
import re
import socket
from uuid import UUID

from azure_monitor_private_audit import resource_id
from azure_private_dns_step30 import InputIssue, Mismatch, read_file, reports, require
from azure_rest_reader import AzureReadOnlyClient, NotReadyError, RestFailure, workload_identity_token_provider
import rest04_private_dns_audit as rest04


NETWORK = "Microsoft.Network/"
NET_API = rest04.API_VERSIONS["pe"]
PROFILES = {group: path.strip("/").removeprefix("providers/") for group, (path, _) in rest04.SERVICE_PROFILES.items()}
PROFILES["azuremonitor"] = "Microsoft.Insights/privateLinkScopes"
MODES = {"Disabled": set(), "Enabled": {"nsg", "udr"}, "NetworkSecurityGroupEnabled": {"nsg"},
         "RouteTableEnabled": {"udr"}}
KINDS = {i: ("manual_isolation_approval" if i == 21 else "flow_evidence_review" if i == 19 else
             "policy_configuration_and_tcp" if i in (11, 13) else "arm_configuration")
         for i in range(1, 22, 2)}


def expect(condition, reason, error=Mismatch):
    if not condition:
        raise error(reason)


def private_networks(values, *, allow_empty=False):
    require(isinstance(values, list) and (bool(values) or allow_empty), "approved IPv4 CIDRs required")
    blocks = [ipaddress.IPv4Network(value) for value in values]
    require(len(set(blocks)) == len(blocks)
            and all(any(block.subnet_of(private) for private in rest04.RFC1918) for block in blocks),
            "CIDRs must be distinct RFC1918 IPv4 networks")
    return blocks


def ids(values):
    return {value.lower() for value in values}


def validate(config):
    require(config.get("schema") == "azure-private-endpoint/az-t26/v1", "unknown AZ-T26 input schema")
    require(config.get("topology") in ("hub", "dev") and config.get("environment") == "nonproduction",
            "reviewed Hub or dev nonproduction topology required")
    require(isinstance(config.get("approval_ref"), str) and config["approval_ref"].strip(),
            "approved scope reference required")
    require(config.get("approved_private_runner") is True, "approved Private Runner required")
    require(isinstance(config["subscriptions"], list) and 1 <= len(config["subscriptions"]) <= 10,
            "explicit approved subscriptions required")
    subscriptions = [str(UUID(value)) for value in config["subscriptions"]]
    require(len(set(subscriptions)) == len(subscriptions), "duplicate approved subscriptions")
    config["subscriptions"] = subscriptions

    def arm(value, kind):
        require(value.startswith("/subscriptions/"), "canonical ARM resource ID required")
        return resource_id(value, kind, subscriptions)

    subnets = config["subnets"]
    require(isinstance(subnets, list) and 1 <= len(subnets) <= 12, "approve one to twelve scoped PE subnets")
    seen_subnets, seen_ips, seen_pe, seen_nics = set(), set(), set(), set()
    vnet_blocks = {}
    for entry in subnets:
        arm(entry["vnet_id"], NETWORK + "virtualNetworks")
        arm(entry["subnet_id"], NETWORK + "virtualNetworks/subnets")
        require(entry["subnet_id"].lower().startswith(entry["vnet_id"].lower() + "/subnets/"),
                "subnet is outside the approved VNet")
        require(entry["subnet_id"].lower() not in seen_subnets, "each subnet may have only one approved purpose")
        seen_subnets.add(entry["subnet_id"].lower())
        require(isinstance(entry["purpose"], str) and re.fullmatch(r"[a-z][a-z0-9-]{0,39}", entry["purpose"]),
                "explicit subnet purpose required")
        blocks = private_networks(entry["cidrs"])
        prior = vnet_blocks.setdefault(entry["vnet_id"].lower(), [])
        for block in blocks:
            require(not any(block.overlaps(existing) for existing in prior),
                    "approved PE subnet CIDRs overlap within one VNet")
            prior.append(block)
        require(entry["mode"] in MODES, "unsupported approved PE network policy mode")
        require(isinstance(entry["required_enforcement"], list)
                and set(entry["required_enforcement"]) <= MODES[entry["mode"]],
                "approved mode must enable each required enforcement mechanism")
        for field, kind in (("nsg_id", "networkSecurityGroups"), ("route_table_id", "routeTables")):
            if entry[field] is not None:
                arm(entry[field], NETWORK + kind)
        require("nsg" not in entry["required_enforcement"] or entry["nsg_id"] is not None,
                "required NSG enforcement needs an associated NSG")
        require("udr" not in entry["required_enforcement"] or entry["route_table_id"] is not None,
                "required UDR enforcement needs an associated route table")
        routes = entry["expected_routes"]
        require(isinstance(routes, list) and len(routes) <= 100
                and (entry["route_table_id"] is not None or not routes),
                "explicit approved route entries required")
        seen_routes = set()
        for route in routes:
            prefix = str(ipaddress.IPv4Network(route["prefix"]))
            require(prefix not in seen_routes, "duplicate approved route")
            seen_routes.add(prefix)
            require(route["next_hop_type"] in {"VirtualAppliance", "Internet", "VnetLocal", "VirtualNetworkGateway", "None"},
                    "unsupported approved next hop type")
            hop_ip = route.get("next_hop_ip")
            require(rest04.private_ip(hop_ip) if route["next_hop_type"] == "VirtualAppliance" else hop_ip is None,
                    "approved next hop must match route type")
        private_networks(entry["source_cidrs"], allow_empty=True)
        require(isinstance(entry["source_asg_ids"], list), "explicit source ASG list required")
        for value in entry["source_asg_ids"]:
            arm(value, NETWORK + "applicationSecurityGroups")
        targets = entry["endpoints"]
        require(isinstance(targets, list) and 1 <= len(targets) <= 25, "approve one to twenty-five endpoints per subnet")
        for target in targets:
            require(target["purpose"] == entry["purpose"], "endpoint purpose conflicts with subnet purpose")
            pe = arm(target["private_endpoint_id"], NETWORK + "privateEndpoints").lower()
            nic = arm(target["nic_id"], NETWORK + "networkInterfaces").lower()
            require(pe not in seen_pe and nic not in seen_nics, "duplicate PE or NIC in declared inventory")
            seen_pe.add(pe)
            seen_nics.add(nic)
            require(target["group_id"] in PROFILES, "unsupported Private Link subresource")
            arm(target["service_id"], PROFILES[target["group_id"]])
            require(isinstance(target["asg_ids"], list), "explicit PE ASG list required")
            for value in target["asg_ids"]:
                arm(value, NETWORK + "applicationSecurityGroups")
            ips = target["expected_private_ips"]
            require(isinstance(ips, list) and 1 <= len(ips) <= 16 and len(set(ips)) == len(ips),
                    "explicit distinct PE addresses required")
            for addr in ips:
                ip = ipaddress.IPv4Address(addr)
                require(any(ip in block for block in blocks), "approved PE address is outside subnet CIDR")
                key = (entry["vnet_id"].lower(), ip)
                require(key not in seen_ips, "duplicate private address in one VNet")
                seen_ips.add(key)
    return config


def usable(body):
    expect(isinstance(body, dict) and not body.get("nextLink"), "ARM inventory unavailable or contains an unfollowed page",
           NotReadyError)
    props = body.get("properties")
    expect(isinstance(props, dict) and not props.get("nextLink"), "incomplete or paged ARM resource properties", NotReadyError)
    expect(props.get("provisioningState") == "Succeeded", "ARM provisioning state is incomplete or unsuccessful", NotReadyError)
    return props


def array(props, field):
    value = props.get(field)
    expect(isinstance(value, list), "required ARM inventory array missing or incomplete", NotReadyError)
    return value


def subnet_prefixes(props):
    value = props.get("addressPrefixes", []) or ([props["addressPrefix"]] if props.get("addressPrefix") else [])
    expect(bool(value), "ARM subnet CIDR unavailable", NotReadyError)
    return {ipaddress.IPv4Network(cidr) for cidr in value}


def linked_id(props, field):
    association = props.get(field)
    expect(association is None or isinstance(association, dict) and isinstance(association.get("id"), str),
           "ARM association is incomplete", NotReadyError)
    return association["id"].lower() if association else None


def assoc(subnet, expected, field):
    actual = linked_id(subnet, field)
    expect(actual == (expected.lower() if expected else None), "ARM association differs from approved design")


def zoning(subnet, entry, endpoint_check):
    expect(subnet_prefixes(subnet) == set(private_networks(entry["cidrs"])), "subnet CIDR differs from approval")
    inventory = array(subnet, "privateEndpoints")
    expect(ids([item["id"] for item in inventory]) == ids([item["private_endpoint_id"] for item in entry["endpoints"]])
           and len(inventory) == len(entry["endpoints"]), "scoped subnet PE inventory differs from approved zoning")
    expect(not array(subnet, "delegations"), "PE subnet contains a delegation outside this dedicated subnet contract")
    endpoint_check()


def policy_mode(subnet, entry):
    actual = subnet.get("privateEndpointNetworkPolicies")
    expect(actual in MODES, "ARM PE network policy mode missing or unsupported", NotReadyError)
    expect(actual == entry["mode"] and set(entry["required_enforcement"]) <= MODES[actual],
           "PE network policy mode differs from required enforcement")


def endpoint(target, entry, pe, nic):
    p, n = usable(pe), usable(nic)
    links = [connection for key in ("privateLinkServiceConnections", "manualPrivateLinkServiceConnections")
             for connection in (p.get(key) or [])]
    expect(bool(links), "PE connection inventory is missing", NotReadyError)
    expect(len(links) == 1, "PE does not have exactly one approved service connection")
    problems, missing = rest04.assess_endpoint({**target, "subnet_id": entry["subnet_id"]}, pe, nic)
    expect(not problems, "REST04 PE/NIC mismatch: " + ", ".join(sorted(set(problems))))
    expect(not missing, "REST04 PE/NIC evidence incomplete: " + ", ".join(sorted(set(missing))), NotReadyError)
    ips = [item["properties"]["privateIPAddress"] for item in array(n, "ipConfigurations")]
    expect(len(ips) == len(set(ips)), "duplicate IP in PE NIC configurations")
    nets = private_networks(entry["cidrs"])
    expect(all(any(ipaddress.IPv4Address(ip) in net for net in nets) for ip in ips),
           "PE NIC IP lies outside the approved subnet range")


def rule_values(rule, singular, plural):
    if rule.get(singular) is not None:
        expect(not rule.get(plural), "ambiguous NSG rule projection", NotReadyError)
        return {rule[singular]}
    return set(rule.get(plural) or [])


def nsg_policy(nsg, entry, category):
    props = usable(nsg)
    rules = [item["properties"] for item in array(props, "securityRules")]
    expect(all(rule.get("direction") in {"Inbound", "Outbound"}
               and rule.get("access") in {"Allow", "Deny"} and type(rule.get("priority")) is int
               for rule in rules), "incomplete NSG rule projection", NotReadyError)
    inbound = [rule for rule in rules if rule["direction"] == "Inbound"]
    allow = [rule for rule in inbound if rule["access"] == "Allow"]
    expect(len({rule["priority"] for rule in inbound}) == len(inbound), "duplicate inbound NSG priority")
    expected_asgs = ids(entry["source_asg_ids"])
    expected_cidrs = set(entry["source_cidrs"])
    if category == "sources":
        sources, groups = set(), set()
        for rule in allow:
            sources |= rule_values(rule, "sourceAddressPrefix", "sourceAddressPrefixes")
            groups |= ids([asg["id"] for asg in rule.get("sourceApplicationSecurityGroups") or []])
        expect(sources == expected_cidrs and groups == expected_asgs,
               "inbound NSG allow sources differ from approved CIDRs or ASGs")
    elif category == "deny":
        deny = [rule for rule in inbound if rule["access"] == "Deny"
                and rule.get("protocol") == "*"
                and rule_values(rule, "sourcePortRange", "sourcePortRanges") == {"*"}
                and rule_values(rule, "destinationPortRange", "destinationPortRanges") == {"*"}
                and rule_values(rule, "sourceAddressPrefix", "sourceAddressPrefixes") == {"*"}
                and not rule.get("sourceApplicationSecurityGroups") and not rule.get("destinationApplicationSecurityGroups")
                and rule_values(rule, "destinationAddressPrefix", "destinationAddressPrefixes")
                in ({"*"}, set(entry["cidrs"]))]
        expect(bool(deny) and all(rule["priority"] < min(d["priority"] for d in deny) for rule in allow),
               "no explicit catch-all inbound deny after the approved allows")
    else:
        expect(bool(allow), "approved minimum TCP 443 allow is absent")
        allowed_destinations = {asg.lower() for target in entry["endpoints"] for asg in target["asg_ids"]}
        for rule in allow:
            dst = rule_values(rule, "destinationAddressPrefix", "destinationAddressPrefixes")
            dst_asgs = ids([item["id"] for item in rule.get("destinationApplicationSecurityGroups") or []])
            expect(rule.get("protocol", "").lower() == "tcp"
                   and rule_values(rule, "destinationPortRange", "destinationPortRanges") == {"443"}
                   and ((bool(dst) and not dst_asgs and (dst == {"*"} or dst <= set(entry["cidrs"])))
                        or (bool(dst_asgs) and not dst and dst_asgs <= allowed_destinations)),
                   "inbound allow has an unapproved protocol, port or destination")


def asgs(pe, nic, target):
    p, n = usable(pe), usable(nic)
    expected = ids(target["asg_ids"])
    expect(ids([asg["id"] for asg in p.get("applicationSecurityGroups") or []]) == expected,
           "PE ASG membership differs from approval")
    for item in array(n, "ipConfigurations"):
        values = item["properties"].get("applicationSecurityGroups") or []
        expect(ids([asg["id"] for asg in values]) == expected, "NIC IP configuration ASG membership differs from approval")


def route_policy(subnet, table, entry):
    assoc(subnet, entry["route_table_id"], "routeTable")
    expected = entry["expected_routes"]
    if entry["route_table_id"] is not None:
        routes = array(usable(table), "routes")
        expect(all(item["properties"].get("provisioningState") == "Succeeded" for item in routes),
               "UDR provisioning state unavailable", NotReadyError)
        observed = {
            (item["properties"]["addressPrefix"], item["properties"]["nextHopType"],
             item["properties"].get("nextHopIpAddress")) for item in routes
        }
    else:
        routes, observed = [], set()
    wanted = {(item["prefix"], item["next_hop_type"], item.get("next_hop_ip")) for item in expected}
    expect(observed == wanted and len(routes) == len(wanted), "UDR entries differ from approved route table baseline")


def observed(check):
    try:
        check()
    except Mismatch as exc:
        return "FAIL", str(exc)
    except NotReadyError as exc:
        return "NOT_READY", str(exc)
    except (RestFailure, ValueError, KeyError, IndexError, TypeError, AttributeError, OSError):
        return "NOT_READY", "approved ARM resource or response fields unavailable"
    return "OBSERVED_NOT_ACCEPTED", ""


def arm_checks(config, client):
    cache = {}

    def read(rid):
        if rid not in cache:
            try:
                cache[rid] = client.get_resource(rid, NET_API)["observation"]
            except (NotReadyError, RestFailure):
                # Permission errors and 404 cannot establish nonexistence.
                cache[rid] = None
        return cache[rid]

    outcome = {i: [] for i in range(1, 18, 2)}
    for row in config["subnets"]:
        def subnet():
            return usable(read(row["subnet_id"]))

        def endpoints(check):
            for target in row["endpoints"]:
                check(target, read(target["private_endpoint_id"]), read(target["nic_id"]))

        def endpoint_inventory():
            endpoints(lambda target, pe, nic: endpoint(target, row, pe, nic))

        def with_policy(category):
            expect("nsg" in MODES.get(subnet().get("privateEndpointNetworkPolicies"), set()),
                   "NSG enforcement on this PE subnet is unconfirmed or out of scope", NotReadyError)
            expect(row["nsg_id"] is not None, "no approved NSG for PE source/port observations", NotReadyError)
            assoc(subnet(), row["nsg_id"], "networkSecurityGroup")
            nsg_policy(read(row["nsg_id"]), row, category)

        def asg_inventory():
            endpoints(lambda target, pe, nic: asgs(pe, nic, target))
            if row["nsg_id"] is not None:
                with_policy("sources")
                with_policy("ports")
            elif row["source_asg_ids"] or any(target["asg_ids"] for target in row["endpoints"]):
                raise NotReadyError("ASG policy references need an approved NSG")

        checks = {
            1: lambda: zoning(subnet(), row, endpoint_inventory),
            3: lambda: (assoc(subnet(), row["nsg_id"], "networkSecurityGroup"),
                        assoc(subnet(), row["route_table_id"], "routeTable")),
            5: lambda: policy_mode(subnet(), row),
            7: lambda: route_policy(subnet(), read(row["route_table_id"]) if row["route_table_id"] else None, row),
            9: endpoint_inventory,
            11: lambda: with_policy("sources"),
            13: lambda: with_policy("deny"),
            15: lambda: (with_policy("sources"), with_policy("ports")),
            17: asg_inventory,
        }
        for i, check in checks.items():
            outcome[i].append(observed(check))
    result = pending("separate runtime or owner evidence required")
    for i, values in outcome.items():
        errors = [(state, reason) for state, reason in values if state != "OBSERVED_NOT_ACCEPTED"]
        if errors:
            result[i] = ("FAIL" if any(state == "FAIL" for state, _ in errors) else "NOT_READY",
                         "; ".join(sorted({reason for _, reason in errors})))
        else:
            reasons = {7: "UDR configuration only; effective route not observed",
                       11: "NSG source config only; allowed path not measured",
                       13: "NSG fallback config only; isolated denied path not measured",
                       17: "scoped PE/NIC membership and source/destination NSG references only"}
            result[i] = ("CONFIG_OBSERVED_NOT_ACCEPTED", reasons.get(i, "scoped ARM configuration only"))
    return result


def probe_input(config):
    plan = config["probe"]
    require(config.get("isolation_approved") is True and bool(plan.get("runner_approval_ref"))
            and bool(plan.get("probe_approval_ref")), "approved isolated Runner and probe required")
    require(plan["direction"] in ("allow", "deny"), "approve allow or deny vantage")
    subnet_index, endpoint_index = plan["subnet_index"], plan["endpoint_index"]
    require(type(subnet_index) is int and type(endpoint_index) is int and subnet_index >= 0 and endpoint_index >= 0,
            "explicit approved endpoint index required")
    subnet = config["subnets"][subnet_index]
    target = subnet["endpoints"][endpoint_index]
    source = ipaddress.IPv4Address(plan["source_ip"])
    source_cidr = private_networks([plan["runner_cidr"]])[0]
    require(source in source_cidr and rest04.private_ip(plan["source_ip"]), "Runner source does not match approved vantage")
    require(plan["destination_ip"] in target["expected_private_ips"] and plan["source_ip"] != plan["destination_ip"],
            "probe destination is outside the approved endpoint IP set")
    allowed_by_cidr = any(source in block for block in private_networks(subnet["source_cidrs"], allow_empty=True))
    if plan["direction"] == "deny":
        require(plan.get("isolated_deny_approved") is True, "explicit denial exercise approval needed")
        require(not allowed_by_cidr and plan.get("outside_approved_source_asgs") is True,
                "deny vantage must be outside approved CIDRs and ASGs")
    else:
        allow_by_asg = str(plan.get("source_asg_id", "")).lower() in ids(subnet["source_asg_ids"])
        require(allowed_by_cidr or allow_by_asg, "allow vantage is outside the approved CIDRs and ASGs")
    return plan


def run_probe(config, client, connect=socket.create_connection):
    plan = probe_input(config)
    entry = config["subnets"][plan["subnet_index"]]
    target = entry["endpoints"][plan["endpoint_index"]]
    pe, nic = (client.get_resource(target[field], NET_API)["observation"]
               for field in ("private_endpoint_id", "nic_id"))
    subnet = usable(client.get_resource(entry["subnet_id"], NET_API)["observation"])
    expect(subnet_prefixes(subnet) == set(private_networks(entry["cidrs"])), "probe subnet CIDR differs from approval")
    endpoint(target, entry, pe, nic)
    identifier = 11 if plan["direction"] == "allow" else 13
    try:
        with connect((plan["destination_ip"], 443), timeout=3, source_address=(plan["source_ip"], 0)) as sock:
            expect(sock.getsockname()[0] == plan["source_ip"] and sock.getpeername()[0] == plan["destination_ip"],
                   "probe socket tuple differs from approved vantage and endpoint")
    except OSError:
        return identifier, ("NOT_READY", "TCP did not connect; corroborate route/policy and flow evidence")
    if identifier == 13:
        return identifier, ("FAIL", "isolated denied vantage unexpectedly connected to approved PE")
    return identifier, ("TCP_OBSERVED_NOT_ACCEPTED", "source-bound TCP 443 connected; TLS, application and policy scope unproven")


def review_flow(document, plan):
    expect(isinstance(document.get("review_ref"), str) and document["review_ref"].strip(),
           "approved flow extract reference required", NotReadyError)
    expect(isinstance(document.get("records"), list) and document["records"], "flow evidence unavailable", NotReadyError)
    expected = "Allow" if plan["direction"] == "allow" else "Deny"
    require(isinstance(plan.get("probe_ref"), str) and plan["probe_ref"].strip(), "explicit probe correlation reference required")
    probe_time = datetime.fromisoformat(plan["observed_at"])
    expect(probe_time.tzinfo is not None, "probe timestamp requires an offset", NotReadyError)
    expect(abs((datetime.now(timezone.utc) - probe_time).total_seconds()) <= 86_400,
           "approved probe timestamp outside the review window", NotReadyError)
    matched = [
        row for row in document["records"]
        if row.get("probe_ref") == plan["probe_ref"] and row.get("source_ip") == plan["source_ip"]
        and row.get("destination_ip") == plan["destination_ip"] and row.get("port") == 443
        and row.get("protocol") == "TCP"
    ]
    expect(len(matched) == 1, "flow extract lacks a single matching approved probe tuple", NotReadyError)
    row = matched[0]
    value = datetime.fromisoformat(row["observed_at"])
    expect(value.tzinfo is not None and abs((value - probe_time).total_seconds()) <= 120,
           "flow record is outside the approved probe correlation window", NotReadyError)
    expect(row.get("decision") == expected, "correlated flow decision differs from approval")


def pending(reason):
    return {i: ("NOT_READY", reason) for i in range(1, 23)}


def client_for(config):
    return AzureReadOnlyClient(config["subscriptions"], workload_identity_token_provider(), read_enabled=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    for flag in ("live", "check-config", "probe", "review-flow"):
        modes.add_argument("--" + flag, action="store_true")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--flow", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    os.umask(0o077)
    result = pending("explicit mode and approved input required")
    mode = "not_run"
    selected = None
    code = 2
    try:
        if args.live or args.check_config or args.probe or args.review_flow:
            require(args.config is not None, "approved config required")
            mode = ("arm_configuration" if args.live else "input_check" if args.check_config else
                    "tcp_probe" if args.probe else "flow_review")
            config = validate(read_file(args.config))
            if args.check_config:
                if "probe" in config:
                    probe_input(config)
                result = pending("input shape checked; no Azure observations")
                code = 0
            elif args.live:
                result = arm_checks(config, client_for(config))
                states = [result[i][0] for i in range(1, 18, 2)]
                code = 1 if "FAIL" in states else 2 if "NOT_READY" in states else 0
            elif args.probe:
                plan = probe_input(config)
                selected = 11 if plan["direction"] == "allow" else 13
                _, result[selected] = run_probe(config, client_for(config))
                code = {"FAIL": 1, "NOT_READY": 2}.get(result[selected][0], 0)
            else:
                selected = 19
                require(args.flow is not None, "approved flow extract required")
                review_flow(read_file(args.flow), probe_input(config))
                result[19] = ("FLOW_EXTRACT_MATCHED_NOT_ACCEPTED", "tuple/time/decision match; provenance and coverage need independent review")
                code = 0
    except Mismatch as exc:
        if selected:
            result[selected] = ("FAIL", str(exc))
        code = 1
    except (InputIssue, NotReadyError) as exc:
        if selected:
            result[selected] = ("NOT_READY", str(exc))
        else:
            result = pending(str(exc))
    except (RestFailure, ValueError, TypeError, KeyError, IndexError, AttributeError, OSError):
        if selected:
            result[selected] = ("NOT_READY", "approved inputs or complete resource observations unavailable")
        else:
            result = pending("approved inputs or complete resource observations unavailable")
    reports(result, mode, args.out, step=26, kinds=KINDS)
    print(f"AZ-T26 mode={mode} Azure acceptance=0 exit={code}; JSON and JUnit written")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
