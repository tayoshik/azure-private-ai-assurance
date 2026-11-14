#!/usr/bin/env python3
"""Fail-closed *textual* checks for initial HCL contracts. Not terraform validate.

No cloud calls, providers, credentials, or remote mutation are used.
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "infra/bootstrap/versions.tf": ['version = "= 4.66.0"', 'storage_use_azuread = true'],
    "infra/bootstrap/main.tf": [
        'resource "azurerm_storage_account" "state"',
        'public_network_access_enabled   = false',
        'shared_access_key_enabled       = false',
        'allow_nested_items_to_be_public = false',
        'https_traffic_only_enabled      = true',
        'min_tls_version                 = "TLS1_2"',
        'versioning_enabled = true',
        'prevent_destroy = true',
        'resource "azurerm_storage_container" "state"',
        'storage_account_id    = azurerm_storage_account.state.id',
        'scope                = azurerm_storage_container.state.resource_manager_id',
        'role_definition_name = "Storage Blob Data Contributor"',
    ],
    "infra/bootstrap/private_state.tf": [
        'resource "azurerm_virtual_network" "bootstrap"',
        'resource "azurerm_private_endpoint" "state_blob"',
        'subresource_names              = ["blob"]',
        'privatelink.blob.core.windows.net',
        'azurerm_private_dns_zone_virtual_network_link',
    ],
    "infra/modules/foundation/main.tf": ['resource "azurerm_resource_group" "workload"'],
    "infra/modules/network/main.tf": [
        'resource "azurerm_virtual_network" "workload"',
        'Microsoft.Network/applicationGateways',
        'Microsoft.Web/serverFarms',
        'resource "azurerm_subnet" "web_private_endpoint"',
        'resource "azurerm_subnet" "data_private_endpoint"',
        'private_endpoint_network_policies = "Enabled"',
    ],
    "infra/modules/private-dns/main.tf": [
        'azurerm_private_dns_zone_virtual_network_link',
        'registration_enabled  = false',
    ],
    "infra/environments/dev/versions.tf": [
        'version = "= 4.66.0"', 'backend "azurerm" {}', 'storage_use_azuread = true'
    ],
    "infra/environments/dev/main.tf": [
        'module "foundation"', 'module "network"', 'module "private_dns"'
    ],
    "infra/environments/dev/variables.tf": [
        'privatelink.azurewebsites.net',
        'privatelink.openai.azure.com',
        'privatelink.search.windows.net',
        'privatelink.documents.azure.com',
        'privatelink.vaultcore.azure.net',
    ],
    "infra/environments/dev/backend.azurerm.example.hcl": [
        'use_azuread_auth     = true', 'use_oidc             = true'
    ]
}


def lexical_balance(source: str) -> bool:
    """Check delimiters and quotes, ignoring HCL line/block comments.

    This is deliberately *not* a replacement for HCL2 parsing/provider validate.
    """
    stack = []
    matches = {"}": "{", "]": "[", ")": "("}
    i = 0
    inside_string = False
    while i < len(source):
        c = source[i]
        if inside_string:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                inside_string = False
            i += 1
            continue
        if source.startswith("//", i) or c == "#":
            k = source.find("\n", i)
            i = k if k >= 0 else len(source)
            continue
        if source.startswith("/*", i):
            k = source.find("*/", i + 2)
            if k < 0:
                return False
            i = k + 2
            continue
        if c == '"':
            inside_string = True
        elif c in "{[(":
            stack.append(c)
        elif c in "}])":
            if not stack or stack.pop() != matches[c]:
                return False
        i += 1
    return not stack and not inside_string


def check(root=ROOT):
    root = Path(root)
    errors = []
    for rel, required in EXPECTED.items():
        path = root / rel
        if not path.is_file():
            errors.append(f"missing: {rel}")
            continue
        s = path.read_text(encoding="utf-8")
        if not lexical_balance(s):
            errors.append(f"unbalanced HCL delimiters: {rel}")
        for pattern in required:
            if pattern not in s:
                errors.append(f"required contract missing in {rel}: {pattern}")
    tf = list((root / "infra").rglob("*.tf"))
    if len(tf) < 18:
        errors.append(f"unexpectedly small HCL set: {len(tf)}")
    for p in (root / "infra").rglob("*.tf"):
        s = p.read_text(encoding="utf-8")
        if re.search(r"(?i)(client_secret|access_key|sas_token)\s*=\s*\"[^\"]+\"", s):
            errors.append(f"possible hardcoded secret: {p}")
        if re.search(r"(?im)^\s*public_network_access_enabled\s*=\s*true", s):
            errors.append(f"public network enabled: {p}")
    if 'backend "azurerm"' in (root / "infra/bootstrap/versions.tf").read_text():
        errors.append("bootstrap must NOT depend on its own remote backend")
    expected_subnets = set(re.findall(r'resource "azurerm_subnet" "([^"]+)"', (root / "infra/modules/network/main.tf").read_text()))
    if expected_subnets != {"app_gateway", "app_outbound", "web_private_endpoint", "data_private_endpoint"}:
        errors.append("workload subnet contract mismatch")
    # Never promote static status to real Azure acceptance.
    return {
        "state": "PASS_OFFLINE_TEXT_REVIEW_ONLY" if not errors else "FAIL",
        "terraform_cli_validation": "NOT_EXECUTED",
        "terraform_plan": "NOT_EXECUTED",
        "terraform_apply": "NOT_EXECUTED",
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "tf_file_count": len(tf),
        "checked_contract_files": len(EXPECTED),
        "errors": errors,
    }


if __name__ == "__main__":
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(bool(result["errors"]))
