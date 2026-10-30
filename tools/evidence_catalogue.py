"""Source-qualified document -> transaction -> record -> report -> decision index.

Build hook for tools/build_site.py. Deliberately reuses Atlas chapter pages and
Reference F; it does not create another competing budget-cycle chapter sequence.
"""
from __future__ import annotations

import html
import json
from collections import defaultdict
from pathlib import Path

KINDS = ("authority", "concept", "document", "transaction", "registry", "report", "decision")
STATUSES = ("documented", "interpretation", "verify_current")
RELATIONS = ("aggregated_into", "authorizes", "available_for_review", "compared_with", "documents", "governs", "instructs", "limits", "posted_to", "requires_followup", "summarized_in", "supports", "supports_request")


def esc(x):
    return html.escape(str(x), quote=True)


def validate(data):
    """Check structural integrity, including dangling links and misleading evidence flags."""
    errors = []
    items = data.get("items", [])
    ids = [n.get("id") for n in items]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate item ID")
    canonical = set(ids)
    for item in items:
        ident = item.get("id", "")
        if not ident or not all(c.islower() or c.isdigit() or c == '-' for c in ident):
            errors.append("Invalid item ID: %r" % ident)
        if item.get("type") not in KINDS or item.get("status") not in STATUSES:
            errors.append("Unknown type/status: %s" % ident)
        if not item.get("name") or not item.get("definition"):
            errors.append("Missing name/definition: %s" % ident)
        if not item.get("chapter", "").startswith("chapters/"):
            errors.append("Missing chapter path: %s" % ident)
        if not (item.get("source") or item.get("source_url")):
            errors.append("Missing provenance: %s" % ident)
        if item.get("source") and item.get("source_url"):
            errors.append("Two competing provenance references: %s" % ident)
    for i, link in enumerate(data.get("links", [])):
        if link.get("from") not in canonical or link.get("to") not in canonical:
            errors.append("Link %d has dangling item ID" % i)
        if link.get("relation") not in RELATIONS or link.get("status") not in STATUSES:
            errors.append("Link %d has unknown relation/status" % i)
        if not link.get("note") or not (link.get("basis") or link.get("basis_url")):
            errors.append("Link %d lacks caveat/source" % i)
        if link.get("basis") and link.get("basis_url"):
            errors.append("Link %d has two competing provenance references" % i)
    if not any('SAAODB' in n.get('aliases', []) for n in items):
        errors.append("Acceptance check: SAAODB must be searchable")
    for t in ('far-1','far-1a','far-1b','far-1c','far-2','far-2a','far-3','far-4','far-5','far-6'):
        if t not in canonical:
            errors.append("Missing pilot report: " + t)
    if errors:
        raise ValueError("Evidence catalogue: " + "; ".join(errors))
    return True


def provenance(record):
    code = record.get('source') or record.get('basis')
    if code:
        return '<a href="reference/f.html#source-%s">%s</a>' % (esc(code.lower()), esc(code))
    return '<a href="%s" rel="noopener">Official source ↗</a>' % esc(record.get('source_url') or record['basis_url'])


def build_evidence_page(c):
    root = c['ROOT']
    data = json.loads((root / 'src/evidence/lineage.json').read_text(encoding='utf-8'))
    validate(data)
    frame, write, search = c['frame'], c['write_page'], c['SEARCH']
    entries = {item['id']: item for item in data['items']}
    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    for edge in data['links']:
        outgoing[edge['from']].append(edge)
        incoming[edge['to']].append(edge)
    sections = []
    for kind in KINDS:
        nodes = [v for v in data['items'] if v['type'] == kind]
        if not nodes:
            continue
        parts = ['<section id="kind-%s"><h2>%s (%d)</h2>' % (esc(kind), esc(kind.capitalize()), len(nodes))]
        for node in nodes:
            label = node['name']
            alias = ', '.join(node.get('aliases', []))
            edges = []
            for edge in incoming[node['id']]:
                other = entries[edge['from']]
                edges.append('<li><a href="#item-%s">%s</a> → <strong>%s</strong> — %s. <span class="muted">[%s; %s]</span></li>' % (
                    esc(other['id']), esc(other['name']), esc(edge['relation'].replace('_', ' ')), esc(edge['note']), provenance(edge), esc(edge['status'])))
            for edge in outgoing[node['id']]:
                other = entries[edge['to']]
                edges.append('<li><strong>%s</strong> → <a href="#item-%s">%s</a> — %s. %s <span class="muted">[%s]</span></li>' % (
                    esc(edge['relation'].replace('_', ' ')), esc(other['id']), esc(other['name']), esc(edge['note']), provenance(edge), esc(edge['status'])))
            parts.append('<article id="item-%s" class="prose-block" style="padding:1rem 0;border-top:1px solid var(--rule)">' % esc(node['id']))
            parts.append('<h3>%s</h3><p>%s</p>' % (esc(label), esc(node['definition'])))
            if alias:
                parts.append('<p class="muted"><strong>Also searched as:</strong> %s</p>' % esc(alias))
            parts.append('<p><a href="%s">Chapter explanation</a> · <a href="reference/c.html">Document catalogue</a> · %s · <span class="muted">Status: %s</span></p>' % (
                esc(node['chapter']), provenance(node), esc(node['status'].replace('_',' '))))
            if edges:
                parts.append('<details><summary>Evidence relationships (%d)</summary><ul>%s</ul></details>' % (len(edges), ''.join(edges)))
            parts.append('</article>')
            # Search aliases stay in the existing search index; no second search service or runtime fetch.
            search.append({'t': label, 'p': 'Evidence pathways · ' + kind, 'u': 'evidence.html#item-' + node['id'],
                           'x': ' '.join([label] + node.get('aliases', []) + [node['definition'], node.get('source', '')])})
        parts.append('</section>')
        sections.append(''.join(parts))
    kind_nav = ' · '.join('<a href="#kind-%s">%s</a>' % (esc(k), esc(k.capitalize())) for k in KINDS if any(x['type']==k for x in data['items']))
    body = ('<div class="doc-head"><p class="eyebrow">Reference · cross-reference layer</p>'
            '<h1>Evidence pathways</h1></div>'
            '<p class="lead">Trace how documentary evidence relates to transactions, registries, reports and administrative decisions.</p>'
            '<p class="prose-block">%s</p>' % esc(data['scope_note']) +
            '<p class="muted">Pilot index: %d items, %d source-qualified relationships.</p>' % (len(data['items']), len(data['links'])) +
            '<nav class="prose-block" aria-label="Evidence category navigation">%s</nav>' % kind_nav +
            '<p class="prose-block"><strong>Read relationship types carefully:</strong> “documents”, “authorizes”, '
            '“aggregated into”, “compared with” and “supports request” have different meanings. A report appearing here '
            'does not establish that an automated system interface exists or that an expenditure was lawful. '
            'A link marked <em>verify current</em> is not an operative compliance instruction.</p>'
            '<p class="prose-block">See the <a href="reference/e.html">glossary</a>, '
            '<a href="reference/c.html">documents and identifiers</a>, '
            '<a href="reference/f.html">source register</a>, and '
            '<a href="reference/g.html">unresolved questions</a>.</p>' + ''.join(sections))
    write('evidence.html', frame('evidence.html', 'Evidence pathways', body, description='Documents, transactions, registries, reports and decisions cross-referenced to their chapters and sources.', section='reference/index.html'))
    search.append({'t':'Evidence pathways','p':'Reference','u':'evidence.html','x':data['scope_note'] + ' document transaction registry report decision glossary FAR BFAR SAAODB'})
    return len(data['items']), len(data['links'])
