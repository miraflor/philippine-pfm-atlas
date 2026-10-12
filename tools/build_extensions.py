#!/usr/bin/env python3
"""Site extensions: guided lessons, systems route, version-separated research models.
Loaded at build time by build_site.py after the 12 October corpus has been rendered.
No changes to the underlying current atlas text or its diagrams.
"""
from __future__ import annotations
import csv, html, json, re, shutil
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup
import mistune
MD=mistune.create_markdown(escape=False,plugins=['table','strikethrough','url'])

def esc(x): return html.escape(str(x),quote=True)


def build_extensions(c):
    root=c['ROOT']; docs=c['DOCS']; atlas=c['ATLAS']; read=c['read']; frame=c['frame']; save=c['save']; write_page=c['write_page']; search=c['SEARCH']; diagrams=c['DIAG']; titles=c['TITLE']; chapter_sources=c['CHAPTERS']
    guides=json.loads((root/'content/guides/index.json').read_text(encoding='utf-8'))
    def make_page(url,title,body,description='',section=None):
        write_page(url,frame(url,title,body,description=description or title,section=section or url))
        search.append({'t':title,'p':'Walkthrough' if url.startswith('guide/') or url=='walkthrough.html' else 'Research models' if url.startswith('models/') else 'Systems and UACS','u':url,'x':BeautifulSoup(body,'html.parser').get_text(' ',strip=True)[:12000]})
    def changed_guide(html_source):
        soup=BeautifulSoup(html_source,'html.parser')
        for a in soup.find_all('a',href=True):
            href=a['href']; p=urlsplit(href)
            if p.scheme or href.startswith('//'): continue
            new=p.path
            if new=='../overview.html': new='../big-picture.html'
            if new.startswith('../processes/') and new.endswith('.html'):
                code=Path(new).name[:2]
                if code.isdigit(): new='../chapters/'+code+'.html'
            if new.startswith('../reference/') and new.endswith('.html'):
                let=Path(new).name[0].lower()
                if let in 'abcdefg':new='../reference/'+let+'.html'
            a['href']=urlunsplit(('', '', new,p.query,p.fragment))
        return str(soup)
    cards=[]
    for i,guide in enumerate(guides,1):
        slug=guide['slug']; url='guide/'+slug+'.html'
        current=changed_guide((root/'content/guides'/f'{slug}.html').read_text(encoding='utf-8'))
        figcards=[]
        for did in guide['diagram_ids']:
            d=diagrams[did]
            figcards.append('<a href="../diagrams/%s.html"><img loading="lazy" src="../atlas/%s" alt="%s"><span><strong>%s</strong> · %s</span></a>'%(did,esc(d['image']),esc(d['title']),did,esc(d['title'])))
        chapters=[]
        for source in guide['chapters']:
            chap=source[:2]
            try:title=next(p.name for p in chapter_sources if p.name[:2]==chap)
            except StopIteration:continue
            chapters.append('<li><a href="../chapters/%s.html">Chapter %s · %s</a></li>'%(chap,chap,esc(titles['processes/'+title])))
        prev='../walkthrough.html' if i==1 else guides[i-2]['slug']+'.html'
        nxt='../models/index.html' if i==len(guides) else guides[i]['slug']+'.html'
        body=f'<p class="eyebrow">Guided lesson {i:02d} of 08 · {esc(guide["time"])} reading</p><h1>{esc(guide["name"])}</h1><p class="muted">An introduction to the current procedural atlas; consult linked chapters and source notes before operational use.</p><article class="prose-block">{current}</article><section><h2>Inspect these diagrams</h2><div class="guided-diagrams">{"".join(figcards)}</div></section><section><h2>Read the full references</h2><ul>{"".join(chapters)}</ul></section><nav class="pager" aria-label="Lesson navigation"><a href="{prev}">← Previous</a><a href="{nxt}">Next →</a></nav>'
        make_page(url,'Lesson %s: %s'%(i,guide['name']),body,section='walkthrough.html')
        cards.append('<a class="lesson-card" href="guide/%s.html"><span class="number">Lesson %02d · %s</span><strong>%s</strong><small>Explore %d diagrams and %d full chapters →</small></a>'%(slug,i,esc(guide['time']),esc(guide['name']),len(guide['diagram_ids']),len(guide['chapters'])))
    body='<p class="eyebrow">Guided walkthrough</p><h1>Understand the system in eight lessons</h1><p class="lead">A guided route from public priorities and budget authority to procurement, actual cash settlement, concurrent accounting and the planned IFMIS environment.</p><p>The lessons come from the walkthrough edition; each now points into the reference edition’s stable diagrams and fully source-linked chapters. This tour is a teaching entry point, not a replacement for procedure-specific legal controls.</p><div class="lesson-grid">'+''.join(cards)+'</div><p><a href="big-picture.html">Read the complete big picture</a> · <a href="reference/f.html">Verify sources</a> · <a href="reference/g.html">Review open questions</a></p>'
    make_page('walkthrough.html','Guided walkthrough',body)

    # Architecture landing page: link to original source-backed chapter and reference, not newly assert an interface.
    essential=[('00b','Authorities and mandates'),('00c','Applications by institution'),('16b','System information relationships'),('16g','Architecture and exchange claims'),('17b','Document lineage and unique IDs')]
    links=[]
    for did,label in essential:
        if did in diagrams:
            d=diagrams[did]
            links.append('<a href="diagrams/%s.html"><strong>%s</strong><br><small>%s</small></a>'%(did,esc(label),esc(d['title'])))
    sysbody='''<p class="eyebrow">Systems and institutional responsibilities</p><h1>Authorities, UACS and IFMIS</h1><p class="lead">An authority grants permission. A document records an event. UACS classifies financial information. An information system may record or exchange that information. These are different relationships.</p>
    <div class="model-note"><strong>Evidence boundary:</strong> The present atlas does not establish that every depicted system connection is a functioning automated interface. Deployment, exchange mechanism and reconciliation must be verified individually. Target IFMIS architecture is not production evidence.</div>
    <div class="path-grid"><a href="reference/a.html"><strong>Authorities</strong><span>Legally assigned roles and institutional mandates.</span></a><a href="reference/b.html"><strong>Systems and exchanges</strong><span>Application inventory and 69 interface/exchange claims with evidence qualifications.</span></a><a href="chapters/16.html"><strong>BTMS and IFMIS</strong><span>Current system landscape and integration reform.</span></a><a href="chapters/17.html"><strong>UACS and record identities</strong><span>Codes versus individual document and transaction identifiers.</span></a></div>
    <h2>Five diagrams to begin with</h2><div class="model-grid">'''+''.join(links)+'''</div><h2>Additional analytical models</h2><p>Earlier exploratory diagrams of identity mapping, integration failure, versioned UACS and authoritative records are preserved separately as <a href="models/index.html">research models</a>, not silently substituted for the latest procedural figures.</p>'''
    make_page('systems.html','Authorities, systems and UACS',sysbody)

    modelroot=root/'research_models'; published=docs/'models'
    shutil.copytree(modelroot/'diagrams',published/'diagrams')
    shutil.copytree(modelroot/'registers',published/'registers')
    (published/'reference').mkdir(exist_ok=True)
    if (modelroot/'registers'/'interface_register.csv').is_file():
        shutil.copy2(modelroot/'registers'/'interface_register.csv',published/'reference'/'interface_register.csv')
    supplemental=json.loads((modelroot/'supplemental_index.json').read_text(encoding='utf-8'))
    # Historical references refer to the complete historical source namespace; keep it available.
    for letter in 'HIJKL':
        matches=list((modelroot/'reference').glob(letter+'_*.md'))
        if not matches: raise AssertionError('missing research reference '+letter)
        mdpath=matches[0]
        (published/'reference').mkdir(exist_ok=True)
        shutil.copy2(mdpath,published/'reference'/mdpath.name)
        soup=BeautifulSoup(MD(mdpath.read_text(encoding='utf-8')), 'html.parser')
        for a in soup.find_all('a',href=True):
            href=a['href'];p=urlsplit(href)
            if p.scheme or href.startswith('//') or href.startswith('#'):continue
            new=p.path
            if new.startswith('../reference/'):
                code=Path(new).name[0]
                if code in 'HIJKL':new=code.lower()+'.html'
                elif code in 'ABCDEFG':new='../../reference/'+code.lower()+'.html'
            if new.startswith('../processes/'):
                n=Path(new).name[:2];new='../../chapters/'+n+'.html'
            if new=='../00_REVISED_BIG_PICTURE.md':new='../index.html'
            if new=='../00_BIG_PICTURE.md':new='../../big-picture.html'
            if new=='G_open_questions_and_known_gaps.md':new='../../reference/g.html'
            if new=='interface_evidence_register.csv':new='../registers/interface_evidence_register.csv'
            # old source diagram links intentionally remain ../diagrams/... and point to copied archive
            a['href']=urlunsplit(('', '', new,p.query,p.fragment))
        intro='<div class="model-note"><strong>Historical research reference (10 October 2026).</strong> Proposed modeling material, not the current procedural atlas and not an official information-system specification. Some older diagram IDs and claims have been superseded.</div>'
        h1=soup.find('h1'); title=h1.get_text(' ',strip=True) if h1 else mdpath.stem
        content=intro+'<article class="prose">'+str(soup)+'</article><p><a href="../index.html">← Research models</a></p>'
        make_page('models/reference/'+letter.lower()+'.html',title,content)
    registries=[]
    for f in sorted((modelroot/'registers').glob('*.csv')):
        with f.open(encoding='utf-8-sig',newline='') as fp:
            rows=list(csv.DictReader(fp))
            cols=list(rows[0]) if rows else []
        htmlrows=[]
        for r in rows[:10]:htmlrows.append('<tr>'+''.join('<td>'+esc(str(r.get(col,''))[:170])+'</td>' for col in cols[:6])+'</tr>')
        table='<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+esc(k)+'</th>' for k in cols[:6])+'</tr></thead><tbody>'+''.join(htmlrows)+'</tbody></table></div>'
        source='registers/'+f.name
        body='<p class="eyebrow">Historical structured model · 10 Oct 2026</p><h1>'+esc(f.stem.replace('_',' ').title())+'</h1><p class="model-note">This CSV is a research-register snapshot, not an export from BTMS or an operational system. Previewing the first 10 records of '+str(len(rows))+'.</p><p><a href="'+source+'" download>Download complete CSV</a></p>'+table+'<p><a href="index.html">← Research models</a></p>'
        ident=f.stem.replace('_','-')
        make_page('models/'+ident+'.html',f.stem.replace('_',' ').title(),body)
        registries.append((ident,f.stem.replace('_',' ').title(),len(rows)))
    for item in supplemental:
        did=item['id'];kind=item['kind'];fname=item['filename']
        path=modelroot/item['path'];code=path.read_text(encoding='utf-8-sig')
        title=re.search(r'^\s*title:\s*["\']?([^\n"\']+)',code,re.M)
        title=title.group(1).strip() if title else fname.rsplit('.',1)[0].replace('_',' ').title()
        page='models/model-'+did+'.html'
        repo_code='diagrams/'+kind+'/'+fname
        body=('<p class="eyebrow">Supplementary analytic model · 10 October 2026</p><h1>'+esc(title)+'</h1>'
            '<div class="model-note"><strong>Versioned, source-only model.</strong> This diagram is from the earlier strengthened research edition. It has not been reconciled against the latest 12 October procedures, and no verified PNG rendering is supplied. A reused ID such as 07h does <em>not</em> replace the current diagram of that ID.</div>'
            '<p><strong>Historical ID:</strong> '+esc(did)+' · <strong>Notation:</strong> '+esc(kind)+' · <a href="'+repo_code+'" download>Download original editable code</a>'
            ' · <a href="../diagrams/'+did+'.html">Compare current ID where it exists</a></p>'
            '<h2>Source code</h2><div class="copy-row"><button type="button" data-copy="model-'+did+'">Copy code</button></div><pre class="model-code" id="model-'+did+'"><code class="model-source">'+esc(code)+'</code></pre>'
            '<p><a href="index.html">← All research models</a></p>')
        if did not in diagrams:
            body=body.replace('<a href="../diagrams/'+did+'.html">Compare current ID where it exists</a>', '<a href="../diagrams/index.html">Current diagram gallery</a>')
        make_page(page,'Research model '+did+': '+title,body)
        item['title']=title
    cards=[]
    for item in supplemental:
        cards.append('<a class="model-card" href="model-%s.html"><strong>%s · %s</strong><small>%s · historical source only</small></a>'%(esc(item['id']),esc(item['id']),esc(item['title']),esc(item['kind'].upper())))
    reference_cards=''.join('<a class="model-card" href="reference/%s.html"><strong>Reference %s</strong><small>Research-model framework and evidence</small></a>'%(x.lower(),x) for x in 'HIJKL')
    regcards=''.join('<a class="model-card" href="%s.html"><strong>%s</strong><small>%d records · downloadable CSV</small></a>'%(ident,esc(name),n) for ident,name,n in registries)
    body='''<p class="eyebrow">Version-separated research archive</p><h1>Additional financial and systems models</h1><p class="lead">Twenty-five supplementary Mermaid and PlantUML source diagrams from the 10 October strengthened edition, alongside typed financial-event, record, control, authority and interface registers.</p>
    <div class="model-note"><strong>Not the authoritative procedural edition.</strong> These research models are provisional analytical perspectives. The current 12 October atlas remains the reference for documented procedures. Historical files with IDs reused by the current atlas are not substituted into its diagrams or chapters. No render is claimed for the 25 diagrams.</div>
    <h2>Explore the supplemental diagrams</h2><div class="model-grid">'''+''.join(cards)+'''</div><h2>Reference-model documents (H–L)</h2><div class="model-grid">'''+reference_cards+'''</div><h2>Structured research registers</h2><div class="model-grid">'''+regcards+'''</div>
    <p><a href="history.html">Browse the complete 106-diagram historical code archive →</a></p><h2>What these models add</h2><p>They distinguish transaction identities from UACS codes; permissions from actual financial balances; source-of-record ownership from data transport; concurrent accounting from a linear payment trail; and current deployment evidence from planned IFMIS integration. These are research claims that require reconciliation with applicable legal texts and agency system specifications.</p>
    <p><a href="../big-picture.html">Read the current big picture</a> · <a href="../systems.html">Current authorities and systems</a> · <a href="../reference/g.html">Known open questions</a></p>'''
    make_page('models/index.html','Research models and registers',body)
    historical=[]
    unique_files={d['filename'] for d in supplemental}
    for f in sorted((modelroot/'diagrams').rglob('*')):
        if not f.is_file() or f.suffix not in ('.mmd','.puml'):continue
        rel=f.relative_to(modelroot).as_posix()
        flag=('Supplementary analytical source' if f.name in unique_files else 'Historical variant of current atlas ID')
        historical.append('<tr><td><a href="'+esc(rel)+'">'+esc(f.name)+'</a></td><td>'+esc(f.suffix[1:].upper())+'</td><td>'+flag+'</td></tr>')
    history='<p class="eyebrow">Historical source archive</p><h1>All 106 source diagrams from 10 October 2026</h1><p class="model-note">This is the unmodified older snapshot. Some titles and IDs coincide with current figures but differ in content. Use the <a href="../diagrams/index.html">current diagram gallery</a> for the presently documented procedures and the <a href="index.html">25 supplementary models</a> for non-overlapping research diagrams.</p><table><thead><tr><th>Original filename</th><th>Notation</th><th>Relationship to current atlas</th></tr></thead><tbody>'+''.join(historical)+'</tbody></table>'
    make_page('models/history.html','Historical diagram source archive',history)
    # compatibility redirects for the educational site's process and reference paths.
    def redirect(old,new,title):
        rel=c['relurl'](old,new)
        # Keep fragment; use a relative destination so it works under any GitHub repo path.
        tiny='''<p class="eyebrow">Compatibility address</p><h1>%s</h1><p>This address has moved to <a href="%s">the current reference page</a>.</p><script>location.replace(%s + location.search + location.hash);</script>'''%(esc(title),esc(rel),json.dumps(rel))
        make_page(old,title,tiny)
    redirect('overview.html','big-picture.html','Big picture')
    for source in chapter_sources:
        redirect('processes/'+source.stem+'.html','chapters/'+source.name[:2]+'.html',source.stem.replace('_',' '))
    for source in c['REFERENCES']:
        redirect('reference/'+source.stem+'.html','reference/'+source.name[0].lower()+'.html',source.stem.replace('_',' '))
    print('extensions: guided lessons',len(guides),'supplemental diagrams',len(supplemental),'research registers',len(registries))
