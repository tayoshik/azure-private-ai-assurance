import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rest01_catalogue",ROOT/"scripts/rest01_catalogue.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

class CatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.index=r.build_index(ROOT)
    def test_total_unique_1716(self):
        self.assertEqual(len(self.index["cases"]),1716)
        self.assertEqual(len({x["id"] for x in self.index["cases"]}),1716)
    def test_all_78_steps_22_each(self):
        for step in range(1,79):
            self.assertEqual(sum(x["step"]==step for x in self.index["cases"]),22)
    def test_no_claimed_live_rest_pass(self):
        self.assertEqual(self.index["azure_live_passes"],0)
        self.assertTrue(all(x["implementation_state"]=="NOT_IMPLEMENTED_FOR_LIVE" for x in self.index["cases"]))
    def test_real_arm_cli_is_candidate_not_implemented(self):
        x=next(x for x in self.index["cases"] if x["id"]=="AZ-T33-01")
        self.assertEqual(x["route"],"REST_CANDIDATE")
    def test_playwright_never_claimed_rest(self):
        x=next(x for x in self.index["cases"] if x["id"]=="AZ-T64-01")
        self.assertEqual(x["route"],"PLAYWRIGHT_TOOL")
    def test_synthetic_never_claimed_rest(self):
        x=next(x for x in self.index["cases"] if x["id"]=="AZ-T20-22")
        self.assertEqual(x["route"],"OFFLINE_SYNTHETIC")
    def test_reject_mutating_az_cli(self):
        self.assertEqual(r.route_case({"command":"az network vnet delete -g x -n y"})[0],"REVIEW_REQUIRED")
    def test_detect_duplicate_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            for f, *_ in r.SOURCES:
                target=Path(tmp)/f;target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/f,target)
            file=Path(tmp)/r.SOURCES[0][0]; data=json.loads(file.read_text());cases=data.get('tests',data.get('cases'))
            cases[1]['id']=cases[0]['id'];file.write_text(json.dumps(data))
            with self.assertRaises(ValueError):r.build_index(tmp)
    def test_unknown_command_review(self):
        self.assertEqual(r.route_case({"command":"az role assignment create --role Owner"})[0],"REVIEW_REQUIRED")

if __name__=="__main__":unittest.main()
