#!/usr/bin/env python3
"""Evidence integrity and scope gate; never grants live PASS or production GO.

A detached Ed25519 signature is validated with OpenSSL, using an independently
pinned trusted public key. Valid signature plus matching hashes/scope yields
REVIEW_REQUIRED only. Identity, controls and final approval must be reviewed
outside this tool by authorized parties.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

HEX64=re.compile(r'^[0-9a-f]{64}$')
TEST=re.compile(r'^AZ-T(\d{2})-(\d{2})$')
HEX_UUID=re.compile(r'^[a-zA-Z0-9][-a-zA-Z0-9_.:/]{4,255}$')


def digest(raw):return hashlib.sha256(raw).hexdigest()


def read_json(p):return json.loads(p.read_text(encoding='utf-8'))


def in_root(root,p):
    root=root.resolve(strict=True)
    p=p.resolve(strict=True)
    if not p.is_relative_to(root):raise ValueError('evidence file outside approved root')
    if not p.is_file():raise ValueError('evidence path is not a regular file')
    return p


def verify(record_file,signature_file,observation_file,baseline_file,scope_file,pubkey_file,pubkey_pin,evidence_root,now=None):
    """Return (NOT_READY | REVIEW_REQUIRED, reasons). Never live PASS."""
    reasons=[]
    try:
        now=(now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        root=Path(evidence_root).resolve(strict=True)
        paths=[in_root(root,Path(p)) for p in (record_file,signature_file,observation_file,baseline_file)]
        record_path,sig_path,obs_path,base_path=paths
        key=Path(pubkey_file).resolve(strict=True)
        if not HEX64.fullmatch(pubkey_pin or '') or digest(key.read_bytes())!=pubkey_pin:
            return 'NOT_READY',['trusted public key SHA-256 mismatch or unpinned key']
        scope=read_json(Path(scope_file))
        record=read_json(record_path)
        if scope.get('approved') is not True or scope.get('fixture') is True:
            reasons.append('independent scope approval absent')
        for k in ('test_id','subscription_id','resource_id','runner_id','authorization_ticket','collector_id','run_id','collected_at','observation_sha256','baseline_sha256'):
            if not isinstance(record.get(k),str) or not record[k].strip():reasons.append('missing '+k)
        if not isinstance(record.get('synthetic'),bool) or record.get('synthetic') is True:
            reasons.append('synthetic or undefined provenance')
        tid=record.get('test_id','');m=TEST.fullmatch(tid)
        if not m or int(m[1]) not in range(1,79) or int(m[2]) not in range(1,23):reasons.append('invalid canonical test ID')
        if record.get('subscription_id')!=scope.get('subscription_id'):reasons.append('subscription mismatch')
        if record.get('resource_id')!=scope.get('resource_id'):reasons.append('resource mismatch')
        if record.get('authorization_ticket')!=scope.get('authorization_ticket'):reasons.append('authorization mismatch')
        if record.get('runner_id') not in scope.get('approved_runners',[]):reasons.append('unapproved runner')
        if record.get('collector_id') not in scope.get('approved_collectors',[]):reasons.append('unapproved collector')
        if record.get('test_id') not in scope.get('approved_test_ids',[]):reasons.append('test ID outside approved scope')
        if not (record.get('resource_id','').lower().startswith('/subscriptions/'+record.get('subscription_id','').lower()+'/')):
            reasons.append('resource outside subscription')
        if not HEX64.fullmatch(record.get('observation_sha256','')) or digest(obs_path.read_bytes())!=record.get('observation_sha256'):
            reasons.append('observation SHA-256 mismatch')
        if not HEX64.fullmatch(record.get('baseline_sha256','')) or digest(base_path.read_bytes())!=record.get('baseline_sha256'):
            reasons.append('baseline SHA-256 mismatch')
        if record.get('baseline_sha256')!=scope.get('approved_baseline_sha256'):
            reasons.append('baseline not independently pinned')
        try:
            stamp=datetime.fromisoformat(record.get('collected_at',''))
            if stamp.tzinfo is None:raise ValueError('timestamp timezone missing')
            stamp=stamp.astimezone(timezone.utc)
            if stamp>now+timedelta(minutes=5):reasons.append('future-dated observation')
            if now-stamp>timedelta(days=7):reasons.append('stale evidence')
        except (ValueError,TypeError):reasons.append('invalid UTC collection timestamp')
        # Verify the exact signed bytes of record.json (not re-serialized data).
        try:
            result=subprocess.run(['openssl','pkeyutl','-verify','-pubin','-inkey',str(key),'-rawin',
                    '-in',str(record_path),'-sigfile',str(sig_path)],
                    capture_output=True,text=True,timeout=15,check=False)
            if result.returncode!=0:reasons.append('Ed25519 signature verification failed')
        except (OSError,subprocess.TimeoutExpired):
            reasons.append('OpenSSL verifier unavailable')
        if record.get('schema_version') != 'evidence-record-v1':
            reasons.append('unsupported evidence schema version')
        if record.get('source_environment') != 'APPROVED_NONPROD_CI':
            reasons.append('unapproved source environment')
        if record.get('verification_level') != 'OBSERVATION_ONLY':
            reasons.append('unexpected verification level')
        # Semantic control criteria deliberately not decided from the envelope alone.
        # Even a good observation must be checked against control-specific rules + independent review.
    except (OSError,ValueError,TypeError,json.JSONDecodeError) as exc:
        reasons.append('invalid evidence: '+str(exc))
    if reasons:return 'NOT_READY',reasons
    return 'REVIEW_REQUIRED',['hashes, scope, timestamp and detached Ed25519 signature verified; control semantics and independent reviewer decision still pending']


def main(argv=None):
    parser=argparse.ArgumentParser()
    for x in ('record','signature','observation','baseline','scope','trusted-pubkey','pubkey-sha256','evidence-root'):
        parser.add_argument('--'+x,required=True)
    args=parser.parse_args(argv)
    status,reasons=verify(args.record,args.signature,args.observation,args.baseline,args.scope,args.trusted_pubkey,args.pubkey_sha256,args.evidence_root)
    print(json.dumps({'decision':status,'azure_live_acceptance':'NOT_READY','reasons':reasons},indent=2))
    return 0 if status=='REVIEW_REQUIRED' else 2

if __name__=='__main__':sys.exit(main())
