## 17 November 2026 — Supplementary data reconciliation (86 assessed reports)

- Synchronized the 597-record database screening, full-text/QA, final taxonomy and 61-study agreement outputs with the newly supplied four-workbook supplementary archive.
- Report retrieval revised from 92 sought / 9 unavailable / 83 assessed to 92 sought / 6 unavailable / 86 assessed. Three newly assessed reports: M-0027 (below QA threshold), M-0745 and M-0809 (eligibility exclusions).
- Updated QA table and CSV to 86 assessed reports: 20 eligibility exclusions and 66 QA-appraised reports (62 pass, 4 fail). The 61 independent studies and one companion report are unchanged.
- Recalculated study-level graphs from revised taxonomy and evaluation coding, including D1 post-hoc 34, D2 aggregated 40, decision fidelity 6, and any evaluation test 9.
- Regenerated agreement and coding-disagreement exports from the supplied current 61-study workbook; 14 agreement measures and 55 category-level disagreements. Agreement reflects initial coding before adjudication, whereas synthesis uses the revised taxonomy.
- Preserved manuscript Figures 1–11 without replacement. The earlier Figure 2 depicts an older assessment snapshot; the live PRISMA cards and table provide current counts.
- The supplied Eligibility table has two total-score discrepancies relative to the criterion-level QA rows: M-0016 (7 vs 6.5) and M-0106 (6.5 vs 6). Public QA uses the criterion sums while the original source workbook is left unchanged.
- Updated UI descriptions and CSV exports; no full abstracts, reviewer notes, or manuscript PDF added to public website assets.

## 8 November 2026 — Source register and agreement synchronization

- Rebuilt screening from the latest 597-record screening workbook, preserving all existing OpenAlex records.
- Rebuilt 83 full-text assessment rows from the updated QA workbook; retained nine not-retrieved identifiers from the earlier register.
- Adopted the final synthesis workbook’s companion code `CO` for M-0038 without increasing the 61 unique studies.
- Added interactive Coding Agreement page and CSV exports from the supplied aligned 61-study, 10,000-bootstrap workbook (14 agreement measures; 55 category-level disagreements).
- Included only derived agreement data in the public package; second-coder remarks and full source agreement workbooks remain offline.
- Kept Figures 1–11 and original site design unchanged. Manuscript PDF and links remain omitted.

## 2026-11-07 — QA register and full-text denominator
- The QA sheet and public table now list 83 full-text-assessed reports; nine unretrieved reports are tracked separately for PRISMA.
- QA scores apply to 65 eligible reports, with 18 eligibility exclusions retaining their full-text decisions but no Q1–Q7 score.
- Reconciled criterion scores with the final synthesis workbook.

# Release changes

## v1.1.0 — 7 November 2026

- Updated primary study-level source to final 61-study / 62-report workbook.
- Added 614 OpenAlex citation-screening records alongside 597 existing database/archive records.
- Updated report-level QA to 92 reports sought (83 assessed, nine unavailable), with current Q1–Q7 and 61 included distinct studies.
- Reconciled metrics: SHAP 24, post-hoc 40, aggregated 35, localised 19, acoustic+lexical 10 and any explanation test 11.
- Replaced old plot assets with exact cropped images of Figures 1–11 from the latest 29-page paper, and updated manuscript download.
- Corrected source/PRISMA/QA website descriptions and provided the original OpenAlex export as a download.
- Maintained forest-green/sage/brown/cream visual palette.
- Updated independent second-coder form to 61 blank study rows.
- Documented 453 missing OpenAlex titles and absent abstracts.

## v1.0.0 — previous snapshot

Original companion based on 597 screening records and 56 included studies, now superseded.

## Website display cleanup (7 November 2026)

- Reproducibility page: removed public manuscript card, known-evidence-limitations card, local rebuild instructions, reconciliation table, and known-limits panel.
- Renamed public display labels “QA v2” to “QA” where used as page headings and download labels; QA source records and score criteria are unchanged.
- Removed `public/downloads/limitations.md` to retire the former direct download URL. `docs/limitations.md` remains in the Git repository as an audit note.
- No counts, Study IDs, screening decisions, taxonomy categories, or research figures were modified.

## Website presentation and manuscript access — 7 November 2026
- Removed manuscript PDF links from the home hero and navigation header.
- Removed the manuscript PDF from the publicly served assets and removed the corresponding existence requirement from validation.
- Removed editorial QA revision notes from the website; numerical QA scores and inclusion decisions are unchanged.
- All eleven figure PNGs, tables, and download datasets remain available.

## 17 November 2026 — taxonomy correction and navigation cleanup
- Updated Figure 3 using the author-supplied `fig_taxonomy(1).pdf` (original vector and high-resolution PNG); Figure 2 PRISMA update retained.
- Removed Results and Coding agreement navigation tabs and page content; no changes to QA, screening, taxonomy data, or coding agreement source files.
- Moved all 11 downloadable research figures into Reproducibility to preserve access while removing Results.
- Verified latest second-coder form matched existing version byte for byte; no duplicate was added.
