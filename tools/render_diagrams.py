#!/usr/bin/env python3
"""Draw the diagrams of src/diagrams/ as PNG images in docs/atlas/rendered/.

Usage, from the root of the repository:

    python3 tools/render_diagrams.py              # draws every diagram whose image is missing or older than its code
    python3 tools/render_diagrams.py 07a 16b      # draws the diagrams whose file name starts with these IDs
    python3 tools/render_diagrams.py --all        # draws every diagram

After a fresh clone every file carries the date of the clone, so the comparison of dates says nothing. Name the IDs
of the diagrams that you changed, or use --all.

Programs that it needs:
    Mermaid      the command-line tool mmdc (npm package @mermaid-js/mermaid-cli). The images of the atlas were drawn
                 with version 11.16.0. If the browser that mmdc uses needs options, put them in a JSON file and set
                 the environment variable MMDC_PUPPETEER_CONFIG to its path.
    PlantUML     Java and plantuml.jar. Set the environment variable PLANTUML_JAR to the path of the jar file.
                 The images were drawn with PlantUML 1.2026.8. The component diagrams 16b and 16g also need Graphviz.
    Pillow       the Python package, to reduce each image to 256 colours. This makes the files smaller and does not
                 change what is shown. Without Pillow the images are kept as drawn.
"""
import glob, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "diagrams")
OUT = os.path.join(ROOT, "docs", "atlas", "rendered")

def reduce_colours(png):
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(png).convert("RGB")
    im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(png, optimize=True)

def draw_mermaid(path):
    base = os.path.basename(path)[:-4]
    out = os.path.join(OUT, base + ".png")
    cmd = ["mmdc", "-i", path, "-o", out, "-b", "white", "-s", "2", "-w", "2000"]
    if os.environ.get("MMDC_PUPPETEER_CONFIG"):
        cmd[1:1] = ["-p", os.environ["MMDC_PUPPETEER_CONFIG"]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(out), out, (r.stdout + r.stderr).strip()

def draw_plantuml(path):
    jar = os.environ.get("PLANTUML_JAR", "")
    if not jar or not os.path.exists(jar):
        return False, "", "set PLANTUML_JAR to the path of plantuml.jar"
    base = os.path.basename(path)[:-5]
    out = os.path.join(OUT, base + ".png")
    cmd = ["java", "-Djava.awt.headless=true", "-DPLANTUML_LIMIT_SIZE=16384", "-jar", jar, "-tpng", "-o", OUT, path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(out), out, (r.stdout + r.stderr).strip()

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    every = "--all" in sys.argv[1:]
    files = sorted(glob.glob(os.path.join(SRC, "mermaid", "*.mmd")) + glob.glob(os.path.join(SRC, "plantuml", "*.puml")))
    chosen = []
    for f in files:
        base = os.path.basename(f).rsplit(".", 1)[0]
        png = os.path.join(OUT, base + ".png")
        if args:
            if any(base.startswith(a) for a in args):
                chosen.append(f)
        elif every or not os.path.exists(png) or os.path.getmtime(png) < os.path.getmtime(f):
            chosen.append(f)
    if not chosen:
        print("Every image is newer than its code file. Nothing to draw. Use --all to draw every diagram.")
        return
    if any(f.endswith(".mmd") for f in chosen) and not shutil.which("mmdc"):
        sys.exit("The program mmdc was not found. Install it with: npm install -g @mermaid-js/mermaid-cli")
    os.makedirs(OUT, exist_ok=True)
    failed = 0
    for f in chosen:
        ok, out, msg = draw_mermaid(f) if f.endswith(".mmd") else draw_plantuml(f)
        name = os.path.basename(f)
        if ok:
            reduce_colours(out)
            print("drawn  ", name)
        else:
            failed += 1
            print("FAILED ", name, "-", msg.splitlines()[-1] if msg else "")
    print("%d drawn, %d failed" % (len(chosen) - failed, failed))
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
