"""Contract-shape regression; no Azure/browser/secret/real app is used."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import validate_playwright_contract as p

ROOT = Path(__file__).resolve().parents[1]


def synthetic_candidate():
    """Intentionally UNVERIFIED test-only data, never an approved live contract."""
    return {
        "schema": "azure-private-ai-playwright-contract/v1",
        "application": {
            "source_repo": "unverified/example-application",
            "commit_sha": "a" * 40,
            "artifact_sha256": "b" * 64,
            "private_base_url": "https://web.qa.internal",
            "health_path": "/healthz",
            "login_path": "/signin",
        },
        "network": {
            "tls_hostname": "web.qa.internal",
            "internal_runner_group": "private-qa",
            "external_runner_group": "separate-deny-observer",
            "dns_owner": "fictional-network-owner",
        },
        "identity": {
            "auth_type": "EntraOIDC",
            "protected_identity_ref": "protected-environment:QA_TEST_IDENTITY_REF",
            "session_revocation_method": "owner-defined-session-revocation",
        },
        "ui": {
            "synthetic_test_data_id": "fictional-data-fixture",
            "selectors": {
                "main": "[data-testid='main']",
                "search_input": "[data-testid='search-input']",
                "search_result": "[data-testid='search-result']",
                "chat_input": "[data-testid='chat-input']",
                "chat_result": "[data-testid='chat-output']",
                "error_container": "[data-testid='error-container']",
            },
        },
        "evidence": {
            "authorization_ticket": "UNVERIFIED-FIXTURE-TICKET",
            "approved_baseline_sha256": "c" * 64,
            "retention_policy_ref": "fictional-private-retention-policy",
            "reviewer_roles": ["fictional-network-reviewer", "fictional-security-reviewer"],
        },
        "scenarios": {
            case: {"assertion_kind": kind, "criterion_reference": "specs/phase6_220_en.json#" + case}
            for case, kind in p.KIND_BY_ID.items()
        },
    }


class PlaywrightContractTests(unittest.TestCase):
    def test_exact_nine_journey_kinds(self):
        self.assertEqual(len(p.KIND_BY_ID), 9)
        self.assertEqual(set(p.KIND_BY_ID), {f"AZ-T64-{n:02}" for n in range(1, 18, 2)})

    def test_complete_synthetic_contract_cannot_grant_azure_pass(self):
        result = p.validate(synthetic_candidate())
        self.assertEqual(result["errors"], [], result)
        self.assertEqual(result["result"], "CONTRACT_STRUCTURE_VALID_EXTERNAL_VERIFICATION_REQUIRED")
        self.assertFalse(result["independent_approval_verified"])
        self.assertFalse(result["private_runner_execution_verified"])
        self.assertFalse(result["app_source_verified_against_repo"])
        self.assertEqual(result["browser_tests_executed"], 0)
        self.assertEqual(result["azure_live_passes"], 0)
        self.assertEqual(result["release_decision"], "NO_GO")

    def test_invalid_or_missing_application_source(self):
        for value in ("not-a-repo", "https://github.com/owner/repo", "", "TODO"):
            data = synthetic_candidate()
            data["application"]["source_repo"] = value
            self.assertEqual(p.validate(data)["result"], "NOT_READY", value)
        data = synthetic_candidate()
        data["application"]["commit_sha"] = "short"
        self.assertEqual(p.validate(data)["result"], "NOT_READY")
        data = synthetic_candidate()
        data["application"]["artifact_sha256"] = "bad"
        self.assertEqual(p.validate(data)["result"], "NOT_READY")

    def test_reject_fake_or_insecure_url(self):
        for url in ("http://web.qa.internal", "https://localhost",
                    "https://127.0.0.1", "https://example.com",
                    "https://web.example.com", "https://user:pw@web.qa.internal",
                    "https://web.qa.internal/?token=not-real",
                    "https://web.qa.internal:9000"):
            data = synthetic_candidate()
            data["application"]["private_base_url"] = url
            self.assertEqual(p.validate(data)["result"], "NOT_READY", url)

    def test_tls_host_must_equal_private_host(self):
        data = synthetic_candidate()
        data["network"]["tls_hostname"] = "some-other.internal"
        self.assertEqual(p.validate(data)["result"], "NOT_READY")

    def test_unauthorized_or_identical_runners_rejected(self):
        data = synthetic_candidate()
        data["network"]["external_runner_group"] = data["network"]["internal_runner_group"]
        self.assertEqual(p.validate(data)["result"], "NOT_READY")

    def test_credentials_must_not_be_embedded_in_manifest(self):
        for name in ("password", "access_token", "client_secret", "private_key", "cookie", "api_key"):
            data = synthetic_candidate()
            data["identity"][name] = "REDACTED-TEST-VALUE"
            o = p.validate(data)
            self.assertEqual(o["result"], "NOT_READY", name)
            self.assertNotIn("REDACTED-TEST-VALUE", json.dumps(o))
        data = synthetic_candidate()
        data["identity"]["protected_identity_ref"] = "actual-plain-text-credential"
        self.assertEqual(p.validate(data)["result"], "NOT_READY")

    def test_reject_missing_wildcard_or_wrong_scenario(self):
        data = synthetic_candidate()
        del data["scenarios"]["AZ-T64-15"]
        self.assertEqual(p.validate(data)["result"], "NOT_READY")
        data = synthetic_candidate()
        data["scenarios"]["AZ-T64-15"]["assertion_kind"] = "page_loaded"
        self.assertEqual(p.validate(data)["result"], "NOT_READY")
        data = synthetic_candidate()
        data["scenarios"]["AZ-T64-17"]["criterion_reference"] = ""
        self.assertEqual(p.validate(data)["result"], "NOT_READY")

    def test_empty_fake_ui_selectors_rejected(self):
        for value in ("", "TODO", "placeholder"):
            data = synthetic_candidate()
            data["ui"]["selectors"]["chat_input"] = value
            self.assertEqual(p.validate(data)["result"], "NOT_READY")

    def test_cannot_self_attest_two_reviewers(self):
        data = synthetic_candidate()
        data["evidence"]["reviewer_roles"] = ["same-role", "same-role"]
        self.assertEqual(p.validate(data)["result"], "NOT_READY")
        data = synthetic_candidate()
        data["evidence"]["approved_baseline_sha256"] = "wrong"
        self.assertEqual(p.validate(data)["result"], "NOT_READY")

    def test_cli_structurally_complete_still_exits_two(self):
        with tempfile.TemporaryDirectory() as folder:
            contract = Path(folder) / "candidate.json"
            contract.write_text(json.dumps(synthetic_candidate()), encoding="utf-8")
            run = subprocess.run([sys.executable,
                                  str(ROOT/"scripts/validate_playwright_contract.py"),
                                  "--contract", str(contract)],
                                 cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 2, run.stderr)
            report = json.loads(run.stdout)
            self.assertEqual(report["result"], "CONTRACT_STRUCTURE_VALID_EXTERNAL_VERIFICATION_REQUIRED")
            self.assertEqual(report["azure_live_passes"], 0)

    def test_cli_missing_or_corrupt_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.json"
            for exists in (False, True):
                if exists:
                    path.write_text("not json", encoding="utf-8")
                run = subprocess.run([sys.executable,
                                      str(ROOT/"scripts/validate_playwright_contract.py"),
                                      "--contract", str(path)],
                                     cwd=ROOT, capture_output=True, text=True, check=False)
                self.assertEqual(run.returncode, 2)
                report = json.loads(run.stdout)
                self.assertEqual(report["result"], "NOT_READY")
                self.assertEqual(report["release_decision"], "NO_GO")

    def test_invalid_root_and_unexpected_types_do_not_crash(self):
        for bad in (None, [], ["unexpected"], {"schema": "unknown"},
                    {"schema": "azure-private-ai-playwright-contract/v1",
                     "ui": {"selectors": None}, "evidence": {"reviewer_roles": []}}):
            o = p.validate(bad)
            self.assertEqual(o["result"], "NOT_READY")
            self.assertEqual(o["release_decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
