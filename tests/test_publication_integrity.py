import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_publication import check, SOURCES

class TestPublication(unittest.TestCase):
    def test_baseline_counts(self):
        result=check()
        self.assertEqual(result["status"],"PASS_OFFLINE_PUBLICATION_ONLY",result["errors"])
        self.assertEqual(result["test_ids"],1716)
        self.assertEqual(result["unique_ids"],1716)
        self.assertEqual(result["azure_live_passes"],0)
        self.assertEqual(result["release_decision"],"NO_GO")
    def test_expected_phase_span(self):
        self.assertEqual(sum(x[3] for x in SOURCES),1716)
        self.assertEqual([(x[1],x[2]) for x in SOURCES],[(1,20),(21,32),(33,45),(46,58),(59,68),(69,78)])

if __name__=="__main__":
    unittest.main()
