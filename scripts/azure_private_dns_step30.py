"""AZ-T30 Private DNS verification, with separate configuration and data-plane evidence."""
from __future__ import annotations

import argparse
from copy import deepcopy
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

from azure_rest_reader import AzureReadOnlyClient, NotReadyError, RestFailure, workload_identity_token_provider
import rest04_private_dns_audit as rest04


PROFILES = {
    "web": ("sites", "azurewebsites.net", 1),
    "scm": ("sites", "scm.azurewebsites.net", 1),
    "openai": ("account", "openai.azure.com", 3),
    "search": ("searchservice", "search.windows.net", 5),
    "cosmos": ("sql", "documents.azure.com", 7),
    "vault": ("vault", "vault.azure.net", 9),
}
KINDS = {**{i: "arm_configuration" for i in range(1, 14, 2)}, 15: "resolver_a",
         17: "ownership_review", 19: "cname_chain", 21: "pe_bound_private_a"}
NAME = re.compile(r"(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?")


class InputIssue(ValueError):
    """Invalid operator input with a sanitized reason."""


class Mismatch(Exception):
    """A sanitized verification mismatch."""


def require(condition, reason):
    if not condition:
        raise InputIssue(reason)


def name(value):
    require(isinstance(value, str) and NAME.fullmatch(value), "invalid DNS name")
    return value


def validate(config):
    require(isinstance(config, dict) and config.get("schema") == "azure-private-dns/az-t30/v1",
            "unknown Private DNS input schema")
    require(config.get("topology") in ("hub", "dev"), "choose hub or dev")
    require(isinstance(config.get("approval_ref"), str) and config["approval_ref"].strip(),
            "approved scope reference required")
    require(config.get("approved_private_runner") is True, "approved Private Runner required")
    targets = config.get("targets")
    require(isinstance(targets, dict) and set(targets) <= PROFILES.keys(), "unknown service profile")
    require(bool(targets), "approved service targets required")
    for profile, entry in targets.items():
        group, suffix, _ = PROFILES[profile]
        arm = rest04.validate_target(entry["arm"])
        require(all(arm[key].startswith("/subscriptions/") and all(
                    part not in ("", ".", "..") for part in arm[key].split("/")[1:])
                    for key in (k for k in arm if k in (*rest04.PATH_KEYS.values(),
                                "service_id", "subnet_id", "vnet_id", "expected_link_vnet_id"))),
                "approved ARM IDs must use canonical absolute resource paths")
        require(arm["group_id"].lower() == group, "target group does not match service profile")
        ordinary = name(entry["ordinary_name"])
        private = name(entry["private_name"])
        require(ordinary.endswith("." + suffix) and ".privatelink." not in ordinary,
                "ordinary name does not match the approved service class")
        require(profile != "web" or not ordinary.endswith(".scm.azurewebsites.net"),
                "SCM name cannot replace the normal App Service target")
        require(private == arm["expected_record_fqdn"], "private name does not match ARM record")
        if profile in ("web", "scm"):
            label = ordinary[:-(len(suffix) + 1)]
            expected_private = label + (".scm" if profile == "scm" else "") + ".privatelink.azurewebsites.net"
            require(private == expected_private, "App Service ordinary/SCM name and pinned Azure DNS record disagree")
        chain = entry["cname_chain"]
        require(isinstance(chain, list) and 2 <= len(chain) <= 9 and all(name(hop) for hop in chain)
                and len(set(chain)) == len(chain) and chain[0] == ordinary and chain[-1] == private,
                "explicit bounded CNAME chain required")
        cidrs = entry["expected_cidrs"]
        require(isinstance(cidrs, list) and 1 <= len(cidrs) <= 8, "approved PE CIDRs required")
        nets = [ipaddress.IPv4Network(cidr) for cidr in cidrs]
        require(all(any(net.subnet_of(block) for block in rest04.RFC1918) for net in nets),
                "PE CIDRs must be within approved private IPv4 space")
        require(all(any(ipaddress.IPv4Address(ip) in net for net in nets) for ip in arm["expected_private_ips"]),
                "pinned PE IP is outside the approved CIDRs")
    if "web" in targets and "scm" in targets:
        web, scm = (targets[key]["arm"] for key in ("web", "scm"))
        exclude = {"a_record_id", "expected_record_fqdn"}
        require(all(web[key] == scm[key] for key in web.keys() - exclude),
                "App Service and SCM must use the same approved PE and DNS topology")
    resolvers = config.get("resolver_ips")
    require(isinstance(resolvers, list) and 1 <= len(resolvers) <= 3
            and all(rest04.private_ip(ip) for ip in resolvers) and len(set(resolvers)) == len(resolvers),
            "supply one to three distinct private IPv4 resolver addresses")
    return config


def dig_query(resolver, fqdn, kind):
    try:
        result = subprocess.run(
            ["dig", "-r", "@" + resolver, fqdn + ".", kind, "+tcp", "+time=2", "+tries=1",
             "+noall", "+comments", "+answer"],
            capture_output=True, text=True, timeout=5, check=False,
        )
    except FileNotFoundError:
        raise NotReadyError("dig is unavailable") from None
    except subprocess.TimeoutExpired:
        raise NotReadyError("DNS query timed out") from None
    if result.returncode:
        raise NotReadyError("DNS query failed or timed out")
    header = re.search(r"status:\s*([A-Z]+),", result.stdout)
    if header is None or header[1] != "NOERROR":
        status = header[1] if header and header[1] in {"NXDOMAIN", "REFUSED", "SERVFAIL"} else "unavailable"
        raise NotReadyError("DNS response " + status)
    rows = []
    for line in result.stdout.splitlines():
        if not line.strip() or line.startswith(";"):
            continue
        fields = line.split()
        if len(fields) != 5 or not fields[1].isdigit() or fields[2] != "IN" or fields[3] not in {"CNAME", "A"}:
            raise Mismatch("unexpected DNS answer format")
        owner, _, _, record_type, data = fields
        rows.append((owner.rstrip(".").lower(), record_type, data.rstrip(".").lower()))
    if len(rows) > 32:
        raise Mismatch("DNS answer exceeds expected size")
    return rows


def check_addresses(rows, chain, expected):
    if not rows:
        raise NotReadyError("DNS answer is empty")
    edges = {(source, "CNAME", destination) for source, destination in zip(chain, chain[1:])}
    actual = set(rows)
    wanted = edges | {(chain[-1], "A", ip) for ip in expected}
    if actual != wanted or len(rows) != len(actual):
        raise Mismatch("A answer owners, aliases or complete address set differ from approval")


def check_aliases(query, resolver, chain):
    for index, owner in enumerate(chain):
        rows = query(resolver, owner, "CNAME")
        expected = [(owner, "CNAME", chain[index + 1])] if index + 1 < len(chain) else []
        if rows != expected:
            raise Mismatch("CNAME hop or terminal alias differs from approval")


def owner_inventory(document):
    require(document.get("complete_for_review") is True, "DNS ownership inventory has not been supplied")
    zones = document.get("zones", [])
    require(isinstance(zones, list) and bool(zones), "approved DNS ownership inventory required")
    bindings = set()
    for entry in zones:
        zone = name(entry["zone"])
        for key in ("dns_view", "zone_resource_id", "owner"):
            require(isinstance(entry[key], str) and entry[key].strip(), "incomplete DNS ownership evidence")
        binding = (entry["dns_view"].casefold(), zone)
        if binding in bindings:
            raise Mismatch("duplicate zone declarations in one DNS visibility domain")
        bindings.add(binding)


def assess_arm(client, targets):
    cache, results = {}, {}
    for profile, entry in targets.items():
        arm = entry["arm"]
        try:
            observations = {}
            for role, api in rest04.API_VERSIONS.items():
                target = arm[rest04.PATH_KEYS[role]]
                key = (target, api)
                if key not in cache:
                    cache[key] = client.get_resource(target, api)
                observations[role] = cache[key]
            # REST04 validates the record against the PE NIC, direct VNet link,
            # target subresource and approval without exposing raw observations.
            result = rest04.assess_target(arm, observations)
            results[profile] = result
        except (NotReadyError, RestFailure, ValueError, TypeError, AttributeError, OSError):
            results[profile] = {"missing": ["approved ARM identity, target or observations unavailable"]}
    return results


def arm_status(evidence, category):
    if evidence is None:
        return "NOT_READY", "approved service/SCM input absent"
    prefixes = {
        "zone": ("vnetLink.",),  # The REST04 evidence envelope already verifies the exact zone object.
        "group": ("pe.", "zoneGroup."),
        "link": ("vnetLink.",),
        "endpoint": ("pe.", "nic.", "zoneGroup.", "vnetLink.", "dns."),
    }[category]
    issues = [item for item in evidence.get("issues", []) if item.startswith(prefixes)]
    missing = [item for item in evidence.get("missing", [])
               if item.startswith(prefixes) or not item.startswith(("pe.", "nic.", "zoneGroup.", "vnetLink.", "dns."))]
    if issues:
        return "FAIL", "REST04 mismatch: " + ", ".join(issues)
    if missing:
        return "NOT_READY", "REST04 evidence incomplete: " + ", ".join(missing)
    return "OBSERVED_NOT_ACCEPTED", ""


def findings(config, client, query=dig_query):
    targets, resolvers = config["targets"], config["resolver_ips"]
    arm = assess_arm(client, targets)
    result = {i: ("NOT_READY", "offline detector is not an Azure observation") for i in range(2, 23, 2)}
    result[17] = ("NOT_READY", "DNS owner must verify inventory completeness and visibility boundaries")
    for i in (*range(1, 10, 2), 11, 13):
        profiles = [key for key, (_, _, group) in PROFILES.items() if group == i or i in (11, 13)]
        category = "group" if i == 11 else "link" if i == 13 else "zone"
        values = [arm_status(arm.get(key), category) for key in profiles]
        # Each zone case uses only that service. The cross-service checks require
        # complete evidence of zone groups and VNet links respectively.
        errors = [(key, state, reason) for key, (state, reason) in zip(profiles, values) if state != "OBSERVED_NOT_ACCEPTED"]
        result[i] = (("FAIL" if any(state == "FAIL" for _, state, _ in errors) else "NOT_READY",
                      "; ".join(f"{key}: {reason}" for key, _, reason in errors))
                     if errors else ("OBSERVED_NOT_ACCEPTED", ""))
    for i in (15, 19, 21):
        errors = []
        for profile in PROFILES:
            if profile not in targets:
                errors.append(("NOT_READY", f"{profile}: approved DNS input absent"))
                continue
            if i == 21:
                status, reason = arm_status(arm[profile], "endpoint")
                if status != "OBSERVED_NOT_ACCEPTED":
                    errors.append((status, f"{profile}: {reason}"))
                    continue
            entry = targets[profile]
            chain = entry["cname_chain"]
            try:
                for resolver in resolvers:
                    if i == 19:
                        check_aliases(query, resolver, chain)
                    else:
                        path = chain if i == 15 else [entry["private_name"]]
                        check_addresses(query(resolver, path[0], "A"), path, entry["arm"]["expected_private_ips"])
            except (Mismatch, NotReadyError) as exc:
                errors.append(("FAIL" if isinstance(exc, Mismatch) else "NOT_READY", f"{profile}: {exc}"))
        result[i] = (("FAIL" if any(state == "FAIL" for state, _ in errors) else "NOT_READY",
                      "; ".join(reason for _, reason in errors))
                     if errors else ("OBSERVED_NOT_ACCEPTED", ""))
    return result


def synthetic_checks():
    """Run paired positive and mutation cases with no I/O."""
    target, baseline = rest04.synthetic_inputs()

    def arm_detector(role, mutate):
        clean = rest04.assess_target(target, baseline, synthetic=True)
        obs = deepcopy(baseline)
        body = obs[role]["observation"]
        mutate(body)
        obs[role]["evidence_sha256"] = rest04.digest(body)
        changed = rest04.assess_target(target, obs, synthetic=True)
        return clean["status"] == "PASS_OFFLINE_FIXTURE_ONLY" and changed["status"] != clean["status"]

    def detects(good, bad):
        good()
        try:
            bad()
        except (ValueError, Mismatch, NotReadyError):
            return True
        return False

    zone_case = {}
    base_target, base_obs = target, baseline
    for profile, (group, _, number) in PROFILES.items():
        if profile == "scm":
            continue
        old_zone = rest04.SERVICE_PROFILES["sites"][1]
        new_zone = rest04.SERVICE_PROFILES[group][1]
        provider = rest04.SERVICE_PROFILES[group][0]
        # Swap the entire linked service and zone in a synthetic, self-consistent graph.
        def convert(obj):
            return json.loads(json.dumps(obj).replace(old_zone, new_zone)
                              .replace("/providers/Microsoft.Web/sites/", provider)
                              .replace('"sites"', json.dumps(group)))
        target, baseline = convert(base_target), convert(base_obs)
        for wrapped in baseline.values():
            wrapped["evidence_sha256"] = rest04.digest(wrapped["observation"])
        zone_case[number + 1] = arm_detector("dns_zone", lambda body: body.update(id=body["id"] + "-wrong"))
    target, baseline = base_target, base_obs
    source, destination = "service.example.invalid", "service.privatelink.example.invalid"
    chain = [source, destination]
    record = (destination, "A", "10.32.5.9")
    alias = (source, "CNAME", destination)
    clean_owner = {"complete_for_review": True, "zones": [
        {"zone": "privatelink.example.invalid", "dns_view": "synthetic", "owner": "synthetic", "zone_resource_id": "synthetic"}]}
    return {**zone_case,
        12: arm_detector("zone_group", lambda body: body["properties"]["privateDnsZoneConfigs"][0]["properties"].update(privateDnsZoneId="wrong")),
        14: arm_detector("vnet_link", lambda body: body["properties"].update(registrationEnabled=True)),
        16: detects(lambda: check_addresses([alias, record], chain, ["10.32.5.9"]),
                    lambda: check_addresses([record], chain, ["10.32.5.9"])),
        18: detects(lambda: owner_inventory(clean_owner),
                    lambda: owner_inventory({**clean_owner, "zones": clean_owner["zones"] * 2})),
        20: detects(lambda: check_aliases(lambda _, host, __: [alias] if host == source else [], "resolver", chain),
                    lambda: check_aliases(lambda *_: [], "resolver", chain)),
        22: detects(lambda: check_addresses([record], [destination], ["10.32.5.9"]),
                    lambda: check_addresses([(destination, "A", "10.32.5.8")], [destination], ["10.32.5.9"])),
    }


def reports(result, mode, output):
    rows = [{"test_id": f"AZ-T30-{i:02}", "kind": KINDS.get(i, "synthetic_detector"),
             "result": state, "reason": reason, "azure_acceptance": "NOT_READY"}
            for i, (state, reason) in sorted(result.items())]
    report = {"mode": mode, "azure_accepted": 0, "release_decision": "NO_GO", "results": rows}
    suite = ET.Element("testsuite", name=f"AZ-T30-{mode}", tests=str(len(rows)),
                       failures=str(sum(x["result"] == "FAIL" for x in rows)),
                       skipped=str(sum(x["result"] == "NOT_READY" for x in rows)))
    for row in rows:
        case = ET.SubElement(suite, "testcase", name=row["test_id"], classname=row["kind"])
        if row["result"] in {"FAIL", "NOT_READY"}:
            ET.SubElement(case, "failure" if row["result"] == "FAIL" else "skipped", message=row["reason"])
        ET.SubElement(case, "system-out").text = row["result"] + "; Azure acceptance NOT_READY"
    output.mkdir(mode=0o700, exist_ok=False)
    (output / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    ET.ElementTree(suite).write(output / "junit.xml", encoding="utf-8", xml_declaration=True)


def read_file(path):
    with path.open("rb") as stream:
        raw = stream.read(65537)
    require(len(raw) <= 65536, "manifest is too large")
    return json.loads(raw)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    for flag in ("live", "selftest", "check-config", "review-ownership"):
        modes.add_argument("--" + flag, action="store_true")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    os.umask(0o077)
    result = {i: ("NOT_READY", "explicit --live and approved --config required") for i in range(1, 23)}
    mode = "not_run"
    exit_code = 2
    if args.selftest:
        mode = "synthetic"
        result = {i: ("MATCHED_OFFLINE", "positive and mutation exercised") if passed else
                  ("FAIL", "synthetic detector did not reject the deviation") for i, passed in synthetic_checks().items()}
        exit_code = int(any(status == "FAIL" for status, _ in result.values()))
    elif args.live or args.check_config or args.review_ownership:
        mode = "live" if args.live else "input_check" if args.check_config else "ownership_extract"
        try:
            require(args.config is not None, "approved --config required")
            document = read_file(args.config)
            if args.review_ownership:
                owner_inventory(document)
                result = {17: ("NOT_READY", "offline ownership fields consistent; human review still required")}
            else:
                config = validate(document)
                if args.check_config:
                    result = {i: ("NOT_READY", "input shape checked locally; test not executed") for i in range(1, 23)}
                    exit_code = 0
                else:
                    subscriptions = sorted({rest04.SUBSCRIPTION.match(entry["arm"]["service_id"])[1]
                                            for entry in config["targets"].values()})
                    client = AzureReadOnlyClient(subscriptions, workload_identity_token_provider(), read_enabled=True)
                    result = findings(config, client)
                    automatic = [result[i][0] for i in KINDS if i != 17]
                    exit_code = 1 if "FAIL" in automatic else 2 if "NOT_READY" in automatic else 0
        except Mismatch as exc:
            result = {17: ("FAIL", str(exc))}
            exit_code = 1
        except NotReadyError as exc:
            result = {i: ("NOT_READY", str(exc)) for i in range(1, 23)}
        except InputIssue as exc:
            result = {i: ("NOT_READY", str(exc)) for i in range(1, 23)}
        except (ValueError, KeyError, TypeError, AttributeError, OSError):
            result = {i: ("NOT_READY", "approved input missing, invalid or unreadable") for i in range(1, 23)}
    reports(result, mode, args.out)
    print(f"AZ-T30 mode={mode} Azure acceptance=0 exit={exit_code}; JSON and JUnit written")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
