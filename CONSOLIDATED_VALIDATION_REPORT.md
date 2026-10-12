# Consolidated Philippine PFM Atlas — validation report

Prepared 13 October 2026 from the two user-supplied GitHub Pages repositories and the 10 October strengthened source archive. Dates within the underlying research retain their own original coverage (current events as of 8 October 2026).

## Build and source preservation

- Current reference corpus: **77 Mermaid diagrams, 8 PlantUML diagrams, 19 process chapters, 7 references**, all inherited without changes to `src/` from `philippine-pfm-atlas (1).zip`.
- Educational walkthrough: **8 guided lessons**, retained as original guided text in `content/guides/`; only website link destinations are translated by the generator to current permanent URLs.
- Historical model archive: **93 Mermaid and 13 PlantUML sources** kept under `research_models/diagrams/`, including **20 Mermaid and 5 PlantUML** supplements not present by filename in the latest corpus. When IDs are reused, the new versions do not overwrite current sources; the whole old inventory is browsable under `docs/models/history.html`.
- Structured research archive: reference documents H–L and six CSV registers, published with explicit historical/analytical status.
- All `src/` and historical diagram/reference/register sources have SHA-256 entries in `SOURCE_SHA256.json`; the consolidation validator checks integrity.

## Tests executed

- `python tools/build_atlas.py --check`: built atlas up to date.
- `python tools/check_atlas.py`: **Problems found: 0**.
- `python tools/build_site.py`: generated static site without errors.
- `python tools/validate_site.py`: **Issues: 0**, **193 HTML pages**, **14,239 local links checked**, **8,052 anchor links**, **15,730 atlas text units found** and **1,686 source-code references linked**; 86 open-point entries and 69 interface catalogue entries remain indexed.
- `python tools/validate_consolidated.py`: **Issues: 0**; checks the eight lessons, 25 supplemental pages, 106 older source files, six registers and historical-revision segregation.
- `node --check tools/site/site.js` and `node --check docs/assets/site.js`: JavaScript syntax passed.
- ZIP archive integrity checked after packaging.

## Not tested / evidence limits

- **Visual browser test could not be completed**. Both file and localhost navigation in the available headless browser returned `ERR_BLOCKED_BY_ADMINISTRATOR`. Static HTML, assets, links and code were checked, but visual alignment and actual user interactions should be smoke-tested after publishing.
- The historical **25 additional diagram sources have no regenerated PNGs**; their pages explicitly label them source-only. The current 85 diagrams retain their existing PNG renders.
- Government legal, technical and production-interface claims in the underlying research have not been independently reverified in this consolidation. Existing references, limitations and uncertainties are preserved rather than silently replaced.
- This package has not been published to GitHub. It has no license grant; review copyright and permissions before public release.


## Light-default theme update (13 October 2026)

The website now defaults to light mode even on devices configured for dark appearance; dark mode is available only through the optional header control. The interface was smoke-tested in headless Chromium using the generated homepage HTML and the actual site CSS/JS. Details are in `THEME_UPDATE.md`.
