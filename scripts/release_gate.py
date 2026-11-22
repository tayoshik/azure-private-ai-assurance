#!/usr/bin/env python3
"""Release gate: fail closed until independently approved Azure live acceptance.

This repository has no authority to sign live evidence or authorize deployment.
Static catalogue validity, CI success and synthetic fixtures NEVER produce GO.
The previous version depended on unpublished validate_catalogue.py and
catalogue_index_1716.json; the gate now uses tracked canonical sources.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

if __package__:
    from .audit_catalogue_dependencies import audit
    from .verify_publication import check as verify_publication
else:
    from audit_catalogue_dependencies import audit
    from verify_publication import check as verify_publication

ROOT = Path(__file__).resolve().parents[1]


def decide(root: Path = ROOT) -> dict:
    root = Path(root)
    reasons: list[str] = []
    catalogue = {}
    dependencies = {}
    metadata = {}
    try:
        catalogue = verify_publication(root)
        if catalogue.get("errors") or catalogue.get("test_ids") != 1716:
            reasons.append("canonical catalogue publication validation failed")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        reasons.append(f"canonical publication validation unavailable: {exc}")

    try:
        dependencies = audit(root)
        if dependencies.get("errors") or dependencies.get("canonical_test_ids") != 1716:
            reasons.append("1,716-ID dependency inventory is incomplete or invalid")
        if dependencies.get("cases_with_unresolved_literal_dependencies", 1716):
            reasons.append(
                f"{dependencies.get('cases_with_unresolved_literal_dependencies', 'unknown')} "
                "catalogue IDs reference missing local scripts or inputs"
            )
    except (OSError, ValueError, TypeError, KeyError) as exc:
        reasons.append(f"dependency inventory unavailable: {exc}")

    try:
        metadata = json.loads((root / "schemas/project-status.json").read_text(encoding="utf-8"))
        if not isinstance(metadata, dict):
            raise ValueError("project-status is not a JSON object")
        if (
            metadata.get("construction_steps") != 78
            or metadata.get("cases_per_step") != 22
            or metadata.get("test_cases") != 1716
        ):
            reasons.append("project-status case counts do not match canonical 78 x 22")
        if (
            metadata.get("azure_live_passes") != 0
            or metadata.get("azure_acceptance_not_ready") != 1716
            or metadata.get("release_decision") != "NO_GO"
        ):
            reasons.append("unverified or altered acceptance claims in project-status")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        reasons.append(f"project-status metadata unavailable: {exc}")

    # Even after missing files are implemented, this code cannot and must not
    # approve Azure live PASS. Signed evidence, operational tests and reviewer
    # authority are external to this public repository.
    reasons.append("independent signed live Azure acceptance evidence has not been verified")
    reasons.append("independent release authority has not issued approval")
    return {
        "decision": "NO_GO",
        "execution_class": "OFFLINE_SOURCE_AUDIT_ONLY",
        "catalogue_test_ids": catalogue.get("test_ids"),
        "catalogue_errors": catalogue.get("errors", []),
        "dependency_unresolved_ids": dependencies.get("cases_with_unresolved_literal_dependencies"),
        "dependency_missing_script_paths": dependencies.get("missing_script_paths", {}),
        "dependency_missing_input_paths": dependencies.get("missing_input_paths", {}),
        "recorded_azure_live_passes": metadata.get("azure_live_passes"),
        "verified_live_azure_passes": 0,
        "independent_approval": "NOT_VERIFIED",
        "reasons": reasons,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    print(json.dumps(decide(args.root), indent=2, ensure_ascii=False, sort_keys=True))
    # A release-denial must not be mistaken for an approved release by callers.
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
