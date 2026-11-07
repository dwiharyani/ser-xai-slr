# Data dictionary — public release

- `screening.json`: 1,211 objects (`id`, year, title if archived, DOI, source, title/abstract decision, report status and source). Database records use M-XXXX. OpenAlex records without associated full-text IDs use OA-W... . All records have unique IDs.
- `qa.json`: 83 full-text reports assessed; `state` records inclusion, QA exclusion, eligibility exclusion and companion. Nine reports not retrieved are tracked in PRISMA counts but excluded from this QA register. `total` is present only where report is appraised following eligibility; Q1–Q7 scores come from final synthesis workbook.
- `eligibility_source.json`: 83 full-text decisions with evidence locations and primary reason codes.
- `studies.json`: 61 unique included studies; each has `d1`, `d2`, `d3`, `d4`, `delivery`, `speechInformation`, method names, reported model, dataset contexts and explanation-evaluation codes.
- `synthesis_memberships.json`: ID lists behind each synthesis-category count.
- `openalex_source.json`: 614 screened citation-search records; titles not archived in 453 and abstracts not present in this export.
- `prisma_source.json`: recorded counts and provenance for the PRISMA flow.
- `search_log.json`: recorded database search metadata.
- `figures.json`: 11 exact manuscript-image crops (file names `fig01.png` ... `fig11.png`).

Null means unknown/not documented, not a negative result. A citation-search record title is explicitly marked unavailable rather than generated. Full abstracts and third-party PDF articles are not served as website content.
