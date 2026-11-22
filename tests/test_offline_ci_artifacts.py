"""Isolated, synthetic-only adversarial tests for public CI artifact safety."""
from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import verify_offline_ci_artifacts as guard


class OfflineArtifactSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="artifact-safe-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        path = self.repo / guard.POLICY_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / guard.POLICY_PATH, path)
        self.folder = self.repo / "artifacts"
        self.stage = self.repo / "artifacts-reviewed"
        self.workflow = "terraform-provider-schema-real.yml"

    def put(self, relative="assurance-scope.txt", data=b"OFFLINE ONLY; Azure PASS 0; NO_GO\n"):
        p = self.folder / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def scan(self):
        return guard.scan(self.workflow, self.folder, self.repo, self.stage)

    def reject(self):
        with self.assertRaises(ValueError):
            self.scan()
        self.assertFalse(self.stage.exists(), "unsafe output must not stage any bytes")

    def test_exact_policy_has_16_named_workflows_and_69_paths(self):
        p = guard.load_policy(self.repo)
        self.assertEqual(len(p["workflow_paths"]), 16)
        self.assertEqual(sum(map(len, p["workflow_paths"].values())), 71)
        self.assertEqual(p["retention_days"], 14)
        self.assertEqual(p["azure_live_passes"], 0)
        self.assertEqual(p["release_decision"], "NO_GO")

    def test_allowlisted_text_is_copied_to_isolated_snapshot_byte_for_byte(self):
        original = self.put()
        report = self.scan()
        self.assertEqual(report["classification"], "OFFLINE_ARTIFACT_PREFLIGHT_PASS")
        self.assertEqual(report["file_count"], 1)
        self.assertEqual(report["azure_live_passes"], 0)
        self.assertEqual(report["network_requests"], 0)
        self.assertEqual(report["release_decision"], "NO_GO")
        staged = self.stage / "assurance-scope.txt"
        self.assertEqual(staged.read_bytes(), original.read_bytes())
        original.write_text("MUTATED AFTER REVIEW", encoding="utf-8")
        self.assertNotEqual(original.read_bytes(), staged.read_bytes())
        self.assertEqual(report["files"][0]["bytes"], staged.stat().st_size)
        self.assertEqual(len(report["files"][0]["sha256"]), 64)
        self.assertNotIn("OFFLINE ONLY", json.dumps(report))

    def test_nested_allowlisted_metadata_only(self):
        self.workflow = "execution-route-inventory.yml"
        self.put("route-1716/execution-route-compact.json", b'{"release_decision":"NO_GO"}')
        r = self.scan()
        self.assertEqual(r["file_count"], 1)
        self.assertEqual((self.stage / "route-1716/execution-route-compact.json").read_text(),
                         '{"release_decision":"NO_GO"}')

    def test_empty_missing_artifact_root_is_non_upload(self):
        result = self.scan()
        self.assertEqual(result["classification"], "SAFE_EMPTY_NO_ARTIFACT_DIR")
        self.assertEqual(result["file_count"], 0)
        self.assertFalse(self.stage.exists())

    def test_empty_existing_directory_is_non_upload(self):
        self.folder.mkdir()
        result = self.scan()
        self.assertEqual(result["classification"], "SAFE_EMPTY_ARTIFACT_DIR")
        self.assertFalse(self.stage.exists())

    def test_unlisted_private_state_is_denied(self):
        self.put("assurance-scope.txt")
        self.put("terraform.tfstate", b'{"resources":[{"sensitive":true}]}')
        self.reject()

    def test_unlisted_secret_dotenv_is_denied(self):
        self.put(".env", b"AZURE_CLIENT_SECRET=secret")
        self.reject()

    def test_unlisted_nested_file_is_denied(self):
        self.put("secrets/payload.json", b'{"message":"dummy"}')
        self.reject()

    def test_artifact_root_symlink_denied(self):
        actual = self.repo / "secret-source"
        actual.mkdir()
        self.folder.symlink_to(actual, target_is_directory=True)
        self.reject()

    def test_artifact_file_symlink_denied(self):
        self.folder.mkdir()
        outside = self.repo / "secret.txt"
        outside.write_text("external", encoding="utf-8")
        (self.folder / "assurance-scope.txt").symlink_to(outside)
        self.reject()

    def test_artifact_directory_symlink_denied(self):
        self.workflow = "execution-route-inventory.yml"
        self.folder.mkdir()
        outside = self.repo / "private"
        outside.mkdir()
        (self.folder / "route-1716").symlink_to(outside, target_is_directory=True)
        self.reject()

    def test_binary_utf8_invalid_is_denied(self):
        self.put(data=b"\xff\xfe\x00")
        self.reject()

    def test_oversized_single_artifact_is_denied(self):
        self.put(data=b"x" * (8_388_608 + 1))
        self.reject()

    def test_unauthorized_workflow_does_not_inherit_other_permissions(self):
        self.put()
        self.workflow = "offline-validation.yml"
        self.reject()

    def test_staging_directory_must_be_absent_before_scan(self):
        self.put()
        self.stage.mkdir()
        with self.assertRaises(ValueError):
            self.scan()

    def test_private_key_pem_blocked(self):
        self.put(data=b"-----BEGIN " + b"PRIVATE KEY-----\n" + b"A" * 40)
        self.reject()

    def test_github_token_signature_blocked(self):
        self.put(data=b'{"auth":"ghp_' + b"A" * 32 + b'"}')
        self.reject()

    def test_aws_access_key_signature_blocked(self):
        self.put(data=b"AKIA" + b"A" * 16)
        self.reject()

    def test_bearer_token_signature_blocked(self):
        self.put(data=b"Authorization: Bearer " + b"a" * 40)
        self.reject()

    def test_storage_account_key_signature_blocked(self):
        self.put(data=b"AccountKey=" + b"A" * 48)
        self.reject()

    def test_sas_signature_blocked(self):
        self.put(data=b"https://example.invalid/?sv=1&sig=" + b"A" * 30)
        self.reject()

    def test_long_credential_field_blocked(self):
        self.put(data=b'{"client_secret":"' + b"A" * 32 + b'"}')
        self.reject()

    def test_jwt_signature_blocked(self):
        self.put(data=b"eyJhbGciOi" + b"A" * 38 + b"." + b"A" * 24 + b"." + b"A" * 24)
        self.reject()

    def test_policy_cannot_be_modified_to_grant_restricted_path(self):
        p = self.repo / guard.POLICY_PATH
        doc = json.loads(p.read_text())
        doc["workflow_paths"][self.workflow].append("terraform.tfstate")
        p.write_text(json.dumps(doc))
        with self.assertRaises(ValueError):
            guard.load_policy(self.repo)

    def test_policy_retention_drift_is_rejected(self):
        p = self.repo / guard.POLICY_PATH
        doc = json.loads(p.read_text())
        doc["retention_days"] = 90
        p.write_text(json.dumps(doc))
        with self.assertRaises(ValueError):
            guard.load_policy(self.repo)

    def test_policy_non_string_path_is_rejected(self):
        p = self.repo / guard.POLICY_PATH
        doc = json.loads(p.read_text())
        doc["workflow_paths"][self.workflow][0] = {"path":"bad"}
        p.write_text(json.dumps(doc))
        with self.assertRaises(ValueError):
            guard.load_policy(self.repo)

    def test_cli_fail_closed_does_not_print_secret_bytes(self):
        secret = b"Authorization: Bearer " + b"Z" * 40
        self.put(data=secret)
        with redirect_stdout(io.StringIO()) as output:
            rc = guard.main(["--root", str(self.folder), "--repo-root", str(self.repo),
                             "--stage", str(self.stage), "--workflow", self.workflow])
        self.assertEqual(rc, 1)
        r = json.loads(output.getvalue())
        self.assertEqual(r["classification"], "BLOCKED_ARTIFACT_UPLOAD")
        self.assertEqual(r["release_decision"], "NO_GO")
        self.assertNotIn(secret.decode(), output.getvalue())
        self.assertFalse(self.stage.exists())

    def test_cli_valid_mock_stays_no_go(self):
        self.put()
        with redirect_stdout(io.StringIO()) as output:
            rc = guard.main(["--root", str(self.folder), "--repo-root", str(self.repo),
                             "--stage", str(self.stage), "--workflow", self.workflow])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(output.getvalue())["release_decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
