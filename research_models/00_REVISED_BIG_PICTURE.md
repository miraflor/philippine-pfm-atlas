# Philippine PFM: strengthened big-picture reference architecture

**Edition 3 · 10 October 2026.** This document is the recommended conceptual entry point. It supersedes the *linear reading* of the earlier [full atlas big picture](00_BIG_PICTURE.md), which is retained with its original evidence and 81 rendered diagrams. This document is a reference model based on the atlas's cited official sources and the additional DBM roadmap/official policy review, **not** a proven nationwide systems integration design. A diagram line about information does not automatically establish a live API.

## 1. The entire PFM system is not one chain

PFM is the public sector's **system of fiscal decision rights, resources, obligations, operations, books, audit and results**. It includes revenue administration and borrowing as well as expenditure. Standard national government agency procurement is one important route, but payroll, sovereign debt, statutory transfers, refunds, pensions, public enterprises and local governments follow other lawful patterns.

**Start with these diagrams:** [00j — domains](diagrams/mermaid/00j_pfm_domains_not_a_pipeline.mmd), [00i — concurrent cycles](diagrams/mermaid/00i_concurrent_pfm_architecture.mmd), [00k — event data model](diagrams/mermaid/00k_event_authority_record_system_metagraph.mmd) and [00l — authority lanes](diagrams/plantuml/00l_four_parallel_authority_lanes.puml). The original [00a one-year overview](diagrams/mermaid/00a_pfm_cycle_overview.mmd) is useful for orientation but **not** a correct universal time ordering for the whole system.

## 2. The independent but interacting dimensions

| Dimension | Fundamental question | Canonical artifacts | Common owner/participant | Why it cannot be collapsed into another dimension |
|---|---|---|---|---|
| Fiscal policy and planning | What priorities, tax/borrowing assumptions and spending ceiling are appropriate? | Plans, fiscal frame, investment program | DEPDev, DBCC, DOF, DBM | Occurs across several budget years and precedes or revises program choices |
| Legal expenditure permission | Can this entity commit public resources for this purpose? | GAA or other legal basis, applicable allotment, statutory conditions | Congress, President, DBM, agency | Neither paper appropriation nor allotment is a transfer of cash |
| Procurement and service delivery | What is purchased/produced/received, and by whom? | Plan, award, contract, accepted delivery, measured performance | Agency, BAC, suppliers, delivery units | Some payments do not involve a contract; physical output is not cash |
| Cash and debt | Can and should the payment settle now? What finances it? | TSA/collections, debt instruments, cash forecast, NCA or other authority, bank settlement | BTr, DOF, DBM, BSP, banks | An approved claim need not have an immediately usable cash channel |
| Accrual and budgetary records | What amount, liability or asset should be recognized for a period? | Registers, journals, ledgers, reports, bank reconciliation | Agency budget and accounting units, BTr as applicable | Recognition can precede, coincide with or follow settlement depending on the event |
| Assurance and outcomes | Was spending lawful, reliable, effective, and corrected when necessary? | Control evidence, performance reports, COA findings, responses | Management, COA, Congress, public | Internal control is concurrent; audit and evaluation extend beyond payments |

A useful discipline is to assign every arrow one kind: **authority**, **temporal dependency**, **document**, **cash**, **information**, **classification**, **record reference**, or **verified integration**. If two distinct meanings are intended, draw two arrows. The original atlas section 5.1 discusses falsifiability of these claims.

## 3. Two independent permissions on ordinary agency spending

The **budget authority** track normally runs from appropriation/funding basis to applicable allotment and lawful obligations. The **cash/payment** track runs from receipts and financing to cash programming, an appropriate disbursement authority and a bank or other valid payment mechanism. They meet at a claim/payment check, but are not the same balance or authorization. Their legal conditions differ by agency, fund, fiscal period and spending route.

[05f — budget versus cash permissions](diagrams/mermaid/05f_independent_authorities_and_cash.mmd) and [11e — Treasury timing and settlement](diagrams/mermaid/11e_treasury_cash_synchronization.mmd). Original [00d — stylized contract payment](diagrams/mermaid/00d_four_chains.mmd) remains an illustration for a standard contractor claim; [07h — payment families](diagrams/mermaid/07h_disbursement_pattern_catalog.mmd) states why 00d's gates are not universal.

## 4. Financial events, records and UACS have different identities

An **event** is an occurrence (e.g., obligation, delivery, accrual, cash settlement) with its own date, actors and amount. A **record** is evidence or a posting for an event; a single event may create several records, and one document can refer to several financial occurrences. An **identifier** establishes which *instance* is being referred to. A **classification** (including UACS) establishes *which kind of spending or revenue* is being described. The same UACS segment can label hundreds of unrelated payments. A contract might support several obligations, and one obligation several vouchers and bank settlements.

[17e — identifier chain](diagrams/mermaid/17e_multi_identifier_lineage.mmd), [17f — code version crosswalk](diagrams/mermaid/17f_uacs_version_crosswalk.mmd), [17g — typed financial records](diagrams/plantuml/17g_financial_record_class_model.puml). The [event](reference/event_register.csv), [record](reference/record_type_register.csv), and [authority](reference/authority_register.csv) catalogues are **candidate schemas** only; they have not been verified against BTMS internals or individual agency accounting systems.

## 5. Accounting and controls are parallel, not post-payment paperwork

Cash receipts, asset delivery, recognition of a payable, accrual of interest, year-end adjusting entries and cash payments are distinct accounting events. Agency registers, financial books, Treasury data and bank confirmations should reconcile **with timing differences made explicit**. The end-of-year report or COA audit may occur later, but ongoing internal controls do not wait for payment.

[08e — independent recognition events](diagrams/mermaid/08e_accounting_recognition_events.mmd), [08f — reconciliations](diagrams/mermaid/08f_multilateral_reconciliation.mmd), [08g — concurrent accounting and assurance](diagrams/plantuml/08g_recording_and_audit_lanes.puml), [09d — audit and response](diagrams/mermaid/09d_controls_audit_and_responses.mmd). For detailed standards and forms the COA GAM and current COA circulars should be checked directly; some original atlas points remain only generally grounded.

## 6. The full range of money entering or leaving government

The [revenue chain](diagrams/mermaid/10e_revenue_administration_full_lifecycle.mmd) includes identification/assessment, payment or arrears, collections, bank settlement, Treasury and agency books, reconciliations, disputes and [refunds](diagrams/mermaid/10f_revenue_refunds_and_adjustments.mmd). The [payment catalogue](diagrams/mermaid/07h_disbursement_pattern_catalog.mmd) prevents an incorrect requirement for procurement/physical acceptance in payroll, debt service, lawful advances and transfers. National-to-local financial support does not absorb an LGU's separate budget law and internal approvals: see [14g](diagrams/mermaid/14g_lgu_two_coupled_cycles.mmd) and the [entity/fund variants](diagrams/mermaid/15g_entity_and_fund_specific_paths.mmd).

PFM also extends past a fiscal year through [guarantees, PPPs, debt, procurement and contingent liabilities](diagrams/mermaid/19c_fiscal_risk_multiyear.mmd), and past financial disbursement through [outputs, outcomes and performance evaluation](diagrams/mermaid/18c_performance_budget_learning.mmd).

## 7. The authorities are not the same as their software

An authority (DBM, BTr, COA, BIR, BOC, DEPDev, Congress, LGU, GOCC, agency head) exercises a legal role. Its documents may be submitted through one system, copied into another and exchanged manually. A bank holds evidence of settlement. An official system **plan** describes intention, not proof that a record actually moved from one application's database to another's.

**BTMS and IFMIS:** official DBM communications reported BTMS launched as interoperable core in 2024, pilot at seven agencies in 2025 and planned expansion to 155 agencies during 2026. The official 2026 PFM Roadmap Midterm Update schedules further data/enterprise integration, rollout and UACS revision in later years. Those facts do not justify declaring every named application linked through a production API.

- [16h — implementation evidence](diagrams/mermaid/16h_ifmis_deployment_confidence.mmd).
- [16i — interface failure and reconciliation](diagrams/mermaid/16i_interface_failure_and_reconciliation.mmd).
- [16j — records of authority and exchanges](diagrams/plantuml/16j_system_of_record_vs_interfaces.puml).
- [Interface evidence register](reference/interface_evidence_register.csv): all 54 historical claims retained but unverified mechanism/deployment left unknown rather than guessed.
- [Evidence rubric](reference/I_interface_evidence_and_status.md) documents what would justify an `API`, `live`, `manual re-entry`, or `missing` claim.

**DBM sources:** [2026 BTMS rollout statement](https://www.dbm.gov.ph/index.php/the-secretary-2/speeches/3800-the-2026-people-s-budget-a-catalyst-for-a-future-ready-philippine-economy); [PFM Roadmap 2024–2028 Midterm Update](https://www.dbm.gov.ph/wp-content/uploads/DBM%20Publications/PFM-Reforms/Midterm-Update/PHIL%20PFM%20Roadmap%20Midterm%20Update%20v2.pdf). Procurement [IRR official-version notice](https://www.gppb.gov.ph/public-advisory-no-09-2026/).

## 8. How to move between the diagrams and the institutional detail

The old atlas's [19 process chapters](processes/01_planning_and_investment_programming.md) through [19 fiscal risks](processes/19_fiscal_risks_ppp_and_contingent_liabilities.md) remain the main detailed narratives. **Edition 3 adds analytic alternative diagrams inside the relevant chapters**. Follow [Reference H (event ontology)](reference/H_reference_model_contract.md), [I (interface evidence)](reference/I_interface_evidence_and_status.md), [J (exception controls)](reference/J_controls_exceptions_and_temporal_model.md), [K (checks)](reference/K_validation_and_traceability.md), and [N (worked use cases)](reference/N_scenario_walkthroughs.md).

Read each drawing with the question: *What assertion is this arrow making, under which rules and for which fiscal period?* A system-to-system arrow must have deployment evidence and a known payload. An arrow from allotment to commitment is a legal dependency; it is not movement of funds. A UACS reference is classification; it is not proof of a shared record key.

## 9. Quality and remaining gaps

The [completeness and evidence matrix](reference/O_domain_completeness_and_evidence.md) openly ranks documentation versus system-interface confidence. The original detailed [open questions](reference/G_open_questions_and_known_gaps.md) still apply. Most important: interface specifications and transaction IDs, financial recognition entries and forms, operating payment exceptions, revenue administration back ends, and special legal entities. The new diagrams are **reference source files without new renders**, because the environment used to produce this edition did not have Mermaid/PlantUML renderers. Its consistency scripts test file relationships and model references, not factual or visual correctness.
