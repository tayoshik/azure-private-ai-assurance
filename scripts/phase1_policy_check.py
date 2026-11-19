#!/usr/bin/env python3
"""Read-only Phase1 design policy checker. No network, no Azure CLI, no apply.
A field match is NEVER an Azure acceptance PASS; local mismatches require independent review.
"""
import argparse, copy, datetime, hashlib, json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
MISSING=object()

def read_json(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def write_json(p,x):
    out=pathlib.Path(p);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def getpath(doc,path):
    obj=doc
    for key in path.split('.'):
        if not isinstance(obj,dict) or key not in obj: return MISSING
        obj=obj[key]
    return obj

def match(value,rule):
    if value is MISSING or value is None: return 'NOT_READY'
    op=rule['operator']; exp=rule['expected']
    if op=='eq': return 'PASS' if type(value) is type(exp) and value==exp else 'FAIL'
    if op=='enum': return 'PASS' if type(value) is str and value in exp else 'FAIL'
    if op=='nonempty': return 'PASS' if isinstance(value,str) and value.strip() and value.upper() not in {'TBD','UNKNOWN','TBC','TODO','N/A'} else 'FAIL'
    if op=='list_nonempty': return 'PASS' if isinstance(value,list) and len(value)>0 and all(isinstance(v,str) and v.strip() and v.upper() not in {'TBD','UNKNOWN'} for v in value) else 'FAIL'
    if op=='positive': return 'PASS' if type(value) in (int,float) and value>0 else 'FAIL'
    raise ValueError('Unknown operator '+op)

def setpath(doc,path,value):
    p=path.split('.'); cur=doc
    for k in p[:-1]:cur=cur.setdefault(k,{})
    cur[p[-1]]=value

def delpath(doc,path):
    p=path.split('.');cur=doc
    for k in p[:-1]:
        if k not in cur:return
        cur=cur[k]
    cur.pop(p[-1],None)

def good_value(rule):
    op=rule['operator']; exp=rule['expected']
    if op=='eq':return exp
    if op=='enum':return exp[0]
    if op=='nonempty':return 'SYNTHETIC_REVIEW_TOKEN'
    if op=='list_nonempty':return ['SYNTHETIC_REVIEW_TOKEN']
    if op=='positive':return 60
    raise ValueError(op)

def bad_value(rule):
    op=rule['operator']; exp=rule['expected']
    if op=='eq':return not exp if type(exp) is bool else '__INVALID__'
    if op=='enum':return '__DISALLOWED__'
    if op=='nonempty':return 'TBD'
    if op=='list_nonempty':return []
    if op=='positive':return -1
    raise ValueError(op)

def selftest(rule):
    base={'_synthetic_fixture':True};setpath(base,rule['field_path'],good_value(rule))
    bad=copy.deepcopy(base);setpath(bad,rule['field_path'],bad_value(rule))
    missing=copy.deepcopy(base);delpath(missing,rule['field_path'])
    actual=[match(getpath(d,rule['field_path']),rule) for d in (base,bad,missing)]
    expected=['PASS','FAIL','NOT_READY']
    return {'positive_id':rule['positive_id'],'negative_id':rule['negative_id'],'field':rule['field_path'], 'synthetic_only':True,'good_fixture':actual[0], 'bad_fixture':actual[1], 'missing_fixture':actual[2], 'selftest_status':'SELFTEST_PASS' if actual==expected else 'SELFTEST_FAIL'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rules',default=str(ROOT/'specs/phase1_policies_110.json'))
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--selftest',action='store_true');group.add_argument('--baseline')
    ap.add_argument('--test-id');ap.add_argument('--all',action='store_true');ap.add_argument('--json-out')
    args=ap.parse_args()
    try:
        rules=read_json(args.rules)
        if not isinstance(rules,list) or len(rules)!=110:
            raise ValueError('expected exactly 110 rules')
        expected={f'AZ-T{s:02}-{n:02}' for s in range(1,11) for n in range(1,23)}
        ids=[x for r in rules for x in (r['positive_id'],r['negative_id'])]
        if (len(set(ids))!=220 or set(ids)!=expected or
            len({r['field_path'] for r in rules})!=110 or
            any(r['positive_id'][-2:] not in [f'{n:02}' for n in range(1,23,2)] or
                r['negative_id'][-2:] not in [f'{n:02}' for n in range(2,23,2)] or
                int(r['positive_id'][4:6])!=r['step'] or
                int(r['negative_id'][4:6])!=r['step'] or
                r['operator'] not in ('eq','enum','positive','list_nonempty','nonempty')
                for r in rules)):
            raise ValueError('canonical rule IDs, steps or predicates inconsistent')
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(json.dumps({'result':'NOT_READY','reason':'Phase 1 canonical rules missing or invalid',
                          'azure_live_pass_count':0}))
        return 2
    if not args.all and not args.test_id:
        print(json.dumps({'result':'NOT_READY','reason':'select --test-id or --all',
                          'azure_live_pass_count':0}))
        return 2
    if args.baseline and args.test_id and args.test_id[-2:] in [f'{n:02}' for n in range(2,23,2)]:
        print(json.dumps({'result':'NOT_READY','reason':'synthetic ID cannot check a real baseline',
                          'azure_live_pass_count':0}))
        return 2
    selected=[r for r in rules if args.all or args.test_id in (r['positive_id'],r['negative_id'])]
    if not selected:
        print(json.dumps({'result':'NOT_READY','reason':'unknown ID',
                          'azure_live_pass_count':0}))
        return 2
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    report={'generated_utc':now,'rules_sha256':hashlib.sha256(pathlib.Path(args.rules).read_bytes()).hexdigest(),'scope':'synthetic selftest' if args.selftest else 'design-document predicate check only; NO live acceptance','azure_live_pass_count':0,'cases':[]}
    if args.selftest:
        report['cases']=[selftest(r) for r in selected]
        report['summary']={'SELFTEST_PASS':sum(r['selftest_status']=='SELFTEST_PASS' for r in report['cases']),'SELFTEST_FAIL':sum(r['selftest_status']=='SELFTEST_FAIL' for r in report['cases'])}
        status=0 if report['summary']['SELFTEST_FAIL']==0 else 1
    else:
        try:
            baseline_path=pathlib.Path(args.baseline)
            data=read_json(baseline_path)
            report['baseline_sha256']=hashlib.sha256(baseline_path.read_bytes()).hexdigest()
            if not isinstance(data,dict):
                raise ValueError('baseline root must be an object')
        except (OSError,ValueError,TypeError) as e:
            data=None;report['error']=str(e)
        for r in selected:
            raw='NOT_READY' if data is None else match(getpath(data,r['field_path']),r)
            if data is None or data.get('_synthetic_fixture') is True or raw=='NOT_READY':
                state='NOT_READY'
            elif raw=='FAIL':
                state='DIFFERENCE_REVIEW_REQUIRED'
            else:
                state='REVIEW_REQUIRED'
            report['cases'].append({'test_id':r['positive_id'], 'field':r['field_path'],
                                   'predicate':raw, 'acceptance_status':state,
                                   'review_notice':'Unsigned local data cannot prove an Azure PASS or authoritative FAIL'})
        report['summary']={s:sum(r['acceptance_status']==s for r in report['cases'])
                           for s in ['DIFFERENCE_REVIEW_REQUIRED','NOT_READY','REVIEW_REQUIRED']}
        status=2  # source-only baseline evaluation is NEVER an acceptance decision
    if args.json_out:write_json(args.json_out,report)
    print(json.dumps({'scope':report['scope'],'summary':report['summary'],'azure_live_pass_count':0},ensure_ascii=False))
    return status
if __name__=='__main__':sys.exit(main())
