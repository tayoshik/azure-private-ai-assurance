import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import review_p1_azure_iac as review

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 11, 19, 8, tzinfo=timezone.utc)


def before(seconds):
    return (NOW - timedelta(seconds=seconds)).isoformat()


def seal(o, a):
    a["metadata"]["observation_sha256"] = review.content_digest(o)
    a["metadata"].pop("approval_record_sha256", None)
    a["metadata"]["approval_record_sha256"] = review.content_digest(a)


def plan_change(address, kind, actions, **after):
    return {"address": address, "type": kind,
            "change": {"actions": actions, "after": after, "after_unknown": {}}}


def fixture(case_id):
    fields = {key: "synthetic-" + key for key in review.CASES[case_id]}
    for key in fields.keys() & {"commit", "source_commit"}:
        fields[key] = "a" * 40
    for key in fields.keys() & {"deployed_at"}:
        fields[key] = before(10)
    meta = dict(case_id=case_id, source_sha256="a" * 64, runner_id="test-runner",
                resource_id="test-resource")
    o = {"metadata": dict(meta, observed_at_utc=before(0)), "observation": fields.copy()}
    a = {"metadata": meta, "expected": fields.copy()}
    odata, adata = o["observation"], a["expected"]
    if case_id == "AZ-T40-15":
        odata.update(
            sanitized_report_sha256="b" * 64,
            scans={key: dict(artifact_count=3, positive_controls=1, unredacted_findings=0)
                   for key in review.LOG_CLASSES},
        )
        adata.update(artifact_count=3, sanitized_report_sha256="b" * 64)
    elif case_id == "AZ-T40-21":
        odata.update(approval_status="approved", approved_at=before(40))
        adata.update(approved_at=before(40))
    elif case_id == "AZ-T41-13":
        odata.update(synthetic_fixture=True, status="success", indexed_documents=5,
                     failed_documents=0, started_at=before(20), completed_at=before(5))
        adata.update(expected_documents=5)
    elif case_id == "AZ-T41-17":
        odata.update(isolated_test=True, status="denied", denial_reason="authorization",
                     http_status=403, fetched_documents=0)
    elif case_id == "AZ-T41-21":
        odata.update(decision="adopt", approval_status="approved",
                     connection_status="approved", reviewed_at=before(20))
        adata.update(decision="adopt", reviewed_at=before(20))
    elif case_id == "AZ-T42-15":
        odata.update(auth_method="managed_identity", internal_runtime=True,
                     token_obtained=True, token_bytes_recorded=False)
    elif case_id in {"AZ-T42-19", "AZ-T43-13"}:
        odata.update(assigned_at=before(100), initial_probe_at=before(90),
                     propagation_verified_at=before(55), retested_at=before(30),
                     propagation_status="verified", retest_status="allowed",
                     initial_request_id="request-1", propagation_probe_id="request-2",
                     retest_request_id="request-3")
        adata.update(max_wait_seconds=90)
        if case_id == "AZ-T43-13":
            odata.update(plane="cosmos_sql_data", client="sdk", account_key_used=False)
    elif case_id == "AZ-T43-21":
        odata.update(operation="update", role_type="cosmos_sql_data",
                     review_status="approved", reviewed_at=before(30))
        adata.update(operation="update", reviewed_at=before(30))
    elif case_id == "AZ-T44-15":
        changes = [
            plan_change("azurerm_search_service.s", "azurerm_search_service",
                        ["delete", "create"], public_network_access_enabled=False),
            plan_change("azurerm_role_assignment.r", "azurerm_role_assignment",
                        ["update"], role_definition_name="Reader"),
            plan_change("data.azurerm_resource_group.r", "azurerm_resource_group", ["read"]),
            plan_change("azurerm_public_ip.p", "azurerm_public_ip", ["delete"]),
            plan_change("azurerm_resource_group.r", "azurerm_resource_group", ["no-op"]),
        ]
        odata.update(sanitized=True, plan={"planned_values": {}, "resource_changes": changes})
        adata.update(required_rules=sorted(review.policy.RULES), reviewers=["one", "two"],
                     approved_resource_changes=copy.deepcopy(changes),
                     plan_sha256=review.content_digest(odata["plan"]))
    seal(o, a)
    return o, a


class AzureIaCReviewTests(unittest.TestCase):
    def result(self, case_id, o, a, verdict, reason=None):
        result = review.assess(case_id, o, a, now=NOW)
        self.assertEqual(result["result"], verdict, result)
        if reason:
            self.assertEqual(result["reason_code"], reason)
        self.assertEqual(result["release_decision"], "NO_GO")
        self.assertEqual(result["azure_live_passes"], 0)
        self.assertFalse(result["origin_signature_verified"])
        self.assertFalse(result["approval_authority_verified"])

    def test_each_case_five_outcomes(self):
        invalid = {
            "AZ-T40-15": ("scans", {}, "MISSING_LOG_SCAN_CLASSES"),
            "AZ-T40-21": ("approval_status", "pending", "UNEXPECTED_APPROVAL_STATUS"),
            "AZ-T41-13": ("status", "failed", "UNEXPECTED_STATUS"),
            "AZ-T41-17": ("http_status", 404, "INDEXER_DENIAL_NOT_DEMONSTRATED"),
            "AZ-T41-21": ("connection_status", "pending", "UNEXPECTED_CONNECTION_STATUS"),
            "AZ-T42-15": ("token_bytes_recorded", True, "UNEXPECTED_TOKEN_BYTES_RECORDED"),
            "AZ-T42-19": ("retested_at", before(60), "PROPAGATION_TIMELINE_MISMATCH"),
            "AZ-T43-13": ("account_key_used", True, "UNEXPECTED_ACCOUNT_KEY_USED"),
            "AZ-T43-21": ("role_type", "management", "UNEXPECTED_ROLE_TYPE"),
            "AZ-T44-15": ("sanitized", False, "UNEXPECTED_SANITIZED"),
        }
        for case_id, fields in review.CASES.items():
            for mode in ("match", "mismatch", "missing", "tampered", "wrong-target",
                         "wrong-case", "tampered-approval"):
                with self.subTest(case=case_id, mode=mode):
                    o, a = fixture(case_id)
                    verdict = "DIFFERENCE_REVIEW_REQUIRED"
                    reason = None
                    if mode == "match":
                        verdict = "REVIEW_REQUIRED"
                    elif mode == "mismatch":
                        key, value, reason = invalid[case_id]
                        o["observation"][key] = (
                            dict(o["observation"][key], tokens={"artifact_count": 3,
                                 "positive_controls": 1, "unredacted_findings": 1})
                            if key == "scans" else value
                        )
                        if key == "scans":
                            reason = "SENSITIVE_CI_LOG_FINDINGS"
                        seal(o, a)
                    elif mode == "missing":
                        o["observation"].pop(fields[0])
                        seal(o, a)
                        verdict, reason = "NOT_READY", "MISSING_" + fields[0].upper()
                    elif mode == "tampered":
                        o["metadata"]["observed_at_utc"] = before(1) if case_id != "AZ-T44-15" else NOW.isoformat().replace("+00:00", "Z")
                        reason = "OBSERVATION_CONTENT_DIGEST_MISMATCH"
                    elif mode == "tampered-approval":
                        a["metadata"]["approval_record_sha256"] = "e" * 64
                        reason = "APPROVAL_CONTENT_DIGEST_MISMATCH"
                    elif mode == "wrong-case":
                        o["metadata"]["case_id"] = a["metadata"]["case_id"] = "AZ-T00-00"
                        seal(o, a)
                        reason = "CASE_ID_DIFFERS"
                    else:
                        o["metadata"]["resource_id"] = "other-resource"
                        seal(o, a)
                        reason = "RESOURCE_ID_MISMATCH"
                    self.result(case_id, o, a, verdict, reason)

    def test_plan_inspects_later_rows_and_both_replacement_legs(self):
        case_id = "AZ-T44-15"
        forbidden = [
            plan_change("azurerm_public_ip.other", "azurerm_public_ip", ["create"]),
            plan_change("azurerm_search_service.other", "azurerm_search_service",
                        ["create", "delete"], public_network_access_enabled=True),
            plan_change("azurerm_role_assignment.other", "azurerm_role_assignment",
                        ["update"], role_definition_name="Owner"),
            plan_change("azurerm_monitor_diagnostic_setting.other",
                        "azurerm_monitor_diagnostic_setting", ["delete", "create"],
                        enabled_log=[{"category": "Audit"}]),
        ]
        for row in forbidden:
            with self.subTest(address=row["address"]):
                o, a = fixture(case_id)
                plan, approved = o["observation"]["plan"], a["expected"]
                plan["resource_changes"].append(row)
                approved["approved_resource_changes"].append(copy.deepcopy(row))
                approved["plan_sha256"] = review.content_digest(plan)
                seal(o, a)
                self.result(case_id, o, a, "DIFFERENCE_REVIEW_REQUIRED", "PLAN_POLICY_VIOLATION")

    def test_plan_rejects_incomplete_or_altered_plan(self):
        case_id = "AZ-T44-15"
        for change, verdict, reason in (
            ("digest", "DIFFERENCE_REVIEW_REQUIRED", "PLAN_CONTENT_DIGEST_MISMATCH"),
            ("missing_row", "DIFFERENCE_REVIEW_REQUIRED", "PLAN_OPERATION_INVENTORY_MISMATCH"),
            ("duplicate", "DIFFERENCE_REVIEW_REQUIRED", "DUPLICATE_PLAN_ADDRESS"),
            ("unknown", "NOT_READY", "UNKNOWN_PLAN_AFTER_VALUES"),
            ("output", "NOT_READY", "UNSUPPORTED_PLAN_CHANGE_SECTION"),
            ("rules", "DIFFERENCE_REVIEW_REQUIRED", "INCOMPLETE_PLAN_RULE_SET"),
            ("reviewers", "NOT_READY", "PLAN_POLICY_EVALUATION_INCOMPLETE"),
        ):
            with self.subTest(change=change):
                o, a = fixture(case_id)
                plan, expected = o["observation"]["plan"], a["expected"]
                rows = plan["resource_changes"]
                if change == "digest":
                    plan["planned_values"]["sentinel"] = "edited"
                elif change == "missing_row":
                    rows.pop()
                elif change == "duplicate":
                    rows.append(copy.deepcopy(rows[0]))
                elif change == "unknown":
                    rows[0]["change"]["after_unknown"] = {"public_network_access_enabled": True}
                elif change == "output":
                    plan["output_changes"] = {"address": {"actions": ["create"]}}
                elif change == "rules":
                    expected["required_rules"].pop()
                else:
                    expected["reviewers"] = ["same", "same"]
                if change != "digest":
                    expected["plan_sha256"] = review.content_digest(plan)
                seal(o, a)
                self.result(case_id, o, a, verdict, reason)

    def test_cli_exit_two_and_no_input_echo(self):
        case_id = "AZ-T42-15"
        marker = "sensitive-fixture-marker"
        with tempfile.TemporaryDirectory() as directory:
            observation = Path(directory) / "observation.json"
            approval = Path(directory) / "approval.json"
            for mode in ("matching", "unexpected-field", "duplicate-key", "nonfinite",
                         "oversized", "missing", "unknown-case"):
                with self.subTest(mode=mode):
                    o, a = fixture(case_id)
                    o["metadata"]["observed_at_utc"] = datetime.now(timezone.utc).isoformat()
                    if mode == "unexpected-field":
                        o["observation"]["access_token"] = marker
                    seal(o, a)
                    raw = json.dumps(o)
                    if mode == "duplicate-key":
                        raw = '{"metadata":{},"metadata":{},"observation":{}}'
                    elif mode == "nonfinite":
                        raw = '{"metadata":NaN}'
                    elif mode == "oversized":
                        raw = " " * (review.prior.MAX_DOC_BYTES + 1)
                    observation.write_text(raw)
                    approval.write_text(json.dumps(a))
                    if mode == "missing":
                        observation.unlink()
                    proc = subprocess.run(
                        [sys.executable, str(ROOT / "scripts/review_p1_azure_iac.py"),
                         "--case-id", marker if mode == "unknown-case" else case_id,
                         "--observation", str(observation), "--approved", str(approval)],
                        capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(proc.returncode, 2, proc.stderr)
                    self.assertNotIn(marker, proc.stdout + proc.stderr)
                    output = json.loads(proc.stdout)
                    result = {"matching": "REVIEW_REQUIRED",
                              "unexpected-field": "DIFFERENCE_REVIEW_REQUIRED"}
                    self.assertEqual(output["result"], result.get(mode, "NOT_READY"))
                    self.assertEqual(output["release_decision"], "NO_GO")
                    self.assertEqual(output["azure_live_passes"], 0)
