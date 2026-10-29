"""Presentation-only enhancements for Philippine PFM Atlas.

Retains the source-backed text, documents, citations, PNGs, and diagram code.
This file is called by tools/build_site.py and by apply_patch.py when
updating the currently published static HTML. Python stdlib only.
"""
from __future__ import annotations
import html
import json
import math
import re
from pathlib import Path
from budget_cycle_nav import (home_cycle, reorganize_diagram_library, lesson_index, phase_context)
from budget_cycle_story import SLOT as CYCLE_STORY_SLOT
from budget_cycle_story import STEP as ACTIVITY_EVIDENCE, PHASES as ACTIVITY_PHASES
from atlas_pages import STEP_ORDER

ROOT = Path(__file__).resolve().parent.parent if Path(__file__).name == 'site_experience.py' and Path(__file__).parent.name == 'tools' else None
# Overlay source is alongside apply_patch.py until installed under tools/.
if ROOT is None:
    ROOT = Path(__file__).resolve().parent

MARK = 'data-atlas-experience="1"'

def esc(s):
    return html.escape(str(s), quote=True)


def enhance_page(url: str, body: str, diagrams: list[dict]) -> str:
    """Idempotent: eligible pages get additional presentation, not new facts."""
    if MARK in body:
        return body
    if url == 'index.html':
        return home(body)
    if url == 'walkthrough.html':
        return walkthrough(body, diagrams)
    if url == 'diagrams/index.html':
        return library(body, diagrams)
    if url == 'about.html':
        return about(body)
    if url.startswith(('chapters/', 'diagrams/', 'guide/')):
        context = phase_context(url)
        if context:
            if url.startswith('chapters/'):
                pid = url.split('/')[-1].split('.')[0]
                return context + activity_reading_guide(pid) + body
            return context + body
    return body


# The source corpus remains word-for-word intact. These are reading aids, not new legal claims.
# Some activity chapters have only their verified step tables, while broader source chapters
# also include technical domains larger than the activity after which they are named.
THIN_ACTIVITIES = frozenset(('P2 P3 P4 P6 P7 P8 P9 P10 P11 L1 L2 L3 L4 E2 A7 A8').split())
WIDE_CONTEXT = {
    'P1': 'Planning, macro-fiscal programming and fiscal risks support the Budget Call; they are not all actions performed at P1.',
    'E1': 'The detailed procurement lifecycle below extends beyond the early procurement activity itself.',
    'E3': 'The discussion of local-government finance describes a related but distinct budgeting pathway.',
    'E4': 'Payroll and personnel administration are related expenditure cases, not synonymous with recording an obligation.',
    'E5': 'Revenue collection, borrowing and debt are broader treasury topics, not parts of the NCA issuance step.',
    'E6': 'Fund clusters and other institutional pathways are related disbursement contexts, not one standard payment workflow.',
    'A4': 'Asset and property accounting provides supporting context; it is not the whole of agency accountability reporting.',
}


def activity_reading_guide(pid):
    """Expose exact evidence locations and honest scope boundaries, with no fabricated procedure."""
    if pid not in STEP_ORDER:
        return ''
    info = ACTIVITY_EVIDENCE[pid]
    phase = next(p for p in ACTIVITY_PHASES if p['id'].upper().startswith(pid[0]))
    labels = {p['id']: p['name'] for p in ACTIVITY_PHASES}
    name = next(name for p in ACTIVITY_PHASES for name, _, id_ in p['steps'] if id_ == pid)
    links = []
    seen = set()
    for chapter, section in info.get('refs', []):
        url = '../chapters/%s.html%s' % (chapter, '#section-' + section.replace('.', '-') if section else '')
        if url not in seen:
            seen.add(url)
            links.append('<a href="%s">%s evidence%s</a>' % (esc(url), esc(chapter),
                         (', section ' + esc(section)) if section else ''))
    for did in info.get('dg', []):
        links.append('<a href="../diagrams/%s.html">Diagram %s</a>' % (esc(did), esc(did)))
    if not links:
        # No source-specific authority is established by absence of a diagram or section link.
        links.append('<a href="../reference/f.html">Source verification ledger</a>')
    if pid in THIN_ACTIVITIES:
        status = ('The source corpus does not provide a self-contained account of this exact activity. '
                  'Its step table records what is supported; the links below lead to relevant phase or '
                  'technical evidence. Do not treat the budget-cycle illustration alone as a procedural rule.')
    elif pid in WIDE_CONTEXT:
        status = WIDE_CONTEXT[pid]
    else:
        return ''
    return ('<aside class="activity-reading" aria-label="Reading guide for this activity">'
            '<p class="atlas-kicker">Evidence and scope</p><p>%s</p>'
            '<div class="activity-reading-links">%s</div></aside>' % (esc(status), ' · '.join(links)))


def hero_threads():
    colors = ['#1f4e8c', '#2e6b2e', '#a35200', '#747474']
    labels = ['Legal authority', 'The claim', 'Cash', 'Records & control']
    out = ['<svg viewBox="0 0 920 310" role="img" aria-labelledby="atlas-hero-title atlas-hero-desc" xmlns="http://www.w3.org/2000/svg">',
        '<title id="atlas-hero-title">Four concurrent lines of public financial management</title>',
        '<desc id="atlas-hero-desc">Authority, claim, cash and recording progress concurrently. A payment depends on the relevant conditions meeting; it is not a single linear chain.</desc>',
        '<g class="thread-guide">']
    for i, (color,label) in enumerate(zip(colors,labels)):
        y = 46+i*69
        out.append(f'<text x="19" y="{y-14}" class="thread-title" fill="{color}">{esc(label)}</text>')
        out.append(f'<path d="M24 {y} H896" stroke="{color}" class="thread-track"/>')
        out.append(f'<path d="M24 {y} H896" stroke="{color}" class="thread-flow thread-{i}"/>')
        for x in (220,480,705):
            out.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#ffffff" stroke="{color}" stroke-width="3"/>')
    out.append('</g>')
    for x,y,label in [(480,115,'01'),(705,115,'02'),(790,184,'03')]:
        out.append(f'<circle cx="{x}" cy="{y}" r="19" class="thread-meet"/><text x="{x}" y="{y+5}" class="thread-num" text-anchor="middle">{label}</text>')
    out.append('</svg>')
    return ''.join(out)


def home(body):
    if '<div class="home">' not in body:
        raise ValueError('Homepage structure changed: .home not found')
    body=body.replace('<div class="home">', '<div class="home atlas-experience" '+MARK+'>',1)
    body=body.replace('<section class="home-intro">', '<section class="home-intro atlas-home-hero"><p class="atlas-kicker">An atlas of public financial management · Philippines</p>',1)
    body=body.replace('<h1>Philippine PFM Atlas</h1>', '<div class="atlas-home-grid"><div class="atlas-home-headline"><h1>Follow the <em>budget cycle.</em></h1><p class="atlas-identity">Philippine PFM Atlas</p><a class="atlas-home-jump" href="#budget-cycle">Explore the budget cycle ↓</a></div><div class="atlas-home-explainer">',1)
    body=body.replace('</section>\n<section class="start-paths"', '</div></div></section>\n<section class="start-paths"',1)
    nav='''<nav class="atlas-page-wayfinder" aria-label="Explore this page">
<a href="#budget-cycle"><span>01</span> Budget cycle</a><a href="#phase-preparation"><span>02</span> Preparation</a><a href="#phase-legislation"><span>03</span> Legislation</a><a href="#phase-execution"><span>04</span> Execution</a><a href="#phase-accountability"><span>05</span> Accountability</a><a href="#lines"><span>06</span> Systems map</a><a href="#reference-files"><span>07</span> References</a><a href="#reliability"><span>08</span> Evidence</a></nav>'''
    body=body.replace('</section>\n<section class="start-paths"', '</section>'+nav+'\n<section class="start-paths"',1)
    accents={'lines':'01 / A system of concurrent processes', 'meeting-points':'02 / Conditions before payment',
             'parts':'03 / Navigate the process', 'reference-files':'04 / Explore the evidence', 'reliability':'05 / Limits and uncertainties'}
    for ident,kicker in accents.items():
        body=body.replace(f'<section id="{ident}">',f'<section id="{ident}" class="atlas-story-section"><p class="atlas-kicker">{kicker}</p>',1)
    controls='''<div class="atlas-map-controls" role="group" aria-label="Highlight a line of public financial management">
<button type="button" data-atlas-line="all" aria-pressed="true">All four lines</button>
<button type="button" data-atlas-line="authority" aria-pressed="false">Legal authority</button>
<button type="button" data-atlas-line="claim" aria-pressed="false">The claim</button>
<button type="button" data-atlas-line="cash" aria-pressed="false">Cash</button>
<button type="button" data-atlas-line="records" aria-pressed="false">Records &amp; control</button></div>'''
    body=body.replace('How do the parts of Philippine public financial management (PFM) relate to each other: the functions, the authorities that perform them, the information systems that these authorities use, and the records that pass from one to the next?', 'Begin with Preparation, Legislation, Execution and Accountability. At each step, examine the institutions, documents, information systems and controls.', 1)
    body=body.replace('<div class="map">',controls+'<div class="map" data-highlight-line="all">',1)
    body=body.replace('<section class="start-paths"', '<section class="start-paths atlas-story-section"',1)
    body=body.replace('<section class="start-paths atlas-story-section"', CYCLE_STORY_SLOT + '\n' + home_cycle() + '\n<section class="start-paths atlas-story-section"', 1)
    return body


LESSON_COPY={
 '01_orient':'Locate the institutions, records and exchanges before following any single transaction.',
 '02_budget':'Trace how priorities and proposals become appropriations through the budget process.',
 '03_authority':'Distinguish permission to incur an obligation from permission and resources to pay it.',
 '04_claim':'Follow procurement, delivery, acceptance and the conditions that make payment due.',
 '05_treasury':'Examine collection, cash management and the mechanisms for settling a payment.',
 '06_records':'Follow the records created by events, the reconciliations, and subsequent oversight.',
 '07_beyond':'Explore important pathways and obligations that do not fit a single purchasing example.',
 '08_integration':'Consider UACS, record identities and what is—and is not—known about systems integration.',
}

def lesson_orbit():
    items=['Orient','Decide','Authorize','Verify','Settle','Account','Beyond','Connect']
    out=['<svg class="atlas-orbit" viewBox="0 0 420 390" role="img" aria-labelledby="atlas-orbit-title atlas-orbit-desc">',
         '<title id="atlas-orbit-title">Eight perspectives on public financial management</title>',
         '<desc id="atlas-orbit-desc">Eight thematic lessons arranged around a common system, rather than presented as a single sequential approval flow.</desc>',
         '<circle cx="210" cy="193" r="135" fill="none" stroke="currentColor" opacity=".14" stroke-dasharray="3 9"/>',
         '<circle cx="210" cy="193" r="77" fill="none" stroke="currentColor" opacity=".07"/>',
         ]
    for i,name in enumerate(items,1):
        angle=-math.pi/2+(i-1)*math.pi/4
        x=210+135*math.cos(angle); y=193+135*math.sin(angle)
        out.append(f'<g class="atlas-orbit-item" data-orbit="{i}">')
        out.append(f'<line x1="210" y1="193" x2="{x:.2f}" y2="{y:.2f}" class="atlas-orbit-spoke"/>')
        out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="19" class="atlas-orbit-node"/>')
        out.append(f'<text x="{x:.2f}" y="{y+5:.2f}" class="atlas-orbit-number" text-anchor="middle">{i:02}</text>')
        # Labels are kept separate in the lesson story cards for readability.
        out.append('</g>')
    out += ['<circle class="atlas-orbit-hub" cx="210" cy="193" r="57"/>',
            '<text x="210" y="187" text-anchor="middle" class="atlas-orbit-label">PFM</text>',
            '<text x="210" y="205" text-anchor="middle" class="atlas-orbit-sub">ONE SYSTEM</text>']
    out.append('</svg>')
    return ''.join(out)


def walkthrough(body, diagrams):
    if '<div class="lesson-grid">' not in body:
        raise ValueError('Walkthrough structure changed: .lesson-grid not found')
    root=ROOT
    path=root/'content'/'guides'/'index.json'
    if not path.exists():
        raise ValueError(f'Guide metadata missing: {path}')
    guides=json.loads(path.read_text(encoding='utf-8'))
    lookup={d['id']:d for d in diagrams}
    cards=[]
    for i,g in enumerate(guides,1):
        if not g.get('diagram_ids') or g['diagram_ids'][0] not in lookup:
            raise ValueError('Missing diagram metadata for lesson '+g['slug'])
        first=lookup[g['diagram_ids'][0]]
        path='atlas/'+first['image']
        title=g['name']; slug=g['slug']
        cards.append(f'''<article class="atlas-lesson-scene" id="lesson-{i:02d}" data-lesson="{i}" data-preview="{esc(path)}" data-preview-id="{esc(first['id'])}" data-preview-title="{esc(first['title'])}">
<div class="atlas-lesson-index"><span>LESSON {i:02d}</span><span>{esc(g['time'])} read</span></div>
<p class="atlas-scene-kicker">{esc(g['kicker'])}</p><h2>{esc(title)}</h2>
<p>{esc(LESSON_COPY[slug])}</p>
<p class="atlas-scene-meta">{len(g['diagram_ids'])} diagrams · {len(g['chapters'])} {"chapter" if len(g['chapters'])==1 else "chapters"}</p>
<a class="atlas-lesson-link" href="guide/{esc(slug)}.html">Read this lesson <span aria-hidden="true">↗</span></a>
<a class="atlas-lesson-preview-link" href="diagrams/{esc(first['id'])}.html">Explore diagram {esc(first['id'])} ↗</a>
</article>''')
    first=lookup[guides[0]['diagram_ids'][0]]
    intro='''<div class="atlas-walk-intro" '''+MARK+'''><p class="atlas-kicker">Eight lenses on one interconnected system</p><div class="atlas-walk-decoration" aria-hidden="true"><span></span><span></span><span></span><span></span></div></div>'''
    body=intro+body
    body=body.replace('<div class="lesson-grid">', lesson_index(guides) + '''<div class="atlas-walk-layout">
<aside class="atlas-walk-pin" aria-label="Lesson visualisation">
<div class="atlas-walk-pin-inner"><p class="atlas-kicker">CURRENT PERSPECTIVE <strong id="atlas-active-number">01 / 08</strong></p>
'''+lesson_orbit()+f'''<div class="atlas-live-figure"><div class="atlas-live-figure-bar"><span>DIAGRAM PREVIEW</span><a id="atlas-active-diagram-link" href="diagrams/{esc(first['id'])}.html">Explore diagram ↗</a></div>
<img id="atlas-active-diagram" src="atlas/{esc(first['image'])}" alt="Diagram {esc(first['id'])}: {esc(first['title'])}" loading="eager"></div>
<p class="atlas-visual-note">These lessons are perspectives on interrelated processes, not eight compulsory steps in one transaction.</p></div></aside>
<div class="atlas-walk-scenes">'''+''.join(cards)+'''</div></div><div class="atlas-all-lessons"><h2>All eight lessons at a glance</h2><div class="lesson-grid">''',1)
    # close original lesson-grid followed by its existing paragraphs
    ending='</div><p><a href="big-picture.html">'
    if ending not in body:
        raise ValueError('Walkthrough closing marker missing')
    body=body.replace(ending,'</div></div><p><a href="big-picture.html">',1)
    return body


def library(body,diagrams):
    if 'class="diagram-group"' not in body:
        raise ValueError('Diagram library structure changed')
    n_mermaid=sum(1 for d in diagrams if d['notation']=='Mermaid')
    n_puml=len(diagrams)-n_mermaid
    hero=f'''<div class="atlas-catalog-hero" {MARK}><p class="atlas-kicker">Visual index · An atlas to explore</p><div class="atlas-catalog-heading"><div><p class="atlas-catalog-overline">DIAGRAM LIBRARY</p><h1>See the system.<br><em>Explore its forms.</em></h1><p>Browse the existing diagrams by chapter, question and notation. Open any card for its explanation, original image, source code and interactive Mermaid view where available.</p></div>
<div class="atlas-catalog-stat" aria-label="Diagram counts"><strong>{len(diagrams)}</strong><span>diagrams in the atlas</span><div><b>{n_mermaid}</b> Mermaid <b>{n_puml}</b> PlantUML</div></div></div></div>'''
    body=hero+body
    # Keep original title and explanatory paragraph, only restyle it (no content removed).
    body=body.replace('<div class="doc-head"><p class="eyebrow">Diagrams</p><h1>The diagrams</h1></div>',
                      '<div class="doc-head atlas-catalog-original"><p class="eyebrow">Reference catalogue</p><h2>The diagrams</h2></div>',1)
    data={d['id']:d for d in diagrams}
    def make_group(m):
        ident=m.group(1)
        heading=m.group(2)
        entries=[d for d in diagrams if d['chapter']==ident]
        if not entries:
            raise ValueError('No diagrams for chapter '+ident)
        cards=[]
        for d in entries:
            did=d['id']
            cards.append(f'''<li class="atlas-diagram-card"><a class="atlas-diagram-card-link" href="{esc(did)}.html">
<div class="atlas-diagram-thumb"><img loading="lazy" decoding="async" src="../atlas/{esc(d['image'])}" alt="Preview of diagram {esc(did)}"/><span class="atlas-diagram-id">{esc(did)}</span></div>
<div class="atlas-diagram-content"><span class="form">{esc(d['form'])}</span><strong>{esc(d['title'])}</strong><span class="q">Question: {esc(d['question'])}</span><span class="atlas-open-caption">Open diagram <span aria-hidden="true">↗</span></span></div>
</a></li>''')
        label = 'THE BIG PICTURE' if ident == 'BP' else 'CHAPTER ' + ident
        return f'''<section class="diagram-group atlas-diagram-group" id="group-{esc(ident)}"><div class="atlas-diagram-group-head"><div><span class="atlas-chapter-label">{esc(label)}</span><h2 id="chapter-{esc(ident)}">{heading}</h2></div><span class="atlas-group-count">{len(entries)} {"diagram" if len(entries)==1 else "diagrams"}</span></div><ul class="diagram-list atlas-diagram-grid">{''.join(cards)}</ul></section>'''
    regex=re.compile(r'<section class="diagram-group"><h2 id="chapter-([A-Z][A-Z0-9]*)">(.*?)</h2><ul class="diagram-list">.*?</ul></section>',re.S)
    body,n=regex.subn(make_group,body)
    if n!=len({d['chapter'] for d in diagrams}):
        raise ValueError(f'Library transformed {n} groups, expected {len(set(d["chapter"] for d in diagrams))}')
    return reorganize_diagram_library(body, diagrams)


# PFM ATLAS BALANCED HERO + ABOUT COLOPHON v1
def about(body):
    """Place authorship and AI disclosure after the unchanged documentation."""
    content = '<section class="atlas-about-colophon" data-atlas-experience="1" aria-labelledby="atlas-colophon-heading">\n<h2 id="atlas-colophon-heading">Authorship and methods</h2>\n<p>The Philippine PFM Atlas is an AI-assisted project. AI tools supported research organization, drafting, code and diagram development. The author directs the work and is responsible for the published material, including its interpretations, corrections, and limitations.</p>\n<p>The atlas is an independent reference, not an official publication or endorsement of the University of the Philippines Diliman, the Scientific Computing Laboratory, or any Philippine government institution. Readers should consult the cited primary sources and recorded open questions.</p>\n<p class="atlas-colophon-signature">Developed and maintained by <strong>James Matthew Miraflor</strong> · Graduate student, Department of Computer Science, University of the Philippines Diliman · Scientific Computing Laboratory.</p>\n</section>'
    return body + "\n" + content
