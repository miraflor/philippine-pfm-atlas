#!/usr/bin/env python3
"""Build the website of the Philippine PFM Atlas in docs/ from the built atlas in docs/atlas/.

Run from the root of the repository, after tools/build_atlas.py:

    python3 tools/build_site.py

It needs the Python packages mistune and beautifulsoup4 (see requirements.txt).

The script writes every file of docs/ except the folder docs/atlas/, which tools/build_atlas.py writes. Before it
writes, it removes everything else in docs/, so that no page of an earlier build remains.

All text of the pages comes from the Markdown files of the atlas. The script adds the navigation, the drawing of the
four lines on the home page, links from each source code to Reference F, fixed anchors for the numbered points and
rows that other texts may cite, and a page for each diagram. The style sheet and the scripts of the website are in
tools/site/.
"""
import copy
import csv
import html
import json
import posixpath
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from site_experience import enhance_page
import budget_cycle_story
import budget_cycle_nav
from atlas_pages import (ORDER, ID as CHAPTER_ID, DIAGRAM_ID, PHASE_KEY, PHASE_NAME, chapter_files, is_phase_intro,
                         page_of_diagram)
import mistune
from bs4 import BeautifulSoup, Comment, NavigableString

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ATLAS = DOCS / "atlas"
SITE_FILES = ROOT / "tools" / "site"
SITE_NAME = "Philippine PFM Atlas"

MD = mistune.create_markdown(escape=False, plugins=["table", "strikethrough", "url"])

LINES = ["authority", "claim", "cash", "records"]
LINE_NAMES = {"authority": "Legal authority", "claim": "The claim", "cash": "Cash", "records": "Records and control"}

NAV = [
    ("index.html", "Budget cycle"),
    ("walkthrough.html", "Guided lessons"),
    ("big-picture.html", "Big picture"),
    ("chapters/index.html", "Chapters"),
    ("diagrams/index.html", "Diagrams"),
    ("systems.html", "Systems & UACS"),
    ("models/index.html", "Research models"),
    ("reference/g.html", "Open points"),
    ("search.html", "Search"),
    ("reference/index.html", "References"),
    ("about.html", "About"),
]

BRAND_MARK = ('<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect width="32" height="32" rx="6" '
              'fill="#ffffff" stroke="#deded9"/><path d="M6 8.5H26" stroke="#1f4e8c" stroke-width="3.2" '
              'stroke-linecap="round"/><path d="M6 14H26" stroke="#2e6b2e" stroke-width="3.2" stroke-linecap="round"/>'
              '<path d="M6 19.5H26" stroke="#a35200" stroke-width="3.2" stroke-linecap="round"/><path d="M6 25H26" '
              'stroke="#555555" stroke-width="3.2" stroke-linecap="round" stroke-dasharray="0.1 4.9"/>'
              '<path d="M17 8.5V14" stroke="#1b1b1b" stroke-width="3.6" stroke-linecap="round"/></svg>')

# ---------------------------------------------------------------------------------------------------------------
# Small helpers


def esc(s):
    return html.escape(str(s), quote=True)


def slugify(s, limit=70):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:limit].strip("-") or "item"


def relurl(frm, to):
    """Relative address of the page 'to' (a path from docs/) as seen from the page 'frm'."""
    return posixpath.relpath(to, posixpath.dirname(frm) or ".")


def root_prefix(url):
    r = posixpath.relpath(".", posixpath.dirname(url) or ".")
    return "" if r == "." else r + "/"


def read(path):
    return path.read_text(encoding="utf-8")


def save(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def fail(msg):
    sys.exit("build_site.py: " + msg)


# ---------------------------------------------------------------------------------------------------------------
# The atlas: files, addresses, diagrams, sources

BIG = ATLAS / "00_BIG_PICTURE.md"
README = ATLAS / "README.md"
REFERENCES = sorted(ATLAS.glob("reference/[A-Z]_*.md"))
if not (ATLAS / "chapters").is_dir() or not REFERENCES or not BIG.exists() or not README.exists():
    fail("docs/atlas/ is incomplete. Run tools/build_atlas.py first.")
CHAPTER_FILE = chapter_files(ATLAS / "chapters")          # {ID: path}, in the order of the atlas
CHAPTERS = list(CHAPTER_FILE.values())

URL = {"00_BIG_PICTURE.md": "big-picture.html", "README.md": "about.html"}
for _pid, _p in CHAPTER_FILE.items():
    URL["chapters/" + _p.name] = "chapters/%s.html" % _pid
for _p in REFERENCES:
    URL["reference/" + _p.name] = "reference/%s.html" % _p.name[0].lower()


def h1_of(path):
    first = read(path).split("\n", 1)[0]
    return first[2:].strip() if first.startswith("# ") else path.stem


TITLE = {rel: h1_of(ATLAS / rel) for rel in URL}

with open(ATLAS / "reference" / "diagram_index.csv", encoding="utf-8", newline="") as _fh:
    DIAGRAMS = list(csv.DictReader(_fh))
DIAG = {d["id"]: d for d in DIAGRAMS}
STEPS = defaultdict(list)
with open(ATLAS / "reference" / "steps_register.csv", encoding="utf-8", newline="") as _fh:
    for _r in csv.DictReader(_fh):
        STEPS[_r["diagram_id"]].append(_r)
for _k in STEPS:
    STEPS[_k].sort(key=lambda r: int(r["step"]) if r["step"].isdigit() else 0)


def table_cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_separator(line):
    return set(line.strip()) <= set("|-: ")


def short_title(text):
    text = re.sub(r"[*`]", "", text)
    text = re.split(r"\s(?:Copy:|Copy by section:|https?://)", text)[0].strip()
    return text if len(text) <= 180 else text[:177].rsplit(" ", 1)[0] + " …"


def read_sources():
    codes, marks, mode = {}, {}, None
    for line in read(ATLAS / "reference" / "F_sources_and_verification.md").split("\n"):
        if not line.startswith("|"):
            mode = None
            continue
        cells = table_cells(line)
        if cells[:2] == ["Code", "Source"]:
            mode = "code"
            continue
        if cells[:2] == ["Mark", "Meaning"]:
            mode = "mark"
            continue
        if is_separator(line):
            continue
        if mode == "code":
            codes[cells[0].strip("`")] = short_title(cells[1])
        elif mode == "mark" and cells[0] in ("GK", "Inference"):
            marks[cells[0]] = short_title(cells[1])
    if not codes or set(marks) != {"GK", "Inference"}:
        fail("could not read the tables of source codes in Reference F")
    return codes, marks


CODES, MARKS = read_sources()
FACTS_AS_OF = re.search(r"Facts on current events are as of ([^.]+)\.", read(README))
FACTS_AS_OF = FACTS_AS_OF.group(1) if FACTS_AS_OF else ""


def chapter_title(pid):
    """The title of a chapter without its ID, for example 'Obligation'."""
    return re.sub(r"^%s\.\s*" % re.escape(pid), "", TITLE["chapters/" + CHAPTER_FILE[pid].name])


def chapter_label(pid):
    return "%s · %s" % (pid, chapter_title(pid))


# ---------------------------------------------------------------------------------------------------------------
# Parts and lines of each chapter, from the table of section 3 of the big picture

PART_LABEL = {
    "A": "A. Decide", "D": "D. Close each period", "E": "E. What remains",
    "Outside the main sequence": "Outside the main sequence",
    "Parallel to the money": "Parallel to the money", "For all parts": "For all parts",
}


ID_TOKEN = r"(?:P1[0-2]|P\d|L[0-5]|E[0-6]|A\d|IS|UACS)"


def ids_in(text):
    """Chapter IDs named in a text: 'P0 to P12, L0' -> ['P0', 'P1', ..., 'P12', 'L0']. Markdown links are read as their text."""
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    out = []
    for m in re.finditer(r"(?<![\w-])(%s)(?: to (%s))?(?![\w-])" % (ID_TOKEN, ID_TOKEN), text):
        a, b = m.group(1), m.group(2)
        if b:
            out += ORDER[ORDER.index(a):ORDER.index(b) + 1]
        else:
            out.append(a)
    return out


def read_chapter_tags():
    """Parts and lines of each chapter, from the table of section 3 of the big picture."""
    tags, inside = defaultdict(list), False
    for line in read(BIG).split("\n"):
        if line.startswith("| Part | Function | Lead authorities |"):
            inside = True
            continue
        if inside and not line.startswith("|"):
            break
        if not inside or is_separator(line):
            continue
        cells = table_cells(line)
        part = cells[0]
        if part.startswith("B, line 1"):
            tag = ("line", "authority")
        elif part.startswith("B, line 2"):
            tag = ("line", "claim")
        elif part.startswith("B, line 3"):
            tag = ("line", "cash")
        elif part == "C":
            tag = ("line", "records")
        elif part[0] in "ADE" and (len(part) == 1 or part[1] == ","):
            tag = ("part", PART_LABEL[part[0]])
        elif part in PART_LABEL:
            tag = ("part", PART_LABEL[part])
        else:
            fail("unknown part in the table of section 3 of the big picture: " + part)
        for pid in ids_in(cells[-1]):
            if pid not in CHAPTER_FILE:
                fail("unknown chapter %s in the table of section 3 of the big picture" % pid)
            if tag not in tags[pid]:
                tags[pid].append(tag)
    return tags


CHAPTER_TAGS = read_chapter_tags()


def chips_html(tags):
    out = []
    for kind, value in sorted(tags, key=lambda t: (t[0] != "line", LINES.index(t[1]) if t[0] == "line" else 0)):
        if kind == "line":
            out.append('<span class="chip line %s">%s</span>' % (value, esc(LINE_NAMES[value])))
        else:
            out.append('<span class="chip">%s</span>' % esc(value))
    return '<div class="chips">%s</div>' % "".join(out)


# ---------------------------------------------------------------------------------------------------------------
# From Markdown to HTML


def replace_in_text(container, pattern, maker, skip=("a", "code", "pre", "script", "style", "svg", "summary")):
    """Replace matches of 'pattern' in the text of 'container' by the tags that 'maker' returns.
    Text inside the elements named in 'skip' is not changed."""
    for node in list(container.find_all(string=True)):
        if isinstance(node, Comment) or any(p.name in skip for p in node.parents if p is not None):
            continue
        text = str(node)
        parts, last = [], 0
        for m in pattern.finditer(text):
            tag = maker(m)
            if tag is None:
                continue
            parts += [text[last:m.start()]] + (tag if isinstance(tag, list) else [tag])
            last = m.end()
        if not parts:
            continue
        parts.append(text[last:])
        node.replace_with(*[NavigableString(p) if isinstance(p, str) else p for p in parts if not (isinstance(p, str) and p == "")])


def heading_id(text, used):
    m = re.match(r"^(\d+(?:\.\d+)*)\.?\s", text)
    if m:
        base = "section-" + m.group(1).replace(".", "-")
    else:
        m = re.match(r"^Diagram\s+([A-Z][A-Z0-9]*-[a-z])\b", text)
        base = ("diagram-" + m.group(1)) if m else slugify(text, 60)
    hid, n = base, 2
    while hid in used:
        hid, n = "%s-%d" % (base, n), n + 1
    used.add(hid)
    return hid


def number_headings(soup):
    used, toc = set(), []
    for h in soup.find_all(["h2", "h3", "h4"]):
        text = h.get_text(" ", strip=True)
        h["id"] = heading_id(text, used)
        if h.name in ("h2", "h3"):
            label = text
            m = re.match(r"^(Diagram\s+[A-Z][A-Z0-9]*-[a-z])\b", text)
            if m:
                label = m.group(1)
            toc.append((h.name, h["id"], label))
    return toc


def rewrite_links(soup, md_rel, page_url):
    base = posixpath.dirname(md_rel)
    for tag, attr in (("a", "href"), ("img", "src")):
        for el in soup.find_all(tag, attrs={attr: True}):
            value = el[attr]
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", value) or value.startswith(("#", "//")):
                continue
            path, _, frag = value.partition("#")
            target = posixpath.normpath(posixpath.join(base, path))
            new = URL.get(target, "atlas/" + target)
            el[attr] = relurl(page_url, new) + ("#" + frag if frag else "")


def diagram_figure(soup, did, page_url):
    d = DIAG[did]
    image = relurl(page_url, "atlas/" + d["image"])
    fig = soup.new_tag("figure", attrs={"class": "diagram", "id": "figure-" + did})
    link = soup.new_tag("a", href=image)
    attrs = {"src": image, "alt": "Diagram %s: %s" % (did, d["title"]), "loading": "lazy"}
    size = png_size(ATLAS / d["image"])
    if size:
        attrs["width"], attrs["height"] = str(size[0]), str(size[1])
    link.append(soup.new_tag("img", attrs=attrs))
    fig.append(link)
    cap = BeautifulSoup('<figcaption><span class="id">%s</span> · <a href="%s">Diagram page: what it shows, '
                        'its steps and its code</a> · <a href="%s">Image in full size</a></figcaption>'
                        % (did, relurl(page_url, "diagrams/%s.html" % did), image), "html.parser")
    fig.append(cap)
    return fig


def embed_diagrams(soup, md_rel, page_url):
    base = posixpath.dirname(md_rel)
    for h in soup.find_all(["h3", "h4"], id=re.compile(r"^diagram-[A-Z][A-Z0-9]*-[a-z]$")):
        did = h["id"][len("diagram-"):]
        if did not in DIAG:
            continue
        para = h.find_next_sibling("p")
        if para is None or not para.get_text().startswith("Code file:"):
            fail("diagram %s in %s has no line 'Code file:'" % (did, md_rel))
        for code in para.find_all("code"):
            text = code.get_text()
            if text.endswith((".mmd", ".puml")):
                a = soup.new_tag("a", href=relurl(page_url, "atlas/" + posixpath.normpath(posixpath.join(base, text))))
                code.wrap(a)
        para.insert_after(diagram_figure(soup, did, page_url))
    # Mermaid code blocks: fold them away under the image
    for code in soup.select("pre > code.language-mermaid"):
        pre = code.parent
        h = pre.find_previous(["h3", "h4"])
        did = h["id"][len("diagram-"):] if h and h.get("id", "").startswith("diagram-") else ""
        details = soup.new_tag("details", attrs={"class": "code"})
        summary = soup.new_tag("summary")
        summary.string = "Mermaid code of diagram %s" % did if did else "Mermaid code"
        pre.wrap(details)
        details.insert(0, summary)
    # PlantUML: the Markdown shows the image and then the code in a <details> block
    for details in soup.find_all("details"):
        if details.find("code", class_="language-plantuml"):
            details["class"] = "code"
    for img in soup.select("p > img"):
        if re.search(r"rendered/[A-Z][A-Z0-9]*-[a-z]_[^/]+\.png$", img.get("src", "")) and not img.parent.get_text(strip=True):
            img.parent.decompose()


def wrap_tables(soup):
    for table in soup.find_all("table"):
        table.wrap(soup.new_tag("div", attrs={"class": "table-wrap"}))


def header_of(table):
    return [th.get_text(" ", strip=True) for th in table.select("thead th")]


def anchor_cell(soup, td, href):
    a = soup.new_tag("a", href=href, attrs={"class": "row-id"})
    for child in list(td.contents):
        a.append(child.extract())
    td.append(a)


STATUS_LABEL = {"open": "Open", "partly": "Partly settled", "settled": "Settled", "differ": "Sources differ"}


def anchor_rows(soup, page, page_url):
    """Fixed anchors for the numbered points and rows that other texts may cite."""
    used = set()

    def unique(base):
        hid, n = base, 2
        while hid in used:
            hid, n = "%s-%d" % (base, n), n + 1
        used.add(hid)
        return hid

    for table in soup.find_all("table"):
        head = header_of(table)
        rows = [tr for tr in table.select("tbody tr") if tr.find("td")]
        if not head:
            continue
        for tr in rows:
            tds = tr.find_all("td")
            first = tds[0].get_text(" ", strip=True)
            hid = None
            if head[0] == "No." and first.isdigit():
                if page == "g":
                    hid = "point-" + first
                    if head[1] == "Subject":
                        status = "differ"
                    else:
                        t = tds[1].get_text(" ", strip=True)
                        status = ("settled" if re.match(r"Settled\b", t) else
                                  "partly" if re.match(r"Partly settled\b", t) else "open")
                    tr["data-status"] = status
                elif head[:3] == ["No.", "From", "To"]:
                    if page == "b":
                        hid = "flow-" + first
                    else:
                        anchor_cell(soup, tds[0], relurl(page_url, "reference/b.html") + "#flow-" + first)
                        continue
                elif page == "c" and head[1] == "From record":
                    hid = "link-" + first
                elif page == "c" and head[1] == "Record":
                    hid = "proof-" + first
                elif page == "f" and head[1] == "Decision":
                    hid = "decision-" + first
            elif page == "f" and head[0] == "Code":
                hid = "source-" + slugify(first.strip("`"))
            elif page == "f" and head[0] == "Mark" and first in MARKS:
                hid = "mark-" + slugify(first)
            elif page == "c" and head[0] == "Document":
                hid = "doc-" + slugify(first)
            elif page == "e" and head[0] == "Term":
                hid = "term-" + slugify(first)
            elif page == "e" and head[0] == "Abbreviation":
                hid = "abbr-" + slugify(first)
            elif page == "a" and head[0] in ("Authority", "Party"):
                hid = "authority-" + slugify(first)
            if hid:
                hid = unique(hid)
                tr["id"] = hid
                anchor_cell(soup, tds[0], "#" + hid)
                if tr.get("data-status"):
                    label = STATUS_LABEL[tr["data-status"]]
                    dot = soup.new_tag("span", attrs={"class": "status-dot st-" + tr["data-status"], "title": label})
                    hidden = soup.new_tag("span", attrs={"class": "visually-hidden"})
                    hidden.string = label
                    dot.append(hidden)
                    tds[0].append(dot)


BRACKET = re.compile(r"\[([A-Za-z][A-Za-z0-9\-]*)((?: [^\[\]]*)?)\]")
TOKEN = re.compile(r"(?<![A-Za-z0-9\-])(%s)(?![A-Za-z0-9\-])"
                   % "|".join(sorted((re.escape(c) for c in list(CODES) + list(MARKS)), key=len, reverse=True)))


def link_sources(soup, page_url):
    f_page = relurl(page_url, "reference/f.html")

    def link(code, text):
        if code in CODES:
            href, title = "%s#source-%s" % (f_page, slugify(code)), CODES[code]
        elif code in MARKS:
            href, title = "%s#mark-%s" % (f_page, slugify(code)), MARKS[code]
        else:
            return None
        a = soup.new_tag("a", href=href, attrs={"class": "basis", "title": title})
        a.string = text
        return a

    replace_in_text(soup, BRACKET, lambda m: link(m.group(1), m.group(0)) if m.group(1) in CODES else None)
    for table in soup.find_all("table"):
        head = header_of(table)
        if "Basis" not in head:
            continue
        k = head.index("Basis")
        for tr in table.select("tbody tr"):
            tds = tr.find_all("td")
            if len(tds) > k:
                tds[k]["class"] = "basis-cell"
                replace_in_text(tds[k], TOKEN, lambda m: link(m.group(1), m.group(0)))


CHAPTER_COLUMNS = ("Chapters", "Chapter", "Chapters affected")
DIAGRAM_COLUMNS = ("Diagrams", "Diagram")
DID_TOKEN = r"(?:BP|P1[0-2]|P\d|L[0-5]|E[0-6]|A\d|IS|UACS)-[a-z]"
SEP = r"(?:,? and |, | to | or )"
SEC = r"\d+(?:\.\d+)*"
CHAP_PHRASE = re.compile(r"\b(?P<word>[Cc]hapters?) (?P<list>%s(?:%s%s)*)(?:, (?P<sword>sections?) (?P<secs>%s(?:(?:,? and |, | to )%s)*))?"
                         r"(?![\w-])" % (ID_TOKEN, SEP, ID_TOKEN, SEC, SEC))
DIAG_PHRASE = re.compile(r"\b(?P<word>[Dd]iagrams?) (?P<list>%s(?:%s%s)*)(?![\w-])" % (DID_TOKEN, SEP, DID_TOKEN))
REF_PHRASE = re.compile(r"\bReference (?P<letter>[A-G])(?:, (?P<kind>section|point) (?P<rnum>\d+(?:\.\d+)*))?\b")
BARE_SECTION = re.compile(r"(?<!, )(?<!its )\b(?P<word>[Ss]ections?) (?P<secs>%s(?:(?:,? and |, | to )%s)*)(?! of\b)(?![\d.]*\d)"
                          % (SEC, SEC))
POINT_IN_G = re.compile(r"\b[Pp]oints? (\d{1,3})\b")
NO_LINK_IN = ("a", "code", "pre", "script", "style", "svg", "summary", "h1", "h2", "h3", "h4")


def linked_tokens(soup, text, pattern, href_of):
    """Nodes for 'text' in which every match of 'pattern' becomes a link (href_of(token) -> href or None)."""
    nodes, last = [], 0
    for m in re.finditer(pattern, text):
        href = href_of(m.group(0))
        if href is None:
            continue
        if m.start() > last:
            nodes.append(NavigableString(text[last:m.start()]))
        a = soup.new_tag("a", href=href)
        a.string = m.group(0)
        nodes.append(a)
        last = m.end()
    if last < len(text):
        nodes.append(NavigableString(text[last:]))
    return nodes


def section_list(secs):
    out = []
    for part in re.split(r",? and |, ", secs):
        if " to " in part:
            out += [x.strip() for x in part.split(" to ")]
        else:
            out.append(part.strip())
    return out


def link_references(soup, page, page_url):
    """Links for the names of chapters, sections, diagrams and reference files in the text, and for the IDs in the
    columns of tables that list chapters or diagrams. The text itself does not change."""
    own = {el["id"] for el in soup.find_all(id=True)}

    def chapter_href(pid, sec=None):
        if pid not in CHAPTER_FILE:
            return None
        href = relurl(page_url, "chapters/%s.html" % pid)
        return href + ("#section-" + sec.replace(".", "-") if sec else "")

    def diagram_href(did):
        return relurl(page_url, "diagrams/%s.html" % did) if did in DIAG else None

    def make_chapter(m):
        ids = ids_in(m.group("list"))
        if any(x not in CHAPTER_FILE for x in ids):
            return None
        secs = section_list(m.group("secs")) if m.group("secs") else []
        if len(ids) == 1 and " to " not in m.group("list") and len(secs) <= 1:
            a = soup.new_tag("a", href=chapter_href(ids[0], secs[0] if secs else None))
            a.string = m.group(0)
            return a
        if len(ids) == 1 and " to " not in m.group("list"):
            head = m.group(0)[:m.start("secs") - m.start()]
            nodes = linked_tokens(soup, head, r"(?<![\w-])%s(?![\w-])" % ID_TOKEN, lambda t: chapter_href(t))
            nodes += linked_tokens(soup, m.group("secs"), SEC, lambda t: chapter_href(ids[0], t))
            return nodes
        return linked_tokens(soup, m.group(0), r"(?<![\w-])%s(?![\w-])" % ID_TOKEN, lambda t: chapter_href(t))

    def make_diagram(m):
        ids = re.findall(DID_TOKEN, m.group("list"))
        if any(d not in DIAG for d in ids):
            return None
        if len(ids) == 1:
            a = soup.new_tag("a", href=diagram_href(ids[0]))
            a.string = m.group(0)
            return a
        return linked_tokens(soup, m.group(0), DID_TOKEN, diagram_href)

    def make_ref(m):
        href = relurl(page_url, "reference/%s.html" % m.group("letter").lower())
        if m.group("kind") == "section":
            href += "#section-" + m.group("rnum").replace(".", "-")
        elif m.group("kind") == "point" and m.group("letter") == "G":
            href += "#point-" + m.group("rnum")
        a = soup.new_tag("a", href=href)
        a.string = m.group(0)
        return a

    def make_bare(m):
        secs = section_list(m.group("secs"))
        if not all("section-" + x.replace(".", "-") in own for x in secs):
            return None
        if len(secs) == 1:
            a = soup.new_tag("a", href="#section-" + secs[0].replace(".", "-"))
            a.string = m.group(0)
            return a
        return linked_tokens(soup, m.group(0), r"(?<=[ ,])%s" % SEC, lambda t: "#section-" + t.replace(".", "-"))

    replace_in_text(soup, CHAP_PHRASE, make_chapter, skip=NO_LINK_IN)
    replace_in_text(soup, DIAG_PHRASE, make_diagram, skip=NO_LINK_IN)
    replace_in_text(soup, REF_PHRASE, make_ref, skip=NO_LINK_IN)
    if page.startswith("chapter"):
        replace_in_text(soup, BARE_SECTION, make_bare, skip=NO_LINK_IN)
    if page == "g":
        def make_point(m):
            a = soup.new_tag("a", href="#point-" + m.group(1))
            a.string = m.group(0)
            return a
        replace_in_text(soup, POINT_IN_G, make_point, skip=NO_LINK_IN)
    if page == "e":
        replace_in_text(soup, re.compile(r"\((?:%s)(?:, (?:%s))*\)" % (ID_TOKEN, ID_TOKEN)),
                        lambda m: linked_tokens(soup, m.group(0), r"(?<![\w-])%s(?![\w-])" % ID_TOKEN, chapter_href),
                        skip=NO_LINK_IN)
    for table in soup.find_all("table"):
        head = header_of(table)
        ccols = [i for i, h in enumerate(head) if h in CHAPTER_COLUMNS]
        dcols = [i for i, h in enumerate(head) if h in DIAGRAM_COLUMNS]
        for tr in table.select("tbody tr"):
            tds = tr.find_all("td")
            for k in ccols:
                if k < len(tds):
                    replace_in_text(tds[k], re.compile(r"(?<![\w-])%s(?![\w-])" % ID_TOKEN),
                                    lambda m: linked_tokens(soup, m.group(0), ".+", chapter_href))
            for k in dcols:
                if k < len(tds):
                    replace_in_text(tds[k], re.compile(DID_TOKEN),
                                    lambda m: linked_tokens(soup, m.group(0), ".+", diagram_href))


def render(md_text, md_rel, page_url, page=""):
    """Markdown of the atlas -> BeautifulSoup of the page body, with links, anchors and diagrams."""
    soup = BeautifulSoup(MD(md_text), "html.parser")
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    toc = number_headings(soup)
    rewrite_links(soup, md_rel, page_url)
    embed_diagrams(soup, md_rel, page_url)
    anchor_rows(soup, page, page_url)
    link_sources(soup, page_url)
    link_references(soup, page, page_url)
    wrap_tables(soup)
    return soup, toc


# ---------------------------------------------------------------------------------------------------------------
# Page frame


def frame(url, title, body, description="", section=None, md_source=None, scripts=("site.js",), body_class="",
          robots=None):
    root = root_prefix(url)
    body = enhance_page(url, body, DIAGRAMS)
    nav = []
    for target, label in NAV:
        current = target == (section or url)
        nav.append('<a href="%s%s"%s>%s</a>' % (root, target, ' aria-current="page"' if current else "", esc(label)))
    md_link = ""
    if md_source:
        md_link = ' · <a href="%satlas/%s">Markdown of this page</a>' % (root, md_source)
    footer = ('<p>%s. An independent reference. It is not an official publication of the Philippine government, '
              'and it does not replace the laws, circulars and manuals that it cites.%s</p>'
              '<p><a href="%sabout.html">About the atlas</a> · <a href="%sreference/f.html">Sources</a> · '
              '<a href="%sreference/g.html">Open points</a>%s</p>'
              % (SITE_NAME, (" Facts on current events are as of %s." % FACTS_AS_OF) if FACTS_AS_OF else "",
                 root, root, root, md_link))
    page_title = title if title == SITE_NAME else "%s · %s" % (title, SITE_NAME)
    script_tags = "".join('<script src="%sassets/%s" defer></script>' % (root, s) for s in scripts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(description or title)}">{'<meta name="robots" content="%s">' % esc(robots) if robots else ''}
<meta name="color-scheme" content="light">
<script>document.documentElement.classList.add('js');try{{if(localStorage.getItem('pfm-atlas-theme')==='dark')document.documentElement.setAttribute('data-theme','dark');}}catch(error){{}}</script>
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body{' class="%s"' % body_class if body_class else ''}>
<a class="skip" href="#main">Skip to the content</a>
<header class="site-header">
<div class="wrap header-row">
<a class="brand" href="{root}index.html">{BRAND_MARK}<span>{SITE_NAME}</span></a>
<form class="header-search" action="{root}search.html" role="search"><label class="visually-hidden" for="q-top">Search the atlas</label><input id="q-top" name="q" type="search" placeholder="Search: SARO, voucher, BTMS"></form>
<button type="button" id="theme-toggle" class="theme-toggle" aria-label="Switch to dark mode">Dark mode</button>
</div>
<nav class="wrap site-nav" aria-label="Main">{''.join(nav)}</nav>
</header>
<main id="main" class="wrap">
{body}
</main>
<footer class="site-footer"><div class="wrap">{footer}</div></footer>
{script_tags}
</body>
</html>
"""


def toc_html(toc):
    items = []
    for level, hid, label in toc:
        items.append('<li%s><a href="#%s">%s</a></li>' % (' class="sub"' if level == "h3" else "", hid, esc(label)))
    return "<ol>%s</ol>" % "".join(items)


def document(url, soup, toc, eyebrow, md_source, section=None, chips="", pager="", before="", wide=False,
             description=""):
    h1 = soup.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else eyebrow
    if h1:
        h1.extract()
    head = '<div class="doc-head"><p class="eyebrow">%s</p><h1>%s</h1>%s</div>' % (esc(eyebrow), esc(title), chips)
    side = ""
    if toc:
        side = ('<aside class="doc-side"><nav class="toc" aria-label="On this page"><p class="toc-title">On this page</p>'
                '%s</nav></aside>' % toc_html(toc))
    mobile = ('<details class="toc-mobile"><summary>On this page</summary><nav class="toc">%s</nav></details>'
              % toc_html(toc)) if toc else ""
    body = ('%s<div class="doc%s">%s<article class="prose">%s%s%s</article></div>%s'
            % (head, " wide" if wide else "", side, mobile, before, str(soup), pager))
    return frame(url, title, body, description=description or title, section=section, md_source=md_source), title


def pager_html(prev, nxt):
    out = []
    if prev:
        out.append('<a class="prev" href="%s">← %s</a>' % (prev[0], esc(prev[1])))
    if nxt:
        out.append('<a class="next" href="%s">%s →</a>' % (nxt[0], esc(nxt[1])))
    return '<nav class="pager" aria-label="Pages">%s</nav>' % "".join(out) if out else ""


# ---------------------------------------------------------------------------------------------------------------
# Search index

SEARCH = []


def index_page(soup, url, page_title):
    """One entry for the text before the first heading and one for each section (h2 or h3)."""
    work = copy.copy(soup)
    for el in work.find_all(["pre", "details", "figure", "script"]):
        el.decompose()
    current = {"t": page_title, "p": page_title, "u": url, "x": []}
    entries = [current]
    for el in work.children:
        name = getattr(el, "name", None)
        if name in ("h2", "h3"):
            current = {"t": el.get_text(" ", strip=True), "p": page_title, "u": "%s#%s" % (url, el.get("id", "")), "x": []}
            entries.append(current)
        elif name:
            current["x"].append(el.get_text(" ", strip=True))
    for e in entries:
        text = re.sub(r"\s+", " ", " ".join(e["x"])).strip()
        if text or e["u"] == url:
            SEARCH.append({"t": e["t"], "p": e["p"], "u": e["u"], "x": text})


# ---------------------------------------------------------------------------------------------------------------
# Pages

WRITTEN = {}


def write_page(url, text):
    WRITTEN[url] = text
    save(DOCS / url, text)


def markdown_page(md_rel, url, eyebrow, page_key="", section=None, chips="", pager="", wide=False):
    soup, toc = render(read(ATLAS / md_rel), md_rel, url, page_key)
    if page_key == "g":
        insert_status_filter(soup)
    text, title = document(url, soup, toc, eyebrow, md_rel, section=section, chips=chips, pager=pager, wide=wide)
    write_page(url, text)
    index_page(soup, url, title)
    return soup


def insert_status_filter(soup):
    rows = soup.find_all("tr", attrs={"data-status": True})
    count = defaultdict(int)
    for tr in rows:
        count[tr["data-status"]] += 1
    buttons = ['<button type="button" data-status="all" aria-pressed="true">All points (%d)</button>' % len(rows)]
    for key in ("open", "partly", "settled", "differ"):
        buttons.append('<button type="button" data-status="%s" aria-pressed="false"><span class="status-dot st-%s" '
                       'aria-hidden="true"></span>%s (%d)</button>' % (key, key, STATUS_LABEL[key], count[key]))
    block = BeautifulSoup('<div class="filter" data-filter="points" role="group" aria-label="Show the points of one '
                          'status">%s</div>' % "".join(buttons), "html.parser")
    first_h2 = soup.find("h2")
    first_h2.insert_before(block)


def chapter_eyebrow(pid):
    key = PHASE_KEY[pid]
    if key == "shared":
        return "Technical reference · %s" % pid
    if is_phase_intro(pid):
        return "%s · Phase overview" % PHASE_NAME[key]
    return "Chapter %s · %s, step %s" % (pid, PHASE_NAME[key], pid[1:])


def build_chapters():
    ids = list(CHAPTER_FILE)
    for i, pid in enumerate(ids):
        p = CHAPTER_FILE[pid]
        prev = ("%s.html" % ids[i - 1], chapter_label(ids[i - 1])) if i > 0 else None
        nxt = ("%s.html" % ids[i + 1], chapter_label(ids[i + 1])) if i + 1 < len(ids) else None
        markdown_page("chapters/" + p.name, URL["chapters/" + p.name], chapter_eyebrow(pid),
                      page_key="chapter" + pid, section="chapters/index.html",
                      chips=chips_html(CHAPTER_TAGS.get(pid, [])), pager=pager_html(prev, nxt))


def build_references():
    for i, p in enumerate(REFERENCES):
        letter = p.name[0]
        prev = ("%s.html" % REFERENCES[i - 1].name[0].lower(), TITLE["reference/" + REFERENCES[i - 1].name]) if i > 0 else None
        nxt = ("%s.html" % REFERENCES[i + 1].name[0].lower(), TITLE["reference/" + REFERENCES[i + 1].name]) if i + 1 < len(REFERENCES) else None
        section = "reference/g.html" if letter == "G" else "reference/index.html"
        markdown_page("reference/" + p.name, URL["reference/" + p.name], "Reference %s" % letter,
                      page_key=letter.lower(), section=section, pager=pager_html(prev, nxt), wide=True)


# --- Home page -------------------------------------------------------------------------------------------------


def block(name):
    m = re.search(r"<!-- site:%s -->\s*\n(.*?)\n\s*<!-- /site:%s -->" % (re.escape(name), re.escape(name)),
                  read(BIG), re.S)
    if not m:
        fail("the block 'site:%s' is missing in the big picture" % name)
    return m.group(1).strip()


MAP = [
    ("authority", 70, "above", [("Appropriation", 330, "L5"), ("Allotment", 450, "E3"), ("Obligation", 590, "E4")]),
    ("claim", 160, "below", [("Plan", 330, "E1"), ("Procurement", 450, "E1"), ("Contract", 590, "E1"),
                             ("Delivery", 675, "E4"), ("Acceptance", 760, "E4")]),
    ("cash", 250, "below", [("Collection and borrowing", 330, "E5"), ("Single account of the Treasury", 460, "E5"),
                            ("Cash authority", 610, "E5"), ("Payment", 900, "E6"), ("Replenishment", 1005, "E6")]),
    ("records", 350, "below", [("Registries", 330, "A4"), ("Journal entries", 470, "A4"),
                               ("Certifications on each document", 620, "E4"), ("Reports", 790, "A4"), ("Audit", 930, "A9")]),
]
MEETINGS = [(1, 590, "authority", "claim"), (2, 760, "authority", "claim"), (3, 900, "claim", "cash")]


def split_label(label):
    if len(label) <= 16:
        return [label]
    spaces = [i for i, c in enumerate(label) if c == " "]
    cut = min(spaces, key=lambda i: abs(i - len(label) / 2))
    return [label[:cut], label[cut + 1:]]


def map_svg(steps_by_line):
    """The four lines with their main steps and the three meeting points. Each label is a word of the table of the
    four lines in section 2 of the big picture; the build stops if a label is missing there."""
    y_of = {key: y for key, y, _, _ in MAP}
    out = ['<svg viewBox="0 0 1080 412" role="group" aria-labelledby="map-title map-desc">',
           '<title id="map-title">The four lines of steps and the three points where they meet</title>',
           '<desc id="map-desc">Legal authority, the claim, cash, and records and control run at the same time. '
           'Meeting point 1 joins legal authority and the claim at the contract and the obligation. Meeting point 2 '
           'joins the obligation and the accepted delivery. Meeting point 3 joins the claim and the cash authority at '
           'the payment. Each step links to its chapter.</desc>']
    for key, y, _, _ in MAP:
        out.append('<text class="name %s" x="20" y="%d">%s</text>' % (key, y + 6, esc(LINE_NAMES[key])))
        out.append('<path class="track %s" d="M300 %dH1050"/>' % (key, y))
    for n, x, a, b in MEETINGS:
        out.append('<path class="meet" d="M%d %dV%d"/>' % (x, y_of[a], y_of[b]))
    stops_at = {(key, x) for key, _, _, stops in MAP for _, x, _ in stops}
    for key, y, side, stops in MAP:
        for label, x, chapter in stops:
            if label.lower() not in steps_by_line[key].lower():
                fail("the label '%s' of the map is not in the table of the four lines in the big picture" % label)
            out.append('<circle class="stop %s" cx="%d" cy="%d" r="8"/>' % (key, x, y))
            lines = split_label(label)
            if side == "above":
                y0 = y - 20 - 17 * (len(lines) - 1)
            else:
                y0 = y + 31
            texts = "".join('<text x="%d" y="%d" text-anchor="middle">%s</text>' % (x, y0 + 17 * i, esc(t))
                            for i, t in enumerate(lines))
            out.append('<a href="chapters/%s.html"><title>Chapter %s: %s</title>%s</a>'
                       % (chapter, chapter, esc(chapter_title(chapter)), texts))
    for n, x, a, b in MEETINGS:
        for key in (a, b):
            if (key, x) not in stops_at:
                out.append('<circle class="stop %s" cx="%d" cy="%d" r="6"/>' % (key, x, y_of[key]))
        cy = (y_of[a] + y_of[b]) // 2
        out.append('<a href="#meeting-point-%d" aria-label="Meeting point %d"><circle class="meet-dot" cx="%d" cy="%d" '
                   'r="15"/><text class="meet-num" x="%d" y="%d" text-anchor="middle">%d</text></a>'
                   % (n, n, x, cy, x, cy + 5, n))
    out.append("</svg>")
    return "\n".join(out)


def link_chapter_numbers(soup, cell, page_url):
    """Links for the chapter IDs in a cell, for example 'P0 to P12, L0 to L5'."""
    def make(m):
        if m.group(0) not in CHAPTER_FILE:
            return None
        a = soup.new_tag("a", href=relurl(page_url, "chapters/%s.html" % m.group(0)))
        a.string = m.group(0)
        return a
    replace_in_text(cell, re.compile(r"(?<![\w-])%s(?![\w-])" % ID_TOKEN), make)


def readme_table(heading_start):
    """Rows of the first table after a heading of the README of the atlas: (link target, other cells)."""
    rows, inside, seen_heading = [], False, False
    for line in read(README).split("\n"):
        if line.startswith(heading_start):
            seen_heading = True
            continue
        if not seen_heading:
            continue
        if line.startswith("|"):
            inside = True
            if is_separator(line):
                continue
            cells = table_cells(line)
            m = re.match(r"\[[^\]]*\]\(([^)]+)\)", cells[0])
            if m:
                rows.append((m.group(1), cells[1:]))
        elif inside:
            break
    return rows


def inline_md(text, md_rel, page_url):
    soup, _ = render(text, md_rel, page_url)
    p = soup.find("p")
    return "".join(str(c) for c in p.contents) if p else esc(text)


def build_home():
    url = "index.html"
    lines_md = block("lines")
    steps_by_line, lines_soup = {}, None
    for line in lines_md.split("\n"):
        if line.startswith("|") and not is_separator(line):
            cells = table_cells(line)
            if cells[0].isdigit():
                steps_by_line[LINES[int(cells[0]) - 1]] = cells[3]
    if set(steps_by_line) != set(LINES):
        fail("the table of the four lines in the big picture does not have four rows")
    lines_soup, _ = render(lines_md, "00_BIG_PICTURE.md", url)
    for tr in lines_soup.select("tbody tr"):
        n = tr.find("td").get_text(strip=True)
        if n.isdigit() and 1 <= int(n) <= 4:
            tr["class"] = "line-" + LINES[int(n) - 1]

    meet_soup, _ = render(block("meeting-points"), "00_BIG_PICTURE.md", url)
    ol = meet_soup.find("ol")
    if ol is None or len(ol.find_all("li", recursive=False)) != 3:
        fail("the block of the meeting points in the big picture does not have three numbered points")
    ol["class"] = "meeting-points"
    for i, li in enumerate(ol.find_all("li", recursive=False), 1):
        li["id"] = "meeting-point-%d" % i
        li["data-n"] = str(i)
        _, _, a, b = MEETINGS[i - 1]
        li.append(BeautifulSoup(chips_html([("line", a), ("line", b)]), "html.parser"))
    cases_soup, _ = render(block("cases"), "00_BIG_PICTURE.md", url)
    parts_soup, _ = render(block("parts"), "00_BIG_PICTURE.md", url)
    for tr in parts_soup.select("tbody tr"):
        link_chapter_numbers(parts_soup, tr.find_all("td")[-1], url)

    big = read(BIG)
    question = re.search(r"## 1\. [^\n]*\n\n([^\n]+)", big).group(1)
    first_para = re.search(r"## 2\. [^\n]*\n\n([^\n]+)", big).group(1)
    opening = " ".join(re.split(r"(?<=\.)\s+", first_para)[:2])
    g_text = read(ATLAS / "reference" / "G_open_questions_and_known_gaps.md")
    numbers = re.search(r"(In numbers: [^\n]*)", g_text)
    numbers = numbers.group(1) if numbers else ""

    lookup = []
    for target, cells in readme_table("## 5. The reference files"):
        if target in URL:
            lookup.append('<a href="%s"><strong>%s</strong><span>%s</span></a>'
                          % (URL[target], esc(TITLE[target]), inline_md(cells[0], "README.md", url)))
    n_mmd = sum(1 for d in DIAGRAMS if d["notation"] == "Mermaid")
    lookup.append('<a href="diagrams/index.html"><strong>Diagrams</strong><span>%d diagrams, %d in Mermaid and %d in '
                  'PlantUML, each with its image, its code and the question that it answers</span></a>'
                  % (len(DIAGRAMS), n_mmd, len(DIAGRAMS) - n_mmd))
    lookup.append('<a href="chapters/index.html"><strong>Chapters</strong><span>The %d chapters: one for each phase and '
                  'for each step of the budget cycle, and two on the information systems and on UACS</span></a>'
                  % len(CHAPTERS))

    body = f"""<div class="home">
<section class="home-intro">
<h1>{SITE_NAME}</h1>
<p class="lead">{esc(question)}</p>
<form class="search-large" action="search.html" role="search"><label class="visually-hidden" for="q-home">Search the atlas</label><input id="q-home" name="q" type="search" placeholder="A word, a code or a form: allotment, LDDAP-ADA, GAM-V1"><button type="submit">Search</button></form>
<p class="muted">Facts on current events are as of {esc(FACTS_AS_OF)}. An independent reference, not an official publication of the Philippine government. <a href="about.html">About the atlas</a>.</p>
</section>
<section class="start-paths" aria-label="Ways to explore the atlas">
<h2>Choose a reading path</h2>
<div class="path-grid"><a href="walkthrough.html"><strong>Learn the system</strong><span>Eight guided lessons, with curated diagrams and full references.</span><span class="more">Start walkthrough →</span></a><a href="chapters/index.html"><strong>Use the reference</strong><span>A chapter for each phase and for each of the 32 steps of the budget cycle, with linked primary-source citations.</span><span class="more">Browse chapters →</span></a><a href="systems.html"><strong>Examine systems</strong><span>Institutional mandates, BTMS and IFMIS, record identity and integration evidence.</span><span class="more">Explore systems →</span></a><a href="models/index.html"><strong>Study the models</strong><span>Earlier analytical diagrams and typed registers, separately identified.</span><span class="more">View research models →</span></a></div>
</section>
<section id="lines">
<h2>The four lines and the points where they meet</h2>
<div class="prose-block"><p>{inline_md(opening, "00_BIG_PICTURE.md", url)}</p></div>
<p class="map-hint">The drawing is wider than the screen. Move it sideways, or read the same lines in the table below it.</p>
<div class="map">{map_svg(steps_by_line)}</div>
<p class="map-note">Each step links to its chapter. The numbers 1 to 3 mark the meeting points, described below. Section 2 of the <a href="big-picture.html#section-2">big picture</a> explains the lines, and diagram <a href="diagrams/BP-d.html">BP-d</a> draws them as a net.</p>
{str(lines_soup)}
</section>
<section id="meeting-points">
<h2>Where the lines meet</h2>
<div class="prose-block">{str(meet_soup)}<div class="cases">{str(cases_soup)}</div></div>
</section>
<section id="parts">
<h2>The five parts and their chapters</h2>
{str(parts_soup)}
</section>
<section id="reference-files">
<h2>Reference files and diagrams</h2>
<div class="lookup">{''.join(lookup)}</div>
</section>
<section id="reliability">
<h2>How far the atlas can be relied on</h2>
<div class="prose-block"><p>From <a href="reference/g.html">Reference G</a>: {esc(numbers)}</p>
<p><a href="big-picture.html#section-15">Section 15 of the big picture</a> says what this means for the use of the atlas. <a href="reference/f.html">Reference F</a> names every source and how it was read.</p></div>
</section>
</div>"""
    page = frame(url, SITE_NAME, body, description=question, section="index.html", body_class="home-page",
                 scripts=("site.js", "cycle-story.js"))
    if page.count(budget_cycle_story.SLOT) != 1:
        fail("the place of the budget-cycle story is missing on the home page")

    def link_fragment(fragment):
        soup = BeautifulSoup(fragment, "html.parser")
        link_sources(soup, url)
        link_references(soup, "", url)
        return str(soup)

    try:
        story = budget_cycle_story.build(
            render_md=lambda md: str(render(md, "00_BIG_PICTURE.md", url)[0]), block=block, big_text=read(BIG),
            link=link_fragment, chapter_dir=ATLAS / "chapters", diagram_ids=set(DIAG),
            source_codes=set(CODES))
    except ValueError as exc:
        fail(str(exc))
    write_page(url, page.replace(budget_cycle_story.SLOT, story, 1))


# --- Index pages -------------------------------------------------------------------------------------------------


INDEX_GROUPS = [("preparation", "Budget phase 01", "Preparation"), ("legislation", "Budget phase 02", "Legislation"),
                ("execution", "Budget phase 03", "Execution"), ("accountability", "Budget phase 04", "Accountability"),
                ("shared", "Shared by all phases", "Information systems and UACS")]


def build_chapter_index():
    """Exactly 32 public numbered chapters, with separately labelled phase overviews and technical references."""
    from atlas_pages import STEP_ORDER
    url = "chapters/index.html"
    subjects = {posixpath.basename(t).split("_", 1)[0]: cells[0] for t, cells in readme_table("## 4. The chapters")}
    missing = [pid for pid in CHAPTER_FILE if pid not in subjects]
    if missing:
        fail("chapters without a subject in the README: " + ", ".join(missing))
    groups = []
    phase_order = [('preparation', 'Preparation', 'P'), ('legislation', 'Legislation', 'L'),
                   ('execution', 'Execution', 'E'), ('accountability', 'Accountability', 'A')]
    for key, title, letter in phase_order:
        intro_id = letter + '0'
        rows = []
        for pid in [i for i in STEP_ORDER if i.startswith(letter)]:
            diagrams = ", ".join('<a class="id" href="../diagrams/%s.html">%s</a>' % (d["id"], d["id"])
                                 for d in DIAGRAMS if d["chapter"] == pid)
            rows.append('<tr><td><a class="row-id" href="%s.html">%s</a></td><td><a href="%s.html">%s</a>%s</td>'
                        '<td>%s</td><td>%s</td></tr>' %
                        (pid, pid, pid, esc(chapter_title(pid)), chips_html(CHAPTER_TAGS.get(pid, [])),
                         inline_md(subjects[pid], "README.md", url), diagrams or '<span class="muted">—</span>'))
        groups.append('<section class="pfm-cycle-index-group" id="cycle-chapters-%s">'
                      '<p class="pfm-cycle-eyebrow">BUDGET PHASE</p><h2>%s</h2>'
                      '<p class="pfm-cycle-lede"><a href="%s.html">Read the %s phase overview</a></p>'
                      '<div class="table-wrap"><table><thead><tr><th>Step</th><th>Chapter</th><th>Subject</th>'
                      '<th>Diagrams</th></tr></thead><tbody>%s</tbody></table></div></section>' %
                      (key, esc(title), intro_id, esc(title), ''.join(rows)))
    extra = ('<section class="pfm-cycle-index-group" id="cycle-chapters-across">'
             '<h2>Technical references</h2><p>The information systems and record classifications support multiple '
             'activities; they are not additional numbered chapters.</p>'
             '<p><a href="IS.html">Information systems and IFMIS</a> · '
             '<a href="UACS.html">UACS and record identifiers</a></p></section>')
    body = ('<div class="doc-head"><p class="eyebrow">Budget cycle</p>'
            '<h1>32 activity chapters</h1></div>'
            '<p class="prose-block">Follow the four phases in budget-cycle order. '
            'Each numbered chapter corresponds to one activity. Phase introductions and technical '
            'references are available where relevant, without forming a second chapter sequence.</p>'
            '<div class="pfm-cycle-catalog" data-atlas-experience="1">%s%s%s</div>' %
            (budget_cycle_nav.section_nav("chapters"), ''.join(groups), extra))
    write_page(url, frame(url, "32 activity chapters", body, section="chapters/index.html"))


def build_reference_index():
    url = "reference/index.html"
    rows = []
    for target, cells in readme_table("## 5. The reference files"):
        if target in URL:
            letter = posixpath.basename(target)[0]
            rows.append('<tr><td><a class="row-id" href="%s">%s</a></td><td><a href="%s">%s</a></td><td>%s</td></tr>'
                        % (posixpath.basename(URL[target]), letter, posixpath.basename(URL[target]),
                           esc(re.sub(r"^Reference [A-Z]\.\s*", "", TITLE[target])),
                           inline_md(cells[0], "README.md", url)))
    body = ('<div class="doc-head"><p class="eyebrow">References</p><h1>The reference files</h1></div>'
            '<div class="table-wrap"><table><thead><tr><th></th><th>Reference</th><th>Content</th></tr></thead>'
            '<tbody>%s</tbody></table></div>'
            '<p class="prose-block">Three tables are also available as CSV files, for use in a spreadsheet or a program: '
            '<a href="../atlas/reference/diagram_index.csv">diagram_index.csv</a>, '
            '<a href="../atlas/reference/steps_register.csv">steps_register.csv</a> and '
            '<a href="../atlas/reference/interface_register.csv">interface_register.csv</a>.</p>' % "".join(rows))
    write_page(url, frame(url, "The reference files", body, section="reference/index.html"))


def build_diagram_index():
    url = "diagrams/index.html"
    groups = []
    for num in ["BP"] + list(CHAPTER_FILE):
        items = [d for d in DIAGRAMS if d["chapter"] == num]
        if not items:
            continue
        heading = "The big picture" if num == "BP" else chapter_label(num)
        lis = "".join('<li><span class="id">%s</span><div><a href="%s.html">%s</a> <span class="form">%s</span>'
                      '<span class="q">Question: %s</span></div></li>'
                      % (d["id"], d["id"], esc(d["title"]), esc(d["form"]), esc(d["question"])) for d in items)
        groups.append('<section class="diagram-group"><h2 id="chapter-%s">%s</h2><ul class="diagram-list">%s</ul></section>'
                      % (num, esc(heading), lis))
    n_mmd = sum(1 for d in DIAGRAMS if d["notation"] == "Mermaid")
    body = ('<div class="doc-head"><p class="eyebrow">Diagrams</p><h1>The diagrams</h1></div>'
            '<p class="prose-block">%d diagrams: %d in Mermaid and %d in PlantUML. The part of an ID before the hyphen '
            'names the chapter that shows the diagram; BP is the big picture. Each diagram has a page with its image, '
            'what it shows, its steps where it is a sequence, and its code.</p>'
            '<p><label for="diagram-filter">Filter by words: </label><input id="diagram-filter" type="search" '
            'placeholder="for example: voucher, BTMS, E4"> <span id="diagram-count" class="muted" role="status"></span></p>%s'
            % (len(DIAGRAMS), n_mmd, len(DIAGRAMS) - n_mmd, "".join(groups)))
    write_page(url, frame(url, "The diagrams", body, section="diagrams/index.html"))


def diagram_bullets(did):
    """The list under the line 'Code file:' of a diagram in its Markdown file, as Markdown."""
    d = DIAG[did]
    md_rel = d["embedded_in"].split(";")[0].strip()
    lines = read(ATLAS / md_rel).split("\n")
    start = next(i for i, l in enumerate(lines) if re.match(r"^#{3,4} Diagram %s(?![\w-])" % re.escape(did), l))
    i = start + 1
    while i < len(lines) and not lines[i].startswith("Code file:"):
        i += 1
    i += 1
    out = []
    while i < len(lines) and (not lines[i].strip() and not out or lines[i].startswith("- ")):
        if lines[i].startswith("- "):
            out.append(lines[i])
        i += 1
    return md_rel, "\n".join(out)


def build_diagram_pages():
    for i, d in enumerate(DIAGRAMS):
        did = d["id"]
        url = "diagrams/%s.html" % did
        md_rel, bullets = diagram_bullets(did)
        about, _ = render(bullets, md_rel, url)
        where = []
        for rel in [r.strip() for r in d["embedded_in"].split(";") if r.strip()]:
            where.append('<a href="%s">%s</a>' % (relurl(url, URL[rel]), esc(TITLE[rel])))
        soup = BeautifulSoup("", "html.parser")
        figure = diagram_figure(soup, did, url)
        figure.find("figcaption").decompose()
        steps = ""
        if STEPS[did]:
            rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                           % (esc(r["step"]), esc(r["who_acts"]), esc(r["towards_whom"]), esc(r["what_is_done_or_passed"]),
                              esc(r["basis"])) for r in STEPS[did])
            table = BeautifulSoup('<table><thead><tr><th>Step</th><th>Who acts</th><th>Towards whom</th>'
                                  '<th>What is done or passed</th><th>Basis</th></tr></thead><tbody>%s</tbody></table>'
                                  % rows, "html.parser")
            link_sources(table, url)
            wrap_tables(table)
            steps = '<h2 id="steps">Steps</h2><p>The numbers are those of the diagram.</p>%s' % str(table)
        code = read(ATLAS / d["code_file"])
        code_links = ('<div class="copy-row"><button type="button" data-copy="code-%s">Copy the code</button>'
                      '<a href="../atlas/%s">Code file</a><a href="../atlas/%s">Image in full size</a></div>'
                      % (did, d["code_file"], d["image"]))
        nav = pager_html(("%s.html" % DIAGRAMS[i - 1]["id"], "Diagram %s" % DIAGRAMS[i - 1]["id"]) if i > 0 else None,
                         ("%s.html" % DIAGRAMS[i + 1]["id"], "Diagram %s" % DIAGRAMS[i + 1]["id"]) if i + 1 < len(DIAGRAMS) else None)
        question = d["question"][:1].upper() + d["question"][1:]
        body = ('<div class="doc-head"><p class="eyebrow">Diagram <span class="id">%s</span> · %s</p><h1>%s</h1>'
                '<p class="prose-block"><strong>Question:</strong> %s</p><p class="muted">In: %s</p></div>%s'
                '<div class="prose-block"><h2 id="about">What the diagram shows</h2>%s</div>'
                '%s<h2 id="code">Code</h2>%s<pre id="code-%s"><code>%s</code></pre>%s'
                % (did, esc(d["form"]), esc(d["title"]), esc(question), " · ".join(where), str(figure), str(about),
                   steps, code_links, did, esc(code), nav))
        write_page(url, frame(url, "Diagram %s: %s" % (did, d["title"]), body, description=d["question"],
                              section="diagrams/index.html"))
        SEARCH.append({"t": "Diagram %s: %s" % (did, d["title"]), "p": "Diagrams", "u": url,
                       "x": re.sub(r"\s+", " ", "Question: %s %s" % (d["question"], about.get_text(" ", strip=True)))})


def build_search_page():
    url = "search.html"
    body = ('<div class="doc-head"><p class="eyebrow">Search</p><h1>Search the atlas</h1></div>'
            '<form id="search-form" class="search-page" action="search.html" role="search"><label class="visually-hidden" '
            'for="q">Search the atlas</label><input id="q" name="q" type="search" placeholder="A word, a code or a form">'
            '<button type="submit">Search</button></form>'
            '<p id="search-status" class="muted" role="status"></p><ol id="results"></ol>'
            '<noscript><p>The search needs JavaScript. Without it, use the <a href="chapters/index.html">chapters</a>, '
            'the <a href="reference/index.html">references</a> and the <a href="diagrams/index.html">diagrams</a>.</p></noscript>')
    write_page(url, frame(url, "Search", body, section="search.html", scripts=("site.js", "search.js")))


# ---------------------------------------------------------------------------------------------------------------


def clean_docs():
    for child in DOCS.iterdir():
        if child.name == "atlas":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def main():
    clean_docs()
    for name in ("style.css", "site.js", "search.js", "cycle-story.js", "favicon.svg"):
        save(DOCS / "assets" / name, read(SITE_FILES / name))
    save(DOCS / ".nojekyll", "")
    build_home()
    markdown_page("00_BIG_PICTURE.md", "big-picture.html", "The big picture", section="big-picture.html")
    build_chapters()
    build_references()
    markdown_page("README.md", "about.html", "About the atlas", section="about.html")
    build_chapter_index()
    build_reference_index()
    build_diagram_index()
    build_diagram_pages()
    build_search_page()
    from build_extensions import build_extensions
    build_extensions(globals())
    import forwarding
    n_forward = forwarding.build(write_page, frame, relurl, chapter_label, lambda d: DIAG[d]["title"],
                                 set(CHAPTER_FILE), set(DIAG))
    save(DOCS / "assets" / "search-index.json", json.dumps(SEARCH, ensure_ascii=False, separators=(",", ":")))
    # Preserve previous direct URLs for raw Markdown, diagram sources and PNGs, without exposing a second catalogue.
    legacy_root = ROOT / "preservation" / "legacy_web"
    if legacy_root.is_dir():
        for item in sorted(legacy_root.rglob("*")):
            if item.is_file():
                destination = DOCS / item.relative_to(legacy_root)
                if not destination.exists():
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, destination)
    print("built site: %d pages, %d diagrams, %d chapters, %d references, %d search entries, %d forwarding pages"
          % (len(WRITTEN), len(DIAGRAMS), len(CHAPTERS), len(REFERENCES), len(SEARCH), n_forward))


if __name__ == "__main__":
    main()
