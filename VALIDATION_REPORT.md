# Validation report

Date of the checks: 29 October 2026. Facts on current events in the atlas are as of 8 October 2026.

## What the repository contains

- 38 chapters in `src/chapters/`: P0 to P12, L0 to L5, E0 to E6, A0 to A9, IS and UACS.
- 7 reference files (A to G), the big picture and the README of the atlas.
- 85 diagrams: 77 in Mermaid and 8 in PlantUML, each with a PNG image.
- 8 guided lessons in `content/guides/`.
- 8 research models (RM-1 to RM-8) with PNG images, 3 research references (H to J) and 6 registers in CSV form in `research_models/`.

## Checks that were run

| Command | Result |
|---|---|
| `python tools/build_atlas.py --check` | `docs/atlas/` agrees with `src/` |
| `python tools/check_atlas.py` | Problems found: 0 |
| `python tools/build_site.py` | 324 pages: 165 pages of content and 159 pages at addresses of an earlier version of the website, which send the reader to the new place |
| `python tools/validate_site.py` | Issues: 0. 18,929 local links, 9,177 links to anchors, 16,486 units of atlas text found word for word on their pages, 1,775 source codes linked to Reference F, 86 points of Reference G, 69 rows of the register of interfaces, 600 search entries |
| `python tools/validate_consolidated.py` | Issues: 0. 132 source files and 27 research files agree with `SOURCE_SHA256.json`; 8 lessons, 8 research models, 159 forwarding pages, none of them in the search |
| `python tools/check_budget_cycle_nav.py` | The story has 15 scenes; the step explorer has 32 steps and 32 panels; the months agree with the budgets served in 2026; each step links to its chapter; each chapter page shows its place in the cycle |
| `node --check` on `site.js`, `cycle-story.js` and `search.js` | No syntax error |

Every address of a web page of the earlier version of the website (193 pages) still opens a page: either the same page, or a page that sends the reader to the new place, with the part after `#` changed to the new section where the section moved.

The images were drawn with Mermaid 11.16.0 (`mmdc`) and PlantUML 1.2026.8.

## Browser test

The pages were opened in headless Chromium at a width of 1366 pixels and of 390 pixels (a phone), in light mode and in dark mode: the home page, the step explorer, the list of chapters, chapters P0, P2 and E4, the list of diagrams, the page of diagram E4-a, the research models, research model RM-1, the page on systems and UACS, and three pages at old addresses. No page showed a script error, except the request for the Mermaid library described below.

## What was not checked

- **Quotations and cited places against the source texts.** `tools/verify_counts.py` needs the five source documents as text files, and the repository does not contain them. Reference F, section 6, gives the result of the last run and the number of passages and citations that the tables of the step chapters repeat.
- **The interactive Mermaid view.** The test environment cannot reach jsDelivr, so the library did not load. The pages then showed the PNG image, as intended. The interactive view should be tried once on the published website.
- **The published website.** The checks used the files in `docs/`. They did not use GitHub Pages.
- **The facts of the atlas.** No legal, technical or interface statement was checked again against its source in this work.
- **Files at old addresses that are not web pages.** A Markdown file, a diagram code file or a PNG image cannot send the reader to a new place. 297 such addresses of the earlier version no longer exist, for example a link to a PNG image of a diagram under its earlier ID.
