"""Validate the budget-cycle navigation in the generated static Atlas site."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from budget_cycle_nav import CHAPTER_PHASE, LESSON_PHASES, PHASES
from atlas_pages import ORDER, STEP_ORDER
from budget_cycle_story import THREE_BUDGETS_VIEW, calendar_span, steps, validate_timeline, typed_edges

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
    assert len(home.select('#budget-cycle details.pfm-cycle-phase')) == 4, 'phase disclosures missing'
    assert home.select_one('#phase-preparation').has_attr('open'), 'Preparation should be open on first load'
    assert len(home.select('#budget-cycle .pfm-phase-steps li')) == 32, '32 phase activity links must remain available'
    assert len(home.select('#budget-cycle .pfm-cycle-activities li')) == 0, 'duplicate activity lists reintroduced'
    assert len(home.select('#cycle-explorer .cs-relation-key span')) == 2, 'relationship legend missing'
    assert 'select("P1")' in (ROOT / 'tools' / 'site' / 'cycle-story.js').read_text(encoding='utf-8')
    main_sections = [x.get('id') or ('paths' if 'start-paths' in x.get('class', []) else '')
                     for x in home.select('.home > section')]
    assert main_sections.index('lines') < main_sections.index('paths'), 'reading paths interrupt the four-line explanation'
    assert main_sections[-1] == 'paths', 'reading paths should conclude the page'
    for p in PHASES:
        assert home.select_one('#phase-' + p['id'])
        assert home.select_one('#phase-' + p['id'] + ' a[href^="chapters/index.html"]')
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
    assert data['edges'] == typed_edges(current), 'stale fiscal-year relation annotations'
    assert sum(e['snapshot_cohorts_differ'] for e in data['edges']) == 8
    assert len([e for e in data['edges'] if e['relation'] == 'feedback-next-budget']) == 2
    assert data['threeView'] == THREE_BUDGETS_VIEW, 'docs/index.html is older than tools/budget_cycle_story.py'
    by_id = {s['id']: s for s in current}
    for item in data['steps']:
        s = by_id[item['id']]
        assert item['calendar'] == list(calendar_span(s)) and item['r'] == list(s['r']) and item['to'] == s['to'], \
            'docs/index.html is older than tools/budget_cycle_story.py (step %s)' % s['id']
        text = ' '.join(home.select_one('#step-' + s['id']).get_text('').split())
        assert ' '.join(s['docs'].split()) in text, \
            'docs/index.html is older than the chapter of step %s (documents)' % s['id']
        # each step of the cycle list and of the explorer opens the chapter of the step
        assert home.select_one('#step-%s a[href="chapters/%s.html"]' % (s['id'], s['id'])), \
            'the explorer panel of %s does not link to its chapter' % s['id']

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

    # Navigation target policy: chapter catalogue stays in the current tab;
    # the budget-cycle explorer opens references in new tabs, not its step chips.
    for link in home.select('#cycle-explorer a[href]'):
        href = link['href']
        if href.startswith('#'):
            assert link.get('target') != '_blank', href
        else:
            assert link.get('target') == '_blank', href
            assert 'noopener' in link.get('rel', []), href

    chapters = page('chapters/index.html')
    assert all(link.get('target') != '_blank' for link in chapters.select('a[href]')), \
        'Chapter index must navigate in the same tab'
    rows = chapters.select('a.row-id[href$=".html"]')
    assert [n.get_text(strip=True) for n in rows] == STEP_ORDER, 'public chapter index must list exactly 32 steps in order'
    assert set(ORDER) == set(CHAPTER_PHASE)
    for key in ('preparation', 'legislation', 'execution', 'accountability', 'across'):
        assert chapters.select_one('#cycle-chapters-' + key)
    for chapter in ORDER:
        detail = page('chapters/' + chapter + '.html')
        assert detail.select_one('.pfm-cycle-context'), chapter

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

    print('OK: four phases, exactly 32 public chapters in cycle order; 85 diagrams, 8 lessons')
    print('OK: each step links to its own chapter; four-line analytical map retained')
    print('OK: budget-cycle story with 15 scenes; step explorer with 32 steps and 32 panels')
    print('OK: calendar months agree with the budgets served in 2026; built page and assets match the tools')


if __name__ == '__main__':
    try:
        check()
    except (AssertionError, ValueError) as error:
        print('Budget-cycle navigation validation failed:',error,file=sys.stderr)
        raise SystemExit(1)
