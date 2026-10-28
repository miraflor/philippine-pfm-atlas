"""Practitioner-oriented budget cycle, presentation only.

The sequence is adapted from the DBM budget-cycle illustration; the timing is
indicative. Each activity links back to an existing, source-backed Atlas chapter.
The national expenditure budget cycle is not the whole of public finance.
"""
from html import escape


PHASES = [
    {
        "id": "preparation", "number": "01", "name": "Preparation",
        "when": "Before the budget year",
        "summary": "From government priorities to the President's proposed budget",
        "actors": "DBM; departments and agencies; RDCs; President and Cabinet",
        "records": "Budget Call; Tier 1 and Tier 2 proposals; Budget Priorities Framework; National Expenditure Program (NEP)",
        "read": [("Budget preparation", "03"), ("Fiscal framework", "02"), ("Planning", "01")],
        "steps": [
            ("Budget Call", "January of the prior FY", "03"),
            ("Citizen engagement", "Before Tier 1 and Tier 2 proposals", "03"),
            ("Regional Development Council consultations", "Before Tier 1 and Tier 2 proposals", "03"),
            ("Program convergence", "Before Tier 1 and Tier 2 proposals", "03"),
            ("Agency Tier 1 proposals: ongoing expenditures", "February of the prior FY", "03"),
            ("Tier 1 deliberations", "March of the prior FY", "03"),
            ("Budget Priorities Framework", "April of the prior FY", "03"),
            ("Agency Tier 2 proposals: new or expanded spending", "May of the prior FY", "03"),
            ("Tier 2 deliberations", "June-July of the prior FY", "03"),
            ("Presentation to the President and Cabinet", "July of the prior FY", "03"),
            ("Confirmation and finalization", "July of the prior FY", "03"),
            ("The President's Budget submitted to Congress", "July-August of the prior FY", "03"),
        ],
    },
    {
        "id": "legislation", "number": "02", "name": "Legislation",
        "when": "Before the budget year",
        "summary": "From the President's proposal to an enacted appropriations law",
        "actors": "House of Representatives; Senate; bicameral conference; President",
        "records": "NEP; General Appropriations Bill (GAB); General Appropriations Act (GAA)",
        "read": [("Budget legislation", "04"), ("Appropriation and release", "05")],
        "steps": [
            ("House deliberations", "August-October of the prior FY", "04"),
            ("Senate deliberations", "September-November of the prior FY", "04"),
            ("Bicameral deliberations", "November-December of the prior FY", "04"),
            ("Ratification and enrolment", "December of the prior FY", "04"),
            ("Enactment of the General Appropriations Act", "December of the prior FY, indicative", "04"),
        ],
    },
    {
        "id": "execution", "number": "03", "name": "Execution",
        "when": "Before and during the budget year",
        "summary": "From spending authority to contracts, cash allocation and payment",
        "actors": "DBM; implementing agencies; Bureau of the Treasury; banks; suppliers and payees",
        "records": "Budget Execution Documents; allotment/ABM/SARO; NCA; obligation records; disbursement vouchers; payment orders",
        "read": [("Release: allotment and cash", "05"), ("Procurement", "06"), ("Obligation and payment", "07"), ("Treasury", "11")],
        "steps": [
            ("Early procurement activities", "October-December of the prior FY", "06"),
            ("Budget execution program", "October-December of the prior FY", "05"),
            ("Allotment release", "January (comprehensive) and throughout the FY", "05"),
            ("Obligation", "Throughout the FY", "07"),
            ("Cash allocation", "January (comprehensive) and throughout the FY", "05"),
            ("Disbursement", "Throughout the FY", "07"),
        ],
    },
    {
        "id": "accountability", "number": "04", "name": "Accountability",
        "when": "Before, during and after the budget year",
        "summary": "From performance targets to reporting, review and independent audit",
        "actors": "Implementing agencies; DBM/DBCC; COA; citizens and oversight institutions",
        "records": "Performance targets; budget and financial accountability reports; in-year reports; DBCC reports; audit reports",
        "read": [("Accounting and reporting", "08"), ("Audit and oversight", "09"), ("Performance and evaluation", "18")],
        "steps": [
            ("Performance targets", "October-December of the prior FY", "18"),
            ("Citizen engagement", "Throughout the FY", "18"),
            ("Monitoring and evaluation", "Throughout the FY", "18"),
            ("Agencies' accountability reports", "Monthly and quarterly", "08"),
            ("Performance review", "Throughout the FY", "18"),
            ("In-year reports", "Monthly and quarterly", "08"),
            ("DBCC Mid-Year Report", "September of the FY", "18"),
            ("DBCC Year-End Report", "Within the next FY", "18"),
            ("Audit report", "Within the next FY", "09"),
        ],
    },
]



# The mapping is a navigation taxonomy, not a change to chapter identifiers or
# a claim that an activity occurs in only one phase.
GROUPS = [
    ('preparation', 'Preparation', ('01', '02', '03')),
    ('legislation', 'Legislation', ('04',)),
    ('execution', 'Execution', ('05', '06', '07', '11', '12', '13')),
    ('accountability', 'Accountability', ('08', '09', '18')),
    ('across', 'Cross-cutting and related pathways', ('00', '10', '14', '15', '16', '17', '19')),
]
CHAPTER_PHASE = {ch: phase for phase, _, codes in GROUPS for ch in codes if ch != '00'}
LESSON_PHASES = {
    '01_orient': ('across',),
    '02_budget': ('preparation', 'legislation'),
    '03_authority': ('execution',),
    '04_claim': ('execution',),
    '05_treasury': ('execution',),
    '06_records': ('accountability',),
    '07_beyond': ('across',),
    '08_integration': ('across',),
}
PHASE_NAMES = {key: label for key, label, _ in GROUPS}
PHASE_INFO = {p['id']: p for p in PHASES}


def _esc(s):
    return escape(str(s), quote=True)


def _link(ch, label, root=''):
    return '<a href="{}chapters/{}.html">{}</a>'.format(root, ch, _esc(label))


def _intro_nav(destination='home', prefix=''):
    """Simple four-phase navigation using the original Atlas typographic tokens."""
    out = ['<nav class="pfm-cycle-nav" aria-label="Navigate by budget phase">']
    for p in PHASES:
        key = p['id']
        anchor = {'home': 'phase-' + key, 'chapters': 'cycle-chapters-' + key,
                  'diagrams': 'cycle-diagrams-' + key,
                  'walkthrough': 'cycle-guide-' + key}[destination]
        out.append('<a href="{}#{}"><span class="pfm-cycle-num">{}</span><strong>{}</strong>'
                   '<span class="pfm-cycle-nav-sub">{}</span></a>'.format(
                       _esc(prefix), anchor, p['number'], _esc(p['name']), _esc(p['when'])))
    out.append('</nav>')
    return ''.join(out)


def home_cycle():
    """Phase-first navigation, followed by all activities in the supplied diagram."""
    out = [
        '<section id="budget-cycle" class="atlas-story-section pfm-cycle" aria-labelledby="pfm-cycle-title">',
        '<p class="atlas-kicker">01 / The national budget process</p>',
        '<h2 id="pfm-cycle-title">Follow the budget, from proposal to audit.</h2>',
        '<p class="pfm-cycle-lede">Choose a familiar phase. Each activity takes you to an existing '
        'Atlas chapter with its agencies, documents, controls and systems.</p>',
        _intro_nav(),
        '<p class="pfm-cycle-caveat"><strong>The phases overlap.</strong> Preparation and legislation '
        'for the next fiscal year run alongside execution of the current budget and review of prior years. '
        'The illustrative months below are not binding deadlines; consult current DBM issuances.</p>',
    ]
    for p in PHASES:
        out.extend([
            '<section class="pfm-cycle-phase" id="phase-{}" aria-labelledby="pfm-cycle-{}-title">'.format(p['id'], p['id']),
            '<div class="pfm-cycle-phase-head"><p class="pfm-cycle-eyebrow">PHASE {}</p>'
            '<h3 id="pfm-cycle-{}-title">{}</h3><p>{}</p></div>'.format(p['number'],p['id'],_esc(p['name']),_esc(p['summary'])),
            '<ol class="pfm-cycle-activities">',
        ])
        for index, (label, timing, chapter) in enumerate(p['steps'], 1):
            out.append('<li><span class="pfm-cycle-step">{:02d}</span><div>{}'
                       '<small>{}</small></div></li>'.format(index, _link(chapter,label), _esc(timing)))
        out.extend([
            '</ol>',
            '<div class="pfm-cycle-metadata"><p><strong>Key actors</strong> {}</p>'
            '<p><strong>Main documents</strong> {}</p></div>'.format(_esc(p['actors']), _esc(p['records'])),
            '<p class="pfm-cycle-read"><strong>Explore further:</strong> {}</p>'.format(
                ' · '.join(_link(ch,label) for label,ch in p['read'])),
            '</section>',
        ])
    out.extend([
        '<aside class="pfm-cycle-related"><p class="pfm-cycle-eyebrow">Across every phase</p>',
        '<h3>How do the records and systems connect?</h3>',
        '<p>The budget cycle orders the work. The original four-line map explains how legal authority, '
        'claims, cash and records intersect. Both views are necessary. Systems and UACS are not a fifth budget phase.</p>',
        '<p><a href="#lines">Four-line analytical map</a> · <a href="systems.html">Systems and UACS</a>'
        ' · <a href="chapters/index.html#cycle-chapters-across">Other PFM pathways</a></p>',
        '</aside>',
        '<p class="pfm-cycle-note">Activity sequence and indicative timing follow the budget-cycle '
        'illustration supplied for this reorganization. Procedural particulars and source qualifications '
        'remain in the linked Atlas chapters.</p>',
        '</section>',
    ])
    return '\n'.join(out)


def _section_nav(destination):
    return (_intro_nav(destination)
            + '<p class="pfm-cycle-secondary"><a href="#cycle-{}-across">'
            'Cross-cutting and related pathways</a></p>'.format(destination if destination != 'walkthrough' else 'guide'))


def chapter_index(body):
    """Group the original 19 chapter table rows; do not rewrite any row or links."""
    import re
    marker = ('<div class="table-wrap"><table><thead><tr><th>No.</th><th>Chapter</th>'
              '<th>Subject</th><th>Diagrams</th></tr></thead><tbody>')
    if body.count(marker) != 1:
        raise ValueError('Chapter-index table marker missing or duplicated')
    before, rest = body.split(marker, 1)
    rows_html, after = rest.split('</tbody></table></div>', 1)
    rows = re.findall(r'<tr>.*?</tr>', rows_html, flags=re.S)
    lookup = {}
    for row in rows:
        m = re.search(r'<a class="row-id" href="(\d\d)\.html">', row)
        if not m or m.group(1) in lookup:
            raise ValueError('Chapter-index row cannot be uniquely assigned to a phase')
        lookup[m.group(1)] = row
    expected = set(CHAPTER_PHASE)
    if set(lookup) != expected or len(rows) != 19:
        raise ValueError('Chapter taxonomy does not cover all 19 original chapters')
    out = ['<div class="pfm-cycle-catalog" data-atlas-experience="1">',
           '<p class="pfm-cycle-lede">Browse the same 19 source-linked chapters, organized by '
           'the national budget cycle. Original chapter numbers and URLs are unchanged.</p>',
           _section_nav('chapters')]
    for key, title, numbers in GROUPS:
        if key == 'across':
            numbers = tuple(ch for ch in numbers if ch != '00')
        group_rows = ''.join(lookup[ch] for ch in numbers)
        out.append('<section class="pfm-cycle-index-group" id="cycle-chapters-{}">'
                   '<p class="pfm-cycle-eyebrow">{}</p><h2>{}</h2>'
                   '<div class="table-wrap"><table><thead><tr><th>No.</th><th>Chapter</th>'
                   '<th>Subject</th><th>Diagrams</th></tr></thead><tbody>{}</tbody></table></div>'
                   '</section>'.format(key, 'RELATED AND SHARED' if key == 'across' else 'BUDGET PHASE',
                                      _esc(title), group_rows))
    out.append('</div>')
    return before + ''.join(out) + after


def reorganize_diagram_library(body, diagrams):
    """Reorder the already-rendered original diagram cards into phase sections."""
    import re
    pat = re.compile(r'<section class="diagram-group atlas-diagram-group" id="group-(\d\d)">.*?</section>', re.S)
    matches = list(pat.finditer(body))
    lookup = {}
    for m in matches:
        if m.group(1) in lookup:
            raise ValueError('Duplicated diagram chapter ' + m.group(1))
        lookup[m.group(1)] = m.group(0)
    expected = {d['chapter'] for d in diagrams}
    if set(lookup) != expected or len(matches) != len(expected):
        raise ValueError('Diagram catalogue groups incomplete; refusing partial reorganization')
    out = ['<div class="pfm-cycle-catalog" data-cycle-catalog="diagrams">',
           '<p class="pfm-cycle-lede">The original diagram previews, questions, Mermaid editor '
           'and PNG links are preserved. Browse them by phase or use the filter above.</p>',
           _section_nav('diagrams')]
    for key, title, numbers in GROUPS:
        groups = [lookup[ch] for ch in numbers if ch in lookup]
        if not groups: continue
        out.append('<section class="pfm-cycle-index-group" id="cycle-diagrams-{}">'
                   '<p class="pfm-cycle-eyebrow">{}</p><h2>{}</h2>{}</section>'.format(
                       key, 'RELATED AND SHARED' if key == 'across' else 'BUDGET PHASE',
                       _esc(title), ''.join(groups)))
    out.append('</div>')
    return body[:matches[0].start()] + ''.join(out) + body[matches[-1].end():]


def lesson_index(guides):
    """Primary reading path by phase; the original eight-scene tutorial is retained below."""
    lookup = {g['slug']: g for g in guides}
    targets = {
        'preparation': ('02_budget',),
        'legislation': ('02_budget',),
        'execution': ('03_authority','04_claim','05_treasury'),
        'accountability': ('06_records',),
        'across': ('01_orient','07_beyond','08_integration'),
    }
    if set(lookup) != set(LESSON_PHASES):
        raise ValueError('Guide taxonomy does not cover the eight original lessons')
    out = ['<section class="pfm-cycle-catalog pfm-cycle-lessons" id="lessons-by-phase" '
           'data-cycle-catalog="lessons"><p class="atlas-kicker">Choose a budget-cycle phase</p>',
           '<h2>Find the lesson for the work you are doing.</h2>',
           '<p class="pfm-cycle-lede">The eight original lessons remain available below. '
           'Some lessons cross phases: the proposal-to-GAA lesson belongs to both Preparation and Legislation.</p>',
           _section_nav('walkthrough')]
    for key, title, _ in GROUPS:
        out.append('<section class="pfm-cycle-index-group" id="cycle-guide-{}">'
                   '<p class="pfm-cycle-eyebrow">{}</p><h3>{}</h3><div class="pfm-cycle-lesson-links">'.format(
                       key, 'RELATED AND SHARED' if key == 'across' else 'BUDGET PHASE', _esc(title)))
        for slug in targets[key]:
            g=lookup[slug]
            out.append('<a href="guide/{}.html"><span>{}</span><strong>{}</strong>'
                       '<small>{} read</small></a>'.format(_esc(slug), _esc(g['kicker']),
                                                      _esc(g['name']), _esc(g['time'])))
        out.append('</div></section>')
    out.append('</section>')
    return ''.join(out)


def phase_context(url):
    """Compact, consistent breadcrumbs for original chapter, diagram and lesson pages."""
    import re
    if url.startswith('chapters/') and re.fullmatch(r'chapters/\d\d\.html', url):
        key=CHAPTER_PHASE.get(url.split('/')[-1][:2])
    elif url.startswith('diagrams/') and re.fullmatch(r'diagrams/\d\d[a-z]\.html', url):
        code=url.split('/')[-1][:2]
        key=CHAPTER_PHASE.get(code) if code!='00' else 'across'
    elif url.startswith('guide/') and re.fullmatch(r'guide/\d\d_[a-z]+\.html', url):
        slug=url.split('/')[-1][:-5]
        keys=LESSON_PHASES.get(slug, ())
        if not keys: return ''
        labels=' · '.join('<a href="../walkthrough.html#cycle-guide-{}">{}</a>'.format(
                         k,_esc(PHASE_NAMES[k])) for k in keys)
        return '<nav class="pfm-cycle-context" aria-label="Budget-cycle context">' \
               '<a href="../walkthrough.html">Guided lessons</a> <span> / </span> {}</nav>'.format(labels)
    else:
        return ''
    if not key: return ''
    return ('<nav class="pfm-cycle-context" aria-label="Budget-cycle context">'
            '<a href="../index.html#budget-cycle">Budget cycle</a> <span> / </span>'
            '<a href="../index.html#{}">{}</a> <span> / </span>'
            '<a href="../{}/index.html#cycle-{}-{}">Browse this phase</a>'
            '</nav>').format('phase-' + key if key != 'across' else 'budget-cycle',_esc(PHASE_NAMES[key]),
                            'chapters' if url.startswith('chapters/') else 'diagrams',
                            'chapters' if url.startswith('chapters/') else 'diagrams',key)
