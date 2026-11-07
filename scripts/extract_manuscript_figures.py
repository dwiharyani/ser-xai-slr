"""Exact figure crops from the supplied manuscript PDF (page geometry 612 x 792 pt)."""
import fitz,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
pdf=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'public/downloads/manuscript-v6.pdf'
out=ROOT/'public/figures/paper';out.mkdir(parents=True,exist_ok=True)
doc=fitz.open(pdf)
# n: (zero-indexed page, x0,y0,x1,y1) ; crop deliberately ends before caption.
rects={
1:(2,48,52,565,355), 2:(4,48,40,564,461), 3:(6,48,40,565,388),
4:(9,48,52,564,265),5:(9,48,290,564,563),
6:(10,48,56,563,255),7:(10,308,288,565,556),
8:(12,48,54,564,261),9:(12,48,296,564,490),
10:(14,48,54,564,397),11:(19,48,53,565,417)}
for n,(p,x0,y0,x1,y1) in rects.items():
    page=doc[p]
    clip=fitz.Rect(x0,y0,x1,y1)
    page.get_pixmap(matrix=fitz.Matrix(2.1,2.1),clip=clip,alpha=False).save(out/f'fig{n:02}.png')
doc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(out/'manuscript-page1.png')
print(f'Extracted {len(rects)} figures and manuscript preview from {pdf.name}')
