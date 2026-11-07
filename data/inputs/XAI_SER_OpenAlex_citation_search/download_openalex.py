"""Re-download the 40 OpenAlex citation-search queries as raw JSON and as CSV.

Usage:  python download_openalex.py            (needs Python 3.8+, no extra packages)
Output: raw_json/<query>.json  (complete API responses, all pages)
        openalex_records_all_queries.csv  (one row per record per query)

OpenAlex is updated continuously, so counts may differ slightly from the run of 7 November 2026
recorded in queries.csv. Report the date of any re-run.
"""
import csv, json, os, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'raw_json'); os.makedirs(OUT, exist_ok=True)
SELECT = 'id,doi,display_name,publication_year,type,primary_location,authorships'

def get(url):
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'citation-search-replication'}), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(2 * (attempt + 1)); last = e
    raise last

rows = []
with open(os.path.join(HERE, 'queries.csv'), newline='', encoding='utf-8') as f:
    queries = list(csv.DictReader(f))
for q in queries:
    kind = 'cited_by' if q['direction'].startswith('backward') else 'cites'
    flt = f"{kind}:{q['openalex_ids'].replace(' | ', '|')},title_and_abstract.search:emotion"
    cursor, pages, results = '*', [], []
    while cursor:
        url = 'https://api.openalex.org/works?' + urllib.parse.urlencode(
            {'filter': flt, 'per_page': 200, 'cursor': cursor, 'select': SELECT})
        d = get(url); pages.append(d); results += d['results']
        cursor = d['meta'].get('next_cursor') if d['results'] else None
        time.sleep(0.2)
    json.dump({'query': q['query'], 'filter': flt, 'retrieved': time.strftime('%Y-%m-%d'), 'meta_count': pages[0]['meta']['count'],
               'results': results}, open(os.path.join(OUT, q['query'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for w in results:
        loc = (w.get('primary_location') or {}).get('source') or {}
        rows.append({'query': q['query'], 'direction': q['direction'], 'openalex_id': w['id'].rsplit('/', 1)[-1],
                     'year': w.get('publication_year'), 'type': w.get('type'), 'doi': (w.get('doi') or '').replace('https://doi.org/', ''),
                     'title': w.get('display_name'), 'venue': loc.get('display_name'),
                     'authors': '; '.join(a['author']['display_name'] for a in w.get('authorships', []) if a.get('author'))})
    print(q['query'], 'meta.count =', pages[0]['meta']['count'], 'retrieved =', len(results))
with open(os.path.join(HERE, 'openalex_records_all_queries.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('done:', len(rows), 'rows')
