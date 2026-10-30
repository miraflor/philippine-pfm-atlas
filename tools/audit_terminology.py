"""Inventory candidate unexplained acronyms in the existing Atlas corpus.

This is a review queue, NOT a claim that listed terms are undefined or that
issuances are missing. Source codes, diagram directives, and URLs are removed.

Usage:
    python tools/audit_terminology.py --output terminology-review.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / 'src/reference/E_glossary.md'
LINEAGE = ROOT / 'src/evidence/lineage.json'
SOURCE_REG = ROOT / 'src/reference/F_sources_and_verification.md'
TOKEN = re.compile(r'(?<![A-Za-z0-9])([A-Z]{2,}[A-Z0-9]*(?:[-][A-Z0-9]+)*)(?![A-Za-z0-9])')


def known_terms():
    text = GLOSSARY.read_text(encoding='utf-8')
    abbr = text.split('## 2. Abbreviations', 1)[-1]
    known = set()
    for line in abbr.splitlines():
        if not line.startswith('|'):
            continue
        name = line.split('|')[1].strip()
        for part in name.split(','):
            part = part.strip()
            if TOKEN.fullmatch(part):
                known.add(part)
    data = json.loads(LINEAGE.read_text(encoding='utf-8'))
    for item in data['items']:
        for name in [item['name']] + item.get('aliases', []):
            if TOKEN.fullmatch(name):
                known.add(name)
    # Reference F itself is the canonical explanation of source codes.
    for line in SOURCE_REG.read_text(encoding='utf-8').splitlines():
        if not line.startswith('|'):
            continue
        code = line.split('|')[1].strip()
        if TOKEN.fullmatch(code):
            known.add(code)
    return known


def candidates():
    known = known_terms()
    found = defaultdict(lambda: {'files':set(), 'mentions':0})
    corpus = list((ROOT / 'src/chapters').glob('*.md')) + list((ROOT / 'src/reference').glob('*.md'))
    corpus.append(ROOT / 'src/00_BIG_PICTURE.md')
    for path in corpus:
        if not path.is_file() or path == GLOSSARY or path == SOURCE_REG:
            continue
        text = path.read_text(encoding='utf-8')
        text = re.sub(r'```.*?```', ' ', text, flags=re.S)
        text = re.sub(r'\{\{.*?\}\}', ' ', text, flags=re.S)
        text = re.sub(r'https?://\S+', ' ', text)
        text = re.sub(r'\[[A-Z][A-Z0-9-]*(?:[^\]]*)\]', ' ', text)
        for value in TOKEN.findall(text):
            if value in known or re.fullmatch(r'[A-Z][0-9]+',value):
                continue
            # Conservative: exclude diagram IDs and short source-like compound labels.
            found[value]['files'].add(path.relative_to(ROOT).as_posix())
            found[value]['mentions'] += 1
    return sorted(((token,meta['mentions'],len(meta['files']), '; '.join(sorted(meta['files'])[:5]))
                   for token,meta in found.items()), key=lambda r:(-r[1],r[0]))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    rows=candidates()
    if args.output:
        with args.output.open('w',encoding='utf-8',newline='') as fh:
            w=csv.writer(fh)
            w.writerow(['candidate_acronym','mentions','files','sample_paths','editorial_action'])
            for row in rows:
                w.writerow([*row,'review definition / alias / false positive'])
        print('Wrote review queue:',args.output.resolve())
    print('Candidates for human review:',len(rows))
    for item in rows[:35]:
        print('%-19s %3d mentions in %2d files' % item[:3])
    print('Caution: these are candidates, not confirmed omissions.')

if __name__=='__main__':
    main()
