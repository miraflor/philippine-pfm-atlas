#!/usr/bin/env python3
"""Check quotations in the atlas against the source texts.

Usage: python3 -I check_quotes.py ATLAS_SRC_DIR DIAGRAM_DIR SOURCE_TEXT_DIR [--all]

A quotation is text between straight double quotes. It is checked when the line
(or, in a diagram file, the comment line) also contains one of the codes of a
source whose full text is in SOURCE_TEXT_DIR. A quotation with "..." is split and
each part is checked. Result per quotation: exact (after whitespace
normalization), loose (letters and digits only, lower case), or NOT FOUND.
"""
import io, os, re, sys

CODES = ("GAM-V1", "GAM-V2", "GAM-V3", "IRR12009", "PD1445")
MINLEN = 12  # characters; shorter quotations are words or names


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("­", "")
    s = s.replace(" ", " ")
    s = re.sub(r"-[ \t]*\n\s*", "-", s)  # a hyphen at the end of a line: join the two parts
    return re.sub(r"\s+", " ", s).strip()


def loose(s):
    return re.sub(r"[^a-z0-9]+", "", norm(s).lower())


def read_corpus(root):
    parts = []
    for d, _, fs in os.walk(root):
        for f in sorted(fs):
            if f.endswith(".txt"):
                try:
                    parts.append(io.open(os.path.join(d, f), encoding="utf-8", errors="replace").read())
                except OSError:
                    pass
    text = "\n".join(parts)
    return norm(text), loose(text)


def quotes_in(line):
    return re.findall(r'"([^"]+)"', line)


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    src, dia, corp = sys.argv[1], sys.argv[2], sys.argv[3]
    show_all = "--all" in sys.argv
    exact_c, loose_c = read_corpus(corp)
    by_hand = set()
    hand_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quotes_by_hand.txt")
    if os.path.exists(hand_file):
        for ln in io.open(hand_file, encoding="utf-8"):
            if ln.strip() and not ln.startswith("#"):
                by_hand.add(loose(ln.split("|")[0]))
    n_hand = 0
    files = []
    for d, _, fs in os.walk(src):
        for f in sorted(fs):
            if f.endswith(".md"):
                files.append((os.path.join(d, f), "md"))
    for d, _, fs in os.walk(dia):
        for f in sorted(fs):
            if f.endswith((".mmd", ".puml")):
                files.append((os.path.join(d, f), "dia"))
    n_exact = n_loose = n_missing = 0
    for path, kind in sorted(files):
        for i, line in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
            if kind == "dia":
                st = line.strip()
                if not (st.startswith("%%") or st.startswith("'")):
                    continue
            if not any(c in line for c in CODES):
                continue
            for q in quotes_in(line):
                for part in re.split(r"\s*\.\.\.\s*", q):
                    part = part.strip().rstrip(".,;:")
                    if len(part) < MINLEN:
                        continue
                    if norm(part) in exact_c:
                        n_exact += 1
                        if show_all:
                            print("exact  %s:%d  %s" % (os.path.relpath(path), i, part[:80]))
                    elif loose(part) in loose_c:
                        n_loose += 1
                        print("loose  %s:%d  %s" % (os.path.relpath(path), i, part[:110]))
                    elif any(loose(part) in h or h in loose(part) for h in by_hand):
                        n_hand += 1
                        if show_all:
                            print("by hand  %s:%d  %s" % (os.path.relpath(path), i, part[:80]))
                    else:
                        n_missing += 1
                        print("NOT FOUND  %s:%d  %s" % (os.path.relpath(path), i, part[:160]))
    print("quotations checked: exact %d, loose %d, checked by hand %d, not found %d" % (n_exact, n_loose, n_hand, n_missing))


if __name__ == "__main__":
    main()
