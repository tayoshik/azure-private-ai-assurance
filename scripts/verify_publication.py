#!/usr/bin/env python3
"""Offline publication integrity audit. Does NOT verify Azure infrastructure."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("specs/english_tests_001_440.json", 1, 20, 440),
    ("specs/phase3_264_en.json", 21, 32, 264),
    ("specs/phase4_286_en.json", 33, 45, 286),
    ("specs/phase5_286_en.json", 46, 58, 286),
    ("specs/phase6_220_en.json", 59, 68, 220),
    ("specs/phase7_220_en.json", 69, 78, 220),
]
DOCS = [f"docs/phase{i}-{c}-english-tests.md" for i,c in enumerate((220,220,264,286,286,220,220),1)]
ID = re.compile(r"^AZ-T([0-9]{2})-([0-9]{2})$")

def check(root=ROOT):
    root = Path(root)
    errors, identifiers = [], []
    phases = []
    for rel, low, high, count in SOURCES:
        path = root / rel
        try:
            source = json.loads(path.read_text(encoding="utf-8"))
            tests = source.get("tests", source.get("cases"))
            if not isinstance(tests,list):
                raise ValueError("tests/cases must be an array")
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{rel}: unreadable catalogue: {exc}")
            continue
        if len(tests) != count:
            errors.append(f"{rel}: {len(tests)} != {count}")
        phases.append(len(tests))
        for item in tests:
            tid=item.get("id","")
            match=ID.fullmatch(tid) if isinstance(tid,str) else None
            if not match:
                errors.append(f"{rel}: malformed ID {tid!r}")
                continue
            step,slot = map(int,match.groups())
            if step < low or step > high or not(1<=slot<=22) or item.get("step") != step:
                errors.append(f"{rel}: wrong step/slot for {tid}")
            if not isinstance(item.get("command"),str) or not item["command"].strip():
                errors.append(f"{rel}: missing command {tid}")
            if item.get("azure_live_pass") is True or item.get("azure_live_passes",0) not in (None,0):
                errors.append(f"{rel}: unjustified live PASS {tid}")
            identifiers.append(tid)
    expected={f"AZ-T{s:02d}-{i:02d}" for s in range(1,79) for i in range(1,23)}
    found=set(identifiers)
    duplicates=[tid for tid,n in Counter(identifiers).items() if n>1]
    if duplicates: errors.append(f"duplicate IDs: {duplicates[:10]}")
    if missing:=sorted(expected-found): errors.append(f"missing IDs: {missing[:10]}")
    if extra:=sorted(found-expected): errors.append(f"unexpected IDs: {extra[:10]}")
    if len(identifiers)!=1716: errors.append(f"total count: {len(identifiers)} != 1716")
    if sum(int(i.rsplit("-",1)[1])%2==0 for i in identifiers)!=858:
        errors.append("synthetic detection slot count inconsistent")
    for rel in DOCS + ["docs/78-step-construction-runbook.md","docs/final-accomplishment-report.md","docs/maintainer-handoff.md"]:
        if not(root/rel).is_file(): errors.append(f"missing document: {rel}")
    return {"status":"FAIL" if errors else "PASS_OFFLINE_PUBLICATION_ONLY",
            "catalogues": phases, "test_ids":len(identifiers),
            "unique_ids":len(found), "azure_live_passes":0,
            "release_decision":"NO_GO", "errors":errors}

if __name__=="__main__":
    report=check()
    print(json.dumps(report,indent=2,ensure_ascii=False))
    raise SystemExit(bool(report["errors"]))
