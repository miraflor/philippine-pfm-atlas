# Light-default website update — validation and scope

Date: 13 October 2026. Applies to the consolidated Philippine PFM Atlas repository.

## Change

- **Default appearance: light**, independent of operating-system theme. No `prefers-color-scheme` dark rule remains.
- **Dark theme: opt-in** through a header button on every one of the 193 generated HTML pages. Button displays `Dark mode` when the page is light and `Light mode` when the page is dark.
- Browser choice is stored under `pfm-atlas-theme` in `localStorage` where permitted. A small synchronous head script applies that preference before the main stylesheet loads; it never automatically enables dark mode from operating-system settings.
- Without JavaScript, the site remains readable in light mode and the inactive theme button is hidden.
- Printed pages use the light palette regardless of the selected screen theme.
- The search page now also includes `site.js` to support the theme toggle; `search.js` continues to handle search.

## Tests

- Rebuilt 193 pages from the original consolidated source corpus.
- Checked that all 193 HTML pages include the toggle and early-preference script.
- Verified the site CSS has `:root[data-theme="dark"]` and no operating-system dark-mode rule.
- Ran `build_atlas.py --check`, `check_atlas.py`, `validate_site.py`, and `validate_consolidated.py`, each without errors.
- `node --check` passed for both source and generated `site.js`.
- Browser tested theme changes using the generated home page and inline copies of the actual site CSS/JS under headless Chromium. With simulated OS dark, it opened white (`rgb(255, 255, 255)`), switched on demand to dark (`rgb(21, 21, 21)`), and switched back to white. The control was visible at mobile width.
- Direct `file://` navigation remains blocked by the browser environment, so a fully hosted end-to-end visual test, and cross-page persistence in that hosted environment, were not completed here. The persistence code was inspected and is part of all pages.
- Current corpus and historical corpus remain protected by the existing SHA-256 manifest and checked by `validate_consolidated.py`.

## Install

Replace your previous consolidated repository files with those in this ZIP, commit and push. GitHub Pages continues to serve `main` / `/docs`; no change in Settings → Pages is needed. Browser users who previously accessed the old version may need to reload to receive the updated stylesheet and JavaScript.

## Files updated from the consolidated edition

- `tools/site/style.css`
- `tools/site/site.js`
- `tools/build_site.py`
- `README.md`
- Rebuilt generated `docs/` (all HTML pages, site CSS and JS)
- `THEME_UPDATE.md` (this file)

No source text, Mermaid, PlantUML, registered research models or diagram PNG was intentionally changed.
