#!/usr/bin/env python3
"""Restore source-only analytical material and raw URL aliases from the pre-migration Git commit.

Requires a local Git repository retaining the original commit. Does not contact the network.
Never modifies existing current research-model files or public chapter files.
Run after overlaying the new chapter corpus and before building the site:
  python tools/preserve_prior_assets.py
The restored source files and aliases must be committed alongside the reorganized corpus.
"""
from __future__ import annotations
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = '092f0e7d3f59fcef684d086509c453c3fefc738e'
ROOTS = ('src', 'research_models', 'docs/atlas', 'docs/models')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, stderr=subprocess.PIPE)


def restore(base=BASE):
    actual = git('rev-parse', base + '^{commit}').decode().strip()
    if actual != base:
        raise ValueError('The original budget-cycle commit is not available locally')
    # One local Git archive is both faster and less error-prone than hundreds of git show calls on Windows.
    available = []
    for item in ROOTS:
        try:
            git('cat-file', '-e', base + ':' + item)
            available.append(item)
        except subprocess.CalledProcessError:
            pass
    archive = git('archive', '--format=tar', base, *available)
    stats = {'research_sources_restored': 0, 'original_research_snapshots': 0,
             'original_atlas_sources': 0, 'legacy_raw_urls': 0}
    records = []
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as tar:
        for member in tar:
            if not member.isfile():
                continue
            name = member.name.replace('\\', '/')
            if name.startswith('/') or '..' in Path(name).parts:
                raise ValueError('Unsafe archive member: ' + name)
            data = tar.extractfile(member).read()
            targets = []
            if name.startswith('research_models/'):
                # Same-path originals that differ are kept as a snapshot, not used to overwrite revised data.
                path = ROOT / name
                if not path.is_file():
                    targets.append(('research_sources_restored', path))
                elif path.read_bytes() != data:
                    targets.append(('original_research_snapshots', ROOT / 'preservation' / 'prior_research' / name))
            if name.startswith('src/'):
                targets.append(('original_atlas_sources', ROOT / 'preservation' / 'prior_sources' / name))
            if name.startswith('docs/atlas/') or name.startswith('docs/models/'):
                # Only raw historic assets; old HTML pages already have explicit forwarding pages.
                if Path(name).suffix.lower() in ('.md', '.mmd', '.puml', '.png', '.svg', '.csv', '.json', '.txt'):
                    targets.append(('legacy_raw_urls', ROOT / 'preservation' / 'legacy_web' / name.removeprefix('docs/')))
            for kind, target in targets:
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists() and target.read_bytes() != data:
                    raise ValueError('Preserved file changed: ' + str(target.relative_to(ROOT)))
                if not target.exists():
                    target.write_bytes(data)
                stats[kind] += 1
                records.append({'file': target.relative_to(ROOT).as_posix(),
                                'origin': name, 'sha256': hashlib.sha256(data).hexdigest()})
    # Check that the preservation exercise really recovered the supplementary research corpus.
    supplemental = ROOT / 'research_models' / 'supplemental_index.json'
    if not supplemental.is_file() or len(json.loads(supplemental.read_text(encoding='utf-8'))) != 25:
        raise ValueError('The full supplementary research index was not recovered')
    for letter in ('K', 'L'):
        if not list((ROOT / 'research_models' / 'reference').glob(letter + '_*.md')):
            raise ValueError('Preserved research reference ' + letter + ' is missing')
    manifest = {'prior_commit': base, 'counts': stats, 'files': sorted(records, key=lambda x:x['file'])}
    out = ROOT / 'preservation' / 'MANIFEST.json'
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Preservation complete:', json.dumps(stats))
    print('Manifest:', out.relative_to(ROOT))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default=BASE, help='Pre-migration source commit; default is the verified main SHA')
    args = parser.parse_args()
    restore(args.base)
