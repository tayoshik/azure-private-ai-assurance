"""Synthetic/offline regressions; never download or display real Actions artifacts."""
from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import triage_historical_actions_archives as triage


class HistoricalActionsArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="actions-triage-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / "incoming"
        self.outdir = self.root / "restricted"
        self.folder.mkdir(mode=0o700)
        self.outdir.mkdir(mode=0o700)
        self.outdir.chmod(0o700)

    def zip(self, entries, name="artifact.zip"):
        p = self.folder / name
        with ZipFile(p, "w", ZIP_DEFLATED) as zf:
            for item, data in entries:
                zf.writestr(item, data)
        return p

    def test_no_match_never_means_safe_or_azure_acceptance(self):
        self.zip([("safe.json", b'{"release_decision":"NO_GO"}')])
        report = triage.scan_directory(self.folder)
        self.assertEqual(report["archives_inspected"], 1)
        self.assertEqual(report["archives_requiring_restricted_review"], 1)
        self.assertEqual(report["archives"][0]["decision"], "MANUAL_REVIEW_REQUIRED")
        self.assertFalse(report["complete_historical_inventory_verified"])
        self.assertEqual(report["azure_live_accepted"], 0)
        self.assertEqual(report["release_decision"], "NO_GO")
        self.assertNotIn("safe.json", json.dumps(report))

    def test_token_is_detected_but_never_reproduced(self):
        secret = "ghp_" + "A" * 32
        self.zip([("secret/customer-PRIVATE.json", secret.encode())])
        report = triage.scan_directory(self.folder)
        row = report["archives"][0]
        self.assertIn("credential_signature_github_token", row["indicators"])
        self.assertIn("sensitive_member_name", row["indicators"])
        self.assertNotIn(secret, json.dumps(report))
        self.assertNotIn("customer-PRIVATE.json", json.dumps(report))

    def test_parent_traversal_is_flagged_without_extraction(self):
        self.zip([("../escape.txt", b"x")])
        r = triage.scan_directory(self.folder)
        self.assertIn("unsafe_member_path", r["archives"][0]["indicators"])
        self.assertFalse((self.root / "escape.txt").exists())

    def test_nested_archive_stays_uninspected_and_flagged(self):
        self.zip([("inside.zip", b"PK\\x03\\x04dummy")])
        r = triage.scan_directory(self.folder)
        self.assertIn("nested_archive_not_inspected", r["archives"][0]["indicators"])

    def test_duplicate_names_are_detected(self):
        from warnings import catch_warnings, simplefilter
        p = self.folder / "duplicate.zip"
        with catch_warnings():
            simplefilter("ignore")
            with ZipFile(p, "w", ZIP_DEFLATED) as zf:
                zf.writestr("same.txt", b"a")
                zf.writestr("same.txt", b"b")
        self.assertIn("duplicate_member_name", triage.inspect_archive(p)["indicators"])

    def test_symlink_file_rejected(self):
        outside = self.root / "external.zip"
        with ZipFile(outside, "w") as zf:
            zf.writestr("okay.txt", b"x")
        (self.folder / "linked.zip").symlink_to(outside)
        with self.assertRaises(ValueError):
            triage.scan_directory(self.folder)

    def test_oversize_member_skipped_and_flagged(self):
        self.zip([("big.txt", b"X" * (triage.MAX_MEMBER_BYTES + 1))])
        r = triage.scan_directory(self.folder)
        self.assertIn("uncompressed_or_ratio_limit", r["archives"][0]["indicators"])
        self.assertEqual(r["archives"][0]["inspected_content_members"], 0)

    def test_corrupt_zip_not_called_clean(self):
        p = self.folder / "corrupt.zip"
        p.write_bytes(b"not a zip")
        self.assertIn("unreadable_zip", triage.inspect_archive(p)["indicators"])

    def test_private_report_and_redacted_stdout(self):
        secret = b"Authorization: Bearer " + b"Z" * 40
        self.zip([("secret.txt", secret)])
        out = self.outdir / "report.json"
        with redirect_stdout(io.StringIO()) as captured:
            rc = triage.main(["--archive-dir", str(self.folder), "--report", str(out)])
        self.assertEqual(rc, 0)
        self.assertEqual(stat.S_IMODE(out.stat().st_mode), 0o600)
        self.assertNotIn(secret.decode(), captured.getvalue())
        self.assertNotIn(secret.decode(), out.read_text())
        with redirect_stdout(io.StringIO()):
            self.assertEqual(triage.main(["--archive-dir", str(self.folder), "--report", str(out)]), 2)

    def test_world_readable_report_directory_rejected(self):
        self.zip([("okay.txt", b"x")])
        self.outdir.chmod(0o755)
        with redirect_stdout(io.StringIO()):
            rc = triage.main(["--archive-dir", str(self.folder), "--report", str(self.outdir / "out.json")])
        self.assertEqual(rc, 2)
        self.assertFalse((self.outdir / "out.json").exists())

    def test_report_must_not_be_placed_inside_incoming(self):
        self.zip([("okay.txt", b"x")])
        with self.assertRaises(ValueError):
            triage.write_private_report({}, self.folder / "report.json", self.folder)

    def test_zip_member_symlink_is_flagged(self):
        p = self.folder / "member_symlink.zip"
        info = ZipInfo("link.txt")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        with ZipFile(p, "w") as zf:
            zf.writestr(info, b"../../somewhere")
        self.assertIn("nonregular_member", triage.inspect_archive(p)["indicators"])


if __name__ == "__main__":
    unittest.main()
