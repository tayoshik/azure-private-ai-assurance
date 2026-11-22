"""Synthetic-only coverage crosswalk for Issue #30 historical Actions job logs."""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
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
import reconcile_historical_job_log_coverage as coverage

SHA = "a" * 40
DIFFERENT_SHA = "b" * 40
DIGEST = "c" * 64
PRE_GUARD = "2026-11-21T00:00:00Z"
POST_GUARD = "2026-11-22T14:00:00Z"
PRODUCERS = {f"w{i}.yml" for i in range(16)}


def job(ident=101, rid=201, sha=SHA, attempt=1):
    return {"id": ident, "run_id": rid, "run_attempt": attempt,
            "head_sha": sha, "name": "SENSITIVE-NEVER-PUBLISH"}


def run(ident=201, date=PRE_GUARD, name="w1.yml", sha=SHA):
    return {"id": ident, "path": ".github/workflows/" + name,
            "created_at": date, "head_sha": sha,
            "status": "completed", "conclusion": "success"}


def triage_row(ident=101, digest=DIGEST, indicators=None):
    return {"job_id": ident, "log_sha256": digest,
            "log_bytes": 100, "indicators": indicators or [],
            "decision": "MANUAL_REVIEW_REQUIRED"}


def triage(rows=None):
    rows = [triage_row()] if rows is None else rows
    return {"schema": coverage.TRIAGE_SCHEMA,
            "scope": "OWNER_SUPPLIED_RESTRICTED_JOB_LOGS_ONLY",
            "logs": rows,
            "job_log_files_present": len(rows),
            "job_logs_content_examined": sum(r["log_sha256"] is not None for r in rows),
            "historical_full_job_log_inventory_verified": False,
            "log_access_exposure_verified": False,
            "historical_exposure_status": "UNKNOWN",
            "independent_security_review_signed": False,
            "azure_live_accepted": 0, "release_decision": "NO_GO"}


class HistoricalJobLogCoverageTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="joblog-coverage-")
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.base.chmod(0o700)
        self.owner = self.base / "owner"
        self.owner.mkdir(mode=0o700)
        self.owner.chmod(0o700)
        self.jobs = self.owner / "jobs.ndjson"
        self.runs = self.owner / "runs.ndjson"
        self.triage = self.owner / "joblogs-triage.json"
        self.out = self.owner / "coverage.json"

    def write(self, path, content):
        path.write_text(content, encoding="utf-8")
        path.chmod(0o600)

    def fixture(self, jobs=None, runs=None, report=None):
        j = [job()] if jobs is None else jobs
        r = [run()] if runs is None else runs
        t = triage() if report is None else report
        self.write(self.jobs, "".join(json.dumps(x) + "\n" for x in j))
        self.write(self.runs, "".join(json.dumps(x) + "\n" for x in r))
        self.write(self.triage, json.dumps(t))
        return j, r, t

    def test_matching_job_log_still_unverified_with_pre_guard_run(self):
        j, r, t = self.fixture()
        result = coverage.link(j, r, t, PRODUCERS)
        self.assertEqual(result["jobs_in_metadata"], 1)
        self.assertEqual(result["local_logs_in_triage_report"], 1)
        self.assertEqual(result["missing_or_unexamined_for_exported_jobs"], 0)
        self.assertEqual(result["classification_counts"],
                         {"PRE_GUARD_OR_OLD_SOURCE_REVIEW_REQUIRED": 1})
        self.assertEqual(result["local_coverage_counts"],
                         {"LOCAL_LOG_HEURISTIC_SCAN_ONLY": 1})
        self.assertEqual(result["historical_exposure_status"], "UNKNOWN")
        self.assertFalse(result["owner_exported_set_completeness_verified"])
        self.assertFalse(result["log_access_exposure_verified"])
        self.assertFalse(result["independent_security_review_signed"])
        self.assertEqual(result["azure_live_accepted"], 0)
        self.assertEqual(result["release_decision"], "NO_GO")
        self.assertFalse(result["review_queue"][0]["original_job_log_content_signed"])

    def test_post_cutoff_run_does_not_prove_guarded_source(self):
        j, r, t = self.fixture(runs=[run(date=POST_GUARD)])
        result = coverage.link(j, r, t, PRODUCERS)
        self.assertEqual(result["classification_counts"],
                         {"POST_CUTOFF_SOURCE_NOT_VERIFIED": 1})
        self.assertFalse(result["run_source_security_guard_verified"])

    def test_missing_local_log_is_explicit_queue_not_safe(self):
        j, r, t = self.fixture(jobs=[job(), job(102)],
                               report=triage([triage_row(101)]))
        result = coverage.link(j, r, t, PRODUCERS)
        self.assertEqual(result["missing_or_unexamined_for_exported_jobs"], 1)
        self.assertEqual(result["review_queue"][1]["local_log_state"],
                         "LOCAL_JOB_LOG_MISSING_OR_NOT_COLLECTED")

    def test_orphan_log_not_laundered_into_known_job(self):
        j, r, t = self.fixture(report=triage([triage_row(101), triage_row(999)]))
        result = coverage.link(j, r, t, PRODUCERS)
        self.assertEqual(result["local_logs_not_in_job_metadata"], 1)
        self.assertEqual(result["classification_counts"][
                         "LOCAL_LOG_WITHOUT_EXPORTED_JOB_METADATA"], 1)
        self.assertEqual(result["review_queue"][-1]["run_id"], None)

    def test_missing_run_is_review_blocker(self):
        j, r, t = self.fixture(jobs=[job(rid=909)])
        result = coverage.link(j, r, t, PRODUCERS)
        self.assertEqual(result["review_queue"][0]["metadata_classification"],
                         "UNMAPPED_RUN_REVIEW_REQUIRED")

    def test_unrecognized_producer_is_review_blocker(self):
        j, r, t = self.fixture(runs=[run(name="unknown-producer.yml")])
        result = coverage.link(j, r, t, PRODUCERS)
        self.assertEqual(result["review_queue"][0]["metadata_classification"],
                         "UNRECOGNIZED_WORKFLOW_REVIEW_REQUIRED")

    def test_run_job_commit_mismatch_is_review_blocker(self):
        j, r, t = self.fixture(jobs=[job(sha=DIFFERENT_SHA)])
        result = coverage.link(j, r, t, PRODUCERS)
        self.assertEqual(result["review_queue"][0]["metadata_classification"],
                         "RUN_JOB_COMMIT_MISMATCH_REVIEW_REQUIRED")

    def test_oversize_unexamined_triage_is_not_inspected(self):
        unexamined = triage_row(digest=None, indicators=["log_size_limit_unexamined"])
        j, r, t = self.fixture(report=triage([unexamined]))
        result = coverage.link(j, r, t, PRODUCERS)
        self.assertEqual(result["missing_or_unexamined_for_exported_jobs"], 1)
        self.assertEqual(result["review_queue"][0]["local_log_state"],
                         "LOCAL_LOG_UNEXAMINED_SIZE_OR_FORMAT")

    def test_duplicate_job_or_run_metadata_rejected(self):
        for js, rs in (([job(), job()], [run()]), ([job()], [run(), run()])):
            with self.subTest(jobs=len(js), runs=len(rs)):
                with self.assertRaises(ValueError):
                    coverage.link(js, rs, triage(), PRODUCERS)

    def test_reject_bad_job_ids_run_attempts_and_run_hashes(self):
        for changed in (job(ident=True), job(attempt=False),
                        job(rid=-4), job(sha="UNVERIFIED")):
            with self.subTest(changed=changed):
                with self.assertRaises(ValueError):
                    coverage.link([changed], [run()], triage(), PRODUCERS)
        with self.assertRaises(ValueError):
            coverage.link([job()], [run(sha="TAMPER")], triage(), PRODUCERS)

    def test_reject_false_approved_triage_and_digest_drift(self):
        _, _, t = self.fixture()
        for key, val in (
            ("historical_exposure_status", "NO_EXPOSURE"),
            ("log_access_exposure_verified", True),
            ("independent_security_review_signed", True),
        ):
            with self.subTest(key=key):
                changed = deepcopy(t)
                changed[key] = val
                self.write(self.triage, json.dumps(changed))
                with self.assertRaises(ValueError):
                    coverage.read_triage(self.triage)
        changed = deepcopy(t)
        changed["logs"][0]["log_sha256"] = "invalid"
        self.write(self.triage, json.dumps(changed))
        with self.assertRaises(ValueError):
            coverage.read_triage(self.triage)

    def test_triage_counts_duplicate_id_and_missing_digest_rejected(self):
        _, _, t = self.fixture()
        for changed in (
            {**t, "job_logs_content_examined": 99},
            {**t, "logs": [triage_row(), triage_row()] ,
             "job_log_files_present": 2, "job_logs_content_examined": 2},
            triage([triage_row(digest=None)]),
        ):
            with self.subTest(changed=changed):
                self.write(self.triage, json.dumps(changed))
                with self.assertRaises(ValueError):
                    coverage.read_triage(self.triage)

    def test_private_file_permissions_and_symlink_rejected(self):
        self.fixture()
        coverage.ensure_private_input(self.jobs)
        self.jobs.chmod(0o644)
        with self.assertRaises(ValueError):
            coverage.ensure_private_input(self.jobs)
        self.jobs.chmod(0o600)
        self.owner.chmod(0o755)
        with self.assertRaises(ValueError):
            coverage.ensure_private_input(self.jobs)
        self.owner.chmod(0o700)
        alias = self.owner / "alias.ndjson"
        alias.symlink_to(self.jobs)
        with self.assertRaises(ValueError):
            coverage.ensure_private_input(alias)

    def test_end_to_end_cli_private_report_and_redacted_stdout(self):
        self.fixture()
        original = coverage.POLICY
        policy = self.owner / "policy.json"
        self.write(policy, json.dumps({"workflow_paths": {n: ["a.json"] for n in PRODUCERS}}))
        coverage.POLICY = policy
        self.addCleanup(setattr, coverage, "POLICY", original)
        with redirect_stdout(io.StringIO()) as output:
            rc = coverage.main(["--jobs", str(self.jobs), "--runs", str(self.runs),
                                "--triage-report", str(self.triage), "--report", str(self.out)])
        self.assertEqual(rc, 0, output.getvalue())
        self.assertEqual(stat.S_IMODE(self.out.stat().st_mode), 0o600)
        public = json.loads(output.getvalue())
        self.assertNotIn("101", output.getvalue())
        self.assertNotIn("201", output.getvalue())
        self.assertNotIn(SHA, output.getvalue())
        self.assertEqual(public["historical_exposure_status"], "UNKNOWN")
        restricted = json.loads(self.out.read_text(encoding="utf-8"))
        self.assertEqual(restricted["review_queue"][0]["job_id"], 101)
        self.assertFalse(restricted["log_access_exposure_verified"])
        with redirect_stdout(io.StringIO()) as other:
            self.assertEqual(coverage.main(
                ["--jobs", str(self.jobs), "--runs", str(self.runs),
                 "--triage-report", str(self.triage), "--report", str(self.out)]), 2)
        self.assertEqual(json.loads(other.getvalue())["release_decision"], "NO_GO")

    def test_invalid_job_row_cli_refuses_and_does_not_create_report(self):
        self.fixture(jobs=[job(sha="BAD")])
        with redirect_stdout(io.StringIO()) as output:
            rc = coverage.main(["--jobs", str(self.jobs), "--runs", str(self.runs),
                                "--triage-report", str(self.triage), "--report", str(self.out)])
        self.assertEqual(rc, 2)
        self.assertEqual(json.loads(output.getvalue())["status"], "JOB_LOG_COVERAGE_BLOCKED")
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
