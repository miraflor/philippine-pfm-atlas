# Reference H — PFM system model: typed events, records, authorities, jurisdictions

**Status:** proposed reference ontology; not enacted law, not BTMS database schema. This document strengthens the descriptive atlas without claiming the public PFM applications share one internal implementation.

## 1. Ontological layers

1. **Jurisdiction and financial entity:** NGA, attached operating unit, LGU, GOCC, GFI, BARMM and special statutory funds can have different spending powers and reporting boundaries. An entity is not an application account.
2. **Authority:** a law, appropriation item, allotment instrument, signed approval or delegated competence. Authorities have author, recipient, amount/purpose limits and validity intervals; authority is not cash.
3. **Event:** a dated occurrence or state change (assessment, appropriation enactment, allotment, obligation, delivery, payment, journal posting, reconciliation, audit notice). Events may be planned, recorded, reversed or corrected. Event records must carry IDs and provenance.
4. **Record:** one identifiable, versioned document, register line, contract, transaction or journal entry. A record's issuer differs from the software displaying a copy.
5. **Classification:** UACS (with funding, organization, location, program/PAP, object dimensions as applicable), COA accounts and other code systems. Classification codes are *types*, not unique document or event identifiers.
6. **Financial or physical state:** allotment balance, unpaid obligations, payables, bank cash, asset ownership, delivered output or claim status. These are not automatically equal amounts.
7. **System and interface:** named application and deployment scope, data owner, exchange method, evidence, and reconciliation; a system in a slide is not evidence of an implemented integration.

## 2. Explicit predicates and relationships

`AUTHORIZES(authority,event,rule_version)`; `EVIDENCES(record,event)`; `REFERENCES(record_1,record_2,role)`; `CLASSIFIES(record,code,version,valid_at)`; `RECORDED_IN(record,system,environment)`; `SENT_VIA(exchange,source_system,target_system,mode)`; `CHANGES(event,balance,amount,as_of)`; `CONSTRains(rule,event,period)`; `SUPERSEDES(new_record,old_record)`; `RECONCILES(record_a,record_b,as_of)`.

References are explicitly many-to-many. One contract can have several obligations, releases and payments; one UACS class can cover many unrelated payments. Shared coding never proves shared identity. An interface may preserve one ID, map it to another, or lose it, and this difference must be recorded.

## 3. Time is mandatory

Store at least `event_date`, `posting_date`, `fiscal_year`, `authority_valid_from/to`, `code_version/effective_date`, and `evidence_checked_at`. A document dated 2025 might pay under 2026 rules; the transaction must be assessed under the appropriate law and fund validity. Cross-year comparison needs a documented code crosswalk, not silent recoding.

## 4. Modeling conventions

- `observed`: authoritative primary documents or operational evidence examined.
- `reported`: credible publication says practice exists; no independently tested interface.
- `inferred`: model joins established facts but technical or legal conditionality remains unverified.
- `target`: planned architecture, **never** a production assertion.
- `unknown`: absence of evidence; **never** assert an integration does not exist.

**Research models:** [RM-1](../diagrams/mermaid/RM-1_event_authority_record_system_metagraph.mmd), [RM-8](../diagrams/plantuml/RM-8_financial_record_class_model.puml).

**Primary research anchors:** [DBM PFM Roadmap Midterm Update](https://www.dbm.gov.ph/wp-content/uploads/DBM%20Publications/PFM-Reforms/Midterm-Update/PHIL%20PFM%20Roadmap%20Midterm%20Update%20v2.pdf); COA Government Accounting Manual; FY 2026 [NBC 599](https://www.dbm.gov.ph/index.php/dbm-issuances/national-budget-circulars?catid=428&id=3824%3Anational-budget-circular-no-599&view=article). The ontology itself is this atlas's proposed analytic structure.
