"""Verify frozen Phase5 source integrity and offline-only guard semantics."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import phase5_guard as p

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "specs/phase5_286.json"
ENGLISH = ROOT / "specs/phase5_286_en.json"


class Phase5RestorationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c, cls.cases = p.load_original()
        cls.en = p.published_translation()

    def test_primary_source_sha256_and_all_ids(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),p.SOURCE_SHA256)
        self.assertEqual(len(self.c),143)
        self.assertEqual(len(self.cases),286)
        self.assertEqual(set(self.cases),p.EXPECTED)
        self.assertEqual(self.en["provenance"]["original_phase5_spec_sha256"],p.SOURCE_SHA256)
        self.assertEqual(self.en["azure_live_passes"],0)

    def test_286_synthetic_original_cases_and_no_azure_pass(self):
        o,code=p.synthetic_check(self.c,"ALL")
        self.assertEqual(code,0,o)
        self.assertEqual(o["case_labels_tested"],286)
        self.assertEqual(o["synthetic_checks_succeeded"],286)
        self.assertEqual(o["azure_live_passes"],0)
        self.assertEqual(o["release_decision"],"NO_GO")

    def test_english_command_line_mode_points_back_to_frozen_original(self):
        proc = subprocess.run([sys.executable,str(ROOT/"scripts/phase5_guard.py"),
              "--selftest","AZ-T46-02","--spec","specs/phase5_286_en.json"],
              cwd=ROOT,text=True,capture_output=True,check=False)
        self.assertEqual(proc.returncode,0,proc.stderr)
        o=json.loads(proc.stdout)
        self.assertEqual(o["synthetic_checks_succeeded"],1)
        self.assertEqual(o["azure_live_passes"],0)

    def test_type_safety_and_missing_value(self):
        self.assertEqual(p.predicate("eq",{"expected":True},1),"MISMATCH")
        self.assertEqual(p.predicate("eq",{"expected":{"x":True}},{"x":1}),"MISMATCH")
        self.assertEqual(p.predicate("eq",{"expected":float("nan")},float("nan")),"MISMATCH")
        self.assertEqual(p.predicate("minimum",{"expected":1},True),"NOT_READY")
        self.assertEqual(p.predicate("maximum",{"expected":3},float("inf")),"NOT_READY")
        self.assertEqual(p.predicate("nonempty",{},[]),"MISMATCH")
        self.assertEqual(p.predicate("private_ip",{"subnet":"10.0.0.0/24"},"10.0.0.2"),"MATCH")
        self.assertEqual(p.predicate("private_ip",{"subnet":"10.0.0.0/24"},"8.8.8.8"),"MISMATCH")
        self.assertEqual(p.predicate("private_ip",{"subnet":"10.0.0.0/24"},"not_ip"),"NOT_READY")
        self.assertEqual(p.predicate("is_true",{},True),"MATCH")
        self.assertEqual(p.predicate("is_false",{},False),"MATCH")
        self.assertEqual(p.predicate("is_true",{},None),"NOT_READY")

    def test_undefined_and_negative_ids_never_get_approval(self):
        for cid in ("AZ-T99-01","AZ-T46-00","AZ-T59-01"):
            output,status=p.synthetic_check(self.c,cid)
            self.assertEqual(status,2)
            self.assertEqual(output["result"],"NOT_READY")
        output,status=p.review_observation(self.c,"AZ-T46-02",None)
        self.assertEqual(status,2)
        self.assertEqual(output["result"],"NOT_READY")

    def test_unsigned_matching_observation_requires_review_exit_2(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"observation.json"
            data=dict(source="untrusted-local-file",resource_id="/subscriptions/example",
                      collected_at_utc="2026-11-19T00:00:00Z",baseline_id="unsigned",
                      reviewer="local-operator",fixture=False,observation=True)
            path.write_text(json.dumps(data),encoding="utf-8")
            output,status=p.review_observation(self.c,"AZ-T46-01",path)
            self.assertEqual(status,2)
            self.assertEqual(output["result"],"REVIEW_REQUIRED")
            self.assertNotIn("PASS",output["result"])
            data["observation"]=False
            path.write_text(json.dumps(data))
            output,status=p.review_observation(self.c,"AZ-T46-01",path)
            self.assertEqual(status,2)
            self.assertEqual(output["result"],"DIFFERENCE_REVIEW_REQUIRED")
            data["synthetic"]=True
            path.write_text(json.dumps(data))
            output,status=p.review_observation(self.c,"AZ-T46-01",path)
            self.assertEqual(status,2)
            self.assertEqual(output["result"],"NOT_READY")

    def test_missing_or_changed_original_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            pth=Path(d)/"untrusted.json"
            pth.write_text(json.dumps({"schema":"azure-phase5-286/v1"}))
            with self.assertRaises(ValueError):
                p.load_original(pth)
            run=subprocess.run([sys.executable,str(ROOT/"scripts/phase5_guard.py"),
                 "--selftest","ALL","--spec",str(pth)],
                 text=True,capture_output=True,check=False)
            self.assertEqual(run.returncode,2)
            self.assertEqual(json.loads(run.stdout)["result"],"NOT_READY")

    def test_canonical_catalogue_requires_real_script_not_exit_zero_claim(self):
        src=json.loads(SOURCE.read_text(encoding="utf-8"))
        published=self.en
        self.assertEqual(len(published["tests"]),286)
        self.assertEqual({x["id"] for x in published["tests"]},p.EXPECTED)
        self.assertEqual(src["live_azure_tests_passed"],0)
        self.assertEqual(sum(x["control_id"] in p.CONTROL_IDS for x in src["controls"]),143)


if __name__ == "__main__":
    unittest.main()
