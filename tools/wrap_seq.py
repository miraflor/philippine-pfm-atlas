#!/usr/bin/env python3
"""Re-wrap the message texts of a Mermaid sequence diagram to a maximum line length.
Usage: wrap_seq.py FILE [WIDTH]. Only lines of the form  A->>B: text  are changed. A trailing <br/>#nbsp; is kept."""
import io, re, sys, textwrap
f = sys.argv[1]; width = int(sys.argv[2]) if len(sys.argv) > 2 else 48
out = []
for line in io.open(f, encoding="utf-8").read().split("\n"):
    m = re.match(r'^(\s*\w+(?:-->>|->>)\w+: )(.*)$', line)
    if not m:
        out.append(line); continue
    head, text = m.groups()
    tail = ""
    if text.endswith("<br/>#nbsp;"):
        text = text[:-len("<br/>#nbsp;")]; tail = "<br/>#nbsp;"
    text = re.sub(r'\s*<br/>\s*', ' ', text).strip()
    text = "<br/>".join(textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False))
    out.append(head + text + tail)
io.open(f, "w", encoding="utf-8", newline="\n").write("\n".join(out))
