# Philippine PFM Atlas

A map of public financial management (PFM) of the Philippine national government: the process from planning to audit, the authorities that participate in it, and their information systems. The atlas follows the budget cycle in the illustration of the Department of Budget and Management (DBM): four phases with 32 steps. It has 38 chapters, 7 reference files and 85 diagrams in Mermaid and PlantUML, and a website that presents them. Facts on current events are as of 8 October 2026.

This is an independent reference. It is not an official publication of the Philippine government, and it does not replace the laws, circulars and manuals that it cites.

**There is no license grant included.** Before publishing publicly, choose whether and how to license material you own and review third-party quotation, diagram, and source usage. Public GitHub viewing alone does not grant permission to reuse.

## Read the atlas

- **Website.** When GitHub Pages is enabled (see below), the website is at `https://USERNAME.github.io/REPOSITORY/`.
- **In the repository.** Start with [the big picture](docs/atlas/00_BIG_PICTURE.md). The [README of the atlas](docs/atlas/README.md) lists every chapter, reference file and diagram.
- **Sources and open points.** [Reference F](docs/atlas/reference/F_sources_and_verification.md) lists every source and how it was read. [Reference G](docs/atlas/reference/G_open_questions_and_known_gaps.md) lists what is not settled.

## How the chapters are arranged

The chapters follow the budget cycle. Each phase has a chapter that describes the phase as a whole, and each step of the phase has a chapter of its own. Two chapters describe what all phases share.

| Phase | Chapter of the phase | Chapters of the steps |
|---|---|---|
| Preparation | P0 | P1 to P12 |
| Legislation | L0 | L1 to L5 |
| Execution | E0 | E1 to E6 |
| Accountability | A0 | A1 to A9 |
| Shared by all phases | | IS (information systems), UACS (the Unified Accounts Code Structure) |

Section 1 of every step chapter is a short table: the phase and the indicative months of the step, its documents, its place on the four lines, the steps that send documents to it and receive documents from it, and links to the sections of the atlas that describe it. Some steps have a full description of their own (for example E4, the obligation and the payment). Other steps are short, and their table links to the exact sections where the atlas describes them (for example P2 to P4).

A diagram has the ID of its chapter, a hyphen and a letter: diagram E4-a is the first diagram of chapter E4. The diagrams of the big picture have the prefix BP.

## The website

| Page | Content |
|---|---|
| Budget cycle (the home page) | A scroll story of the 32 steps of the DBM illustration, a step explorer, and the map of the four lines with their meeting points |
| Guided lessons | Eight short lessons, each with a few diagrams |
| Big picture | The whole on a few pages |
| Chapters | The 38 chapters, in the order of the budget cycle, grouped by phase |
| References | Authorities, systems, documents and identifiers, laws, terms, sources, open points |
| Diagrams | One page for each diagram: the image, what it shows, its steps where it is a sequence, and its code. The list is grouped by chapter |
| Systems and UACS | A starting page for the information systems and the codes |
| Research models | Eight models that are not part of the chapters, each with a note on what it is for, and the research references and registers |
| Open points | Reference G, with a filter by status: open, partly settled, settled, sources differ |
| Search | Search in the text of all pages, including codes and form names such as `LDDAP-ADA` |

**Budget-cycle story and step explorer.** Below the opening of the home page, a scroll story follows the 32 steps of the DBM budget-cycle illustration: the loop, the same steps on a calendar (three budgets in one year), the Execution steps on the four lines with one payment and its three meeting points, and the documents that connect steps across the loop. A step explorer below it opens each step: its documents, its place on the four lines, the chapter of the step, the diagrams, the sources, and the steps that receive its documents. Each step has an address, for example `index.html#step-E4`.

The step data and the connecting sentences are in `tools/budget_cycle_story.py`. When the site is built, the script reads the documents, the place on the four lines and the items that the loop does not show from section 1 of each step chapter, so the explorer and the chapter always agree. It also checks every chapter section, diagram, source code and step that it names, checks that the steps that send and receive documents agree with the chapters, and checks that the months of each step agree with the budget it serves. The quotations are taken from section 2 of the big picture at build time, so they stay word for word. `THREE_BUDGETS_VIEW` in the same file chooses how the scene "Three budgets in one year" draws the steps: `'rows'` (each budget in full) or `'slice'` (one bar for each step, at its place in 2026). The drawing and the explorer run in `tools/site/cycle-story.js`. Without JavaScript the story reads as text and all 32 step panels are shown.

**Reading links between steps.** The story uses the calendar year 2026 to show budgets that run at the same time, while the links between steps describe general relationships within the life of one budget. These links are not evidence that the GAA for FY 2027 authorizes a release in FY 2026. The use of a performance review in a later budget proposal is a relationship between years, and the story names it as such. The scene that shows three budgets does not mean that every fiscal year has active steps on every date. The dates in the DBM illustration are indicative, not deadlines.

**The four lines.** The main finding of the atlas is about structure. PFM is not one flow of steps. Four lines of steps run at the same time: legal authority, the claim, cash, and records. A payment is possible only where the lines meet. The map of the four lines is on the home page below the budget-cycle story, and each point on the map links to its chapter.

All text of the website comes from the Markdown files of the atlas. The website adds navigation and links: each source code in square brackets, for example `[GAM-V1 Ch.6 s.12]`, links to its entry in Reference F, and each mention of a chapter, a diagram or a reference file links to it. Colour marks the four lines, with the colours of diagram BP-d: blue for legal authority, green for the claim, orange for cash, grey for records. The budget-cycle story of the home page also gives each of the four budget phases a colour that no line uses.

Every page can be read without JavaScript. The search, the two filters (open points, diagrams), the scroll story and the interactive diagrams need it. The website loads one program from another server: when a Mermaid diagram comes into view, the browser loads the Mermaid library (version 11.16.0) from jsDelivr to draw the diagram so that the reader can zoom, move and edit it. Everything else is in `docs/`. Without that library, or with the button "View original PNG", the reader sees the PNG image of the diagram.

## Appearance: light mode by default

Every visitor starts in **light mode**, whatever the appearance setting of the computer or phone. A **Dark mode** button in the site header changes the colours, and the browser keeps that choice for the next visit. The button then shows **Light mode** to change back. Printed pages use light colours.

The theme is in `tools/site/style.css`, `tools/site/site.js`, and the header template in `tools/build_site.py`. Rebuild with `python tools/build_site.py`; `docs/assets/` and all generated pages then show the change.

## Identifiers

Other texts can cite the atlas by these identifiers.

| Item | Identifier | Address on the website |
|---|---|---|
| Chapter | P0 to P12, L0 to L5, E0 to E6, A0 to A9, IS, UACS | `chapters/E4.html` |
| Section of a chapter | Its number | `chapters/E4.html#section-3` |
| Budget-cycle step | The ID of its chapter (P1 to P12, L1 to L5, E1 to E6, A1 to A9) | `index.html#step-E4` |
| Diagram | The ID of its chapter (or BP), a hyphen and a letter | `diagrams/E4-b.html` |
| Reference file | A letter, A to G | `reference/g.html` |
| Point of Reference G | Its number | `reference/g.html#point-60` |
| Row of the register of interfaces (Reference B, section 4) | Its number | `reference/b.html#flow-41` |
| Source | Its code in Reference F | `reference/f.html#source-gam-v1` |
| Research model | RM-1 to RM-8 | `models/RM-1.html` |

A section number changes when a section is added before it, so the addresses of sections are less stable than the addresses of chapters and diagrams. A new diagram receives the next free letter of its chapter. A removed item leaves its identifier unused.

`tools/forwarding.json` and `tools/research_forwarding.json` list addresses that an earlier version of the website used. For each of them the build writes a small page that sends the reader to the page that now holds the same content, so links in other documents keep working. These pages are not in the search, not in any list of the website, and are marked for search engines as pages not to index. Keep these two files when you change the website.

## How the repository is organized

| Folder | Content | Edited by hand? |
|---|---|---|
| `src/` | The sources of the atlas: the big picture, the README of the atlas, the chapters in `src/chapters/` (one file for each chapter, named by its ID), the reference files in `src/reference/`, and the diagram code in `src/diagrams/mermaid/` and `src/diagrams/plantuml/` | Yes. Every change of the atlas is made here |
| `docs/atlas/` | The atlas built from `src/`: Markdown files, copies of the diagram code, PNG images in `rendered/`, three CSV files in `reference/` | No. `tools/build_atlas.py` writes it, except the images, which `tools/render_diagrams.py` draws |
| `docs/` (the other files) | The website, built from `docs/atlas/`. GitHub Pages serves this folder | No. `tools/build_site.py` writes it |
| `content/guides/` | The eight guided lessons | Yes |
| `research_models/` | The eight research models, their images in `rendered/`, the research references H to J and six registers in CSV form. Its README says what each part is | Yes |
| `tools/` | Scripts that build and check the atlas and the website. `tools/atlas_pages.py` holds the list of chapters in the order of the budget cycle. `tools/site/` holds the style sheet, the scripts and the icon of the website | Yes |
| `deployment/` | An optional GitHub Actions workflow that is not active | Yes |
| `.github/` | A form for readers who report an error or give a source | Yes |

## Update the atlas

Run these commands from the root of the repository.

1. Edit the files in `src/`.
2. If the code of a diagram changed, draw its image again: `python tools/render_diagrams.py E4-a` (the ID of the diagram). For a research model add `--research`. The script says which programs it needs.
3. Build the atlas: `python tools/build_atlas.py`
4. Check the atlas: `python tools/check_atlas.py`. It must end with `Problems found: 0`.
5. Build and check the website: `python tools/build_site.py`, then `python tools/validate_site.py`, `python tools/validate_consolidated.py` and `python tools/check_budget_cycle_nav.py`. The validators must end with `Issues: 0`. These scripts need the packages in `requirements.txt` (`python -m pip install -r requirements.txt`, once).
6. If you changed a file in `src/`, `content/guides/` or `research_models/` on purpose, record the new state: `python tools/validate_consolidated.py --update`. This writes `SOURCE_SHA256.json`, which the validator uses to find changes that were not intended.
7. Commit the changes of `src/` and `docs/` together.

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

## Research models

The folder `research_models/` holds eight models, RM-1 to RM-8, that are not part of the chapters. A research model is a proposal, a method or a general model. It is not a description of Philippine PFM from a source, so it is kept apart from the chapters, and its page on the website says what it is for and why it is not in a chapter. The research references H to J and the six registers in CSV form are research material of the same kind. The register of events names, for each event, the chapter of the atlas that describes it.
