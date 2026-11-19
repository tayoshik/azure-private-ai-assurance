"""Regress static-check risk ranking and five fail-closed semantic comparisons."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import triage_static_criteria as t
from scripts import review_high_risk_static as h

ROOT = Path(__file__).resolve().parents[1]


class ReviewPriorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = t.triage(ROOT)

    def test_all_160_original_static_source_flags_and_1716_cases(self):
        d = self.data
        self.assertEqual(d["errors"], [])
        self.assertEqual(d["catalogue_test_ids"], 1716)
        self.assertEqual(d["static_review_candidates"], 160)
        self.assertEqual(len(d["cases"]), 160)
        self.assertEqual(len({x["id"] for x in d["cases"]}), 160)

    def test_top_five_are_real_source_cases_not_imaginary_new_claims(self):
        d = self.data
        self.assertEqual(set(d["first_five_critical_ids"]), set(t.FIRST_FIVE))
        self.assertEqual([x["id"] for x in d["cases"][:5]], list(t.FIRST_FIVE))
        self.assertTrue(all(x["priority"] == "P0" for x in d["cases"][:5]))
        self.assertTrue(all(x["published_command"] and
                            x["published_acceptance_criterion"] for x in d["cases"]))

    def test_nobody_receives_live_acceptance_or_signed_approval(self):
        d = self.data
        self.assertEqual(d["live_azure_acceptances"], 0)
        self.assertEqual(d["release_decision"], "NO_GO")
        self.assertEqual(sum(d["priority_counts"].values()), 160)
        for row in d["cases"]:
            self.assertFalse(row["criterion_verified"])
            self.assertFalse(row["independent_approval_verified"])
            self.assertEqual(row["azure_acceptance"], "NOT_READY")

    def test_missing_root_fails_inventory_and_does_not_create_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = t.triage(Path(tmp))
        self.assertTrue(d["errors"])
        self.assertEqual(d["live_azure_acceptances"], 0)
        self.assertEqual(d["release_decision"], "NO_GO")

    def test_ranker_cli_strict_always_denies_and_writes_deterministic_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/"ranked.json"
            cmd = [sys.executable, str(ROOT/"scripts/triage_static_criteria.py"),
                   "--out", str(output), "--strict"]
            run = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(run.returncode, 2, run.stderr)
            d = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(d["static_review_candidates"],160)
            self.assertEqual([x["id"] for x in d["cases"][:5]],list(t.FIRST_FIVE))


class FiveSemanticTrapsTests(unittest.TestCase):
    def test_tls_grep_does_not_accidentally_accept_ignore_https_errors_true(self):
        approved = {"approved_tls_hostname":"web.internal.example"}
        bad={"playwright_config_text": "use: { ignoreHTTPSErrors: true }"}
        good={"playwright_config_text": "use: { ignoreHTTPSErrors: false }"}
        self.assertEqual(h.predicate("AZ-T20-13",bad,approved)[0],"DIFFERENCE_REVIEW_REQUIRED")
        self.assertEqual(h.predicate("AZ-T20-13",good,approved)[0],"REVIEW_REQUIRED")
        self.assertEqual(h.predicate("AZ-T20-13",{"playwright_config_text":"rejectUnauthorized:false"},approved)[0],
                         "DIFFERENCE_REVIEW_REQUIRED")
        self.assertEqual(h.predicate("AZ-T20-13",good,{})[0],"NOT_READY")

    def test_plan_hash_must_match_exact_approved_digest_of_file_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"unapproved-plan.bin"
            path.write_bytes(b"SYNTHETIC_PLAN_NEVER_AZURE")
            actual=hashlib.sha256(path.read_bytes()).hexdigest()
            observed={"plan_path":str(path)}
            self.assertEqual(h.predicate("AZ-T45-03",observed,{"plan_sha256":actual})[0],
                             "REVIEW_REQUIRED")
            self.assertEqual(h.predicate("AZ-T45-03",observed,{"plan_sha256":"0"*64})[0],
                             "DIFFERENCE_REVIEW_REQUIRED")
            self.assertEqual(h.predicate("AZ-T45-03",observed,{"plan_sha256":"invalid"})[0],
                             "NOT_READY")
            observed["plan_path"]=str(path)+"-absent"
            self.assertEqual(h.predicate("AZ-T45-03",observed,{"plan_sha256":actual})[0],
                             "NOT_READY")

    def test_two_reviewers_must_be_distinct_from_change_author_and_executor(self):
        obs={"change_author":"author","executor":"deployer","reviewers":[
             {"identity_id":"sec-reviewer","role":"security"},
             {"identity_id":"ops-reviewer","role":"operations"}]}
        approved={"approved_reviewer_identities":["sec-reviewer","ops-reviewer"]}
        self.assertEqual(h.predicate("AZ-T45-19",obs,approved)[0],"REVIEW_REQUIRED")
        obs["reviewers"][1]["identity_id"]="deployer"
        self.assertEqual(h.predicate("AZ-T45-19",obs,approved)[0],"DIFFERENCE_REVIEW_REQUIRED")
        obs["reviewers"][1]["identity_id"]="sec-reviewer"
        self.assertEqual(h.predicate("AZ-T45-19",obs,approved)[0],"DIFFERENCE_REVIEW_REQUIRED")
        obs["reviewers"][1]["identity_id"]="ops-reviewer"
        obs["reviewers"][1]["role"]="security"
        self.assertEqual(h.predicate("AZ-T45-19",obs,approved)[0],"DIFFERENCE_REVIEW_REQUIRED")

    def test_artifact_digest_and_source_commit_both_compared(self):
        approved={"artifact_sha256":"a"*64,"source_commit_sha":"b"*40}
        observed=dict(approved)
        self.assertEqual(h.predicate("AZ-T40-11",observed,approved)[0],"REVIEW_REQUIRED")
        observed["source_commit_sha"]="c"*40
        self.assertEqual(h.predicate("AZ-T40-11",observed,approved)[0],
                         "DIFFERENCE_REVIEW_REQUIRED")
        observed["artifact_sha256"]="broken"
        self.assertEqual(h.predicate("AZ-T40-11",observed,approved)[0],"NOT_READY")

    def test_apply_record_cannot_use_nonempty_but_mismatched_executor(self):
        approved={"plan_sha256":"a"*64,"source_commit_sha":"b"*40,
                  "executor":"approved-deployer","change_ticket":"CHG-EXAMPLE-TEST"}
        observed=dict(approved)
        self.assertEqual(h.predicate("AZ-T45-21",observed,approved)[0],"REVIEW_REQUIRED")
        observed["executor"]="unapproved-deployer"
        self.assertEqual(h.predicate("AZ-T45-21",observed,approved)[0],
                         "DIFFERENCE_REVIEW_REQUIRED")
        observed["executor"]=""
        self.assertEqual(h.predicate("AZ-T45-21",observed,approved)[0],"NOT_READY")

    def test_invalid_inputs_are_not_authoritatively_classified(self):
        for cid in ("AZ-T20-13","AZ-T45-03","AZ-T45-19","AZ-T40-11","AZ-T45-21","AZ-T99-01"):
            result=h.review(cid,None,None)
            self.assertEqual(result["result"],"NOT_READY")
            self.assertEqual(result["live_azure_passes"],0)
            self.assertFalse(result["independent_signer_or_approval_verified"])
            self.assertEqual(result["release_decision"],"NO_GO")

    def test_positive_looking_local_evidence_always_exits_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=Path(tmp)/"approved.json"
            o=Path(tmp)/"observed.json"
            payload={"artifact_sha256":"a"*64,"source_commit_sha":"b"*40}
            a.write_text(json.dumps(payload),encoding="utf-8")
            o.write_text(json.dumps(payload),encoding="utf-8")
            proc=subprocess.run([sys.executable,str(ROOT/"scripts/review_high_risk_static.py"),
               "--case-id","AZ-T40-11","--observation",str(o),"--approved",str(a)],
               cwd=ROOT,capture_output=True,text=True,check=False)
            self.assertEqual(proc.returncode,2)
            result=json.loads(proc.stdout)
            self.assertEqual(result["result"],"REVIEW_REQUIRED")
            self.assertEqual(result["live_azure_passes"],0)
            self.assertEqual(result["release_decision"],"NO_GO")


if __name__ == "__main__":
    unittest.main()
