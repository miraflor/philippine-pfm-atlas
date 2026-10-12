# Philippine PFM Atlas

A set of diagrams and descriptions that map public financial management (PFM) of the Philippine national government: the process, the authorities that participate in it, and their information systems. Facts are as of 8 October 2026. The last checks of sources were made in the night from 8 to 9 October 2026, Philippine time.

This is the strengthened third edition (10 October 2026), preserving the second edition as a documented baseline. Original charts remain as teaching/legacy views; see **New analytical diagrams** and **Critical limitations** below. The original second edition It adds two chapters, 14 diagrams and several reference tables to the first version of 8 October 2026. [Reference F, section 6](reference/F_sources_and_verification.md), lists every change and the reason for it.

## 1. Where to start

1. **Start with [00_REVISED_BIG_PICTURE.md](00_REVISED_BIG_PICTURE.md)** (edition 3 conceptual map). Then read [00_BIG_PICTURE.md](00_BIG_PICTURE.md) for the original detailed overview and its eight diagrams.
2. Open the chapter of the part you need (section 4 below). Each chapter explains one process and contains its diagrams.
3. Use the reference files for the authorities, the information systems, the documents, the laws, the terms, the sources, and the open questions (section 5).
4. Before a diagram is reused for another purpose, read section 5.1 of the big picture. It names the eight kinds of arrows of this atlas and, for each kind, an observation that would show an arrow to be wrong.

## 2. What the package contains

The package preserves the original 73 Mermaid and 8 PlantUML views and adds **20 Mermaid and 5 PlantUML reference diagrams**, for **93 Mermaid + 13 PlantUML diagrams (106 source files)**. Existing 81 PNG renders are retained as a *legacy visual snapshot*. New diagrams are editable source files only, not pre-rendered. The original checker is retained, with a strengthened checker under `tools/check_strengthened_atlas.py`. The 19 detailed process chapters are preserved and updated with links to expanded views.

The new `Reference H through L guides and the additional CSV registers make the models consistent across process, actor, record, rule, and systems views.


## New analytical diagrams (edition 3)

These supersede older linear figures as the preferred **analytical** views; original figures remain useful introductions.

| ID | View | Editable source |
|---|---|---|
| 00i | PFM concurrent operating architecture | [Mermaid source](diagrams/mermaid/00i_concurrent_pfm_architecture.mmd) |
| 00j | PFM domains and non-procurement exceptions | [Mermaid source](diagrams/mermaid/00j_pfm_domains_not_a_pipeline.mmd) |
| 00k | Shared reference model of a financial event | [Mermaid source](diagrams/mermaid/00k_event_authority_record_system_metagraph.mmd) |
| 05f | Budget authority and cash authority have different predicates | [Mermaid source](diagrams/mermaid/05f_independent_authorities_and_cash.mmd) |
| 07h | Different disbursement patterns have different gates | [Mermaid source](diagrams/mermaid/07h_disbursement_pattern_catalog.mmd) |
| 07i | Standard contractor payment with explicit branch cases | [Mermaid source](diagrams/mermaid/07i_standard_contract_payment_controls.mmd) |
| 08e | Accounting recognition is event-driven, not post-payment | [Mermaid source](diagrams/mermaid/08e_accounting_recognition_events.mmd) |
| 08f | Reconciliation across budget, accounting, bank and physical evidence | [Mermaid source](diagrams/mermaid/08f_multilateral_reconciliation.mmd) |
| 09d | Three lines of assurance and feedback | [Mermaid source](diagrams/mermaid/09d_controls_audit_and_responses.mmd) |
| 10e | Revenue administration beyond collecting tax | [Mermaid source](diagrams/mermaid/10e_revenue_administration_full_lifecycle.mmd) |
| 10f | Tax refund, overpayment and payment corrections | [Mermaid source](diagrams/mermaid/10f_revenue_refunds_and_adjustments.mmd) |
| 11e | Treasury planning, liquidity and settlement | [Mermaid source](diagrams/mermaid/11e_treasury_cash_synchronization.mmd) |
| 14g | LGU own budget and national transfers are coupled, not one cycle | [Mermaid source](diagrams/mermaid/14g_lgu_two_coupled_cycles.mmd) |
| 15g | Entity and funding channel variants | [Mermaid source](diagrams/mermaid/15g_entity_and_fund_specific_paths.mmd) |
| 16h | IFMIS implementation is not equivalent to an interface | [Mermaid source](diagrams/mermaid/16h_ifmis_deployment_confidence.mmd) |
| 16i | IFMIS interface failure and duplicate entry pattern | [Mermaid source](diagrams/mermaid/16i_interface_failure_and_reconciliation.mmd) |
| 17e | Multi-identifier lineage across planning, budget and payments | [Mermaid source](diagrams/mermaid/17e_multi_identifier_lineage.mmd) |
| 17f | UACS code revisions and crosswalk controls | [Mermaid source](diagrams/mermaid/17f_uacs_version_crosswalk.mmd) |
| 18c | Performance evidence flows into later budget cycles | [Mermaid source](diagrams/mermaid/18c_performance_budget_learning.mmd) |
| 19c | Future-year fiscal commitments and contingent risk | [Mermaid source](diagrams/mermaid/19c_fiscal_risk_multiyear.mmd) |
| 00l | Parallel PFM workstreams by authority | [PlantUML source](diagrams/plantuml/00l_four_parallel_authority_lanes.puml) |
| 07j | Alternative disbursement control gates | [PlantUML source](diagrams/plantuml/07j_payment_control_gate_sequence.puml) |
| 08g | Independent accounting and assurance processes | [PlantUML source](diagrams/plantuml/08g_recording_and_audit_lanes.puml) |
| 16j | Authority, source-of-record and integration distinction | [PlantUML source](diagrams/plantuml/16j_system_of_record_vs_interfaces.puml) |
| 17g | Typed financial records with stable IDs and versioned classification | [PlantUML source](diagrams/plantuml/17g_financial_record_class_model.puml) |

### Critical limits on legacy views

- **00a** is a teaching sequence, not an event order: accounting recognition, controls, procurement preparation and receipts occur contemporaneously. Use **00i** and **00l** for chronology.
- **00d** and **07b** illustrate a standard contract-payment scenario, not universal conditions for payroll, lawful advances, transfers, debt service or refunds. Use **07h**, **07i** and **07j**.
- **00f** is an illustrative one-year traversal, not an operational process for each actor; use **00l** and **08g** for parallelism.
- **16b/16g/16d** include known applications and architecture concepts; do **not** infer a live machine-to-machine interface from proximity, a flow arrow, or the use of UACS. Use **16h**, **16i** and `reference/I_interface_evidence_and_status.md`.
- Figures in `rendered/` are the **original edition 2 render set**; no new image is misrepresented as generated or visually validated.

## 3. All diagrams

The first two characters of an ID give the chapter. Chapter 00 is the big picture.

| ID | Title | Form | Code file | Image |
|---|---|---|---|---|
| 00a | The whole PFM cycle of the national government, and the chapter that describes each part | Mermaid flowchart | [`00a_pfm_cycle_overview.mmd`](diagrams/mermaid/00a_pfm_cycle_overview.mmd) | [image](rendered/00a_pfm_cycle_overview.png) |
| 00b | The authorities of Philippine PFM, grouped by their position in government | Mermaid flowchart | [`00b_authorities_map.mmd`](diagrams/mermaid/00b_authorities_map.mmd) | [image](rendered/00b_authorities_map.png) |
| 00c | Information systems of Philippine PFM, grouped by the institution that owns or operates each one | Mermaid flowchart | [`00c_systems_landscape.mmd`](diagrams/mermaid/00c_systems_landscape.mmd) | [image](rendered/00c_systems_landscape.png) |
| 00d | Four parallel chains and the three points where they must meet (one contract payment) | Mermaid flowchart | [`00d_four_chains.mmd`](diagrams/mermaid/00d_four_chains.mmd) | [image](rendered/00d_four_chains.png) |
| 00e | Three budgets are active in one calendar year (example: calendar year 2026) | Mermaid Gantt chart | [`00e_calendar_three_budgets.mmd`](diagrams/mermaid/00e_calendar_three_budgets.mmd) | [image](rendered/00e_calendar_three_budgets.png) |
| 00f | One fiscal year from plan to audit: who acts at each step (national government agency) | PlantUML activity diagram with lanes | [`00f_end_to_end_swimlane.puml`](diagrams/plantuml/00f_end_to_end_swimlane.puml) | [image](rendered/00f_end_to_end_swimlane.png) |
| 00g | What passes between the authorities: decisions, money and information | Mermaid flowchart | [`00g_exchanges_between_authorities.mmd`](diagrams/mermaid/00g_exchanges_between_authorities.mmd) | [image](rendered/00g_exchanges_between_authorities.png) |
| 00h | One contract with dates: a school building paid from the FY 2026 budget (invented example, real rules) | Mermaid Gantt chart | [`00h_worked_example_one_contract.mmd`](diagrams/mermaid/00h_worked_example_one_contract.mmd) | [image](rendered/00h_worked_example_one_contract.png) |
| 01a | From development plan to budget proposal: the chain of plans, national and local | Mermaid flowchart | [`01a_plan_hierarchy.mmd`](diagrams/mermaid/01a_plan_hierarchy.mmd) | [image](rendered/01a_plan_hierarchy.png) |
| 01b | Investment programming: how a project enters the PIP and TRIP and reaches the budget | Mermaid sequence diagram | [`01b_investment_programming_sequence.mmd`](diagrams/mermaid/01b_investment_programming_sequence.mmd) | [image](rendered/01b_investment_programming_sequence.png) |
| 02a | The fiscal frame: what the DBCC receives, what it decides, and where each decision is used | Mermaid flowchart | [`02a_fiscal_framework.mmd`](diagrams/mermaid/02a_fiscal_framework.mmd) | [image](rendered/02a_fiscal_framework.png) |
| 03a | Budget preparation: from the fiscal program to the President's budget (example: FY 2027 budget, prepared in 2026) | Mermaid sequence diagram | [`03a_budget_preparation_sequence.mmd`](diagrams/mermaid/03a_budget_preparation_sequence.mmd) | [image](rendered/03a_budget_preparation_sequence.png) |
| 03b | Budget preparation by office (example: FY 2027 budget, prepared in 2026) | PlantUML activity diagram with lanes | [`03b_budget_preparation_swimlane.puml`](diagrams/plantuml/03b_budget_preparation_swimlane.puml) | [image](rendered/03b_budget_preparation_swimlane.png) |
| 03c | The Two-Tier Budgeting Approach: how one program or project enters the proposed budget | Mermaid flowchart | [`03c_two_tier_budgeting.mmd`](diagrams/mermaid/03c_two_tier_budgeting.mmd) | [image](rendered/03c_two_tier_budgeting.png) |
| 03d | Budget preparation records: from agency forms to the documents sent to Congress | Mermaid flowchart | [`03d_budget_forms_and_documents.mmd`](diagrams/mermaid/03d_budget_forms_and_documents.mmd) | [image](rendered/03d_budget_forms_and_documents.png) |
| 04a | Budget legislation: from the President's budget to the General Appropriations Act (GAA) | Mermaid sequence diagram | [`04a_legislation_sequence.mmd`](diagrams/mermaid/04a_legislation_sequence.mmd) | [image](rendered/04a_legislation_sequence.png) |
| 04b | States of the budget bill, from proposal to law | Mermaid state diagram | [`04b_bill_states.mmd`](diagrams/mermaid/04b_bill_states.mmd) | [image](rendered/04b_bill_states.png) |
| 04c | Kinds of appropriation: the legal bases on which public money may be paid | Mermaid flowchart | [`04c_appropriation_types.mmd`](diagrams/mermaid/04c_appropriation_types.mmd) | [image](rendered/04c_appropriation_types.png) |
| 05a | Release of funds: two separate authorities, allotment (to commit) and cash authority (to pay). Example: FY 2026 | Mermaid sequence diagram | [`05a_release_sequence.mmd`](diagrams/mermaid/05a_release_sequence.mmd) | [image](rendered/05a_release_sequence.png) |
| 05b | Which release document applies to one budget item (FY 2026 rules) | Mermaid flowchart | [`05b_release_decision_tree.mmd`](diagrams/mermaid/05b_release_decision_tree.mmd) | [image](rendered/05b_release_decision_tree.png) |
| 05c | States of one budget line, and the exits at each stage | Mermaid state diagram | [`05c_budget_line_states.mmd`](diagrams/mermaid/05c_budget_line_states.mmd) | [image](rendered/05c_budget_line_states.png) |
| 05d | Kinds of disbursement authority: who issues each one, to whom, and what it allows | Mermaid flowchart | [`05d_cash_authorities.mmd`](diagrams/mermaid/05d_cash_authorities.mmd) | [image](rendered/05d_cash_authorities.png) |
| 05e | Changing an allotment during the year: modification, use of personnel allotment, augmentation from savings | Mermaid flowchart | [`05e_modification_and_savings.mmd`](diagrams/mermaid/05e_modification_and_savings.mmd) | [image](rendered/05e_modification_and_savings.png) |
| 06a | Procurement planning: from a need to an approved procurement plan, aligned with the budget calendar | Mermaid flowchart | [`06a_procurement_planning.mmd`](diagrams/mermaid/06a_procurement_planning.mmd) | [image](rendered/06a_procurement_planning.png) |
| 06b | Competitive bidding under the New Government Procurement Act (RA 12009): who does what, with the time limits | Mermaid sequence diagram | [`06b_competitive_bidding_sequence.mmd`](diagrams/mermaid/06b_competitive_bidding_sequence.mmd) | [image](rendered/06b_competitive_bidding_sequence.png) |
| 06c | The eleven modes of procurement in RA 12009 | Mermaid flowchart | [`06c_procurement_modes.mmd`](diagrams/mermaid/06c_procurement_modes.mmd) | [image](rendered/06c_procurement_modes.png) |
| 06d | Competitive bidding under RA 12009: decisions, loops and exits | PlantUML activity diagram with lanes | [`06d_competitive_bidding_swimlane.puml`](diagrams/plantuml/06d_competitive_bidding_swimlane.puml) | [image](rendered/06d_competitive_bidding_swimlane.png) |
| 06e | States of one contract, from award to closing | Mermaid state diagram | [`06e_contract_implementation.mmd`](diagrams/mermaid/06e_contract_implementation.mmd) | [image](rendered/06e_contract_implementation.png) |
| 06f | A contract that lasts more than one year: the Multi-Year Contractual Authority (MYCA) | Mermaid flowchart | [`06f_multi_year_contracts.mmd`](diagrams/mermaid/06f_multi_year_contracts.mmd) | [image](rendered/06f_multi_year_contracts.png) |
| 07a | From obligation to payment: who certifies what (goods, services and works of a national agency) | Mermaid sequence diagram | [`07a_obligation_to_payment_sequence.mmd`](diagrams/mermaid/07a_obligation_to_payment_sequence.mmd) | [image](rendered/07a_obligation_to_payment_sequence.png) |
| 07b | The three meeting points before a payment (national agency, contract for goods, services or works) | PlantUML activity diagram with lanes | [`07b_obligation_to_payment_swimlane.puml`](diagrams/plantuml/07b_obligation_to_payment_swimlane.puml) | [image](rendered/07b_obligation_to_payment_swimlane.png) |
| 07c | The chain of certifications for one payment: who signs, what the signature states, and who checks it | Mermaid flowchart | [`07c_voucher_certifications.mmd`](diagrams/mermaid/07c_voucher_certifications.mmd) | [image](rendered/07c_voucher_certifications.png) |
| 07d | Payment and settlement: how money moves from the Treasury Single Account to the payee (Modified Disbursement System) | Mermaid sequence diagram | [`07d_payment_settlement_sequence.mmd`](diagrams/mermaid/07d_payment_settlement_sequence.mmd) | [image](rendered/07d_payment_settlement_sequence.png) |
| 07e | Ways in which a national agency settles a payment | Mermaid flowchart | [`07e_payment_modes.mmd`](diagrams/mermaid/07e_payment_modes.mmd) | [image](rendered/07e_payment_modes.png) |
| 07f | States of one cash advance, from grant to liquidation | Mermaid state diagram | [`07f_cash_advance_states.mmd`](diagrams/mermaid/07f_cash_advance_states.mmd) | [image](rendered/07f_cash_advance_states.png) |
| 07g | When a step fails: who acts, where the transaction continues, and which record shows it | Mermaid flowchart | [`07g_when_a_step_fails.mmd`](diagrams/mermaid/07g_when_a_step_fails.mmd) | [image](rendered/07g_when_a_step_fails.png) |
| 08a | Two sets of records in each agency: budget registries and accounting books | Mermaid flowchart | [`08a_accounting_records_flow.mmd`](diagrams/mermaid/08a_accounting_records_flow.mmd) | [image](rendered/08a_accounting_records_flow.png) |
| 08b | Reporting: which report goes to whom, through which system, and when | Mermaid flowchart | [`08b_reporting_flows.mmd`](diagrams/mermaid/08b_reporting_flows.mmd) | [image](rendered/08b_reporting_flows.png) |
| 08c | Five measures of the same spending: the record, the report, and the reason why each differs from the next | Mermaid flowchart | [`08c_five_measures_of_one_spending.mmd`](diagrams/mermaid/08c_five_measures_of_one_spending.mmd) | [image](rendered/08c_five_measures_of_one_spending.png) |
| 08d | From the reports of each body to national totals: who adds what, and on which basis | Mermaid flowchart | [`08d_from_agency_reports_to_national_totals.mmd`](diagrams/mermaid/08d_from_agency_reports_to_national_totals.mmd) | [image](rendered/08d_from_agency_reports_to_national_totals.png) |
| 09a | External audit by COA: from submission of accounts to the annual reports | Mermaid sequence diagram | [`09a_audit_sequence.mmd`](diagrams/mermaid/09a_audit_sequence.mmd) | [image](rendered/09a_audit_sequence.png) |
| 09b | States of one audit finding on a transaction | Mermaid state diagram | [`09b_audit_finding_states.mmd`](diagrams/mermaid/09b_audit_finding_states.mmd) | [image](rendered/09b_audit_finding_states.png) |
| 09c | Layers of control and oversight over one spending agency | Mermaid flowchart | [`09c_oversight_map.mmd`](diagrams/mermaid/09c_oversight_map.mmd) | [image](rendered/09c_oversight_map.png) |
| 10a | Receipts of the national government: kinds, collectors, and the fund each receipt enters | Mermaid flowchart | [`10a_revenue_classification.mmd`](diagrams/mermaid/10a_revenue_classification.mmd) | [image](rendered/10a_revenue_classification.png) |
| 10b | Collection of taxes and customs duties: from the taxpayer to the Treasury Single Account | Mermaid sequence diagram | [`10b_tax_and_customs_collection_sequence.mmd`](diagrams/mermaid/10b_tax_and_customs_collection_sequence.mmd) | [image](rendered/10b_tax_and_customs_collection_sequence.png) |
| 10c | Fees and other income collected by an agency: from payment to the correct fund | Mermaid flowchart | [`10c_agency_collections.mmd`](diagrams/mermaid/10c_agency_collections.mmd) | [image](rendered/10c_agency_collections.png) |
| 10d | A tax refund: how money collected as tax is paid back | Mermaid sequence diagram | [`10d_tax_refund_sequence.mmd`](diagrams/mermaid/10d_tax_refund_sequence.mmd) | [image](rendered/10d_tax_refund_sequence.png) |
| 11a | The Treasury Single Account and the other bank accounts of the government | Mermaid flowchart | [`11a_tsa_account_structure.mmd`](diagrams/mermaid/11a_tsa_account_structure.mmd) | [image](rendered/11a_tsa_account_structure.png) |
| 11b | Cash programming: how the amount of cash authority for a period is decided | Mermaid sequence diagram | [`11b_cash_programming_sequence.mmd`](diagrams/mermaid/11b_cash_programming_sequence.mmd) | [image](rendered/11b_cash_programming_sequence.png) |
| 11c | Financing and debt: from the borrowing need to debt service | Mermaid flowchart | [`11c_financing_and_debt.mmd`](diagrams/mermaid/11c_financing_and_debt.mmd) | [image](rendered/11c_financing_and_debt.png) |
| 11d | One foreign project loan: approvals, signing, use of the loan and repayment | Mermaid sequence diagram | [`11d_foreign_loan_sequence.mmd`](diagrams/mermaid/11d_foreign_loan_sequence.mmd) | [image](rendered/11d_foreign_loan_sequence.png) |
| 12a | Personnel spending: from an authorized position to the monthly payroll and the remittances | Mermaid sequence diagram | [`12a_position_to_payroll_sequence.mmd`](diagrams/mermaid/12a_position_to_payroll_sequence.mmd) | [image](rendered/12a_position_to_payroll_sequence.png) |
| 12b | Personnel spending: sources of the allotment, and where each part of the gross pay goes | Mermaid flowchart | [`12b_personnel_funding_and_deductions.mmd`](diagrams/mermaid/12b_personnel_funding_and_deductions.mmd) | [image](rendered/12b_personnel_funding_and_deductions.png) |
| 13a | Life of a physical asset: from plan to disposal, with the record made at each stage | Mermaid flowchart | [`13a_asset_lifecycle.mmd`](diagrams/mermaid/13a_asset_lifecycle.mmd) | [image](rendered/13a_asset_lifecycle.png) |
| 14a | Budget cycle of a local government unit (province, city or municipality) under the Local Government Code | Mermaid sequence diagram | [`14a_lgu_budget_sequence.mmd`](diagrams/mermaid/14a_lgu_budget_sequence.mmd) | [image](rendered/14a_lgu_budget_sequence.png) |
| 14b | Money of a local government: sources, and the limits that every local budget must respect | Mermaid flowchart | [`14b_lgu_funds_and_mandatory_allocations.mmd`](diagrams/mermaid/14b_lgu_funds_and_mandatory_allocations.mmd) | [image](rendered/14b_lgu_funds_and_mandatory_allocations.png) |
| 14c | Points of contact between the national PFM system and a local government | Mermaid flowchart | [`14c_national_local_interfaces.mmd`](diagrams/mermaid/14c_national_local_interfaces.mmd) | [image](rendered/14c_national_local_interfaces.png) |
| 14d | Local budget cycle: decision points and their effects (province, city or municipality) | PlantUML activity diagram with lanes | [`14d_lgu_budget_swimlane.puml`](diagrams/plantuml/14d_lgu_budget_swimlane.puml) | [image](rendered/14d_lgu_budget_swimlane.png) |
| 14e | Money that a local government raises itself: real property tax and loans | Mermaid flowchart | [`14e_local_revenue_and_borrowing.mmd`](diagrams/mermaid/14e_local_revenue_and_borrowing.mmd) | [image](rendered/14e_local_revenue_and_borrowing.png) |
| 14f | The budget of a barangay: who prepares, who enacts, who reviews | Mermaid sequence diagram | [`14f_barangay_budget_sequence.mmd`](diagrams/mermaid/14f_barangay_budget_sequence.mmd) | [image](rendered/14f_barangay_budget_sequence.png) |
| 15a | Government corporations (GOCCs): corporate operating budget, budgetary support and reports | Mermaid sequence diagram | [`15a_gocc_budget_sequence.mmd`](diagrams/mermaid/15a_gocc_budget_sequence.mmd) | [image](rendered/15a_gocc_budget_sequence.png) |
| 15b | Transfer of funds from one agency to another body that will implement | Mermaid sequence diagram | [`15b_inter_agency_transfers.mmd`](diagrams/mermaid/15b_inter_agency_transfers.mmd) | [image](rendered/15b_inter_agency_transfers.png) |
| 15c | The path after allotment depends on the kind of spending | Mermaid flowchart | [`15c_spending_paths.mmd`](diagrams/mermaid/15c_spending_paths.mmd) | [image](rendered/15c_spending_paths.png) |
| 15d | Fund clusters: seven groups of money inside one agency, each with its own books and reports | Mermaid flowchart | [`15d_fund_clusters.mmd`](diagrams/mermaid/15d_fund_clusters.mmd) | [image](rendered/15d_fund_clusters.png) |
| 15e | Money for disasters: standby funds of agencies, the national fund, and the fund of each local government | Mermaid flowchart | [`15e_disaster_funds.mmd`](diagrams/mermaid/15e_disaster_funds.mmd) | [image](rendered/15e_disaster_funds.png) |
| 15f | Cash aid to persons: from the list of beneficiaries to the credit in each account | Mermaid sequence diagram | [`15f_cash_aid_to_persons_sequence.mmd`](diagrams/mermaid/15f_cash_aid_to_persons_sequence.mmd) | [image](rendered/15f_cash_aid_to_persons_sequence.png) |
| 16a | Information systems by PFM function: in use today, and planned under the IFMIS | Mermaid flowchart | [`16a_systems_by_function.mmd`](diagrams/mermaid/16a_systems_by_function.mmd) | [image](rendered/16a_systems_by_function.png) |
| 16b | Spending side: information systems inside their owner institutions, and the data that passes between them (2026) | PlantUML component diagram | [`16b_systems_components_spending.puml`](diagrams/plantuml/16b_systems_components_spending.puml) | [image](rendered/16b_systems_components_spending.png) |
| 16c | BTMS Budget Execution Module: records, the links between them, and the checks made by the system | Mermaid flowchart | [`16c_btms_execution_flow.mmd`](diagrams/mermaid/16c_btms_execution_flow.mmd) | [image](rendered/16c_btms_execution_flow.png) |
| 16d | Planned IFMIS: BTMS as the core, other systems connected through interfaces | Mermaid flowchart | [`16d_ifmis_target_architecture.mmd`](diagrams/mermaid/16d_ifmis_target_architecture.mmd) | [image](rendered/16d_ifmis_target_architecture.png) |
| 16e | Digital PFM in the Philippines - main events, 2011 to 2028 | Mermaid timeline | [`16e_digital_pfm_timeline.mmd`](diagrams/mermaid/16e_digital_pfm_timeline.mmd) | [image](rendered/16e_digital_pfm_timeline.png) |
| 16f | Public verification of DBM release documents with a blockchain record | Mermaid sequence diagram | [`16f_document_verification_blockchain.mmd`](diagrams/mermaid/16f_document_verification_blockchain.mmd) | [image](rendered/16f_document_verification_blockchain.png) |
| 16g | Revenue and treasury side: information systems and accounts inside their owner institutions (2026) | PlantUML component diagram | [`16g_systems_components_revenue_treasury.puml`](diagrams/plantuml/16g_systems_components_revenue_treasury.puml) | [image](rendered/16g_systems_components_revenue_treasury.png) |
| 17a | Structure of the Unified Accounts Code Structure (UACS): 54 digits in five segments | Mermaid flowchart | [`17a_uacs_structure.mmd`](diagrams/mermaid/17a_uacs_structure.mmd) | [image](rendered/17a_uacs_structure.png) |
| 17b | The chain of records for one purchase: each record's own number, the codes it contains, and the link to the next record | Mermaid flowchart | [`17b_identifier_chain.mmd`](diagrams/mermaid/17b_identifier_chain.mmd) | [image](rendered/17b_identifier_chain.png) |
| 17c | Records of budget execution as a data model: fields, own numbers (PK) and quoted numbers (FK) | Mermaid entity-relationship diagram | [`17c_record_lineage_er.mmd`](diagrams/mermaid/17c_record_lineage_er.mmd) | [image](rendered/17c_record_lineage_er.png) |
| 17d | Why UACS alone cannot follow one contract: a code names a class, a document number names one record | Mermaid flowchart | [`17d_uacs_class_not_instance.mmd`](diagrams/mermaid/17d_uacs_class_not_instance.mmd) | [image](rendered/17d_uacs_class_not_instance.png) |
| 18a | From a target in the budget law to a reported result: the path of performance information | Mermaid flowchart | [`18a_performance_information_flow.mmd`](diagrams/mermaid/18a_performance_information_flow.mmd) | [image](rendered/18a_performance_information_flow.png) |
| 18b | Four ways to examine performance, and the question that each one answers | Mermaid flowchart | [`18b_four_examinations_of_performance.mmd`](diagrams/mermaid/18b_four_examinations_of_performance.mmd) | [image](rendered/18b_four_examinations_of_performance.png) |
| 19a | Fiscal risks: payments that the Treasury may have to make, although no budget line of today names them | Mermaid flowchart | [`19a_fiscal_risks_map.mmd`](diagrams/mermaid/19a_fiscal_risks_map.mmd) | [image](rendered/19a_fiscal_risks_map.png) |
| 19b | A national public-private partnership: approvals, promises of the government, and the two links to the budget | PlantUML activity diagram with lanes | [`19b_ppp_project_swimlane.puml`](diagrams/plantuml/19b_ppp_project_swimlane.puml) | [image](rendered/19b_ppp_project_swimlane.png) |


## 4. The chapters

| File | Subject | Diagrams |
|---|---|---|
| [processes/01_planning_and_investment_programming.md](processes/01_planning_and_investment_programming.md) | Development plan, investment program, appraisal of large projects | 01a, 01b |
| [processes/02_macro_fiscal_framework.md](processes/02_macro_fiscal_framework.md) | The DBCC and the fiscal program | 02a |
| [processes/03_budget_preparation.md](processes/03_budget_preparation.md) | Budget Call, proposals in two tiers, the budget of the President | 03a to 03d |
| [processes/04_budget_legislation.md](processes/04_budget_legislation.md) | Congress, veto, reenactment, kinds of appropriation | 04a to 04c |
| [processes/05_budget_release_allotment_and_cash_authority.md](processes/05_budget_release_allotment_and_cash_authority.md) | Allotment and cash authority | 05a to 05e |
| [processes/06_procurement.md](processes/06_procurement.md) | Procurement under Republic Act No. 12009, early procurement, contracts for more than one year | 06a to 06f |
| [processes/07_obligation_delivery_payment.md](processes/07_obligation_delivery_payment.md) | Obligation, acceptance, voucher, payment through the bank, and what happens when a step fails | 07a to 07g |
| [processes/08_accounting_and_reporting.md](processes/08_accounting_and_reporting.md) | Registries, books, reports, five measures of one spending, national totals | 08a to 08d |
| [processes/09_audit_and_oversight.md](processes/09_audit_and_oversight.md) | Audit by COA, notices, oversight | 09a to 09c |
| [processes/10_revenue_collection.md](processes/10_revenue_collection.md) | Taxes, customs duties, fees, refunds | 10a to 10d |
| [processes/11_treasury_cash_and_debt.md](processes/11_treasury_cash_and_debt.md) | Treasury Single Account, cash program, borrowing, debt | 11a to 11d |
| [processes/12_personnel_and_payroll.md](processes/12_personnel_and_payroll.md) | Positions, payroll, remittances | 12a, 12b |
| [processes/13_assets_and_property.md](processes/13_assets_and_property.md) | Life of a physical asset | 13a |
| [processes/14_local_governments.md](processes/14_local_governments.md) | Local budget cycle and its contacts with the national system, property tax, loans, barangay budgets | 14a to 14f |
| [processes/15_gocc_transfers_and_fund_clusters.md](processes/15_gocc_transfers_and_fund_clusters.md) | Government corporations, fund transfers, other spending paths, disaster funds, cash aid, fund clusters | 15a to 15f |
| [processes/16_information_systems_and_ifmis.md](processes/16_information_systems_and_ifmis.md) | Systems, data flows, BTMS, the planned IFMIS, the COMPASS portal | 16a to 16g |
| [processes/17_uacs_and_record_identifiers.md](processes/17_uacs_and_record_identifiers.md) | UACS and the numbers that connect records | 17a to 17d |
| [processes/18_performance_information_and_evaluation.md](processes/18_performance_information_and_evaluation.md) | Targets, reports of results, performance review, evaluation | 18a, 18b |
| [processes/19_fiscal_risks_ppp_and_contingent_liabilities.md](processes/19_fiscal_risks_ppp_and_contingent_liabilities.md) | Fiscal risks, partnerships with private firms, promises under conditions | 19a, 19b |

Most chapters have the same parts: the question it answers, the idea in plain words with one case where the process works and one where it fails, the authorities and their roles, the steps, the documents and identifiers, the information systems, the controls (what each one checks and what it does not check), the timing, the reported weaknesses, the diagrams, and the verification status.

## 5. The reference files

| File | Content |
|---|---|
| [reference/A_authorities_and_mandates.md](reference/A_authorities_and_mandates.md) | Every authority, its role, its systems, its legal basis |
| [reference/B_information_systems_inventory.md](reference/B_information_systems_inventory.md) | Every information system: owner, user, recipient of the data, content. Planned systems. A register of the 54 flows between systems, each with the evidence for it. Status of BTMS |
| [reference/C_documents_and_identifiers.md](reference/C_documents_and_identifiers.md) | Every document of the process: who issues it, what it does, how it is identified. For 34 records: what the record proves and what it does not prove |
| [reference/D_legal_framework.md](reference/D_legal_framework.md) | Constitution, laws, orders, circulars, bills |
| [reference/E_glossary.md](reference/E_glossary.md) | Terms, each with the term that it should not be confused with, and abbreviations |
| [reference/F_sources_and_verification.md](reference/F_sources_and_verification.md) | Every source with its code, its address and the way it was read. Defects. Documents that were not opened. The changes of the second version |
| [reference/G_open_questions_and_known_gaps.md](reference/G_open_questions_and_known_gaps.md) | Contradictions between sources, facts that could not be verified, and the coverage of each subject |

## 6. How accuracy is marked

Every table of steps has a column "Basis". Every diagram file contains comment lines that name its sources.

| Mark | Meaning |
|---|---|
| A code in square brackets, for example [NBC599] or [RA12009 s.49] | I opened this source during this work and found the fact in it. Reference F explains each code |
| GK | General knowledge. I wrote the line from what I know, and I did not open a source for it. Check these lines first |
| Inference | My own conclusion from two or more sources. No source states it in these words |

Three limits apply to everything. I read most sources through a tool that returns a summary of the page with short quotations, not the full text. Some official files are scanned images, and parts of them were unreadable. Rules that are set each year are given for fiscal year 2026 or 2027.

Three important documents could not be opened: the Government Accounting Manual, Book VI of the Administrative Code of 1987, and most of the Government Auditing Code. A fourth, the implementing rules of the procurement law, could be read only as far as section 35.5. The parts of the atlas that depend on them are marked GK. Two facts of 2026 are known to me only from press releases and press reports: Executive Order No. 126 on the COMPASS portal, and the state of the FY 2027 budget bill.

## 7. Conventions in the diagram files

**Header comments.** Each `.mmd` file has comment lines near its start (they begin with `%%`). Each `.puml` file has comment lines that begin with `'`. The lines have fixed openings:

| Opening of the line | Content |
|---|---|
| `QUESTION THIS DIAGRAM ANSWERS:` | The one question that the diagram answers |
| `IDEA:` | The idea in plain words |
| `READING:` | How to read the shapes, arrows and colours |
| `SOURCES:` | The sources, by code |
| `GENERAL KNOWLEDGE, NOT OPENED IN A SOURCE HERE:` | The parts of the diagram that are not from an opened source |
| `INFERENCE:` | A statement in the diagram that is my own conclusion |
| `ADDED IN OCTOBER 2026:` | What was added in the second version |
| Other openings, for example `NOT STATED IN THE SOURCES I READ:` | Limits of the diagram |

**Colours.** In the overview diagrams and in most others, the colour of a frame or box marks the kind of authority: blue for the executive (DBM, DEPDev, the President and the collegial bodies), purple for Congress, green for spending agencies and local governments, yellow for the finance side (DOF and its bureaus, the Treasury accounts, the banks), light orange for COA and the other independent bodies, a stronger orange for BTMS, and grey for parties outside government and for planned items. Some diagrams use colour for another purpose, and their `READING:` line says so.

**Arrows.** In diagrams that show exchanges: a thin solid arrow is a decision or a document, a thick arrow is money, a dotted arrow is information. In the two component diagrams of chapter 16, a dashed grey arrow means that no electronic interface is described in the sources. Section 5.1 of the big picture lists all kinds of arrows.

**Numbers in sequence diagrams.** The steps are numbered by Mermaid. The tables of steps in the chapters use the same numbers.

**One technical mark in sequence diagrams.** A step that an actor performs alone (a message from an actor to itself) ends with a line that contains only `#nbsp;`. This code means a non-breaking space, which is a space character that the program does not delete. The empty line moves the text away from the step number in the picture. It has no other meaning.

**Why some diagrams are in PlantUML.** Mermaid is the main notation. Eight diagrams are in PlantUML because Mermaid cannot draw them well: six lane diagrams with parallel bars or decision points (00f, 03b, 06d, 07b, 14d, 19b), and two component diagrams that place systems inside frames of their owner institutions (16b, 16g).

## 8. How to render the diagrams

The images in `rendered/` were made with Mermaid 11.16 (through the command-line tool `mmdc`, version 11.16.0) and PlantUML 1.2026.8. Afterwards each image was reduced to 256 colours, which makes the files smaller and does not change what is shown.

```
# Mermaid: needs Node.js and the package @mermaid-js/mermaid-cli
mmdc -i diagrams/mermaid/07a_obligation_to_payment_sequence.mmd -o 07a.png -b white -s 2 -w 2000

# PlantUML: needs Java and plantuml.jar. The two component diagrams also need Graphviz
java -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.jar -tpng diagrams/plantuml/07b_obligation_to_payment_swimlane.puml
```

The code can also be pasted into an online editor for Mermaid or PlantUML. Most `.mmd` files start with a block between two lines of three hyphens. This block sets the title and one layout option, and it needs a recent version of Mermaid.

## 9. Notes on the Markdown files

- In the chapters, each Mermaid diagram appears as a code block that many Markdown viewers draw as a picture. The code block is the content of the `.mmd` file without its comment lines. The comment lines are shown above the block as a list.
- Each PlantUML diagram appears as an image from `rendered/`, with its code below it.
- The tables of steps were generated from the sequence diagrams, so the numbers and texts of the steps agree with the diagrams.
- Each paragraph is one line of text, without line breaks inside it.
- The folder `reference/` also contains three files in CSV form (text with commas between the values, which a spreadsheet or a program can open). `diagram_index.csv` has one row for each diagram: its ID, its form, its title, the question it answers, its files, and the Markdown files that contain it. `steps_register.csv` has one row for each numbered step of the 19 sequence diagrams that have a table of steps: who acts, towards whom, what is done, and the basis. `interface_register.csv` is the register of Reference B, section 4. The three files are written by the same script that builds the Markdown files, so they agree with them.

## 10. How to check the package

The script `tools/check_atlas.py` tests that the parts of the package agree with each other. It needs Python 3 and no other program.

```
python3 tools/check_atlas.py
```

| It checks | Why |
|---|---|
| Every diagram file has an image, states its question and names its sources | A diagram without a stated question cannot be judged |
| No Mermaid flowchart uses a reserved word of Mermaid, for example `end`, `class` or `call`, as the name of a node | Such a file looks correct as text and cannot be drawn |
| Every code block in a Markdown file is equal to a diagram file, and every diagram file is in a Markdown file | A description and its diagram must not differ |
| Every link leads to a file that exists | |
| Every source code in square brackets and in a column "Basis" is defined in Reference F | A code without a definition cannot be traced |
| Every table row has the right number of cells, and no cell of a column "Basis" is empty | |
| The CSV files agree with the diagram files and with Reference B. The steps in the register agree with the sequence diagrams | |
| Every paragraph is on one line | |

With the option `--render` the script also draws every Mermaid file, if the program `mmdc` is installed. The script does not test whether a statement of the atlas is true. That needs the sources.

For this version the script reports no problem, and all 81 diagrams were drawn with the versions named in section 8.

## 11. What the package contains beyond the request

The first request was for diagram code in Mermaid (and in PlantUML where that is better), for a description of each process, and for a big-picture description. The second request was to check a second atlas and to take improvements from it. The package contains six things that are outside the two requests. I name them here so that they can be ignored or deleted.

1. `rendered/`: an image of every diagram, so that the diagrams can be seen without any tool.
2. `reference/`: seven reference files. Files A and B contain the inventory of the authorities and of their information systems. Files F and G contain the sources and the open questions.
3. This README.
4. The three CSV files in `reference/`.
5. The script in `tools/`.
6. Two additions that result from my own search and not from the second atlas: the COMPASS portal with Executive Order No. 126 of 2026 (chapter 16, section 11), and the state of the FY 2027 budget bill in October 2026 (chapter 04, section 9). Reference F, section 6.6, names them.

## 12. What the atlas does not cover

Tax policy and tax administration beyond the flow of collections and refunds. Social security institutions and government financial institutions. The Bangsamoro region and its block grant. The bodies with fiscal autonomy. Accounting standards in detail. Amounts of guarantees and of other contingent liabilities. Reference G, section 3, gives the state of coverage for every subject, with its least certain part.

## New machine-readable reference registers (edition 3)

| File | What it describes | Guarantee |
|---|---|---|
| [Authority register](reference/authority_register.csv) | Institutional actors, roles, scope and source code | Conceptual actor IDs, **not operational delegations** |
| [Record type register](reference/record_type_register.csv) | Versioned document and record families | Schemas not verified with live agency systems |
| [Event register](reference/event_register.csv) | A type, responsible actor, evidence, output and controls | Conceptual relationships, not chronological logs |
| [Control rule register](reference/control_rule_register.csv) | Gate conditions and primary-reference anchors | Illustrative; not exhaustive legal checklists |
| [Interface evidence register](reference/interface_evidence_register.csv) | The 54 legacy interface assertions split into 15 auditable fields | All technical/deployment unknowns kept explicit |

**Recommended entry:** the new [reference model](reference/H_reference_model_contract.md), [control patterns](reference/J_controls_exceptions_and_temporal_model.md), and [interface evidence protocol](reference/I_interface_evidence_and_status.md). The original interface register is preserved intact for traceability.

New code consolidated in the [sourcebook](reference/M_sourcebook_new_diagrams.md).

See the [seven transaction walk-throughs](reference/N_scenario_walkthroughs.md) and [domain completeness matrix](reference/O_domain_completeness_and_evidence.md) for practical interpretation and research priorities.
