#!/usr/bin/env python3
"""No-Azure, fail-closed source-to-DAG reconciliation for exactly 55/147."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DAG = "docs/terraform-implementation-dag.md"
MAP = "specs/terraform-dag-source-map.json"
ROW = re.compile(r'^\| \*\*([A-Z]{1,2}\d{2})\*\* [^|]*\|([^|]*)\| \x60([^\x60]+)\x60 \| ([A-Z_]+) \|$', re.M)
NODE_REF = re.compile(r"[A-Z]{1,2}\d{2}")
EXPECTED_CLASSES = {
    "CODE_SOURCE_PRESENT_ONLY": 30,
    "DESIGN_INPUT_NOT_MATERIALIZED": 5,
    "LIVE_APPROVAL_NOT_READY": 14,
    "OFFLINE_ARTIFACT_NOT_MATERIALIZED": 2,
    "OPTIONAL_DECISION_PENDING": 3,
    "OPTIONAL_AMPLS_PARTIAL": 1,
}
LEGACY_ABSENT = {
    "B02": "infra/bootstrap/storage_security.tf",
    "N02": "infra/modules/network/vnet.tf",
    "N03": "infra/modules/network/subnets.tf",
    "O02": "infra/modules/monitoring/private-observability.tf",
    "A01": "infra/modules/azure-openai/account.tf",
    "A02": "infra/modules/azure-openai/deployment.tf",
    "A05": "infra/modules/private-endpoints/ai-data.tf",
    "A06": "infra/modules/identity/data-roles.tf",
    "W04": "infra/modules/private-endpoints/webapp.tf",
    "GW02": "infra/modules/application-gateway/tls-cert.tf",
}
# Source anchors confirm mapped syntax, NOT independent control acceptance.
ANCHORS = {
    "B02": ('resource "azurerm_storage_account" "state" {',
            'resource "azurerm_storage_container" "state" {'),
    "N02": ('resource "azurerm_virtual_network" "workload" {',),
    "N03": ('resource "azurerm_subnet" "app_gateway" {',
            'resource "azurerm_subnet" "app_outbound" {',
            'resource "azurerm_subnet" "web_private_endpoint" {',
            'resource "azurerm_subnet" "data_private_endpoint" {'),
    "O02": ('resource "azurerm_monitor_private_link_scope" "monitor" {',),
    "A01": ('resource "azurerm_cognitive_account" "openai" {',),
    "A02": ('resource "azurerm_cognitive_deployment" "model" {',),
    "A05": ('resource "azurerm_private_endpoint" "openai" {',
            'resource "azurerm_private_endpoint" "search" {',
            'resource "azurerm_private_endpoint" "cosmos" {'),
    "A06": ('resource "azurerm_role_assignment" "openai_user" {',
            'resource "azurerm_role_assignment" "search_reader" {',
            'resource "azurerm_cosmosdb_sql_role_assignment" "app" {'),
    "W04": ('resource "azurerm_private_endpoint" "web_app" {',),
    "GW02": ('ssl_certificate {',
             'key_vault_secret_id = var.key_vault_certificate_secret_versionless_id'),
}
RECONCILED = {
    "B02": "infra/bootstrap/main.tf",
    "N02": "infra/modules/network/main.tf",
    "N03": "infra/modules/network/main.tf",
    "O02": "infra/modules/monitoring/private-link.tf",
    "A01": "infra/modules/azure-openai/main.tf",
    "A02": "infra/modules/azure-openai/main.tf",
    "A05": "infra/modules/ai-private-endpoints/main.tf",
    "A06": "infra/modules/ai-data-rbac/main.tf",
    "W04": "infra/modules/webapp-private-endpoint/webapp.tf",
    "GW02": "infra/modules/application-gateway/gateway.tf",
}


def path_at(root: Path, rel: str) -> Path:
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
        raise ValueError("unsafe or empty relative deliverable")
    canonical_root = root.resolve()
    result = (root / rel.rstrip("/")).resolve()
    if not result.is_relative_to(canonical_root):
        raise ValueError("deliverable escapes root")
    return result


def parse_dag(text: str):
    entries = {}
    errors = []
    for matched in ROW.finditer(text):
        ident, deps, rel, mode = matched.groups()
        if ident in entries:
            errors.append("duplicate DAG ID " + ident)
        entries[ident] = {
            "id": ident,
            "prerequisites": NODE_REF.findall(deps),
            "declared_path": rel,
            "mode": mode,
        }
    edges = sum(len(r["prerequisites"]) for r in entries.values())
    if len(entries) != 55 or edges != 147:
        errors.append("DAG must retain 55 nodes / 147 dependencies")
    for ident, row in entries.items():
        for d in row["prerequisites"]:
            if d not in entries:
                errors.append(ident + ": unknown dependency " + d)
            if d == ident:
                errors.append(ident + ": self dependency")
    visiting, visited = set(), set()
    def dfs(ident):
        if ident in visiting:
            errors.append("cycle involving " + ident)
            return
        if ident in visited:
            return
        visiting.add(ident)
        for d in entries[ident]["prerequisites"]:
            if d in entries:
                dfs(d)
        visiting.remove(ident)
        visited.add(ident)
    for ident in entries:
        dfs(ident)
    return entries, edges, errors


def inspect(root: Path = ROOT, *, include_nodes: bool = True) -> dict:
    root = Path(root)
    try:
        text = (root / DAG).read_text(encoding="utf-8")
        manifest = json.loads((root / MAP).read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        return {
            "schema": "terraform-dag-source-audit/v1",
            "status": "INVALID_DAG_SOURCE",
            "errors": ["missing or invalid DAG/manifest: " + type(exc).__name__],
            "azure_live_passes": 0,
            "release_decision": "NO_GO",
        }
    entries, edges, errors = parse_dag(text)
    if not isinstance(manifest, dict):
        manifest = {}
        errors.append("manifest is not an object")
    for key, value in {
        "schema": "terraform-dag-path-status/v1",
        "source_dag": DAG,
        "dag_nodes": 55,
        "dag_edges": 147,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
    }.items():
        if manifest.get(key) != value:
            errors.append("invalid manifest field: " + key)
    records = manifest.get("nodes")
    if not isinstance(records, list):
        records = []
        errors.append("manifest nodes must be an array")
    seen = set()
    counts = Counter()
    rows = {}
    for record in records:
        if not isinstance(record, dict) or set(record) != {
            "id", "mode", "declared_path", "classification",
        }:
            errors.append("invalid manifest node record")
            continue
        ident = record["id"]
        if not isinstance(ident, str) or ident in seen:
            errors.append("invalid or duplicate manifest node ID")
            continue
        seen.add(ident)
        expected = entries.get(ident)
        if expected is None:
            errors.append("unknown manifest node " + ident)
            continue
        if record["mode"] != expected["mode"] or record["declared_path"] != expected["declared_path"]:
            errors.append(ident + ": DAG/manifest path or mode drift")
            continue
        rel, status = record["declared_path"], record["classification"]
        try:
            target = path_at(root, rel)
        except ValueError:
            errors.append(ident + ": unsafe declared path")
            continue
        present = target.is_dir() if rel.endswith("/") else target.is_file()
        mode = expected["mode"]
        counts[status] += 1
        if status == "CODE_SOURCE_PRESENT_ONLY":
            if mode != "CODE" or not present or not target.is_file():
                errors.append(ident + ": CODE path absent/not source")
        elif status == "OPTIONAL_AMPLS_PARTIAL":
            if ident != "O02" or mode != "OPTIONAL" or not present:
                errors.append(ident + ": AMPLS optional partial mapping invalid")
        elif status == "OPTIONAL_DECISION_PENDING":
            if mode != "OPTIONAL" or ident == "O02" or present:
                errors.append(ident + ": optional decision requires explicit review")
        elif status == "LIVE_APPROVAL_NOT_READY":
            if mode not in ("APPROVAL", "LIVE_GATE", "REVIEW") or present:
                errors.append(ident + ": live/approval artifact needs review")
        elif status == "OFFLINE_ARTIFACT_NOT_MATERIALIZED":
            if mode != "OFFLINE_GATE" or present:
                errors.append(ident + ": offline artifact needs explicit review")
        elif status == "DESIGN_INPUT_NOT_MATERIALIZED":
            if mode not in ("DESIGN", "INPUT") or present:
                errors.append(ident + ": design input needs explicit review")
        else:
            errors.append(ident + ": unknown source classification")
        if ident in RECONCILED:
            if rel != RECONCILED[ident]:
                errors.append(ident + ": obsolete source mapping")
            if target.is_file():
                try:
                    hcl = target.read_text(encoding="utf-8")
                    for anchor in ANCHORS[ident]:
                        if not re.search(r"(?m)^\s*" + re.escape(anchor) + r"\s*$", hcl):
                            errors.append(ident + ": source HCL anchor missing")
                except (OSError, UnicodeError):
                    errors.append(ident + ": HCL unreadable")
            if path_at(root, LEGACY_ABSENT[ident]).exists():
                errors.append(ident + ": legacy path unexpectedly exists")
        rows[ident] = {
            "mode": mode,
            "deliverable": rel,
            "source_state": status,
            "declared_path_present": present,
            "prerequisites": expected["prerequisites"],
            "node_closed_or_approved": False,
            "azure_acceptance": "NOT_READY",
        }
    if set(entries) != seen or set(rows) != set(entries):
        errors.append("manifest and DAG node IDs do not match")
    if dict(counts) != EXPECTED_CLASSES:
        errors.append("source classification counts drifted")
    result = {
        "schema": "terraform-dag-source-audit/v1",
        "status": "INVALID_DAG_SOURCE" if errors else "SOURCE_PATHS_RECONCILED_NOT_ACCEPTED",
        "dag_node_count": len(entries),
        "dag_edge_count": edges,
        "source_classes": dict(sorted(counts.items())),
        "reported_nodes": len(rows),
        "code_nodes_approved": 0,
        "independent_review_approvals": 0,
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "errors": errors,
        "limitations": [
            "File and Terraform resource presence do not establish deployment or acceptance",
            "Optional AMPLS is only partial; three optional modules need an owner decision",
            "No Terraform command, Azure CLI, browser, credentials or network access is used",
            "All canonical 1,716 live acceptance cases remain NOT_READY",
        ],
    }
    if include_nodes:
        result["nodes"] = rows
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--summary-only", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)
    result = inspect(args.root, include_nodes=not args.summary_only)
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 1 if result["errors"] else (2 if args.strict else 0)


if __name__ == "__main__":
    raise SystemExit(main())
