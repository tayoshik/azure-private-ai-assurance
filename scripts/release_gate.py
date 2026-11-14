#!/usr/bin/env python3
"""Conservative release gate: never promote synthetic evidence to live success."""
import argparse,json,sys
from pathlib import Path
from validate_catalogue import check

def decide(root):
    errors=check(root)
    if errors:return {'decision':'NO_GO','reasons':['catalogue validation failed']+errors[:3]}
    index=json.loads((root/'specs/catalogue_index_1716.json').read_text())
    reasons=[]
    if index['azure_live_passes']<1716:reasons.append('live acceptance coverage incomplete')
    if index.get('release_decision')!='GO':reasons.append('independent release approval unavailable')
    if index['counts']['synthetic_detector_tests']>0:reasons.append('synthetic detector checks do not establish Azure control acceptance')
    # This repository deliberately cannot sign or issue a GO decision.
    return {'decision':'NO_GO','reasons':reasons or ['independent approved live evidence required'],'live_passes':index['azure_live_passes']}

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
    args=p.parse_args(); result=decide(args.root);print(json.dumps(result,indent=2));return 0
if __name__=='__main__':sys.exit(main())
