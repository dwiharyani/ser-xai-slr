# Explainable AI for Speech Emotion Recognition

**A Systematic Review and Multidimensional Taxonomy**  
Dwi Haryani · Hamdi A. Al-Jamimi · Björn W. Schuller

Research companion website for the latest manuscript snapshot (8 November 2026). The website is made with React, TypeScript and Vite, retaining the manuscript-inspired forest green, sage, warm brown and cream palette. Figures 1–11 were extracted from the manuscript provided for the research snapshot. The full manuscript PDF is not distributed through this website.

## Study-flow snapshot

| Unit | Records/reports/studies |
|---|---:|
| Unique screening records from databases and archives | 597 |
| Records screened from OpenAlex citation searching | 614 |
| **Total records screened** | **1,211** |
| Full-text reports sought (81 + 11) | 92 |
| Full-text reports not retrieved (4 + 5) | 9 |
| **Full-text reports assessed (77 + 6)** | **83** |
| Excluded at eligibility | 18 |
| Eligible reports appraised with QA | 65 |
| Below QA gate | 3 |
| **Reports passing QA** | **62** |
| **Unique studies included in synthesis** | **61** |

The 62 passing reports comprise 61 unique studies plus one companion report of the same underlying study. Figures and synthesis always use the 61-study denominator. These counts are verified from the updated source registers, not manually substituted into the website. The 61-study synthesis includes five new studies found in OpenAlex citation searching.

## Run locally

Install Node.js 22 or later:

```bash
npm ci
npm run dev
```

Open the local URL shown by Vite (typically `http://localhost:5173`). The website uses version-controlled JSON snapshots, so Python or the original XLSX workbooks are **not** required to browse or build it.

To build the GitHub Pages site:

```bash
npm run build
```

To validate the scientific snapshot (standard Python 3, no third-party Python packages):

```bash
python scripts/validate.py
```

## Data sources and rebuilding

- `data/inputs/Final_Included_Excluded_Studies_XAI_SER_Final.xlsx`: authoritative final decisions, QA criteria and study-level synthesis.
- `data/inputs/XAI_SER_QA_Fix_Final.xlsx`: updated 83-report assessed full-text/QA register, used for the public QA page.
- `data/inputs/XAI_SER_QA_FullText_Final.xlsx`: earlier register retained solely to preserve 9 not-retrieved report identifiers and ancillary fields.
- `data/inputs/XAI_SER_Screening_597_Full.xlsx`: detailed original screening metadata and abstracts.
- `data/inputs/XAI_SER_OpenAlex_citation_search/`: recorded OpenAlex queries, seed reports, CSV exports and query logs.
- `public/data/`: derived, versioned, structured JSON actually loaded by the website.
- `public/downloads/`: public CSV exports of website fields and the original citation-search ZIP; no manuscript PDF is served.
- `public/figures/paper/`: direct PNG crops of Figures 1–11 from the latest PDF.

The optional converter `scripts/rebuild_latest.py` reads the four source XLSX files using `artifact_tool` in an environment where that library is available. Its outputs are committed in `public/data` and `public/downloads`, so GitHub Actions does **not** need the spreadsheet converter. `scripts/extract_manuscript_figures.py` requires PyMuPDF only if regenerating image crops; the resulting images are committed.

The Coding Agreement page uses 61 paired coding records and 14 Cohen’s κ measures from the user-supplied aligned workbook. Public downloads contain only numerical coding summaries and category-level differences, without raw reviewer remarks; to rebuild these agreement snapshots offline, use `python scripts/build_agreement.py /local/path/to/XAI_SER_Inter_Rater_Reliability_61_Studies_aligned.xlsx`. The original second-coder and aligned workbooks are deliberately not added to this publicly shareable repository package.

**Public-release review:** Workbooks under `data/inputs/` include original abstracts and full-text reviewer extraction notes. The website intentionally excludes full abstracts and third-party PDF articles. Before making the repository public, check rights and institutional permissions for redistributing the source workbooks; remove originals if necessary. The website continues to work from the committed public JSON/CSV snapshots.

## Data integrity limits

The database/archive register has 597 detailed records; the OpenAlex archival CSV contains 614 screened records, but **453 lack recorded titles and none retain abstracts**. These cannot be independently re-screened from the current export. The website flags missing metadata rather than reconstructing it. 

Recorded QA is *reporting-quality appraisal*, not proof that an explanation is faithful. The study codes D1–D4 concern explanations, whereas corpus, language, elicitation and model architecture remain contextual attributes.

## GitHub Pages

1. Create a repository on GitHub (for example, `xai-ser-review`).
2. Upload the **contents** of this directory into its root on the `main` branch, including `.github/workflows/pages.yml`.
3. Under **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
4. Push changes to `main`. The workflow builds Vite and deploys the `dist` artifact.

**This ZIP is a repository template, not a live published website.** The author must publish it through their GitHub account.

## Scope

The review includes explainable emotion recognition from spoken audio, transcripts originating from the same speech, or both. A model using visual or physiological signals is eligible only when the speech-derived explanatory evidence can be separately identified.
