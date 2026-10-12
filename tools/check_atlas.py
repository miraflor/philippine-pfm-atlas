#!/usr/bin/env python3
"""Consistency checks for the Philippine PFM Atlas.

Run from the root of the repository:

    python3 tools/check_atlas.py            # checks the built atlas in docs/atlas/
    python3 tools/check_atlas.py PATH       # checks the atlas in the folder PATH
    python3 tools/check_atlas.py --render   # also draws every Mermaid file with the program "mmdc", if it is installed

The script needs Python 3 and nothing else. It changes no file of the atlas.
It prints one line for each problem and ends with the number of problems. The exit code is 0 when there is none.

What it checks
  1  Every diagram file has an image in rendered/, and every image has a diagram file.
  2  Every diagram file states the question that it answers and names its sources.
  3  No Mermaid flowchart uses a reserved word of Mermaid (for example "end", "class", "call") as the name of a node.
     Such a file looks correct in a text editor and cannot be drawn.
  4  Every Mermaid or PlantUML code block in a Markdown file is equal to a diagram file without its comment lines,
     and every diagram file appears in at least one Markdown file.
  5  Every relative link in a Markdown file leads to a file that exists.
  6  Every source code in square brackets, for example [NBC599], is defined in Reference F, section 2.
     The same holds for the codes in the columns named "Basis".
  7  Every row of a table has as many cells as the header of the table, and no cell of a column "Basis" is empty.
  8  The three CSV files in reference/ agree with the diagram files and with the register of interfaces in Reference B.
     For every sequence diagram that has a table of steps: the number and the text of the steps agree with the diagram.
  9  Every paragraph of a Markdown file is on one line.
 10  No Markdown file contains an unfilled placeholder of the form {{NAME}}.

What it does not check
  Whether a statement of the atlas is true. That needs the sources. Reference F lists them, and Reference G lists
  the statements that are not verified.
"""
import csv, glob, os, re, shutil, subprocess, sys, tempfile

RESERVED = {"end", "class", "call", "click", "style", "default", "graph", "flowchart", "subgraph",
            "direction", "linkStyle", "classDef", "href", "interpolate"}

problems = []
def bad(kind, where, text):
    problems.append((kind, where, text))
    print("%-18s %s: %s" % (kind, where, text))

def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()

def code_without_comments(text, marker):
    """The code of a diagram file as it is shown in the Markdown files:
    comment lines removed (a comment that starts with ---- is a section mark and stays), double blank lines removed."""
    kept = []
    for line in text.split("\n"):
        t = line.strip()
        if t.startswith(marker) and not t[len(marker):].strip().startswith("----"):
            continue
        kept.append(line)
    res = []
    for line in kept:
        if line.strip() == "" and (not res or res[-1].strip() == ""):
            continue
        res.append(line)
    return "\n".join(res).strip("\n")

def comment_lines(text, marker):
    return [l.strip()[len(marker):].strip() for l in text.split("\n") if l.strip().startswith(marker)]

def diagram_type(text):
    for line in text.split("\n"):
        w = line.strip().split(" ")[0]
        if w in ("flowchart", "graph", "sequenceDiagram", "stateDiagram-v2", "erDiagram", "gantt", "timeline"):
            return w
    return ""

def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    render = "--render" in sys.argv[1:]
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = os.path.abspath(args[0]) if args else os.path.join(repo, "docs", "atlas")
    rel = lambda p: os.path.relpath(p, root)
    mmd = sorted(glob.glob(os.path.join(root, "diagrams", "mermaid", "*.mmd")))
    puml = sorted(glob.glob(os.path.join(root, "diagrams", "plantuml", "*.puml")))
    png = sorted(glob.glob(os.path.join(root, "rendered", "*.png")))
    mds = sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True))
    if not mmd or not mds:
        print("No atlas found in", root)
        return 2
    print("Atlas folder: %s" % root)
    print("Files: %d Mermaid, %d PlantUML, %d images, %d Markdown" % (len(mmd), len(puml), len(png), len(mds)))

    # 1 diagram files and images
    bases = {os.path.basename(p).rsplit(".", 1)[0]: p for p in mmd + puml}
    images = {os.path.basename(p)[:-4] for p in png}
    for b in sorted(set(bases) - images):
        bad("NO IMAGE", rel(bases[b]), "no file rendered/%s.png" % b)
    for b in sorted(images - set(bases)):
        bad("NO DIAGRAM FILE", "rendered/%s.png" % b, "no diagram file with this name")
    ids = {}
    for b in bases:
        ids.setdefault(b.split("_")[0], []).append(b)
    for i, names in sorted(ids.items()):
        if len(names) > 1:
            bad("SAME ID", i, "used by %s" % ", ".join(sorted(names)))

    # 2 header comments, 3 reserved words
    for p in mmd + puml:
        text = read(p)
        marker = "'" if p.endswith(".puml") else "%%"
        com = comment_lines(text, marker)
        if sum(1 for c in com if c.startswith("QUESTION THIS DIAGRAM ANSWERS:")) != 1:
            bad("NO QUESTION", rel(p), "the file needs exactly one comment line that starts with QUESTION THIS DIAGRAM ANSWERS:")
        if not any(re.search(r'\[[A-Za-z][A-Za-z0-9\-]*(?: [^\]\[]*)?\]', c) or "SOURCES" in c.split(":")[0] or c.startswith("GENERAL KNOWLEDGE") for c in com):
            bad("NO SOURCES", rel(p), "no comment line names a source in square brackets or general knowledge")
        if p.endswith(".mmd") and diagram_type(text) in ("flowchart", "graph"):
            found = set()
            for line in code_without_comments(text, "%%").split("\n"):
                t = line.strip()
                if not t or t.startswith(("classDef", "class ", "style ", "linkStyle", "subgraph", "end", "direction", "flowchart", "graph", "click ", "---", "title:", "config:")):
                    continue
                t = re.sub(r'"[^"]*"', '""', t)           # labels cannot contain node names
                t = re.sub(r'\|[^|]*\|', ' ', t)          # labels of arrows
                for m in re.finditer(r'(?<![\w.])([A-Za-z_][A-Za-z0-9_]*)\s*(?=\[|\(|\{|>|:::|\s*(?:-->|---|-\.|==>|===|~~~|--|$))', t):
                    if m.group(1) in RESERVED:
                        found.add(m.group(1))
            for w in sorted(found):
                bad("RESERVED WORD", rel(p), "node name '%s' is a reserved word of Mermaid" % w)

    # 4 code blocks in Markdown files against diagram files
    code = {}
    for p in mmd:
        code[code_without_comments(read(p), "%%")] = p
    for p in puml:
        code[code_without_comments(read(p), "'")] = p
    seen = set()
    for f in mds:
        text = read(f)
        for m in re.finditer(r'^```(mermaid|plantuml)\n(.*?)\n```\s*$', text, flags=re.S | re.M):
            block = m.group(2).strip("\n")
            if block in code:
                seen.add(code[block])
            else:
                first = block.split("\n")[1 if block.startswith("---") else 0][:60]
                bad("BLOCK DIFFERS", rel(f), "a %s block is not equal to any diagram file (%s ...)" % (m.group(1), first))
    for p in mmd + puml:
        if p not in seen:
            bad("NOT EMBEDDED", rel(p), "the diagram is in no Markdown file")

    # 5 relative links
    for f in mds:
        text = re.sub(r'^```.*?^```\s*$', '', read(f), flags=re.S | re.M)
        for m in re.finditer(r'\]\(([^)\s]+)\)', text):
            link = m.group(1)
            if re.match(r'^[a-z]+://', link) or link.startswith("#") or link.startswith("mailto:"):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(f), link.split("#")[0]))
            if not os.path.exists(target):
                bad("BROKEN LINK", rel(f), link)
        for m in re.finditer(r'`((?:\.\./)?(?:diagrams|rendered|reference|tools|processes)/[^`\s]+)`', text):
            target = os.path.normpath(os.path.join(os.path.dirname(f), m.group(1)))
            if not os.path.exists(target) and not os.path.exists(os.path.join(root, m.group(1))) and not os.path.exists(os.path.join(repo, m.group(1))):
                bad("BROKEN PATH", rel(f), m.group(1))

    # 6 source codes
    fpath = os.path.join(root, "reference", "F_sources_and_verification.md")
    defined = set()
    if not os.path.exists(fpath):
        bad("NO REFERENCE F", "reference/", "F_sources_and_verification.md is missing")
    else:
        ftext = read(fpath)
        part = re.split(r'(?m)^## 3\. ', re.split(r'(?m)^## 2\. ', ftext)[1])[0]
        for line in part.split("\n"):
            if line.startswith("|") and not line.startswith("| Code") and not line.startswith("|---"):
                for c in split_row(line)[0].split(","):
                    if c.strip():
                        defined.add(c.strip())
    shape = re.compile(r'^(?:[A-Za-z]+\d[A-Za-z0-9]*(?:-[A-Za-z0-9]+)*|[A-Z][A-Za-z0-9]*(?:-[A-Z0-9][A-Za-z0-9]*)+)$')
    roman = re.compile(r'^[IVX]+(?:-[A-Z])?$')
    used = {}
    def note(codeword, where):
        used.setdefault(codeword, set()).add(where)
    cite = re.compile(r'\[([A-Za-z][A-Za-z0-9\-]*)(?: [^\]\[]*)?\](?!\()')
    for f in mds:
        text = re.sub(r'^```.*?^```\s*$', '', read(f), flags=re.S | re.M)
        for m in cite.finditer(text):
            note(m.group(1), rel(f))
    for p in mmd + puml:
        marker = "'" if p.endswith(".puml") else "%%"
        for c in comment_lines(read(p), marker):
            for m in cite.finditer(c):
                note(m.group(1), rel(p))
    basis_cells = 0
    for f in mds:
        lines = re.sub(r'^```.*?^```\s*$', '', read(f), flags=re.S | re.M).split("\n")
        header = None
        for n, line in enumerate(lines, 1):
            if not line.startswith("|"):
                header = None
                continue
            cells = split_row(line)
            if header is None:
                header = cells
                continue
            if set(line.replace("|", "").strip()) <= set("-: "):
                continue
            # 7 table shape
            if len(cells) != len(header):
                bad("TABLE ROW", "%s line %d" % (rel(f), n), "%d cells, the header has %d" % (len(cells), len(header)))
                continue
            if "Basis" in header:
                cell = cells[header.index("Basis")]
                basis_cells += 1
                if not cell:
                    bad("EMPTY BASIS", "%s line %d" % (rel(f), n), line[:70])
                for tok in re.findall(r'[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*', cell):
                    if tok in defined:
                        note(tok, rel(f))
                    elif shape.match(tok) and not roman.match(tok):
                        note(tok, rel(f))
    for c in sorted(used):
        if c in defined:
            continue
        if shape.match(c) and not roman.match(c):
            bad("UNDEFINED CODE", ", ".join(sorted(used[c])[:3]), "[%s] is not defined in Reference F, section 2" % c)
    for c in sorted(defined - set(used)):
        bad("UNUSED CODE", "reference/F_sources_and_verification.md", "%s is defined and never used" % c)
    print("Source codes: %d defined, %d cells of columns 'Basis' checked" % (len(defined), basis_cells))

    # 8 CSV files
    ref = os.path.join(root, "reference")
    def rows_of(name):
        p = os.path.join(ref, name)
        if not os.path.exists(p):
            bad("NO CSV FILE", "reference/" + name, "missing")
            return []
        with open(p, encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    index = rows_of("diagram_index.csv")
    if index:
        listed = {r["code_file"] for r in index}
        real = {rel(p).replace(os.sep, "/") for p in mmd + puml}
        for x in sorted(real - listed):
            bad("CSV INDEX", "reference/diagram_index.csv", "no row for %s" % x)
        for x in sorted(listed - real):
            bad("CSV INDEX", "reference/diagram_index.csv", "row for a file that does not exist: %s" % x)
    steps = rows_of("steps_register.csv")
    by_file = {}
    for r in steps:
        by_file.setdefault(r["diagram_file"], []).append(r)
    for name, rows in sorted(by_file.items()):
        p = os.path.join(root, "diagrams", "mermaid", name)
        if not os.path.exists(p):
            bad("CSV STEPS", "reference/steps_register.csv", "diagram file %s does not exist" % name)
            continue
        msgs = []
        for line in read(p).split("\n"):
            m = re.match(r'(\w+)(-->>|->>)(\w+): (.*)', line.strip())
            if m:
                t = re.sub(r'(<br/>)?#nbsp;', '', m.group(4))
                msgs.append(re.sub(r'<br/>', ' ', t).replace("|", "/").strip())
        if [int(r["step"]) for r in rows] != list(range(1, len(msgs) + 1)):
            bad("CSV STEPS", name, "the diagram has %d steps, the register has %d rows" % (len(msgs), len(rows)))
            continue
        for r, msg in zip(rows, msgs):
            if r["what_is_done_or_passed"] != msg:
                bad("CSV STEPS", name, "step %s differs from the diagram" % r["step"])
            if not r["basis"].strip():
                bad("CSV STEPS", name, "step %s has no basis" % r["step"])
    iface = rows_of("interface_register.csv")
    bpath = os.path.join(ref, "B_information_systems_inventory.md")
    if iface and os.path.exists(bpath):
        table = []
        on = False
        for line in read(bpath).split("\n"):
            if line.startswith("### 4.1") or line.startswith("### 4.2") or line.startswith("### 4.3"):
                on = True
            elif line.startswith("## ") or line.startswith("### "):
                on = False
            if on and line.startswith("|"):
                c = split_row(line)
                if len(c) == 9 and c[0].isdigit():
                    table.append(c)
        if len(table) != len(iface):
            bad("CSV INTERFACES", "reference/interface_register.csv", "%d rows, Reference B has %d" % (len(iface), len(table)))
        else:
            for c, r in zip(table, iface):
                if c != [r["no"], r["from"], r["to"], r["what_passes"], r["kind"], r["carrier"], r["stage_of_use"], r["check_of_both_sides"], r["basis"]]:
                    bad("CSV INTERFACES", "reference/interface_register.csv", "row %s differs from Reference B" % r["no"])
    print("CSV files: %d diagrams, %d steps of %d sequence diagrams, %d interfaces" % (len(index), len(steps), len(by_file), len(iface)))

    # 9 one paragraph = one line
    plain = lambda s: bool(s.strip()) and not re.match(r'^\s*(\||#|[-*+] |\d+\. |>|```|<|!\[|\*Part of|\{\{)', s)
    for f in mds:
        lines = read(f).split("\n")
        fence = False
        for n in range(len(lines) - 1):
            if lines[n].startswith("```"):
                fence = not fence
            if fence:
                continue
            if plain(lines[n]) and plain(lines[n + 1]) and not lines[n + 1].startswith("```"):
                bad("WRAPPED PARAGRAPH", "%s line %d" % (rel(f), n + 1), lines[n][:60])

    # 10 no unfilled placeholder
    for f in mds:
        text = re.sub(r'^```.*?^```\s*$', '', read(f), flags=re.S | re.M)
        for m in re.finditer(r'\{\{[A-Za-z_:|0-9 ,=.;-]+\}\}', text):
            bad("PLACEHOLDER", rel(f), m.group(0)[:60])

    # optional: draw every Mermaid file
    if render:
        exe = shutil.which("mmdc")
        if not exe:
            print("--render: the program mmdc was not found. Install the package @mermaid-js/mermaid-cli to use this option.")
        else:
            tmp = tempfile.mkdtemp(prefix="atlas_render_")
            ok = 0
            for p in mmd:
                out = os.path.join(tmp, os.path.basename(p)[:-4] + ".svg")
                cmd = [exe, "-i", p, "-o", out]
                cfg = os.environ.get("MMDC_PUPPETEER_CONFIG")
                if cfg:
                    cmd += ["-p", cfg]
                r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                if r.returncode == 0 and os.path.exists(out):
                    ok += 1
                else:
                    bad("DOES NOT RENDER", rel(p), (r.stdout or "").strip().split("\n")[0][:120])
            shutil.rmtree(tmp, ignore_errors=True)
            print("--render: %d of %d Mermaid files were drawn" % (ok, len(mmd)))

    print("")
    print("Problems found: %d" % len(problems))
    return 0 if not problems else 1

if __name__ == "__main__":
    sys.exit(main())
