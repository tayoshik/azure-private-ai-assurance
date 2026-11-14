#!/usr/bin/env python3
"""Offline catalogue consistency checks. Does not authenticate to Azure."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs/english_tests_001_440.json"
DOCS = (
    ROOT / "docs/phase1-220-english-tests.md",
    ROOT / "docs/phase2-220-english-tests.md",
)

def main():
    catalogue = json.loads(SPEC.read_text(encoding="utf-8"))
    cases = catalogue.get("cases", [])
    expected = [f"AZ-T{s:02d}-{n:02d}" for s in range(1, 21) for n in range(1, 23)]
    ids = [row.get("id") for row in cases]
    errors = []
    if ids != expected:
        errors.append("Incorrect ID order, ID count, or missing cases")
    if catalogue.get("azure_live_pass_count") != 0 or catalogue.get("not_ready") != 440:
        errors.append("Unsupported Azure live test claims")
    for doc, subset in zip(DOCS, [expected[:220], expected[220:]]):
        text = doc.read_text(encoding="utf-8")
        found = re.findall(r"(?m)^### (AZ-T\d{2}-\d{2}) — ", text)
        if found != subset:
            errors.append(f"Incorrect case headings in {doc.name}")
    for row in cases:
        if row.get("acceptance_status") != "NOT_READY" or row.get("azure_live_pass") is not False:
            errors.append(f"Invalid live acceptance claim for {row.get('id')}")
        for field in ("command", "preconditions", "expected", "evidence", "failure_response"):
            if not row.get(field):
                errors.append(f"Missing {field} for {row.get('id')}")
        if re.search(r"\b(?:terraform apply|az login)\b", row.get("command", "")):
            errors.append(f"Prohibited active command in {row.get('id')}")
    positives = sum(row.get("execution_class") != "OFFLINE_DETECTOR" for row in cases)
    negatives = len(cases) - positives
    if (positives, negatives) != (220, 220):
        errors.append("Incorrect positive / synthetic-negative split")
    if errors:
        print("NOT_READY:", "\n".join(errors[:20]))
        return 1
    print("PASS: 440 stable test IDs, English docs and JSON agree.")
    print("220 positive design/read-only cases; 220 synthetic detector cases.")
    print("Azure live passes: 0. This test never contacted Azure.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
