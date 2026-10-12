#!/usr/bin/env python3
"""Run the two source checks on the sources in src/ and compare their results with the numbers written in
Reference F, section 6 ("Result of the last run, on DATE: ...").

Usage, from the root of the repository:

    python3 tools/verify_counts.py FOLDER_WITH_THE_SOURCE_TEXTS

The folder must contain the five source documents converted to plain text (see tools/check_refs.py for the names).
The repository does not contain them. Without the folder the script stops and says so.
Exit code 1 when a number in the text differs from the result of the run.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

def main():
    if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
        print("Give the folder with the source texts as the first argument. Nothing was checked.")
        sys.exit(2)
    args = [os.path.join(ROOT, "src"), os.path.join(ROOT, "src", "diagrams"), os.path.abspath(sys.argv[1])]
    q = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "check_quotes.py")] + args, capture_output=True, text=True).stdout.strip().split("\n")[-1]
    r = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "check_refs.py")] + args, capture_output=True, text=True).stdout.strip().split("\n")[-1]
    print(q)
    print(r)
    mq = re.search(r"exact (\d+), loose (\d+), checked by hand (\d+), not found (\d+)", q)
    mr = re.search(r"found (\d+), not found (\d+)", r)
    if not mq or not mr:
        print("A check did not end with its summary line")
        sys.exit(1)
    with open(os.path.join(ROOT, "src", "reference", "F_sources_and_verification.md"), encoding="utf-8") as fh:
        f = fh.read()
    ok = True
    t = re.search(r"Result of the last run, on [^:]+: (\d+) passages were found word for word\. None was found only by a looser comparison, and none was missing\. (\d+) more passages", f)
    if not t or (t.group(1), t.group(2)) != (mq.group(1), mq.group(3)) or mq.group(2) != "0" or mq.group(4) != "0":
        print("QUOTATIONS: the text of Reference F does not agree with the run")
        ok = False
    t2 = re.search(r"Result of the last run, on [^:]+: ([\d,]+) citations of a place were tested, and every place exists", f)
    if not t2 or t2.group(1).replace(",", "") != mr.group(1) or mr.group(2) != "0":
        print("PLACES: the text of Reference F does not agree with the run")
        ok = False
    print("Reference F agrees with the runs" if ok else "DIFFERENCE")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
