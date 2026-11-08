"""Rebuild the public XAI-SER companion from the actual final workbooks and recorded OpenAlex export.
Dependency: artifact_tool (spreadsheet reading), Python standard library. Never infer a decision from a title.
Raw abstracts are deliberately not included in the public JSON/CSV files.
"""
from pathlib import Path
from artifact_tool import Blob, SpreadsheetFile
import csv, json, re, hashlib, collections, sys
R=Path(__file__).resolve().parents[1]
D=R/'public/data'; W=R/'public/downloads'; D.mkdir(parents=True,exist_ok=True); W.mkdir(exist_ok=True)
I=R/'data/inputs';
def save(n,obj): (D/f'{n}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf8')
def cfg(n):return json.loads((R/f'config/{n}.json').read_text())
def sheetrows(w,name,headerrow,firstrow,endrow,ncols):
    vals=w.worksheets.get_item(name).get_range_by_indexes(headerrow-1,0,endrow-headerrow+1,ncols).values
    headers=[str(a).strip() if a is not None else '' for a in vals[0]]
    for ri,row in enumerate(vals[1:],headerrow+1):
        if not any(v is not None and str(v).strip() for v in row): continue
        yield ri,{k:v for k,v in zip(headers,row) if k}
def txt(v):return '' if v is None else str(v).strip()
def public_qa_note(v):
    s=txt(v)
    # Retain criterion evidence while omitting internal revision commentary.
    return re.sub(r"^Verified on 7 Nov 2026 against the authors' version of the ICASSP paper \(arXiv:2504\.05368\)\. ", '', s)
def ids(v):return re.findall(r'M-\d{4}',txt(v))
def export(n,rows):
    if not rows:return
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with (W/f'{n}.csv').open('w',newline='',encoding='utf-8-sig') as f:
        wr=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');wr.writeheader()
        for row in rows:
            val={k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()}
            val={k:"'"+v if isinstance(v,str) and v.startswith(('=','+','-','@')) else v for k,v in val.items()}
            wr.writerow(val)
print('Reading final workbooks',flush=True)
final=SpreadsheetFile.import_xlsx(Blob.load(str(I/'Final_Included_Excluded_Studies_XAI_SER_Final.xlsx')))
qa_book=SpreadsheetFile.import_xlsx(Blob.load(str(I/'XAI_SER_QA_FullText_Final.xlsx')))
qa_fixed_book=SpreadsheetFile.import_xlsx(Blob.load(str(I/'XAI_SER_QA_Fix_Final.xlsx')))
screen_book=SpreadsheetFile.import_xlsx(Blob.load(str(I/'XAI_SER_Screening_597_Full.xlsx')))
F=lambda s,h,start,end,n:sheetrows(final,s,h,start,end,n)
q_orig={txt(v['Study ID']):(row,v) for row,v in sheetrows(qa_book,'QA',1,2,130,35) if re.fullmatch(r'M-\d{4}',txt(v.get('Study ID')))}
# The working QA sheet has only 83 assessed full texts. Nine unsuccessful retrievals
# are retained separately for the PRISMA retrieval count, not QA table/export.
not_retrieved_orig={txt(v['Study ID']):(row,v) for row,v in sheetrows(qa_book,'Not retrieved',1,2,30,35) if re.fullmatch(r'M-\d{4}',txt(v.get('Study ID')))}
assert len(q_orig)==83 and len(not_retrieved_orig)==9
assert not (set(q_orig)&set(not_retrieved_orig))
q_orig.update(not_retrieved_orig)
assert len(q_orig)==92
# The newly supplied 83-report QA workbook overrides the earlier register for
# assessed papers. Original register remains used only for 9 not-retrieved items
# and older contextual descriptors absent from the new QA workbook.
qa_fixed={txt(v['Study ID']):(row,v) for row,v in sheetrows(qa_fixed_book,'QA',4,5,100,20) if re.fullmatch(r'M-\d{4}',txt(v.get('Study ID')))}
assert len(qa_fixed)==83 and not (set(qa_fixed)&set(not_retrieved_orig))
for i,(newrow,q) in qa_fixed.items():
    assert i in q_orig,('Missing old register source',i)
    orig=dict(q_orig[i][1])
    for field,to in [('Year','Year'),('Title','Study title'),('DOI','DOI'),('Decision','Eligibility decision'),('Page / figure / table','Evidence: page / figure'),('Criterion-level justification','Criterion-level justification')]:
        if q.get(field) is not None: orig[to]=q[field]
    orig['Full-text review stage']='Assessed'
    q_orig[i]=(newrow,orig)
screen_orig={txt(v['Study ID']):(row,v) for row,v in sheetrows(screen_book,'Screening',1,2,700,29) if re.fullmatch(r'M-\d{4}',txt(v.get('Study ID')))}
screens=[]
for row,v in F('Screening 597',4,5,650,12):
    i=txt(v.get('Master ID'))
    if not re.fullmatch(r'M-\d{4}',i):continue
    meta=screen_orig.get(i,(None,{}))[1]
    screens.append({'id':i,'year':v.get('Year'),'title':v.get('Title'),'databases':v.get('Sources'),'doi':v.get('DOI'),
      'publicationType':meta.get('Document type'),'frozenDecision':meta.get('Frozen title/abstract decision'),
      'currentDecision':v.get('Title/abstract decision'),'ruleCode':meta.get('Reassessment rule ID'),
      'screeningEvidence':meta.get('Screening evidence level'),'abstractAvailable':bool(meta.get('Full abstract / supplied summary')),
      'fullTextState':v.get('Full-text decision') or 'Not advanced','source':{'file':'Final synthesis workbook','sheet':'Screening 597','row':row}})
assert len(screens)==597,len(screens)
# Recorded citation-search export retains 614 distinct OpenAlex records; many titles are missing.
alex=[]; mapping={}
with (I/'XAI_SER_OpenAlex_citation_search/records_2021_2026.csv').open(encoding='utf-8-sig',newline='') as f:
    for a in csv.DictReader(f):
        decision=a['decision'];
        if not (decision.startswith('Sought:') or decision.startswith('Excluded at title/abstract:')): continue
        oa=a['openalex_id'];d={'id':'OA-'+oa,'openalexId':oa,'year':a['year'],
            'title':a['title_if_recorded'] or 'Title not retained in the archived export',
            'databases':'OpenAlex citation searching','doi':a['doi'],'publicationType':'Not recorded',
            'currentDecision':'Full text sought' if decision.startswith('Sought:') else 'Excluded at title/abstract',
            'frozenDecision':None,'ruleCode':decision,'queryIds':a['queries'],'abstractAvailable':False,
            'fullTextState':'Not advanced','source':{'file':'OpenAlex citation search','sheet':'records_2021_2026.csv'}}
        alex.append(d);mapping[oa]=d
assert len(alex)==614,(len(alex),len(set(x['openalexId'] for x in alex)))
with (I/'XAI_SER_OpenAlex_citation_search/reports_sought.csv').open(encoding='utf-8-sig',newline='') as f:
    for v in csv.DictReader(f):
        if v['openalex_id'] in mapping:
            d=mapping[v['openalex_id']];d['id']=v['master_id'];d['title']=v['title'] or d['title'];d['fullTextState']=v['decision']
sc_all=screens+alex
assert len(sc_all)==1211 and len({r['id'] for r in sc_all})==1211
save('screening',sc_all);save('screening_source',screens);save('openalex_source',alex)
# Eligibility and report-level QA: final synthesis is the authority when QA workbooks differ.
el=[]
for row,v in F('Eligibility',4,5,140,18):
    i=txt(v.get('Master ID'))
    if not re.fullmatch(r'M-\d{4}',i):continue
    el.append({'id':i,'decision':v.get('Full-text decision'),'gate':v.get('QA v2 result'),'total':v.get('QA v2 total /7'),
        'reasonCode':v.get('Code'),'rationale':v.get('Rationale or main result'), 'locator':v.get('Page / figure / table'),
        'title':v.get('Title'),'year':v.get('Year'),'doi':v.get('DOI'),'route':v.get('Identification route'),
        'studyFamily':v.get('Study family'),'source':{'file':'Final synthesis workbook','sheet':'Eligibility','row':row}})
assert len(el)==83,len(el)
E={r['id']:r for r in el}
qa_vals={}
for row,v in F('QA',4,5,150,17):
    i=txt(v.get('Master ID'))
    if not re.fullmatch(r'M-\d{4}',i):continue
    qa_vals[i]=dict(v,sourceRow=row)
qa=[]
for i,(row,q) in q_orig.items():
    fin=E.get(i);fq=qa_vals.get(i,{})
    state=('Pending retrieval' if not fin else 'Included study' if fin['decision']=='Include' else 'Companion report' if fin['decision']=='Companion' else 'Excluded after QA' if fin['gate']=='Fail' and fin['reasonCode']=='Q' else 'Excluded at eligibility')
    score={f'Q{k}':fq.get({1:'Q1 task',2:'Q2 data',3:'Q3 protocol',4:'Q4 XAI approach',5:'Q5 XAI evidence',6:'Q6 recognition results',7:'Q7 interpretation'}[k]) for k in range(1,8)}
    # QA performance is assessed only after eligibility. Keep pre-eligibility scores out of the published QA register.
    can_score=bool(fin and fin.get('gate') in ('Pass','Fail') and fin.get('reasonCode') in ('IN','Q','COMP','CO'))
    if not can_score:score={f'Q{k}':None for k in range(1,8)}
    status='Final register, criterion-level verified' if can_score else ('No full text retrieved' if not fin else 'Eligibility exclusion; QA scores not applicable')
    row_obj={'id':i,'year':q.get('Year'),'title':q.get('Study title'),'doi':q.get('DOI'), 'state':state,
     'decision':q.get('Eligibility decision'),'finalDecision':fin.get('decision') if fin else 'Awaiting full text',
     'gate':fin.get('gate') if fin else None,'total':fin.get('total') if can_score else None,
     'reviewStatus':q.get('Full-text review stage'),'scorePublicationStatus':status,
     'reasonCode':fin.get('reasonCode') if fin else None,'reason':fin.get('rationale') if fin else None,
     'locator':fin.get('locator') if fin else q.get('Evidence: page / figure'),'finalLocator':fin.get('locator') if fin else None,
     'methods':q.get('XAI method'),'target':q.get('Explanation target'),'datasets':q.get('Corpus / datasets'),
     'setting':q.get('Input / SER setting'),'observedOutput':q.get('Observed explanation result'),
     'justification':public_qa_note(q.get('Criterion-level justification') or fq.get('Criterion-level justification')) if can_score else None,
     'limitations':q.get('Evidence limitations'),'source':{'file':'Final synthesis workbook','sheet':'QA','row':fq.get('sourceRow')} }
    row_obj.update(score);qa.append(row_obj)
assert len(qa)==92,len(qa)
qa_all=qa  # 92 sought; includes nine not retrieved, needed only for PRISMA accounting.
qa=[r for r in qa_all if r['state']!='Pending retrieval']
assert len(qa)==83 and {r['id'] for r in qa}==set(E)
assert sum(r['total'] is not None for r in qa)==65
# Scores in the supplied QA workbook must agree with the final synthesis.assert sum(r['state']=='Excluded at eligibility' for r in qa)==18
for r in qa:
    if r['total'] is not None:
        scores=[r[f'Q{k}'] for k in range(1,8)]
        assert all(x in (0,0.5,1) for x in scores),(r['id'],scores)
        assert abs(float(r['total'])-sum(scores))<.001,(r['id'],r['total'],sum(scores))
        qfix=qa_fixed[r['id']][1]
        for k in range(1,8):
            nm={1:'Q1 task',2:'Q2 data',3:'Q3 protocol',4:'Q4 XAI approach',5:'Q5 XAI evidence',6:'Q6 recognition results',7:'Q7 interpretation'}[k]
            assert float(qfix[nm])==float(r[f'Q{k}']),(r['id'],nm,qfix[nm],r[f'Q{k}'])
save('qa',qa);save('qa_source',qa);save('eligibility_source',el)
# Full extraction + taxonomy, from final included reports.
ex={}
for row,v in F('Extraction',4,5,130,20):
    i=txt(v.get('Master ID'))
    if re.fullmatch(r'M-\d{4}',i):ex[i]=v
rawtax={}
for row,v in F('Taxonomy',4,5,130,15):
    i=txt(v.get('Master ID'))
    if re.fullmatch(r'M-\d{4}',i):rawtax[i]=v
mem=[]
for row,v in F('Synthesis',4,5,300,9):
    if not v.get('Dimension') or not v.get('Category'):continue
    codes=ids(v.get('Contributing Master IDs'))
    mem.append({'dimension':v.get('Dimension'),'category':v.get('Category'),
      'reportedCount':v.get('Studies'),'ids':codes,'sourceRow':row})
for r in mem:
    assert int(r['reportedCount'])==len(set(r['ids'])),('MISMATCH',r)
save('synthesis_memberships',mem)
def memberships(dim,i):return [str(m['category']) for m in mem if m['dimension']==dim and i in m['ids']]
d1map=cfg('d1map');fam=cfg('family');corp=cfg('corpus');study=[]
for rec in el:
    if rec['decision']!='Include':continue
    i=rec['id'];a=rawtax.get(i,{});x=ex.get(i,{});s=next((p for p in sc_all if p['id']==i),{})
    methods=memberships('XAI method',i)
    if not methods: methods=[z.strip() for z in txt(a.get('D4 Implemented methods')).split(',') if z.strip()]
    data=memberships('Named corpus in evaluated pipeline',i)
    if not data: data=[z.strip() for z in txt(x.get('Corpora in evaluated pipeline')).split(',') if z.strip()]
    d1raw=txt(a.get('D1 Relation to model'));d2raw=txt(a.get('D2 Temporal evidence'))
    d2='Aggregated' if d2raw.startswith('Reported evidence summarized') else 'Unresolved' if d2raw.startswith('Temporal correspondence unresolved') else 'Localised' if ('localiz' in d2raw.lower() or 'time-preserving' in d2raw.lower()) else 'Unresolved'
    d1=d1map.get(d1raw,d1raw or 'Not coded')
    speech=txt(a.get('Speech information explained'));speech='Acoustic and lexical' if 'lexical' in speech.lower() else 'Acoustic only'
    deliveryraw=txt(a.get('Delivery format'))
    delivery='Includes audible output' if 'audio' in deliveryraw.lower() or 'audible' in deliveryraw.lower() else 'Verbal (text, cue phrases)' if deliveryraw.startswith('Text') else 'Ranked list or prose' if deliveryraw.startswith('Prose') else 'Visual (plot, map, table)'
    languages=sorted(set(q for c in data for q in (corp[c][0].split('; ') if c in corp else ['Not mapped'])))
    elicitation=sorted(set(corp[c][1] if c in corp else 'Not mapped' for c in data))
    mgroup=txt(x.get('Model group')) or 'Not supplied'
    study.append({'id':i,'title':rec['title'],'year':rec['year'],'doi':rec['doi'],'authors':None,
      'publicationType':s.get('publicationType') or memberships('Publication type',i) or 'Not supplied',
      'publicationCategory':('Journal article' if 'journal' in txt(s.get('publicationType')).lower() or txt(s.get('publicationType'))=='Article' else 'Conference paper' if 'conference' in txt(s.get('publicationType')).lower() else 'Not supplied'),
      'databases':s.get('databases') or rec['route'], 'd1':d1,'d1Raw':d1raw,'d2':d2,'d2Raw':d2raw,
      'd3':a.get('D3 Explained representation') or x.get('Explanation target'),
      'd4':sorted(f for f,aliases in fam.items() if set(methods)&set(aliases)),
      'methods':methods,'datasets':data,'languages':languages,'elicitation':elicitation,
      'model':x.get('Explained SER model / pipeline'),'modelGroup':mgroup, 'delivery':delivery,
      'speechInformation':speech,'input':a.get('Input to explained system'),
      'evaluation':memberships('Validation / sensitivity',i),'locator':x.get('PDF locator'),
      'fidelityEvidence':x.get('Fidelity test'),'stabilityEvidence':x.get('Stability / robustness'),
      'humanEvaluation':x.get('Human evaluation type'),'recognitionReported':any(r['id']==i and r['Q6'] is not None and r['Q6']>0 for r in qa),
      'source':{'file':'Final synthesis workbook','sheet':'Taxonomy'}})
assert len(study)==61,len(study)
# Publication-type metadata are incomplete for some sources; do not impute unknown classes.
assert len(study)==61
save('studies',study)
# source-specific metrics, aggregate counts from the 61 unique included study rows
c={'screened':len(sc_all),'databaseScreened':len(screens),'citationScreened':len(alex),'sought':len(qa_all),
 'databaseSought':81,'citationSought':11,'notRetrieved':len(qa_all)-len(el),'assessed':len(el),'included':len(study),
 'reportsIncluded':sum(q['gate']=='Pass' for q in qa),'companion':sum(r['decision']=='Companion' for r in el),
 'eligible':sum(q['gate'] in ('Pass','Fail') for q in qa), 'passed':sum(q['gate']=='Pass' for q in qa),
 'qaFailed':sum(q['gate']=='Fail' and q['reasonCode']=='Q' for q in qa),
 'eligibilityExcluded':sum(q['state']=='Excluded at eligibility' for q in qa),
 'posthoc':sum('Post-hoc analysis of a trained model'==s['d1'] for s in study),
 'shap':sum('SHAP' in s['methods'] for s in study),
 'aggregated':sum(s['d2']=='Aggregated' for s in study),
 'localised':sum(s['d2']=='Localised' for s in study),
 'lexical':sum(s['speechInformation']=='Acoustic and lexical' for s in study),
 'fidelity':sum('Direct prediction faithfulness' in x['evaluation'] for x in study),
 'human':sum('Human evaluation of explanations' in x['evaluation'] for x in study),
 'anyEvaluation':sum(bool(set(x['evaluation']) & {'Direct prediction faithfulness','Human evaluation of explanations','Controlled robustness of explanation or cue outputs','Repeated-run stability of explanations','Human task performance with explanation conditions','Automated scoring of generated rationales'}) for x in study),
 'pendingScreeningLabels':0,'missingOpenAlexTitles':sum('not retained' in s['title'] for s in alex)}
assert c['reportsIncluded']==62 and c['notRetrieved']==9 and c['eligible']==65 and c['qaFailed']==3,(c)
expected={'screened':1211,'assessed':83,'included':61,'passed':62,'posthoc':40,'shap':24,'aggregated':35,'localised':19,'lexical':10,'fidelity':7,'human':4,'anyEvaluation':11}
comparison=[{'metric':k,'manuscript':v,'computed':c[k],'match':v==c[k]} for k,v in expected.items()]
print('RECONCILIATION',comparison,flush=True)
# preserve dynamically defined chart choices and codebook
prev= json.loads((D/'summary.json').read_text()); charts=prev['charts']
for ch in charts:
    key=ch['key'];multi=ch['multi'];counts=collections.Counter()
    for st in study:
        raw=st.get(key)
        if multi:
            for x in set(raw if isinstance(raw,list) else [raw]):counts[str(x or 'Not supplied')]+=1
        else:counts[str(raw or 'Not supplied')]+=1
    ch['denominator']=len(study)
    ch['bars']=[{'label':v,'count':n} for v,n in (sorted(counts.items()) if key=='year' else sorted(counts.items(),key=lambda z:(-z[1],z[0])))]
issue=[{'kind':'OpenAlex metadata limitation','id':'Citation screening','detail':f"{c['missingOpenAlexTitles']} of 614 archived citation records have no recorded title, and the export does not retain abstracts. Their historical decisions cannot be independently audited from this snapshot."},
 {'kind':'Screening provenance','id':'Database records','detail':'597 database-and-archive screening records use the final register; public web exports exclude full abstracts for redistribution reasons. The source workbook retains their metadata.'},
 {'kind':'Study versus report','id':'Companion','detail':'62 passing reports represent 61 distinct studies. Companion M-0038 is merged with its journal extension and excluded from study-level counts.'}]
summary={'counts':c,'comparison':comparison,'charts':charts,'issues':issue,'snapshot':'2026-11-08'}
save('summary',summary)
# use the actual final workbook search/flow tables
search=[]
for row,v in F('Search log',4,5,40,9):
    if v.get('Source'):search.append({'database':v['Source'],'occurrences':v.get('Records (all years)'),
    'dateEvidence':v.get('Date and limits'),'query':v.get('Search string')})
save('search_log',search)
prisma=[]
for row,v in F('PRISMA',4,5,90,8):
    if v.get('Stage / unit'):prisma.append({'stage':v['Stage / unit'],'count':v.get('N'),
    'basis':v.get('Source or derivation'),'interpretation':v.get('Interpretation')})
save('prisma_source',prisma)
criteria=[]
for row,v in sheetrows(qa_fixed_book,'Criteria',4,5,16,10):
    if txt(v.get('Criterion')).startswith('Q'):criteria.append(v)
save('qa_criteria',criteria)
# Public codebook from previous version remains valid D1–D4; supplement with exact current taxonomy columns.
prov={'snapshot':'2026-11-08','sourceFiles':[], 'primaryWorkbook':'Final_Included_Excluded_Studies_XAI_SER_Final.xlsx',
 'qaWorkbook':'XAI_SER_QA_Fix_Final.xlsx','scope':'Speech-derived acoustic or linguistic evidence, or both',
 'privacy':'Abstracts and third-party full-text PDFs are not redistributed via the website.'}
for p in [I/'Final_Included_Excluded_Studies_XAI_SER_Final.xlsx',I/'XAI_SER_QA_Fix_Final.xlsx',I/'XAI_SER_Screening_597_Full.xlsx',I/'XAI_SER_OpenAlex_citation_search/records_2021_2026.csv']:
    prov['sourceFiles'].append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
save('provenance',prov)
# New exact figure images are sourced from manuscript PDF, not re-estimated from separate plot code.
figures=[{'id':f'fig{n:02}','title':title,'note':f'Exact figure crop from final manuscript, page {pg}. Consult the caption and original paper for context.','page':pg} for n,title,pg in [
 (1,'Conceptual overview',3),(2,'PRISMA selection flow',5),(3,'Four-dimensional taxonomy',7),(4,'Publication profile',10),
 (5,'Explanation–model relationship',10),(6,'Explained target and temporal resolution',11),(7,'Explanation methods',11),
 (8,'Method families by explained target',13),(9,'Explanation evaluation',13),(10,'Corpus, language and model contexts',15),(11,'Evidence gaps and research agenda',20)]]
save('figures',figures)
# Downloads generated only from public fields. Keep original sheets in data/inputs for local, controlled re-running.
for name,rows in [('screening',sc_all),('openalex_records',alex),('qa',qa),('eligibility',el),('taxonomy',study),('synthesis_memberships',mem),('prisma_source',prisma),('search_log',search),('qa_criteria',criteria)]:export(name,rows)
export('audit_trail',[{'id':s['id'],'title':s['title'],'screeningDecision':s.get('currentDecision'),'finalDecision':E.get(s['id'],{}).get('decision'),'source':s['databases']} for s in sc_all])
print('COUNTS',json.dumps(c),flush=True)
