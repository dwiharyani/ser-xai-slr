"""Build public, non-identifying agreement summaries from a supplied aligned XLSX.

Run (offline; artifact_tool required):
    python scripts/build_agreement.py '/path/to/XAI_SER_Inter_Rater_Reliability_61_Studies_aligned.xlsx'

This does not publish the source second-coder workbook, reviewer remarks or any full texts.
"""
import csv
import json
import re
import sys
from pathlib import Path
from collections import Counter
from artifact_tool import SpreadsheetFile, Blob

R = Path(__file__).resolve().parents[1]
if len(sys.argv) != 2:
    raise SystemExit('Pass the local aligned agreement workbook as the sole argument.')
source = Path(sys.argv[1])
w = SpreadsheetFile.import_xlsx(Blob.load(str(source)))
D = R / 'public/data'; P = R / 'public/downloads'
known = {x['id'] for x in json.loads((D/'studies.json').read_text())}
assert len(known) == 61

def rows(name, width, limit=170):
    values = w.worksheets.get_item(name).get_range_by_indexes(0,0,limit,width).values
    headers=[str(x or '').strip() for x in values[0]]
    return [{k:v for k,v in zip(headers,row) if k} for row in values[1:] if row and re.fullmatch(r'M-\d{4}',str(row[0] or '').strip())]

def num(v):
    return None if v is None or str(v).strip()=='' else float(v)

primary=rows('Primary coding',15)
methods=rows('D4 methods',20)
secondary=rows('Secondary coding',24)
assert len(primary)==len(methods)==len(secondary)==61
assert {r['Study ID'] for r in primary}=={r['Study ID'] for r in methods}=={r['Study ID'] for r in secondary}==known

result_sheet=w.worksheets.get_item('Results').get_range('A5:J25').values
assert result_sheet[0][0]=='Dimension / category'
results=[]
for row in result_sheet[1:]:
    if row[0] is None or row[1] is None:continue
    label=str(row[0]); results.append({'dimension':label,'agreed':int(row[1]),'n':int(row[2]),'agreement':num(row[3]),'expected':num(row[4]),'kappa':num(row[5]),'ciLow':num(row[6]),'ciHigh':num(row[7]),'disagreed':int(row[8]),'bootstrapValid':int(row[9])})
assert len(results)==14,(len(results),[r['dimension'] for r in results])
assert all(r['n']==61 and r['agreed']+r['disagreed']==61 for r in results)
assert all(abs(r['agreement']-r['agreed']/61)<1e-9 for r in results)

# Compute categorical kappa from recorded pairings to check the reported totals.
def kappa_pair(pairs):
    N=len(pairs); first=Counter(a for a,b in pairs); second=Counter(b for a,b in pairs)
    observed=sum(a==b for a,b in pairs)/N
    expected=sum(first[c]*second[c] for c in set(first)|set(second))/N**2
    return (observed-expected)/(1-expected) if 1-expected>1e-12 else None
pairs_out=[]
for p in primary:
    d={'id':p['Study ID'],'title':p['Study title']}
    for dim in ('D1','D2','D3'):
        a=p[f'{dim} first coder'];b=p[f'{dim} second coder']
        d[dim.lower()+'First']=a;d[dim.lower()+'Second']=b;d[dim.lower()+'Match']=a==b
    pairs_out.append(d)

test_rows=[(r['dimension'], r['kappa']) for r in results[:3]]
for name, expected in test_rows:
    pairs=[(p[f'{name} first coder'],p[f'{name} second coder']) for p in primary]
    actual=kappa_pair(pairs)
    assert abs(actual-expected)<1e-9,(name,actual,expected)

for prefix,records in [('D4',methods),('secondary',secondary)]:
    columns=list(records[0]); checked=set()
    for c in columns:
        if not c.endswith('· First'):continue
        head=c[:-len(' · First')]
        b=head+' · Second'
        if b not in columns:continue
        pairs=[(str(r[c]),str(r[b])) for r in records]
        if head.startswith('D4 '): label=head
        elif head.startswith('Delivery'): label='Delivery'
        elif head.startswith('Speech information'): label='Speech information'
        elif head.startswith('Evaluation '): label=head
        else:continue
        for s in results:
            if s['dimension']==label:
                calc=kappa_pair(pairs)
                if calc is not None:assert abs(calc-s['kappa'])<1e-9,(label,calc,s['kappa'])
                assert sum(a==b for a,b in pairs)==s['agreed'],label
                checked.add(label)
                break
    print(prefix,'verified:',sorted(checked))

raw_disagreements=rows('Disagreements',7,200)
public_disagreements=[]
for v in raw_disagreements:
    public_disagreements.append({'id':v['Study ID'],'dimension':v['Dimension / category'],
       'firstCoder':v['First coder'],'secondCoder':v['Second coder']})
assert all(r['id'] in known for r in public_disagreements)
assert len(public_disagreements)==sum(r['disagreed'] for r in results),(len(public_disagreements),sum(r['disagreed'] for r in results))

agreement={'nStudies':61,'bootstrapResamples':10000,'status':'Pre-adjudication; aligned coding framework as supplied',
  'definition':'Observed agreement and Cohen’s kappa with percentile-bootstrap 95% confidence intervals. Multilabel dimensions are evaluated per binary category.',
  'results':results,'methodNote':'D4 uses five binary method families; each evaluation type is assessed separately. Low-prevalence evaluation categories may yield unstable kappa.',
  'source':'XAI_SER_Inter_Rater_Reliability_61_Studies_aligned.xlsx'}
(D/'agreement.json').write_text(json.dumps(agreement,ensure_ascii=False,indent=2)+'\n')
(D/'agreement_pairs.json').write_text(json.dumps(pairs_out,ensure_ascii=False,indent=2)+'\n')
(D/'agreement_disagreements.json').write_text(json.dumps(public_disagreements,ensure_ascii=False,indent=2)+'\n')

def export(name,items):
    fields=list(dict.fromkeys(k for r in items for k in r))
    with (P/f'{name}.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for row in items:
            w.writerow({k:(chr(39)+str(v)) if isinstance(v,str) and v.startswith(('=','+','-','@')) else v for k,v in row.items()})
export('coding_agreement',results)
export('coding_pairs',pairs_out)
export('coding_disagreements',public_disagreements)
print('AGREEMENT',len(primary),'study pairs;',len(results),'measurements;',len(public_disagreements),'recorded differences')
