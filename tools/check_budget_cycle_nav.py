"""Validate the budget-cycle navigation in the generated static Atlas site."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from budget_cycle_nav import CHAPTER_PHASE, LESSON_PHASES, PHASES
from budget_cycle_story import THREE_BUDGETS_VIEW, calendar_span, steps, validate_timeline

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

    # Budget-cycle story and step explorer (tools/budget_cycle_story.py, tools/site/cycle-story.js).
    assert home.select_one('#cycle-story'), 'Budget-cycle story missing on the home page'
    assert len(home.select('#cycle-story .cs-step')) == 15
    data = json.loads(home.select_one('#cs-data').string)
    assert len(data['steps']) == 32
    assert len(home.select('#cycle-explorer .cs-cell')) == 32
    panels = home.select('#cycle-explorer .cs-panel')
    assert len(panels) == 32
    names = [label for p in PHASES for label, _, _ in p['steps']]
    assert [x.select_one('h3').get_text(strip=True) for x in panels] == names, 'Explorer names differ from PHASES'
    assert all(x.get('id') == 'step-' + x.get('data-step') for x in panels)
    assert home.select_one('script[src="assets/cycle-story.js"]'), 'cycle-story.js not loaded on the home page'
    assert (DOCS / 'assets' / 'cycle-story.js').is_file()
    # The built page, script and styles must come from the current tools (rebuild with tools/build_site.py).
    for name in ('cycle-story.js', 'style.css'):
        assert (DOCS / 'assets' / name).read_bytes() == (ROOT / 'tools' / 'site' / name).read_bytes(), \
            'docs/assets/%s is older than tools/site/%s: rebuild the site' % (name, name)
    current = steps()
    validate_timeline(current)
    assert data['threeView'] == THREE_BUDGETS_VIEW, 'docs/index.html is older than tools/budget_cycle_story.py'
    by_id = {s['id']: s for s in current}
    for item in data['steps']:
        s = by_id[item['id']]
        assert item['calendar'] == list(calendar_span(s)) and item['r'] == list(s['r']) and item['to'] == s['to'], \
            'docs/index.html is older than tools/budget_cycle_story.py (step %s)' % s['id']
        text = ' '.join(home.select_one('#step-' + s['id']).get_text(' ', strip=True).split())
        assert ' '.join(s['docs'].split()) in text, \
            'docs/index.html is older than tools/budget_cycle_story.py (documents of %s)' % s['id']

    # An FY 2025 closeout is not active in October 2026: do not claim all three are active every day.
    def active_in_month(fy, month):
        return sum(calendar_span(item, fy)[0] <= month < calendar_span(item, fy)[1] for item in current)
    assert all(active_in_month(fy, 13) > 0 for fy in (2025, 2026, 2027)), 'February 2026 should have three active FY cohorts'
    assert active_in_month(2025, 21) == 0, 'October 2026 should not include an FY 2025 closeout step'
    story_text = home.select_one('#cycle-story').get_text(' ', strip=True)
    explorer_text = home.select_one('#cycle-explorer').get_text(' ', strip=True)
    assert 'by October, this illustration shows two' in story_text
    assert 'At every date, steps of three different budgets are active' not in story_text
    assert 'Downstream process links' in explorer_text and 'Upstream process links' in explorer_text
    assert 'performance-review feedback informs proposals for a later budget' in explorer_text
    assert 'Hands its documents to (same budget year)' not in explorer_text

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
    print('OK: budget-cycle story with 15 scenes; step explorer with 32 steps and 32 panels')
    print('OK: calendar months agree with the budgets served in 2026; built page and assets match the tools')


if __name__ == '__main__':
    try:
        check()
    except (AssertionError, ValueError) as error:
        print('Budget-cycle navigation validation failed:',error,file=sys.stderr)
        raise SystemExit(1)
