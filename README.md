# Philippine PFM Atlas — consolidated GitHub Pages edition

A map of public financial management (PFM) of the Philippine national government: the process from planning to audit, the authorities that participate in it, and their information systems. The atlas has 19 chapters, 7 reference files and 85 diagrams in Mermaid and PlantUML, and a website that presents them. Facts on current events are as of 8 October 2026.

This is an independent reference. It is not an official publication of the Philippine government, and it does not replace the laws, circulars and manuals that it cites.

## Three ways to use the site

- **Learn:** `docs/walkthrough.html` contains eight illustrated lessons adopted from the guided-walkthrough edition.
- **Reference:** the 19 current chapters and their 85 Mermaid/PlantUML diagrams retain short, stable URLs, citation anchors, and source-linked explanations.
- **Research models:** `docs/models/index.html` provides 25 additional source-only analytic diagrams and the H–L reference guides/registers from the strengthened 10 October edition. Those models are **not** silently promoted to current operational claims.

**There is no license grant included.** Before publishing publicly, choose whether and how to license material you own and review third-party quotation, diagram, and source usage. Public GitHub viewing alone does not grant permission to reuse.

## Read the atlas

- **Website.** When GitHub Pages is enabled (see below), the website is at `https://USERNAME.github.io/REPOSITORY/`.
- **In the repository.** Start with [the big picture](docs/atlas/00_BIG_PICTURE.md). The [README of the atlas](docs/atlas/README.md) lists every chapter, reference file and diagram.
- **Sources and open points.** [Reference F](docs/atlas/reference/F_sources_and_verification.md) lists every source and how it was read. [Reference G](docs/atlas/reference/G_open_questions_and_known_gaps.md) lists what is not settled.

## Appearance: light mode by default

Every visitor starts in **light mode**, regardless of the computer or phone's system appearance.
A **Dark mode** button in the site header is optional; selecting it stores that visitor's
choice locally in the browser. The header button then offers **Light mode** to switch back.
The site requires no external theme service, and printed pages use light colors.

The theme's editable source is `tools/site/style.css`, `tools/site/site.js`, and the
header template in `tools/build_site.py`. Rebuild with `python tools/build_site.py`;
`docs/assets/` and all generated pages will reflect the change.

## The website

The main finding of the atlas is about structure. PFM is not one flow of steps. Four lines of steps run at the same time: legal authority, the claim, cash, and records. A payment is possible only where the lines meet. The home page of the website therefore shows these four lines and the three points where they meet, and every step on it leads to its chapter.

| Page | Content |
|---|---|
| Map (the home page) | The four lines and their meeting points, as a drawing and in words, two cases, the five parts of PFM with their chapters, and the reference files |
| Big picture | The whole on a few pages |
| Chapters | The 19 chapters, each marked with the lines and parts to which it belongs |
| References | Authorities, systems, documents and identifiers, laws, terms, sources, open points |
| Diagrams | One page for each diagram: the image, what it shows, its steps where it is a sequence, and its code |
| Open points | Reference G, with a filter by status: open, partly settled, settled, sources differ |
| Search | Search in the text of all pages, including codes and form names such as `LDDAP-ADA` |

All text of the website comes from the Markdown files of the atlas. The website adds navigation and links: each source code in square brackets, for example `[GAM-V1 Ch.6 s.12]`, links to its entry in Reference F, and each mention of a chapter, a diagram or a reference file links to it. Colour marks only the four lines, with the colours of diagram 00d: blue for legal authority, green for the claim, orange for cash, grey for records. The website loads nothing from other servers. Every page can be read without JavaScript; only the search and the two filters (open points, diagrams) need it.

## Identifiers that do not change

Other texts can cite the atlas by these identifiers. After the website is public, an identifier is not changed and is not given to another item. A new item receives the next free number, and a removed item leaves its number unused.

| Item | Identifier | Address on the website |
|---|---|---|
| Chapter | Two digits, 01 to 19 | `chapters/07.html` |
| Reference file | A letter, A to G | `reference/g.html` |
| Point of Reference G | Its number | `reference/g.html#point-60` |
| Row of the register of interfaces (Reference B, section 4) | Its number | `reference/b.html#flow-41` |
| Source | Its code in Reference F | `reference/f.html#source-gam-v1` |
| Diagram | Its ID, for example 07b | `diagrams/07b.html` |

Sections also have addresses, for example `chapters/07.html#section-7-2`. A section number changes when a section is added before it, so these addresses are not fixed.

## How the repository is organized

| Folder | Content | Edited by hand? |
|---|---|---|
| `src/` | The sources of the atlas: Markdown files with build directives, and the diagram code in `src/diagrams/mermaid/` and `src/diagrams/plantuml/` | Yes. Every change of the atlas is made here |
| `docs/atlas/` | The atlas built from `src/`: Markdown files, copies of the diagram code, PNG images in `rendered/`, three CSV files in `reference/` | No. `tools/build_atlas.py` writes it |
| `docs/` (the other files) | The website, built from `docs/atlas/`. GitHub Pages serves this folder | No. `tools/build_site.py` writes it |
| `tools/` | Scripts that build and check the atlas and the website, including `build_extensions.py` and `validate_consolidated.py`. `tools/site/` holds the style sheet, the scripts and the icon of the website | Yes |
| `deployment/` | An optional GitHub Actions workflow that is not active | Yes |
| `.github/` | A form for readers who report an error or give a source | Yes |

## Update the atlas

Run these commands from the root of the repository.

1. Edit the files in `src/`.
2. If the code of a diagram changed, draw its image again: `python tools/render_diagrams.py 07a` (the ID of the diagram). The script says which programs it needs.
3. Build the atlas: `python tools/build_atlas.py`
4. Check the atlas: `python tools/check_atlas.py`. It must end with `Problems found: 0`.
5. Build and check the website: `python tools/build_site.py`, then `python tools/validate_site.py` and `python tools/validate_consolidated.py`. The second command must end with `Issues: 0`. These two scripts need the packages in `requirements.txt` (`python -m pip install -r requirements.txt`, once).
6. Commit the changes of `src/` and `docs/` together.

`python tools/build_atlas.py --check` tells whether `docs/atlas/` agrees with `src/`, without changing a file.

`tools/validate_site.py` checks more than links. It finds every paragraph, list item, heading and table cell of the atlas on its web page, word for word. It checks that every source code in square brackets is a link to Reference F, that every link to an anchor finds its anchor, and that the statuses of the points of Reference G agree with the numbers that Reference G states.

Two more checks need the five source documents of the atlas (the three volumes of the Government Accounting Manual, the Government Auditing Code and the Implementing Rules of RA 12009) converted to plain text in one folder. The repository does not contain them. With that folder, `python tools/verify_counts.py FOLDER` compares every quotation and every cited section with the texts, and tests that the results agree with Reference F, section 6.

## Publish the website on GitHub Pages

1. Create an empty repository on GitHub. Do not let GitHub add a README, a license or a `.gitignore`.
2. Push the content of this folder to the branch `main`:

   ```
   git init
   git add .
   git commit -m "Philippine PFM Atlas"
   git branch -M main
   git remote add origin https://github.com/USERNAME/REPOSITORY.git
   git push -u origin main
   ```

3. In the repository on GitHub, open **Settings**, then **Pages**. Under **Build and deployment**, choose **Deploy from a branch**, the branch **main** and the folder **/docs**, and save.
4. After a few minutes the website is at `https://USERNAME.github.io/REPOSITORY/`.

The file `docs/.nojekyll` must be in the repository. It tells GitHub Pages to serve the files as they are. A public repository is needed for GitHub Pages on a free GitHub account.

[PUBLISHING.md](PUBLISHING.md) gives more detail, and the optional workflow that builds and publishes the website with GitHub Actions.

## Programs that the scripts need

| Task | Programs |
|---|---|
| Build and check the atlas | Python 3 (the scripts were run with Python 3.13). No other package |
| Build and check the website | Python 3 and the packages mistune and beautifulsoup4 (`requirements.txt`) |
| Draw the images | Node.js with `@mermaid-js/mermaid-cli` (the images were drawn with version 11.16.0), Java with PlantUML (version 1.2026.8) and Graphviz, and the Python package Pillow |

## Attribution and update policy

The current 12 October atlas is the only source for the main procedural chapters. Earlier diagrams are preserved under a separate `research_models/` namespace with their original code IDs retained in filenames and distinct `model-` page URLs. Where they disagree with current procedures, treat them as historical exploratory models, not corrections to the 12 October edition. New/edited charts need refreshed PNGs for the **main** diagram gallery; the 25 supplementary diagrams remain explicitly source-only until independently rendered and reviewed.

The site is self-contained: no CDN, no remote data calls, no database or GitHub Actions required for browsing. Build commands require Python and the packages in `requirements.txt`.
