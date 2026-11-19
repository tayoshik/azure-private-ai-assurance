"""Offline negative-path tests for Phase 4 plan policy guard."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.plan_policy_guard import decision

ROOT = Path(__file__).resolve().parents[1]


def test_scope():
    return {
        "approval_id": "SYNTH-UNIT-ONLY",
        "plan_sha256": "a" * 64,
        "source_commit": "abcdef012345",
        "approved_addresses": ["module.example.test"],
        "reviewers": ["reviewer_a", "reviewer_b"],
    }


def plan(kind, after=None, actions=("update",)):
    return {"resource_changes": [{
        "address": "module.example.test", "type": kind,
        "change": {"actions": list(actions), "after": after},
    }]}


class PlanPolicyTests(unittest.TestCase):
    def assess(self, rule, kind, after=None, actions=("update",), scope=None):
        return decision(rule, plan(kind, after, actions), scope or test_scope(), "a" * 64)[0]

    def test_rules_fail_on_realistic_synthetic_adverse_changes(self):
        self.assertEqual(self.assess("public_ip", "azurerm_public_ip", {}, ("create",)), "FAIL")
        self.assertEqual(self.assess("public_access", "azurerm_cognitive_account",
                                     {"public_network_access_enabled": True}), "FAIL")
        self.assertEqual(self.assess("rbac", "azurerm_role_assignment",
                                     {"role_definition_name": "Owner"}, ("create",)), "FAIL")
        self.assertEqual(self.assess("diagnostics", "azurerm_monitor_diagnostic_setting",
                                     None, ("delete",)), "FAIL")
        self.assertEqual(self.assess("diagnostics", "azurerm_monitor_diagnostic_setting",
                                     {"enabled_log": []}), "FAIL")

    def test_ambiguous_cases_fail_closed(self):
        self.assertEqual(self.assess("public_access", "azurerm_cognitive_account", {}), "NOT_READY")
        self.assertEqual(self.assess("rbac", "azurerm_role_assignment", {}), "NOT_READY")
        self.assertEqual(self.assess("diagnostics", "azurerm_monitor_diagnostic_setting",
                                     {"enabled_log": [123]}), "NOT_READY")
        self.assertEqual(self.assess("public_ip", "azurerm_public_ip", {},
                                     scope={**test_scope(), "reviewers": ["a", "a"]}), "NOT_READY")
        self.assertEqual(self.assess("public_ip", "azurerm_public_ip", {},
                                     scope={**test_scope(), "approved_addresses": []}), "NOT_READY")
        self.assertEqual(self.assess("public_ip", "azurerm_public_ip", {},
                                     scope={**test_scope(), "plan_sha256": "b"*64}), "NOT_READY")
        self.assertEqual(self.assess("public_ip", "azurerm_public_ip", {},
                                     actions=("delete", "create")), "NOT_READY")

    def test_clean_result_requires_external_review(self):
        self.assertEqual(self.assess("public_access", "azurerm_cognitive_account",
                                     {"public_network_access_enabled": False}), "REVIEW_REQUIRED")
        self.assertEqual(self.assess("diagnostics", "azurerm_monitor_diagnostic_setting",
                                     {"enabled_log": [{"category": "AuditEvent"}]}), "REVIEW_REQUIRED")
        self.assertEqual(self.assess("rbac", "azurerm_role_assignment",
                                     {"role_definition_name": "Reader"}, ("create",)), "REVIEW_REQUIRED")

    def test_clean_cli_returns_exit_two_not_success(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            data = plan("azurerm_cognitive_account", {"public_network_access_enabled": False})
            raw = json.dumps(data).encode("utf-8")
            p = base / "plan.json"
            p.write_bytes(raw)
            sc = test_scope()
            sc["plan_sha256"] = hashlib.sha256(raw).hexdigest()
            meta = base / "approval.json"
            meta.write_text(json.dumps(sc))
            proc = subprocess.run([
                sys.executable, str(ROOT / "scripts/plan_policy_guard.py"),
                "--rule", "public_access", "--plan", str(p), "--scope", str(meta),
            ], cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 2)
            j = json.loads(proc.stdout)
            self.assertEqual(j["result"], "REVIEW_REQUIRED")
            self.assertIs(j["azure_live_pass"], False)
            self.assertEqual(j["release_decision"], "NO_GO")

    def test_unknown_rule_is_not_ready(self):
        self.assertEqual(decision("not_real", {}, test_scope(), "a"*64)[0], "NOT_READY")


if __name__ == "__main__":
    unittest.main()
