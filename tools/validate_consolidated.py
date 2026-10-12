#!/usr/bin/env python3
"""Check reconciliation and source integrity of the consolidated website.
This complements tools/validate_site.py; it is not a legal or live-interface verification.
"""
import csv, hashlib, json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'; issues=[]
def check(condition,message):
    if not condition:issues.append(message)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'SOURCE_SHA256.json').read_text(encoding='utf-8'))
for rel,expected in manifest['current_corpus'].items():
    p=ROOT/rel
    check(p.is_file() and digest(p)==expected,f'current source altered: {rel}')
for rel,expected in manifest['historical_corpus'].items():
    p=ROOT/rel
    check(p.is_file() and digest(p)==expected,f'archival source altered: {rel}')

guides=json.loads((ROOT/'content/guides/index.json').read_text(encoding='utf-8'))
check(len(guides)==8,'expected eight lessons')
check((DOCS/'walkthrough.html').is_file(),'walkthrough missing')
for g in guides:
    path=DOCS/'guide'/(g['slug']+'.html')
    check(path.exists(),'missing lesson '+g['slug'])
    if path.exists():
        soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
        for did in g['diagram_ids']:check(bool(soup.find('a',href='../diagrams/'+did+'.html')),f'{g["slug"]} no diagram {did}')

models=json.loads((ROOT/'research_models/supplemental_index.json').read_text(encoding='utf-8'))
check(len(models)==25,'expected 25 supplemental models')
check(sum(x['kind']=='mermaid' for x in models)==20,'expected 20 extra Mermaid')
check(sum(x['kind']=='plantuml' for x in models)==5,'expected 5 extra PlantUML')
original={p.name for p in (ROOT/'src/diagrams').rglob('*') if p.is_file()}
check(not any(x['filename'] in original for x in models),'supplemental name overwrites current diagram')
for item in models:
    path=ROOT/'research_models'/item['path']
    mirror=DOCS/'models'/item['path']
    page=DOCS/'models'/('model-'+item['id']+'.html')
    check(path.exists() and mirror.exists() and page.exists(),f'missing source or viewer {item["id"]}')
    if path.exists() and mirror.exists():check(digest(path)==digest(mirror),f'archival diagram changed in publish copy {item["id"]}')
for suffix in 'hijkl':check((DOCS/'models/reference'/f'{suffix}.html').is_file(),f'research reference {suffix} missing')
for csvname in ['event_register.csv','record_type_register.csv','authority_register.csv','control_rule_register.csv','interface_evidence_register.csv','interface_register.csv']:
    check((DOCS/'models/registers'/csvname).is_file(),f'missing archived register {csvname}')
    check((DOCS/'models'/csvname.replace('_','-').removesuffix('.csv')).with_suffix('.html').is_file(),f'missing register overview {csvname}')
for old in ['overview.html']:
    check((DOCS/old).is_file(),f'missing compat URL {old}')
for path in list((DOCS/'processes').glob('*.html'))+list((DOCS/'reference').glob('*_*.html')):
    check('location.replace' in path.read_text(encoding='utf-8'),f'not a redirect: {path}')
search=json.loads((DOCS/'assets/search-index.json').read_text(encoding='utf-8'))
urls={x['u'].split('#')[0] for x in search}
for key in ['walkthrough.html','systems.html','models/index.html']:
    check(key in urls,f'missing in search: {key}')
for item in models:check('models/model-'+item['id']+'.html' in urls,f'model not searchable {item["id"]}')
for item in guides:check('guide/'+item['slug']+'.html' in urls,f'lesson not searchable {item["slug"]}')
print('Consolidated checks: current source:',len(manifest['current_corpus']),'archived source:',len(manifest['historical_corpus']), 'guides:',len(guides),'model pages:',len(models),'search entries:',len(search))
print('Issues:',len(issues))
for msg in issues:print(' -',msg)
sys.exit(bool(issues))
