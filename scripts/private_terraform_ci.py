"""Private Terraform execution contract. Network and Terraform require an explicit live phase."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from email.utils import formatdate
import hashlib
import ipaddress
import json
import logging
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib import parse, request
from uuid import UUID

from azure_entra_step29 import AUTHORITY, EXCHANGE_AUDIENCE, GITHUB_ISSUER, checked_assertion
from azure_monitor_private_audit import PrivateHTTPSConnection, resolve_private, resource_id
from azure_rest_reader import NotReadyError


REPO = "tayoshik/azure-private-ai-assurance"
STORAGE_SCOPE = "https://storage.azure.com/.default"
ROLES = {"read": "Storage Blob Data Reader", "plan": "Storage Blob Data Contributor",
         "apply": "Storage Blob Data Contributor"}
DIGEST = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"[0-9a-f]{40}")
PRIVATE = tuple(ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"))
MAX_PLAN_BYTES = 64 * 1024 * 1024
MAX_TTL = timedelta(hours=2)


def check(condition, reason):
    if not condition:
        raise NotReadyError(reason)


def approved_text(value):
    return isinstance(value, str) and bool(value.strip()) and not re.search(
        r"[<>]|\b(?:replace|example|placeholder|changeme|todo|tbd)\b", value, re.I)


def guid(value):
    parsed = UUID(value)
    check(parsed.int != 0, "a placeholder UUID remains")
    return str(parsed)


def ipv4(cidr):
    result = ipaddress.IPv4Network(cidr)
    check(any(result.subnet_of(net) for net in PRIVATE), "CIDRs must be approved private IPv4 networks")
    return result


def validate(data):
    check(data.get("schema") == "private-terraform-ci/v1" and data.get("environment") == "nonprod"
          and data.get("cloud") == "AzurePublic" and data.get("repository") == REPO,
          "approved AzurePublic nonproduction scope and repository required")
    check(re.fullmatch(r"[a-z][a-z0-9]{2,25}", data["region"]) and approved_text(data["region"]),
          "approved Azure region required")
    for key in ("scope_approval_ref", "administrator_ref", "private_runner_approval_ref", "reviewer_policy_ref"):
        check(approved_text(data[key]), "required approvals or owners are missing")
    for key in ("subscription_id", "tenant_id"):
        data[key] = guid(data[key])

    group_id = data["target_resource_group_id"]
    prefix = f"/subscriptions/{data['subscription_id']}/resourceGroups/"
    check(group_id.startswith(prefix) and re.fullmatch(r"[A-Za-z0-9_.()-]{1,90}", group_id[len(prefix):])
          and approved_text(group_id[len(prefix):]), "exact approved workload resource group scope required")

    runner = data["runner"]
    check(runner.get("placement") == "independent_management" and runner.get("ephemeral") is True
          and runner.get("group") == "azure-private-nonprod" and approved_text(runner.get("owner")),
          "approved independent ephemeral private Runner group required")
    management = ipv4(runner["cidr"])
    network = data["network"]
    check(network.get("topology") in ("hub", "dev") and approved_text(network.get("dns_owner"))
          and approved_text(network.get("pe_approver")), "approved topology, DNS owner and PE approver required")
    if network["topology"] == "hub":
        check(network.get("isolated_blob_dns") is False, "shared Hub and owned isolated Blob DNS are mutually exclusive")
        resource_id(network["hub_blob_dns_zone_id"], "Microsoft.Network/privateDnsZones",
                    [guid(network["hub_dns_subscription_id"])])
        check(network["hub_blob_dns_zone_id"].lower().endswith("/privatelink.blob.core.windows.net"),
              "shared DNS must be the exact Azure Public Blob Private DNS zone")
    else:
        check(network.get("hub_blob_dns_zone_id") is None and network.get("hub_dns_subscription_id") is None
              and network.get("isolated_blob_dns") is True, "new dev DNS needs isolated Blob DNS ownership")
    bootstrap, workload = (ipv4(network[key]) for key in ("bootstrap_vnet_cidr", "workload_vnet_cidr"))
    check(not any(a.overlaps(b) for a, b in ((bootstrap, workload), (management, bootstrap), (management, workload))),
          "management, bootstrap and workload CIDRs overlap")
    pe_net = ipv4(network["bootstrap_pe_cidr"])
    check(pe_net.subnet_of(bootstrap), "state PE subnet must fit the bootstrap VNet")
    subnets = network["workload_subnets"]
    check({"gateway", "web_pe", "data_pe", "app_outbound"} <= subnets.keys(), "workload subnet roles missing")
    prior = []
    for cidr in subnets.values():
        selected = ipv4(cidr)
        check(selected.subnet_of(workload) and all(not selected.overlaps(item) for item in prior),
              "workload subnet is outside its VNet or overlaps another subnet")
        prior.append(selected)

    backend = data["backend"]
    check(backend.get("ownership") in ("existing", "bootstrap") and approved_text(backend.get("owner")),
          "backend ownership decision required")
    check(all(backend.get(key) is False for key in ("public_access", "shared_key", "sas"))
          and backend.get("auth") == "oidc_entra", "state backend requires private Entra OIDC without fallback")
    check(re.fullmatch(r"[a-z0-9]{3,24}", backend["account"]) and approved_text(backend["account"])
          and re.fullmatch(r"[a-z0-9](?:[a-z0-9]|-(?!-)){1,61}[a-z0-9]", backend["container"])
          and approved_text(backend["container"]), "approved storage account and container names required")
    check(re.fullmatch(r"[a-zA-Z0-9_-]{1,50}\.tfstate", backend["key"]) and approved_text(backend["key"]),
          "state key must be an exact non-placeholder Blob name")
    ips = backend["private_ips"]
    check(isinstance(ips, list) and 1 <= len(ips) <= 8 and len(ips) == len(set(ips))
          and all(isinstance(ip, str) and ipaddress.IPv4Address(ip) in pe_net for ip in ips), "approved exact private Blob PE addresses required")
    check(type(backend.get("allow_initial_missing_state")) is bool, "explicit state-initialization decision required")

    principals, clients = set(), set()
    check(set(data["identity"]) == set(ROLES), "separate read, plan and apply identities required")
    for role, backend_role in ROLES.items():
        binding = data["identity"][role]
        env = "nonprod-" + role
        check(binding.get("environment") == env and binding.get("subject") == f"repo:{REPO}:environment:{env}"
              and binding.get("issuer") == GITHUB_ISSUER and binding.get("exchange_audience") == EXCHANGE_AUDIENCE,
              "GitHub OIDC environment, subject, issuer or audience differs from approval")
        check(binding.get("backend_role") == backend_role and approved_text(binding.get("target_role_ref")),
              "approved separate backend and deployment role references required")
        binding["client_id"], binding["principal_id"] = guid(binding["client_id"]), guid(binding["principal_id"])
        clients.add(binding["client_id"])
        principals.add(binding["principal_id"])
    check(len(clients) == len(principals) == len(ROLES) and clients.isdisjoint(principals),
          "role identities must be distinct service-principal and client IDs")
    return data


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def timestamp(value):
    dt = datetime.fromisoformat(value)
    check(dt.tzinfo is not None, "plan timestamps require time zones")
    return dt


def plan_manifest(cfg, commit, run_id, plan, inputs, lock, state_version, now):
    check(COMMIT.fullmatch(commit) and re.fullmatch(r"[0-9]+", run_id), "exact source commit and plan run required")
    return {"schema": "private-terraform-plan/v1", "commit": commit, "run_id": run_id, "environment": cfg["environment"],
            "contract_sha256": digest(encoded(cfg)), "inputs_sha256": digest(inputs), "lock_sha256": digest(lock),
            "plan_sha256": digest(plan), "state_version": state_version, "created": now.isoformat(), "expires": (now + MAX_TTL).isoformat()}


def verify_plan(cfg, commit, run_id, raw_manifest, plan, inputs, lock, state_version, approval, now):
    data = json.loads(raw_manifest)
    created, expires = timestamp(data["created"]), timestamp(data["expires"])
    check(created <= now < expires and timedelta(0) < expires - created <= MAX_TTL,
          "saved plan expired or has an invalid lifetime")
    check(data == plan_manifest(cfg, commit, run_id, plan, inputs, lock, state_version, created),
          "plan, commit, environment, backend, state version, inputs or lock changed")
    check(approval.get("manifest_sha256") == digest(raw_manifest)
          and approval.get("plan_sha256") == data["plan_sha256"] and approval.get("commit") == commit
          and approval.get("environment") == cfg["environment"] and approval.get("run_id") == run_id
          and approved_text(approval.get("approval_ref"))
          and created <= timestamp(approval["approved_at"]) <= now,
          "independent saved-plan approval missing or bound to a different deployment")
    return data


def context(role, commit, env):
    check(role in ROLES and COMMIT.fullmatch(commit)
          and env.get("GITHUB_ACTIONS") == "true" and env.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
          and env.get("GITHUB_REPOSITORY") == REPO and env.get("GITHUB_REF") == "refs/heads/main"
          and env.get("GITHUB_REF_PROTECTED") == "true" and env.get("GITHUB_SHA") == commit
          and env.get("APPROVED_JOB_ENVIRONMENT") == "nonprod-" + role,
          "live phases require the protected main dispatch, exact commit and matching environment")


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def github_assertion(env, http=None):
    # This URL/token is supplied by the Actions runtime, never by the manifest.
    target = parse.urlsplit(env["ACTIONS_ID_TOKEN_REQUEST_URL"])
    check(target.scheme == "https" and target.hostname and target.hostname.endswith(".actions.githubusercontent.com")
          and not target.username and not target.password and target.port in (None, 443) and not target.fragment,
          "GitHub assertion endpoint is not approved")
    query = [(k, v) for k, v in parse.parse_qsl(target.query) if k != "audience"]
    query.append(("audience", EXCHANGE_AUDIENCE))
    url = parse.urlunsplit(target._replace(query=parse.urlencode(query)))
    req = request.Request(url, headers={"Authorization": "Bearer " + env["ACTIONS_ID_TOKEN_REQUEST_TOKEN"],
                                        "Accept": "application/json"})
    opener = http or request.build_opener(request.ProxyHandler({}), NoRedirect()).open
    with opener(req, timeout=10) as response:
        raw = response.read(65537)
    check(len(raw) <= 65536, "GitHub assertion response is too large")
    value = json.loads(raw)["value"]
    check(isinstance(value, str) and 0 < len(value) <= 32768, "GitHub assertion response invalid")
    return value


def backend_head(host, ip, path, token, connection=PrivateHTTPSConnection):
    conn = connection(host, ip)
    try:
        conn.request("HEAD", path, headers={"Authorization": "Bearer " + token, "x-ms-version": "2023-11-03",
                                               "x-ms-date": formatdate(usegmt=True)})
        response = conn.getresponse()
        return response.status, response.getheader("x-ms-error-code"), response.getheader("ETag")
    finally:
        conn.close()


def probe(cfg, role, assertion, *, resolver=resolve_private, transport=PrivateHTTPSConnection,
          credential_factory=None, head=backend_head, report=lambda stage: None):
    backend = cfg["backend"]
    host = backend["account"] + ".blob.core.windows.net"
    expected = set(backend["private_ips"])
    addresses = resolver(host, expected)
    check(set(addresses) == expected, "resolver IPv4 set differs from approved Blob PE addresses")
    report("private_dns")
    for ip in addresses:
        conn = transport(host, ip)
        try:
            conn.connect()
        finally:
            conn.close()
    report("hostname_tls")
    if credential_factory is None:
        from azure.identity import ClientAssertionCredential
        credential_factory = ClientAssertionCredential
    identity = credential_factory(cfg["tenant_id"], cfg["identity"][role]["client_id"], lambda: assertion,
                                  authority=AUTHORITY, logging_enable=False)
    try:
        token = identity.get_token(STORAGE_SCOPE).token
        check(isinstance(token, str) and bool(token), "Storage audience token unavailable")
    finally:
        identity.close()
    report("storage_oidc_exchange")
    container = "/" + backend["container"]
    versions = set()
    for ip in addresses:
        status, _, _ = head(host, ip, container + "?restype=container", token)
        check(status == 200, "Blob data-plane container HEAD denied or unavailable")
        status, reason, etag = head(host, ip, container + "/" + backend["key"], token)
        if status == 200 and etag:
            versions.add(digest(etag.encode()))
        elif backend["allow_initial_missing_state"] and (status, reason) == (404, "BlobNotFound"):
            versions.add("explicitly_absent")
        else:
            raise NotReadyError("state Blob HEAD denied, missing or unavailable")
    check(len(versions) == 1, "state version differed across approved Blob peers")
    report("blob_data_plane_head")
    return versions.pop()


def protected_path(path, *, require_mount=False):
    check(path.is_absolute() and path.resolve() == path and path.is_dir()
          and (not require_mount or os.path.ismount(path)), "approved restricted plan volume unavailable")
    check(path not in (Path("/"), Path.home(), Path.cwd()) and not path.is_relative_to(Path.cwd()),
          "plan volume must be separate from checkout and home")
    return path


def read_restricted(path, limit):
    # Resolve a single approved bundle path and refuse symlink substitution.
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        import stat
        check(stat.S_ISREG(os.fstat(fd).st_mode), "expected a regular restricted plan file")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            raw = stream.read(limit + 1)
    finally:
        os.close(fd)
    check(0 < len(raw) <= limit, "restricted file size is outside the approved bound")
    return raw


def terraform_env(cfg, role, environment, temporary, assertion_path):
    # Rebuild the provider/backend credential settings. Ignore ambient CLI, MSI, SAS,
    # shared key, provider debug logs, TF_CLI_ARGS and TF_VAR overrides.
    result = {k: v for k, v in environment.items() if not k.upper().startswith(
        ("ARM_", "AZURE_", "TF_", "TFE_", "ACTIONS_ID_TOKEN_", "TF_PRIVATE_"))
        and k.upper() not in {"HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
                              "GH_TOKEN", "GITHUB_TOKEN", "ACTIONS_RUNTIME_TOKEN"}}
    overrides = {
        "ARM_CLIENT_ID": cfg["identity"][role]["client_id"], "ARM_TENANT_ID": cfg["tenant_id"],
        "ARM_SUBSCRIPTION_ID": cfg["subscription_id"], "ARM_ENVIRONMENT": "public",
        "ARM_USE_OIDC": "true", "ARM_USE_AZUREAD": "true", "ARM_USE_CLI": "false", "ARM_USE_MSI": "false",
        "ARM_RESOURCE_PROVIDER_REGISTRATIONS": "none",
        "AZURE_CONFIG_DIR": str(temporary / "azure-empty-config"),
        "ARM_OIDC_TOKEN_FILE_PATH": str(assertion_path), "TF_IN_AUTOMATION": "true",
        "TF_INPUT": "false", "TF_DATA_DIR": str(temporary / "terraform-data"),
        "TF_CLI_CONFIG_FILE": str(temporary / "terraform.rc"),
    }
    result.update(overrides)
    return result


def terraform(phase, root, env, *arguments):
    completed = subprocess.run(["terraform", f"-chdir={root}", *arguments], env=env, check=False,
                               stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    check(completed.returncode == 0, f"Terraform {phase} failed; raw output withheld")


def validated_tfvars(cfg, raw):
    check(len(raw) <= 262144, "restricted tfvars is too large")
    values = json.loads(raw)
    net = cfg["network"]
    expected_subnets = {k: net["workload_subnets"][v] for k, v in {
        "app_gateway": "gateway", "web_private_endpoint": "web_pe", "data_private_endpoint": "data_pe",
        "app_outbound": "app_outbound"}.items()}
    check(values["subscription_id"] == cfg["subscription_id"] and values["location"] == cfg["region"]
          and values["resource_group_name"].lower() == cfg["target_resource_group_id"].rsplit("/", 1)[1].lower()
          and values["vnet_cidr"] == net["workload_vnet_cidr"] and values["subnet_cidrs"] == expected_subnets,
          "workload tfvars scope or network differs from approval")
    monitoring = values.get("monitoring_private_link", {})
    check(monitoring.get("mode", "disabled") in ("disabled", net["topology"])
          and (monitoring.get("mode") != "dev"
               or monitoring.get("dev_subnet_cidr") == net["workload_subnets"].get("monitor_pe")),
          "monitor topology or subnet differs from approval")
    return raw


def perform(role, cfg, commit, env, selected_plan=None):
    context(role, commit, env)
    checkout = Path.cwd()
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    check(actual == commit and not subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"]), "checkout is not the exact clean approved commit")
    logging.getLogger("azure").addHandler(logging.NullHandler())
    logging.getLogger("azure").propagate = False
    with tempfile.TemporaryDirectory(prefix="private-tf-") as folder:
        work = Path(folder)
        assertion = work / "assertion"
        assertion.write_text(github_assertion(env), encoding="ascii")
        value = checked_assertion(assertion, cfg["identity"][role])
        state_version = probe(cfg, role, value, report=lambda name: print(f"OBSERVED {name}", flush=True))
        if role == "read":
            return
        root = checkout / "infra/environments/dev"
        check(not any(root.glob("*.auto.tfvars*"))
              and all(p.name == "terraform.tfvars.example" for p in root.glob("terraform.tfvars*")),
              "unexpected automatic Terraform variable input")
        check(not any(root.glob("override.tf*")) and not any(root.glob("*_override.tf*")),
              "unexpected Terraform override file")
        lock = (root / ".terraform.lock.hcl").read_bytes()
        inputs = validated_tfvars(cfg, env["TF_PRIVATE_TFVARS"].encode())
        plans = protected_path(Path(env["APPROVED_PLAN_VOLUME"]), require_mount=True)
        run_id = env["GITHUB_RUN_ID"] if role == "plan" else selected_plan
        check(isinstance(run_id, str) and re.fullmatch(r"[0-9]{1,22}", run_id), "approved plan run ID required")
        bundle = plans / run_id
        local_plan = work / "deployment.tfplan"
        if role == "apply":
            protected_path(bundle)
            source_plan = read_restricted(bundle / "deployment.tfplan", MAX_PLAN_BYTES)
            raw_manifest = read_restricted(bundle / "manifest.json", 16384)
            approval = json.loads(env["TF_PRIVATE_PLAN_APPROVAL"])
            verify_plan(cfg, commit, run_id, raw_manifest, source_plan, inputs, lock, state_version,
                        approval, datetime.now(timezone.utc))
            local_plan.write_bytes(source_plan)
        (work / "terraform.rc").touch()
        tfenv = terraform_env(cfg, role, env, work, assertion)
        (work / "azure-empty-config").mkdir()
        check(shutil.which("az", path=tfenv.get("PATH")) is None,
              "Terraform 1.9.8 backend requires an isolated Runner image without Azure CLI fallback")
        version = subprocess.check_output(["terraform", "version", "-json"], env=tfenv,
                                          stderr=subprocess.DEVNULL)
        info = json.loads(version)
        check(info.get("terraform_version") == "1.9.8" and info.get("platform") == "linux_amd64",
              "Terraform 1.9.8 linux_amd64 Runner required")
        backend = cfg["backend"]
        backend_args = [f"-backend-config={key}={backend[field]}" for key, field in (
            ("storage_account_name", "account"), ("container_name", "container"), ("key", "key"))]
        terraform("init", root, tfenv, "init", "-input=false", "-lockfile=readonly",
                  "-backend-config=use_azuread_auth=true", "-backend-config=use_oidc=true", *backend_args)
        if role == "plan":
            started = datetime.now(timezone.utc)
            var_file = work / "deployment.tfvars.json"
            var_file.write_bytes(inputs)
            terraform("plan", root, tfenv, "plan", "-input=false", "-lock-timeout=60s",
                      f"-var-file={var_file}", f"-out={local_plan}")
            plan = read_restricted(local_plan, MAX_PLAN_BYTES)
            # A first init or a Blob lease metadata update during plan can change the ETag.
            # Refresh the scoped token and bind the post-plan version, in addition to Terraform's stale-plan guard.
            assertion.write_text(github_assertion(env), encoding="ascii")
            value = checked_assertion(assertion, cfg["identity"]["plan"])
            state_version = probe(cfg, "plan", value)
            check(state_version != "explicitly_absent", "backend did not persist the initialized state Blob")
            manifest = plan_manifest(cfg, commit, run_id, plan, inputs, lock, state_version, started)
            # Create once in a protected mount. Reviewers approve its manifest and plan hashes separately.
            bundle.mkdir(mode=0o700)
            (bundle / "deployment.tfplan").write_bytes(plan)
            (bundle / "manifest.json").write_bytes(encoded(manifest))
        else:
            # Re-check after init at the execution boundary. Terraform also refuses stale state under its lease.
            verify_plan(cfg, commit, run_id, raw_manifest, local_plan.read_bytes(), inputs, lock, state_version,
                        approval, datetime.now(timezone.utc))
            terraform("apply", root, tfenv, "apply", "-input=false", "-lock-timeout=60s", str(local_plan))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-config", type=Path)
    mode.add_argument("--live-role", choices=ROLES)
    parser.add_argument("--commit")
    parser.add_argument("--plan-run-id")
    args = parser.parse_args(argv)
    os.umask(0o077)
    try:
        if args.check_config is not None:
            config = validate(json.loads(read_restricted(args.check_config, 65536)))
            print("CONFIG_SHAPE_VALID_NO_AZURE")
        else:
            context(args.live_role, args.commit or "", os.environ)
            config = validate(json.loads(os.environ["TF_PRIVATE_CONTRACT"]))
            perform(args.live_role, config, args.commit, os.environ, args.plan_run_id)
            print("SCOPED_PHASE_COMPLETED_NOT_AZURE_ACCEPTANCE")
        return 0
    except NotReadyError as exc:
        # Other helpers/SDKs may emit exception messages containing operational identifiers.
        if args.live_role:
            print("NOT_READY private phase stopped; use completed stage markers and restricted diagnostics")
        else:
            print(f"NOT_READY {exc}")
    except Exception:
        print("NOT_READY missing or unavailable approved input, prerequisite or scoped operation")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
