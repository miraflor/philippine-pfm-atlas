"""Practitioner-oriented budget cycle, presentation only.

The sequence is adapted from the DBM budget-cycle illustration; the timing is
indicative. Each step has its own chapter of the atlas, with the same ID (P1 to A9),
and each phase has a chapter that describes it as a whole (P0, L0, E0, A0).
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
        "read": [("The phase as a whole", "P0"), ("Plans, fiscal program and fiscal risks", "P1"),
                 ("The forms of the proposal", "P5"), ("The documents that go to Congress", "P12")],
        "steps": [
            ("Budget Call", "January of the prior FY", "P1"),
            ("Citizen engagement", "Before Tier 1 and Tier 2 proposals", "P2"),
            ("Regional Development Council consultations", "Before Tier 1 and Tier 2 proposals", "P3"),
            ("Program convergence", "Before Tier 1 and Tier 2 proposals", "P4"),
            ("Agency Tier 1 proposals: ongoing expenditures", "February of the prior FY", "P5"),
            ("Tier 1 deliberations", "March of the prior FY", "P6"),
            ("Budget Priorities Framework", "April of the prior FY", "P7"),
            ("Agency Tier 2 proposals: new or expanded spending", "May of the prior FY", "P8"),
            ("Tier 2 deliberations", "June-July of the prior FY", "P9"),
            ("Presentation to the President and Cabinet", "July of the prior FY", "P10"),
            ("Confirmation and finalization", "July of the prior FY", "P11"),
            ("The President's Budget submitted to Congress", "July-August of the prior FY", "P12"),
        ],
    },
    {
        "id": "legislation", "number": "02", "name": "Legislation",
        "when": "Before the budget year",
        "summary": "From the President's proposal to an enacted appropriations law",
        "actors": "House of Representatives; Senate; bicameral conference; President",
        "records": "NEP; General Appropriations Bill (GAB); General Appropriations Act (GAA)",
        "read": [("The phase as a whole", "L0"), ("Kinds of appropriation", "L5")],
        "steps": [
            ("House deliberations", "August-October of the prior FY", "L1"),
            ("Senate deliberations", "September-November of the prior FY", "L2"),
            ("Bicameral deliberations", "November-December of the prior FY", "L3"),
            ("Ratification and enrolment", "December of the prior FY", "L4"),
            ("Enactment of the General Appropriations Act", "December of the prior FY, indicative", "L5"),
        ],
    },
    {
        "id": "execution", "number": "03", "name": "Execution",
        "when": "Before and during the budget year",
        "summary": "From spending authority to contracts, cash allocation and payment",
        "actors": "DBM; implementing agencies; Bureau of the Treasury; banks; suppliers and payees",
        "records": "Budget Execution Documents; allotment/ABM/SARO; NCA; obligation records; disbursement vouchers; payment orders",
        "read": [("The phase as a whole", "E0"), ("Procurement", "E1"), ("Obligation and the claim", "E4"),
                 ("Cash and the Treasury", "E5"), ("Payment", "E6")],
        "steps": [
            ("Early procurement activities", "October-December of the prior FY", "E1"),
            ("Budget execution program", "October-December of the prior FY", "E2"),
            ("Allotment release", "January (comprehensive) and throughout the FY", "E3"),
            ("Obligation", "Throughout the FY", "E4"),
            ("Cash allocation", "January (comprehensive) and throughout the FY", "E5"),
            ("Disbursement", "Throughout the FY", "E6"),
        ],
    },
    {
        "id": "accountability", "number": "04", "name": "Accountability",
        "when": "Before, during and after the budget year",
        "summary": "From performance targets to reporting, review and independent audit",
        "actors": "Implementing agencies; DBM/DBCC; COA; citizens and oversight institutions",
        "records": "Performance targets; budget and financial accountability reports; in-year reports; DBCC reports; audit reports",
        "read": [("The phase as a whole", "A0"), ("Performance information", "A1"), ("Records and reports", "A4"),
                 ("Audit", "A9")],
        "steps": [
            ("Performance targets", "October-December of the prior FY", "A1"),
            ("Citizen engagement", "Throughout the FY", "A2"),
            ("Monitoring and evaluation", "Throughout the FY", "A3"),
            ("Agencies' accountability reports", "Monthly and quarterly", "A4"),
            ("Performance review", "Throughout the FY", "A5"),
            ("In-year reports", "Monthly and quarterly", "A6"),
            ("DBCC Mid-Year Report", "September of the FY", "A7"),
            ("DBCC Year-End Report", "Within the next FY", "A8"),
            ("Audit report", "Within the next FY", "A9"),
        ],
    },
]



# The chapters of each phase: the chapter of the phase as a whole, then the chapters of its steps. The key 'across'
# holds the chapters and diagrams that all phases share.
GROUPS = [
    ('preparation', 'Preparation', tuple('P%d' % i for i in range(13))),
    ('legislation', 'Legislation', tuple('L%d' % i for i in range(6))),
    ('execution', 'Execution', tuple('E%d' % i for i in range(7))),
    ('accountability', 'Accountability', tuple('A%d' % i for i in range(10))),
    ('across', 'Shared by all phases', ('BP', 'IS', 'UACS')),
]
CHAPTER_PHASE = {ch: phase for phase, _, codes in GROUPS for ch in codes if ch != 'BP'}
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
    """Compact four-phase wayfinder; the adjacent illustrated explorer is the one actionable 32-step route."""
    out = [
        '<section id="budget-cycle" class="atlas-story-section pfm-cycle" aria-labelledby="pfm-cycle-title">',
        '<p class="atlas-kicker">The national budget process</p>',
        '<h2 id="pfm-cycle-title">Explore the budget through its four phases.</h2>',
        '<p class="pfm-cycle-lede">The interactive step explorer above opens each of the 32 activities. '
        'Browse the same activities as full chapters, or read an introduction to any phase.</p>',
        _intro_nav(),
        '<p class="pfm-cycle-caveat"><strong>Several budget years overlap.</strong> '
        'The calendar is illustrative, not an authoritative schedule of annual deadlines.</p>',
    ]
    for p in PHASES:
        out.append('<section class="pfm-cycle-phase" id="phase-%s"><div class="pfm-cycle-phase-head">'
                   '<p class="pfm-cycle-eyebrow">PHASE %s</p><h3>%s</h3><p>%s</p></div>'
                   '<p><a href="chapters/index.html#cycle-chapters-%s">Explore the %d activities</a> · '
                   '<a href="chapters/%s0.html">Phase overview</a></p></section>' %
                   (p['id'], p['number'], _esc(p['name']), _esc(p['summary']), p['id'],
                    len(p['steps']), p['id'][0].upper()))
    out.append('<aside class="pfm-cycle-related"><h3>Evidence beyond the expenditure sequence</h3>'
               '<p>The four-line map below explains how legal authority, claims, cash and records interact. '
               '<a href="systems.html">Information systems and UACS</a> support multiple activities.</p></aside>'
               '</section>')
    return '\n'.join(out)


def section_nav(destination):
    """The four phases and the shared chapters, as links to the sections of an index page."""
    return (_intro_nav(destination)
            + '<p class="pfm-cycle-secondary"><a href="#cycle-{}-across">'
            'Shared by all phases</a></p>'.format(destination if destination != 'walkthrough' else 'guide'))


_section_nav = section_nav


def reorganize_diagram_library(body, diagrams):
    """Group the diagram cards (one group per chapter) into the four phases and the shared chapters."""
    import re
    pat = re.compile(r'<section class="diagram-group atlas-diagram-group" id="group-([A-Z][A-Z0-9]*)">.*?</section>', re.S)
    matches = list(pat.finditer(body))
    lookup = {}
    for m in matches:
        if m.group(1) in lookup:
            raise ValueError('Duplicated diagram group ' + m.group(1))
        lookup[m.group(1)] = m.group(0)
    expected = {d['chapter'] for d in diagrams}
    if set(lookup) != expected or len(matches) != len(expected):
        raise ValueError('Diagram catalogue groups incomplete; refusing partial reorganization')
    out = ['<div class="pfm-cycle-catalog" data-cycle-catalog="diagrams">',
           '<p class="pfm-cycle-lede">Browse the diagrams by phase, or use the filter above.</p>',
           section_nav('diagrams')]
    for key, title, codes in GROUPS:
        groups = [lookup[ch] for ch in codes if ch in lookup]
        if not groups:
            continue
        out.append('<section class="pfm-cycle-index-group" id="cycle-diagrams-{}">'
                   '<p class="pfm-cycle-eyebrow">{}</p><h2>{}</h2>{}</section>'.format(
                       key, 'SHARED BY ALL PHASES' if key == 'across' else 'BUDGET PHASE',
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
    """Breadcrumbs for chapter, diagram and lesson pages: the phase to which the page belongs."""
    import re
    m = re.fullmatch(r'chapters/([A-Z][A-Z0-9]*)\.html', url)
    d = re.fullmatch(r'diagrams/([A-Z][A-Z0-9]*)-[a-z]\.html', url)
    if m:
        key = CHAPTER_PHASE.get(m.group(1))
    elif d:
        key = 'across' if d.group(1) == 'BP' else CHAPTER_PHASE.get(d.group(1))
    elif url.startswith('guide/') and re.fullmatch(r'guide/\d\d_[a-z]+\.html', url):
        slug = url.split('/')[-1][:-5]
        keys = LESSON_PHASES.get(slug, ())
        if not keys:
            return ''
        labels = ' · '.join('<a href="../walkthrough.html#cycle-guide-{}">{}</a>'.format(
            k, _esc(PHASE_NAMES[k])) for k in keys)
        return ('<nav class="pfm-cycle-context" aria-label="Budget-cycle context">'
                '<a href="../walkthrough.html">Guided lessons</a> <span> / </span> {}</nav>'.format(labels))
    else:
        return ''
    if not key:
        return ''
    where = 'chapters' if url.startswith('chapters/') else 'diagrams'
    return ('<nav class="pfm-cycle-context" aria-label="Budget-cycle context">'
            '<a href="../index.html#budget-cycle">Budget cycle</a> <span> / </span>'
            '<a href="../index.html#{}">{}</a> <span> / </span>'
            '<a href="../{}/index.html#cycle-{}-{}">Browse this phase</a>'
            '</nav>').format('phase-' + key if key != 'across' else 'budget-cycle', _esc(PHASE_NAMES[key]),
                             where, where, key)
