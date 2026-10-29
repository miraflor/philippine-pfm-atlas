#!/usr/bin/env python3
"""Check the integrity of the sources and of the parts of the website that build_extensions.py writes.
This complements tools/validate_site.py; it is not a legal or live-interface verification.

    python3 tools/validate_consolidated.py            # check
    python3 tools/validate_consolidated.py --update   # write SOURCE_SHA256.json again, after a deliberate change of the sources

SOURCE_SHA256.json holds the SHA-256 digest of every file in src/ and in research_models/. A change of a source that
was not made on purpose shows here as a difference.
"""
import hashlib, json, sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]; DOCS = ROOT / 'docs'; issues = []
MANIFEST = ROOT / 'SOURCE_SHA256.json'


def check(condition, message):
    if not condition:
        issues.append(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def corpus(folder):
    return {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted((ROOT / folder).rglob('*')) if p.is_file()}


if '--update' in sys.argv[1:]:
    MANIFEST.write_text(json.dumps({'current_corpus': corpus('src'), 'research_corpus': corpus('research_models')},
                                   indent=1) + '\n', encoding='utf-8')
    print('SOURCE_SHA256.json written')
    sys.exit(0)

manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
for key, folder in (('current_corpus', 'src'), ('research_corpus', 'research_models')):
    now = corpus(folder)
    for rel, expected in manifest[key].items():
        check(rel in now and now[rel] == expected, f'source altered or missing: {rel}')
    for rel in sorted(set(now) - set(manifest[key])):
        issues.append(f'source not in SOURCE_SHA256.json: {rel}')

guides = json.loads((ROOT / 'content/guides/index.json').read_text(encoding='utf-8'))
check(len(guides) == 8, 'expected eight lessons')
check((DOCS / 'walkthrough.html').is_file(), 'walkthrough missing')
for g in guides:
    path = DOCS / 'guide' / (g['slug'] + '.html')
    check(path.exists(), 'missing lesson ' + g['slug'])
    if path.exists():
        soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
        for did in g['diagram_ids']:
            check(bool(soup.find('a', href='../diagrams/' + did + '.html')), f'{g["slug"]} no diagram {did}')
        for pid in g['chapters']:
            check(bool(soup.find('a', href='../chapters/' + pid + '.html')), f'{g["slug"]} no chapter {pid}')

models = json.loads((ROOT / 'research_models/models_index.json').read_text(encoding='utf-8'))
check([m['id'] for m in models] == ['RM-%d' % i for i in range(1, len(models) + 1)], 'research models are not RM-1 to RM-n')
current = {p.name.split('_')[0] for p in (ROOT / 'src/diagrams').rglob('*') if p.is_file()}
for item in models:
    check(item['id'] not in current, f'research model ID {item["id"]} is also a diagram of the atlas')
    check(bool(item.get('purpose')) and bool(item.get('not_in_a_chapter')), f'research model {item["id"]} has no note')
    path = ROOT / 'research_models' / item['path']; mirror = DOCS / 'models' / item['path']
    page = DOCS / 'models' / (item['id'] + '.html')
    check(path.exists() and mirror.exists() and page.exists(), f'missing source or page {item["id"]}')
    if path.exists() and mirror.exists():
        check(digest(path) == digest(mirror), f'research model changed in the published copy {item["id"]}')
for letter in 'hij':
    check((DOCS / 'models/reference' / f'{letter}.html').is_file(), f'research reference {letter} missing')
for csvname in ['event_register.csv', 'record_type_register.csv', 'authority_register.csv', 'control_rule_register.csv',
                'interface_evidence_register.csv', 'interface_register.csv']:
    check((DOCS / 'models/registers' / csvname).is_file(), f'missing register {csvname}')
    check((DOCS / 'models' / csvname.replace('_', '-').removesuffix('.csv')).with_suffix('.html').is_file(),
          f'missing register page {csvname}')
check((DOCS / 'overview.html').is_file(), 'missing address overview.html')
forwarding = [p for p in DOCS.rglob('*.html') if 'location.replace(' in p.read_text(encoding='utf-8')]
for path in forwarding:
    check('<meta name="robots" content="noindex">' in path.read_text(encoding='utf-8'),
          f'forwarding page without noindex: {path.relative_to(DOCS)}')
search = json.loads((DOCS / 'assets/search-index.json').read_text(encoding='utf-8'))
urls = {x['u'].split('#')[0] for x in search}
for key in ['walkthrough.html', 'systems.html', 'models/index.html']:
    check(key in urls, f'missing in search: {key}')
for item in models:
    check('models/' + item['id'] + '.html' in urls, f'model not searchable {item["id"]}')
for item in guides:
    check('guide/' + item['slug'] + '.html' in urls, f'lesson not searchable {item["slug"]}')
for path in forwarding:
    check(path.relative_to(DOCS).as_posix() not in urls, f'forwarding page in the search index: {path.relative_to(DOCS)}')
print('Consolidated checks: sources:', len(manifest['current_corpus']), 'research sources:', len(manifest['research_corpus']),
      'guides:', len(guides), 'research models:', len(models), 'forwarding pages:', len(forwarding),
      'search entries:', len(search))
print('Issues:', len(issues))
for msg in issues:
    print(' -', msg)
sys.exit(bool(issues))
