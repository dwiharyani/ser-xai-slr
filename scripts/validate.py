"""Fast standard-library validation for the committed public JSON snapshot."""
import json, pathlib, collections
R=pathlib.Path(__file__).resolve().parents[1];D=R/'public/data'
read=lambda n:json.loads((D/f'{n}.json').read_text())
s=read('summary');c=s['counts'];study=read('studies');screen=read('screening');qa=read('qa');fig=read('figures')
assert len(screen)==1211 and len({r['id'] for r in screen})==1211
assert len(qa)==83 and len(study)==61 and len({r['id'] for r in study})==61
assert len([r for r in qa if r['state']=='Pending retrieval'])==0
assert sum(r['total'] is not None for r in qa)==65
assert sum(r['state']=='Excluded at eligibility' for r in qa)==18
assert c['sought']==92 and c['notRetrieved']==9 and c['assessed']==83
assert sum(r['state']=='Included study' for r in qa)==61
assert sum(r['state']=='Companion report' for r in qa)==1
assert all(v['match'] for v in s['comparison'])
assert all((R/f"public/figures/paper/{f['id']}.png").exists() for f in fig)
assert not (R/'public/downloads/manuscript-v6.pdf').exists(), 'Manuscript PDF must not be published'
assert (R/'public/downloads/XAI_SER_OpenAlex_citation_search.zip').exists()
# Independent coding supplied as an aligned 61-study agreement snapshot.
a=read('agreement'); ap=read('agreement_pairs'); ad=read('agreement_disagreements')
assert a['nStudies']==61 and a['bootstrapResamples']==10000
assert len(ap)==61 and {r['id'] for r in ap}=={r['id'] for r in study}
assert len(a['results'])==14 and all(r['n']==61 and r['agreed']+r['disagreed']==61 for r in a['results'])
assert len(ad)==sum(r['disagreed'] for r in a['results'])==55
assert {r['dimension']:r['agreed'] for r in a['results']}['D1']==53
assert {r['dimension']:r['agreed'] for r in a['results']}['D2']==54
assert {r['dimension']:r['agreed'] for r in a['results']}['D3']==40
assert all(r['id'] in {x['id'] for x in study} for r in ad)
assert {r['id'] for r in qa if r['state']=='Companion report'}=={'M-0038'}
assert {r['id']:r['reasonCode'] for r in qa}['M-0038']=='CO'
for f in ('coding_agreement.csv','coding_pairs.csv','coding_disagreements.csv'):
    assert (R/'public/downloads'/f).exists()
print('VALID: 1211 screened, 92 sought (9 unavailable), 83 assessed, 65 scored, 62 passed, 61 studies, 11 figures; 61 inter-rater pairs, 14 measures, 55 disagreements.')
