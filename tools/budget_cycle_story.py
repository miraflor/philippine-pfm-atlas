"""Budget-cycle story and step explorer for the home page. Presentation only.

The 32 steps, their names, their order and their indicative timing come from budget_cycle_nav.PHASES, which follows
the DBM budget-cycle illustration. Each step has a chapter of the atlas with the same ID. The table in section 1 of that
chapter gives the documents of the step, its place on the four lines and what the loop does not show; the explorer
quotes these cells word for word. This file adds the drawing data, the steps that receive the documents of each step
(checked against the table of the chapter), and links to further chapter sections and diagrams. Every chapter section
and diagram that it names is checked against the atlas when the site is built.

The quotations in the story are taken at build time from the blocks and the list of section 2 of the big picture,
so they stay word for word the same as the atlas. The connecting sentences of the story are written here.

Called by tools/build_site.py (build_home). The drawing and the explorer run in tools/site/cycle-story.js; without
JavaScript the page shows the text of the story and every step panel. Python standard library and bs4 only.
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

from bs4 import BeautifulSoup

from budget_cycle_nav import PHASES

SLOT = '<!-- pfm-cycle-story -->'

# The "three budgets in one year" scene. 'rows': each step has three bars, one for each of the budgets FY 2025,
# FY 2026 and FY 2027, so that each budget is seen in full; the bars active on the moving date are strong.
# 'slice': one bar for each step, at the place of the budget that the step serves in calendar year 2026.
THREE_BUDGETS_VIEW = 'rows'

PH_KEY = {'preparation': 'prep', 'legislation': 'leg', 'execution': 'exec', 'accountability': 'acc'}
ID_PREFIX = {'preparation': 'P', 'legislation': 'L', 'execution': 'E', 'accountability': 'A'}

# Position of each step in the DBM illustration: (column, row) of a 5 x 13 grid, clockwise from the top left.
POS = {'P1': (1, 1), 'P2': (2, 1), 'P3': (3, 1), 'P4': (4, 1), 'P5': (5, 1), 'P6': (5, 2), 'P7': (5, 3),
       'P8': (5, 4), 'P9': (5, 5), 'P10': (5, 6), 'P11': (5, 7), 'P12': (5, 8), 'L1': (5, 9), 'L2': (5, 10),
       'L3': (5, 11), 'L4': (5, 12), 'L5': (5, 13), 'E1': (4, 13), 'E2': (3, 13), 'E3': (2, 13), 'E4': (1, 13),
       'E5': (1, 12), 'E6': (1, 11), 'A1': (1, 10), 'A2': (1, 9), 'A3': (1, 8), 'A4': (1, 7), 'A5': (1, 6),
       'A6': (1, 5), 'A7': (1, 4), 'A8': (1, 3), 'A9': (1, 2)}

# Per step:
#   short  two short lines for the boxes of the drawing
#   r      indicative months, relative to January of the fiscal year (0); "of the prior FY" is negative.
#          Months marked "assumed" are not stated by the illustration; see the note under STEP.
#   fy     the fiscal year that the step serves when it is done in calendar year 2026
#   line   (line, position 0..1, label side, label, short label) on the four-line drawing, or None
#   to     steps that receive documents of this step
#   refs   further (chapter, section) of the atlas; section None = the whole chapter
#   dg     diagrams
# The documents of a step, its place on the four lines ('ln') and what the loop does not show ('note') are read from
# the table in section 1 of the chapter of the step (BRIEF_ROWS).
# Assumed months: P2-P4 in January ("before Tier 1 and Tier 2 proposals"); A8 January to March and A9 January to
# September of the next fiscal year ("within the next FY").
# Each range in r is relative to the fiscal year of one budget. The same step therefore happens in different calendar
# months for different budgets (calendar_span). In calendar year 2026 a step serves exactly one budget, fy; the build
# checks this against r. A hand-off in 'to' is always between steps of the same budget year.
STEP = {
    'P1': dict(short=['Budget Call'], r=(-12, -11), fy=2027, to=['P5', 'P8'],
             refs=[('P0', '5'), ('P5', '2'), ('P0', '8')], dg=['P0-a']),
    'P2': dict(short=['Citizen', 'engagement'], r=(-12, -11), fy=2027, to=['P5', 'P8'], refs=[('P5', '2')]),
    'P3': dict(short=['RDC', 'consultations'], r=(-12, -11), fy=2027, to=['P5', 'P8'], refs=[('P5', '2')]),
    'P4': dict(short=['Program', 'convergence'], r=(-12, -11), fy=2027, to=['P5', 'P8'], refs=[('P5', '2')]),
    'P5': dict(short=['Agency Tier 1', 'proposals'], r=(-11, -10), fy=2027, to=['P6'],
             refs=[('P5', '2'), ('P0', '6')]),
    'P6': dict(short=['Tier 1', 'deliberations'], r=(-10, -9), fy=2027, to=['P7'], refs=[('P0', '5')], dg=['P0-c']),
    'P7': dict(short=['Budget Priorities', 'Framework'], r=(-9, -8), fy=2027, to=['P8'], refs=[('P0', '5')]),
    'P8': dict(short=['Agency Tier 2', 'proposals'], r=(-8, -7), fy=2027, to=['P9'], refs=[('P5', '2')], dg=['P0-c']),
    'P9': dict(short=['Tier 2', 'deliberations'], r=(-7, -5), fy=2027, to=['P10'], refs=[('P0', '5')]),
    'P10': dict(short=['Presentation to', 'President, Cabinet'], r=(-6, -5), fy=2027, to=['P11'], refs=[('P0', '5')]),
    'P11': dict(short=['Confirmation and', 'finalization'], r=(-6, -5), fy=2027, to=['P12'], refs=[('P0', '5')]),
    'P12': dict(short=["The President's", 'Budget'], r=(-6, -4), fy=2027, to=['L1', 'E1'],
             refs=[('P12', '2'), ('E1', '2.5')]),
    'L1': dict(short=['House', 'deliberations'], r=(-5, -2), fy=2027, to=['L2'], refs=[('L0', '5'), ('L0', '7')],
             dg=['L0-a']),
    'L2': dict(short=['Senate', 'deliberations'], r=(-4, -1), fy=2027, to=['L3'], refs=[('L0', '5'), ('L0', '7')]),
    'L3': dict(short=['Bicameral', 'deliberations'], r=(-2, 0), fy=2027, to=['L4'], refs=[('L0', '5'), ('L0', '7')]),
    'L4': dict(short=['Ratification and', 'enrolment'], r=(-1, 0), fy=2027, to=['L5'], refs=[('L0', '7')]),
    'L5': dict(short=['Enactment of', 'the GAA'], r=(-1, 0), fy=2027, line=('authority', 0.1, 'up', 'GAA', 'GAA'),
             to=['E3', 'A1'], refs=[('L0', '7'), ('E3', '2')]),
    'E1': dict(short=['Early', 'procurement'], r=(-3, 0), fy=2027,
             line=('claim', 0.16, 'down', 'Early procurement', 'Procure'), to=['E4'],
             refs=[('E1', '2.5'), ('E1', '2.6')], dg=['E1-b']),
    'E2': dict(short=['Budget execution', 'program'], r=(-3, 0), fy=2027,
             line=('cash', 0.36, 'down', 'Disbursement program (BED 3)', 'BED 3'), to=['E3', 'E5', 'A1'],
             refs=[('E0', '7'), ('E5', '3.3')]),
    'E3': dict(short=['Allotment', 'release'], r=(0, 12), fy=2026,
             line=('authority', 0.28, 'up', 'Allotment release', 'Allotment'), to=['E4'],
             refs=[('E0', '5'), ('E3', '2')], dg=['E0-a', 'E3-a']),
    'E4': dict(short=['Obligation'], r=(0, 12), fy=2026, line=('authority', 0.47, 'up', 'Obligation', 'Obligation'),
             to=['E6', 'A4'], refs=[('E4', '5'), ('E4', '6'), ('E4', '7')], dg=['E4-a']),
    'E5': dict(short=['Cash', 'allocation'], r=(0, 12), fy=2026,
             line=('cash', 0.52, 'up', 'Cash allocation (NCA)', 'NCA'), to=['E6'], refs=[('E5', '2'), ('E5', '3.5')],
             dg=['E5-a']),
    'E6': dict(short=['Disbursement'], r=(0, 12), fy=2026, line=('cash', 0.84, 'down', 'Disbursement', 'Payment'),
             to=['A4', 'A6'], refs=[('E4', '5'), ('E6', '2'), ('E4', '7')], dg=['E4-a']),
    'A1': dict(short=['Performance', 'targets'], r=(-3, 0), fy=2027, to=['A4', 'A5'], refs=[('A1', '5')]),
    'A2': dict(short=['Citizen', 'engagement'], r=(0, 12), fy=2026),
    'A3': dict(short=['Monitoring and', 'evaluation'], r=(0, 12), fy=2026, refs=[('A3', '2')]),
    'A4': dict(short=['Accountability', 'reports'], r=(0, 12), fy=2026,
             line=('records', 0.86, 'down', 'Accountability reports', 'Reports'), to=['A5', 'A6'],
             refs=[('A4', '6')], dg=['A4-c']),
    'A5': dict(short=['Performance', 'review'], r=(0, 12), fy=2026, to=['P5', 'P8'], refs=[('A1', '5')]),
    'A6': dict(short=['In-year', 'reports'], r=(0, 12), fy=2026, refs=[('A6', '2')]),
    'A7': dict(short=['DBCC Mid-Year', 'Report'], r=(8, 9), fy=2026),
    'A8': dict(short=['DBCC Year-End', 'Report'], r=(12, 15), fy=2025),
    'A9': dict(short=['Audit report'], r=(12, 21), fy=2025, line=('records', 0.96, 'up', 'Audit report', 'Audit'),
             refs=[('A9', '5'), ('A9', '7')], dg=['A9-a']),
}

# Steps of the four lines that the loop does not draw: (label, short label, line, position, label side).
INSERTED = [('Contract', 'Contract', 'claim', .47, 'down'), ('Delivery', 'Delivery', 'claim', .62, 'up'),
            ('Acceptance', 'Accept', 'claim', .74, 'down'), ('Voucher (DV)', 'DV', 'claim', .84, 'up'),
            ('Collection, borrowing', 'Collect', 'cash', .06, 'down'),
            ('Single account (TSA)', 'TSA', 'cash', .20, 'up'), ('Replenishment', 'Replenish', 'cash', .95, 'up'),
            ('Registry entry', 'Registry', 'records', .47, 'down'), ('Payable recorded', 'Payable', 'records', .74, 'up')]

# Arrows between steps that are far apart in the loop: (from, to, number, general knowledge).
ARCS = {'docs1': [('L5', 'E3', 1, 0), ('E2', 'E5', 2, 0), ('E2', 'A1', 3, 0), ('P12', 'E1', 4, 0)],
        'docs2': [('P2', 'P5', 5, 0), ('P3', 'P5', 5, 0), ('P4', 'P5', 5, 0), ('E6', 'A4', 6, 0), ('A4', 'A5', 7, 0),
                  ('A5', 'P5', 8, 1)]}


def _esc(s):
    return escape(str(s), quote=True)


ROOT = Path(__file__).resolve().parents[1]
BRIEF_ROWS = {'docs': 'Documents', 'ln': 'On the four lines', 'note': 'Not drawn in the loop',
              'receives': 'Receives documents from', 'passes': 'Passes documents to'}
STEP_ID = r'(?:P1[0-2]|P\d|L[0-5]|E[0-6]|A\d)'


def named_steps(text):
    """Step IDs named in a text; 'P1 to P4' names P1, P2, P3 and P4."""
    order = [p + str(i) for p, n in (('P', 12), ('L', 5), ('E', 6), ('A', 9)) for i in range(1, n + 1)]
    out = []
    for m in re.finditer(r'(?<![\w-])(%s)(?: to (%s))?(?![\w-])' % (STEP_ID, STEP_ID), text):
        a, b = m.group(1), m.group(2)
        out += order[order.index(a):order.index(b) + 1] if b else [a]
    return out


def brief(chapter_dir, sid):
    """The rows of the table in section 1 of the chapter of a step: {label: cell}."""
    files = sorted(Path(chapter_dir).glob(sid + '_*.md'))
    if len(files) != 1:
        raise ValueError('budget_cycle_story: the chapter of step %s was not found in %s' % (sid, chapter_dir))
    text = files[0].read_text(encoding='utf-8')
    m = re.search(r'^## 1\. The step in the budget cycle\n\n(.*?)(?:\n\n|\Z)', text, re.S | re.M)
    if not m:
        raise ValueError('budget_cycle_story: chapter %s has no section 1 "The step in the budget cycle"' % sid)
    rows = {}
    for line in m.group(1).split('\n')[2:]:
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows[cells[0]] = cells[1]
    return rows


def steps(chapter_dir=None):
    """The 32 steps in the order of the illustration, joined with the data of this file and of the chapters."""
    chapter_dir = chapter_dir or ROOT / 'docs' / 'atlas' / 'chapters'
    out = []
    for phase in PHASES:
        prefix = ID_PREFIX[phase['id']]
        for i, (label, timing, chapter) in enumerate(phase['steps'], 1):
            sid = prefix + str(i)
            if sid not in STEP:
                raise ValueError('budget_cycle_story: no data for step ' + sid)
            if chapter != sid:
                raise ValueError('budget_cycle_story: step %s points to chapter %s, not to its own chapter' % (sid, chapter))
            d = dict(STEP[sid])
            d.update(id=sid, ph=PH_KEY[phase['id']], phase=phase['name'], name=label, timing=timing, chapter=chapter)
            rows = brief(chapter_dir, sid)
            for key, row in BRIEF_ROWS.items():
                d[key] = rows.get(row, '')
            for key in ('to', 'refs', 'dg'):
                d.setdefault(key, [])
            d.setdefault('line', None)
            named = named_steps(d['passes'])
            if sorted(named) != sorted(d['to']):
                raise ValueError('budget_cycle_story: step %s passes documents to %s in this file and to %s in its '
                                 'chapter' % (sid, d['to'], named))
            out.append(d)
    if len(out) != 32 or {s['id'] for s in out} != set(STEP) or set(POS) != set(STEP):
        raise ValueError('budget_cycle_story: the steps do not match the 32 steps of budget_cycle_nav.PHASES')
    ids = {s['id'] for s in out}
    for s in out:
        for t in s['to']:
            if t not in ids:
                raise ValueError('budget_cycle_story: %s hands documents to an unknown step %s' % (s['id'], t))
    for s in out:
        receives = sorted(x['id'] for x in out if s['id'] in x['to'])
        named = sorted(named_steps(s['receives']))
        if receives != named:
            raise ValueError('budget_cycle_story: step %s receives documents from %s by the data of this file, and from %s '
                             'by its chapter' % (s['id'], receives, named))
    return out


def calendar_span(step, fy=None):
    """Calendar months of a step for the budget of fiscal year fy (default: the budget it serves in 2026).
    Month 0 is January 2025; calendar year 2026 is months 12 to 24."""
    origin = 12 * ((fy or step['fy']) - 2025)
    return (origin + step['r'][0], origin + step['r'][1])


def validate_timeline(steps_list):
    """The timing must agree with the fiscal year that each step serves in calendar year 2026."""
    by = {s['id']: s for s in steps_list}
    for s in steps_list:
        active = [fy for fy in (2025, 2026, 2027)
                  if calendar_span(s, fy)[0] < 24 and calendar_span(s, fy)[1] > 12]
        if active != [s['fy']]:
            raise ValueError('budget_cycle_story: in 2026, step %s serves FY %s, but its months give %s'
                             % (s['id'], s['fy'], active or 'no budget'))
    expected = {('P1', 2026): (0, 1), ('E3', 2026): (12, 24), ('A9', 2026): (24, 33),
                ('P1', None): (12, 13), ('E1', None): (21, 24), ('E3', None): (12, 24),
                ('A1', None): (21, 24), ('A8', None): (12, 15), ('A9', None): (12, 21)}
    for (sid, fy), span in expected.items():
        if calendar_span(by[sid], fy) != span:
            raise ValueError('budget_cycle_story: wrong calendar months for %s (FY %s)' % (sid, fy or by[sid]['fy']))


def _sections(chapter_dir, chapter):
    files = sorted(Path(chapter_dir).glob(chapter + '_*.md'))
    if len(files) != 1:
        raise ValueError('budget_cycle_story: chapter %s not found' % chapter)
    text = files[0].read_text(encoding='utf-8')
    return set(re.findall(r'^#{2,4} (\d+(?:\.\d+)*)\.? ', text, re.M))


def _atlas_links(s, chapter_dir, diagram_ids):
    """The chapter of the step, then further chapter sections and diagrams."""
    parts = ['<a href="chapters/%s.html">Chapter %s</a>' % (s['id'], s['id'])]
    by_chapter = {}
    for ch, sec in s['refs']:
        by_chapter.setdefault(ch, []).append(sec)
    for ch, secs in by_chapter.items():
        known = _sections(chapter_dir, ch)
        links = []
        for sec in secs:
            if sec is None:
                continue
            if sec not in known:
                raise ValueError('budget_cycle_story: chapter %s has no section %s (step %s)' % (ch, sec, s['id']))
            links.append('<a href="chapters/%s.html#section-%s">%s</a>' % (ch, sec.replace('.', '-'), sec))
        if ch == s['id'] and links:
            parts.append('section%s %s' % ('s' if len(links) > 1 else '', ', '.join(links)))
        elif ch != s['id']:
            head = '<a href="chapters/%s.html">Chapter %s</a>' % (ch, ch)
            if links:
                head += ', section%s %s' % ('s' if len(links) > 1 else '', ', '.join(links))
            parts.append(head)
    for did in s['dg']:
        if did not in diagram_ids:
            raise ValueError('budget_cycle_story: unknown diagram %s (step %s)' % (did, s['id']))
        parts.append('<a href="diagrams/%s.html">diagram %s</a>' % (did, did))
    return ' · '.join(parts)


def _li_html(soup_html, index):
    soup = BeautifulSoup(soup_html, 'html.parser')
    ol = soup.find('ol')
    items = ol.find_all('li', recursive=False) if ol else []
    if len(items) != 3:
        raise ValueError('budget_cycle_story: the block of the meeting points does not have three items')
    return ''.join(str(c) for c in items[index].contents)


def _paragraphs(soup_html):
    return [''.join(str(c) for c in p.contents) for p in BeautifulSoup(soup_html, 'html.parser').find_all('p')]


def _quote(html, where='Atlas, the big picture, section 2'):
    return '<blockquote class="cs-quote">%s<span class="cs-from">%s</span></blockquote>' % (html, _esc(where))


def build(render_md, block, big_text, link, chapter_dir, diagram_ids, source_codes):
    """HTML of the story and the explorer.

    render_md(markdown) -> HTML of the big picture with its links; block(name) -> the markdown of a site block;
    big_text -> the markdown of the big picture; link(html) -> the HTML with source codes, chapters and diagrams linked;
    chapter_dir -> folder of the chapter Markdown files; diagram_ids -> the identifiers of the diagrams;
    source_codes -> the codes that Reference F defines."""
    S = steps(chapter_dir)
    validate_timeline(S)
    if THREE_BUDGETS_VIEW not in ('rows', 'slice'):
        raise ValueError("budget_cycle_story: THREE_BUDGETS_VIEW must be 'rows' or 'slice'")
    for s in S:
        for key in ('docs', 'ln', 'note'):
            for code in re.findall(r'\[([A-Za-z][A-Za-z0-9\-]*)[ \]]', s[key]):
                if code not in source_codes:
                    raise ValueError('budget_cycle_story: step %s cites %s, which Reference F does not define'
                                     % (s['id'], code))
    by = {s['id']: s for s in S}

    # Quotations, word for word from the big picture.
    meet = render_md(block('meeting-points'))
    meet_paras = _paragraphs(meet)
    if not meet_paras or 'A payment can be made only at a point where the lines meet' not in meet_paras[0]:
        raise ValueError('budget_cycle_story: the first paragraph of the meeting points has changed')
    cases = _paragraphs(render_md(block('cases')))
    if len(cases) != 2 or not cases[1].startswith('A case where it fails'):
        raise ValueError('budget_cycle_story: the block of the two cases has changed')
    fail_case = re.sub(r'^A case where it fails:\s*', '', cases[1])
    fail_case = fail_case[:1].upper() + fail_case[1:]
    bullets = {}
    for key, start in (('three', 'Three budgets are active in one calendar year.'),
                       ('records', 'The records do not wait for the payment.')):
        m = re.search(r'^- (\*\*%s\*\*[^\n]*)$' % re.escape(start), big_text, re.M)
        if not m:
            raise ValueError('budget_cycle_story: the point "%s" is missing in section 2 of the big picture' % start)
        p = _paragraphs(render_md(m.group(1)))
        bullets[key] = p[0] if p else ''

    phase_over = {}
    for phase in PHASES:
        phase_over[PH_KEY[phase['id']]] = (
            '<span class="cs-big" style="color:var(--cs-%s)">%s</span><span class="cs-sm"><b>Key actors</b> %s</span>'
            '<span class="cs-sm"><b>Main documents</b> %s</span>'
            % (PH_KEY[phase['id']], _esc(phase['name']), _esc(phase['actors']), _esc(phase['records'])))
    counts = {PH_KEY[p['id']]: len(p['steps']) for p in PHASES}
    summary = {PH_KEY[p['id']]: p['summary'] for p in PHASES}

    def pill(ph, n):
        return ('<span class="cs-pill"><i style="background:var(--cs-%s)"></i>Phase %d · %d steps</span>'
                % (ph, n, counts[ph]))

    scenes = [
        ('hero', '<p class="atlas-kicker">The budget cycle, told in steps</p>'
                 '<h2 id="cs-title">The budget cycle, step by step</h2>'
                 '<p class="cs-lede">Thirty-two steps in four phases: the cycle as the DBM budget-cycle illustration '
                 'draws it, and as budget practitioners know it.</p>'
                 '<p>Scroll down. The same 32 steps then show when each one happens, how one payment clears, and '
                 'which documents pass from one step to another.</p>'
                 '<p class="cs-skip"><a href="#cycle-explorer">Go to the step explorer</a> · '
                 '<a href="#budget-cycle">Go to the list of steps</a></p>'),
        ('prep', pill('prep', 1) + '<h3>Preparation</h3><p>%s. It starts with the Budget Call in January and ends '
                 'when the President\'s Budget goes to Congress in July or August, all in the year before the budget '
                 'year.</p><p class="cs-note">For the FY 2027 budget, agencies encoded their Tier 1 and Tier 2 '
                 'proposals in OSBPS from 6 March to 28 April 2026. [NBM156]</p>' % _esc(summary['prep'])),
        ('leg', pill('leg', 2) + '<h3>Legislation</h3><p>%s: the House, the Senate, the bicameral conference, '
                'ratification, and the enactment of the General Appropriations Act.</p><p class="cs-note">The FY '
                '2026 GAA, Republic Act No. 12314, took effect on 5 January 2026. [NBC599]</p>' % _esc(summary['leg'])),
        ('exec', pill('exec', 3) + '<h3>Execution</h3><p>%s. Two of the six steps start before the budget year: '
                 'early procurement and the budget execution program, from October to December of the prior '
                 'year.</p>' % _esc(summary['exec'])),
        ('acc', pill('acc', 4) + '<h3>Accountability</h3><p>%s. The phase starts before the budget year, with the '
                'performance targets, and ends in the year after it, with the DBCC Year-End Report and the audit '
                'report.</p>' % _esc(summary['acc'])),
        ('time', '<p class="atlas-kicker">The same steps, in time</p><h3>One loop takes about three calendar '
                 'years</h3><p>The loop shows the order of the steps. Its timing labels place each step in time: '
                 '"of the prior FY", "throughout the FY", "within the next FY". On a calendar, the FY 2026 budget runs '
                 'from the Budget Call in January 2025 to the audit report in 2027.</p><p class="cs-note">The months '
                 'are indicative, not binding deadlines; consult current DBM issuances.</p>'),
        ('three', '<p class="atlas-kicker">The same steps, in time</p><h3>Three budgets in one year</h3>'
                  + _quote(bullets['three']) +
                  ('<p>The faded bars are the same 32 steps for FY 2025 and FY 2027. The moving line is a date in '
                   '2026. During much of 2026, steps from three budget years overlap; by October, this illustration shows two.</p>'
                   if THREE_BUDGETS_VIEW == 'rows' else
                   '<p>Each bar now sits where its step happens in 2026, for the budget that the step serves: '
                   'FY 2027 for preparation and legislation, FY 2026 for execution, FY 2025 for the year-end report '
                   'and the audit. The moving line is a date in 2026. During much of the year, steps from three budget '
                   'years overlap; by October, this illustration shows two.</p>')),
        ('lines', '<p class="atlas-kicker">Inside Execution</p><h3>Four lines, not one row</h3><p>The loop draws '
                  'Execution as one row of six steps. In the atlas, these steps sit on four lines of work that run at '
                  'the same time: legal authority, the claim, cash, and records and control. Steps from other phases '
                  'join them: the GAA starts the authority line, and the accountability reports and the audit sit on '
                  'the records line.</p>' + _quote(meet_paras[0]) +
                  '<p class="cs-note">Labels in grey italics are steps that the loop does not draw: the contract, the '
                  'delivery, the acceptance, the voucher.</p>'),
        ('mp1', '<p class="atlas-kicker">One payment under a contract</p><h3>Meeting point 1</h3>'
                + _quote(_li_html(meet, 0))),
        ('mp2', '<p class="atlas-kicker">One payment under a contract</p><h3>Meeting point 2</h3>'
                + _quote(_li_html(meet, 1)) + _quote(bullets['records'])),
        ('mp3', '<p class="atlas-kicker">One payment under a contract</p><h3>Meeting point 3</h3>'
                + _quote(_li_html(meet, 2))),
        ('fail', '<p class="atlas-kicker">The same payment, a second ending</p><h3>When the lines do not meet in '
                 'time</h3>' + _quote(fail_case)),
        ('docs1', '<p class="atlas-kicker">Back to the loop</p><h3>Documents connect steps that are far apart</h3>'
                  '<p>The arrows of the illustration go from each step to the next. Documents also connect steps '
                  'across the loop. These arrows trace the same budget through its lifecycle; the FY labels elsewhere are a 2026 snapshot, not a single transaction.</p><ol class="cs-hand">'
                  '<li><b>1</b><span>GAA to allotment release: for items without pre-conditions, the GAA itself is the '
                  'allotment order. [NBC599]</span></li>'
                  '<li><b>2</b><span>Budget execution program to cash allocation: DBM issues NCAs from the monthly '
                  'disbursement programs (BED 3). [NBC599] [MC51]</span></li>'
                  '<li><b>3</b><span>Budget execution program to performance targets: the Physical Plan (BED 2) holds '
                  'the quarterly targets. [NBC599 s.3.9]</span></li>'
                  '<li><b>4</b><span>President\'s Budget to early procurement: once it is submitted, an agency may '
                  'start bidding, but may not award. [IRR12009 s.12.1, s.12.4]</span></li></ol>'),
        ('docs2', '<p class="atlas-kicker">Back to the loop</p><h3>The loop closes through forms and reports</h3>'
                  '<ol class="cs-hand">'
                  '<li><b>5</b><span>Citizen engagement, RDC consultations and program convergence to the agency '
                  'proposals: BP Forms D, C and 206. [NBM156]</span></li>'
                  '<li><b>6</b><span>Disbursement to accountability reports: obligations and disbursements in the '
                  'registries are reported in FAR 1, each quarter. [JC2019-1]</span></li>'
                  '<li><b>7</b><span>Accountability reports to performance review: DBM reviews the year from BAR 1 '
                  'and the financial reports. [PBB2024]</span></li>'
                  '<li class="cs-gk"><b>8</b><span>Performance review to proposals for the next budget. The atlas marks this use '
                  'as general knowledge, not a source it read, so the arrow is dashed.</span></li></ol>'),
        ('end', '<p class="atlas-kicker">Your turn</p><h3>Open any step</h3><p>The explorer below keeps the loop and '
                'opens each step: its documents, its place on the four lines, the atlas sub-steps and sections, and '
                'the steps it hands documents to. You can also find a document by name, such as SARO, NCA or '
                'LDDAP-ADA.</p><p><a href="#cycle-explorer">Go to the step explorer</a></p>'),
    ]
    for code in re.findall(r'\[([A-Za-z][A-Za-z0-9\-]*)[ \]]', ''.join(html for _, html in scenes)):
        if code not in source_codes:
            raise ValueError('budget_cycle_story: the story cites %s, which Reference F does not define' % code)
    steps_html = ''.join('<section class="cs-step%s" data-scene="%s"><div>%s</div></section>'
                         % (' cs-first' if i == 0 else (' cs-last' if i == len(scenes) - 1 else ''), name, html)
                         for i, (name, html) in enumerate(scenes))

    data = {
        'steps': [{'id': s['id'], 'ph': s['ph'], 'short': s['short'], 'name': s['name'], 'r': list(s['r']),
                   'calendar': list(calendar_span(s)), 'fy': s['fy'], 'pos': list(POS[s['id']]),
                   'line': list(s['line']) if s['line'] else None, 'to': s['to']} for s in S],
        'threeView': THREE_BUDGETS_VIEW,
        'inserted': [list(x) for x in INSERTED],
        'arcs': {k: [list(a) for a in v] for k, v in ARCS.items()},
        'overlay': dict(phase_over, hero='<span class="cs-big">32 steps<br>4 phases<br>1 loop</span><span '
                                          'class="cs-sm">Positions and order follow the DBM budget-cycle illustration. '
                                          'Start at the top left and go clockwise.</span>',
                        end='<span class="cs-big">Open any step</span><span class="cs-sm">The explorer below '
                            'keeps this loop.</span>'),
    }
    data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

    story = ('<section id="cycle-story" class="cs-story" aria-labelledby="cs-title">'
             '<div class="cs-layout">'
             '<div class="cs-fig" aria-hidden="true">'
             '<svg class="cs-svg" data-layout="loop" focusable="false"><defs><marker id="cs-ah" viewBox="0 0 10 10" '
             'refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9z" '
             'class="cs-ahp"/></marker></defs></svg>'
             '<div class="cs-ov"></div><div class="cs-cap"></div></div>'
             '<div class="cs-steps">%s</div></div>'
             '<script type="application/json" id="cs-data">%s</script>'
             '</section>' % (link(steps_html), data_json))

    # Explorer: the loop as 32 links, and one panel per step, rendered here so that the page reads without JavaScript.
    cells, panels = [], []
    order = [s['id'] for s in S]
    for i, s in enumerate(S):
        col, row = POS[s['id']]
        cells.append('<a class="cs-cell ph-%s f%d" href="#step-%s" data-step="%s" style="grid-column:%d;grid-row:%d">'
                     '<span class="cs-cid">%s</span><span class="cs-cnm">%s</span><span class="cs-cfy">FY %d</span></a>'
                     % (s['ph'], s['fy'], s['id'], s['id'], col, row, s['id'], _esc(s['name']), s['fy']))
        receives = [x['id'] for x in S if s['id'] in x['to']]
        prev_id, next_id = order[i - 1], order[(i + 1) % len(order)]

        def chips(ids):
            return '<span class="cs-chips">%s</span>' % ''.join(
                '<a class="cs-chip" href="#step-%s" data-step="%s">%s · %s</a>'
                % (t, t, t, _esc(by[t]['name'])) for t in ids)

        rows = [('Serves, when done in calendar year 2026', 'FY %d' % s['fy'])]
        if s['docs']:
            rows.append(('Documents', _esc(s['docs'])))
        if s['ln']:
            k = s['line'][0] if s['line'] else 'records'
            rows.append(('On the four lines', '<span class="cs-ln" style="color:var(--%s);background:var(--%s-tint)">'
                                              '%s</span>' % (k, k, _esc(s['ln']))))
        if s['note']:
            rows.append(('What the loop does not show', _esc(s['note'])))
        if s['to']:
            rows.append(('Downstream process links', chips(s['to'])))
        if receives:
            rows.append(('Upstream process links', chips(receives)))
        rows.append(('In the loop', chips([prev_id, next_id])))
        rows.append(('In the atlas', _atlas_links(s, chapter_dir, diagram_ids)))
        search = ' '.join([s['id'], s['name'], re.sub(r'\[[^\]]*\]', '', s['docs']), s['note'], s['ln']]).lower()
        panels.append('<article class="cs-panel" id="step-%s" data-step="%s" data-search="%s">'
                      '<p class="cs-lab">%s · %s · %s</p><h3>%s</h3><dl>%s</dl></article>'
                      % (s['id'], s['id'], _esc(search), s['id'], _esc(s['phase']), _esc(s['timing']),
                         _esc(s['name']), ''.join('<dt>%s</dt><dd>%s</dd>' % r for r in rows)))

    explorer = ('<section id="cycle-explorer" class="cs-explorer" aria-labelledby="cs-ex-title">'
                '<div class="cs-ex-head"><p class="atlas-kicker">Step explorer</p>'
                '<h2 id="cs-ex-title">The 32 steps, opened</h2>'
                '<p class="cs-note">Same positions and order as the DBM budget-cycle illustration. Select a step. '
                'Dashed blue outlines mark downstream links; dashed orange outlines mark upstream links. '
                'Most relationships follow one budget through its lifecycle; performance-review feedback informs proposals for a later budget. '
                'The FY labels show activities taking place in 2026, not one literal transaction trail. Each step has its own address, for example '
                '<a href="#step-E4">#step-E4</a>.</p></div>'
                '<div class="cs-controls">'
                '<span class="cs-colour"><span>Colour by</span><span class="cs-seg" role="group" aria-label="Colour '
                'the steps by"><button type="button" data-colour="phase" aria-pressed="true">Phase</button>'
                '<button type="button" data-colour="fy" aria-pressed="false">Fiscal year served in 2026</button>'
                '</span></span>'
                '<span class="cs-find"><label for="cs-q">Find a document</label><input id="cs-q" type="search" '
                'placeholder="SARO, NCA, BP Form 202" autocomplete="off"><span class="cs-hint" aria-live="polite">'
                '</span></span></div>'
                '<p class="cs-legend"></p>'
                '<div class="cs-grid">%s<div class="cs-panels">%s</div></div>'
                '<p class="cs-note">Step names, order and indicative timing follow the DBM budget-cycle illustration; '
                'the months are not binding deadlines. "Serves" names the budget that the step works on when it is '
                'done in calendar year 2026. Where the atlas names no document for a step, the panel leaves the field '
                'out.</p>'
                '</section>' % (''.join(cells), link(''.join(panels))))
    return story + explorer
