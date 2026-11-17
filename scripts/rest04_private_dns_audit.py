#!/usr/bin/env python3
"""REST04: fail-closed PE/NIC/DNS configuration consistency assessor.

Local CLI is SYNTHETIC ONLY; no Azure calls occur. A separately approved CI
caller may use audit_client() with REST02's allowlisted read-only GET client.
No outcome from this module represents completed private DNS resolution,
network reachability, TLS validation, or live Azure acceptance.
"""
from __future__ import annotations

import argparse
import copy
import ipaddress
import json
import re
import sys
from pathlib import Path

from azure_rest_reader import AzureReadOnlyClient, NotReadyError
from rest03_resource_audit import digest

API_VERSIONS = {"pe": "2025-05-01", "nic": "2025-05-01", "zone_group": "2025-05-01",
                "dns_zone": "2018-09-01", "a_record": "2018-09-01", "vnet_link": "2018-09-01"}
ROLES = tuple(API_VERSIONS)
PATH_KEYS = {"pe": "private_endpoint_id", "nic": "nic_id", "zone_group": "zone_group_id",
             "dns_zone": "dns_zone_id", "a_record": "a_record_id", "vnet_link": "vnet_link_id"}
SUBSCRIPTION = re.compile(r"^/subscriptions/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/", re.I)
RESOURCE = re.compile(r"^/subscriptions/[0-9a-f-]+/resourceGroups/[^/?#]+/providers/[A-Za-z0-9.]+/[A-Za-z0-9./_-]+$", re.I)
EXPECTED_TYPES = {"pe": "microsoft.network/privateendpoints", "nic": "microsoft.network/networkinterfaces",
                  "zone_group": "microsoft.network/privateendpoints/privatednszonegroups",
                  "dns_zone": "microsoft.network/privatednszones",
                  "a_record": "microsoft.network/privatednszones/a",
                  "vnet_link": "microsoft.network/privatednszones/virtualnetworklinks"}
RFC1918 = tuple(ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"))
# Service/Private Link subresource and public-cloud private DNS pair must agree.
# Add non-public-cloud mappings only after separately reviewed architecture ADR.
SERVICE_PROFILES = {
    "sites": ("/providers/microsoft.web/sites/", "privatelink.azurewebsites.net"),
    "account": ("/providers/microsoft.cognitiveservices/accounts/", "privatelink.openai.azure.com"),
    "searchservice": ("/providers/microsoft.search/searchservices/", "privatelink.search.windows.net"),
    "sql": ("/providers/microsoft.documentdb/databaseaccounts/", "privatelink.documents.azure.com"),
    "vault": ("/providers/microsoft.keyvault/vaults/", "privatelink.vaultcore.azure.net"),
    "blob": ("/providers/microsoft.storage/storageaccounts/", "privatelink.blob.core.windows.net"),
}


def same_id(a, b):
    return isinstance(a, str) and isinstance(b, str) and a.casefold() == b.casefold()


def get_path(v, *parts):
    for name in parts:
        if not isinstance(v, dict) or name not in v:
            return None
        v = v[name]
    return v


def private_ip(s):
    try:
        ip = ipaddress.ip_address(s)
    except (ValueError, TypeError):
        return False
    return ip.version == 4 and any(ip in cidr for cidr in RFC1918)


def validate_target(target):
    """Validate manifest scope without guessing asset IDs, IPs or FQDNs."""
    required = {*PATH_KEYS.values(), "service_id", "subnet_id", "vnet_id", "group_id",
                "expected_private_ips", "expected_record_fqdn"}
    if (not isinstance(target, dict) or not required <= set(target)
            or set(target) - required - {"expected_link_vnet_id"}):
        raise ValueError("REST04 manifest requires exactly the documented fields")
    ids = [*PATH_KEYS.values(), "service_id", "subnet_id", "vnet_id"]
    if "expected_link_vnet_id" in target:
        ids.append("expected_link_vnet_id")
    for key in ids:
        value = target.get(key)
        if not isinstance(value, str) or not RESOURCE.fullmatch(value) or not SUBSCRIPTION.match(value):
            raise ValueError("REST04 manifest contains malformed ARM resource ID")
    subs = {SUBSCRIPTION.match(target[k]).group(1).casefold() for k in ids}
    if len(subs) != 1:
        raise ValueError("REST04 v1 requires single approved subscription scope")
    if "expected_link_vnet_id" in target and not re.fullmatch(
            r"/subscriptions/[0-9a-f-]+/resourceGroups/[^/?#]+/providers/Microsoft[.]Network/virtualNetworks/[A-Za-z0-9_.-]+",
            target["expected_link_vnet_id"], re.I):
        raise ValueError("expected linked VNet must be an exact VNet resource ID")
    pe = target["private_endpoint_id"].casefold()
    zone = target["dns_zone_id"].casefold()
    expected_types = {"private_endpoint_id": "/microsoft.network/privateendpoints/",
        "nic_id": "/microsoft.network/networkinterfaces/",
        "zone_group_id": "/microsoft.network/privateendpoints/",
        "dns_zone_id": "/microsoft.network/privatednszones/",
        "a_record_id": "/microsoft.network/privatednszones/",
        "vnet_link_id": "/microsoft.network/privatednszones/",
        "subnet_id": "/microsoft.network/virtualnetworks/",
        "vnet_id": "/microsoft.network/virtualnetworks/"}
    for key, fragment in expected_types.items():
        if fragment not in target[key].casefold():
            raise ValueError("unexpected ARM type in manifest")
    if not target["zone_group_id"].casefold().startswith(pe + "/privatednszonegroups/"):
        raise ValueError("DNS zone group must be child of approved PE")
    if not target["a_record_id"].casefold().startswith(zone + "/a/"):
        raise ValueError("A record must be child of approved private DNS zone")
    if not target["vnet_link_id"].casefold().startswith(zone + "/virtualnetworklinks/"):
        raise ValueError("VNet link must be child of approved private DNS zone")
    if not target["subnet_id"].casefold().startswith(target["vnet_id"].casefold() + "/subnets/"):
        raise ValueError("subnet is not inside approved VNet")
    group = target["group_id"]
    if not isinstance(group, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", group):
        raise ValueError("invalid approved PE group")
    profile = SERVICE_PROFILES.get(group.casefold())
    if profile is None or profile[0] not in target["service_id"].casefold():
        raise ValueError("service type/Private Link group is not an approved REST04 profile")
    if target["dns_zone_id"].split("/")[-1].casefold() != profile[1]:
        raise ValueError("DNS zone mismatches service Private Link group")
    ips = target["expected_private_ips"]
    if not isinstance(ips, list) or not 1 <= len(ips) <= 8 or any(not private_ip(ip) for ip in ips) or len(set(ips)) != len(ips):
        raise ValueError("approved private IPs must be distinct RFC1918 IPv4 addresses")
    fqdn = target["expected_record_fqdn"]
    if not isinstance(fqdn, str) or not re.fullmatch(r"[a-z0-9][a-z0-9.-]{2,252}", fqdn) or fqdn.endswith("."):
        raise ValueError("invalid pinned FQDN")
    zone_name = target["dns_zone_id"].split("/")[-1]
    record_name = target["a_record_id"].split("/")[-1]
    if fqdn.casefold() != (record_name + "." + zone_name).casefold():
        raise ValueError("A record/FQDN/zone name do not match")
    return target


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or manifest.get("schema") != "azure-private-ai-assurance/rest04-manifest/v1":
        raise ValueError("unknown REST04 manifest schema")
    ts = manifest.get("targets")
    if not isinstance(ts, list) or not 1 <= len(ts) <= 25:
        raise ValueError("REST04 must use 1..25 explicit targets")
    seen = set()
    for target in ts:
        validate_target(target)
        key = target["private_endpoint_id"].casefold()
        if key in seen:
            raise ValueError("duplicate PE manifest entry")
        seen.add(key)
    return ts


def _verified_observations(target, observations):
    if not isinstance(observations, dict) or set(observations) != set(ROLES):
        return None
    raw = {}
    for role in ROLES:
        wrap = observations.get(role)
        if not isinstance(wrap, dict) or wrap.get("state") != "OBSERVED_NOT_ACCEPTED":
            return None
        rid = target[PATH_KEYS[role]]
        body = wrap.get("observation")
        if not isinstance(body, dict) or not same_id(wrap.get("resource_id"), rid) or not same_id(body.get("id"), rid):
            return None
        if not isinstance(wrap.get("evidence_sha256"), str) or wrap["evidence_sha256"] != digest(body):
            return None
        if not same_id(body.get("type"), EXPECTED_TYPES[role]):
            return None
        raw[role] = body
    return raw


def assess_target(target, observations, *, synthetic=False):
    """Verify ARM control-plane consistency; a good observation is NOT a DNS probe."""
    target = validate_target(target)
    result = {"target_sha256": digest(target), "status": "NOT_READY", "azure_live_acceptance": "NOT_READY",
              "private_dns_runtime_proven": False, "azure_live_passes": 0}
    data = _verified_observations(target, observations)
    if data is None:
        return {**result, "missing": ["complete, scoped, digest-verified REST02 observations"]}
    problems, missing = [], []
    pe, nic, grp, zone, arec, link = (data[k] for k in ROLES)
    pep = get_path(pe, "properties") or {}
    def must_equal(actual, expected, check):
        if actual is None:
            missing.append(check)
        elif not same_id(actual, expected):
            problems.append(check)
    def status_ok(actual, expected, check):
        if not isinstance(actual, str):
            missing.append(check)
        elif actual.casefold() != expected.casefold():
            problems.append(check)
    must_equal(get_path(pep,"subnet","id"), target["subnet_id"], "pe.subnet")
    if get_path(pep,"provisioningState") is not None:
        status_ok(pep["provisioningState"], "Succeeded", "pe.provisioningState")
    nics = get_path(pep,"networkInterfaces")
    if not isinstance(nics, list) or not nics:
        missing.append("pe.networkInterfaces")
    elif len(nics) != 1 or not isinstance(nics[0],dict):
        missing.append("pe.networkInterfaces unreviewed topology")
    else:
        must_equal(nics[0].get("id"), target["nic_id"], "pe.nic")
    connections = []
    for key in ("privateLinkServiceConnections", "manualPrivateLinkServiceConnections"):
        xs = pep.get(key)
        if xs is not None and not isinstance(xs,list):
            missing.append("pe.connections malformed")
        elif isinstance(xs,list):
            connections.extend(xs)
    if not connections:
        missing.append("pe.connections")
    for conn in connections:
        c = get_path(conn,"properties")
        if not isinstance(c,dict):
            missing.append("pe.connection.properties")
            continue
        must_equal(c.get("privateLinkServiceId"),target["service_id"], "pe.service")
        groups = c.get("groupIds")
        if not isinstance(groups,list):
            missing.append("pe.groupIds")
        elif len(groups) != 1 or not same_id(groups[0],target["group_id"]):
            problems.append("pe.groupIds")
        status_ok(get_path(c,"privateLinkServiceConnectionState","status"),"Approved","pe.approval")
    nicp = get_path(nic,"properties") or {}
    must_equal(get_path(nicp,"privateEndpoint","id"),target["private_endpoint_id"],"nic.privateEndpoint")
    ips = []
    configs = nicp.get("ipConfigurations")
    if not isinstance(configs,list) or not configs:
        missing.append("nic.ipConfigurations")
    else:
        for ic in configs:
            props = get_path(ic,"properties")
            if not isinstance(props,dict):
                missing.append("nic.ipConfiguration.properties")
                continue
            ip = props.get("privateIPAddress")
            if not private_ip(ip):
                if ip is None:
                    missing.append("nic.privateIPAddress")
                else:
                    problems.append("nic.privateIPAddress not approved private IPv4")
            else:
                ips.append(ip)
            must_equal(get_path(props,"subnet","id"),target["subnet_id"],"nic.ipconfig.subnet")
            if props.get("publicIPAddress") is not None:
                problems.append("nic.publicIPAddress configured")
    if ips and set(ips) != set(target["expected_private_ips"]):
        problems.append("nic.privateIPAddress != approved IP set")
    gp = get_path(grp,"properties") or {}
    status_ok(gp.get("provisioningState"),"Succeeded","zoneGroup.provisioningState")
    configs = gp.get("privateDnsZoneConfigs")
    if not isinstance(configs,list) or len(configs)!=1:
        missing.append("zoneGroup.privateDnsZoneConfigs exact-one expected")
    else:
        must_equal(get_path(configs[0],"properties","privateDnsZoneId"),target["dns_zone_id"],"zoneGroup.zone")
        records = get_path(configs[0],"properties","recordSets")
        # recordSets are not populated by every supported API shape. When present,
        # check them too, but always retrieve authoritative A record separately.
        if records is not None:
            if not isinstance(records,list):
                missing.append("zoneGroup.recordSets malformed")
            else:
                for r in records:
                    if not isinstance(r,dict):
                        missing.append("zoneGroup.recordSets malformed")
                        break
                    if same_id(r.get("fqdn"),target["expected_record_fqdn"]):
                        vals=r.get("ipAddresses")
                        if not isinstance(vals,list) or set(vals)!=set(target["expected_private_ips"]):
                            problems.append("zoneGroup.recordSets IP mismatch")
    # Zone object identity/type already checked by REST02 observation wrapper.
    lp = get_path(link,"properties") or {}
    must_equal(get_path(lp,"virtualNetwork","id"),target.get("expected_link_vnet_id", target["vnet_id"]),"vnetLink.vnet")
    if lp.get("registrationEnabled") is not False:
        if lp.get("registrationEnabled") is None:
            missing.append("vnetLink.registrationEnabled")
        else:
            problems.append("vnetLink.registrationEnabled must be false")
    status_ok(lp.get("provisioningState"),"Succeeded","vnetLink.provisioningState")
    if "virtualNetworkLinkState" in lp:
        status_ok(lp["virtualNetworkLinkState"],"Completed","vnetLink.state")
    arp = get_path(arec,"properties") or {}
    entries = arp.get("aRecords")
    if not isinstance(entries,list) or not entries:
        missing.append("dns.aRecords")
    else:
        record_ips=[]
        for row in entries:
            ip=get_path(row,"ipv4Address")
            if not private_ip(ip):
                if ip is None:missing.append("dns.aRecord.ipv4Address")
                else:problems.append("dns.aRecord not approved private IPv4")
            else:record_ips.append(ip)
        if record_ips and set(record_ips)!=set(target["expected_private_ips"]):
            problems.append("dns.aRecord != approved NIC IP set")
    # Actual DNS resolution, recursive forwarding, routing, TLS and effective NSG
    # are outside ARM's control-plane response and remain unproven.
    if problems:
        state="FAIL_OFFLINE_POLICY_FIXTURE" if synthetic else "FAIL_POLICY_OBSERVED"
    elif missing:
        state="NOT_READY"
    else:
        state="PASS_OFFLINE_FIXTURE_ONLY" if synthetic else "OBSERVED_PENDING_PRIVATE_DNS_PROBE"
    return {**result,"status":state,"issues":sorted(set(problems)),"missing":sorted(set(missing)),
            "observations_sha256":digest({role:observations[role]["evidence_sha256"] for role in ROLES}),
            "control_plane_checks": ["PE approval, NIC/subnet, Private DNS zone group, A record, VNet link"]}


def audit_client(client: AzureReadOnlyClient, manifest):
    """Approved read-only CI only; never executes from the command-line entrypoint."""
    targets=validate_manifest(manifest)
    outcomes=[]
    try:
        for target in targets:
            observations={r:client.get_resource(target[PATH_KEYS[r]],API_VERSIONS[r]) for r in ROLES}
            outcomes.append(assess_target(target,observations))
    except (NotReadyError,ValueError):
        return {"status":"NOT_READY","reason_class":"missing approved ARM access or complete evidence",
                "azure_live_passes":0,"azure_live_acceptance":"NOT_READY","results":outcomes}
    if any(x["status"]=="FAIL_POLICY_OBSERVED" for x in outcomes):status="FAIL_POLICY_OBSERVED"
    elif any(x["status"]=="NOT_READY" for x in outcomes):status="NOT_READY"
    else:status="OBSERVED_PENDING_PRIVATE_DNS_PROBE"
    return {"status":status,"azure_live_passes":0,"azure_live_acceptance":"NOT_READY",
            "private_dns_runtime_proven":False,"results":outcomes}


def synthetic_inputs():
    sid="01234567-89ab-4def-8123-0123456789ab"
    rg=f"/subscriptions/{sid}/resourceGroups/rg-synthetic/providers/Microsoft.Network"
    service=f"/subscriptions/{sid}/resourceGroups/rg-synthetic/providers/Microsoft.Web/sites/web-synthetic"
    pe=rg+"/privateEndpoints/pe-web"
    nic=rg+"/networkInterfaces/pe-web-nic"
    vnet=rg+"/virtualNetworks/vnet-test"
    subnet=vnet+"/subnets/snet-pe"
    zone=rg+"/privateDnsZones/privatelink.azurewebsites.net"
    target={"private_endpoint_id":pe,"nic_id":nic,"zone_group_id":pe+"/privateDnsZoneGroups/default",
            "dns_zone_id":zone,"a_record_id":zone+"/A/web-synthetic",
            "vnet_link_id":zone+"/virtualNetworkLinks/test-link", "service_id":service,
            "subnet_id":subnet,"vnet_id":vnet,"group_id":"sites",
            "expected_private_ips":["10.32.5.9"],"expected_record_fqdn":"web-synthetic.privatelink.azurewebsites.net"}
    bodies={
        "pe":{"id":pe,"type":"Microsoft.Network/privateEndpoints","properties":{
            "subnet":{"id":subnet},"networkInterfaces":[{"id":nic}],"provisioningState":"Succeeded",
            "privateLinkServiceConnections":[{"properties":{"privateLinkServiceId":service,"groupIds":["sites"],
                "privateLinkServiceConnectionState":{"status":"Approved"}}}]}},
        "nic":{"id":nic,"type":"Microsoft.Network/networkInterfaces","properties":{
            "privateEndpoint":{"id":pe},"ipConfigurations":[{"properties":{"privateIPAddress":"10.32.5.9",
                "subnet":{"id":subnet}}}]}},
        "zone_group":{"id":target["zone_group_id"],"type":"Microsoft.Network/privateEndpoints/privateDnsZoneGroups",
            "properties":{"provisioningState":"Succeeded","privateDnsZoneConfigs":[{"properties":{"privateDnsZoneId":zone}}]}},
        "dns_zone":{"id":zone,"type":"Microsoft.Network/privateDnsZones","properties":{"numberOfRecordSets":1}},
        "a_record":{"id":target["a_record_id"],"type":"Microsoft.Network/privateDnsZones/A",
            "properties":{"aRecords":[{"ipv4Address":"10.32.5.9"}],"ttl":3600}},
        "vnet_link":{"id":target["vnet_link_id"],"type":"Microsoft.Network/privateDnsZones/virtualNetworkLinks",
            "properties":{"virtualNetwork":{"id":vnet},"registrationEnabled":False,"provisioningState":"Succeeded",
                "virtualNetworkLinkState":"Completed"}}}
    observations={r:{"state":"OBSERVED_NOT_ACCEPTED","resource_id":target[PATH_KEYS[r]],
                     "observation":d,"evidence_sha256":digest(d)} for r,d in bodies.items()}
    return target,observations


def selftest():
    target,obs=synthetic_inputs()
    good=assess_target(target,obs,synthetic=True)
    bad=copy.deepcopy(obs)
    bad["pe"]["observation"]["properties"]["privateLinkServiceConnections"][0]["properties"]["privateLinkServiceConnectionState"]["status"]="Pending"
    bad["pe"]["evidence_sha256"]=digest(bad["pe"]["observation"])
    fail=assess_target(target,bad,synthetic=True)
    missing=copy.deepcopy(obs);missing["a_record"]["evidence_sha256"]="0"*64
    nr=assess_target(target,missing,synthetic=True)
    actual=assess_target(target,obs)
    expected=["PASS_OFFLINE_FIXTURE_ONLY","FAIL_OFFLINE_POLICY_FIXTURE","NOT_READY","OBSERVED_PENDING_PRIVATE_DNS_PROBE"]
    got=[good["status"],fail["status"],nr["status"],actual["status"]]
    if got!=expected or any(x["azure_live_passes"]!=0 for x in (good,fail,nr,actual)):
        raise AssertionError(f"REST04 selftest mismatch {got}")
    return {"status":"PASS_OFFLINE_FIXTURES_ONLY","good":got[0],"bad":got[1],
            "missing":got[2],"unproven_private_dns":got[3],"azure_live_passes":0,
            "private_runner_available":False,"release_decision":"NO_GO"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--selftest",action="store_true")
    g.add_argument("--fixture",type=Path,help="SYNTHETIC observation fixture only; never live acceptance")
    args=p.parse_args()
    if args.selftest:
        result=selftest()
    else:
        fixture=json.loads(args.fixture.read_text(encoding="utf-8"))
        validate_manifest(fixture)
        targets=fixture["targets"]
        observations=fixture.get("observations")
        if not isinstance(observations,list) or len(observations)!=len(targets):
            raise ValueError("fixture requires one synthetic observation map per target")
        results=[assess_target(t,o,synthetic=True) for t,o in zip(targets,observations)]
        if any(r["status"]=="FAIL_OFFLINE_POLICY_FIXTURE" for r in results):status="FAIL_OFFLINE_POLICY_FIXTURE"
        elif any(r["status"]=="NOT_READY" for r in results):status="NOT_READY"
        else:status="PASS_OFFLINE_FIXTURES_ONLY"
        result={"status":status,"results":results,"azure_live_passes":0,"release_decision":"NO_GO"}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result["status"]=="PASS_OFFLINE_FIXTURES_ONLY" else 1

if __name__=="__main__":
    sys.exit(main())
