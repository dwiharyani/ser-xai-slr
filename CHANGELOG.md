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
