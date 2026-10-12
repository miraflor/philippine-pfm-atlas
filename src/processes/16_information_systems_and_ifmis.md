# 16. Information systems and the IFMIS

*Part of the Philippine PFM Atlas. Facts as of 8 October 2026. The statements on PhilGEPS and row 41 of the register are based on documents of the GPPB that I read on 12 October 2026. The codes in the column "Basis" are explained in [Reference F](../reference/F_sources_and_verification.md). "GK" means general knowledge that I did not open in a source during this work.*

## 1. The question this chapter answers

Which information system holds which record today, which institution owns it, by which carrier does each record pass from one system or body to the next, and what is the planned Integrated Financial Management Information System (IFMIS) meant to change?

The inventory of all systems, with owner, user and recipient of each one, is in [Reference B](../reference/B_information_systems_inventory.md). Reference B also contains a register of every flow between two systems or bodies. For each flow the register says what passes, by which carrier, whether it is in use, which control compares both sides, and where I read it. This chapter explains how the systems relate to each other.

## 2. The idea in plain words

Each institution built a system for its own part of the process. DBM has systems for budget proposals, positions, releases and reports. COA gives agencies systems for registries and books. BTr has systems for collections, cash and securities. BIR, BOC, the banks and DEPDev have their own. Each system serves the part of the process for which it was built. The difficulty lies between the systems. For most flows the sources describe a person who enters or uploads the content in the next system, or a paper copy. For few flows they describe a program that sends to another program, and for many they do not say how the content passes (section 6, and Reference B, section 4.4). The Roadmap names three gaps of this arrangement: the same report is prepared more than once, processing is manual, and the systems are not integrated [ROADMAP2024].

There are two ways to integrate. In the first, one large system replaces all the others. In the second, each institution keeps its system, one system holds the central records of budget execution, and the other systems exchange agreed records with it through interfaces. An **interface** (in the documents: API, application programming interface) is a defined way in which one program sends data to another and receives data from it.

The Philippine plan is the second way. The Roadmap describes interfaces that connect the existing separate systems to a central core, and says that agencies keep their existing systems [ROADMAP2024]. Its action plan calls BTMS the "interoperable core" of the IFMIS [SFA6].

A case where this design works: system A and system B use the same code for the same budget line and the same number for the same document. A record made in A can then be found in B without the help of a person.

A case where it fails: A and B use different codes, or give the same word different meanings. The interface then passes records that cannot be matched with each other. The action plan names this gap ("inconsistent classification codes across PFM systems") and plans three remedies: a review of UACS, one PFM data model, and a metadata registry, which is a list of the agreed definition of every data field [SFA6].

Terms. **IFMIS**: the Integrated Financial Management Information System that Executive Order No. 29 of 2023 tells all national government entities to adopt. **BTMS**: the Budget and Treasury Management System of DBM. **Core**: the system that holds the central records and to which the others connect. **Rollout**: the introduction of a system in one group of agencies after another.

## 3. What is known about the IFMIS

This section collects what the sources say, because the IFMIS is described in several documents and none of them gives the full picture.

| Subject | What the source says | Basis |
|---|---|---|
| First order | Executive Order No. 55 of 6 September 2011 ordered a Government Integrated Financial Management Information System (GIFMIS) for online accounting and monitoring of obligations and disbursements linked to cash management, a Treasury Single Account, and the PFM Committee, which was formed from an earlier committee on the GIFMIS | EO55 |
| Present order | Executive Order No. 29 of 1 June 2023. Its title begins "Strengthening the Integration of Public Financial Management Information Systems" and also names the amendment of Executive Order No. 55. All national government departments, agencies and instrumentalities, including government corporations, are directed to adopt and implement the IFMIS for government financial transactions. Local governments are encouraged to do so | EO29 |
| Scope in the order | Full digitalization of PFM processes through the IFMIS: budget management, budget execution, cash management, accounting and reporting | EO29 |
| What the order does not say | It gives no definition of the IFMIS. It does not name BTMS, the Treasury Single Account or UACS | EO29 |
| Who steers | The PFM Committee: representatives of DBM, DOF, COA and BTr. It must make a five-year development plan for the IFMIS, harmonize processes and systems, oversee the PFM Reforms Roadmap and review it at mid-term, and report each year to the Office of the President. DICT gives technical and policy support | EO29 |
| Money | First from the appropriations of the agencies and the corporate budgets, later from their budget proposals | EO29 |
| Design | Interfaces connect the existing systems to a central core. Agencies keep their systems | ROADMAP2024 |
| Core | BTMS | SFA6 |
| Present module of the core | The Budget Execution Module, with five functions. Modules for budget management and for treasury may follow | CL2025-8 |
| Status of the core | DBM and BTr use BTMS. Five more pilot agencies prepare in 2026. Plan: about 110 to 115 agencies in 2027 and 198 in 2028, 315 in total. A speech of the Secretary of Budget and Management of January 2026 gives other dates and numbers (section 7.3) | INQ-BTMS, SFA6, DBM-SPEECH26 |
| The IFMIS in the procurement rules | The rules of the procurement law say that the electronic and uniform payment system for procuring entities and suppliers "shall be defined in the context of the Integrated Financial Management Information System to be developed by the DBM, COA, and Department of Finance". This sentence names three developers. It does not name BTr, which is a member of the PFM Committee | IRR12009 s.21, EO29 |
| Common rules still to be made | Review and update of UACS in 2026 and 2027, with changes to the systems in 2027 and 2028. One PFM data model, a metadata registry, data governance, a framework of system controls | SFA6 |
| New systems planned | A project monitoring and reporting system (IPMRS), a human resources and payroll system (NGHRPS), a payment platform (eGovPay), a unified portal | SFA6 |
| Portal for the public | The COMPASS portal of DBM is in use since 26 June 2026. It combines the proposed budget, the budget law, allotments, obligations and disbursements. Executive Order No. 126 of 28 September 2026 makes it the platform of the government for budget and expenditure disclosures. According to the press release of DBM, the order says that the portal must be able to interface with existing systems, and it names the IFMIS, BTMS, PhilGEPS and DIME (section 11) | COMPASS-LAUNCH, EO126 |

## 4. Authorities and governance of the systems

| Body | Role | Basis |
|---|---|---|
| PFM Committee | Steers PFM reform and the IFMIS. Members: DBM, DOF, COA, BTr. The Roadmap names the DBM Secretary, the Secretary of Finance and the COA Chairperson as principals, and DICT and NEDA (now DEPDev) as resource institutions | EO29, ROADMAP2024 |
| DBM | Owns BTMS, OSBPS, GMIS, ADRS, URS, the COMPASS portal and the document verification record. Operates the BTMS project management office. Issues the rollout schedule | CL2025-8, NBM156, GMIS, ADRS, NBC599, COMPASS-LAUNCH, DBM-BLOCKCHAIN |
| COMPASS Council | Created by Executive Order No. 126 of 2026 for the public portal. Chair: DBM. Co-chair: DICT. Members: DOF and DILG. It approves the policies and the data standards of the portal and monitors compliance | EO126 |
| Central Project Management Group | Part of the governance of the BTMS project, together with the PFM Committee and the DBM project management office. I did not record its tasks | CL2025-8 |
| Each agency in the rollout | Forms a project implementation team, prepares a matrix of who may do what in the system, and migrates its data | CL2025-8 |
| COA | Owns eNGAS, the eBudget for agencies, and the AFR System | COA-GAS |
| BTr | Owns eTRAMS, NGCDS, NRoSS and the National Asset Registry System | BTR-SYS |
| DEPDev | Owns PIPOL | PIP-MEMO |
| PS-DBM | Operates PhilGEPS, with a Virtual Store and an eMarketplace for common-use supplies and equipment. Since October 2025 it publishes the registry of the beneficial owners of bidders through PhilGEPS, on an interim authority of the GPPB | RA12009 s.20, PS-FAQ, GPPB2025-11 |
| Technical Support Office of the GPPB | Receives the procurement plans and the procurement monitoring reports of all procuring entities, since 2026 through an online form | GPPB-TSO2026-2 |
| BIR, BOC | Own the filing, payment and customs systems. The customs system in use is named E2M | BIR-PAY, BOC-MOD |
| Servicing banks | Own the payment facilities, for example the eMDS of LBP | eMDS |
| BLGF | Owns eSRE | eSRE |
| DICT | Gives technical and policy support to the IFMIS. Leads the planned eGovPay platform with the working group on digital payments. Co-chairs the COMPASS Council and sets the standards of the portal for interoperability, cybersecurity and data management. Operates the national public key infrastructure (PNPKI). Built TradeNet | EO29, SFA6, EO126, PNPKI, TRADENET |
| DOF | Its Secretary chairs the steering committee of the National Single Window, whose platform is TradeNet. Member of the COMPASS Council | TRADENET, EO126 |

## 5. Systems by PFM function, today and planned

Diagram 16a shows this table as a picture. The right column is a plan, not a fact.

| No. | Function | System in use and its owner | Plan | Basis |
|---|---|---|---|---|
| 1 | Investment program | PIPOL (DEPDev) | An integrated planning and budgeting tool for the investment program, with a pilot in 2026 and 2027. A new project monitoring and reporting system (IPMRS). PIPOL and DIME will be assessed for fit. A working group of the planning department and DBM was created to link PIPOL and OSBPS | PIP-MEMO, SFA1, SFA6, ROADMAP2024 |
| 2 | Budget proposals and the proposed budget | OSBPS version 2.0 and BPMS (DBM) | Kept, and connected to the core through interfaces. This is my reading of the general statement in the Roadmap | NBM156, ROADMAP2024 |
| 3 | Positions and the personnel budget | GMIS with PSIPOP (DBM) | One human resources and payroll system (NGHRPS) | GMIS, SFA6 |
| 4 | Appropriations and release documents | e-Budget of DBM, and ADRS | Budget management module of BTMS at a later stage. This is my reading | ROADMAP2024, ADRS, CL2025-8 |
| 5 | Procurement notices and awards | PhilGEPS (PS-DBM), with a Virtual Store and an eMarketplace for common-use items. In September 2025 two versions of the portal existed, and 69 agencies used at least four modules of the electronic bidding facility of the modernized one. The earlier version takes no new posting from 1 March 2026 | Interface between PhilGEPS and BTMS. The rules also require a payment feature of PhilGEPS that can interface with the bank of the procuring entity | RA12009 s.20, IRR12009 s.20, PS-FAQ, CL2025-8, GPPB2025-09 |
| 6 | Obligations | A registry in each agency: paper, spreadsheet, or the eBudget of COA | BTMS: commitment and obligations management | COA-GAS, CL2025-8 |
| 7 | Payment orders | LDDAP-ADA or check to the servicing bank, on paper copies or through the facility of the bank, such as eMDS | BTMS: payments management, by electronic transfer or check | CL2013-16A, GAM-V1 Ch.6 s.56, s.58, eMDS, CL2025-8 |
| 8 | Receipts of agencies | Official receipts and agency records. Collection reports of depository banks in NGCDS (BTr) | BTMS: receipt management. A common payment platform (eGovPay) | BTR-SYS, CL2025-8, SFA6 |
| 9 | Property | Records in each agency. National Asset Registry System (BTr) | BTMS: property, plant and equipment management | BTR-SYS, CL2025-8 |
| 10 | Accounting | eNGAS of COA, other software or spreadsheets, in each agency | BTMS: accounting and financial reporting | COA-GAS, CL2025-8 |
| 11 | Plans and accountability reports | URS (DBM). Statements to COA through the AFR System | Reports produced from BTMS data. URS stays until agencies migrate | NBC599, JC2019-1, COA-GAS, GAA2026-GP |
| 12 | Cash, collections, debt | eTRAMS, NGCDS, NRoSS and the accounting systems of BTr | Treasury modules of BTMS at a later stage | BTR-SYS, CL2025-8 |
| 13 | Tax and customs | eFPS, eBIRForms and payment gateways (BIR). The E2M customs system (BOC) and Payment Application Secure | The receipts side is connected through interfaces. This is my reading. BOC plans a Customs Processing System that is based on E2M | BIR-PAY, PAS, BOC-MOD |
| 14 | Payroll | A separate system in each agency | NGHRPS | GK, SFA6 |
| 15 | Project monitoring | DIME (DBM) and agency systems | IPMRS, with a pilot in 2028 | ROADMAP-MID, SFA6 |
| 16 | Local governments | Own systems. Reports to BLGF in eSRE | A separate systems hub for local governments | eSRE, ROADMAP2024 |
| 17 | Common to all rows | UACS codes. Content passed by reports, by paper copies and by a second entry. Controls by signatures on the forms of the Manual. Off-budget funds only in periodic reports | Integration and data architecture, review of UACS, off-budget accounts into BTMS or URS, a unified portal. A portal for the public, COMPASS, is in use since June 2026 (section 11) | JC2017-1, GAM-V2, ROADMAP2024, SFA6, COMPASS-LAUNCH |

### 5.1 Two services of the whole government that are related to the PFM systems

Two systems hold no budget, payment or accounting record, and for that reason they have no row in the table. One of them concerns the permits that an importer needs before a customs declaration. The other concerns electronic signatures.

| System | Owner | What it does | Relation to PFM | Basis |
|---|---|---|---|---|
| TradeNet | DOF coordinates the agencies that join. DICT built the platform | It is the platform of the National Single Window. An importer or exporter applies there for the permits of the regulating agencies. The steering committee adopted it in 2017. The aim at that time was 66 agencies and 10 economic zones, and a connection to the single window of the ASEAN countries | The permits come before the goods declaration at BOC (chapter 10). A link between TradeNet and the customs system, and the present state of TradeNet, are not verified | TRADENET. Order of the steps: GK |
| PNPKI, Philippine National Public Key Infrastructure | DICT | It issues digital certificates. With a certificate a person or an office proves its identity and signs a file electronically | An electronic signature can replace a signature on paper on a PFM document. Whether the documents of DBM, of BTMS or of the banks are signed with these certificates is not verified | PNPKI. Use for PFM documents: not found |

## 6. What passes between systems and bodies today, and by which carrier

Diagrams 16b (spending side) and 16g (revenue and treasury side) show the systems inside their owner institutions, with what passes between them. Diagram 08a shows what passes between the units of one agency. The tables below list the same flows. They are produced from the register in Reference B, section 4, which has two more columns for each flow: the control that compares both sides, and the basis.

One word for each flow, such as "Electronic", would mix three different questions. The tables answer them one by one.

- **Kind**: what passes. Data, a document, an authority (a document that gives a right or sets a limit), or money.
- **Carrier**: how it passes. "System to system" means that one program sends to another and no person copies the content. "Entry by the sender" means that a person of the sending body enters or uploads the content in a system of the receiver. "Entry in own system" means that staff enter it in a record or system of their own body. "Paper" means signed paper copies. "Electronic, kind not stated" means that a source describes an electronic channel and does not say of which kind.
- **Stage of use**: whether a source describes the flow as existing today, as existing for a part of the agencies, as required or described without a confirmation of use, or as planned.

"Not stated" never means "absent". It means that the sources that I read do not say.

A case where the difference matters: an agency sends its budget forms to DBM through OSBPS. A source describes this as an online submission [NBM156]. That is an electronic flow, and it is also a second entry by a person: the staff of the agency type or upload the figures that they hold in their own files. The carrier "Entry by the sender" says both things. The one word "Electronic" hid the second.

### 6.1 Spending side

{{register:spending}}

Rows 17 and 32 are two carriers of the same documents. The Manual of 2015 describes five paper copies of each payment order and four of its summary list, and it describes the electronic facility of the Land Bank as a mode for the agencies with sub-accounts at that bank [GAM-V1 Ch.6 s.56, s.58]. I read no figure on how many agencies use each carrier today.

For row 2 the sources do not say that no interface exists. They state that no standard project identifier exists, that the two platforms lack interoperability, that many proposals are still submitted on paper or in spreadsheet files, that a working group of the planning department and DBM was created to link the two systems, and that an integrated tool is planned [SFA1][ROADMAP2024]. They do not state how the content of an entry in PIPOL reaches a budget form today.

Row 41: since 2026 a procuring entity sends its procurement plan and its monitoring report to the GPPB through an online form, and no longer by email [GPPB-TSO2026-2]. The form of the plan names the source of funds in words and has no budget code (chapter 17, section 6). The body that receives the plans of all entities therefore cannot match their lines with budget lines by a number (Inference).

On row 13: a resolution of the GPPB gives the state of PhilGEPS in September 2025. Two versions existed, the earlier one was to close in steps until the first semester of 2026, and 69 agencies used the electronic bidding facility of the modernized one [GPPB2025-09]. On row 39: in the Electronic Marketplace of PhilGEPS an entity pays through an eWallet, a Government Purchase Card or another electronic mode, and the Procurement Service pays the merchant after the entity accepts the goods [GPPB2025-10]. Chapter 06, section 9, gives both in detail.

### 6.2 Revenue and treasury side

{{register:revenue}}

The sources say that eTRAMS monitors the revenue collections and the disbursements of the national government [BTR-SYS]. They do not say who sends the data on tax and customs collections to it, and they do not say into which BTr system the reports FAR 3, 4 and 5 go. They also do not say which system supplies the figures of the COMPASS portal, and how often these figures are updated [COMPASS-LAUNCH].

### 6.3 Inside one agency

{{register:inside}}

These flows pass between the budget unit, the accounting unit, the cash unit and the property unit of the same agency. The Manual prescribes them as paper copies of forms. Where the units keep their records in different systems, each flow is a point where the same figure is written a second time. In an agency that uses BTMS these records are entries in one system (section 7).

### 6.4 What the register shows

The counts are in Reference B, section 4.4. Four observations follow from them, and each is a statement about the sources, not a measurement of the systems.

1. For few flows a source describes a program that sends to another program. Most of these are planned, required or limited to the agencies on BTMS.
2. The most frequent carrier that the sources describe is an entry or upload by a person of the sending body in a system of the receiver. For the receiver the flow is electronic. For the sender it is a second entry.
3. Around the payment itself, the Manual of 2015 prescribes paper: the payment order and its summary list to the bank, a copy from the bank to BTr, the validated copy back to the agency, the monthly bank statement, and the paid vouchers to the auditor.
4. For about one flow in four, the sources that I read do not state the carrier. Among them are the Notice of Cash Allocation from DBM to the bank and the reports of the banks to BTr.

## 7. BTMS, the core

Diagram 16c shows the records of the Budget Execution Module and the links between them.

### 7.1 Scope and functions

BTMS starts where the agency receives its allotment and its NCA, and ends at the disbursement [BTMS-SITE]. The circular of 2025 makes it the primary system for the expenditure transactions of all national agencies that have appropriations in the budget law, in a phased rollout, and says that all payments are recorded in it: personnel services, operating expenses, capital outlays and financial expenses [CL2025-8].

| Function | Records | Basis |
|---|---|---|
| 1. Commitment and obligations management | Purchase request, commitment, purchase order, obligation request. An obligation request is made manually, from a commitment, or from an approved purchase order | CL2025-8, BTMS-SITE |
| 2. Payments management | Goods received note, goods return note, disbursement voucher, payment by electronic funds transfer (PESONet, InstaPay) or by check, payment extract, bank reconciliation | CL2025-8, BTMS-SITE |
| 3. Receipt management | Revenue voucher, revenue receipt voucher | CL2025-8, BTMS-SITE |
| 4. Property, plant and equipment management | Register of assets and asset transactions | CL2025-8, BTMS-SITE |
| 5. Accounting and financial reporting | Journal entry voucher, ledgers, and the reports FAR 1 to 6, BAR 1, the registry of allotments and the NCA listings | CL2025-8, BTMS-SITE |
| Changes to allotments | Modification Advice Form, Advice for use of PS Allotment | CL2025-8 |

### 7.2 Rules that the system enforces

| Rule | How it is enforced outside BTMS | How BTMS enforces it | Basis |
|---|---|---|---|
| No obligation above the allotment | The budget unit checks the allotment in its registry, and its head signs Box B of the obligation request | The system blocks commitments and obligations above the allotment | GAM-V1 Ch.3 s.15, GAM-V2 App.11, BTMS-SITE |
| No payment above the cash authority | The head of accounting reads the registry of the NCA and certifies "Cash available" in Box C of the voucher. The bank checks the NCA balance | The system enforces the limits of the cash allocation and of the bank balance | GAM-V1 Ch.6 s.12, GAM-V2 App.32, BTMS-SITE. Bank check: GK |
| A voucher belongs to an obligation | The number of the obligation request is written on the voucher and on each line of the payment order | The voucher is linked to an approved obligation request | GAM-V2 App.32, App.42, BTMS-SITE |
| Payment only for what was ordered and received | The original acceptance report is attached to the voucher on paper | The voucher is matched with the purchase order and the goods received note | GAM-V1 Ch.8 s.15, BTMS-SITE |
| The books agree with the bank | Bank reconciliation statement each month, by the chief accountant. The 2025 assessment rates the practice partial | Automatic reconciliation each day from electronic bank statements | GAM-V1 Ch.21 s.4, PEFA2025, BTMS-SITE |
| Every transaction reaches the books | Accounting staff prepare a journal entry voucher and enter it in eNGAS or other software | The system creates the journal entry from the voucher, the revenue vouchers and the asset transactions. Entries at the end of a period are made manually | GAM-V2 App.36, COA-GAS, BTMS-SITE |
| DBM, COA and BTr receive the same reports | Agencies enter data in URS. Only reports generated by URS are accepted | Reports are produced from the records of BTMS | JC2019-1, CL2025-8 |

What the system cannot check: whether the goods received note is true. That fact is still stated by a person (chapter 07).

### 7.3 Status in October 2026

| Fact | Basis |
|---|---|
| BTMS was first adopted for budget execution by DBM Circular Letter No. 2019-4, and was later revived | CL2025-8 |
| The present system was launched in May 2025. From its first transactions on 17 December 2025 to the end of that year it processed about PHP 4.25 billion | INQ-BTMS |
| Seven pilot agencies were identified for 2026. Two of them, DBM and BTr, already use the system. Five prepare | INQ-BTMS |
| Plan: 110 agencies in 2027 and 198 in 2028, 315 in total. The action plan counts 2, then 115, then 198 | INQ-BTMS, SFA6 |
| A third source disagrees with the two rows above. In a speech of 22 January 2026 the Secretary of Budget and Management said: "We launched its interoperable core, the Budget and Treasury Management System (BTMS), in 2024 and even piloted it with seven agencies in 2025." The speech also says that the system is expanded to 155 national agencies in 2026. The atlas states the three sources and does not decide between them. Where a diagram or the register must show one state, it shows the account of the two rows above, because two sources agree on it and it is the more detailed one | DBM-SPEECH26 |
| Target share of the budget executed through BTMS: 50 percent, then 80 percent | SFA6 |
| A third-party audit and certification of BTMS is planned for 2026 and 2027 | SFA6 |
| Until an agency migrates, its reports are submitted through URS or other electronic means | GAA2026-GP |
| Interfaces are foreseen with procurement, document management, electronic funds transfer and financial systems. Which of them are in use: not verified | CL2025-8 |
| The order on the COMPASS portal of September 2026 names BTMS among the systems with which the portal must be able to interface | EO126 |

## 8. The planned IFMIS

Diagram 16d shows the plan in layers.

| Layer | Content | State | Basis |
|---|---|---|---|
| Who decides | PFM Committee. BTMS project management office in DBM, central project management group, a team in each agency | Exists | EO29, CL2025-8 |
| Common rules for all connected systems | UACS, reviewed and updated. One PFM data model and a metadata registry. Interface standards and data governance. A framework of system controls | Planned for 2026 to 2028 | SFA6 |
| Core | BTMS, Budget Execution Module | In use, in phased rollout | CL2025-8, INQ-BTMS |
| Core, later | Budget management module and treasury modules | Planned | CL2025-8 |
| Interface layer | Each connected system keeps its functions and exchanges agreed records with the core | Planned | ROADMAP2024, SFA6 |
| National systems to be connected | The Roadmap figure names ADRS, BPMS, BTMS, DIME, eBudget, eNGAS, NGCDS, OSBPS, the Treasury Single Account and URS. The circular adds procurement, document management and electronic funds transfer | Named | ROADMAP2024, CL2025-8 |
| New systems | IPMRS: concept in 2026, procurement in 2026 and 2027, development in 2027 and 2028, pilot in 2028. NGHRPS. eGovPay platform: assessment in 2026, phased rollout to 2028. Unified portal and mobile applications | Planned | SFA6 |
| Portal for the public | COMPASS. The action plan names a unified portal and mobile applications. The sources that I read do not say that COMPASS is that planned portal. Diagrams 16a and 16d place it there, and this is my reading | In use since June 2026 | COMPASS-LAUNCH, EO126, SFA6 |
| Hub for local governments | The Roadmap figure names eBudget, eCAT, ePFMAT, National Tax Allotment and the National Wealth Portal | Named. Functions of eCAT and ePFMAT are not explained | ROADMAP2024 |
| Off-budget accounts | Into BTMS, or into URS if that is not feasible. Feasibility report in the fourth quarter of 2026, pilot in 2028 | Planned | SFA6 |

The sources do not give a plan that replaces each present system by a named successor. The statement is general: agencies keep their systems and connect them.

## 9. Main events, 2011 to 2028

Diagram 16e shows these events on a time line.

| Year | Event | Basis |
|---|---|---|
| 2011 | Executive Order No. 55: GIFMIS and the Treasury Single Account | EO55 |
| 2013 to 2014 | Payment of suppliers by bank credit through the LDDAP-ADA, in full use from 1 March 2014. UACS starts as the single coding structure | CL2013-16A. Start year of UACS: GK |
| 2015 | A joint order of DBM and DOF adopts eMDS as one of the modes of disbursement. COA prescribes the Government Accounting Manual, in force from 1 January 2016 | GAM-V1 Ch.6 s.58, COA2015-007 |
| 2017 | UACS revised with the program classification | JC2017-1 |
| 2019 | BTMS first adopted for budget execution. Cash budgeting starts | CL2025-8, EO91 |
| 2021 | ADRS in pilot from 1 October. NGCDS of BTr in use from May | ADRS, BTR-SYS |
| 2022 | Execution plans and reports through URS. Order on digital payments | NBC599 (which cites the circular letters), BTR-SITE |
| 2023 | Executive Order No. 29 on the IFMIS | EO29 |
| 2024 | New procurement law. PFM Reforms Roadmap 2024 to 2028 | RA12009, ROADMAP2024 |
| 2025 | Rules of the procurement law in effect on 25 February. BTMS launched in May. Release documents can be verified against a blockchain record from 30 July. Circular on BTMS on 28 August. First BTMS transactions on 17 December. The Senate passes the CADENA bill on 15 December | GPPB-ADV, INQ-BTMS, DBM-BLOCKCHAIN, CL2025-8, CADENA-NEWS |
| 2026 | DBM and BTr use BTMS, five more pilot agencies prepare. Midterm update of the Roadmap, launched on 25 June. COMPASS portal for the public, launched on 26 June. Executive Order No. 126 on the portal, signed on 28 September. Review of UACS starts | INQ-BTMS, ROADMAP-MID, COMPASS-LAUNCH, EO126, SFA6 |
| 2027 (plan) | About 110 to 115 more agencies on BTMS. Interfaces and data standards introduced | INQ-BTMS, SFA6 |
| 2028 (plan) | 198 more agencies, 315 in total. Pilots of IPMRS and of off-budget accounts | INQ-BTMS, SFA6 |

## 10. Public verification of release documents

DBM has one application that uses a blockchain. Its purpose is narrow, and it is often described too broadly.

The steps are those of diagram 16f.

{{steps:16f|1-2=DBM-BLOCKCHAIN, ADRS;3=GK;4=ADRS, DBM-BLOCKCHAIN;5=GK;6=DBM-BLOCKCHAIN;7=GK;8-9=DBM-BLOCKCHAIN. Method: GK}}

| Question | Answer | Basis |
|---|---|---|
| What is it? | A blockchain application for the Action Document Releasing System, built with a private company. It is in operation since 30 July 2025 | DBM-BLOCKCHAIN |
| What does it record? | Release documents of DBM that pass through ADRS, such as a SARO or an advice of NCA | DBM-BLOCKCHAIN, ADRS |
| Who can check? | Any person, by the QR code on the document | DBM-BLOCKCHAIN |
| What does a successful check prove? | That DBM issued this document with this content | Follows from the design |
| What does it not prove? | That the release was correct, that the agency obligated or paid the amount, or that anything was delivered. Allotments, obligations and payments are recorded in the systems of sections 5 to 7, not in this record | Follows from the design |
| Which network and which form of record? | Not stated by DBM. Press reports that quote the company name a public network and one token for each document | DBM-BLOCKCHAIN (press reports) |

A related bill is in Congress, and a related order was signed in September 2026 (section 11). The Senate approved Senate Bill No. 1506, known as the CADENA Act, on third reading on 15 December 2025 with 17 votes in favour and none against. According to a press report of 5 October 2026, the House of Representatives has not passed it: the House version was referred to the Committee on Appropriations on 9 May 2026, and that committee has published no timetable [CADENA-NEWS]. I did not open the text of the bill. Press reports say that it would require budget documents and records to be published on a blockchain.

## 11. The COMPASS portal and Executive Order No. 126

The systems of sections 5 to 8 serve the institutions that run the budget. A portal for the public answers a different question: what can a person outside the government see, and who is responsible for the figure that is shown?

DBM launched the COMPASS portal on 26 June 2026. The name is short for Centralized Open Monitoring Platform for Appropriations and Spending Statistics. On 28 September 2026, Executive Order No. 126 made the portal the platform of the government for budget and expenditure disclosures. I could not find the text of the order. The table uses six documents: four releases of DBM and of the Philippine Information Agency, and two press reports. Reference F lists them under the codes COMPASS-LAUNCH and EO126. The quotations are from these documents, and they are not checked against the order.

| Subject | What the sources say | Basis |
|---|---|---|
| Content at the launch | The proposed budget (NEP), the budget law (GAA), allotments, obligations and disbursements in one portal with a search function. A user can follow spending "by department, agency, funding purpose, and fiscal year" | COMPASS-LAUNCH |
| Content that the order requires | Financial and program performance, the implementation and completion status of projects, procurement information, and other transparency information of the budget cycle. Projects with private partners and projects with foreign assistance are included as far as they use public funds | EO126 |
| Who must submit | All national government agencies and instrumentalities, including government corporations and government financial institutions. They must "submit, regularly update, disclose and publish relevant information through COMPASS". Local governments are encouraged to participate. They are not required | EO126 |
| Who is responsible for the figures | Each covered agency is responsible "for the accuracy, completeness, and timeliness of the information it submits" | EO126 |
| Links to other systems | The portal must be "capable of interfacing with existing government systems". The press release of DBM names the IFMIS, BTMS, PhilGEPS, DIME and the eGovPH application. The council must ensure that the portal is integrated with the financial systems of DBM, COA, DOF and other oversight bodies | EO126 |
| Technology | The portal "may utilize distributed ledger technology, including blockchain or other emerging technologies". This is a permission. It is not a duty | EO126 |
| Who decides | The COMPASS Council: DBM as chair, DICT as co-chair, DOF and DILG as members. It approves policies and data standards, monitors compliance and meets at least once in each quarter. DBM operates the portal and has custody of the data. DICT sets the standards for interoperability, cybersecurity and data management | EO126 |
| Exceptions | Information that a law forbids to publish, information on national defense and security, and personal data that the Data Privacy Act protects. For each item that an agency withholds or redacts, it publishes a log with the legal basis, the approving authority and the date | EO126 |
| Sanctions and money | Non-compliance may be a ground for administrative and disciplinary sanctions. The first costs are charged to the current appropriations of DBM, DICT and other agencies | EO126 |
| Not stated in the documents that I read | The date on which the order takes effect, deadlines for the agencies, the system that supplies the figures of the portal today, how often the figures are updated, and the section numbers of the order | Not found in COMPASS-LAUNCH and EO126 |

A case where the portal answers a question. A person wants to know how much of the budget of one department was released and how much was obligated. Before June 2026 the person had to open several reports of DBM and of the agency. The portal shows these amounts in one place.

A case where the portal does not answer the question. A person wants to know whether a road that is shown as completed exists. The portal shows what the agency submitted. The order makes the agency responsible for the accuracy of that information, and the documents that I read describe no check by another body before publication [EO126]. The check of a delivery remains what chapter 07 describes: inspection and acceptance by the agency, and later the audit by COA.

Three things are similar to the portal and are not the same thing.

| Thing | What it is | Difference from the COMPASS portal | Basis |
|---|---|---|---|
| The blockchain record of section 10 | A record of each release document that DBM issued | It lets a person check that one copy of a document is authentic. It publishes no totals. The portal publishes amounts and gives no proof for a single document | DBM-BLOCKCHAIN, COMPASS-LAUNCH |
| The CADENA bill | A bill that, according to press reports, would require the publication of budget records on a blockchain | The bill would make a distributed ledger a duty by law. The order permits this technology and does not require it. The bill is not law | CADENA-NEWS, EO126 |
| The unified portal of the action plan | A planned portal with mobile applications | The sources that I read do not say that COMPASS is this planned portal | SFA6 |

The permission to use a distributed ledger does not change what a published figure proves. A ledger of this kind can show that a record was not changed after it was written. It cannot show that the record was true when it was written.

## 12. What the assessments report

| Finding | Basis |
|---|---|
| Three gaps of the present systems: the same report is prepared more than once, processing is manual, and the systems are not integrated | ROADMAP2024 |
| No single system follows a proposal from the investment program to the budget. A working group was created to link PIPOL and OSBPS | ROADMAP2024 |
| No standard project identifier exists. The planning and the budgeting platforms lack interoperability. Many proposals and reports are still submitted on paper or in spreadsheet files | SFA1 |
| Classification codes are not consistent across PFM systems | SFA6 |
| The accuracy of quarterly reports is rated C because manual processes remain (PEFA indicator 28.3). Coverage of reports through URS is rated B (indicator 28.1) | PEFA2025 |
| Bank reconciliation is partial (PEFA indicator 27.1, score C) | PEFA2025 |
| The national asset registry is not yet in full use (PEFA indicator 12.2, score C) | PEFA2025 |
| DBM operates a central personnel information system and payroll is reconciled monthly (PEFA indicator 23.1, score B) | PEFA2025 |

## 13. Diagrams

{{mermaid:16a}}

{{plantuml:16b}}

{{plantuml:16g}}

{{mermaid:16c}}

{{mermaid:16d}}

{{mermaid:16e}}

{{mermaid:16f}}

## 14. Verification status

- **Verified in a source:** Executive Orders No. 55 and No. 29 [EO55][EO29]. The functions, transactions, reports, governance and interfaces of BTMS [CL2025-8]. The scope and the system checks of BTMS [BTMS-SITE]. The status and the targets [INQ-BTMS][SFA6]. The systems by function, the gaps and the design of the IFMIS [ROADMAP2024]. The planned systems and standards [SFA6][SFA1]. The flows of section 6, each from the source named in its row of the register in Reference B. The paper flows between the agency, the bank, BTr and the auditor, and the flows between the units of one agency [GAM-V1 Ch.3, Ch.5, Ch.6, Ch.21]. The place of the IFMIS and of PhilGEPS in the procurement rules [IRR12009 ss.20-23]. The document verification application [DBM-BLOCKCHAIN]. The state of the CADENA bill [CADENA-NEWS]. The COMPASS portal and Executive Order No. 126, read in four official releases and two press reports and not in the text of the order [COMPASS-LAUNCH][EO126]. The name of the customs system in use and the plan of a new one [BOC-MOD]. The facilities of the modernized PhilGEPS for common-use items [PS-FAQ]. The state of PhilGEPS in September 2025, the modes of payment in its Electronic Marketplace, the registry of beneficial owners and the submission of procurement plans to the GPPB, each read as a summary on 12 October 2026 [GPPB2025-09][GPPB2025-10][GPPB2025-11][GPPB-TSO2026-2]. TradeNet as adopted in 2017 [TRADENET]. The public key infrastructure of DICT [PNPKI].
- **Sources that disagree:** the dates and numbers of the BTMS rollout [INQ-BTMS][SFA6][DBM-SPEECH26].
- **My reading, not stated in a source:** the plans in rows 2, 4 and 13 of section 5. The four observations of section 6.4. The statements on what a blockchain record proves and does not prove. The place of the COMPASS portal in the box of the planned unified portal in diagrams 16a and 16d. The statement that the portal publishes what agencies submit without a check by another body: the documents that I read describe no such check, and the order itself may contain one.
- **General knowledge, to check:** what BPMS and the e-Budget of DBM do, the flows between OSBPS, BPMS, the e-Budget and ADRS, what the customs system does, the order of permits and customs declaration, bank reports to BIR, payroll systems of agencies, the usual method of a blockchain record (a hash of the document).
- **Not found in the sources I read:** how the content of PIPOL reaches the budget proposal today, how many agencies send payment orders on paper and how many through a bank facility, the channel by which an NCA reaches the bank, the sender of collection data to eTRAMS, the BTr system that receives FAR 3, 4 and 5, the functions of PMIS, "BTr NGAS", the "Online Cash Planning Reporting System", eCAT and ePFMAT, the internal data model of BTMS, the interfaces of BTMS that are already in use, the network and record format of the document verification application, the text of Executive Order No. 126 and its date of effect, the system that supplies the figures of the COMPASS portal and the frequency of its updates, the present state of TradeNet and of the planned Customs Processing System, the use of PNPKI certificates on PFM documents, the features of PhilGEPS that are in use in October 2026, and how an entity deposits money in the eWallet of the Electronic Marketplace.
