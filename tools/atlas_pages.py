"""The chapters of the atlas, in reading order. Python standard library only.

The chapters follow the budget cycle in the illustration of DBM: four phases, each with a chapter that describes the
phase as a whole (P0, L0, E0, A0) and one chapter for each of its steps (P1 to P12, L1 to L5, E1 to E6, A1 to A9).
Two chapters describe what all phases share: the information systems (IS) and UACS (UACS).

A chapter file is src/chapters/<ID>_<name>.md. A diagram ID is the chapter ID, a hyphen and a letter, for example E4-a.
The diagrams of the big picture have the prefix BP.
"""
import re
from pathlib import Path

PHASES = [
    ('P', 'preparation', 'Preparation', 12),
    ('L', 'legislation', 'Legislation', 5),
    ('E', 'execution', 'Execution', 6),
    ('A', 'accountability', 'Accountability', 9),
]
SHARED = ['IS', 'UACS']
# Only these 32 IDs are numbered public activity chapters; P0/L0/E0/A0 are phase overviews.
STEP_ORDER = [p + str(i) for p, _, _, n in PHASES for i in range(1, n + 1)]
PHASE_OVERVIEWS = [p + '0' for p, _, _, _ in PHASES]
SUPPORT_PAGES = PHASE_OVERVIEWS + SHARED
ORDER = [p + str(i) for p, _, _, n in PHASES for i in range(0, n + 1)] + SHARED
PHASE_KEY = {p + str(i): key for p, key, _, n in PHASES for i in range(0, n + 1)}
PHASE_KEY.update({x: 'shared' for x in SHARED})
PHASE_NAME = {key: name for _, key, name, _ in PHASES}
PHASE_NAME['shared'] = 'Shared by all phases'
BIG_PICTURE = 'BP'
ID = re.compile(r'^(P1[0-2]|P\d|L[0-5]|E[0-6]|A\d|IS|UACS)$')
DIAGRAM_ID = re.compile(r'^(BP|P1[0-2]|P\d|L[0-5]|E[0-6]|A\d|IS|UACS)-([a-z])$')


def is_phase_intro(pid):
    return pid[0] in 'PLEA' and pid[1:] == '0'


def chapter_files(folder):
    """{ID: path} of the chapter files in folder; stops if the set of chapters is not the expected one."""
    found = {}
    for p in sorted(Path(folder).glob('*.md')):
        pid = p.name.split('_', 1)[0]
        if not ID.match(pid):
            raise SystemExit('unexpected chapter file: %s' % p)
        if pid in found:
            raise SystemExit('two files for chapter %s' % pid)
        found[pid] = p
    if set(found) != set(ORDER):
        raise SystemExit('chapters missing: %s; unexpected: %s'
                         % (sorted(set(ORDER) - set(found)), sorted(set(found) - set(ORDER))))
    return {pid: found[pid] for pid in ORDER}


def page_of_diagram(did):
    return did.rsplit('-', 1)[0]


def diagram_sort_key(did):
    page = page_of_diagram(did)
    return (-1 if page == BIG_PICTURE else ORDER.index(page), did.rsplit('-', 1)[1])
