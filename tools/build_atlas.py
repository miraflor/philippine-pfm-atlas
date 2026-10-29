#!/usr/bin/env python3
"""Build the Markdown files of the atlas from the sources in src/.

Run from the root of the repository:

    python3 tools/build_atlas.py           # writes docs/atlas/ from src/
    python3 tools/build_atlas.py --check   # builds into a temporary folder and reports any file of docs/atlas/ that differs

Directives in the source files (each alone on a line):
  {{mermaid:ID}}             embed a Mermaid diagram (ID = unique file-name prefix, for example E4-a)
  {{plantuml:ID}}            embed a PlantUML diagram as image + code
                             The heading of an embedded diagram is one level below the heading before it.
  {{steps:ID|1=CODE;2-4=CODE;...}}   table of the numbered steps of a sequence diagram
  {{index:diagrams}}         table of all diagram files (id, title, form, code file, image)
  {{count:interfaces}}       counts by carrier, stage of use and kind of the register of interfaces in the same file
  {{register:SIDE}}          short table of the register of interfaces of Reference B (SIDE = spending, revenue, inside)

Besides the Markdown files, the script copies the diagram files from src/diagrams/ to docs/atlas/diagrams/ and writes
three CSV files into docs/atlas/reference/: diagram_index.csv, steps_register.csv, interface_register.csv.
It does not draw the images in docs/atlas/rendered/. For that, see tools/render_diagrams.py.
"""
import os, re, sys, glob, csv, shutil, tempfile, filecmp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_pages import diagram_sort_key, page_of_diagram  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "docs", "atlas")
MMD = os.path.join(SRC, "diagrams", "mermaid")
PUML = os.path.join(SRC, "diagrams", "plantuml")

LABELS = [
    ("QUESTION THIS DIAGRAM ANSWERS", "Question"),
    ("IDEA", "Idea"),
    ("READING", "How to read it"),
    ("FORM", "Form"),
]

def find(folder, ident, ext):
    hits = sorted(glob.glob(os.path.join(folder, ident + "*" + ext)))
    if len(hits) != 1:
        raise SystemExit(f"directive {ident}{ext}: {len(hits)} matches {hits}")
    return hits[0]

def split_comments(text, marker):
    """Return (comments, code_without_header_comments).
    A comment that starts with ---- is a section mark inside the code and stays in the code."""
    comments, code = [], []
    for line in text.split("\n"):
        t = line.strip()
        if t.startswith(marker) and not t[len(marker):].strip().startswith("----"):
            comments.append(t[len(marker):].strip())
        else:
            code.append(line)
    return comments, "\n".join(code)

def mermaid_title(text):
    m = re.search(r'^title:\s*"(.*)"\s*$', text, flags=re.M)
    if m:
        return m.group(1)
    m = re.search(r'^\s*title\s+(.*)$', text, flags=re.M)
    return m.group(1).strip() if m else ""

ACRONYMS = {"DBCC", "UACS", "DBM", "GK", "BTMS", "FAR", "GAA", "NCA", "IFMIS", "COA", "BTr", "FY", "I"}
SPECIAL = {"PLANTUML": "PlantUML"}

def smart_label(head):
    """Sentence case for a heading written in capitals. Acronyms and text in brackets stay as written."""
    out = []
    for tok in re.split(r'(\[[^\]]*\]|\([^)]*\)|\s+)', head):
        if tok is None or tok == "":
            continue
        if tok.isspace() or tok.startswith("[") or tok.startswith("("):
            out.append(tok)
            continue
        core = tok.strip(",.;")
        if core in SPECIAL:
            out.append(tok.replace(core, SPECIAL[core]))
        elif core in ACRONYMS or re.match(r'^\d', core):
            out.append(tok)
        else:
            out.append(tok.lower())
    s = "".join(out)
    return s[:1].upper() + s[1:]

def comment_block(comments):
    out = []
    for c in comments:
        head, sep, body = c.partition(":")
        bare = re.sub(r'\[[^\]]*\]|\([^)]*\)', '', head)
        is_head = bool(sep) and re.search(r'[A-Z]', bare) and not re.search(r'[a-z]', bare) and len(head) < 90
        if is_head:
            head = head.strip()
            label = None
            for key, lab in LABELS:
                if head == key:
                    label = lab
            if label is None:
                label = smart_label(head)
            out.append(f"- **{label}:** {body.strip()}")
        else:
            out.append(f"- {c}")
    return "\n".join(out)

def tidy_code(code):
    # drop blank lines left where comment lines were removed (keep single blank lines)
    lines = code.split("\n")
    res = []
    for l in lines:
        if l.strip() == "" and (not res or res[-1].strip() == ""):
            continue
        res.append(l)
    return "\n".join(res).strip("\n")

def emb_mermaid(ident, rel, level=3):
    path = find(MMD, ident, ".mmd")
    base = os.path.basename(path)[:-4]
    text = open(path, encoding="utf-8").read()
    title = mermaid_title(text)
    comments, code = split_comments(text, "%%")
    parts = [f"{'#' * level} Diagram {title}", "",
             f"Code file: `{rel}diagrams/mermaid/{base}.mmd`. Rendered image: [`{rel}rendered/{base}.png`]({rel}rendered/{base}.png).", ""]
    if comments:
        parts += [comment_block(comments), ""]
    parts += ["```mermaid", tidy_code(code), "```", ""]
    return "\n".join(parts)

def emb_plantuml(ident, rel, level=3):
    path = find(PUML, ident, ".puml")
    base = os.path.basename(path)[:-5]
    text = open(path, encoding="utf-8").read()
    m = re.search(r'^title\s+(.*)$', text, flags=re.M)
    title = m.group(1).strip() if m else base
    comments, code = split_comments(text, "'")
    parts = [f"{'#' * level} Diagram {title} (PlantUML)", "",
             f"Code file: `{rel}diagrams/plantuml/{base}.puml`. Rendered image: [`{rel}rendered/{base}.png`]({rel}rendered/{base}.png).", ""]
    if comments:
        parts += [comment_block(comments), ""]
    parts += [f"![{title}]({rel}rendered/{base}.png)", "",
              "<details>", "<summary>PlantUML code</summary>", "",
              "```plantuml", tidy_code(code), "```", "", "</details>", ""]
    return "\n".join(parts)

def parse_basis(spec):
    d = {}
    for item in spec.split(";"):
        item = item.strip()
        if not item:
            continue
        k, v = item.split("=", 1)
        k = k.strip(); v = v.strip()
        for part in k.split(","):
            part = part.strip()
            if "-" in part:
                a, b = part.split("-")
                for i in range(int(a), int(b) + 1):
                    d[i] = v
            else:
                d[int(part)] = v
    return d

def emb_steps(arg, rel):
    ident, _, spec = arg.partition("|")
    path = find(MMD, ident.strip(), ".mmd")
    text = open(path, encoding="utf-8").read()
    basis = parse_basis(spec)
    parts_map = {}
    rows = []
    n = 0
    for line in text.split("\n"):
        t = line.strip()
        m = re.match(r'participant (\w+) as (.*)', t)
        if m:
            parts_map[m.group(1)] = re.sub(r'<br/>', ' ', m.group(2))
            continue
        m = re.match(r'(\w+)(-->>|->>)(\w+): (.*)', t)
        if m:
            n += 1
            a, _, b, msg = m.groups()
            msg = re.sub(r'(<br/>)?#nbsp;', '', msg)   # spacer line used only for the picture
            msg = re.sub(r'<br/>', ' ', msg).replace("|", "/").strip()
            who = parts_map.get(a, a)
            to = parts_map.get(b, b)
            if n not in basis:
                raise SystemExit(f"{os.path.basename(path)}: no basis given for step {n}")
            target = "(own action)" if a == b else to
            rows.append(f"| {n} | {who} | {target} | {msg} | {basis[n]} |")
            STEP_ROWS.append([os.path.basename(path)[:-4].split("_")[0], os.path.basename(path), n, who, target, msg, basis[n]])
    extra = [k for k in basis if k > n]
    if extra:
        raise SystemExit(f"{os.path.basename(path)}: basis given for steps that do not exist {extra}")
    head = ["| No. | Who acts | Towards whom | What is done or passed | Basis |", "|---|---|---|---|---|"]
    return "\n".join(head + rows) + "\n"

EMBEDDED = set()
EMBED_AT = {}      # diagram file name -> list of Markdown files that embed it
STEP_ROWS = []     # rows for steps_register.csv
IFACE_ROWS = []    # rows for interface_register.csv

KINDS = ["Data", "Document", "Authority", "Money"]
CARRIERS = ["System to system", "Entry by the sender", "Download by the receiver", "Entry in own system",
            "Electronic, kind not stated", "Paper", "Bank transfer", "Cash or check", "Public website", "Not stated"]
STAGES = ["In use", "In use for part", "Described or required, use not verified", "Planned", "Not stated"]
SIDES = [("### 4.1", "spending"), ("### 4.2", "revenue and treasury"), ("### 4.3", "inside one agency")]
REGISTER_FILE = os.path.join(SRC, "reference", "B_information_systems_inventory.md")

def read_register(text):
    """Rows of the register of interfaces: tables under the headings '### 4.1', '### 4.2' and '### 4.3'.
    A row has nine cells: No., From, To, What passes, Kind, Carrier, Stage of use, Check of both sides, Basis.
    Returned row: [no, side, from, to, what, kind, carrier, stage, check, basis]."""
    rows, side = [], None
    for line in text.split("\n"):
        hit = [s for h, s in SIDES if line.startswith(h)]
        if hit:
            side = hit[0]
        elif line.startswith("### ") or line.startswith("## "):
            side = None
        if side and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[0].isdigit():
                if len(cells) != 9:
                    raise SystemExit(f"register of interfaces: row {cells[0]} has {len(cells)} cells, 9 expected")
                if cells[4] not in KINDS:
                    raise SystemExit(f"register of interfaces: unknown kind '{cells[4]}' in row {cells[0]}")
                if cells[5] not in CARRIERS:
                    raise SystemExit(f"register of interfaces: unknown carrier '{cells[5]}' in row {cells[0]}")
                if cells[6] not in STAGES:
                    raise SystemExit(f"register of interfaces: unknown stage '{cells[6]}' in row {cells[0]}")
                if not cells[7] or not cells[8]:
                    raise SystemExit(f"register of interfaces: empty cell in row {cells[0]}")
                if cells[8] == "GK" and (cells[5] != "Not stated" or cells[6] != "Not stated"):
                    raise SystemExit(f"register of interfaces: row {cells[0]} is based on GK, so carrier and stage must be 'Not stated'")
                if (cells[4] == "Money") != (cells[5] in ("Bank transfer", "Cash or check")):
                    raise SystemExit(f"register of interfaces: row {cells[0]}: the kind Money needs a money carrier, and a money carrier needs the kind Money")
                rows.append([int(cells[0]), side] + cells[1:])
    nums = [r[0] for r in rows]
    # The number of a row is an identifier that does not change, so that other texts can cite it. A row that is
    # added receives the next free number and stands in the table of its side. A row that is removed leaves its
    # number unused. Each number may therefore occur only once, and gaps are allowed.
    repeated = sorted({n for n in nums if nums.count(n) > 1})
    if repeated or any(n < 1 for n in nums):
        raise SystemExit(f"register of interfaces: each row number must be positive and occur once; repeated: {repeated}")
    return rows

def count_table(rows, col, values, head):
    sides = [s for _, s in SIDES]
    out = [f"| {head} | Spending side | Revenue and treasury side | Inside one agency | Total |", "|---|---|---|---|---|"]
    tot = [0, 0, 0]
    for v in values:
        n = [sum(1 for r in rows if r[col] == v and r[1] == s) for s in sides]
        if sum(n) == 0:
            continue
        tot = [a + b for a, b in zip(tot, n)]
        out.append(f"| {v} | {n[0]} | {n[1]} | {n[2]} | {sum(n)} |")
    out.append(f"| All rows | {tot[0]} | {tot[1]} | {tot[2]} | {sum(tot)} |")
    return out

def emb_count(arg, text):
    if arg != "interfaces":
        raise SystemExit("unknown count directive " + arg)
    rows = read_register(text)
    IFACE_ROWS[:] = rows
    out = ["By carrier:", ""] + count_table(rows, 6, CARRIERS, "Carrier")
    out += ["", "By stage of use:", ""] + count_table(rows, 7, STAGES, "Stage of use")
    out += ["", "By kind:", ""] + count_table(rows, 5, KINDS, "Kind")
    data = [r for r in rows if r[5] != "Money"]
    n = lambda c: sum(1 for r in data if r[6] == c)
    gk = sum(1 for r in rows if r[9] == "GK" or "The flow: GK" in r[9])
    out += ["", f"The register has {len(rows)} rows. {len(rows) - len(data)} of them are movements of money. Of the other {len(data)} rows:",
            "",
            f"- {n('System to system')} have the carrier \"System to system\". The number of these with the stage \"In use\" for all users is {sum(1 for r in data if r[6] == 'System to system' and r[7] == 'In use')}.",
            f"- {n('Entry by the sender')} are entered or uploaded by a person of the sending body in a system of the receiver.",
            f"- {n('Entry in own system')} are entered by staff in a record or system of their own body.",
            f"- {n('Paper')} pass on paper.",
            f"- {n('Download by the receiver') + n('Public website')} are downloads or public websites.",
            f"- {n('Electronic, kind not stated')} have an electronic channel whose kind the sources do not state.",
            f"- For {n('Not stated')} the sources do not state the carrier. For {gk} of these the flow itself is from general knowledge.",
            "",
            "These numbers describe what the sources say. They are not a measurement of the systems."]
    return "\n".join(out) + "\n"

def emb_register(arg):
    names = {"spending": "spending", "revenue": "revenue and treasury", "inside": "inside one agency"}
    if arg not in names:
        raise SystemExit("unknown register directive " + arg)
    rows = [r for r in read_register(open(REGISTER_FILE, encoding="utf-8").read()) if r[1] == names[arg]]
    out = ["| No. | From | To | What passes | Kind | Carrier | Stage of use |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r[0]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} |")
    return "\n".join(out) + "\n"

def diagram_form(text, is_puml):
    if is_puml:
        return "PlantUML activity diagram with lanes" if re.search(r'^\|', text, flags=re.M) else "PlantUML component diagram"
    names = {"flowchart": "Mermaid flowchart", "sequenceDiagram": "Mermaid sequence diagram",
             "stateDiagram-v2": "Mermaid state diagram", "erDiagram": "Mermaid entity-relationship diagram",
             "gantt": "Mermaid Gantt chart", "timeline": "Mermaid timeline"}
    for line in text.split("\n"):
        w = line.strip().split(" ")[0]
        if w in names:
            return names[w]
    return "Mermaid"

def emb_index(rel):
    rows = ["| ID | Title | Form | Code file | Image |", "|---|---|---|---|---|"]
    items = []
    for p in glob.glob(os.path.join(MMD, "*.mmd")):
        text = open(p, encoding="utf-8").read()
        base = os.path.basename(p)[:-4]
        items.append((base, mermaid_title(text), diagram_form(text, False), f"{rel}diagrams/mermaid/{base}.mmd"))
    for p in glob.glob(os.path.join(PUML, "*.puml")):
        text = open(p, encoding="utf-8").read()
        base = os.path.basename(p)[:-5]
        m = re.search(r'^title\s+(.*)$', text, flags=re.M)
        items.append((base, m.group(1).strip() if m else base, diagram_form(text, True), f"{rel}diagrams/plantuml/{base}.puml"))
    for base, title, form, code in sorted(items, key=lambda x: diagram_sort_key(x[0].split("_")[0])):
        ident = base.split("_")[0]
        title = re.sub(r'^' + re.escape(ident) + r'\s+', '', title)
        rows.append(f"| {ident} | {title} | {form} | [`{os.path.basename(code)}`]({code}) | [image]({rel}rendered/{base}.png) |")
    return "\n".join(rows) + "\n"

def build(srcfile):
    relpath = os.path.relpath(srcfile, SRC)
    depth = relpath.count(os.sep)
    rel = "../" * depth
    out = []
    srctext = open(srcfile, encoding="utf-8").read()
    level = 1
    for line in srctext.split("\n"):
        h = re.match(r'^(#{1,6}) ', line)
        if h:
            level = len(h.group(1))
        m = re.match(r'^\{\{(mermaid|plantuml|steps|index|count|register):(.*)\}\}\s*$', line)
        if not m:
            out.append(line)
            continue
        kind, arg = m.group(1), m.group(2).strip()
        if kind == "mermaid":
            name = os.path.basename(find(MMD, arg, ".mmd"))
            EMBEDDED.add(name); EMBED_AT.setdefault(name, []).append(relpath.replace(os.sep, "/"))
            out.append(emb_mermaid(arg, rel, min(level + 1, 4)))
        elif kind == "plantuml":
            name = os.path.basename(find(PUML, arg, ".puml"))
            EMBEDDED.add(name); EMBED_AT.setdefault(name, []).append(relpath.replace(os.sep, "/"))
            out.append(emb_plantuml(arg, rel, min(level + 1, 4)))
        elif kind == "index":
            out.append(emb_index(rel))
        elif kind == "count":
            out.append(emb_count(arg, srctext))
        elif kind == "register":
            out.append(emb_register(arg))
        else:
            out.append(emb_steps(arg, rel))
    dest = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out).rstrip("\n") + "\n")
    return dest

def header_line(text, marker, key):
    for line in text.split("\n"):
        t = line.strip()
        if t.startswith(marker):
            body = t[len(marker):].strip()
            if body.startswith(key + ":"):
                return body[len(key) + 1:].strip()
    return ""

def write_csv_files():
    ref = os.path.join(OUT, "reference")
    # 1. index of all diagrams
    rows = []
    for p in sorted(glob.glob(os.path.join(MMD, "*.mmd")) + glob.glob(os.path.join(PUML, "*.puml")),
                    key=lambda p: diagram_sort_key(os.path.basename(p).split("_")[0])):
        text = open(p, encoding="utf-8").read()
        name = os.path.basename(p)
        puml = name.endswith(".puml")
        base = name.rsplit(".", 1)[0]
        ident = base.split("_")[0]
        if puml:
            m = re.search(r'^title\s+(.*)$', text, flags=re.M)
            title = m.group(1).strip() if m else base
        else:
            title = mermaid_title(text)
        title = re.sub(r'^' + re.escape(ident) + r'\s+', '', title)
        rows.append([ident, page_of_diagram(ident), "PlantUML" if puml else "Mermaid", diagram_form(text, puml), title,
                     header_line(text, "'" if puml else "%%", "QUESTION THIS DIAGRAM ANSWERS"),
                     ("diagrams/plantuml/" if puml else "diagrams/mermaid/") + name, "rendered/" + base + ".png",
                     "; ".join(EMBED_AT.get(name, []))])
    with open(os.path.join(ref, "diagram_index.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["id", "chapter", "notation", "form", "title", "question", "code_file", "image", "embedded_in"])
        w.writerows(rows)
    # 2. all numbered steps of the sequence diagrams that have a table of steps
    with open(os.path.join(ref, "steps_register.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["diagram_id", "diagram_file", "step", "who_acts", "towards_whom", "what_is_done_or_passed", "basis"])
        w.writerows(sorted(STEP_ROWS, key=lambda r: (diagram_sort_key(r[0]), r[2])))
    # 3. register of interfaces
    with open(os.path.join(ref, "interface_register.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["no", "side", "from", "to", "what_passes", "kind", "carrier", "stage_of_use", "check_of_both_sides", "basis"])
        w.writerows(IFACE_ROWS)
    print("csv files: diagram_index %d rows, steps_register %d rows, interface_register %d rows" % (len(rows), len(STEP_ROWS), len(IFACE_ROWS)))

def copy_diagrams():
    """Copy the diagram files to OUT/diagrams and remove copies whose source no longer exists."""
    for kind in ("mermaid", "plantuml"):
        src_dir = os.path.join(SRC, "diagrams", kind)
        dst_dir = os.path.join(OUT, "diagrams", kind)
        os.makedirs(dst_dir, exist_ok=True)
        names = set(os.listdir(src_dir))
        for name in sorted(names):
            shutil.copyfile(os.path.join(src_dir, name), os.path.join(dst_dir, name))
        for name in sorted(set(os.listdir(dst_dir)) - names):
            os.remove(os.path.join(dst_dir, name))
            print("removed old copy", os.path.join("diagrams", kind, name))

def remove_stale(built):
    """Remove Markdown files of OUT that no source file produced, and folders that are left empty."""
    keep = {os.path.abspath(p) for p in built}
    for p in sorted(glob.glob(os.path.join(OUT, "**", "*.md"), recursive=True)):
        if os.path.abspath(p) not in keep:
            os.remove(p)
            print("removed old file", os.path.relpath(p, OUT))
    for d, dirs, fs in sorted(os.walk(OUT, topdown=False)):
        if d != OUT and not os.listdir(d):
            os.rmdir(d)


def build_all():
    files = sorted(glob.glob(os.path.join(SRC, "**", "*.md"), recursive=True))
    built = []
    for f in files:
        d = build(f)
        built.append(d)
        print("built", os.path.relpath(d, OUT))
    remove_stale(built)
    copy_diagrams()
    allfiles = {os.path.basename(p) for p in glob.glob(os.path.join(MMD, "*.mmd"))} | {os.path.basename(p) for p in glob.glob(os.path.join(PUML, "*.puml"))}
    missing = sorted(allfiles - EMBEDDED)
    print("diagram files:", len(allfiles), "embedded in a Markdown file:", len(EMBEDDED))
    if missing:
        print("NOT EMBEDDED ANYWHERE:", missing)
    write_csv_files()

def compare(built, current):
    """Files of the built tree that are missing or different in the current tree (images are not built and not compared)."""
    diffs = []
    for d, _, fs in os.walk(built):
        for f in fs:
            p = os.path.join(d, f)
            rel = os.path.relpath(p, built)
            q = os.path.join(current, rel)
            if not os.path.exists(q) or not filecmp.cmp(p, q, shallow=False):
                diffs.append(rel)
    return sorted(diffs)

if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        current = OUT
        with tempfile.TemporaryDirectory() as tmp:
            OUT = tmp
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                build_all()
            diffs = compare(tmp, current)
        if diffs:
            print("docs/atlas is not up to date with src/. Run: python3 tools/build_atlas.py")
            for d in diffs:
                print("  differs:", d)
            sys.exit(1)
        print("docs/atlas is up to date with src/")
    else:
        build_all()
