#!/usr/bin/env python3
"""Site extensions: guided lessons, the page on systems and UACS, and the research models.
Loaded at build time by build_site.py, after the chapters, references and diagrams. The text of the atlas is not
changed here.
"""
from __future__ import annotations
import csv, html, json, re, shutil
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup
import mistune
import forwarding

MD = mistune.create_markdown(escape=False, plugins=['table', 'strikethrough', 'url'])


def esc(x):
    return html.escape(str(x), quote=True)


def build_extensions(c):
    root = c['ROOT']; docs = c['DOCS']; frame = c['frame']; write_page = c['write_page']; search = c['SEARCH']
    diagrams = c['DIAG']; chapter_file = c['CHAPTER_FILE']; chapter_title = c['chapter_title']; relurl = c['relurl']
    guides = json.loads((root / 'content/guides/index.json').read_text(encoding='utf-8'))

    def make_page(url, title, body, description='', section=None, kind='Research models'):
        write_page(url, frame(url, title, body, description=description or title, section=section or url))
        search.append({'t': title, 'p': kind, 'u': url,
                       'x': BeautifulSoup(body, 'html.parser').get_text(' ', strip=True)[:12000]})

    def forward(old, new, label):
        write_page(old, forwarding.page(old, new, label, {}, frame, relurl))

    # --- Guided lessons ---------------------------------------------------------------------------------------
    def changed_guide(html_source):
        soup = BeautifulSoup(html_source, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']; p = urlsplit(href)
            if p.scheme or href.startswith('//'):
                continue
            new = p.path
            if new == '../overview.html':
                new = '../big-picture.html'
            if new.startswith('../reference/') and new.endswith('.html'):
                let = Path(new).name[0].lower()
                if let in 'abcdefg':
                    new = '../reference/' + let + '.html'
            a['href'] = urlunsplit(('', '', new, p.query, p.fragment))
        return str(soup)

    cards = []
    for i, guide in enumerate(guides, 1):
        slug = guide['slug']; url = 'guide/' + slug + '.html'
        current = changed_guide((root / 'content/guides' / f'{slug}.html').read_text(encoding='utf-8'))
        figcards = []
        for did in guide['diagram_ids']:
            d = diagrams[did]
            figcards.append('<a href="../diagrams/%s.html"><img loading="lazy" src="../atlas/%s" alt="%s"><span><strong>%s</strong> · %s</span></a>'
                            % (did, esc(d['image']), esc(d['title']), did, esc(d['title'])))
        chapters = []
        for pid in guide['chapters']:
            if pid not in chapter_file:
                raise SystemExit('lesson %s names an unknown chapter %s' % (slug, pid))
            chapters.append('<li><a href="../chapters/%s.html">Chapter %s · %s</a></li>' % (pid, pid, esc(chapter_title(pid))))
        prev = '../walkthrough.html' if i == 1 else guides[i - 2]['slug'] + '.html'
        nxt = '../models/index.html' if i == len(guides) else guides[i]['slug'] + '.html'
        body = (f'<p class="eyebrow">Guided lesson {i:02d} of 08 · {esc(guide["time"])} reading</p><h1>{esc(guide["name"])}</h1>'
                '<p class="muted">An introduction to the atlas. Consult the linked chapters and source notes before '
                f'operational use.</p><article class="prose-block">{current}</article><section><h2>Inspect these diagrams</h2>'
                f'<div class="guided-diagrams">{"".join(figcards)}</div></section><section><h2>Read the full references</h2>'
                f'<ul>{"".join(chapters)}</ul></section><nav class="pager" aria-label="Lesson navigation"><a href="{prev}">'
                f'← Previous</a><a href="{nxt}">Next →</a></nav>')
        make_page(url, 'Lesson %s: %s' % (i, guide['name']), body, section='walkthrough.html', kind='Walkthrough')
        cards.append('<a class="lesson-card" href="guide/%s.html"><span class="number">Lesson %02d · %s</span><strong>%s</strong>'
                     '<small>Explore %d diagrams and %d chapters →</small></a>'
                     % (slug, i, esc(guide['time']), esc(guide['name']), len(guide['diagram_ids']), len(guide['chapters'])))
    body = ('<p class="eyebrow">Guided walkthrough</p><h1>Understand the system in eight lessons</h1><p class="lead">A '
            'guided route from public priorities and budget authority to procurement, actual cash settlement, concurrent '
            'accounting and the planned IFMIS environment.</p><p>Each lesson points to the diagrams and the chapters of the '
            'atlas, with their sources. This tour is a teaching entry point, not a replacement for procedure-specific '
            'legal controls.</p><div class="lesson-grid">' + ''.join(cards) + '</div><p><a href="big-picture.html">Read the '
            'complete big picture</a> · <a href="reference/f.html">Verify sources</a> · <a href="reference/g.html">Review '
            'open questions</a></p>')
    make_page('walkthrough.html', 'Guided walkthrough', body, kind='Walkthrough')

    # --- Systems and UACS -------------------------------------------------------------------------------------
    essential = [('BP-b', 'Authorities and mandates'), ('BP-h', 'Applications by institution'),
                 ('IS-b', 'System information relationships'), ('IS-c', 'Architecture and exchange claims'),
                 ('UACS-b', 'Document lineage and unique IDs')]
    links = []
    for did, label in essential:
        d = diagrams[did]
        links.append('<a href="diagrams/%s.html"><strong>%s</strong><br><small>%s</small></a>' % (did, esc(label), esc(d['title'])))
    sysbody = ('<p class="eyebrow">Systems and institutional responsibilities</p><h1>Authorities, UACS and IFMIS</h1>'
               '<p class="lead">An authority grants permission. A document records an event. UACS classifies financial '
               'information. An information system may record or exchange that information. These are different '
               'relationships.</p><div class="model-note"><strong>Evidence boundary:</strong> The atlas does not establish '
               'that every depicted system connection is a functioning automated interface. Deployment, exchange mechanism '
               'and reconciliation must be verified individually. Target IFMIS architecture is not production evidence.</div>'
               '<div class="path-grid"><a href="reference/a.html"><strong>Authorities</strong><span>Legally assigned roles '
               'and institutional mandates.</span></a><a href="reference/b.html"><strong>Systems and exchanges</strong><span>'
               'Application inventory and 69 interface/exchange claims with evidence qualifications.</span></a><a '
               'href="chapters/IS.html"><strong>BTMS and IFMIS</strong><span>Chapter IS: the current system landscape and '
               'integration reform.</span></a><a href="chapters/UACS.html"><strong>UACS and record identities</strong><span>'
               'Codes versus individual document and transaction identifiers.</span></a></div>'
               '<h2>Five diagrams to begin with</h2><div class="model-grid">' + ''.join(links) + '</div><h2>Research '
               'models</h2><p>Models of the identity of records, of the evidence for interfaces, of failed exchanges and '
               'of versioned UACS codes are kept apart as <a href="models/index.html">research models</a>, each with a note '
               'on what it is for.</p>')
    make_page('systems.html', 'Authorities, systems and UACS', sysbody, kind='Systems and UACS')

    # --- Research models --------------------------------------------------------------------------------------
    modelroot = root / 'research_models'; published = docs / 'models'
    shutil.copytree(modelroot / 'diagrams', published / 'diagrams')
    shutil.copytree(modelroot / 'registers', published / 'registers')
    if (modelroot / 'rendered').is_dir():
        shutil.copytree(modelroot / 'rendered', published / 'rendered')
    (published / 'reference').mkdir(exist_ok=True)
    shutil.copy2(modelroot / 'registers' / 'interface_register.csv', published / 'reference' / 'interface_register.csv')
    models = json.loads((modelroot / 'models_index.json').read_text(encoding='utf-8'))
    own_refs = {p.name[0] for p in (modelroot / 'reference').glob('[A-Z]_*.md')}
    references = []
    for mdpath in sorted((modelroot / 'reference').glob('[A-Z]_*.md')):
        letter = mdpath.name[0]
        shutil.copy2(mdpath, published / 'reference' / mdpath.name)
        soup = BeautifulSoup(MD(mdpath.read_text(encoding='utf-8')), 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']; p = urlsplit(href)
            if p.scheme or href.startswith('//') or href.startswith('#'):
                continue
            new = p.path
            m = re.match(r'^(?:\.\./reference/)?([A-Z])_[a-z_]+\.md$', new)
            if m:
                new = (m.group(1).lower() + '.html') if m.group(1) in own_refs else '../../reference/%s.html' % m.group(1).lower()
            elif new.endswith('.csv') and '/' not in new and (modelroot / 'registers' / new).is_file():
                new = '../registers/' + new
            a['href'] = urlunsplit(('', '', new, p.query, p.fragment))
        intro = ('<div class="model-note"><strong>Research reference.</strong> Proposed modelling material, not a chapter '
                 'of the atlas and not an official information-system specification.</div>')
        h1 = soup.find('h1'); title = h1.get_text(' ', strip=True) if h1 else mdpath.stem
        make_page('models/reference/%s.html' % letter.lower(), title,
                  intro + '<article class="prose">' + str(soup) + '</article><p><a href="../index.html">← Research models</a></p>')
        # K/L are retained as unlisted historical research records, not promoted into the current navigation.
        if letter not in ('K','L'):
            references.append((letter, title))
    registries = []
    for f in sorted((modelroot / 'registers').glob('*.csv')):
        with f.open(encoding='utf-8-sig', newline='') as fp:
            rows = list(csv.DictReader(fp))
            cols = list(rows[0]) if rows else []
        htmlrows = ['<tr>' + ''.join('<td>' + esc(str(r.get(col, ''))[:170]) + '</td>' for col in cols[:6]) + '</tr>' for r in rows[:10]]
        table = ('<div class="table-scroll"><table><thead><tr>' + ''.join('<th>' + esc(k) + '</th>' for k in cols[:6])
                 + '</tr></thead><tbody>' + ''.join(htmlrows) + '</tbody></table></div>')
        name = f.stem.replace('_', ' ').title()
        body = ('<p class="eyebrow">Research register</p><h1>' + esc(name) + '</h1><p class="model-note">This CSV is a '
                'research register, not an export from BTMS or from another operational system. The table shows the '
                'first 10 of its ' + str(len(rows)) + ' records.</p><p><a href="registers/' + f.name + '" download>'
                'Download the complete CSV</a></p>' + table + '<p><a href="index.html">← Research models</a></p>')
        ident = f.stem.replace('_', '-')
        make_page('models/' + ident + '.html', name, body)
        registries.append((ident, name, len(rows)))
    for item in models:
        mid = item['id']; code = (modelroot / item['path']).read_text(encoding='utf-8-sig')
        image = ''
        png = published / 'rendered' / (Path(item['filename']).stem + '.png')
        if png.is_file():
            image = ('<figure class="diagram"><a href="rendered/%s"><img src="rendered/%s" alt="Research model %s: %s" '
                     'loading="lazy"></a></figure>' % (png.name, png.name, mid, esc(item['title'])))
        notation = 'Mermaid' if item['kind'] == 'mermaid' else 'PlantUML'
        body = ('<p class="eyebrow">Research model ' + esc(mid) + '</p><h1>' + esc(item['title']) + '</h1>'
                '<div class="model-note"><p><strong>What it is for.</strong> ' + esc(item['purpose']) + '</p>'
                '<p><strong>Why it is not in a chapter.</strong> ' + esc(item['not_in_a_chapter']) + '</p></div>'
                + image + '<p><strong>Notation:</strong> ' + notation + ' · <a href="' + esc(item['path']) + '" download>'
                'Download the code</a></p><h2>Code</h2><div class="copy-row"><button type="button" data-copy="model-'
                + esc(mid) + '">Copy the code</button></div><pre class="model-code" id="model-' + esc(mid) + '"><code '
                'class="model-source">' + esc(code) + '</code></pre><p><a href="index.html">← All research models</a></p>')
        make_page('models/%s.html' % mid, 'Research model %s: %s' % (mid, item['title']), body)
    # Restore the entire source-only analytical collection, not just models considered non-redundant.
    # This collection is not another public chapter structure. An old research sketch must never be
    # silently replaced by a different current operational diagram merely because the topics overlap.
    supplemental = modelroot / 'supplemental_index.json'
    retained_supplemental = []
    if supplemental.is_file():
        entries = json.loads(supplemental.read_text(encoding='utf-8'))
        if len(entries) != 25 or len({x['id'] for x in entries}) != 25:
            raise ValueError('Preserved analytical collection must contain all 25 distinct sketches')
        for entry in entries:
            rel = Path(entry['path'])
            if rel.is_absolute() or '..' in rel.parts:
                raise ValueError('Unsafe analytical source location: ' + str(rel))
            source = modelroot / rel
            if not source.is_file():
                raise ValueError('Missing preserved model source: ' + str(source))
            code = source.read_text(encoding='utf-8-sig')
            mid = entry['id']
            label = rel.stem.replace('_', ' ').replace('-', ' ')
            category = 'Mermaid' if entry['kind'] == 'mermaid' else 'PlantUML'
            content = ('<p class="eyebrow">Supplementary analytical sketch</p><h1>' + esc(label) + '</h1>'
                       '<p class="model-note"><strong>Source-only analytical sketch.</strong> This model is '
                       'exploratory and is not evidence of an operational interface or a universal government process. '
                       'It is retained for analysis, not substituted for a diagram that answers a narrower question.</p>'
                       '<p><strong>Notation:</strong> ' + category + ' · <a href="' + esc(entry['path']) + '" download>'
                       'Get source code</a></p><h2>Source</h2><pre class="model-code"><code class="model-source">'
                       + esc(code) + '</code></pre><p><a href="index.html">← Analytical models</a></p>')
            make_page('models/model-%s.html' % mid, 'Supplementary model: ' + label, content)
            retained_supplemental.append((mid, label))
    supplemental_cards = ''.join('<a class="model-card" href="model-%s.html"><strong>%s</strong>'
                                 '<small>Source-only supplementary analysis</small></a>' % (esc(i), esc(label))
                                 for i, label in retained_supplemental)
    cards = ''.join('<a class="model-card" href="%s.html"><strong>%s · %s</strong><small>%s</small></a>'
                    % (esc(m['id']), esc(m['id']), esc(m['title']), esc(m['purpose'])) for m in models)
    reference_cards = ''.join('<a class="model-card" href="reference/%s.html"><strong>%s</strong><small>Research reference</small></a>'
                              % (x.lower(), esc(t)) for x, t in references)
    regcards = ''.join('<a class="model-card" href="%s.html"><strong>%s</strong><small>%d records · downloadable CSV</small></a>'
                       % (ident, esc(name), n) for ident, name, n in registries)
    body = ('<p class="eyebrow">Research models</p><h1>Research models and registers</h1><p class="lead">%d research models, '
            '%d research references and %d registers of typed events, records, rules, authorities and interfaces.</p>'
            '<div class="model-note"><strong>Not part of the chapters.</strong> A research model is a proposal, a method or a '
            'general model. It is not a description of Philippine PFM from a source, so it is kept apart from the '
            'chapters. Each model page says what the model is for, and why it is not in a chapter.</div>'
            '<h2>The research models</h2><div class="model-grid">%s</div>'
            '<h2>Additional analytical sketches</h2><p>Supplementary source-only models remain available in full; '
            'conceptual similarity does not establish equivalence.</p><div class="model-grid">%s</div>'
            '<h2>Research references</h2><div class="model-grid">%s</div>'
            '<h2>Research registers</h2><div class="model-grid">%s</div>'
            '<p><a href="../big-picture.html">Read the big picture</a> · <a href="../systems.html">Authorities, systems and '
            'UACS</a> · <a href="../reference/g.html">Open points</a></p>'
            % (len(models) + len(retained_supplemental), len(references), len(registries), cards, supplemental_cards, reference_cards, regcards))
    make_page('models/index.html', 'Research models and registers', body)

    # --- Pages at addresses that the site no longer uses ------------------------------------------------------
    rf = json.loads((root / 'tools' / 'research_forwarding.json').read_text(encoding='utf-8'))
    for old, new in rf['kept'].items():
        if not any(mid == old for mid, _ in retained_supplemental):
            forward('models/model-%s.html' % old, 'models/%s.html' % new, 'research model %s' % new)
    for old, did in rf['redundant'].items():
        # Only use a fallback forwarding page if the preserved model source genuinely is unavailable.
        # Do not redirect a broadly scoped research sketch to a narrower current-procedure diagram.
        if not any(mid == old for mid, _ in retained_supplemental):
            forward('models/model-%s.html' % old, 'diagrams/%s.html' % did, 'diagram %s: %s' % (did, diagrams[did]['title']))
    forward('models/history.html', 'models/index.html', 'the research models')
    for letter in 'kl':
        if letter.upper() not in own_refs:
            forward('models/reference/%s.html' % letter, 'models/index.html', 'the research models')
    forward('overview.html', 'big-picture.html', 'the big picture')
    for source in c['REFERENCES']:
        forward('reference/' + source.stem + '.html', 'reference/' + source.name[0].lower() + '.html',
                c['TITLE']['reference/' + source.name])
    print('extensions: guided lessons', len(guides), 'research models', len(models), 'research registers', len(registries))
