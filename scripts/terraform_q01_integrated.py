#!/usr/bin/env python3
"""Q01: reconcile Stage 1-6 offline source contracts (never Azure acceptance)."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECKERS = [
    'check_terraform_stage1.py',
    'check_terraform_n04.py',
    'check_terraform_i01_i03.py',
    'check_terraform_a01_a06.py',
    'check_terraform_w01_w05.py',
    'check_terraform_gw01_gw05.py',
]
REQUIRED = [
    'infra/bootstrap/main.tf',
    'infra/bootstrap/private_state.tf',
    'infra/bootstrap/versions.tf',
    'infra/environments/dev/main.tf',
    'infra/environments/dev/versions.tf',
    'infra/modules/network/policy.tf',
    'infra/modules/app-service/webapp.tf',
    'infra/modules/application-gateway/gateway.tf',
    'infra/modules/application-gateway/waf-policy.tf',
    'infra/modules/monitoring/main.tf',
]
FORBIDDEN_SECRET = re.compile(
    r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{25,}',
    re.I,
)


def review(root: Path = ROOT, *, require_fmt: bool = False) -> dict:
    root = Path(root)
    failures = []
    checker_summaries = []
    tf_paths = sorted((root / 'infra').rglob('*.tf')) if (root / 'infra').is_dir() else []
    if len(tf_paths) < 61:
        failures.append(f'Terraform HCL files incomplete: {len(tf_paths)} < 61 (Stage 6 baseline)')
    for rel in REQUIRED:
        if not (root / rel).is_file():
            failures.append(f'missing required source: {rel}')
    for path in tf_paths:
        data = path.read_text(encoding='utf-8')
        if FORBIDDEN_SECRET.search(data):
            failures.append(f'possible committed secret: {path.relative_to(root)}')
    bootstrap_version = root / 'infra/bootstrap/versions.tf'
    if bootstrap_version.exists() and re.search(r'backend\s+"azurerm"\s*\{', bootstrap_version.read_text()):
        failures.append('Bootstrap must not use its own AzureRM remote backend')
    dev_version = root / 'infra/environments/dev/versions.tf'
    if dev_version.exists():
        data = dev_version.read_text()
        if not re.search(r'version\s*=\s*"=\s*\d+\.\d+\.\d+"', data):
            failures.append('AzureRM version must be pinned to an exact version')
        if 'backend "azurerm"' not in data:
            failures.append('Workload root must use AzureRM remote backend')
    for filename in CHECKERS:
        script = root / 'scripts' / filename
        if not script.is_file():
            failures.append(f'missing contract checker: {filename}')
            continue
        process = subprocess.run(
            [sys.executable, str(script)], cwd=root,
            capture_output=True, text=True, timeout=120, check=False,
        )
        try:
            obj = json.loads(process.stdout)
            status = obj.get('state', obj.get('status', 'UNKNOWN'))
            errs = obj.get('errors', [])
            if not isinstance(errs, list):
                raise ValueError('errors is not a list')
        except (ValueError, TypeError):
            status, errs = 'UNPARSEABLE', ['checker emitted no valid JSON']
        if process.returncode or errs or not str(status).startswith('PASS_OFFLINE'):
            failures.append(f'{filename}: failed or incomplete; rc={process.returncode} status={status}')
        checker_summaries.append({'script': filename, 'status': status, 'error_count': len(errs)})
    fmt = 'NOT_EXECUTED'
    if require_fmt:
        exe = shutil.which('terraform')
        if exe is None:
            failures.append('terraform CLI not installed (fmt check NOT_READY)')
            fmt = 'NOT_READY'
        else:
            run = subprocess.run([exe, 'fmt', '-check', '-recursive', 'infra'],
                                 cwd=root, capture_output=True, text=True, timeout=90, check=False)
            fmt = 'PASS' if run.returncode == 0 else 'FAIL'
            if run.returncode:
                failures.append('terraform fmt -check -recursive infra failed (inspect locally)')
    fingerprint = hashlib.sha256('\n'.join(
        str(path.relative_to(root)) + ':' + hashlib.sha256(path.read_bytes()).hexdigest()
        for path in tf_paths
    ).encode()).hexdigest()
    return {
        'status': 'FAIL' if failures else 'PASS_OFFLINE_CONTRACT_ONLY',
        'terraform_file_count': len(tf_paths),
        'source_fingerprint_sha256': fingerprint,
        'checkers': checker_summaries,
        'terraform_fmt': fmt,
        'terraform_init': 'NOT_EXECUTED',
        'terraform_validate': 'NOT_EXECUTED',
        'terraform_plan': 'NOT_EXECUTED',
        'terraform_apply': 'NOT_EXECUTED',
        'azure_live_passes': 0,
        'live_acceptance_not_ready': 1716,
        'release_decision': 'NO_GO',
        'errors': failures,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--require-fmt', action='store_true', help='Run terraform fmt only when approved CLI exists')
    args = p.parse_args()
    out = review(require_fmt=args.require_fmt)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return int(bool(out['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
