# Public downloads

CSV exports are generated from the 17 November 2026 supplementary data snapshot: 1,211 screening records, 92 full-text reports sought (6 not retrieved), 86 assessed rows in `qa.csv` (66 formally scored), and a 61-study synthesis. The OpenAlex archive is provided as a separate ZIP. Source workbooks containing full abstracts and original reviewer notes are not served from this static website.

Missing OpenAlex metadata is not imputed. Figure image crops (PNG) are available in `figures/paper/`. The complete manuscript PDF is not distributed.

## Independent coding (17 November 2026)

- `coding_agreement.csv` — 14 agreement measures from the supplied aligned coding workbook (61 matched studies), with confidence intervals and counts.
- `coding_pairs.csv` — per-study first/second coder D1–D3 labels and match flags.
- `coding_disagreements.csv` — 55 category-level disagreements, without reviewers' free-text remarks.

Sanitized public workbooks `XAI_SER_First_Coder_Coding_Public.xlsx` and `XAI_SER_Second_Coder_Coding_Public.xlsx` reproduce the initial categorical coding of the 61 included studies, without evidence-locator free text, reviewer remarks or personal notes. The independently supplied blank form `XAI_SER_Second_Coder_Form.xlsx` was checked against the newer copy and is unchanged. Raw source workbooks and the aligned agreement source file are not among public downloads. Agreement values reflect initial independent coding before adjudication; synthesis charts use the revised final taxonomy.

The updated PRISMA diagram is available as `../figures/paper/fig02.png` and `../figures/paper/fig02.pdf`.

Figure 3 taxonomy diagram was updated from the supplied `fig_taxonomy(1).pdf` and is available as `../figures/paper/fig03.png` and `../figures/paper/fig03.pdf`. The Results and Coding agreement tabs were retired; coding CSV and reviewer forms remain downloadable.
