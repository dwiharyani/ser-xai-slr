Citation searching (backward and forward) for the systematic review
"Explainable AI for Speech Emotion Recognition" - OpenAlex, run 7 November 2026

Files
  seeds.csv                Seeds and their OpenAlex IDs (57 reports of included studies, 2 closest reviews,
                           2 related preprints; M-0016 is not indexed in OpenAlex).
  queries.csv              The 40 API requests (20 backward = references of the seeds, 20 forward = works citing
                           the seeds), three seeds per request, restricted to "emotion" in title or abstract,
                           with meta.count and the number of records before and from 2021.
  responses/B01..F20.txt   Records returned by each request on 7 Nov 2026: OpenAlex ID | year | DOI | title.
                           Titles are recorded for records kept for closer screening; "x" marks records
                           excluded on their title (the title can be looked up from the OpenAlex ID or DOI).
  records_2021_2026.csv    The 702 unique records from 2021-2026 with the queries that returned them and the
                           screening decision.
  reports_sought.csv       The 11 reports sought for full text, with route, decision and QA v2 total.
  prisma_flow.csv          Counts for the PRISMA "identification via other methods" branch.
  download_openalex.py     Re-runs all 40 requests and saves the complete API responses (raw_json/) and one CSV
                           with titles, venues and authors. OpenAlex is updated continuously, so a re-run can
                           give slightly different counts; report the date of the re-run.

Screening rules
  Removed before screening: publication year before 2021; duplicate links; records already identified
  (seed or record in the database screening register, matched by DOI or normalised title); preprints and
  non-reports (arXiv, SSRN, Research Square, dataset deposits). Remaining records were screened on title and
  abstract, and reports sought were assessed with the same eligibility criteria (E1-E5) and QA v2 rubric
  as the database records.
