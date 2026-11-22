#!/usr/bin/env python3
"""Offline structural consistency check for the two pinned AzureRM lockfiles.

No Terraform CLI or Azure credentials are used. Passing this script never
proves that providers were installed, verified or deployed successfully.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ROOTS = ("infra/bootstrap", "infra/environments/dev")
PROVIDER = "registry.terraform.io/hashicorp/azurerm"
VERSION = "4.66.0"
CLI_CONSTRAINT = ">= 1.9.0, < 2.0.0"
H1 = re.compile(r"h1:[A-Za-z0-9+/]{43}=")
ZH = re.compile(r"zh:[0-9a-f]{64}")
PROVIDER_BLOCK = re.compile(r'provider\s+"([^"]+)"\s*\{([^{}]*)\}', re.S)


def inspect(root: Path = ROOT) -> dict:
    root = Path(root)
    errors: list[str] = []
    locks: dict[str, dict] = {}
    lock_contents: dict[str, bytes] = {}
    for rel in ROOTS:
        base = root / rel
        versions = base / "versions.tf"
        lock = base / ".terraform.lock.hcl"
        try:
            versions_content = versions.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{rel}: versions.tf unavailable: {type(exc).__name__}")
            continue
        if not re.search(r'(?m)^\s*version\s*=\s*"=\s*4\.66\.0"', versions_content):
            errors.append(f"{rel}: AzureRM provider is not exactly pinned")
        if not re.search(r'\bsource\s*=\s*"hashicorp/azurerm"', versions_content):
            errors.append(f"{rel}: AzureRM source is not pinned")
        if not re.search(r'\brequired_version\s*=\s*"' + re.escape(CLI_CONSTRAINT) + r'"',
                         versions_content):
            errors.append(f"{rel}: Terraform CLI range drift")
        try:
            raw = lock.read_bytes()
            content = raw.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{rel}: lockfile unavailable: {type(exc).__name__}")
            continue
        lock_contents[rel] = raw
        locks[rel] = {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
            "provider": PROVIDER,
            "version": VERSION,
        }
        entries = PROVIDER_BLOCK.findall(content)
        if len(entries) != 1 or entries[0][0] != PROVIDER:
            errors.append(f"{rel}: must contain exactly one locked AzureRM provider")
            continue
        body = entries[0][1]
        if not re.search(r'\bversion\s*=\s*"' + re.escape(VERSION) + r'"', body):
            errors.append(f"{rel}: locked AzureRM version drift")
        if not re.search(r'\bconstraints\s*=\s*"' + re.escape(VERSION) + r'"', body):
            errors.append(f"{rel}: locked AzureRM constraints drift")
        checksum_block = re.search(r'\bhashes\s*=\s*\[([^\[\]]*)\]', body, re.S)
        if not checksum_block:
            errors.append(f"{rel}: lockfile checksum list missing")
            continue
        digests = re.findall(r'"([^"]+)"', checksum_block[1])
        if (len(digests) < 2 or
                len(set(digests)) != len(digests) or
                not any(H1.fullmatch(d) for d in digests) or
                not any(ZH.fullmatch(d) for d in digests) or
                any(not (H1.fullmatch(d) or ZH.fullmatch(d)) for d in digests)):
            errors.append(f"{rel}: malformed/duplicate/missing lockfile digests")
    if len(lock_contents) == len(ROOTS):
        if lock_contents[ROOTS[0]] != lock_contents[ROOTS[1]]:
            errors.append("bootstrap and dev lockfiles diverged: independent review required")
    return {
        "schema": "terraform-azurerm-readonly-lock-preflight/v1",
        "classification": "FAIL_SOURCE" if errors else "PASS_SOURCE_LOCK_CONSISTENCY_ONLY",
        "roots": list(ROOTS),
        "locks": locks,
        "pinned_provider": PROVIDER + "@" + VERSION,
        "terraform_cli_range": CLI_CONSTRAINT,
        "terraform_init": "NOT_EXECUTED_BY_THIS_SCRIPT",
        "terraform_validate": "NOT_EXECUTED_BY_THIS_SCRIPT",
        "terraform_plan": "NOT_EXECUTED",
        "terraform_apply": "NOT_EXECUTED",
        "azure_live_passes": 0,
        "release_decision": "NO_GO",
        "errors": errors,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    obj = inspect(args.root)
    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 1 if obj["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
