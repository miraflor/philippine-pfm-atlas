"""Check evidence lineage catalogue and, optionally, the built site/search index.

Run after python tools/build_atlas.py and python tools/build_site.py.
"""
from __future__ import annotations

import json
from pathlib import Path
from evidence_catalogue import validate

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'src/evidence/lineage.json').read_text(encoding='utf-8'))
validate(data)
ids = {e['id'] for e in data['items']}
for e in data['links']:
    assert e['from'] in ids and e['to'] in ids
assert any('SAAODB' in e.get('aliases', []) and e['id']=='far-1' for e in data['items'])
assert any(e['id']=='far-family' and 'FAR' in e['aliases'] for e in data['items'])
assert any(e['id']=='bfar-family' and 'BFAR' in e['aliases'] for e in data['items'])

page = ROOT / 'docs/evidence.html'
idx = ROOT / 'docs/assets/search-index.json'
if not page.exists() or not idx.exists():
    raise SystemExit('Build the website first: python tools/build_site.py')
html = page.read_text(encoding='utf-8')
for node in data['items']:
    assert 'id="item-' + node['id'] + '"' in html, node['id']
search = json.loads(idx.read_text(encoding='utf-8'))
for query, canonical in [('SAAODB','far-1'),('FAR No. 1','far-1'),('FAR 1C','far-1c'),('BFAR','bfar-family'),('COA 94-013','coa-94-013'),('LDDAP-ADA','lddap-ada')]:
    expected = 'evidence.html#item-' + canonical
    assert any(e['u'] == expected and query.casefold() in (e['t'] + ' ' + e['x']).casefold() for e in search), (query,expected)
print('Evidence catalogue: %d items, %d links; aliases, anchors, search passed.' % (len(data['items']),len(data['links'])))
