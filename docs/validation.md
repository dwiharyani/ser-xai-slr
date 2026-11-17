# Data and visual validation

The source of record is `Final_Included_Excluded_Studies_XAI_SER_Final.xlsx`, supported by the current full-text QA workbook and OpenAlex archive.

The public data build verifies: 597 database/archive screened + 614 OpenAlex screened = 1,211; 92 sought, 6 not retrieved, 86 assessed, 66 QA-eligible, 62 passing reports, 61 unique studies. The 61-study synthesis yields 34 post-hoc, 24 SHAP, 40 aggregated, 19 localised, 10 acoustic+lexical, 6 fidelity, 4 human, 9 any explanation test. All source-register checks use the revised supplementary snapshot; previously extracted manuscript figures remain unchanged.

Run `python scripts/validate.py` to verify uniqueness and referenced image/data paths. Exact Figures 1–11 are cropped from the supplied manuscript PDF; interactive charts are recalculated from the 61-study JSON.

The local environment may not have all npm tarballs available. The GitHub Actions workflow performs `npm ci`, `npm run build` and a data-integrity check on its internet-enabled runner.
