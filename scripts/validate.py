"""Fast standard-library validation for the committed public JSON snapshot."""
import json, pathlib, collections
R=pathlib.Path(__file__).resolve().parents[1];D=R/'public/data'
read=lambda n:json.loads((D/f'{n}.json').read_text())
s=read('summary');c=s['counts'];study=read('studies');screen=read('screening');qa=read('qa');fig=read('figures')
assert len(screen)==1211 and len({r['id'] for r in screen})==1211
assert len(qa)==92 and len(study)==61 and len({r['id'] for r in study})==61
assert len([r for r in qa if r['state']=='Pending retrieval'])==9
assert sum(r['state']=='Included study' for r in qa)==61
assert sum(r['state']=='Companion report' for r in qa)==1
assert all(v['match'] for v in s['comparison'])
assert all((R/f"public/figures/paper/{f['id']}.png").exists() for f in fig)
assert not (R/'public/downloads/manuscript-v6.pdf').exists(), 'Manuscript PDF must not be published'
assert (R/'public/downloads/XAI_SER_OpenAlex_citation_search.zip').exists()
print('VALID: 1211 screening, 92 reports sought, 83 assessed, 62 passing reports, 61 studies; 11 manuscript figures.')
