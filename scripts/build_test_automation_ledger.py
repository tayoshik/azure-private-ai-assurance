"""Recompute the literal catalogue references and the implemented Step 31 overlay."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CATALOGUES = ("english_tests_001_440", "phase3_264_en", "phase4_286_en",
              "phase5_286_en", "phase6_220_en", "phase7_220_en")
SCRIPT_REF = re.compile(r"(?<![\w/.-])(?:scripts|tests)/[\w./-]+\.(?:py|sh|ts|js|mjs|ps1)\b")
RUNTIME = {3, 5, 9, 11, 13, 15}
OPTIONAL_CONFIG = {7, 17, 21}
BASELINE = {"missing_script_reference": 999, "no_direct_script_reference": 717}


def ledger():
    rows = {}
    counts = Counter()
    for name in CATALOGUES:
        source = f"specs/{name}.json"
        content = json.loads((ROOT / source).read_text(encoding="utf-8"))
        for case in content.get("tests", content.get("cases", [])):
            case_id = case["id"]
            if case_id in rows:
                raise ValueError(f"Duplicate ID: {case_id}")
            refs = set(SCRIPT_REF.findall(case["command"]))
            missing = sorted(ref for ref in refs if not (ROOT / ref).is_file())
            status = "missing_script_reference" if missing else "tracked_script_reference" if refs else "no_direct_script_reference"
            counts[status] += 1
            implementation = "NOT_REVIEWED_IN_THIS_OVERLAY"
            if case["step"] == 31:
                number = int(case_id.rsplit("-", 1)[1])
                implementation = ("OFFLINE_CHECK" if number % 2 == 0 else
                                  "RUNTIME_OBSERVER" if number in RUNTIME else
                                  "OPTIONAL_ARM_CONFIGURATION_ONLY" if number in OPTIONAL_CONFIG else
                                  "MANUAL_REVIEW_REQUIRED")
            rows[case_id] = {"catalogue": source, "action_reference": status, "missing": missing,
                             "implementation": implementation, "azure_acceptance": "NOT_READY"}
    expected = {f"AZ-T{step:02}-{number:02}" for step in range(1, 79) for number in range(1, 23)}
    if set(rows) != expected:
        raise ValueError("Catalogue ID coverage differs from the approved range")
    summary = {
        "baseline_commit": "ed2168fe492261e373f563829c9268b7ac727681",
        "baseline_literal_references": BASELINE,
        "current_literal_references": {key: counts[key] for key in (*BASELINE, "tracked_script_reference")},
        "implementation_counts": dict(sorted(Counter(r["implementation"] for r in rows.values()).items())),
        "azure_accepted": 0,
        "release_decision": "NO_GO",
    }
    # One stable line per case keeps diff review and machine consumption straightforward.
    return ("{\n  \"summary\": " + json.dumps(summary, sort_keys=True) + ",\n  \"cases\": {\n"
            + ",\n".join(f"    {json.dumps(k)}: {json.dumps(v, sort_keys=True)}" for k, v in sorted(rows.items()))
            + "\n  }\n}\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = ROOT / "specs/test-automation-ledger.json"
    output = ledger().encode("utf-8")
    if args.check:
        if path.read_bytes() != output:
            parser.exit(2, "Automation ledger is stale. Recompute and review it.\n")
        print("Automation ledger verified: 1,716 IDs.")
    else:
        path.write_bytes(output)


if __name__ == "__main__":
    main()
