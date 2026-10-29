# Reference L — What changed in strengthened edition 3

**Prepared:** 10 October 2026, building on the user's 8–9 October source atlas. Original 19 chapters, existing 81 editable diagram source files, rendered images, 3 CSV registers and research bibliography are preserved.

## Material improvements

- **Concurrent architecture:** 00i and 00l correct the visual implication that all accounting and internal/external control starts after payment.
- **Scope of PFM:** 00j distinguishes revenue assessment, arrears, debt, cash, risks and institutional variants from ordinary purchasing.
- **Event data model:** 00k, 17e, 17f and 17g define event/record identity, financial balance, versioned classification, and multi-document linkage.
- **Separate permissions:** 05f shows allotment/commitment versus cash/payment authority and the need to inspect alternatives.
- **Payment controls:** 07h, 07i and 07j separate contractor acceptance, progress, lawful advances, payroll, transfers, debt service and refunds.
- **Accounting and audit:** 08e, 08f, 08g, 09d model contemporaneous accrual events, 4-way reconciliations and ongoing assurance.
- **Coverage:** 10e/10f revenue assessment and refund flows; 11e cash forecasting; 14g LGU cycles; 15g entity/fund variants; 18c performance learning; 19c multi-year risks.
- **Operational truthfulness:** 16h, 16i, 16j and interface evidence register split deployment stage, mechanism, data ownership and evidence confidence.
- **Registers:** authority, event, record, rule and interface-evidence CSVs, separate from the original source registers.

## Corrections and what is *not* claimed

1. Do not interpret 00a or 00f as an exact actual time order across all actors. Their explanatory diagrams are retained, but the new diagrams are authoritative as **reference modeling views**, not as legislation.
2. Do not interpret 00d's three joins as a universal payment rule.
3. Do not interpret all named PFM software as part of a deployed IFMIS or assert a direct PIPOL/OSBPS link is absent without operational evidence.
4. Do not interpret a shared UACS code as a universally unique key.
5. New diagrams and ontological entities are **conceptual**. They have not been validated against real BTr, DBM, BIR, BOC, agency, COA or bank production data and interface specifications.
6. This edition **does not assert that it has read every law and administrative manual in full**. The old atlas's open-questions register remains applicable. New references contain directly linked official statements, not invented field-level mappings.

## Highest priority unresolved questions

- Does each asserted information exchange use API, batch, file, manual re-entry or another path for a *particular environment and agency*?
- What is the precise field-level mapping among planning IDs, UACS PAPs, obligations, vouchers, bank settlement, financial journals, and assets?
- How do deferred appropriations, multi-year funds, grant conditions and direct lender payments affect balances across fiscal years?
- Which COA/BTr bank-reconciliation routines and audit evidence are operationally performed in each spending unit?
- How do BARMM, GFIs, pension funds, special accounts and corporate transfers differ from the NGA baseline?
- What are the exact controls for each payment exception under the applicable law and FY-specific circulars?

See the original [open questions](G_open_questions_and_known_gaps.md) and the [new conformance rules](K_validation_and_traceability.md).
