#!/usr/bin/env python3
"""Conservative Phase 6 observation classifier; never emits live Azure PASS.

Legacy --expected values in published commands are display-only assertions, not
a release gate. Missing/synthetic/unverified evidence cannot exit successfully.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

INCONCLUSIVE = {"nxdomain", "http_403", "timeout", "connection_refused", "tls_error"}
DEVIATIONS = {"unexpected_public_ip", "unauthorized_http_200"}


def classify(record, *, synthetic_testing=False):
    if not isinstance(record, dict):
        return "NOT_READY"
    if (record.get("asset_exists") is not True
            or record.get("baseline_approved") is not True
            or record.get("evidence_present") is not True):
        return "NOT_READY"
    if not synthetic_testing and (
            record.get("synthetic") is True
            or record.get("fixture") is True
            or record.get("source") == "SYNTHETIC"):
        return "NOT_READY"
    observation = record.get("observation")
    if not isinstance(observation, str):
        return "NOT_READY"
    mode = record.get("mode", "external_negative")
    if observation in DEVIATIONS:
        return "DIFFERENCE_REVIEW_REQUIRED"
    if observation == "tls_error" and mode == "internal_positive":
        return "DIFFERENCE_REVIEW_REQUIRED"
    if observation == "denied_with_control_plane":
        if (record.get("control_plane_private_confirmed") is True
                and record.get("external_network_confirmed") is True
                and isinstance(record.get("resource_id"), str)
                and bool(record["resource_id"])
                and isinstance(record.get("collected_at_utc"), str)
                and bool(record["collected_at_utc"])):
            return "REVIEW_REQUIRED"
        return "NOT_READY"
    return "NOT_READY"


def test_cases():
    good = {"asset_exists": True, "baseline_approved": True,
            "evidence_present": True, "source": "SYNTHETIC"}
    cases = [
        ({**good, "asset_exists": False}, "NOT_READY"),
        ({**good, "observation": "http_403"}, "NOT_READY"),
        ({**good, "observation": "timeout"}, "NOT_READY"),
        ({**good, "observation": "nxdomain"}, "NOT_READY"),
        ({**good, "observation": "connection_refused"}, "NOT_READY"),
        ({**good, "observation": "tls_error"}, "NOT_READY"),
        ({**good, "observation": "tls_error", "mode": "internal_positive"}, "DIFFERENCE_REVIEW_REQUIRED"),
        ({**good, "observation": "unauthorized_http_200"}, "DIFFERENCE_REVIEW_REQUIRED"),
        ({**good, "observation": "unexpected_public_ip"}, "DIFFERENCE_REVIEW_REQUIRED"),
        ({**good, "observation": "denied_with_control_plane", "control_plane_private_confirmed": True,
          "external_network_confirmed": True, "resource_id": "SYNTHETIC", "collected_at_utc": "SYNTHETIC"},
         "REVIEW_REQUIRED"),
    ]
    return cases


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--expected", choices=["Pass", "Fail", "NotReady"])
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        cases = test_cases()
        failures = [i for i, (row, expected) in enumerate(cases)
                    if classify(row, synthetic_testing=True) != expected]
        print(json.dumps({
            "result": "SELFTEST_PASS" if not failures else "SELFTEST_FAIL",
            "execution_class": "OFFLINE_SYNTHETIC_ONLY",
            "synthetic_cases": len(cases), "errors": failures,
            "azure_live_passes": 0, "release_decision": "NO_GO"
        }, sort_keys=True))
        return 0 if not failures else 1
    if args.input is None:
        print(json.dumps({"result": "NOT_READY", "reason": "input missing",
                          "azure_live_passes": 0, "release_decision": "NO_GO"}))
        return 2
    try:
        obj = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        print(json.dumps({"result": "NOT_READY", "reason": "input unreadable or invalid",
                          "azure_live_passes": 0, "release_decision": "NO_GO"}))
        return 2
    status = classify(obj)
    print(json.dumps({"result": status, "legacy_expected": args.expected,
                      "azure_live_passes": 0, "release_decision": "NO_GO",
                      "scope": "UNTRUSTED_LOCAL_EVIDENCE",
                      "note": "Never treat equality with legacy --expected as accepted Azure evidence"}, sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
