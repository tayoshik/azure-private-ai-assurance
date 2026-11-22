"""Synthetic-only historical GitHub Actions artifact metadata tests."""
from __future__ import annotations
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import reconcile_historical_actions_inventory as m


class MetadataReviewTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        self.art = self.root / "artifacts.ndjson"
        self.runs = self.root / "runs.ndjson"
        self.reports = self.root / "reports"
        self.reports.mkdir(mode=0o700)
        self.reports.chmod(0o700)
        self.producers = {f"w{i}.yml" for i in range(16)}

    def a(self, ident=2, runid=1, created="2026-11-22T12:00:00Z", expired=False):
        return {"id": ident, "name": "SENSITIVE-NAME-NEVER-LEAK",
                "workflow_run": {"id": runid},
                "size_in_bytes": 100, "expired": expired,
                "created_at": created, "expires_at": "2026-12-06T12:00:00Z"}

    def r(self, ident=1, name="w1.yml", created="2026-11-22T11:00:00Z"):
        return {"id": ident, "path": ".github/workflows/" + name,
                "created_at": created, "head_sha": "abc"}

    def save(self, items, path):
        path.write_text("".join(json.dumps(i) + "\n" for i in items))
        path.chmod(0o600)

    def test_pre_guard_does_not_mean_safe(self):
        x = m.reconcile([self.a()], [self.r()], self.producers)
        self.assertEqual(x["class_counts"]["PRE_GUARD_HISTORICAL_CANDIDATE"], 1)
        self.assertFalse(x["historical_full_inventory_verified"])
        self.assertFalse(x["artifact_content_inspected"])
        self.assertEqual(x["historical_exposure_status"], "UNKNOWN")
        self.assertEqual(x["release_decision"], "NO_GO")
        self.assertNotIn("SENSITIVE-NAME-NEVER-LEAK", json.dumps(x))

    def test_after_cutoff_guard_not_verified(self):
        x = m.reconcile([self.a(created="2026-11-22T13:00:00Z")],
                        [self.r(created="2026-11-22T13:00:00Z")], self.producers)
        self.assertEqual(x["class_counts"]["AFTER_CUTOFF_GUARD_NOT_VERIFIED"], 1)

    def test_missing_run_must_be_reviewed(self):
        x = m.reconcile([self.a(runid=999)], [], self.producers)
        self.assertEqual(x["class_counts"]["UNMAPPED_RUN_RESTRICTED_REVIEW"], 1)

    def test_unknown_producer_never_marked_approved(self):
        x = m.reconcile([self.a()], [self.r(name="other.yml")], self.producers)
        self.assertEqual(x["class_counts"]["NON_PRODUCER_OR_UNKNOWN_WORKFLOW_REVIEW"], 1)

    def test_duplicate_metadata_ids_rejected(self):
        self.save([self.a(), self.a()], self.art)
        with self.assertRaises(ValueError):
            m.read_private_ndjson(self.art, kind="artifacts")

    def test_world_readable_inputs_rejected(self):
        self.save([self.a()], self.art)
        self.art.chmod(0o644)
        with self.assertRaises(ValueError):
            m.read_private_ndjson(self.art, kind="artifacts")

    def test_bad_schema_rejected(self):
        self.save([{"id": 1, "size_in_bytes": "100"}], self.art)
        with self.assertRaises(ValueError):
            m.read_private_ndjson(self.art, kind="artifacts")

    def test_private_report_mode_and_no_overwrite(self):
        out = self.reports / "out.json"
        m.create_private_report({"ok": 1}, out, (self.art, self.runs))
        self.assertEqual(stat.S_IMODE(out.stat().st_mode), 0o600)
        with self.assertRaises(FileExistsError):
            m.create_private_report({}, out, (self.art, self.runs))

    def test_public_report_directory_rejected(self):
        self.reports.chmod(0o755)
        with self.assertRaises(ValueError):
            m.create_private_report({}, self.reports / "out.json", (self.art, self.runs))

    def test_cli_never_emits_original_artifact_names(self):
        policy = self.root / "policy.json"
        policy.write_text(json.dumps({"workflow_paths": {n: ["a.json"] for n in self.producers}}))
        old = m.POLICY
        m.POLICY = policy
        self.addCleanup(setattr, m, "POLICY", old)
        self.save([self.a()], self.art)
        self.save([self.r()], self.runs)
        b = io.StringIO()
        with redirect_stdout(b):
            rc = m.main(["--artifacts", str(self.art), "--runs", str(self.runs),
                         "--report", str(self.reports / "out.json")])
        self.assertEqual(rc, 0)
        self.assertNotIn("SENSITIVE-NAME-NEVER-LEAK", b.getvalue())
        self.assertEqual(json.loads(b.getvalue())["release_decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
