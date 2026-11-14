#!/usr/bin/env python3
"""Offline consistency and basic secret-safety checks; does not connect to Azure."""
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parent.parent
REQUIRED=["README.md","SECURITY.md","CONTRIBUTING.md","docs/executive-report.md","docs/ten-turn-roadmap.md","docs/current-status.md","docs/architecture-baseline.md","docs/acceptance-criteria.md","docs/source-provenance.md","docs/github-publishing.md","schemas/project-status.json","schemas/test-allocation.json","schemas/source-inventory.json"]
def validate(root=ROOT):
    errors=[]
    for rel in REQUIRED:
        p=root/rel
        if not p.is_file() or p.stat().st_size==0: errors.append(f"missing or empty: {rel}")
    if errors:return errors
    try:
        s=json.loads((root/"schemas/project-status.json").read_text(encoding="utf8"))
        a=json.loads((root/"schemas/test-allocation.json").read_text(encoding="utf8"))
        i=json.loads((root/"schemas/source-inventory.json").read_text(encoding="utf8"))
    except (OSError,ValueError) as e:return [f"invalid metadata: {e}"]
    if s["construction_steps"]*s["cases_per_step"]!=1716 or s["test_cases"]!=1716:errors.append("case counts inconsistent")
    if s["positive_cases"]+s["deviation_detection_cases"]!=1716:errors.append("test polarization inconsistent")
    if s["azure_live_passes"]!=0 or s["azure_acceptance_not_ready"]!=1716 or s["release_decision"]!="NO_GO":errors.append("live result falsely upgraded")
    covered=[];total=0
    for p in a["phases"]:
        ids=list(range(p["step_start"],p["step_end"]+1))
        covered+=ids;total+=p["test_cases"]
        if len(ids)*22!=p["test_cases"]:errors.append("phase allocation invalid")
    if covered!=list(range(1,79)) or total!=1716:errors.append("78-step mapping invalid")
    for key,item in i["files"].items():
        if not re.fullmatch(r"[a-f0-9]{64}",item.get("sha256","")):errors.append(f"invalid inventory digest for {key}")
    if list(root.rglob("*.tfstate")) or list(root.rglob("*.pfx")):errors.append("forbidden sensitive file")
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in (".md",".json",".py",".yml"):continue
        try:t=p.read_text(encoding="utf8")
        except UnicodeDecodeError:errors.append("nonutf8 file "+str(p));continue
        if re.search(r"gh[pousr]_[A-Za-z0-9]{25,}",t):errors.append("suspected GitHub token")
        if "-----BEGIN "+"PRIVATE KEY-----" in t:errors.append("private key contents")
    return errors
if __name__=="__main__":
    e=validate()
    if e:
        print("NOT_READY",e);sys.exit(1)
    print("PASS: metadata, 78 steps / 1716 IDs, baseline no-live claims and local security checks")
    print("This is not an Azure live control check.")
