#!/usr/bin/env python3
"""Independently hash-check the full source and raw-URL preservation manifest."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
manifest_path=ROOT/'preservation/MANIFEST.json'
if not manifest_path.is_file():
    raise SystemExit('Preservation missing. Run python tools/preserve_prior_assets.py before publishing.')
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
if manifest['prior_commit']!='092f0e7d3f59fcef684d086509c453c3fefc738e':
    raise SystemExit('Unexpected historical baseline')
for entry in manifest['files']:
    p=ROOT/entry['file']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:
        raise SystemExit('Preserved file missing or changed: '+entry['file'])
counts=manifest['counts']
if counts['research_sources_restored']<90 or counts['legacy_raw_urls']<180 or counts['original_atlas_sources']<100:
    raise SystemExit('Recovery incomplete: '+str(counts))
index=json.loads((ROOT/'research_models/supplemental_index.json').read_text(encoding='utf-8'))
if len(index)!=25:
    raise SystemExit('Full supplementary research index missing')
for item in index:
    if not (ROOT/'research_models'/item['path']).is_file():
        raise SystemExit('Research sketch missing: '+item['id'])
for letter in ('K','L'):
    if not list((ROOT/'research_models/reference').glob(letter+'_*.md')):
        raise SystemExit('Research reference '+letter+' missing')
for item in index:
    assert (ROOT/'docs/models'/('model-'+item['id']+'.html')).exists(), item['id']
print('OK: complete original source snapshot, full research corpus, and historic raw-file aliases')
print('Recovered assets:',counts,'checksum entries:',len(manifest['files']))
