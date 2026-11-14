#!/usr/bin/env python3
"""G03/Q01 provider verification preflight. No Terraform/Azure commands are run."""
from __future__ import annotations
import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOTS = ('infra/bootstrap', 'infra/environments/dev')
PROVIDER_PIN = '= 4.66.0'


def audit(root: Path = ROOT, *, require_lock: bool = False) -> dict:
    root = Path(root)
    errors, blockers, lock_state = [], [], {}
    tf_files = sorted((root / 'infra').rglob('*.tf'))
    if len(tf_files) < 61:
        errors.append(f'expected at least 61 Terraform source files, found {len(tf_files)}')
    for rel in ROOTS:
        base = root / rel
        versions = base / 'versions.tf'
        if not versions.is_file():
            errors.append(f'missing: {versions.relative_to(root)}')
            continue
        data = versions.read_text(encoding='utf-8')
        if not re.search(r'(?m)^\s*version\s*=\s*"= 4\.66\.0"', data):
            errors.append(f'{rel}: AzureRM provider is not exactly pinned to 4.66.0')
        if not re.search(r'required_version\s*=\s*"[^\"]*1\.9\.0[^\"]*"', data):
            errors.append(f'{rel}: Terraform CLI minimum version contract missing')
        remote = bool(re.search(r'(?m)^\s*(?:terraform\s*\{\s*)?backend\s+"azurerm"', data))
        if rel.endswith('bootstrap') and remote:
            errors.append('bootstrap backend must not depend on its own Azure Blob account')
        if rel.endswith('dev') and not remote:
            errors.append('dev backend must be explicit azurerm')
        lock = base / '.terraform.lock.hcl'
        if not lock.is_file():
            lock_state[rel] = 'MISSING'
            blockers.append(f'{rel}/.terraform.lock.hcl requires signed-provider generation and independent review')
        else:
            contents = lock.read_text(encoding='utf-8')
            lock_state[rel] = 'PRESENT_UNVERIFIED'
            if not re.search(r'provider\s+"registry\.terraform\.io/hashicorp/azurerm"', contents):
                errors.append(f'{rel}: azurerm provider missing in lockfile')
            if not re.search(r'(?m)^\s*version\s*=\s*"4\.66\.0"', contents):
                errors.append(f'{rel}: pinned version mismatch in lockfile')
            if not re.search(r'"(?:h1:|zh:)[^\"]+"', contents):
                errors.append(f'{rel}: lockfile checksum absent')
    cli_present = shutil.which('terraform') is not None
    if not cli_present:
        blockers.append('Terraform CLI absent in this execution environment; run official provider workflow')
    result = {
        'status': 'FAIL_SOURCE' if errors else 'PASS_SOURCE_WITH_PROVIDER_GATES_NOT_READY',
        'provider_pin': PROVIDER_PIN,
        'terraform_source_files': len(tf_files),
        'cli_found_locally': cli_present,
        'lockfiles': lock_state,
        'fmt': 'NOT_EXECUTED',
        'init': 'NOT_EXECUTED',
        'validate': 'NOT_EXECUTED',
        'terraform_plan': 'NOT_EXECUTED',
        'terraform_apply': 'NOT_EXECUTED',
        'azure_live_passes': 0,
        'release_decision': 'NO_GO',
        'errors': errors,
        'blockers': blockers,
    }
    if require_lock and blockers:
        result['status'] = 'NOT_READY_PROVIDER_GATES'
    return result


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--require-lock', action='store_true', help='fail closed if lockfiles or CLI are absent')
    args = p.parse_args()
    data = audit(require_lock=args.require_lock)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 1 if data['errors'] else (2 if args.require_lock and data['blockers'] else 0)


if __name__ == '__main__':
    raise SystemExit(main())