"""Pages at the addresses of an earlier arrangement of the website. Each page sends the reader to the page that now
holds the content, and keeps the part of the address after '#' where the section has a new place.

The data are in tools/forwarding.json. The pages are not listed anywhere and are not in the search index. Called by
tools/build_site.py.
"""
import html
import json
import posixpath
from pathlib import Path

DATA = Path(__file__).resolve().parent / 'forwarding.json'


def esc(s):
    return html.escape(str(s), quote=True)


def page(url, target, label, anchors, frame, relurl):
    """A page at 'url' that sends the reader to 'target' (a path from docs/), with a map of old anchors."""
    rel = relurl(url, target)
    amap = {k: relurl(url, v) for k, v in anchors.items()}
    script = ('<script>(function(){var m=%s;var h=location.hash.slice(1);var t=(h&&m[h])?m[h]:%s;'
              'location.replace(t);})();</script>' % (json.dumps(amap), json.dumps(rel)))
    body = ('<div class="doc-head"><p class="eyebrow">Address moved</p><h1>This page has moved</h1></div>'
            '<p class="prose-block">Its content is now in <a href="%s">%s</a>.</p>%s' % (esc(rel), esc(label), script))
    return frame(url, 'Page moved', body, description='This page has moved.', robots='noindex')


def build(write_page, frame, relurl, chapter_label, diagram_title, chapter_ids, diagram_ids):
    data = json.loads(DATA.read_text(encoding='utf-8'))
    n = 0
    for old, info in data['chapters'].items():
        target = 'chapters/%s.html' % info['page']
        anchors = {k: 'chapters/' + v for k, v in info['anchors'].items()}
        if info['page'] not in chapter_ids or any(v.split('/')[1].split('.')[0] not in chapter_ids for v in anchors.values()):
            raise SystemExit('forwarding.json names a chapter that does not exist (%s)' % old)
        label = 'chapter %s' % chapter_label(info['page'])
        write_page('chapters/%s.html' % old, page('chapters/%s.html' % old, target, label, anchors, frame, relurl))
        n += 1
    for stem, old in data['process_pages'].items():
        info = data['chapters'][old]
        target = 'chapters/%s.html' % info['page']
        anchors = {k: 'chapters/' + v for k, v in info['anchors'].items()}
        url = 'processes/%s.html' % stem
        write_page(url, page(url, target, 'chapter %s' % chapter_label(info['page']), anchors, frame, relurl))
        n += 1
    for old, new in data['diagrams'].items():
        if new not in diagram_ids:
            raise SystemExit('forwarding.json names a diagram that does not exist (%s)' % new)
        url = 'diagrams/%s.html' % old
        write_page(url, page(url, 'diagrams/%s.html' % new, 'diagram %s: %s' % (new, diagram_title(new)), {}, frame,
                             relurl))
        n += 1
    return n
