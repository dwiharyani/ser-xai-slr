#!/usr/bin/env python3
"""Remove visual research figures from the Reproducibility route only.

The PRISMA image in Methodology and the taxonomy figures remain unchanged.
Safe to run repeatedly against old/new XAI-SER App.tsx versions.
"""
from pathlib import Path

source = Path(__file__).resolve().parents[1] / 'src' / 'App.tsx'
if not source.exists():
    raise SystemExit(f'ERROR: Cannot find {source}. Run from the XAI-SER repository.')
text = source.read_text(encoding='utf-8')
start = text.find('function Downloads(')
if start == -1:
    raise SystemExit('ERROR: Downloads component not found; no changes made.')
ends = [p for marker in ('\nconst pageFromHash', '\nexport default function App')
        if (p := text.find(marker, start + 1)) != -1]
if not ends:
    raise SystemExit('ERROR: Cannot locate the end of Downloads component; no changes made.')
end = min(ends)
replacement = '''function Downloads(){return <>
 <Head eyebrow="Reproducibility materials" title="Research data and documentation">Access screening, quality assessment, taxonomy, PRISMA sources, and search logs for the 61-study synthesis. No third-party article PDFs or full abstracts are published through the site.</Head>
 <div className="download-list">{downloadItems.map(([file,title,type,description])=><a href={asset(`downloads/${file}`)} download key={file}><span className="file-type">{type}</span><span><strong>{title}</strong><small>{description}</small></span><span aria-hidden="true">↓</span></a>)}</div>
 </>}
'''
new_text = text[:start] + replacement + text[end:]
new_text = new_text.replace('<Downloads data={data}/>', '<Downloads/>')
check_start = new_text.find('function Downloads(')
check_end = min(x for x in [new_text.find('\nconst pageFromHash',check_start),new_text.find('\nexport default function App',check_start)] if x!=-1)
block = new_text[check_start:check_end]
if any(item in block for item in ('Research figures', 'figure-gallery','<img', 'data.figures', 'taxonomy-figure-grid')):
    raise SystemExit('ERROR: Figure content remains inside Downloads; no changes made.')
if 'function Taxonomy' not in new_text or 'function Methodology' not in new_text:
    raise SystemExit('ERROR: Main website structure differs unexpectedly; no changes made.')
if new_text != text:
    source.write_text(new_text,encoding='utf-8')
    print('UPDATED: Reproducibility now contains only research data and documentation downloads.')
else:
    print('ALREADY CLEAN: Reproducibility has no Research figures gallery.')
print('SAFE: Taxonomy and Methodology figure components were not modified.')
