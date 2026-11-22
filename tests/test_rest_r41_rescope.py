"""Offline mutation tests for the R41 proposed REST test scope crosswalk."""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_rest_r41_rescope as r41


class RescopeCrosswalk(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="r41-test-")
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        for relative in (r41.PROPOSAL, *r41.ORIGINALS):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)

    def load(self, relative=r41.PROPOSAL):
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def save(self, obj, relative=r41.PROPOSAL):
        (self.root / relative).write_text(
            json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_exact_13_original_records_are_proposals_only(self):
        result = r41.inspect(self.root)
        self.assertEqual(result["result"], "CROSSWALK_VERIFIED_PROPOSAL_UNAPPROVED")
        self.assertEqual(result["reviewed_case_count"], 13)
        self.assertEqual(result["case_ids"], list(r41.EXPECTED))
        self.assertEqual(result["original_id_count"], 1716)
        self.assertFalse(result["approved"])
        self.assertEqual(result["api_unit_test_passes"], 0)
        self.assertEqual(result["azure_live_passes"], 0)
        self.assertEqual(result["release_decision"], "NO_GO")
        self.assertEqual(result["errors"], [])

    def test_proposal_cannot_claim_approval_or_test_pass(self):
        mutations = (
            ("approval_status", "APPROVED"),
            ("frozen_case_modifications", 1),
            ("azure_independent_acceptance", 1),
            ("release_decision", "GO"),
            ("frozen_case_count", 13),
        )
        for key, value in mutations:
            with self.subTest(key=key):
                original = self.load()
                original[key] = value
                self.save(original)
                self.assertNotEqual(r41.inspect(self.root)["errors"], [])
                shutil.copyfile(ROOT / r41.PROPOSAL, self.root / r41.PROPOSAL)
        for key, value in (
            ("approval", "APPROVED"), ("api_unit_test_pass", True),
            ("frozen_case_changed", True), ("azure_live_acceptance", "PASS")
        ):
            with self.subTest(key=key):
                data = self.load()
                data["cases"][0][key] = value
                self.save(data)
                self.assertTrue(r41.inspect(self.root)["errors"])
                shutil.copyfile(ROOT / r41.PROPOSAL, self.root / r41.PROPOSAL)

    def test_reject_missing_or_duplicate_cases(self):
        data = self.load()
        data["cases"].pop()
        self.save(data)
        self.assertNotEqual(r41.inspect(self.root)["result"],
                            "CROSSWALK_VERIFIED_PROPOSAL_UNAPPROVED")
        data = self.load()
        data["cases"] = deepcopy(self.load_original_cases())
        data["cases"][1]["id"] = data["cases"][0]["id"]
        self.save(data)
        self.assertTrue(r41.inspect(self.root)["errors"])

    def load_original_cases(self):
        return json.loads((ROOT / r41.PROPOSAL).read_text(encoding="utf-8"))["cases"]

    def test_reject_proposal_drift_from_original(self):
        for field in ("frozen_command", "frozen_expected", "old_ref_path",
                      "frozen_catalogue", "proposed_disposition"):
            with self.subTest(field=field):
                data = self.load()
                data["cases"][0][field] = "incorrect"
                self.save(data)
                self.assertTrue(r41.inspect(self.root)["errors"])
                shutil.copyfile(ROOT / r41.PROPOSAL, self.root / r41.PROPOSAL)

    def test_reject_canonical_original_mutation(self):
        relative = "specs/english_tests_001_440.json"
        document = self.load(relative)
        row = next(x for x in document["cases"] if x["id"] == "AZ-T20-07")
        row["command"] = "echo this must never substitute for original"
        self.save(document, relative)
        result = r41.inspect(self.root)
        self.assertIn("AZ-T20-07: frozen command drift", result["errors"])

    def test_missing_original_is_not_a_success(self):
        (self.root / "specs/phase6_220_en.json").unlink()
        result = r41.inspect(self.root)
        self.assertTrue(result["errors"])
        self.assertEqual(result["result"], "INVALID_CROSSWALK")

    def test_missing_proposal_is_not_a_success(self):
        (self.root / r41.PROPOSAL).unlink()
        result = r41.inspect(self.root)
        self.assertEqual(result["result"], "INVALID_PROPOSAL")
        self.assertFalse(result["approved"])

    def test_strict_blocks_without_scope_approval(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(r41.main(["--root", str(self.root)]), 0)
            self.assertEqual(r41.main(["--root", str(self.root), "--strict"]), 2)


if __name__ == "__main__":
    unittest.main()
