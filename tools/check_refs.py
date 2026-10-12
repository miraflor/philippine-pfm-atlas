#!/usr/bin/env python3
"""Check that every section, chapter, annex or appendix that the atlas cites from the five
sources held as text exists in those texts.

Usage: python3 -I check_refs.py ATLAS_SRC_DIR DIAGRAM_DIR SOURCE_TEXT_DIR

SOURCE_TEXT_DIR must contain these conversions to plain text (made here with "pdftotext -layout"):
  gam_v1.txt           Government Accounting Manual, Volume I
  irr12009.txt         Implementing Rules and Regulations of RA 12009
  pd1445.txt           Presidential Decree No. 1445
  gam_v2_forms_txt/    one file for each form of Volume II, named "Appendix 32 - DV.txt" and so on

It checks the place only: that Volume I, chapter 6 has a section 63, that the Rules have a
section 71.2.8, that the Code has a section 115, that Volume II has an Appendix 32. It does not
check that the statement beside the citation is what the section says.
"""
import io, os, re, sys

def gam_v1_sections(path):
    lines = io.open(path, encoding="utf-8", errors="replace").read().split("\n")
    start = {}
    end22 = None
    for i, l in enumerate(lines):
        m = re.match(r"^[\s\f]*Chapter (\d+)[\s\f]*$", l)
        if m and int(m.group(1)) not in start:
            start[int(m.group(1))] = i
        if end22 is None and re.match(r"^[\s\f]*Annex A[\s\f]*$", l) and 22 in start:
            end22 = i
    out = {}
    chapters = sorted(start)
    for n, ch in enumerate(chapters):
        a = start[ch]
        b = start[chapters[n + 1]] if n + 1 < len(chapters) else (end22 or len(lines))
        secs = set()
        for l in lines[a:b]:
            m = re.match(r"\s*Sec\. (\d+)\.", l)
            if m:
                secs.add(int(m.group(1)))
        out[ch] = secs
    annexes = set(re.findall(r"(?m)^[\s\f]*Annex ([A-Q])[\s\f]*$", "\n".join(lines)))
    return out, annexes


def irr_sections(path):
    t = io.open(path, encoding="utf-8", errors="replace").read()
    main = set(int(x) for x in re.findall(r"(?m)^\s*Section (\d+)\.", t))
    sub = set(re.findall(r"(?m)^\s*(\d+(?:\.\d+){1,3})\s", t))
    return main, sub


def pd_sections(path):
    t = io.open(path, encoding="utf-8", errors="replace").read()
    return set(int(x) for x in re.findall(r"(?mi)^\s*Section (\d+)\.", t))


def appendices(folder):
    out = set()
    for f in os.listdir(folder):
        m = re.match(r"Appendix (\d+[A-D]?)\b", f)
        if m:
            out.add(m.group(1))
    return out


def expand(tok):
    """'s.12' -> ['12']; 'ss.14-39' -> ['14', ..., '39']; 's.71.2.8' -> ['71.2.8']; 'ss.48-50' -> 48..50."""
    m = re.match(r"ss?\.(\d+(?:\.\d+)*)(?:-(\d+(?:\.\d+)*))?(?:\([0-9a-z]+\))*$", tok)
    if not m:
        return []
    a, b = m.group(1), m.group(2)
    if b and "." not in a and "." not in b:
        return [str(i) for i in range(int(a), int(b) + 1)]
    return [a] + ([b] if b else [])


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    src, dia, corp = sys.argv[1:4]
    v1, annexes = gam_v1_sections(os.path.join(corp, "gam_v1.txt"))
    irr_main, irr_sub = irr_sections(os.path.join(corp, "irr12009.txt"))
    pd = pd_sections(os.path.join(corp, "pd1445.txt"))
    apps = appendices(os.path.join(corp, "gam_v2_forms_txt"))
    files = []
    for d, _, fs in os.walk(src):
        files += [os.path.join(d, f) for f in sorted(fs) if f.endswith(".md")]
    for d, _, fs in os.walk(dia):
        files += [os.path.join(d, f) for f in sorted(fs) if f.endswith((".mmd", ".puml"))]
    tok_re = re.compile(r"(GAM-V1|GAM-V2|GAM-V3|IRR12009|PD1445)|(Ch\.\d+)|(Annex(?:es)? [A-Q]\b(?:(?:,| and) [A-Q]\b)*)|(App\.\d+[A-D]?)|(ss?\.\d+(?:\.\d+)*(?:-\d+(?:\.\d+)*)?(?:\([0-9a-z]+\))*)|([A-Z][A-Za-z]*\d[A-Za-z0-9]*(?:-[A-Za-z0-9]+)*|[A-Z]{2,}[A-Za-z0-9]*(?:-[A-Z0-9][A-Za-z0-9]*)+)")
    n_ok = n_bad = 0
    for path in sorted(files):
        for i, line in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
            if not any(c in line for c in ("GAM-V1", "GAM-V2", "GAM-V3", "IRR12009", "PD1445")):
                continue
            # look only at citation contexts: text in square brackets, and table cells
            parts = re.findall(r"\[([^\]\[]*)\]", line)
            if line.lstrip().startswith("|"):
                parts += [c for c in line.split("|")]
            seen = set()
            for part in parts:
                cur = None; ch = None
                for m in tok_re.finditer(part):
                    code, chap, annex, app, sec, other = m.groups()
                    if code:
                        cur, ch = code, None
                    elif other:
                        cur, ch = None, None
                    elif cur is None:
                        continue
                    elif chap and cur in ("GAM-V1", "GAM-V3"):
                        ch = int(chap[3:])
                        ok = (ch in v1) if cur == "GAM-V1" else (1 <= ch <= 3)
                        key = (cur, chap)
                        if key not in seen:
                            seen.add(key)
                            if ok: n_ok += 1
                            else:
                                n_bad += 1; print("NO SUCH CHAPTER  %s:%d  %s %s" % (os.path.relpath(path), i, cur, chap))
                    elif annex and cur == "GAM-V1":
                        for a in re.findall(r"\b([A-Q])\b", annex.split(" ", 1)[1]):
                            key = (cur, "Annex", a)
                            if key in seen: continue
                            seen.add(key)
                            if a in annexes: n_ok += 1
                            else:
                                n_bad += 1; print("NO SUCH ANNEX  %s:%d  %s Annex %s" % (os.path.relpath(path), i, cur, a))
                    elif app and cur == "GAM-V2":
                        a = app[4:]
                        key = (cur, app)
                        if key in seen: continue
                        seen.add(key)
                        if a in apps: n_ok += 1
                        else:
                            n_bad += 1; print("NO SUCH APPENDIX  %s:%d  %s %s" % (os.path.relpath(path), i, cur, app))
                    elif sec:
                        for s in expand(sec):
                            key = (cur, ch, s)
                            if key in seen: continue
                            seen.add(key)
                            if cur == "GAM-V1":
                                ok = ch is not None and "." not in s and int(s) in v1.get(ch, ())
                            elif cur == "IRR12009":
                                ok = (int(s) in irr_main) if "." not in s else (s in irr_sub or int(s.split(".")[0]) in irr_main and s in irr_sub)
                            elif cur == "PD1445":
                                ok = "." not in s and int(s) in pd
                            else:
                                continue
                            if ok: n_ok += 1
                            else:
                                n_bad += 1; print("NO SUCH SECTION  %s:%d  %s %s %s" % (os.path.relpath(path), i, cur, ("Ch.%d" % ch) if ch else "", sec))
    print("places checked: found %d, not found %d" % (n_ok, n_bad))


if __name__ == "__main__":
    main()
