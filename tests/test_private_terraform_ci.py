"""Offline Private Runner, backend and saved-plan contract regressions."""
from copy import deepcopy
from datetime import timedelta, datetime, timezone
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import private_terraform_ci as ci

SHA = "a" * 40
SUB = "00000000-0000-0000-0000-000000000001"


def fixture():
    data = json.loads((ROOT / "specs/private-terraform-ci.example.json").read_text())
    data.update(region="eastus", subscription_id=SUB, tenant_id="00000000-0000-0000-0000-000000000002",
                target_resource_group_id=f"/subscriptions/{SUB}/resourceGroups/rg-synthetic",
                scope_approval_ref="approved synthetic scope", administrator_ref="synthetic administrator",
                private_runner_approval_ref="approved synthetic runner", reviewer_policy_ref="synthetic reviewer policy")
    data["runner"].update(ephemeral=True, owner="synthetic owner", cidr="10.44.8.0/24")
    data["network"].update(topology="dev", dns_owner="synthetic dns", pe_approver="synthetic pe", isolated_blob_dns=True,
                           bootstrap_vnet_cidr="10.20.0.0/16", bootstrap_pe_cidr="10.20.10.0/24",
                           workload_vnet_cidr="10.21.0.0/16",
                           workload_subnets={key: f"10.21.{i}.0/24" for i, key in enumerate(
                               ("gateway", "web_pe", "data_pe", "app_outbound"), 1)})
    data["backend"].update(ownership="bootstrap", owner="synthetic owner", account="syntheticbackend",
                           container="tfstate", key="dev.tfstate", private_ips=["10.20.10.4"])
    for i, role in enumerate(ci.ROLES, 10):
        data["identity"][role].update(client_id=f"00000000-0000-0000-0000-{i:012}",
                                      principal_id=f"00000000-0000-0000-0000-{i+10:012}",
                                      target_role_ref="scoped synthetic role")
    return data


class PrivateCI(unittest.TestCase):
    def setUp(self):
        self.cfg = ci.validate(fixture())

    def reject(self, mutate, message):
        cfg = deepcopy(self.cfg)
        mutate(cfg)
        with self.assertRaisesRegex(ci.NotReadyError, message):
            ci.validate(cfg)

    def test_missing_approval_and_placeholder_values(self):
        self.reject(lambda cfg: cfg.update(administrator_ref=None), "required approvals")
        self.reject(lambda cfg: cfg["backend"].update(account="changeme"), "storage account")
        self.reject(lambda cfg: cfg.update(tenant_id="00000000-0000-0000-0000-000000000000"), "placeholder UUID")

    def test_hub_scope_explicit_and_private_backend_only(self):
        self.reject(lambda cfg: cfg["backend"].update(shared_key=True), "without fallback")
        net = self.cfg["network"]
        net.update(topology="hub", isolated_blob_dns=False, hub_dns_subscription_id=SUB,
                   hub_blob_dns_zone_id=f"/subscriptions/{SUB}/resourceGroups/rg-dns/providers/Microsoft.Network/privateDnsZones/privatelink.blob.core.windows.net")
        self.assertEqual(ci.validate(self.cfg)["network"]["topology"], "hub")
        net["hub_blob_dns_zone_id"] += "-wrong"
        with self.assertRaisesRegex(ci.NotReadyError, "exact Azure Public Blob"):
            ci.validate(self.cfg)

    def test_cidr_conflicts_and_unapproved_peer(self):
        self.reject(lambda cfg: cfg["runner"].update(cidr="10.20.9.0/24"), "CIDRs overlap")
        self.reject(lambda cfg: cfg["network"]["workload_subnets"].update(web_pe="10.21.1.0/24"), "outside its VNet or overlaps")
        self.reject(lambda cfg: cfg["backend"].update(private_ips=["10.21.9.8"]), "Blob PE addresses")

    def test_wrong_subject_and_shared_identity(self):
        self.reject(lambda cfg: cfg["identity"]["apply"].update(subject=cfg["identity"]["plan"]["subject"]), "OIDC environment")
        self.reject(lambda cfg: cfg["identity"]["plan"].update(client_id=cfg["identity"]["read"]["client_id"]), "distinct")
        self.reject(lambda cfg: cfg["identity"]["read"].update(backend_role=ci.ROLES["apply"]), "separate backend")

    def test_live_event_restricted_to_protected_main_and_matching_environment(self):
        environment = {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "workflow_dispatch",
                       "GITHUB_REPOSITORY": ci.REPO, "GITHUB_REF": "refs/heads/main", "GITHUB_REF_PROTECTED": "true",
                       "GITHUB_SHA": SHA, "APPROVED_JOB_ENVIRONMENT": "nonprod-apply"}
        ci.context("apply", SHA, environment)
        for key, value in (("GITHUB_EVENT_NAME", "pull_request_target"), ("GITHUB_REF", "refs/heads/feature"),
                           ("GITHUB_REF_PROTECTED", "false"), ("GITHUB_SHA", "b" * 40),
                           ("APPROVED_JOB_ENVIRONMENT", "nonprod-plan")):
            with self.subTest(key=key), self.assertRaisesRegex(ci.NotReadyError, "protected main"):
                ci.context("apply", SHA, {**environment, key: value})

    def test_no_oidc_token_sent_to_lookalike_host(self):
        http = Mock()
        with self.assertRaisesRegex(ci.NotReadyError, "endpoint"):
            ci.github_assertion({"ACTIONS_ID_TOKEN_REQUEST_URL": "https://x.actions.githubusercontent.com.invalid/v1",
                                 "ACTIONS_ID_TOKEN_REQUEST_TOKEN": "synthetic-only"}, http)
        http.assert_not_called()

    def test_dns_failure_stops_before_transport_and_oidc(self):
        transport, credential, head = Mock(), Mock(), Mock()
        resolver = Mock(side_effect=ci.NotReadyError("DNS failure"))
        with self.assertRaisesRegex(ci.NotReadyError, "DNS"):
            ci.probe(self.cfg, "read", "synthetic", resolver=resolver, transport=transport,
                     credential_factory=credential, head=head)
        transport.assert_not_called()
        credential.assert_not_called()
        head.assert_not_called()

    def test_data_plane_403_is_not_ready_even_after_storage_token(self):
        transport, credential, trace = Mock(), Mock(), []
        credential.return_value.get_token.return_value.token = "synthetic-not-a-token"
        resolver = Mock(return_value=self.cfg["backend"]["private_ips"])
        head = Mock(return_value=(403, "AuthorizationPermissionMismatch", None))
        with self.assertRaisesRegex(ci.NotReadyError, "data-plane"):
            ci.probe(self.cfg, "read", "synthetic", resolver=resolver, transport=transport, credential_factory=credential,
                     head=head, report=trace.append)
        self.assertEqual(trace, ["private_dns", "hostname_tls", "storage_oidc_exchange"])
        credential.return_value.get_token.assert_called_once_with(ci.STORAGE_SCOPE)

    def test_requires_exact_blob_error_for_approved_initial_state(self):
        self.cfg["backend"]["allow_initial_missing_state"] = True
        credential = Mock()
        credential.return_value.get_token.return_value.token = "synthetic"
        args = {"resolver": Mock(return_value=self.cfg["backend"]["private_ips"]), "transport": Mock(),
                "credential_factory": credential}
        head = Mock(side_effect=[(200, None, None), (404, "BlobNotFound", None)])
        self.assertEqual(ci.probe(self.cfg, "plan", "synthetic", head=head, **args), "explicitly_absent")
        head.side_effect = [(200, None, None), (404, "ContainerNotFound", None)]
        with self.assertRaisesRegex(ci.NotReadyError, "state Blob"):
            ci.probe(self.cfg, "read", "synthetic", head=head, **args)

    def test_saved_plan_identity_expiry_state_and_approval(self):
        now = datetime.now(timezone.utc)
        plan, inputs, lock, state = b"synthetic-plan", b"synthetic-input", b"synthetic-lock", ci.digest(b"etag")
        manifest = ci.encoded(ci.plan_manifest(self.cfg, SHA, "12", plan, inputs, lock, state, now))
        approval = {"manifest_sha256": ci.digest(manifest), "plan_sha256": ci.digest(plan), "commit": SHA,
                    "environment": "nonprod", "run_id": "12", "approval_ref": "synthetic review",
                    "approved_at": now.isoformat()}
        arguments = [self.cfg, SHA, "12", manifest, plan, inputs, lock, state, approval, now]
        self.assertEqual(ci.verify_plan(*arguments)["commit"], SHA)
        for index, value in ((1, "b" * 40), (2, "13"), (4, b"substituted"), (5, b"different-input"),
                             (6, b"different-lock"), (7, "explicitly_absent"), (8, {**approval, "approval_ref": ""}),
                             (9, now + timedelta(hours=3))):
            mutated = arguments.copy()
            mutated[index] = value
            with self.subTest(index=index), self.assertRaises(ci.NotReadyError):
                ci.verify_plan(*mutated)

    def test_ambient_fallbacks_and_debug_are_stripped(self):
        env = ci.terraform_env(self.cfg, "plan", {"ARM_ACCESS_KEY": "synthetic", "TF_LOG": "TRACE",
                                                  "TF_CLI_ARGS": "-lock=false", "HTTPS_PROXY": "synthetic"},
                               Path("/tmp/restricted"), Path("/tmp/restricted/assertion"))
        self.assertTrue({"ARM_ACCESS_KEY", "TF_LOG", "TF_CLI_ARGS", "HTTPS_PROXY"}.isdisjoint(env))
        self.assertEqual(env["ARM_USE_CLI"], "false")
        self.assertEqual(env["ARM_USE_AZUREAD"], "true")

    def test_terraform_scope_binding_and_no_symlink(self):
        net = self.cfg["network"]
        values = {"subscription_id": SUB, "location": "eastus", "resource_group_name": "rg-synthetic",
                  "vnet_cidr": net["workload_vnet_cidr"], "subnet_cidrs": dict(zip(
                      ("app_gateway", "web_private_endpoint", "data_private_endpoint", "app_outbound"),
                      net["workload_subnets"].values(), strict=True))}
        self.assertEqual(ci.validated_tfvars(self.cfg, ci.encoded(values)), ci.encoded(values))
        values["subscription_id"] = "different"
        with self.assertRaisesRegex(ci.NotReadyError, "differs from approval"):
            ci.validated_tfvars(self.cfg, ci.encoded(values))
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            target = base / "private"
            target.write_bytes(b"mock")
            link = base / "alias"
            link.symlink_to(target)
            with self.assertRaises(OSError):
                ci.read_restricted(link, 1024)

    def test_live_candidate_is_inactive_manual_and_protected(self):
        candidate = (ROOT / "ci/private-terraform.CANDIDATE.yml").read_text()
        self.assertFalse((ROOT / ".github/workflows/private-terraform.yml").exists())
        self.assertIn("\non:\n  workflow_dispatch:", candidate)
        self.assertNotRegex(candidate, r"(?m)^  (push|pull_request|pull_request_target):")
        self.assertIn("cancel-in-progress: false", candidate)
        self.assertNotIn("upload-artifact", candidate)
        for role in ci.ROLES:
            self.assertIn(f"environment: nonprod-{role}", candidate)
            self.assertIn(f"--live-role {role}", candidate)
        for pattern in ("github.ref_protected", "inputs.commit == github.sha", "persist-credentials: false",
                        "group: azure-private-nonprod"):
            self.assertEqual(candidate.count(pattern), 3)
        self.assertEqual(len(re.findall(r"uses: actions/checkout@[0-9a-f]{40}", candidate)), 3)
        self.assertIn("TF_PRIVATE_PLAN_APPROVAL", candidate)
