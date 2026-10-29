#!/usr/bin/env python3
"""Append hashes for restored research files without accepting changes to existing published sources."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'SOURCE_SHA256.json'

def run():
    manifest = json.loads(PATH.read_text(encoding='utf-8'))
    for field, root in [('current_corpus', 'src'), ('research_corpus', 'research_models')]:
        now = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted((ROOT / root).rglob('*')) if p.is_file()}
        before = manifest[field]
        altered = [p for p, h in before.items() if now.get(p) != h]
        if altered:
            raise ValueError('Existing source changed or missing; refusing to rewrite evidence hashes: ' + repr(altered[:10]))
        new = sorted(set(now) - set(before))
        if field == 'current_corpus' and new:
            raise ValueError('Unexpected new primary research files: ' + repr(new))
        for p in new:
            before[p] = now[p]
        manifest[field] = dict(sorted(before.items()))
        print(field, 'added', len(new), 'verified old records', len(before)-len(new))
    PATH.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')

if __name__ == '__main__': run()
