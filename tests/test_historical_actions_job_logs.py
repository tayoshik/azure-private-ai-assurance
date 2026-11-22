"""Issue #30 synthetic-only local historical job-log triage tests."""
from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import triage_historical_actions_job_logs as triage


class HistoricalActionsJobLogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="joblog-triage-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / "input"
        self.reports = self.root / "reports"
        self.folder.mkdir(mode=0o700)
        self.reports.mkdir(mode=0o700)
        self.folder.chmod(0o700)
        self.reports.chmod(0o700)

    def log(self, job_id, contents=b"synthetic job logs; offline only"):
        target = self.folder / f"job-{job_id}.log"
        target.write_bytes(contents)
        target.chmod(0o600)
        return target

    def test_no_signature_never_proves_confidentiality_or_inventory(self):
        self.log(123)
        r = triage.scan_directory(self.folder)
        self.assertEqual(r["job_log_files_present"], 1)
        self.assertEqual(r["job_logs_content_examined"], 1)
        self.assertEqual(r["jobs_requiring_manual_review"], 1)
        self.assertFalse(r["historical_full_job_log_inventory_verified"])
        self.assertFalse(r["log_access_exposure_verified"])
        self.assertEqual(r["historical_exposure_status"], "UNKNOWN")
        self.assertEqual(r["azure_live_accepted"], 0)
        self.assertEqual(r["release_decision"], "NO_GO")
        self.assertEqual(r["logs"][0]["decision"], "MANUAL_REVIEW_REQUIRED")

    def test_github_token_signature_detected_not_echoed(self):
        secret = b"ghp_" + b"A" * 35
        self.log(456, b"some masked? no " + secret)
        r = triage.scan_directory(self.folder)
        self.assertIn("credential_signature_github_token", r["logs"][0]["indicators"])
        self.assertNotIn(secret.decode(), json.dumps(r))

    def test_bearer_and_private_key_signatures_detected_not_echoed(self):
        secret = b"Authorization: Bearer " + b"A" * 40
        self.log(123, secret + b"\n-----BEGIN PRIVATE KEY-----\n")
        r = triage.scan_directory(self.folder)
        self.assertIn("credential_signature_authorization_credential", r["logs"][0]["indicators"])
        self.assertIn("credential_signature_private_key", r["logs"][0]["indicators"])
        self.assertNotIn(secret.decode(), json.dumps(r))

    def test_oidc_request_and_env_markers_are_review_indicators(self):
        self.log(123, b"ACTIONS_ID_TOKEN_REQUEST_TOKEN=something\n"
                      b"ARM_CLIENT_SECRET=synthetic\n"
                      b"::add-mask::hidden\n")
        flags = triage.scan_directory(self.folder)["logs"][0]["indicators"]
        self.assertIn("oidc_token_runtime_marker", flags)
        self.assertIn("environment_credential_assignment", flags)
        self.assertIn("github_workflow_command_secret_marker", flags)

    def test_debug_secret_hint_and_terraform_sensitive_paths(self):
        self.log(123, b"+ export TF_VAR_password=something\n"
                      b"plan saved as approval.tfplan\n***\n")
        flags = triage.scan_directory(self.folder)["logs"][0]["indicators"]
        self.assertIn("shell_xtrace_or_debug", flags)
        self.assertIn("terraform_sensitive_state_or_plan_reference", flags)
        self.assertIn("github_mask_placeholder_unverifiable", flags)

    def test_oversized_log_is_unexamined_not_cleared(self):
        f = self.log(123, b"")
        with f.open("wb") as stream:
            stream.truncate(triage.MAX_LOG_BYTES + 1)
        row = triage.scan_directory(self.folder)["logs"][0]
        self.assertIn("log_size_limit_unexamined", row["indicators"])
        self.assertIsNone(row["log_sha256"])
        self.assertEqual(row["decision"], "INDICATORS_PRESENT_RESTRICTED_REVIEW_REQUIRED")

    def test_unexpected_zip_or_nonlog_file_is_rejected(self):
        self.log(123)
        (self.folder / "other.zip").write_bytes(b"x")
        with self.assertRaises(ValueError):
            triage.scan_directory(self.folder)

    def test_symlink_is_rejected_without_reading_target(self):
        outside = self.root / "private-value.log"
        outside.write_bytes(b"hidden")
        (self.folder / "job-123.log").symlink_to(outside)
        with self.assertRaises(ValueError):
            triage.scan_directory(self.folder)

    def test_world_readable_log_is_rejected(self):
        self.log(123).chmod(0o644)
        with self.assertRaises(ValueError):
            triage.scan_directory(self.folder)

    def test_world_readable_input_directory_is_rejected(self):
        self.log(123)
        self.folder.chmod(0o755)
        with self.assertRaises(ValueError):
            triage.scan_directory(self.folder)

    def test_hardlinked_log_is_rejected(self):
        original = self.log(123)
        os.link(original, self.folder / "job-456.log")
        with self.assertRaises(ValueError):
            triage.scan_directory(self.folder)

    def test_duplicate_numeric_job_id_is_rejected(self):
        self.log(123)
        second = self.folder / "job-0123.log"
        second.write_bytes(b"x")
        second.chmod(0o600)
        with self.assertRaises(ValueError):
            triage.scan_directory(self.folder)

    def test_empty_input_does_not_claim_success(self):
        with self.assertRaises(ValueError):
            triage.scan_directory(self.folder)

    def test_private_report_and_console_are_redacted(self):
        secret = b"ghp_" + b"X" * 35
        self.log(987654321, b"synthetic " + secret)
        path = self.reports / "triage.json"
        with redirect_stdout(io.StringIO()) as output:
            rc = triage.main(["--log-dir", str(self.folder), "--report", str(path)])
        self.assertEqual(rc, 0, output.getvalue())
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        self.assertNotIn(secret.decode(), path.read_text(encoding="utf-8"))
        self.assertNotIn(secret.decode(), output.getvalue())
        self.assertNotIn("987654321", output.getvalue())
        self.assertEqual(json.loads(output.getvalue())["release_decision"], "NO_GO")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(triage.main(["--log-dir", str(self.folder),
                                         "--report", str(path)]), 2)

    def test_public_report_directory_rejected(self):
        self.log(123)
        self.reports.chmod(0o755)
        with redirect_stdout(io.StringIO()):
            rc = triage.main(["--log-dir", str(self.folder),
                              "--report", str(self.reports / "report.json")])
        self.assertEqual(rc, 2)
        self.assertFalse((self.reports / "report.json").exists())

    def test_report_inside_input_dir_rejected(self):
        self.log(123)
        with redirect_stdout(io.StringIO()):
            rc = triage.main(["--log-dir", str(self.folder),
                              "--report", str(self.folder / "report.json")])
        self.assertEqual(rc, 2)
        self.assertFalse((self.folder / "report.json").exists())


if __name__ == "__main__":
    unittest.main()
