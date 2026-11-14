import json,unittest,tempfile,shutil
from pathlib import Path
from scripts.validate_package import validate
ROOT=Path(__file__).resolve().parent.parent
class ProjectBaselineTests(unittest.TestCase):
    def test_package(self): self.assertEqual(validate(),[])
    def test_counts(self):
        x=json.loads((ROOT/"schemas/project-status.json").read_text())
        self.assertEqual((x["construction_steps"],x["cases_per_step"],x["test_cases"]),(78,22,1716))
    def test_live_not_pass(self):
        x=json.loads((ROOT/"schemas/project-status.json").read_text())
        self.assertEqual((x["azure_live_passes"],x["azure_acceptance_not_ready"],x["release_decision"]),(0,1716,"NO_GO"))
    def test_phase_counts(self):
        x=json.loads((ROOT/"schemas/test-allocation.json").read_text())
        self.assertEqual([p["test_cases"] for p in x["phases"]],[220,220,264,286,286,220,220])
    def test_reject_private_key(self):
        with tempfile.TemporaryDirectory() as d:
            shutil.copytree(ROOT,Path(d)/"r")
            (Path(d)/"r"/"bad.md").write_text("-----BEGIN "+"PRIVATE KEY-----")
            self.assertTrue(validate(Path(d)/"r"))
    def test_reject_github_token(self):
        with tempfile.TemporaryDirectory() as d:
            shutil.copytree(ROOT,Path(d)/"r")
            (Path(d)/"r"/"bad.md").write_text("ghp_"+"a"*40)
            self.assertTrue(validate(Path(d)/"r"))
if __name__=="__main__":unittest.main()
