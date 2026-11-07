# Data and visual validation

The source of record is `Final_Included_Excluded_Studies_XAI_SER_Final.xlsx`, supported by the current full-text QA workbook and OpenAlex archive.

The public data build verifies: 597 database/archive screened + 614 OpenAlex screened = 1,211; 92 sought, 9 not retrieved, 83 assessed, 65 QA-eligible, 62 passing reports, 61 unique studies. The 61-study synthesis yields 40 post-hoc, 24 SHAP, 35 aggregated, 19 localised, 10 acoustic+lexical, 7 fidelity, 4 human, 11 any explanation test. All 13 comparison metrics match the current manuscript.

Run `python scripts/validate.py` to verify uniqueness and referenced image/data paths. Exact Figures 1–11 are cropped from the supplied manuscript PDF; interactive charts are recalculated from the 61-study JSON.

The local environment may not have all npm tarballs available. The GitHub Actions workflow performs `npm ci`, `npm run build` and a data-integrity check on its internet-enabled runner.
