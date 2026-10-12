#!/usr/bin/env python3
"""Check the website in docs/ after tools/build_site.py.

Run from the root of the repository:

    python3 tools/validate_site.py

It checks:
  1. Every page has a language, a title, a main heading and the style sheet.
  2. Every local link and image leads to a file that exists, and every link to an anchor (#...) finds that anchor.
  3. No page loads a script, a style sheet or an image from another server.
  4. Every Markdown file of the atlas has its page, and every diagram has its page, its code file and its image.
  5. Every paragraph, list item, heading and table cell of each Markdown file appears on its page, word for word.
  6. Every source code in square brackets that Reference F defines is a link to Reference F.
  7. The fixed anchors exist: every point of Reference G, every row of the register in Reference B, every source
     of Reference F.
  8. The statuses of the points of Reference G agree with the numbers that Reference G states.
  9. The home page has the drawing of the four lines, the three meeting points and the table of the five parts.
 10. The search index covers every page of text.
It ends with "Issues: 0" when everything agrees, and exits with code 1 otherwise.
"""
import csv
import json
import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import mistune
from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ATLAS = DOCS / "atlas"
MD = mistune.create_markdown(escape=False, plugins=["table", "strikethrough", "url"])
issues = []


def issue(msg):
    issues.append(msg)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


# --- Which page shows which Markdown file ---
URL = {"00_BIG_PICTURE.md": "big-picture.html", "README.md": "about.html"}
for p in sorted(ATLAS.glob("processes/[0-9][0-9]_*.md")):
    URL["processes/" + p.name] = "chapters/%s.html" % p.name[:2]
for p in sorted(ATLAS.glob("reference/[A-Z]_*.md")):
    URL["reference/" + p.name] = "reference/%s.html" % p.name[0].lower()

pages = {}
for path in sorted(DOCS.rglob("*.html")):
    rel = path.relative_to(DOCS).as_posix()
    if rel.startswith("atlas/"):
        continue
    pages[rel] = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
ids = {rel: {el["id"] for el in soup.find_all(id=True)} for rel, soup in pages.items()}

# --- 1 to 3: structure, links, anchors, outside resources ---
n_links = n_anchors = 0
for rel, soup in pages.items():
    if not (soup.html and soup.html.get("lang")):
        issue(f"{rel}: no language on <html>")
    if not soup.title or not soup.title.get_text(strip=True):
        issue(f"{rel}: no <title>")
    if not soup.find("h1"):
        issue(f"{rel}: no main heading")
    if not soup.find("link", rel="stylesheet", href=re.compile(r"assets/style\.css$")):
        issue(f"{rel}: no style sheet")
    if "<!-- site:" in str(soup) or "{{" in soup.get_text():
        issue(f"{rel}: a build marker or directive remains in the page")
    for tag, attr in (("script", "src"), ("link", "href"), ("img", "src"), ("iframe", "src"), ("source", "src")):
        for el in soup.find_all(tag, attrs={attr: True}):
            if re.match(r"^(https?:)?//", el[attr]):
                issue(f"{rel}: <{tag}> loads {el[attr]} from another server")
    for el in soup.find_all(["a", "img", "script", "link"]):
        value = el.get("href") or el.get("src")
        if not value or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", value) or value.startswith("//"):
            continue
        parts = urlsplit(value)
        target = rel if not parts.path else posixpath.normpath(posixpath.join(posixpath.dirname(rel), unquote(parts.path)))
        if not (DOCS / target).is_file():
            issue(f"{rel}: broken link {value}")
            continue
        n_links += 1
        if parts.fragment and target.endswith(".html"):
            n_anchors += 1
            if parts.fragment not in ids.get(target, set()):
                issue(f"{rel}: the anchor #{parts.fragment} does not exist in {target}")

# --- 4: pages and files that must exist ---
for md_rel, url in URL.items():
    if url not in pages:
        issue(f"no page {url} for {md_rel}")
for name in ["index.html", "search.html", "chapters/index.html", "reference/index.html", "diagrams/index.html",
             ".nojekyll", "assets/style.css", "assets/site.js", "assets/search.js", "assets/favicon.svg",
             "assets/search-index.json"]:
    if not (DOCS / name).is_file():
        issue(f"missing file docs/{name}")
with open(ATLAS / "reference" / "diagram_index.csv", encoding="utf-8", newline="") as fh:
    diagrams = list(csv.DictReader(fh))
for d in diagrams:
    for p in (DOCS / "diagrams" / (d["id"] + ".html"), ATLAS / d["code_file"], ATLAS / d["image"]):
        if not p.is_file():
            issue(f"diagram {d['id']}: missing {p.relative_to(ROOT)}")

# --- 5 and 6: every text unit of the atlas is on its page; every source code is a link ---
codes, head = set(), None
for line in (ATLAS / "reference" / "F_sources_and_verification.md").read_text(encoding="utf-8").split("\n"):
    if not line.startswith("|"):
        head = None
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if head is None:
        head = cells
    elif head[:2] == ["Code", "Source"] and not set(line.strip()) <= set("|-: "):
        codes.add(cells[0].strip("`"))
BRACKET = re.compile(r"\[([A-Za-z][A-Za-z0-9\-]*)((?: [^\[\]]*)?)\]")


def bracket_marks(soup):
    n = 0
    for node in soup.find_all(string=True):
        if isinstance(node, Comment) or any(p.name in ("a", "code", "pre", "script", "style", "summary") for p in node.parents if p):
            continue
        n += sum(1 for m in BRACKET.finditer(str(node)) if m.group(1) in codes)
    return n


n_units = n_marks = 0
for md_rel, url in URL.items():
    if url not in pages:
        continue
    source = BeautifulSoup(MD((ATLAS / md_rel).read_text(encoding="utf-8")), "html.parser")
    for el in source.find_all("pre"):
        el.decompose()
    for c in source.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    page_main = pages[url].find("main")
    page_text = norm(page_main.get_text(""))
    for el in source.find_all(["p", "li", "td", "th", "h1", "h2", "h3", "h4"]):
        unit = norm(el.get_text(""))
        if not unit:
            continue
        n_units += 1
        if unit not in page_text:
            issue(f"{url}: text of {md_rel} not found on the page: {unit[:90]}")
    expected = bracket_marks(source)
    linked = sum(1 for a in page_main.find_all("a", class_="basis") if a.get_text().startswith("["))
    n_marks += linked
    if expected != linked:
        issue(f"{url}: {expected} source codes in square brackets, {linked} linked to Reference F")

# --- 7: fixed anchors ---
def numbers_in_tables(md_rel, first_cells):
    out = set()
    head = None
    for line in (ATLAS / md_rel).read_text(encoding="utf-8").split("\n"):
        if not line.startswith("|"):
            head = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if head is None:
            head = cells
            continue
        if head[:len(first_cells)] == first_cells and cells[0].isdigit():
            out.add(cells[0])
    return out


g_md = next(r for r in URL if r.startswith("reference/G_"))
b_md = next(r for r in URL if r.startswith("reference/B_"))
g_points = numbers_in_tables(g_md, ["No."])
for n in sorted(g_points, key=int):
    if "point-" + n not in ids.get("reference/g.html", set()):
        issue(f"reference/g.html: no anchor point-{n}")
b_rows = numbers_in_tables(b_md, ["No.", "From", "To"])
for n in sorted(b_rows, key=int):
    if "flow-" + n not in ids.get("reference/b.html", set()):
        issue(f"reference/b.html: no anchor flow-{n}")
f_ids = ids.get("reference/f.html", set())
for code in sorted(codes):
    slug = re.sub(r"[^a-z0-9]+", "-", code.lower()).strip("-")
    if "source-" + slug not in f_ids:
        issue(f"reference/f.html: no anchor source-{slug}")
for mark in ("mark-gk", "mark-inference"):
    if mark not in f_ids:
        issue(f"reference/f.html: no anchor {mark}")

# --- 8: statuses of the points of Reference G ---
g_page = pages.get("reference/g.html")
statuses = {}
if g_page:
    for tr in g_page.find_all("tr", attrs={"data-status": True}):
        statuses[tr["data-status"]] = statuses.get(tr["data-status"], 0) + 1
    stated = re.search(r"the file has (\d+) points\. (\d+) are differences between sources.*?(\d+) are facts that I could "
                       r"not verify.*?(\d+) of them are settled, (\d+) are settled in part, and (\d+) are open",
                       (ATLAS / g_md).read_text(encoding="utf-8"))
    if not stated:
        issue("Reference G: the sentence with the numbers of points was not found")
    else:
        total, differ, facts, settled, partly, open_ = (int(x) for x in stated.groups())
        found = (sum(statuses.values()), statuses.get("differ", 0), statuses.get("settled", 0) + statuses.get("partly", 0)
                 + statuses.get("open", 0), statuses.get("settled", 0), statuses.get("partly", 0), statuses.get("open", 0))
        if found != (total, differ, facts, settled, partly, open_):
            issue(f"Reference G states {total} points ({differ} differences; {settled} settled, {partly} in part, {open_} "
                  f"open), the page finds {found[0]} ({found[1]} differences; {found[3]} settled, {found[4]} in part, "
                  f"{found[5]} open)")

# --- 9: home page ---
home = pages.get("index.html")
if home:
    if len(home.select(".map path.track")) != 4:
        issue("index.html: the drawing does not have four lines")
    if len(home.select(".map circle.meet-dot")) != 3:
        issue("index.html: the drawing does not have three meeting points")
    if len(home.select("ol.meeting-points > li")) != 3:
        issue("index.html: the list of the meeting points does not have three items")
    if len(home.select("#parts tbody tr")) != 5:
        issue("index.html: the table of the five parts does not have five rows")
    if len(home.select("#lines tbody tr")) != 4:
        issue("index.html: the table of the four lines does not have four rows")

# --- 10: search index ---
try:
    index = json.loads((DOCS / "assets" / "search-index.json").read_text(encoding="utf-8"))
    covered = {e["u"].split("#")[0] for e in index}
    for md_rel, url in URL.items():
        if url not in covered:
            issue(f"the search index has no entry for {url}")
    for d in diagrams:
        if "diagrams/%s.html" % d["id"] not in covered:
            issue(f"the search index has no entry for diagram {d['id']}")
except (OSError, ValueError, KeyError) as exc:
    issue(f"the search index cannot be read: {exc}")
    index = []

print(f"Pages: {len(pages)} | local links: {n_links} | links to anchors: {n_anchors} | atlas text units found: "
      f"{n_units} | source codes linked: {n_marks} | points of G: {len(g_points)} {dict(sorted(statuses.items()))} | "
      f"rows of the register: {len(b_rows)} | search entries: {len(index)}")
print(f"Issues: {len(issues)}")
for msg in issues[:100]:
    print(" -", msg)
sys.exit(1 if issues else 0)
