# Public downloads

CSV exports are generated from the final 2026-11-07 data snapshot: 1,211 screening records, 92 full-text reports sought (9 not retrieved), 83 assessed rows in `qa.csv` (65 formally scored), and a 61-study synthesis. The OpenAlex archive is provided as a separate ZIP. Source workbooks containing full abstracts and original reviewer notes are not served from this static website.

Missing OpenAlex metadata is not imputed. Figure image crops (PNG) are available in `figures/paper/`. The complete manuscript PDF is not distributed.

## Independent coding (8 November 2026)

- `coding_agreement.csv` — 14 agreement measures from the supplied aligned coding workbook (61 matched studies), with confidence intervals and counts.
- `coding_pairs.csv` — per-study first/second coder D1–D3 labels and match flags.
- `coding_disagreements.csv` — 55 category-level disagreements, without reviewers' free-text remarks.

The full second-coder and aligned agreement source workbooks are not included among public downloads. The values reflect pre-adjudication coding; the first-coder taxonomy remains the input for synthesis charts.
