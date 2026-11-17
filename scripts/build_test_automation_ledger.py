"""Recompute the literal catalogue references and the implemented Step 26, Step 30 and Step 31 overlays."""
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
    missing_replacements = 0
    no_direct_mapped = 0
    step26_missing_replacements = 0
    step26_arm_routes = 0
    step26_extract_routes = 0
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
            overlay = {}
            if case["step"] == 30:
                number = int(case_id.rsplit("-", 1)[1])
                if number == 17:
                    implementation = "MANUAL_REVIEW_REQUIRED"
                    command = "--review-ownership"
                elif number % 2 == 0:
                    implementation = "OFFLINE_CHECK"
                    command = "--selftest"
                    missing_replacements += bool(missing)
                else:
                    implementation = "AZURE_ARM_CONFIGURATION" if number <= 13 else "PRIVATE_RUNNER_DNS"
                    command = "--live"
                    no_direct_mapped += status == "no_direct_script_reference"
                overlay = {"entry_point": "scripts/azure_private_dns_step30.py " + command,
                           "mapping": "docs/azure-private-dns-step30.md"}
            if case["step"] == 26:
                number = int(case_id.rsplit("-", 1)[1])
                if number % 2 == 0:
                    implementation = "OFFLINE_CHECK"
                    entry_point = "tests/test_azure_private_endpoint_step26.py --evidence"
                    step26_missing_replacements += bool(missing)
                elif number == 21:
                    implementation = "MANUAL_REVIEW_REQUIRED"
                    entry_point = "scripts/azure_private_endpoint_step26.py --check-config"
                elif number == 19:
                    implementation = "FLOW_EVIDENCE_REVIEW"
                    entry_point = "scripts/azure_private_endpoint_step26.py --review-flow"
                    step26_extract_routes += status == "no_direct_script_reference"
                else:
                    implementation = "CONFIG_AND_SINGLE_TCP_OBSERVER" if number in (11, 13) else "AZURE_ARM_CONFIGURATION"
                    entry_point = "scripts/azure_private_endpoint_step26.py --live" + (
                        "; separate --probe" if number in (11, 13) else "")
                    step26_arm_routes += status == "no_direct_script_reference"
                overlay = {"entry_point": entry_point, "mapping": "docs/azure-private-endpoint-step26.md",
                           "original_requirement_complete": False}
            rows[case_id] = {"catalogue": source, "action_reference": status, "missing": missing,
                             "implementation": implementation, "azure_acceptance": "NOT_READY", **overlay}
    expected = {f"AZ-T{step:02}-{number:02}" for step in range(1, 79) for number in range(1, 23)}
    if set(rows) != expected:
        raise ValueError("Catalogue ID coverage differs from the approved range")
    summary = {
        "baseline_commit": "ed2168fe492261e373f563829c9268b7ac727681",
        "baseline_literal_references": BASELINE,
        "current_literal_references": {key: counts[key] for key in (*BASELINE, "tracked_script_reference")},
        "implementation_counts": dict(sorted(Counter(r["implementation"] for r in rows.values()).items())),
        "step30_resolution": {
            "missing_literal_references_with_step30_offline_replacement": missing_replacements,
            "missing_literal_references_without_step30_replacement": counts["missing_script_reference"] - missing_replacements,
            "no_direct_reference_with_step30_live_mapping": no_direct_mapped,
            "no_direct_reference_without_step30_live_mapping": counts["no_direct_script_reference"] - no_direct_mapped,
        },
        "step26_resolution": {
            "new_offline_replacements_of_missing_literal_references": step26_missing_replacements,
            "missing_literal_references_without_step26_or_step30_replacement":
                counts["missing_script_reference"] - missing_replacements - step26_missing_replacements,
            "new_arm_routes_for_cases_without_direct_reference": step26_arm_routes,
            "new_flow_extract_route_for_case_without_direct_reference": step26_extract_routes,
            "no_direct_reference_without_step26_or_step30_arm_or_live_route":
                counts["no_direct_script_reference"] - no_direct_mapped - step26_arm_routes,
            "no_direct_reference_without_step26_or_step30_executable_route":
                counts["no_direct_script_reference"] - no_direct_mapped - step26_arm_routes - step26_extract_routes,
            "step26_original_requirements_completed_in_runtime": 0,
        },
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
