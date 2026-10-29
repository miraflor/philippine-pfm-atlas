# Philippine PFM Atlas

A set of diagrams and descriptions that map public financial management (PFM) of the Philippine national government: the process, the authorities that participate in it, and their information systems. Facts on current events are as of 8 October 2026.

The atlas is based mainly on five texts that were read in full as files: the three volumes of the Government Accounting Manual, the Government Auditing Code, and the Implementing Rules of the procurement law. Book VI of the Administrative Code, the release rules of the budget, the issuances of the GPPB after the Implementing Rules and many other sources were read through a tool that returns a summary with short quotations. [Reference F](reference/F_sources_and_verification.md) lists every source and the way it was read, and in section 5 the decisions that shape the atlas.

This atlas is not an official publication of the Philippine government. It does not replace the laws, circulars and manuals that it cites.

## 1. Where to start

1. Read [00_BIG_PICTURE.md](00_BIG_PICTURE.md). It gives the whole on a few pages and contains the eight overview diagrams.
2. Open the chapter of the part you need (section 4 below). Each chapter explains one process and contains its diagrams.
3. Use the reference files for the authorities, the information systems, the documents, the laws, the terms, the sources, and the open questions (section 5).
4. Before a diagram is reused for another purpose, read section 5.1 of the big picture. It names the nine kinds of arrows of this atlas and, for each kind, an observation that would show an arrow to be wrong.
5. To see what is not settled, read [Reference G](reference/G_open_questions_and_known_gaps.md): 18 differences between sources and 68 facts that I could not verify, each with a number.

## 2. What the atlas contains

| Folder or file | Content | Number of files |
|---|---|---|
| `00_BIG_PICTURE.md` | The big picture | 1 |
| `README.md` | This file | 1 |
| `processes/` | One description for each process | 19 |
| `reference/` | Reference files A to G in Markdown | 7 |
| `reference/` | Three tables in CSV form, for use by a program (section 9) | 3 |
| `diagrams/mermaid/` | Diagram code in Mermaid (`.mmd`) | 77 |
| `diagrams/plantuml/` | Diagram code in PlantUML (`.puml`) | 8 |
| `rendered/` | A PNG image of every diagram | 85 |

In the repository these files are in the folder `docs/atlas/`. They are built from the sources in the folder `src/` by the script `tools/build_atlas.py`, and the website of the atlas is built from them (section 10, and the README of the repository).

## 3. All diagrams

The first two characters of an ID give the chapter. Chapter 00 is the big picture.

| ID | Title | Form | Code file | Image |
|---|---|---|---|---|
| 00a | The whole of PFM for the national government: what happens in order, what happens at the same time, and the chapter for each part | Mermaid flowchart | [`00a_pfm_cycle_overview.mmd`](diagrams/mermaid/00a_pfm_cycle_overview.mmd) | [image](rendered/00a_pfm_cycle_overview.png) |
| 00b | The authorities of Philippine PFM, grouped by their position in government | Mermaid flowchart | [`00b_authorities_map.mmd`](diagrams/mermaid/00b_authorities_map.mmd) | [image](rendered/00b_authorities_map.png) |
| 00c | Information systems of Philippine PFM, grouped by the institution that owns or operates each one | Mermaid flowchart | [`00c_systems_landscape.mmd`](diagrams/mermaid/00c_systems_landscape.mmd) | [image](rendered/00c_systems_landscape.png) |
| 00d | Three lines of steps, the three points where they must meet, and the record that each act writes (one payment under a contract) | Mermaid flowchart | [`00d_four_chains.mmd`](diagrams/mermaid/00d_four_chains.mmd) | [image](rendered/00d_four_chains.png) |
| 00e | Three budgets are active in one calendar year (example: calendar year 2026) | Mermaid Gantt chart | [`00e_calendar_three_budgets.mmd`](diagrams/mermaid/00e_calendar_three_budgets.mmd) | [image](rendered/00e_calendar_three_budgets.png) |
| 00f | One fiscal year from plan to audit: who acts at each step, and which record is written there (national government agency) | PlantUML activity diagram with lanes | [`00f_end_to_end_swimlane.puml`](diagrams/plantuml/00f_end_to_end_swimlane.puml) | [image](rendered/00f_end_to_end_swimlane.png) |
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
| 06c | The eleven modes of procurement in RA 12009, with the type that the GPPB added in 2026 | Mermaid flowchart | [`06c_procurement_modes.mmd`](diagrams/mermaid/06c_procurement_modes.mmd) | [image](rendered/06c_procurement_modes.png) |
| 06d | Competitive bidding under RA 12009: decisions, loops and exits | PlantUML activity diagram with lanes | [`06d_competitive_bidding_swimlane.puml`](diagrams/plantuml/06d_competitive_bidding_swimlane.puml) | [image](rendered/06d_competitive_bidding_swimlane.png) |
| 06e | States of one contract, from award to closing | Mermaid state diagram | [`06e_contract_implementation.mmd`](diagrams/mermaid/06e_contract_implementation.mmd) | [image](rendered/06e_contract_implementation.png) |
| 06f | A contract that lasts more than one year: the Multi-Year Contractual Authority (MYCA) | Mermaid flowchart | [`06f_multi_year_contracts.mmd`](diagrams/mermaid/06f_multi_year_contracts.mmd) | [image](rendered/06f_multi_year_contracts.png) |
| 06g | A framework agreement: funds are certified before each order, not before the agreement | Mermaid flowchart | [`06g_framework_agreement.mmd`](diagrams/mermaid/06g_framework_agreement.mmd) | [image](rendered/06g_framework_agreement.png) |
| 07a | From obligation to payment: who certifies what, and which record each step writes (goods bought by a national agency, paid by payment order) | Mermaid sequence diagram | [`07a_obligation_to_payment_sequence.mmd`](diagrams/mermaid/07a_obligation_to_payment_sequence.mmd) | [image](rendered/07a_obligation_to_payment_sequence.png) |
| 07b | The three meeting points before a payment, and the record written at each step (national agency, contract for goods) | PlantUML activity diagram with lanes | [`07b_obligation_to_payment_swimlane.puml`](diagrams/plantuml/07b_obligation_to_payment_swimlane.puml) | [image](rendered/07b_obligation_to_payment_swimlane.png) |
| 07c | The chain of certifications for one payment: who signs, what the signature states, and who checks it | Mermaid flowchart | [`07c_voucher_certifications.mmd`](diagrams/mermaid/07c_voucher_certifications.mmd) | [image](rendered/07c_voucher_certifications.png) |
| 07d | Payment and settlement: how money moves from the Treasury Single Account to the payee (Modified Disbursement System) | Mermaid sequence diagram | [`07d_payment_settlement_sequence.mmd`](diagrams/mermaid/07d_payment_settlement_sequence.mmd) | [image](rendered/07d_payment_settlement_sequence.png) |
| 07e | Ways in which a national agency settles a payment | Mermaid flowchart | [`07e_payment_modes.mmd`](diagrams/mermaid/07e_payment_modes.mmd) | [image](rendered/07e_payment_modes.png) |
| 07f | States of one cash advance, from grant to liquidation | Mermaid state diagram | [`07f_cash_advance_states.mmd`](diagrams/mermaid/07f_cash_advance_states.mmd) | [image](rendered/07f_cash_advance_states.png) |
| 07g | When a step fails: who acts, where the transaction continues, and which record shows it | Mermaid flowchart | [`07g_when_a_step_fails.mmd`](diagrams/mermaid/07g_when_a_step_fails.mmd) | [image](rendered/07g_when_a_step_fails.png) |
| 07h | Kinds of payment: what creates the claim, what proves it before payment, and what the books record at that time | Mermaid flowchart | [`07h_kinds_of_claim.mmd`](diagrams/mermaid/07h_kinds_of_claim.mmd) | [image](rendered/07h_kinds_of_claim.png) |
| 07i | A works contract with an advance, progress billings and retention money (example of the Manual) | Mermaid sequence diagram | [`07i_advance_progress_retention.mmd`](diagrams/mermaid/07i_advance_progress_retention.mmd) | [image](rendered/07i_advance_progress_retention.png) |
| 08a | The records inside one agency: which unit keeps which record, from which document, and which report is built from it | Mermaid flowchart | [`08a_accounting_records_flow.mmd`](diagrams/mermaid/08a_accounting_records_flow.mmd) | [image](rendered/08a_accounting_records_flow.png) |
| 08b | Reporting: which report goes to whom, through which system, and when | Mermaid flowchart | [`08b_reporting_flows.mmd`](diagrams/mermaid/08b_reporting_flows.mmd) | [image](rendered/08b_reporting_flows.png) |
| 08c | Five measures of the same spending: the record, the report, and the reason why each differs from the next | Mermaid flowchart | [`08c_five_measures_of_one_spending.mmd`](diagrams/mermaid/08c_five_measures_of_one_spending.mmd) | [image](rendered/08c_five_measures_of_one_spending.png) |
| 08d | From the reports of each body to national totals: who adds what, and on which basis | Mermaid flowchart | [`08d_from_agency_reports_to_national_totals.mmd`](diagrams/mermaid/08d_from_agency_reports_to_national_totals.mmd) | [image](rendered/08d_from_agency_reports_to_national_totals.png) |
| 08e | One event, several records: what each unit and each body writes for the same purchase (national agency, payment order, tax withheld) | Mermaid flowchart | [`08e_one_event_several_records.mmd`](diagrams/mermaid/08e_one_event_several_records.mmd) | [image](rendered/08e_one_event_several_records.png) |
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
| 16b | Spending side: information systems inside their owner institutions, and what passes between them (2026) | PlantUML component diagram | [`16b_systems_components_spending.puml`](diagrams/plantuml/16b_systems_components_spending.puml) | [image](rendered/16b_systems_components_spending.png) |
| 16c | BTMS Budget Execution Module: records, the links between them, and the checks made by the system | Mermaid flowchart | [`16c_btms_execution_flow.mmd`](diagrams/mermaid/16c_btms_execution_flow.mmd) | [image](rendered/16c_btms_execution_flow.png) |
| 16d | Planned IFMIS: BTMS as the core, other systems connected through interfaces | Mermaid flowchart | [`16d_ifmis_target_architecture.mmd`](diagrams/mermaid/16d_ifmis_target_architecture.mmd) | [image](rendered/16d_ifmis_target_architecture.png) |
| 16e | Digital PFM in the Philippines - main events, 2011 to 2028 | Mermaid timeline | [`16e_digital_pfm_timeline.mmd`](diagrams/mermaid/16e_digital_pfm_timeline.mmd) | [image](rendered/16e_digital_pfm_timeline.png) |
| 16f | Public verification of DBM release documents with a blockchain record | Mermaid sequence diagram | [`16f_document_verification_blockchain.mmd`](diagrams/mermaid/16f_document_verification_blockchain.mmd) | [image](rendered/16f_document_verification_blockchain.png) |
| 16g | Revenue and treasury side: information systems and accounts inside their owner institutions (2026) | PlantUML component diagram | [`16g_systems_components_revenue_treasury.puml`](diagrams/plantuml/16g_systems_components_revenue_treasury.puml) | [image](rendered/16g_systems_components_revenue_treasury.png) |
| 17a | Structure of the Unified Accounts Code Structure (UACS): 54 digits in five segments | Mermaid flowchart | [`17a_uacs_structure.mmd`](diagrams/mermaid/17a_uacs_structure.mmd) | [image](rendered/17a_uacs_structure.png) |
| 17b | The chain of records for one purchase: each record's own number, the codes it contains, and the number that connects it to the next record | Mermaid flowchart | [`17b_identifier_chain.mmd`](diagrams/mermaid/17b_identifier_chain.mmd) | [image](rendered/17b_identifier_chain.png) |
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
| [processes/06_procurement.md](processes/06_procurement.md) | Procurement under Republic Act No. 12009 and the guidelines of the GPPB to August 2026, the forms of the procurement plans, early procurement, contracts for more than one year, framework agreements, the election period of 2026 | 06a to 06g |
| [processes/07_obligation_delivery_payment.md](processes/07_obligation_delivery_payment.md) | Obligation, acceptance, voucher, payment through the bank, the kinds of claim, advance payment and retention, cash advances, and what happens when a step fails | 07a to 07i |
| [processes/08_accounting_and_reporting.md](processes/08_accounting_and_reporting.md) | Which unit keeps which record, one event in several records, reports, closing of a period, five measures of one spending, national totals | 08a to 08e |
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
| [reference/B_information_systems_inventory.md](reference/B_information_systems_inventory.md) | Every information system: owner, user, recipient of the data, content. Planned systems. A register of 69 flows between systems and bodies. For each flow: what passes, its kind, its carrier, its stage of use, the check that compares both sides, and the basis. Status of BTMS |
| [reference/C_documents_and_identifiers.md](reference/C_documents_and_identifiers.md) | Every document of the process: who issues it, what it does, how it is identified. The forms of the Manual with their appendix numbers. The 19 links between records. For 39 records: what the record proves and what it does not prove |
| [reference/D_legal_framework.md](reference/D_legal_framework.md) | Constitution, laws, orders, circulars, bills. The provisions of the Auditing Code and of Book VI of the Administrative Code that the atlas uses |
| [reference/E_glossary.md](reference/E_glossary.md) | Terms, each with the term that it should not be confused with, and abbreviations |
| [reference/F_sources_and_verification.md](reference/F_sources_and_verification.md) | Every source with its code, its address and the way it was read. Defects. Documents that were not opened. The decisions that shape the atlas. The checks of quotations and of cited places |
| [reference/G_open_questions_and_known_gaps.md](reference/G_open_questions_and_known_gaps.md) | Differences between sources, facts that could not be verified, and the coverage of each subject |

## 6. How accuracy is marked

Every table of steps has a column "Basis". Every diagram file contains comment lines that name its sources.

| Mark | Meaning |
|---|---|
| A code in square brackets, for example [NBC599] or [RA12009 s.49] | I opened this source during this work and found the fact in it. Reference F explains each code |
| GK | General knowledge. I wrote the line from what I know, and I did not open a source for it. Check these lines first |
| Inference | My own conclusion from two or more sources. No source states it in these words |

Two more marks are used. Where two texts that I read say different things, the text says "a difference between two sources", states both, and does not decide. In the register of interfaces, "Not stated" means that the sources are silent. It does not mean that a flow or a system is absent.

How the sources were read. Five sources were read as files, word for word: the three volumes of the Government Accounting Manual of 2015, the Government Auditing Code of 1978, and the Implementing Rules of the procurement law as approved in February 2025. A program compares every quotation from these five with the text (section 10). I read the other sources through a tool that returns a summary of the page with short quotations, not the full text. Some official files are scanned images, and parts of them were unreadable.

Four limits remain. The Manual is of 2015, and I checked only one later change of it, the threshold of PHP 50,000 for property. The file of the Implementing Rules is the text of February 2025. I read the list of the resolutions of the GPPB to 14 August 2026 and fourteen of them, but only as summaries. Book VI of the Administrative Code was read as summaries with quotations, and its chapter 2 was not opened. Two facts of 2026 are known to me only from press releases and press reports: Executive Order No. 126 on the COMPASS portal, and the state of the FY 2027 budget bill. Rules that are set each year are given for fiscal year 2026 or 2027.

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
| `MORE SOURCES:` | Sources for parts of the diagram that the line `SOURCES:` does not name |
| Other openings, for example `NOT STATED IN THE SOURCES I READ:` | Limits of the diagram |

**Colours.** In the overview diagrams and in most others, the colour of a frame or box marks the kind of authority: blue for the executive (DBM, DEPDev, the President and the collegial bodies), purple for Congress, green for spending agencies and local governments, yellow for the finance side (DOF and its bureaus, the Treasury accounts, the banks), light orange for COA and the other independent bodies, a stronger orange for BTMS, and grey for parties outside government and for planned items. Some diagrams use colour for another purpose, and their `READING:` line says so.

**Arrows.** In diagrams that show exchanges: a thin solid arrow is a decision or a document, a thick arrow is money, a dotted arrow is information. In the two component diagrams of chapter 16, a solid black arrow means that a source describes an electronic channel, and a dashed grey arrow means paper, an entry by staff in a record of their own body, or a carrier that the sources do not state. The label of each arrow says which. In diagram 17b the colour of an arrow says whether a field of a form holds the number that links two records. Section 5.1 of the big picture lists all kinds of arrows.

**Numbers in sequence diagrams.** The steps are numbered by Mermaid. The tables of steps in the chapters use the same numbers.

**One technical mark in sequence diagrams.** A step that an actor performs alone (a message from an actor to itself) ends with a line that contains only `#nbsp;`. This code means a non-breaking space, which is a space character that the program does not delete. The empty line moves the text away from the step number in the picture. It has no other meaning.

**Why some diagrams are in PlantUML.** Mermaid is the main notation. Eight diagrams are in PlantUML because Mermaid cannot draw them well: six lane diagrams with parallel bars or decision points (00f, 03b, 06d, 07b, 14d, 19b), and two component diagrams that place systems inside frames of their owner institutions (16b, 16g).

## 8. How to render the diagrams

The images in `rendered/` were made with Mermaid 11.16 (through the command-line tool `mmdc`, version 11.16.0) and PlantUML 1.2026.8. Afterwards each image was reduced to 256 colours, which makes the files smaller and does not change what is shown.

In the repository the script `tools/render_diagrams.py` draws the images from the code files in `src/diagrams/` and reduces their colours. Its first lines say which programs it needs. One diagram can also be drawn by hand:

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
- In the big picture, four blocks stand between a line `<!-- site:NAME -->` and a line `<!-- /site:NAME -->`: the five parts, the four lines, the meeting points and the two cases. Markdown viewers do not show these lines. The website of the atlas shows the four blocks on its home page as well.
- The folder `reference/` also contains three files in CSV form (text with commas between the values, which a spreadsheet or a program can open). `diagram_index.csv` has one row for each diagram: its ID, its form, its title, the question it answers, its files, and the Markdown files that contain it. `steps_register.csv` has one row for each numbered step of the 20 sequence diagrams that have a table of steps: who acts, towards whom, what is done, and the basis. `interface_register.csv` is the register of Reference B, section 4, with the columns number, side, from, to, what passes, kind, carrier, stage of use, check of both sides, and basis. The three files are written by the same script that builds the Markdown files, so they agree with them.
- The Markdown files of the atlas are generated. A change is made in the source file in `src/`, and the script `tools/build_atlas.py` writes the file again. A change made only in `docs/atlas/` is lost at the next build.

## 10. How to check the atlas

The folder `tools/` of the repository contains the scripts. They need Python 3. Run them from the root of the repository.

**The first script** tests that the parts of the atlas agree with each other.

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
| The CSV files agree with the diagram files and with Reference B. The steps in the register agree with the sequence diagrams. Each row of the register of interfaces uses only the allowed values for kind, carrier and stage of use | |
| Every paragraph is on one line | |
| No file contains a placeholder that was not filled | |

With the option `--render` the script also draws every Mermaid file, if the program `mmdc` is installed.

**The second script** compares quotations with the source texts.

```
python3 tools/check_quotes.py src src/diagrams FOLDER_WITH_THE_SOURCE_TEXTS
```

It reads every line that names one of the five sources that I hold as text, takes each passage between quotation marks of 12 characters or more, and searches it in the text files. The repository does not contain these text files, because they are conversions of the five documents. A reader who wants to repeat the check must convert the same five documents to plain text and put them in one folder. The file `tools/quotes_by_hand.txt` lists the passages that the script cannot find for a stated reason and that I compared myself.

**The third script** tests that every place that the atlas cites in the same five sources exists: that Volume I of the Manual has a chapter 6 with a section 63, that the Rules have a section 71.2.8, that Volume II has an Appendix 32. It needs the same folder of source texts.

```
python3 tools/check_refs.py src src/diagrams FOLDER_WITH_THE_SOURCE_TEXTS
```

The script `tools/verify_counts.py` runs the second and the third script and tests that their results agree with the numbers written in Reference F, section 6.

No script tests whether a statement without quotation marks is true. The third script shows that a cited section exists, and not that the section says what the atlas says. That needs a reader with the sources.

At the last run the first script reported no problem, and all 85 diagrams were drawn with the versions named in section 8. The results of the second and of the third script are in Reference F, section 6. When the second or the third script is run on the built files in `docs/atlas/` and not on `src/`, its numbers are higher, because each chapter repeats the comment lines of its diagrams.

## 11. What the atlas does not cover

Tax policy and tax administration beyond the flow of collections and refunds. Social security institutions and government financial institutions. The Bangsamoro region and its block grant. The bodies with fiscal autonomy. The accounting standards for single subjects, for example financial instruments and leases: the Manual has a chapter for each, and I did not read these chapters. Amounts of guarantees and of other contingent liabilities. What agencies do in practice where practice differs from the rules: the atlas draws the rules and reports what one assessment of 2025 says about practice. Reference G, section 3, gives the state of coverage for every subject, with its least certain part.
