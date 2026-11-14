#!/usr/bin/env python3
"""REST01: source-preserving routing index for all 1,716 documented tests.

This script DOES NOT execute the documented commands or promise that an Azure
CLI expression can automatically be translated to a REST endpoint.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    ("specs/english_tests_001_440.json", 1, 20, 440),
    ("specs/phase3_264_en.json", 21, 32, 264),
    ("specs/phase4_286_en.json", 33, 45, 286),
    ("specs/phase5_286_en.json", 46, 58, 286),
    ("specs/phase6_220_en.json", 59, 68, 220),
    ("specs/phase7_220_en.json", 69, 78, 220),
)
ID_RE = re.compile(r"^AZ-T(\d\d)-(\d\d)$")
SAFE_CLI_VERBS = frozenset({"show", "list", "get"})


def route_case(case: dict) -> tuple[str, str, str]:
    """Return proposed execution route, api family, and conservative reason."""
    command = str(case.get("command", "")).strip()
    cls = str(case.get("execution_class", "")).upper()
    polarity = str(case.get("polarity", "")).upper()
    variant = str(case.get("variant", "")).upper()
    synthetic = ("SYNTHETIC" in cls or "OFFLINE_DETECTOR" in cls
                 or "SYNTHETIC" in polarity or "DEVIATION_DETECTION" in variant
                 or "--selftest" in command)
    if synthetic:
        return "OFFLINE_SYNTHETIC", "NONE", "Synthetic detector; no Azure evidence"
    if re.match(r"^az\s+", command):
        tokens = command.split()
        if "rest" in tokens[1:3]:
            return "REVIEW_REQUIRED", "ARM_OR_DATA", "Raw az rest may mutate; method must be reviewed"
        if "graph" in tokens[1:3] and "query" in tokens[2:5]:
            return "REST_CANDIDATE", "RESOURCE_GRAPH", "Proposed REST translation; not implemented"
        if "monitor" in tokens[1:3] and "query" in tokens:
            return "REST_CANDIDATE", "MONITOR_LOGS", "Requires separate log query API design"
        if len(tokens) > 2 and tokens[-1] not in SAFE_CLI_VERBS:
            # Search for the first verb in a command whose arguments can follow it.
            action = next((t for t in tokens[2:] if t in SAFE_CLI_VERBS), None)
        else:
            action = tokens[-1] if tokens else None
        if action in SAFE_CLI_VERBS:
            return "REST_CANDIDATE", "ARM_MANAGEMENT", "Read-only CLI source; ARM endpoint/version not yet verified"
        return "REVIEW_REQUIRED", "UNKNOWN", "CLI subcommand not confirmed read-only"
    if command.startswith("terraform "):
        return "TERRAFORM_TOOL", "NONE", "Use pinned Terraform CLI/approval gates"
    if command.startswith("npx ") or "playwright" in command.lower():
        return "PLAYWRIGHT_TOOL", "NONE", "Use approved browser/internal runner"
    if command.startswith(("dig ", "getent ", "curl ", "openssl ")):
        return "NETWORK_TOOL", "NONE", "Require correct network vantage point"
    return "LOCAL_EVIDENCE_OR_REVIEW", "NONE", "Local file/tool or human evidence review"


def build_index(root: Path = ROOT) -> dict:
    root = Path(root)
    rows = []
    provenance = []
    seen = set()
    for filename, low, high, expected in SOURCES:
        raw = (root / filename).read_bytes()
        catalog = json.loads(raw)
        cases = catalog.get("tests", catalog.get("cases"))
        if not isinstance(cases, list) or len(cases) != expected:
            raise ValueError(f"{filename}: expected {expected} tests")
        provenance.append({"path": filename, "sha256": hashlib.sha256(raw).hexdigest(), "cases": expected})
        for entry in cases:
            if not isinstance(entry, dict):
                raise ValueError(f"{filename}: invalid case")
            case_id = entry.get("id")
            m = ID_RE.fullmatch(str(case_id))
            if not m or case_id in seen:
                raise ValueError(f"{filename}: malformed or duplicate test ID: {case_id}")
            seen.add(case_id)
            step, ordinal = int(m[1]), int(m[2])
            if not (low <= step <= high and 1 <= ordinal <= 22 and entry.get("step") == step):
                raise ValueError(f"{filename}: step/ordinal mismatch for {case_id}")
            route, family, reason = route_case(entry)
            rows.append({"id": case_id, "step": step, "source": filename,
                         "execution_class": entry.get("execution_class", "UNKNOWN"),
                         "route": route, "api_family_candidate": family,
                         "reason": reason, "implementation_state": "NOT_IMPLEMENTED_FOR_LIVE",
                         "azure_live_acceptance": "NOT_READY",
                         "original_command": entry.get("command", "")})
    expected_ids = {f"AZ-T{s:02d}-{n:02d}" for s in range(1, 79) for n in range(1, 23)}
    if seen != expected_ids:
        raise ValueError(f"incomplete 1716 catalogue: missing={len(expected_ids-seen)} extra={len(seen-expected_ids)}")
    counts = dict(sorted(collections.Counter(row["route"] for row in rows).items()))
    rows.sort(key=lambda x: (x["step"], x["id"]))
    return {"schema": "azure-private-ai-assurance/rest01-routing/v1",
            "status": "ROUTING_CANDIDATES_ONLY", "azure_live_passes": 0,
            "release_decision": "NO_GO", "case_count": len(rows),
            "route_counts": counts, "source_catalogues": provenance, "cases": rows}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--output", type=Path, default=None)
    p.add_argument("--test-id", default=None)
    p.add_argument("--summary", action="store_true")
    args = p.parse_args()
    result = build_index(args.root)
    if args.test_id:
        selection = [c for c in result["cases"] if c["id"] == args.test_id]
        if not selection:
            print(json.dumps({"status": "NOT_FOUND", "id": args.test_id})); return 2
        rendered = selection[0]
    elif args.summary:
        rendered = {k: v for k, v in result.items() if k != "cases"}
    else:
        rendered = result
    output = json.dumps(rendered, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
