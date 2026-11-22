"""R41 13-case owner decision packet regressions: no silent N/A or approval."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_r41_owner_decision_packet as decisions
from audit_rest_r41_rescope import EXPECTED, ORIGINALS, PROPOSAL, inspect


class R41DecisionPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = decisions.packet(ROOT, include_cases=True)
        cls.proposal = json.loads((ROOT / PROPOSAL).read_text(encoding="utf-8"))

    def test_exact_frozen_13_case_crosswalk_and_group_counts(self):
        r = self.report
        self.assertEqual(r["status"], "DECISION_PACKET_PREPARED_NOT_APPROVED")
        self.assertEqual(r["historical_ids"], 1716)
        self.assertEqual(r["r41_cases"], len(r["cases"]))
        self.assertEqual(list(r["cases"]), list(EXPECTED))
        self.assertEqual(r["review_group_counts"], decisions.EXPECTED_GROUP_COUNTS)
        self.assertEqual(sum(r["review_group_counts"].values()), 13)
        self.assertEqual(inspect(ROOT)["result"],
                         "CROSSWALK_VERIFIED_PROPOSAL_UNAPPROVED")

    def test_every_id_has_source_locked_immutable_fingerprint_and_evidence(self):
        for original in self.proposal["cases"]:
            ident = original["id"]
            row = self.report["cases"][ident]
            with self.subTest(ident=ident):
                self.assertEqual(row["immutable_contract_sha256"],
                                 decisions.contract_digest(original))
                self.assertEqual(len(row["immutable_contract_sha256"]), 64)
                self.assertEqual(row["frozen_catalogue"], original["frozen_catalogue"])
                self.assertEqual(row["old_ref_path"], original["old_ref_path"])
                self.assertEqual(row["proposed_disposition"],
                                 original["proposed_disposition"])
                self.assertEqual(row["review_group"], decisions.GATES[ident][0])
                self.assertEqual(row["required_owner_and_reviewer_evidence_classes"],
                                 list(decisions.GATES[ident][1]))
                self.assertEqual(len(row["required_owner_and_reviewer_evidence_classes"]), 3)

    def test_every_approval_option_is_unselected_and_no_command_was_run(self):
        r = self.report
        self.assertEqual(r["scope_decisions_approved"], 0)
        self.assertEqual(r["owner_signatures_verified"], 0)
        self.assertEqual(r["independent_reviewer_signatures_verified"], 0)
        self.assertEqual(r["original_commands_executed"], 0)
        self.assertEqual(r["api_unit_test_passes_claimed"], 0)
        self.assertEqual(r["azure_live_passes"], 0)
        self.assertEqual(r["azure_not_ready"], 1716)
        self.assertEqual(r["release_decision"], "NO_GO")
        for item in r["cases"].values():
            self.assertIsNone(item["owner_decision_selected"])
            self.assertIsNone(item["approved_endpoint_or_na"])
            self.assertFalse(item["scope_change_approved"])
            self.assertFalse(item["signed_owner_evidence_verified"])
            self.assertFalse(item["independent_reviewer_signed"])
            self.assertFalse(item["original_command_executed"])
            self.assertEqual(item["azure_live_acceptance"], "NOT_READY")

    def test_health_requires_real_named_service_endpoint_decision(self):
        row = self.report["cases"]["AZ-T64-07"]
        self.assertEqual(row["review_group"], "HEALTH_ENDPOINT_DECISION")
        self.assertIn("PROOF_OF_ACTUAL_APPLICABLE_HEALTH_ENDPOINT_OR_NONE",
                      row["required_owner_and_reviewer_evidence_classes"])
        self.assertNotIn("APPROVE_EXPLICIT_NA_WITH_IMPACT_REVIEW",
                         row["available_decision_options_NOT_SELECTED"])
        self.assertIsNone(row["approved_endpoint_or_na"])

    def test_dom_cannot_automatically_be_replaced_by_api_schema_or_na(self):
        row = self.report["cases"]["AZ-T64-09"]
        self.assertEqual(row["review_group"], "UI_ONLY_REQUIREMENT_DECISION")
        self.assertIn("APPROVE_EXPLICIT_NA_WITH_IMPACT_REVIEW",
                      row["available_decision_options_NOT_SELECTED"])
        self.assertIn("APPROVE_SEPARATE_SCHEMA_REQUIREMENT_WITH_NEW_ID",
                      row["available_decision_options_NOT_SELECTED"])
        self.assertIsNone(row["owner_decision_selected"])
        self.assertFalse(row["scope_change_approved"])

    def test_search_openai_api_contracts_not_promoted_to_live(self):
        for ident in ("AZ-T64-11", "AZ-T64-13"):
            with self.subTest(ident=ident):
                row = self.report["cases"][ident]
                self.assertIn("LIVE_", " ".join(
                    row["required_owner_and_reviewer_evidence_classes"]))
                self.assertFalse(row["original_command_executed"])
                self.assertEqual(row["azure_live_acceptance"], "NOT_READY")

    def test_original_frozen_command_or_proposal_edit_changes_digest(self):
        old = self.proposal["cases"][0]
        for field, newvalue in (
            ("frozen_command", old["frozen_command"] + " && echo not-approved"),
            ("proposed_disposition", "APPROVED"),
            ("approval", "APPROVED"),
        ):
            with self.subTest(field=field):
                changed = deepcopy(old)
                changed[field] = newvalue
                self.assertNotEqual(decisions.contract_digest(old),
                                    decisions.contract_digest(changed))

    def test_reject_manipulated_source_approval_status(self):
        with tempfile.TemporaryDirectory(prefix="r41-source-negative-") as td:
            root = Path(td)
            for rel in (PROPOSAL, *ORIGINALS):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, target)
            doc = json.loads((root/PROPOSAL).read_text(encoding="utf-8"))
            doc["cases"][8]["approval"] = "APPROVED"
            (root/PROPOSAL).write_text(json.dumps(doc), encoding="utf-8")
            with self.assertRaises(decisions.DecisionError):
                decisions.packet(root)

    def test_reject_approval_or_missing_source_as_success(self):
        with tempfile.TemporaryDirectory(prefix="r41-source-negative-") as td:
            root = Path(td)
            for rel in (PROPOSAL, *ORIGINALS):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, target)
            (root/"specs/phase6_220_en.json").unlink()
            with self.assertRaises(decisions.DecisionError):
                decisions.packet(root)

    def test_cli_normal_and_strict_expected_denial(self):
        for strict, wanted in ((False, 0), (True, 2)):
            cmd = [sys.executable, str(ROOT / "scripts/build_r41_owner_decision_packet.py"),
                   "--summary-only"]
            if strict:
                cmd.append("--strict")
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True,
                               text=True, check=False)
            self.assertEqual(p.returncode, wanted, p.stderr + p.stdout)
            result = json.loads(p.stdout)
            self.assertEqual(result["r41_cases"], 13)
            self.assertEqual(result["scope_decisions_approved"], 0)
            self.assertEqual(result["release_decision"], "NO_GO")
            self.assertNotIn("cases", result)

    def test_json_output_no_raw_original_command_or_expected(self):
        with tempfile.TemporaryDirectory(prefix="r41-decision-json-") as td:
            dest = Path(td) / "r41-decision-packet.json"
            p = subprocess.run(
                [sys.executable, str(ROOT/"scripts/build_r41_owner_decision_packet.py"),
                 "--out", str(dest)], cwd=ROOT,
                capture_output=True, text=True, check=False)
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            raw = dest.read_text(encoding="utf-8")
            parsed = json.loads(raw)
            self.assertEqual(list(parsed["cases"]), list(EXPECTED))
            self.assertNotIn('"frozen_command"', raw)
            self.assertNotIn('"frozen_expected"', raw)
            self.assertNotIn('"api_unit_test_pass": true', raw.lower())
            self.assertEqual(parsed["release_decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
