# Reference K — Source assurance, conformance rules and reproducibility

## 1. Traceability

Original chapters and diagrams remain unchanged except explicit analytical navigation notes and additions. Version 3 additions are indexed in `reference/diagram_index.csv` and detailed in `reference/L_change_log_and_remaining_limits.md`. New diagrams have editable source code but intentionally **no PNG render**; original 81 PNGs remain as legacy visual snapshots and are not claimed to have been updated.

## 2. Non-equivalent assertions

- `record has UACS` is not `record belongs to a known contract`;
- `system is deployed` is not `its integration with a second system is deployed`;
- `appropriation` is not `allotment`, which is not `obligation`, `payable` or `cash`;
- `source says planned` is not `production evidence`;
- `COA audit may occur` is not `COA approved this individual payment in advance`;
- `classified amount reconciles` is not `each micro-record matches`.

## 3. Automated checks

Run `python tools/check_atlas.py` (the original checker) and `python tools/check_strengthened_atlas.py` (new source / metadata / register checks). The latter checks uniqueness and file presence, cross-references in new docs, code fences / diagram starts, allowed source values, event/authority/control/record references and duplicate IDs. It does **not** certify Mermaid rendering, PlantUML rendering, legal correctness, deployments or actual transaction tests.

## 4. Evidence and correction log

A correction requires `statement_id`, file+line or diagram ID, previous wording, replacement, source URL/title, date, reason, status (`confirmed` / `inferred` / `open`), and reviewer. If a source has changed since 8 October 2026, record its release/effective date rather than retroactively rewriting FY 2026 rules. The atlas is a mapping exercise, not legal advice or a substitute for current agency manuals.

## 5. Research priorities

1. Cross-check payment and accounting entries against actual COA GAM Volumes I/II and current implementing circulars.
2. Obtain primary production evidence for actual BTMS and banking interfaces.
3. Validate UACS mapping and crosswalks at record-level, not only aggregate code lists.
4. Deepen BIR, BOC, BTr revenue and debt transaction details and reconciliation.
5. Model LGU, GOCC, GFI, BARMM and special account variants with the same rigor as central NGAs.
