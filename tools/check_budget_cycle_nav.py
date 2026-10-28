"""Validate the budget-cycle navigation in the generated static Atlas site."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from budget_cycle_nav import CHAPTER_PHASE, LESSON_PHASES, PHASES

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'


def check():
    def page(path):
        p = DOCS / path
        if not p.is_file():
            raise AssertionError('Missing generated page: ' + path)
        return BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')

    home = page('index.html')
    assert len(home.select('#budget-cycle .pfm-cycle-phase')) == 4
    assert len(home.select('#budget-cycle .pfm-cycle-activities li')) == 32
    for p in PHASES:
        assert home.select_one('#phase-' + p['id'])
        assert len(home.select('#phase-{} .pfm-cycle-activities li'.format(p['id']))) == len(p['steps'])
    assert home.select_one('#lines .map'), 'Four-line map must not be removed'

    chapters = page('chapters/index.html')
    original = chapters.select('a.row-id[href$=".html"]')
    assert len(original) == 19
    assert {n.get_text(strip=True) for n in original} == set(CHAPTER_PHASE)
    for key in ('preparation', 'legislation', 'execution', 'accountability', 'across'):
        assert chapters.select_one('#cycle-chapters-' + key)
    for chapter in CHAPTER_PHASE:
        detail = page('chapters/' + chapter + '.html')
        assert detail.select_one('.pfm-cycle-context')

    diagrams = page('diagrams/index.html')
    diagram_cards = diagrams.select('.atlas-diagram-card')
    # The current source-backed atlas has 85 diagrams; never silently lose one.
    assert len(diagram_cards) == 85, len(diagram_cards)
    ids = [c.select_one('.atlas-diagram-id').get_text(strip=True) for c in diagram_cards]
    assert len(set(ids)) == 85
    for key in ('preparation', 'legislation', 'execution', 'accountability', 'across'):
        assert diagrams.select_one('#cycle-diagrams-' + key)
    for did in ids:
        detail = page('diagrams/' + did + '.html')
        assert detail.select_one('.pfm-cycle-context'), did

    guided = page('walkthrough.html')
    assert len(guided.select('.atlas-lesson-scene')) == 8
    assert guided.select_one('#cycle-guide-preparation')
    assert guided.select_one('#cycle-guide-legislation')
    assert guided.select_one('#cycle-guide-execution')
    assert guided.select_one('#cycle-guide-accountability')
    assert guided.select_one('#cycle-guide-across')
    for slug in LESSON_PHASES:
        detail=page('guide/'+slug+'.html')
        assert detail.select_one('.pfm-cycle-context'), slug

    print('OK: four phases, 32 activities, 19 chapters, 85 diagrams, 8 lessons')
    print('OK: existing four-line analytical map and detail links retained')


if __name__ == '__main__':
    try:
        check()
    except (AssertionError, ValueError) as error:
        print('Budget-cycle navigation validation failed:',error,file=sys.stderr)
        raise SystemExit(1)
